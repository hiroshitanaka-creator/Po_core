"""Integration tests: Tensor → Safety → Pareto pipeline.

Tests the key subsystems working together without mocking,
ensuring that data flows correctly through the pipeline.
"""

from datetime import datetime, timezone

import pytest

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.tensors.engine import (
    compute_blocked_tensor,
    compute_freedom_pressure,
    compute_semantic_delta,
    compute_tensors,
)

# ── Tensor computation integration ──────────────────────────────────────


class TestTensorComputation:
    """Test tensor engine produces valid results for real prompts."""

    def test_compute_tensors_returns_snapshot(self):
        """Full tensor computation returns a valid TensorSnapshot."""
        result = compute_tensors("I must choose between two career paths.")
        assert isinstance(result, TensorSnapshot)
        # Values may be in .metrics or .values (backward compat) — use as_dict()
        d = result.as_dict()
        assert "freedom_pressure" in d
        assert "semantic_delta" in d
        assert "blocked_tensor" in d

    def test_freedom_pressure_range(self):
        """Freedom pressure is always in [0, 1]."""
        prompts = [
            "What time is it?",
            "I must decide now whether to leave everything behind.",
            "Should I sacrifice my career for my family?",
            "",
        ]
        for prompt in prompts:
            fp = compute_freedom_pressure(prompt)
            assert 0.0 <= fp.value <= 1.0, f"FP out of range for: {prompt!r}"

    def test_semantic_delta_range(self):
        """Semantic delta is always in [0, 1]."""
        result = compute_semantic_delta(
            "What is consciousness?", "An emergent property."
        )
        assert 0.0 <= result <= 1.0

    def test_blocked_tensor_derived_correctly(self):
        """Blocked tensor is derived from freedom_pressure and semantic_delta."""
        bt = compute_blocked_tensor(0.0, 0.0)
        assert 0.0 <= bt <= 1.0

        # High FP + low SD should reduce blocked tensor
        bt_high_fp = compute_blocked_tensor(0.9, 0.1)
        bt_low_fp = compute_blocked_tensor(0.1, 0.1)
        assert bt_high_fp <= bt_low_fp  # Higher FP → less blocked

    def test_high_stakes_prompt_increases_freedom_pressure(self):
        """A high-stakes ethical prompt should have higher FP than a trivial one."""
        fp_trivial = compute_freedom_pressure("What color is the sky?")
        fp_ethical = compute_freedom_pressure(
            "I must decide whether to report my employer's illegal activity, "
            "risking my career and family's financial security."
        )
        assert fp_ethical.value >= fp_trivial.value

    def test_tensor_snapshot_properties(self):
        """TensorSnapshot provides convenience properties."""
        snap = TensorSnapshot.now(
            metrics={
                "freedom_pressure": 0.7,
                "semantic_delta": 0.3,
                "blocked_tensor": 0.2,
            }
        )
        assert snap.freedom_pressure == 0.7
        assert snap.semantic_delta == 0.3
        assert snap.blocked_tensor == 0.2


# ── SafetyMode inference integration ────────────────────────────────────


class TestSafetyModeInference:
    """Test safety mode is inferred correctly from tensor values."""

    def test_normal_mode_low_pressure(self):
        """Low freedom pressure → NORMAL mode."""
        snap = TensorSnapshot.now(metrics={"freedom_pressure": 0.15})
        mode, value = infer_safety_mode(snap)
        assert mode == SafetyMode.NORMAL
        assert value == 0.15

    def test_warn_mode_medium_pressure(self):
        """Medium freedom pressure → WARN mode."""
        snap = TensorSnapshot.now(metrics={"freedom_pressure": 0.35})
        mode, _ = infer_safety_mode(snap)
        assert mode == SafetyMode.WARN

    def test_critical_mode_high_pressure(self):
        """High freedom pressure → CRITICAL mode."""
        snap = TensorSnapshot.now(metrics={"freedom_pressure": 0.55})
        mode, _ = infer_safety_mode(snap)
        assert mode == SafetyMode.CRITICAL

    def test_missing_metric_defaults_to_warn(self):
        """Missing freedom_pressure metric → WARN (fail-closed)."""
        snap = TensorSnapshot.now(metrics={})
        mode, value = infer_safety_mode(snap)
        assert mode == SafetyMode.WARN
        assert value is None

    def test_custom_thresholds(self):
        """Custom SafetyModeConfig thresholds are respected."""
        config = SafetyModeConfig(warn=0.3, critical=0.5)
        snap = TensorSnapshot.now(metrics={"freedom_pressure": 0.4})
        mode, _ = infer_safety_mode(snap, config)
        assert mode == SafetyMode.WARN


