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

Phase 6-B additions:
  dialectic_mode="dialectic" enables Hegelian 3-round structure:
    Round 1 (Thesis)     — all philosophers propose normally
    Round 2 (Antithesis) — high-interference pairs REFUTE each other
    Round 3 (Synthesis)  — Synthesizer philosophers integrate the debate
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from po_core.deliberation.clustering import ClusterResult, PositionClusterer
from po_core.deliberation.emergence import EmergenceDetector, EmergenceSignal
from po_core.deliberation.influence import InfluenceTracker, InfluenceWeight
from po_core.deliberation.roles import (
    SYNTHESIZER_PHILOSOPHERS,
    DebateRole,
    assign_role,
    get_role_prompt_prefix,
)
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
    role: str = DebateRole.STANDARD.value  # Phase 6-B: dialectic role for this round


@dataclass
class DeliberationResult:
    """Result of multi-round deliberation."""

    proposals: List[Proposal]
    rounds: List[RoundTrace]
    interaction_matrix: Optional[InteractionMatrix] = None
    emergence_signals: List[EmergenceSignal] = field(default_factory=list)
    influence_weights: Dict[str, InfluenceWeight] = field(default_factory=dict)
    cluster_result: Optional[ClusterResult] = None  # Phase 6-C1

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
                    "role": r.role,
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
            "clustering": (
                self.cluster_result.to_dict() if self.cluster_result else None
            ),
        }


