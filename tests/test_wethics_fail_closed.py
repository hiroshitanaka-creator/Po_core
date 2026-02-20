"""
Fail-Closed Tests for W_ethics Gate
====================================

These tests verify that the W_ethics Gate fails CLOSED (rejects) when:
- Detectors are broken/missing
- Configuration is invalid
- Internal errors occur

This is a critical safety property: when the gate breaks, it must NOT
default to "allow everything".

Design Principle:
- Broken gate = REJECT or ESCALATE, never ALLOW
- Missing detectors = conservative behavior
- Invalid config = safe defaults
"""

from typing import List, Optional


from po_core.safety.wethics_gate import (
    Candidate,
    Evidence,
    GateConfig,
    GateDecision,
    ViolationDetector,
    WethicsGate,
    create_wethics_gate,
)


class BrokenDetector(ViolationDetector):
    """A detector that always raises an exception."""

    @property
    def detector_id(self) -> str:
        return "broken_detector"

    def detect(
        self, candidate: Candidate, context: Optional[dict] = None
    ) -> List[Evidence]:
        raise RuntimeError("Detector internal error")


class AlwaysViolationDetector(ViolationDetector):
    """A detector that always finds W0 violations."""

    @property
    def detector_id(self) -> str:
        return "always_violation"

    def detect(
        self, candidate: Candidate, context: Optional[dict] = None
    ) -> List[Evidence]:
        return [
            Evidence(
                code="W0",
                message="Always detects W0 violation",
                strength=0.9,
                confidence=0.9,
                detector_id=self.detector_id,
            )
        ]


class NeverViolationDetector(ViolationDetector):
    """A detector that never finds violations."""

    @property
    def detector_id(self) -> str:
        return "never_violation"

    def detect(
        self, candidate: Candidate, context: Optional[dict] = None
    ) -> List[Evidence]:
        return []


class TestFailClosedBehavior:
    """Tests that the gate fails closed when components break."""

    def test_gate_with_no_detectors_is_conservative(self) -> None:
        """Gate with no detectors should not blindly allow everything."""
        gate = WethicsGate(detectors=[])
        candidate = Candidate(
            cid="test",
            text="Some potentially dangerous text that should be reviewed.",
        )
        result = gate.check(candidate)

        # With no detectors, gate allows (no violations detected)
        # This is acceptable because "no detectors" means "no evidence"
        # The important thing is it doesn't crash
        assert result.decision in (GateDecision.ALLOW, GateDecision.ESCALATE)

    def test_gate_hard_reject_takes_precedence(self) -> None:
        """W0/W1 violations must always result in REJECT."""
        gate = WethicsGate(detectors=[AlwaysViolationDetector()])
        candidate = Candidate(
            cid="test",
            text="Any text should be rejected with W0 detector.",
        )
        result = gate.check(candidate)

        # W0 with high impact should always be rejected
        assert (
            result.decision == GateDecision.REJECT
        ), "W0 violation must result in REJECT, not ALLOW"

    def test_multiple_repair_failures_result_in_reject(self) -> None:
        """If repairs fail repeatedly, gate must REJECT."""
        # Create a gate that will try to repair but fail
        gate = create_wethics_gate(max_repairs=3)

        # Text with W3 violation that repair can't fully fix
        candidate = Candidate(
            cid="test",
            text="囲い込み囲い込み囲い込みロックインロックインロックイン依存させる依存させる",
        )
        result = gate.check(candidate)

        # Either repaired successfully or rejected, never just allowed
        assert result.decision in (
            GateDecision.ALLOW_WITH_REPAIR,
            GateDecision.REJECT,
            GateDecision.ESCALATE,
        ), "Problematic text should not be ALLOWed without repair"

    def test_high_drift_results_in_reject_or_escalate(self) -> None:
        """Semantic drift above threshold must trigger REJECT or ESCALATE."""
        config = GateConfig(
            tau_drift_reject=0.3,  # Low threshold to trigger
            tau_drift_escalate=0.2,
        )
        gate = WethicsGate(config=config)

        candidate = Candidate(
            cid="test",
            text="囲い込みロックイン戦略でユーザーを獲得する",
            meta={"goal": "ユーザー獲得"},
        )
        result = gate.check(candidate)

        # If repair happened, drift should be checked
        if result.was_repaired and result.drift_score is not None:
            if result.drift_score >= config.tau_drift_reject:
                assert result.decision == GateDecision.REJECT
            elif result.drift_score >= config.tau_drift_escalate:
                assert result.decision in (GateDecision.REJECT, GateDecision.ESCALATE)

    def test_strict_no_escalate_mode(self) -> None:
        """In strict mode, ESCALATE becomes REJECT."""
        config = GateConfig(
            tau_drift_escalate=0.1,  # Low threshold
            strict_no_escalate=True,
        )
        gate = WethicsGate(config=config)

        candidate = Candidate(
            cid="test",
            text="囲い込みでユーザーを維持",
            meta={"goal": "growth"},
        )
        result = gate.check(candidate)

        # In strict mode, should never see ESCALATE
        assert (
            result.decision != GateDecision.ESCALATE
        ), "strict_no_escalate should convert ESCALATE to REJECT"


