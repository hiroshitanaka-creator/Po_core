"""
Policy-Aware Aggregator
=======================

SafetyModeを読んで裁定する aggregator。
危険時は保守案を優先して勝手に締まる。

- CRITICAL: refuse/ask_clarification を強く優先
- WARN: ask_clarification/answer を優先
- NORMAL: confidence で単純選択

これで Gate の前段で「保守的な提案」が勝つ確率が上がる。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.ports.aggregator import AggregatorPort


@dataclass(frozen=True)
class PolicyAwareAggregator(AggregatorPort):
    """
    Policy-aware aggregator.

    SafetyMode を読んで裁定し、危険時は保守案を優先する。
    """

    config: SafetyModeConfig

    def aggregate(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        proposals: Sequence[Proposal],
    ) -> Proposal:
        """
        Aggregate proposals with policy-aware scoring.

        Args:
            ctx: Request context
            intent: Parsed intent
            tensors: Current tensor snapshot
            proposals: List of proposals from philosophers

        Returns:
            Best proposal based on policy-aware scoring
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

        mode, fp = infer_safety_mode(tensors, self.config)

        # Filter to preferred action types based on mode
        working_proposals = list(proposals)

        if mode == SafetyMode.CRITICAL:
            preferred = [p for p in working_proposals if p.action_type in ("refuse", "ask_clarification")]
            if preferred:
                working_proposals = preferred
        elif mode in (SafetyMode.WARN, SafetyMode.UNKNOWN):
            preferred = [p for p in working_proposals if p.action_type in ("ask_clarification", "answer", "refuse")]
            if preferred:
                working_proposals = preferred

        def score(p: Proposal) -> float:
            """Calculate policy-aware score for a proposal."""
            s = float(p.confidence)

            # Penalize risk and assumption tags
            s -= 0.15 * len(p.risk_tags)
            s -= 0.05 * len(p.assumption_tags)

            # Mode-specific scoring
            if mode == SafetyMode.CRITICAL:
                if p.action_type == "refuse":
                    s += 0.50
                elif p.action_type == "ask_clarification":
                    s += 0.20
                else:
                    s -= 1.00  # Heavily penalize other actions
            elif mode in (SafetyMode.WARN, SafetyMode.UNKNOWN):
                if p.action_type == "ask_clarification":
                    s += 0.25
                elif p.action_type == "answer":
                    s += 0.05
                elif p.action_type == "refuse":
                    s += 0.00
            # NORMAL: no additional scoring, use confidence only

            return s

        # Select best proposal (tie-breaker: proposal_id for determinism)
        best = max(working_proposals, key=lambda p: (score(p), p.proposal_id))

        # Add aggregation metadata
        extra = dict(best.extra) if isinstance(best.extra, Mapping) else {}
        extra["aggregation"] = {
            "strategy": "policy_aware_v1",
            "mode": mode.value,
            "freedom_pressure": "" if fp is None else str(fp),
            "selected": best.proposal_id,
            "candidates": len(proposals),
        }

        return Proposal(
            proposal_id=best.proposal_id,
            action_type=best.action_type,
            content=best.content,
            confidence=best.confidence,
            assumption_tags=list(best.assumption_tags),
            risk_tags=list(best.risk_tags),
            extra=extra,
        )


__all__ = ["PolicyAwareAggregator"]
