"""
Tests for WG.ACT.MODE.001 - SafetyMode Degradation Policy
"""
from datetime import datetime, timezone

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.safety.wethics_gate.policies.action_mode_001 import SafetyModeDegradationPolicy


def _ctx() -> Context:
    return Context(
        request_id="test-mode",
        user_input="test",
        created_at=datetime.now(timezone.utc),
    )


def _intent() -> Intent:
    return Intent(
        goals=["goal1"],
        constraints=[],
        weights={},
    )


def _proposal() -> Proposal:
    return Proposal(
        proposal_id="p1",
        action_type="answer",
        content="test response",
    )


def _memory() -> MemorySnapshot:
    return MemorySnapshot(items=[], summary="", meta={})


def test_mode_normal_passes():
    """NORMAL mode should pass (no intervention)."""
    policy = SafetyModeDegradationPolicy()
    tensors = TensorSnapshot(
        version="v1",
        metrics={"freedom_pressure": 0.3},  # Below warn threshold (0.6)
    )
    result = policy.check(_ctx(), _intent(), _proposal(), tensors, _memory())
    assert result is None  # Pass


def test_mode_warn_revises():
    """WARN mode should REVISE with ask_clarification."""
    policy = SafetyModeDegradationPolicy()
    tensors = TensorSnapshot(
        version="v1",
        metrics={"freedom_pressure": 0.7},  # Between warn (0.6) and critical (0.85)
    )
    result = policy.check(_ctx(), _intent(), _proposal(), tensors, _memory())
    assert result is not None
    assert result.decision == Decision.REVISE
    assert result.meta.get("forced_action") == "ask_clarification"
    assert result.meta.get("safety_mode") == "warn"


def test_mode_critical_rejects():
    """CRITICAL mode should REJECT with refuse."""
    policy = SafetyModeDegradationPolicy()
    tensors = TensorSnapshot(
        version="v1",
        metrics={"freedom_pressure": 0.9},  # Above critical (0.85)
    )
    result = policy.check(_ctx(), _intent(), _proposal(), tensors, _memory())
    assert result is not None
    assert result.decision == Decision.REJECT
    assert result.meta.get("forced_action") == "refuse"
    assert result.meta.get("safety_mode") == "critical"


def test_mode_missing_defaults_to_warn():
    """Missing metric should default to WARN (fail-safe)."""
    policy = SafetyModeDegradationPolicy()
    tensors = TensorSnapshot(
        version="v1",
        metrics={},  # No freedom_pressure metric
    )
    result = policy.check(_ctx(), _intent(), _proposal(), tensors, _memory())
    assert result is not None
    assert result.decision == Decision.REVISE
    assert result.meta.get("forced_action") == "ask_clarification"
    assert result.meta.get("safety_mode") == "warn"


def test_rule_id():
    """Verify rule ID is correct."""
    policy = SafetyModeDegradationPolicy()
    assert policy.rule_id == "WG.ACT.MODE.001"
    assert policy.priority == 5