class DeliberationEngine:
    """
    Multi-round philosopher deliberation engine.

    Args:
        max_rounds: Maximum number of deliberation rounds (1 = no deliberation).
        top_k_pairs: Number of high-interference pairs to select for re-proposal.
        convergence_threshold: Stop if mean proposal change falls below this.
        dialectic_mode: "standard" (default) or "dialectic" (Hegelian 3-round).
            In dialectic mode, max_rounds is forced to at least 3.
    """

    def __init__(
        self,
        max_rounds: int = 2,
        top_k_pairs: int = 5,
        convergence_threshold: float = 0.1,
        detect_emergence: bool = True,
        emergence_threshold: float = 0.65,
        track_influence: bool = True,
        prompt_mode: str = "debate",
        dialectic_mode: str = "standard",
        enable_clustering: bool = False,
        cluster_k_min: int = 2,
        cluster_k_max: int = 6,
    ):
        self.dialectic_mode = (
            dialectic_mode
            if dialectic_mode in ("standard", "dialectic")
            else "standard"
        )
        # Dialectic mode requires at least 3 rounds (Thesis, Antithesis, Synthesis)
        if self.dialectic_mode == "dialectic":
            max_rounds = max(max_rounds, 3)
        self.max_rounds = max(1, max_rounds)
        self.top_k_pairs = top_k_pairs
        self.convergence_threshold = convergence_threshold
        self.prompt_mode = (
            prompt_mode if prompt_mode in ("basic", "debate") else "debate"
        )
        self._emergence_detector = (
            EmergenceDetector(threshold=emergence_threshold)
            if detect_emergence
            else None
        )
        self._influence_tracker = InfluenceTracker() if track_influence else None
        self._clusterer = (
            PositionClusterer(k_min=cluster_k_min, k_max=cluster_k_max)
            if enable_clustering
            else None
        )

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
        is_dialectic = self.dialectic_mode == "dialectic"
        rounds: List[RoundTrace] = []
        all_emergence: List[EmergenceSignal] = []
        current_proposals = list(round1_proposals)
        baseline_proposals = list(round1_proposals)  # Round 1 = baseline

        # Round 1 trace (already computed externally)
        round1_role = assign_role(1, is_dialectic)
        rounds.append(
            RoundTrace(
                round_number=1,
                n_proposals=len(current_proposals),
                n_revised=0,
                role=round1_role.value,
            )
        )

        # Seed influence tracker with round-1 baselines
        if self._influence_tracker is not None:
            self._influence_tracker.reset()
            self._influence_tracker.set_baseline(baseline_proposals)

        # Phase 6-C1: cluster philosophers by position after round 1
        cluster_result: Optional[ClusterResult] = None
        if self._clusterer is not None and len(current_proposals) >= 2:
            _init_matrix = InteractionMatrix.from_proposals(current_proposals)
            cluster_result = self._clusterer.cluster(
                _init_matrix.harmony, _init_matrix.names
            )

        if self.max_rounds <= 1 or len(current_proposals) < 2:
            return DeliberationResult(
                proposals=current_proposals,
                rounds=rounds,
                interaction_matrix=None,
                cluster_result=cluster_result,
            )

        # Build philosopher lookup by name
        ph_lookup = _build_philosopher_lookup(philosophers)

        # Rounds 2..max_rounds
        interaction_matrix = None
        for round_num in range(2, self.max_rounds + 1):
            round_role = assign_role(round_num, is_dialectic)

            if is_dialectic and round_role == DebateRole.SYNTHESIS:
                # Synthesis round: Synthesizer philosophers integrate the full debate
                counterarguments = _collect_synthesis_counterarguments(
                    current_proposals, SYNTHESIZER_PHILOSOPHERS, ph_lookup
                )
                sender_map: Dict[str, str] = {
                    name: "the debate" for name in counterarguments
                }

                if not counterarguments:
                    rounds.append(
                        RoundTrace(
                            round_number=round_num,
                            n_proposals=len(current_proposals),
                            n_revised=0,
                            role=round_role.value,
                        )
                    )
                    break

                revised_proposals = _re_propose(
                    ph_lookup,
                    counterarguments,
                    ctx,
                    intent,
                    tensors,
                    memory,
                    round_num=round_num,
                    sender_map=sender_map,
                    prompt_mode=self.prompt_mode,
                    role=round_role,
                )

                n_revised = len(revised_proposals)
                current_proposals = _merge_proposals(
                    current_proposals, revised_proposals
                )

                rounds.append(
                    RoundTrace(
                        round_number=round_num,
                        n_proposals=len(current_proposals),
                        n_revised=n_revised,
                        role=round_role.value,
                    )
                )
                continue

            # Standard or Antithesis round: use high-interference pairs
            interaction_matrix = InteractionMatrix.from_proposals(current_proposals)
            hi_pairs = interaction_matrix.high_interference_pairs(
                top_k=self.top_k_pairs
            )

            if not hi_pairs:
                rounds.append(
                    RoundTrace(
                        round_number=round_num,
                        n_proposals=len(current_proposals),
                        n_revised=0,
                        interaction_summary=interaction_matrix.summary(),
                        role=round_role.value,
                    )
                )
                break

            revised_names: set = set()
            counterarguments = {}
            sender_map = {}
            for pair in hi_pairs:
                _collect_counterargument(
                    pair, current_proposals, counterarguments, revised_names, sender_map
                )

            revised_proposals = _re_propose(
                ph_lookup,
                counterarguments,
                ctx,
                intent,
                tensors,
                memory,
                round_num=round_num,
                sender_map=sender_map,
                prompt_mode=self.prompt_mode,
                role=round_role,
            )

            n_revised = len(revised_proposals)
            current_proposals = _merge_proposals(current_proposals, revised_proposals)

            if self._emergence_detector is not None and revised_proposals:
                signals = self._emergence_detector.detect(
                    baseline_proposals, revised_proposals, round_num
                )
                all_emergence.extend(signals)

                if self._emergence_detector.has_strong_emergence(signals):
                    rounds.append(
                        RoundTrace(
                            round_number=round_num,
                            n_proposals=len(current_proposals),
                            n_revised=n_revised,
                            interaction_summary=interaction_matrix.summary(),
                            role=round_role.value,
                        )
                    )
                    break

            if self._influence_tracker is not None and revised_proposals:
                self._influence_tracker.update(revised_proposals, sender_map)

            rounds.append(
                RoundTrace(
                    round_number=round_num,
                    n_proposals=len(current_proposals),
                    n_revised=n_revised,
                    interaction_summary=interaction_matrix.summary(),
                    role=round_role.value,
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
            cluster_result=cluster_result,
        )


# ── Internal helpers ─────────────────────────────────────────────────


def _build_philosopher_lookup(philosophers: Sequence) -> Dict[str, object]:
    """Build philosopher lookup keyed by both full name and philosopher_id.

    Full name (``ph.name``) is the primary key used by antithesis/standard
    rounds.  The lowercase class name (``type(ph).__name__.lower()``) is
    registered as a secondary key so that ``SYNTHESIZER_PHILOSOPHERS`` — which
    stores manifest IDs like ``"hegel"`` — can resolve correctly even when the
    instance name is ``"Georg Wilhelm Friedrich Hegel"``.
    """
    lookup = {}
    for ph in philosophers:
        name = getattr(ph, "name", None) or str(ph)
        lookup[name] = ph
        # Secondary key: lowercase class name matches manifest philosopher_id
        class_id = type(ph).__name__.lower()
        lookup.setdefault(class_id, ph)
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
    a_content = ""
    b_content = ""
    for p in proposals:
        author = _get_author(p)
        if author == pair.philosopher_a:
            a_content = p.content
        elif author == pair.philosopher_b:
            b_content = p.content

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


def _collect_synthesis_counterarguments(
    current_proposals: List[Proposal],
    synthesizer_names: List[str],
    ph_lookup: Dict[str, object],
) -> Dict[str, str]:
    """Build synthesis counterarguments for Synthesizer philosophers.

    Each synthesizer receives the combined text of all current proposals
    so they can integrate the full debate into a higher-order synthesis.
    """
    # Aggregate all proposals into a combined summary (max 10 proposals, 300 chars each)
    proposal_texts = []
    for p in current_proposals:
        author = _get_author(p)
        label = author if author else "Unknown"
        if p.content:
            proposal_texts.append(f"[{label}]: {p.content[:300]}")

    combined = "\n\n".join(proposal_texts[:10])

    # Only include synthesizers that exist in the philosopher lookup
    return {name: combined for name in synthesizer_names if name in ph_lookup}


def _build_debate_prompt(
    user_input: str,
    counter_text: str,
    sender_name: str,
    round_num: int,
    prompt_mode: str,
    role_prefix: str = "",
) -> str:
    """Build enriched user_input for counterargument re-proposal.

    prompt_mode="basic":  legacy soft counterargument (Phase 2 behavior)
    prompt_mode="debate": structured rebuttal with explicit obligations (Phase 6-A)
    role_prefix:          role instruction prepended before the debate prompt (Phase 6-B)
    """
    prefix_block = f"{role_prefix}\n" if role_prefix else ""

    if prompt_mode == "basic":
        return (
            f"{prefix_block}"
            f"{user_input}\n\n"
            f"[Counterargument from a fellow philosopher: {counter_text[:500]}]"
        )

    # "debate" mode — structured rebuttal obligation
    sender_label = sender_name if sender_name else "a fellow philosopher"
    return (
        f"{prefix_block}"
        f"{user_input}\n\n"
        f"[PHILOSOPHICAL CHALLENGE — Round {round_num}]\n"
        f"{sender_label} opposes your position with the following argument:\n\n"
        f'"{counter_text[:600]}"\n\n'
        f"You MUST respond by addressing all three points:\n"
        f"1. Steelman: Identify the strongest part of {sender_label}'s argument.\n"
        f"2. Refutation: Expose the core flaw or blind spot in their reasoning.\n"
        f"3. Defense: Sharpen and defend your own position with a new or deeper argument.\n\n"
        f"Do NOT repeat your previous response verbatim. "
        f"Engage directly with {sender_label}'s specific claims."
    )


def _re_propose(
    ph_lookup: Dict[str, object],
    counterarguments: Dict[str, str],
    ctx: DomainContext,
    intent: Intent,
    tensors: TensorSnapshot,
    memory: MemorySnapshot,
    round_num: int = 2,
    sender_map: Optional[Dict[str, str]] = None,
    prompt_mode: str = "debate",
    role: Optional[DebateRole] = None,
) -> List[Proposal]:
    """Re-run propose() for philosophers with counterargument context."""
    role_prefix = get_role_prompt_prefix(role) if role is not None else ""
    role_value = role.value if role is not None else DebateRole.STANDARD.value

    revised = []
    for name, counter_text in counterarguments.items():
        ph = ph_lookup.get(name)
        if ph is None or not hasattr(ph, "propose"):
            continue

        sender_name = (sender_map or {}).get(name, "a fellow philosopher")
        enriched_input = _build_debate_prompt(
            ctx.user_input,
            counter_text,
            sender_name,
            round_num,
            prompt_mode,
            role_prefix,
        )
        enriched_ctx = DomainContext(
            request_id=ctx.request_id,
            user_input=enriched_input,
            created_at=ctx.created_at,
        )

        try:
            new_proposals = ph.propose(enriched_ctx, intent, tensors, memory)
            if new_proposals:
                suffix = f":d{round_num}"
                candidates = [p for p in new_proposals if p is not None]
                if not candidates:
                    continue
                selected = max(candidates, key=lambda p: float(p.confidence))
                discarded_n = max(0, len(candidates) - 1)
                extra = dict(selected.extra) if isinstance(selected.extra, dict) else {}
                extra["deliberation_round"] = round_num
                extra["debate_sender"] = sender_name
                extra["prompt_mode"] = prompt_mode
                extra["dialectic_role"] = role_value
                if discarded_n > 0:
                    extra["deliberation_discarded_alternatives"] = discarded_n
                # Preserve PO_CORE author metadata for downstream scoring
                if PO_CORE not in extra or AUTHOR not in extra.get(PO_CORE, {}):
                    po_meta = extra.get(PO_CORE, {})
                    if not isinstance(po_meta, dict):
                        po_meta = {}
                    po_meta[AUTHOR] = name
                    extra[PO_CORE] = po_meta
                revised.append(
                    Proposal(
                        proposal_id=selected.proposal_id.replace(":0", suffix),
                        action_type=selected.action_type,
                        content=selected.content,
                        confidence=min(selected.confidence + 0.1, 1.0),
                        assumption_tags=list(selected.assumption_tags),
                        risk_tags=list(selected.risk_tags),
                        extra=extra,
                    )
                )
        except Exception:
            # Philosopher failed in re-proposal round → keep original
            continue

    return revised


def _merge_proposals(
    original: List[Proposal], revised: List[Proposal]
) -> List[Proposal]:
    """
    Merge revised proposals into original set.

    Revised proposals REPLACE originals from the same philosopher.
    """
    revised_authors = set()
    for p in revised:
        revised_authors.add(_get_author(p))

    merged = [p for p in original if _get_author(p) not in revised_authors]
    merged.extend(revised)
    return merged
