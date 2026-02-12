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

    @property
    def n_rounds(self) -> int:
        return len(self.rounds)

    @property
    def total_proposals(self) -> int:
        return len(self.proposals)

    def summary(self) -> Dict:
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
                self.interaction_matrix.summary()
                if self.interaction_matrix
                else None
            ),
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
    ):
        self.max_rounds = max(1, max_rounds)
        self.top_k_pairs = top_k_pairs
        self.convergence_threshold = convergence_threshold

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
        current_proposals = list(round1_proposals)

        # Round 1 trace (already computed externally)
        rounds.append(RoundTrace(
            round_number=1,
            n_proposals=len(current_proposals),
            n_revised=0,
        ))

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
                rounds.append(RoundTrace(
                    round_number=round_num,
                    n_proposals=len(current_proposals),
                    n_revised=0,
                    interaction_summary=interaction_matrix.summary(),
                ))
                break

            # Identify philosophers that need to re-propose
            revised_names = set()
            counterarguments: Dict[str, str] = {}
            for pair in hi_pairs:
                # Each philosopher in a high-interference pair receives
                # the other's proposal as a counterargument
                _collect_counterargument(
                    pair, current_proposals, counterarguments, revised_names
                )

            # Re-propose for affected philosophers
            revised_proposals = _re_propose(
                ph_lookup, counterarguments, ctx, intent, tensors, memory
            )

            # Merge: replace old proposals with revised ones
            n_revised = len(revised_proposals)
            current_proposals = _merge_proposals(
                current_proposals, revised_proposals
            )

            rounds.append(RoundTrace(
                round_number=round_num,
                n_proposals=len(current_proposals),
                n_revised=n_revised,
                interaction_summary=interaction_matrix.summary(),
            ))

        return DeliberationResult(
            proposals=current_proposals,
            rounds=rounds,
            interaction_matrix=interaction_matrix,
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
) -> None:
    """Collect counterarguments for both philosophers in a pair."""
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
    if b_content and pair.philosopher_a not in counterarguments:
        counterarguments[pair.philosopher_a] = b_content
        revised_names.add(pair.philosopher_a)


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
                    revised.append(Proposal(
                        proposal_id=p.proposal_id.replace(":0", ":d2"),
                        action_type=p.action_type,
                        content=p.content,
                        confidence=min(p.confidence + 0.1, 1.0),
                        assumption_tags=list(p.assumption_tags),
                        risk_tags=list(p.risk_tags),
                        extra=extra,
                    ))
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
