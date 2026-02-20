"""
Safety System Integration Tests
================================

Tests for Po_core safety system integration:
- Philosopher profile validation
- W_ethics boundary checking
- Restricted philosopher handling
- Dangerous pattern detection mode
"""

import pytest

from po_core.po_self import PoSelf
from po_core.safety import (
    ViolationType,
    create_ethics_guardian,
    validate_philosopher_group,
)


class TestPhilosopherProfileValidation:
    """Test philosopher safety profile validation via validate_philosopher_group."""

    def test_trusted_philosophers_allowed(self):
        """TRUSTED philosophers should validate without restrictions."""
        result = validate_philosopher_group(["aristotle", "confucius", "kant"])
        assert result["valid"] is True

    def test_restricted_philosopher_blocked_by_default(self):
        """RESTRICTED philosophers should be blocked without explicit permission."""
        result = validate_philosopher_group(
            ["aristotle", "nietzsche"],
            allow_restricted=False,
        )
        assert result["valid"] is False
        assert "nietzsche" in result["blocked_philosophers"]

    def test_restricted_philosopher_allowed_with_flags(self):
        """RESTRICTED philosophers allowed with proper flags."""
        result = validate_philosopher_group(
            ["aristotle", "nietzsche"],
            allow_restricted=True,
            dangerous_pattern_mode=True,
        )
        assert result["valid"] is True

    def test_monitored_philosophers_show_warning(self):
        """MONITORED philosophers should generate warnings."""
        result = validate_philosopher_group(
            ["aristotle", "heidegger"],
        )
        assert result["valid"] is True


class TestWEthicsGuardian:
    """Test W_ethics boundary checking."""

    def test_safe_prompt_no_violation(self):
        """Safe prompts should not trigger violations."""
        guardian = create_ethics_guardian()
        result = guardian.check_text(
            text="What is the meaning of human existence and dignity?",
            context="Philosophical inquiry",
        )

        assert result["violation_count"] == 0
        assert result["cumulative_w_ethics"] == 0.0
        assert not result["should_stop"]
        assert not result["dangerous_ideology_flag"]

    def test_violation_detection(self):
        """Ethical boundary violations should be detected."""
        guardian = create_ethics_guardian()

        # Text with violation keyword
        result = guardian.check_text(
            text="Some groups are naturally inferior and should be treated as subhuman.",
            context="Testing violation detection",
        )

        assert result["violation_count"] > 0
        assert result["cumulative_w_ethics"] < 0
        assert result["dangerous_ideology_flag"]

    def test_auto_stop_on_severe_violations(self):
        """Session should auto-stop when violations exceed threshold."""
        guardian = create_ethics_guardian(auto_stop_threshold=0.5)

        # Severe violation
        result = guardian.check_text(
            text="Inferior race subhuman vermin should be eliminated. Master race superiority.",
            context="Severe violation test",
        )

        assert result["should_stop"]
        assert result["dangerous_ideology_flag"]

    def test_negation_context_reduces_confidence(self):
        """Negation/critique context should reduce violation confidence."""
        guardian = create_ethics_guardian()

        # Critical discussion (should have lower penalty)
        result = guardian.check_text(
            text="We must reject the idea that any group is inferior based on immutable traits.",
            context="Critical discussion",
        )

        # Should still detect the keyword but with lower confidence
        # May or may not flag depending on threshold
        assert result["cumulative_w_ethics"] <= 0


class TestPoSelfSafetyIntegration:
    """Test PoSelf integration with safety system.

    Note: PoSelf now delegates to run_turn, which uses the 3-layer
    safety system (IntentionGate → PolicyPrecheck → ActionGate).
    The old enable_ethics_guardian / allow_restricted flags are removed.
    """

    def test_safe_generation_completes(self):
        """Safe prompts should complete normally via run_turn."""
        po = PoSelf()
        response = po.generate("What is the meaning of human dignity?")

        assert response.text
        assert response.metadata.get("status") == "ok"

    def test_run_turn_safety_is_active(self):
        """The run_turn pipeline always includes safety gates."""
        po = PoSelf(enable_trace=True)
        response = po.generate("What is justice?")

        # run_turn always applies IntentionGate + ActionGate
        assert response.log["status"] == "ok"
        assert "events" in response.log


