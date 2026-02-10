"""
Tests for WG.ACT.ACTTYPE.001 - Action Type Allowlist Policy
"""

from datetime import datetime, timezone

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.safety.wethics_gate.action_gate import PolicyActionGate
from po_core.safety.wethics_gate.policies.action_acttype_001 import (
    ActionTypeAllowlistPolicy,
)


def test_action_rejects_unknown_action_type():
    """Unknown action_type should be rejected."""
    gate = PolicyActionGate([ActionTypeAllowlistPolicy()])
    ctx = Context("r1", datetime.now(timezone.utc), "x")
    prop = Proposal(
        proposal_id="p1",
        action_type="tool_call",  # Not in allowlist
        content="do something",
        confidence=0.9,
    )
    v = gate.judge(
        ctx, Intent.neutral(), prop, TensorSnapshot.empty(), MemorySnapshot()
    )
    assert v.decision == Decision.REJECT
    assert "WG.ACT.ACTTYPE.001" in v.rule_ids


def test_action_allows_answer():
    """'answer' action_type should be allowed."""
    gate = PolicyActionGate([ActionTypeAllowlistPolicy()])
    ctx = Context("r1", datetime.now(timezone.utc), "x")
    prop = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="The answer is 42",
        confidence=0.9,
    )
    v = gate.judge(
        ctx, Intent.neutral(), prop, TensorSnapshot.empty(), MemorySnapshot()
    )
    assert v.decision == Decision.ALLOW


def test_action_allows_refuse():
    """'refuse' action_type should be allowed."""
    gate = PolicyActionGate([ActionTypeAllowlistPolicy()])
    ctx = Context("r1", datetime.now(timezone.utc), "x")
    prop = Proposal(
        proposal_id="p1",
        action_type="refuse",
        content="I cannot help with that",
        confidence=0.9,
    )
    v = gate.judge(
        ctx, Intent.neutral(), prop, TensorSnapshot.empty(), MemorySnapshot()
    )
    assert v.decision == Decision.ALLOW


def test_action_allows_ask_clarification():
    """'ask_clarification' action_type should be allowed."""
    gate = PolicyActionGate([ActionTypeAllowlistPolicy()])
    ctx = Context("r1", datetime.now(timezone.utc), "x")
    prop = Proposal(
        proposal_id="p1",
        action_type="ask_clarification",
        content="Could you clarify what you mean?",
        confidence=0.9,
    )
    v = gate.judge(
        ctx, Intent.neutral(), prop, TensorSnapshot.empty(), MemorySnapshot()
    )
    assert v.decision == Decision.ALLOW


def test_action_rejects_shell_action_type():
    """'shell' action_type should be rejected."""
    gate = PolicyActionGate([ActionTypeAllowlistPolicy()])
    ctx = Context("r1", datetime.now(timezone.utc), "x")
    prop = Proposal(
        proposal_id="p1",
        action_type="shell",
        content="rm -rf /",
        confidence=0.9,
    )
    v = gate.judge(
        ctx, Intent.neutral(), prop, TensorSnapshot.empty(), MemorySnapshot()
    )
    assert v.decision == Decision.REJECT
    assert "WG.ACT.ACTTYPE.001" in v.rule_ids
