"""
WG.ACT.ACTTYPE.001 - Action Type Allowlist
==========================================

Rejects proposals with unknown action_type.
Prevents philosophers from creating arbitrary action types.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Optional

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.safety.wethics_gate.policies.base import ActionPolicy


@dataclass(frozen=True)
class ActionTypeAllowlistPolicy(ActionPolicy):
    """
    WG.ACT.ACTTYPE.001
    Allowlist for action_type. Rejects unknown types.
    """

    rule_id: str = "WG.ACT.ACTTYPE.001"
    priority: int = 5  # High priority (early check)

    allow: FrozenSet[str] = frozenset({"answer", "refuse", "ask_clarification"})
    # tool_call should only be allowed after tool constraints are in place

    def check(
        self,
        ctx: Context,
        intent: Intent,
        proposal: Proposal,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> Optional[SafetyVerdict]:
        if proposal.action_type in self.allow:
            return None

        return SafetyVerdict(
            decision=Decision.REJECT,
            rule_ids=[self.rule_id],
            reasons=[
                f"[{self.rule_id}] 許可されていない action_type: '{proposal.action_type}'"
            ],
            required_changes=[
                f"action_type を許可集合 {sorted(self.allow)} のいずれかに制限してください。",
            ],
            meta={"stage": "action", "action_type": proposal.action_type},
        )


__all__ = ["ActionTypeAllowlistPolicy"]