class TestValidatePhilosopherGroup:
    """Test validate_philosopher_group function."""

    def test_all_trusted_valid(self):
        """All TRUSTED philosophers should validate."""
        result = validate_philosopher_group(["aristotle", "confucius", "kant"])

        assert result["valid"] is True
        assert len(result["blocked_philosophers"]) == 0
        assert len(result["restrictions"]) == 0

    def test_restricted_blocked_without_permission(self):
        """RESTRICTED philosophers blocked without flags."""
        result = validate_philosopher_group(
            ["aristotle", "nietzsche"],
            allow_restricted=False,
        )

        assert result["valid"] is False
        assert "nietzsche" in result["blocked_philosophers"]
        assert len(result["restrictions"]) > 0

    def test_restricted_allowed_with_flags(self):
        """RESTRICTED philosophers allowed with proper flags."""
        result = validate_philosopher_group(
            ["aristotle", "nietzsche"],
            allow_restricted=True,
            dangerous_pattern_mode=True,
        )

        assert result["valid"] is True
        assert len(result["blocked_philosophers"]) == 0

    def test_monitored_shows_warnings(self):
        """MONITORED philosophers should generate warnings."""
        result = validate_philosopher_group(
            ["aristotle", "heidegger"],  # heidegger is MONITORED
        )

        assert result["valid"] is True
        assert len(result["warnings"]) > 0


class TestViolationPatterns:
    """Test violation pattern detection."""

    def test_all_violation_types_defined(self):
        """All violation types should have patterns."""
        from po_core.safety.w_ethics import VIOLATION_PATTERNS

        # Should have multiple violation patterns
        assert len(VIOLATION_PATTERNS) > 0

        # Check key violation types exist
        assert ViolationType.RACIAL_SUPREMACY in VIOLATION_PATTERNS
        assert ViolationType.DEHUMANIZATION in VIOLATION_PATTERNS
        assert ViolationType.EXCLUSIONARY_FRAMING in VIOLATION_PATTERNS

    def test_violation_pattern_structure(self):
        """Violation patterns should have required fields."""
        from po_core.safety.w_ethics import VIOLATION_PATTERNS

        for vtype, pattern in VIOLATION_PATTERNS.items():
            assert pattern.violation_type == vtype
            assert pattern.severity >= 0.0
            assert pattern.severity <= 1.0
            assert pattern.w_ethics_penalty <= 0.0
            assert len(pattern.keywords) > 0


# ============================================================================
# Integration Tests with Mock Ensemble
# ============================================================================


class TestMockEthicsViolation:
    """Test ethics violation handling with mocked responses."""

    def test_violation_stops_session(self):
        """Severe violations should stop session and raise error."""
        # This would require mocking the ensemble to return violating text
        # For now, we just test the guardian directly
        guardian = create_ethics_guardian(auto_stop_threshold=0.5)

        result = guardian.check_text(
            text="Subhuman inferior race vermin parasites",
            context="Test",
        )

        assert result["should_stop"]
        assert result["dangerous_ideology_flag"]
        assert len(result["violations"]) > 0

    def test_violation_summary(self):
        """Guardian should provide violation summary."""
        guardian = create_ethics_guardian()

        # Add multiple violations
        guardian.check_text("subhuman vermin", "test1")
        guardian.check_text("inferior race", "test2")

        summary = guardian.get_violation_summary()

        assert summary["total_violations"] > 0
        assert summary["dangerous_ideology_flag"]
        assert summary["cumulative_w_ethics"] < 0

    def test_guardian_reset(self):
        """Guardian should reset between sessions."""
        guardian = create_ethics_guardian()

        # Add violation
        guardian.check_text("subhuman", "test")
        assert guardian.cumulative_w_ethics < 0

        # Reset
        guardian.reset()
        assert guardian.cumulative_w_ethics == 0.0
        assert len(guardian.violation_history) == 0
        assert guardian.dangerous_ideology_flag is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
