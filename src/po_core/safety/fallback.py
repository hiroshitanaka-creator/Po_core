"""
Safety Fallback Composition
===========================

When a verdict is REJECT or REVISE, this module composes a safe
fallback Proposal instead of simply blocking.

This prevents "silent death" - the system always responds.
"""

from __future__ import annotations

import uuid
from typing import Optional

from po_core.domain.context import Context
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision, SafetyVerdict


def compose_fallback(
    ctx: Context,
    verdict: SafetyVerdict,
    *,
    stage: str,
) -> Proposal:
    """
    Compose a safe fallback Proposal from a negative verdict.

    Policies can set `meta["forced_action"]` to override the default.
    Otherwise:
      - REJECT → "refuse"
      - REVISE → "ask_clarification"

    Args:
        ctx: Request context
        verdict: The negative verdict (REJECT or REVISE)
        stage: Pipeline stage where blocking occurred ("intention" or "action")

    Returns:
        A safe Proposal with action_type set appropriately
    """
    forced = verdict.meta.get("forced_action")

    if forced is None:
        forced = (
            "refuse" if verdict.decision == Decision.REJECT else "ask_clarification"
        )

    # Build explanation from verdict reasons
    reasons_str = "; ".join(verdict.reasons[:3]) if verdict.reasons else "安全上の理由"
    required_str = (
        "; ".join(verdict.required_changes[:2]) if verdict.required_changes else ""
    )

    if verdict.decision == Decision.REJECT:
        content = f"申し訳ありませんが、このリクエストにはお応えできません。理由: {reasons_str}"
    else:
        if required_str:
            content = f"リクエストを明確化していただけますか？{required_str}"
        else:
            content = f"リクエストを明確化していただけますか？理由: {reasons_str}"

    return Proposal(
        proposal_id=f"fallback-{uuid.uuid4().hex[:12]}",
        action_type=forced,
        content=content,
        confidence=1.0,  # We are certain this is a safe response
        assumption_tags=[f"fallback_{stage}"],
        risk_tags=[],
        extra={
            "fallback": True,
            "stage": stage,
            "original_decision": verdict.decision.value,
            "rule_ids": verdict.rule_ids,
        },
    )


def is_fallback(proposal: Proposal) -> bool:
    """Check if a proposal is a fallback response."""
    return proposal.extra.get("fallback", False) is True


__all__ = ["compose_fallback", "is_fallback"]
