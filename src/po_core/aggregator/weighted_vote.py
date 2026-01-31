"""
Weighted Vote Aggregator
========================

Aggregates proposals by selecting the highest-confidence one.
"""
from __future__ import annotations

from typing import Sequence

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.ports.aggregator import AggregatorPort


class WeightedVoteAggregator(AggregatorPort):
    """
    Aggregator that selects the proposal with highest confidence.

    In case of ties, uses proposal_id for deterministic selection.
    """

    def aggregate(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        proposals: Sequence[Proposal],
    ) -> Proposal:
        """
        Aggregate proposals by selecting the highest-confidence one.

        Args:
            ctx: Request context
            intent: Current intent
            tensors: Tensor snapshot
            proposals: Sequence of proposals to aggregate

        Returns:
            The selected proposal, or a refuse proposal if none provided.
        """
        if not proposals:
            return Proposal(
                proposal_id=f"{ctx.request_id}:aggregate:none",
                action_type="refuse",
                content="No proposals generated.",
                confidence=0.0,
                assumption_tags=["no_proposals"],
                risk_tags=["system"],
            )

        return max(proposals, key=lambda p: (p.confidence, p.proposal_id))


__all__ = ["WeightedVoteAggregator"]
