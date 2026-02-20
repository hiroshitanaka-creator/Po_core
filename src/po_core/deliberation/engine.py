"""
Deliberation Engine
====================

Multi-round philosopher dialogue for emergent reasoning.

Design (from PHASE_PLAN_v2.md):
  Round 1: All philosophers propose() independently.
  Round 2: InteractionMatrix identifies high-interference pairs.
           Those pairs receive counterarguments and re-propose.

When max_rounds=1, produces identical behavior to the current pipeline
(backward compatible — no deliberation, just pass-through).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from po_core.deliberation.emergence import EmergenceDetector, EmergenceSignal
from po_core.deliberation.influence import InfluenceTracker, InfluenceWeight
from po_core.domain.context import Context as DomainContext
from po_core.domain.intent import Intent
from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.tensors.interaction_tensor import InteractionMatrix, InteractionPair


@dataclass
class RoundTrace:
    """Record of a single deliberation round."""

    round_number: int
    n_proposals: int
    n_revised: int
    interaction_summary: Optional[Dict] = None


@dataclass
class DeliberationResult:
    """Result of multi-round deliberation."""

    proposals: List[Proposal]
    rounds: List[RoundTrace]
    interaction_matrix: Optional[InteractionMatrix] = None
    emergence_signals: List[EmergenceSignal] = field(default_factory=list)
    influence_weights: Dict[str, InfluenceWeight] = field(default_factory=dict)

    @property
    def n_rounds(self) -> int:
        return len(self.rounds)

    @property
    def total_proposals(self) -> int:
        return len(self.proposals)

    @property
    def has_emergence(self) -> bool:
        """True if any emergence signal was detected."""
        return bool(self.emergence_signals)

    @property
    def peak_novelty(self) -> float:
        """Highest novelty score across all emergence signals (0.0 if none)."""
        if not self.emergence_signals:
            return 0.0
        return max(s.novelty_score for s in self.emergence_signals)

    def summary(self) -> Dict:
        top_influencers = sorted(
            [(n, w.total_influence()) for n, w in self.influence_weights.items()],
            key=lambda x: x[1],
            reverse=True,
        )[:3]
        return {
            "n_rounds": self.n_rounds,
            "total_proposals": self.total_proposals,
            "rounds": [
                {
                    "round": r.round_number,
                    "n_proposals": r.n_proposals,
                    "n_revised": r.n_revised,
                }
                for r in self.rounds
            ],
            "interaction_summary": (
                self.interaction_matrix.summary() if self.interaction_matrix else None
            ),
            "emergence": {
                "detected": self.has_emergence,
                "n_signals": len(self.emergence_signals),
                "peak_novelty": round(self.peak_novelty, 4),
            },
            "top_influencers": [
                {"philosopher": n, "influence": round(s, 4)} for n, s in top_influencers
            ],
        }


class DeliberationEngine:
    """
    Multi-round philosopher deliberation engine.

    Args:
        max_rounds: Maximum number of deliberation rounds (1 = no deliberation).
        top_k_pairs: Number of high-interference pairs to select for re-proposal.
        convergence_threshold: Stop if mean proposal change falls below this.
    """

    def __init__(
        self,
        max_rounds: int = 2,
        top_k_pairs: int = 5,
        convergence_threshold: float = 0.1,
        detect_emergence: bool = True,
        emergence_threshold: float = 0.65,
        track_influence: bool = True,
    ):
        self.max_rounds = max(1, max_rounds)
        self.top_k_pairs = top_k_pairs
        self.convergence_threshold = convergence_threshold
        self._emergence_detector = (
            EmergenceDetector(threshold=emergence_threshold)
            if detect_emergence
            else None
        )
        self._influence_tracker = InfluenceTracker() if track_influence else None

    def deliberate(
        self,
        philosophers: Sequence,
        ctx: DomainContext,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
        round1_proposals: List[Proposal],
    ) -> DeliberationResult:
        """
        Run multi-round deliberation starting from round 1 proposals.

        Args:
            philosophers: Loaded philosopher instances (from registry.load())
            ctx: Request context
            intent: Computed intent
            tensors: Computed tensor snapshot
            memory: Memory snapshot
            round1_proposals: Proposals from round 1 (PartyMachine output)

        Returns:
            DeliberationResult with final proposals and round traces
        """
        rounds: List[RoundTrace] = []
        all_emergence: List[EmergenceSignal] = []
        current_proposals = list(round1_proposals)
        baseline_proposals = list(round1_proposals)  # Round 1 = baseline

        # Round 1 trace (already computed externally)
        rounds.append(
            RoundTrace(
                round_number=1,
                n_proposals=len(current_proposals),
                n_revised=0,
            )
        )

        # Seed influence tracker with round-1 baselines
        if self._influence_tracker is not None:
            self._influence_tracker.reset()
            self._influence_tracker.set_baseline(baseline_proposals)

        if self.max_rounds <= 1 or len(current_proposals) < 2:
            return DeliberationResult(
                proposals=current_proposals,
                rounds=rounds,
                interaction_matrix=None,
            )

        # Build philosopher lookup by name
        ph_lookup = _build_philosopher_lookup(philosophers)

        # Rounds 2..max_rounds
        interaction_matrix = None
        for round_num in range(2, self.max_rounds + 1):
            # Compute interaction matrix from current proposals
            interaction_matrix = InteractionMatrix.from_proposals(current_proposals)

            # Select high-interference pairs
            hi_pairs = interaction_matrix.high_interference_pairs(
                top_k=self.top_k_pairs
            )

            if not hi_pairs:
                # No interference → no deliberation needed
                rounds.append(
                    RoundTrace(
                        round_number=round_num,
                        n_proposals=len(current_proposals),
                        n_revised=0,
                        interaction_summary=interaction_matrix.summary(),
                    )
                )
                break

            # Identify philosophers that need to re-propose
            # sender_map: {recipient_name → sender_name} for influence tracking
            revised_names: set = set()
            counterarguments: Dict[str, str] = {}
            sender_map: Dict[str, str] = {}
            for pair in hi_pairs:
                _collect_counterargument(
                    pair, current_proposals, counterarguments, revised_names, sender_map
                )

            # Re-propose for affected philosophers
            revised_proposals = _re_propose(
                ph_lookup, counterarguments, ctx, intent, tensors, memory
            )

            # Merge: replace old proposals with revised ones
            n_revised = len(revised_proposals)
            current_proposals = _merge_proposals(current_proposals, revised_proposals)

            # Emergence detection: compare revised proposals to round-1 baseline
            if self._emergence_detector is not None and revised_proposals:
                signals = self._emergence_detector.detect(
                    baseline_proposals, revised_proposals, round_num
                )
                all_emergence.extend(signals)

                # Strong emergence → stop deliberation, let this proposal win
                if self._emergence_detector.has_strong_emergence(signals):
                    rounds.append(
                        RoundTrace(
                            round_number=round_num,
                            n_proposals=len(current_proposals),
                            n_revised=n_revised,
                            interaction_summary=interaction_matrix.summary(),
                        )
                    )
                    break

            # Influence tracking
            if self._influence_tracker is not None and revised_proposals:
                self._influence_tracker.update(revised_proposals, sender_map)

            rounds.append(
                RoundTrace(
                    round_number=round_num,
                    n_proposals=len(current_proposals),
                    n_revised=n_revised,
                    interaction_summary=interaction_matrix.summary(),
                )
            )

        influence_weights = (
            self._influence_tracker.weights()
            if self._influence_tracker is not None
            else {}
        )

        return DeliberationResult(
            proposals=current_proposals,
            rounds=rounds,
            interaction_matrix=interaction_matrix,
            emergence_signals=all_emergence,
            influence_weights=influence_weights,
        )


# ── Internal helpers ─────────────────────────────────────────────────


def _build_philosopher_lookup(philosophers: Sequence) -> Dict[str, object]:
    """Build name → philosopher mapping."""
    lookup = {}
    for ph in philosophers:
        name = getattr(ph, "name", None) or str(ph)
        lookup[name] = ph
    return lookup


def _get_author(proposal: Proposal) -> str:
    """Extract author name from proposal.extra."""
    extra = proposal.extra if isinstance(proposal.extra, dict) else {}
    pc = extra.get(PO_CORE, {})
    return pc.get(AUTHOR, "") or extra.get("philosopher", "")


def _collect_counterargument(
    pair: InteractionPair,
    proposals: List[Proposal],
    counterarguments: Dict[str, str],
    revised_names: set,
    sender_map: Optional[Dict[str, str]] = None,
) -> None:
    """Collect counterarguments for both philosophers in a pair.

    Args:
        sender_map: If provided, also records {recipient → sender} for
                    downstream influence tracking.
    """
    # Find proposals by these philosophers
    a_content = ""
    b_content = ""
    for p in proposals:
        author = _get_author(p)
        if author == pair.philosopher_a:
            a_content = p.content
        elif author == pair.philosopher_b:
            b_content = p.content

    # Each receives the other's argument as counterpoint
    # Guard checks the RECIPIENT (not sender) to avoid overwriting
    if a_content and pair.philosopher_b not in counterarguments:
        counterarguments[pair.philosopher_b] = a_content
        revised_names.add(pair.philosopher_b)
        if sender_map is not None:
            sender_map[pair.philosopher_b] = pair.philosopher_a
    if b_content and pair.philosopher_a not in counterarguments:
        counterarguments[pair.philosopher_a] = b_content
        revised_names.add(pair.philosopher_a)
        if sender_map is not None:
            sender_map[pair.philosopher_a] = pair.philosopher_b


def _re_propose(
    ph_lookup: Dict[str, object],
    counterarguments: Dict[str, str],
    ctx: DomainContext,
    intent: Intent,
    tensors: TensorSnapshot,
    memory: MemorySnapshot,
) -> List[Proposal]:
    """Re-run propose() for philosophers with counterargument context."""
    revised = []
    for name, counter_text in counterarguments.items():
        ph = ph_lookup.get(name)
        if ph is None or not hasattr(ph, "propose"):
            continue

        # Build enriched context with counterargument
        enriched_ctx = DomainContext(
            request_id=ctx.request_id,
            user_input=(
                f"{ctx.user_input}\n\n"
                f"[Counterargument from a fellow philosopher: {counter_text[:500]}]"
            ),
            created_at=ctx.created_at,
        )

        try:
            new_proposals = ph.propose(enriched_ctx, intent, tensors, memory)
            if new_proposals:
                # Mark as deliberation round 2
                for p in new_proposals:
                    extra = dict(p.extra) if isinstance(p.extra, dict) else {}
                    extra["deliberation_round"] = 2
                    # Preserve PO_CORE author metadata for downstream scoring
                    if PO_CORE not in extra or AUTHOR not in extra.get(PO_CORE, {}):
                        po_meta = extra.get(PO_CORE, {})
                        if not isinstance(po_meta, dict):
                            po_meta = {}
                        po_meta[AUTHOR] = name
                        extra[PO_CORE] = po_meta
                    revised.append(
                        Proposal(
                            proposal_id=p.proposal_id.replace(":0", ":d2"),
                            action_type=p.action_type,
                            content=p.content,
                            confidence=min(p.confidence + 0.1, 1.0),
                            assumption_tags=list(p.assumption_tags),
                            risk_tags=list(p.risk_tags),
                            extra=extra,
                        )
                    )
        except Exception:
            # Philosopher failed in round 2 → keep original
            continue

    return revised


def _merge_proposals(
    original: List[Proposal], revised: List[Proposal]
) -> List[Proposal]:
    """
    Merge revised proposals into original set.

    Revised proposals REPLACE originals from the same philosopher.
    """
    # Build set of revised authors
    revised_authors = set()
    for p in revised:
        revised_authors.add(_get_author(p))

    # Keep originals whose author was NOT revised, plus all revised
    merged = [p for p in original if _get_author(p) not in revised_authors]
    merged.extend(revised)
    return merged
