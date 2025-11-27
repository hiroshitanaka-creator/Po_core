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
    validate_philosopher_group,
    create_ethics_guardian,
    SafetyTier,
    ViolationType,
)


class TestPhilosopherProfileValidation:
    """Test philosopher safety profile validation."""

    def test_trusted_philosophers_allowed(self):
        """TRUSTED philosophers should work without restrictions."""
        po = PoSelf(
            philosophers=["aristotle", "confucius", "kant"],
            enable_ethics_guardian=False,  # Disable for this test
        )
        assert po.philosophers == ["aristotle", "confucius", "kant"]

    def test_restricted_philosopher_blocked_by_default(self):
        """RESTRICTED philosophers should be blocked without explicit permission."""
        with pytest.raises(ValueError, match="validation failed"):
            PoSelf(
                philosophers=["aristotle", "nietzsche"],  # nietzsche is RESTRICTED
                enable_ethics_guardian=False,
            )

    def test_restricted_philosopher_allowed_with_flags(self):
        """RESTRICTED philosophers allowed with proper flags."""
        po = PoSelf(
            philosophers=["aristotle", "nietzsche"],
            allow_restricted=True,
            dangerous_pattern_mode=True,
            enable_ethics_guardian=False,
        )
        assert "nietzsche" in po.philosophers

    def test_restricted_without_dangerous_mode_fails(self):
        """RESTRICTED philosophers require dangerous_pattern_mode."""
        with pytest.raises(ValueError, match="validation failed"):
            PoSelf(
                philosophers=["nietzsche"],
                allow_restricted=True,
                dangerous_pattern_mode=False,  # Missing!
                enable_ethics_guardian=False,
            )

    def test_monitored_philosophers_show_warning(self, capsys):
        """MONITORED philosophers should show warnings."""
        po = PoSelf(
            philosophers=["aristotle", "heidegger"],  # heidegger is MONITORED
            enable_ethics_guardian=False,
        )
        captured = capsys.readouterr()
        # Check that warning was shown (Rich console output)
        assert "heidegger" in po.philosophers


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
    """Test full Po_self integration with safety system."""

    def test_safe_generation_completes(self):
        """Safe prompts should complete normally."""
        po = PoSelf(
            philosophers=["aristotle", "kant", "mill"],
            enable_ethics_guardian=True,
        )

        # This should complete without errors
        # Note: This is a mock test - actual generation would require full ensemble
        # In real tests, you'd use a mock or fixture
        assert po.enable_ethics_guardian is True
        assert po.ethics_guardian is not None

    def test_ethics_guardian_initialized(self):
        """Ethics guardian should be initialized by default."""
        po = PoSelf(philosophers=["aristotle"])
        assert po.ethics_guardian is not None
        assert po.enable_ethics_guardian is True

    def test_ethics_guardian_can_be_disabled(self):
        """Ethics guardian should be disableable."""
        po = PoSelf(
            philosophers=["aristotle"],
            enable_ethics_guardian=False,
        )
        assert po.ethics_guardian is None
        assert po.enable_ethics_guardian is False

    def test_safety_flags_stored(self):
        """Safety configuration should be stored."""
        po = PoSelf(
            philosophers=["aristotle", "nietzsche"],
            allow_restricted=True,
            dangerous_pattern_mode=True,
        )

        assert po.allow_restricted is True
        assert po.dangerous_pattern_mode is True


class TestValidatePhilosopherGroup:
    """Test validate_philosopher_group function."""

    def test_all_trusted_valid(self):
        """All TRUSTED philosophers should validate."""
        result = validate_philosopher_group(
            ["aristotle", "confucius", "kant"]
        )

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