# ── SafetyVerdict integration ───────────────────────────────────────────


class TestSafetyVerdictConstruction:
    """Test safety verdict factory methods and properties."""

    def test_allow_verdict(self):
        """Allow verdict is properly constructed."""
        v = SafetyVerdict.allow()
        assert v.is_allowed
        assert not v.is_rejected
        assert not v.needs_revision
        assert v.decision == Decision.ALLOW

    def test_reject_verdict(self):
        """Reject verdict carries reasons."""
        v = SafetyVerdict.reject(
            rule_ids=["W0_illegal"],
            reasons=["Contains illegal intent"],
        )
        assert v.is_rejected
        assert not v.is_allowed
        assert "W0_illegal" in v.rule_ids
        assert len(v.reasons) == 1

    def test_revise_verdict(self):
        """Revise verdict includes required changes."""
        v = SafetyVerdict.revise(
            rule_ids=["W3_lockin"],
            reasons=["Dependency lock-in detected"],
            required_changes=["Add data portability clause"],
        )
        assert v.needs_revision
        assert len(v.required_changes) == 1

    def test_fail_closed_verdict(self):
        """Fail-closed creates a reject verdict."""
        v = SafetyVerdict.fail_closed(RuntimeError("unexpected error"))
        assert v.is_rejected


# ── Proposal construction ───────────────────────────────────────────────


class TestProposalConstruction:
    """Test proposal objects for aggregation."""

    def test_proposal_immutable(self):
        """Proposals are frozen dataclasses."""
        p = Proposal(
            proposal_id="p1",
            action_type="answer",
            content="Test content",
            confidence=0.8,
        )
        with pytest.raises(AttributeError):
            p.content = "modified"  # type: ignore[misc]

    def test_proposal_to_dict(self):
        """Proposals serialize correctly."""
        p = Proposal(
            proposal_id="p1",
            action_type="answer",
            content="Test",
            confidence=0.75,
            assumption_tags=["ethics"],
        )
        d = p.to_dict()
        assert d["proposal_id"] == "p1"
        assert d["confidence"] == 0.75
        assert "ethics" in d["assumption_tags"]


# ── End-to-end: Tensor → SafetyMode → Proposal ─────────────────────────


class TestTensorToSafetyModePipeline:
    """Integration test: compute tensors, infer safety mode, verify pipeline consistency."""

    def test_ethical_prompt_pipeline(self):
        """An ethical dilemma should flow through the pipeline correctly."""
        prompt = "Should I lie to protect someone I love from painful truth?"

        # Step 1: Compute tensors
        snap = compute_tensors(prompt)
        assert isinstance(snap, TensorSnapshot)

        # Step 2: Infer safety mode
        mode, fp_value = infer_safety_mode(snap)
        assert isinstance(mode, SafetyMode)

        # Step 3: Create a proposal
        proposal = Proposal(
            proposal_id="test-p1",
            action_type="answer",
            content="This is a nuanced ethical question requiring careful consideration.",
            confidence=0.6,
            assumption_tags=["ethics", "relationships"],
        )

        # Step 4: Verify consistency
        assert proposal.confidence > 0
        assert snap.freedom_pressure >= 0
        assert mode in (SafetyMode.NORMAL, SafetyMode.WARN, SafetyMode.CRITICAL)

    def test_trivial_prompt_pipeline(self):
        """A trivial prompt should be handled without crashing."""
        prompt = "Hello, how are you?"

        snap = compute_tensors(prompt)
        mode, _ = infer_safety_mode(snap)

        # Trivial prompts may be NORMAL or WARN depending on metric availability.
        # The key invariant: compute_tensors + infer_safety_mode never crashes.
        assert mode in (SafetyMode.NORMAL, SafetyMode.WARN, SafetyMode.CRITICAL)
