"""
WG.ACT.MODE.001 - Action SafetyMode Degradation Policy
======================================================

When SafetyMode is WARN or CRITICAL at action stage,
force degradation unless the proposal is already safe.

Priority: 15 (after type check - let safe actions pass first)

Behavior:
- NORMAL: pass (no intervention)
- WARN: REVISE unless action_type is safe (ask_clarification, refuse)
- CRITICAL: REVISE to refuse unless already refuse
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Optional

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot


@dataclass(frozen=True)
class ActionModeDegradePolicy:
    """
    Force degradation when SafetyMode is elevated at action stage.

    Unlike the intention-stage policy, this one allows "safe" actions
    through - we don't need to degrade if the proposal is already
    asking for clarification or refusing.
    """

    rule_id: str = "WG.ACT.MODE.001"
    priority: int = 15  # After type check - let safe actions pass first
    config: SafetyModeConfig = field(default_factory=SafetyModeConfig)

    # Actions that are inherently safe and don't need degradation
    safe_actions: FrozenSet[str] = frozenset({"ask_clarification", "refuse"})

    def check(
        self,
        ctx: Context,
        intent: Intent,
        proposal: Proposal,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> Optional[SafetyVerdict]:
        """
        Check SafetyMode and enforce degradation if needed.

        Returns:
            SafetyVerdict if mode is elevated and action is unsafe, None otherwise.
        """
        mode, value = infer_safety_mode(tensors, self.config)

        if mode == SafetyMode.NORMAL:
            return None

        if mode == SafetyMode.WARN:
            # Allow safe actions through in WARN mode
            if proposal.action_type in self.safe_actions:
                return None
            return SafetyVerdict(
                decision=Decision.REVISE,
                rule_ids=[self.rule_id],
                reasons=[
                    f"[{self.rule_id}] SafetyMode=warn のため ask_clarification へ縮退",
                ],
                required_changes=[
                    "action_type を ask_clarification に変更してください。"
                ],
                meta={
                    "stage": "action",
                    "mode": mode.value,
                    "forced_action": "ask_clarification",
                    "value": "" if value is None else str(value),
                },
            )

        if mode == SafetyMode.CRITICAL:
            # Only allow refuse in CRITICAL mode
            if proposal.action_type == "refuse":
                return None
            return SafetyVerdict(
                decision=Decision.REVISE,
                rule_ids=[self.rule_id],
                reasons=[
                    f"[{self.rule_id}] SafetyMode=critical のため refuse へ縮退",
                ],
                required_changes=["action_type を refuse に変更してください。"],
                meta={
                    "stage": "action",
                    "mode": mode.value,
                    "forced_action": "refuse",
                    "value": "" if value is None else str(value),
                },
            )

        return None


# Backward compat alias
SafetyModeDegradationPolicy = ActionModeDegradePolicy


__all__ = ["ActionModeDegradePolicy", "SafetyModeDegradationPolicy"]