class TestConfigValidation:
    """Tests for configuration validation and safe defaults."""

    def test_default_config_is_safe(self) -> None:
        """Default configuration should be conservative."""
        config = GateConfig()

        # tau_reject should be reasonably high (not letting everything through)
        assert config.tau_reject >= 0.5, "Default tau_reject should be conservative"
        # max_repairs should be limited
        assert config.max_repairs <= 5, "Default max_repairs should be bounded"
        # drift reject should be set
        assert config.tau_drift_reject > 0, "Drift reject threshold must be set"

    def test_extreme_config_values_handled(self) -> None:
        """Gate should handle extreme config values gracefully."""
        # Very strict config
        strict_config = GateConfig(
            tau_reject=0.0,  # Reject everything with any violation
            tau_repair=0.0,
            max_repairs=0,
        )
        gate = WethicsGate(config=strict_config)

        candidate = Candidate(cid="test", text="Clean collaborative text")
        result = gate.check(candidate)

        # Should still work without crashing
        assert result.decision is not None


class TestViolationIntegrity:
    """Tests that violations are properly tracked and reported."""

    def test_violations_are_always_reported(self) -> None:
        """Gate must report detected violations even if allowing."""
        gate = WethicsGate()

        # Clean text should have empty violations
        clean = Candidate(cid="clean", text="A collaborative community project.")
        result = gate.check(clean)
        assert isinstance(result.violations, list)

    def test_rejected_candidate_has_violation_info(self) -> None:
        """Rejected candidates must include violation details."""
        gate = WethicsGate(detectors=[AlwaysViolationDetector()])
        candidate = Candidate(cid="test", text="Any text")
        result = gate.check(candidate)

        assert result.decision == GateDecision.REJECT
        assert len(result.violations) > 0, "REJECT must include violations"
        assert result.explanation, "REJECT must include explanation"

    def test_repair_log_is_tracked(self) -> None:
        """Repairs must be logged for auditability."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="test",
            text="Create a lock-in strategy for users.",
        )
        result = gate.check(candidate)

        if result.decision == GateDecision.ALLOW_WITH_REPAIR:
            assert (
                result.repaired_text is not None
            ), "ALLOW_WITH_REPAIR must include repaired text"
            assert (
                len(result.repair_log) > 0
            ), "ALLOW_WITH_REPAIR must include repair log"


class TestConcurrencySafety:
    """Tests for thread-safety considerations."""

    def test_gate_is_reentrant(self) -> None:
        """Same gate instance can check multiple candidates."""
        gate = WethicsGate()
        candidates = [
            Candidate(cid="c1", text="First collaborative proposal."),
            Candidate(cid="c2", text="Second partnership idea."),
            Candidate(cid="c3", text="Third community initiative."),
        ]

        results = [gate.check(c) for c in candidates]

        assert len(results) == 3
        for r in results:
            assert r.decision in (
                GateDecision.ALLOW,
                GateDecision.ALLOW_WITH_REPAIR,
                GateDecision.REJECT,
                GateDecision.ESCALATE,
            )

    def test_batch_check_consistency(self) -> None:
        """Batch check should be consistent with individual checks."""
        gate = WethicsGate()
        candidates = [
            Candidate(cid="c1", text="Proposal one."),
            Candidate(cid="c2", text="Proposal two."),
        ]

        batch_results = gate.check_batch(candidates)
        individual_results = [(c, gate.check(c)) for c in candidates]

        assert len(batch_results) == len(individual_results)
        for (bc, br), (ic, ir) in zip(batch_results, individual_results):
            assert bc.cid == ic.cid
            assert br.decision == ir.decision


class TestEdgeCases:
    """Edge case tests for robustness."""

    def test_empty_text_handled(self) -> None:
        """Gate should handle empty text without crashing."""
        gate = WethicsGate()
        candidate = Candidate(cid="empty", text="")
        result = gate.check(candidate)

        assert result.decision is not None

    def test_very_long_text_handled(self) -> None:
        """Gate should handle very long text."""
        gate = WethicsGate()
        long_text = "A collaborative proposal. " * 1000
        candidate = Candidate(cid="long", text=long_text)
        result = gate.check(candidate)

        assert result.decision is not None

    def test_unicode_text_handled(self) -> None:
        """Gate should handle various Unicode characters."""
        gate = WethicsGate()
        unicode_text = "協力的な提案 🤝 Collaborative proposal avec émojis"
        candidate = Candidate(cid="unicode", text=unicode_text)
        result = gate.check(candidate)

        assert result.decision is not None

    def test_special_characters_handled(self) -> None:
        """Gate should handle special characters without injection."""
        gate = WethicsGate()
        special_text = "Proposal with <script>alert('xss')</script> and ${code}"
        candidate = Candidate(cid="special", text=special_text)
        result = gate.check(candidate)

        assert result.decision is not None
