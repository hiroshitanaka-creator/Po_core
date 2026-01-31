"""
Policy-based WethicsGate
========================

Unified 2-stage ethics gate implementing WethicsGatePort.
Wraps PolicyIntentionGate and PolicyActionGate.
"""
from __future__ import annotations

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.safety.wethics_gate.intention_gate import PolicyIntentionGate
from po_core.safety.wethics_gate.action_gate import PolicyActionGate


class PolicyWethicsGate:
    """
    Unified 2-stage ethics gate implementing WethicsGatePort.

    This gate combines:
    - PolicyIntentionGate for judge_intent
    - PolicyActionGate for judge_action
    """

    def __init__(
        self,
        intention: PolicyIntentionGate,
        action: PolicyActionGate,
    ):
        self._intention = intention
        self._action = action

    def judge_intent(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> SafetyVerdict:
        """Judge an intent (Stage 1)."""
        return self._intention.judge(ctx, intent, tensors, memory)

    def judge_action(
        self,
        ctx: Context,
        intent: Intent,
        proposal: Proposal,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> SafetyVerdict:
        """Judge a proposal (Stage 2)."""
        return self._action.judge(ctx, intent, proposal, tensors, memory)


__all__ = ["PolicyWethicsGate"]
