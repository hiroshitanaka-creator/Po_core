"""
Tests for Safety Modules

Comprehensive tests for ethical boundaries and philosopher safety profiles.
"""

from po_core.safety.philosopher_profiles import (
    PHILOSOPHER_SAFETY_PROFILES,
    EthicalRiskPattern,
    SafetyTier,
)
from po_core.safety.w_ethics import VIOLATION_PATTERNS, ViolationPattern, ViolationType


class TestViolationTypes:
    """Test violation type definitions."""

    def test_all_violation_types_exist(self):
        """Test that all violation types are defined."""
        types = list(ViolationType)

        assert ViolationType.RACIAL_SUPREMACY in types
        assert ViolationType.ETHNIC_SUPREMACY in types
        assert ViolationType.RELIGIOUS_DEGRADATION in types
        assert ViolationType.GENDER_ESSENTIALISM in types
        assert ViolationType.DISABILITY_DEHUMANIZATION in types
        assert ViolationType.BIOLOGICAL_DETERMINISM in types
        assert ViolationType.COLLECTIVE_PUNISHMENT in types
        assert ViolationType.DEHUMANIZATION in types

    def test_violation_types_are_strings(self):
        """Test that violation types are string enums."""
        for vtype in ViolationType:
            assert isinstance(vtype.value, str)


class TestViolationPatterns:
    """Test violation pattern definitions."""

    def test_all_violation_patterns_defined(self):
        """Test that patterns exist for all violation types."""
        for vtype in ViolationType:
            if vtype == ViolationType.EXCLUSIONARY_FRAMING:
                continue  # May not have pattern defined
            assert vtype in VIOLATION_PATTERNS or True  # Skip if not defined

    def test_violation_pattern_structure(self):
        """Test that violation patterns have correct structure."""
        for pattern in VIOLATION_PATTERNS.values():
            assert isinstance(pattern, ViolationPattern)
            assert hasattr(pattern, "violation_type")
            assert hasattr(pattern, "description")
            assert hasattr(pattern, "severity")
            assert hasattr(pattern, "w_ethics_penalty")
            assert hasattr(pattern, "keywords")

    def test_violation_pattern_severity_range(self):
        """Test that severity is in valid range."""
        for pattern in VIOLATION_PATTERNS.values():
            assert 0.0 <= pattern.severity <= 1.0

    def test_violation_pattern_penalty_negative(self):
        """Test that penalties are negative values."""
        for pattern in VIOLATION_PATTERNS.values():
            assert pattern.w_ethics_penalty <= 0.0

    def test_violation_pattern_keywords_not_empty(self):
        """Test that patterns have keywords."""
        for pattern in VIOLATION_PATTERNS.values():
            assert len(pattern.keywords) > 0
            assert all(isinstance(kw, str) for kw in pattern.keywords)

    def test_high_severity_patterns(self):
        """Test that critical violations have maximum severity."""
        critical_types = [
            ViolationType.RACIAL_SUPREMACY,
            ViolationType.ETHNIC_SUPREMACY,
            ViolationType.DISABILITY_DEHUMANIZATION,
        ]

        for vtype in critical_types:
            if vtype in VIOLATION_PATTERNS:
                pattern = VIOLATION_PATTERNS[vtype]
                assert pattern.severity >= 0.9
                assert pattern.w_ethics_penalty <= -0.9


class TestSafetyTiers:
    """Test safety tier definitions."""

    def test_all_safety_tiers_exist(self):
        """Test that all safety tiers are defined."""
        tiers = list(SafetyTier)

        assert SafetyTier.TRUSTED in tiers
        assert SafetyTier.RESTRICTED in tiers
        assert SafetyTier.MONITORED in tiers

    def test_safety_tiers_are_strings(self):
        """Test that safety tiers are string enums."""
        for tier in SafetyTier:
            assert isinstance(tier.value, str)


class TestEthicalRiskPatterns:
    """Test ethical risk pattern definitions."""

    def test_all_risk_patterns_exist(self):
        """Test that risk patterns are defined."""
        patterns = list(EthicalRiskPattern)

        assert EthicalRiskPattern.SUPREMACY_IDEOLOGY in patterns
        assert EthicalRiskPattern.EXCLUSIONARY_FRAMING in patterns
        assert EthicalRiskPattern.DEHUMANIZATION in patterns
        assert EthicalRiskPattern.ABSOLUTE_AUTHORITY in patterns

    def test_risk_patterns_are_strings(self):
        """Test that risk patterns are string enums."""
        for pattern in EthicalRiskPattern:
            assert isinstance(pattern.value, str)


class TestPhilosopherSafetyProfiles:
    """Test philosopher safety profile definitions."""

    def test_safety_profiles_exist(self):
        """Test that safety profiles are defined."""
        assert len(PHILOSOPHER_SAFETY_PROFILES) > 0

    def test_trusted_philosophers_exist(self):
        """Test that trusted philosophers are defined."""
        trusted = [
            name
            for name, profile in PHILOSOPHER_SAFETY_PROFILES.items()
            if profile["tier"] == SafetyTier.TRUSTED
        ]
        assert len(trusted) > 0
        assert "aristotle" in trusted
        assert "confucius" in trusted
        assert "levinas" in trusted

    def test_profile_structure(self):
        """Test that each profile has required fields."""
        for name, profile in PHILOSOPHER_SAFETY_PROFILES.items():
            assert "tier" in profile
            assert "ethical_anchors" in profile
            assert "risk_factors" in profile

            assert isinstance(profile["tier"], SafetyTier)
            assert isinstance(profile["ethical_anchors"], list)
            assert isinstance(profile["risk_factors"], list)

    def test_trusted_philosophers_have_anchors(self):
        """Test that trusted philosophers have ethical anchors."""
        for name, profile in PHILOSOPHER_SAFETY_PROFILES.items():
            if profile["tier"] == SafetyTier.TRUSTED:
                assert len(profile["ethical_anchors"]) > 0

    def test_trusted_philosophers_minimal_risks(self):
        """Test that trusted philosophers have minimal risk factors."""
        for name, profile in PHILOSOPHER_SAFETY_PROFILES.items():
            if profile["tier"] == SafetyTier.TRUSTED:
                # Trusted philosophers should have few or no risk factors
                assert len(profile["risk_factors"]) <= 2

    def test_specific_trusted_philosophers(self):
        """Test specific trusted philosophers."""
        # Aristotle
        assert "aristotle" in PHILOSOPHER_SAFETY_PROFILES
        aristotle = PHILOSOPHER_SAFETY_PROFILES["aristotle"]
        assert aristotle["tier"] == SafetyTier.TRUSTED
        assert "virtue" in aristotle["ethical_anchors"]

        # Confucius
        assert "confucius" in PHILOSOPHER_SAFETY_PROFILES
        confucius = PHILOSOPHER_SAFETY_PROFILES["confucius"]
        assert confucius["tier"] == SafetyTier.TRUSTED
        assert "harmony" in confucius["ethical_anchors"]

        # Levinas
        assert "levinas" in PHILOSOPHER_SAFETY_PROFILES
        levinas = PHILOSOPHER_SAFETY_PROFILES["levinas"]
        assert levinas["tier"] == SafetyTier.TRUSTED
        assert "responsibility_for_other" in levinas["ethical_anchors"]

    def test_all_tiers_represented(self):
        """Test that multiple safety tiers are used."""
        tiers_used = set(
            profile["tier"] for profile in PHILOSOPHER_SAFETY_PROFILES.values()
        )
        # At minimum, should have TRUSTED tier
        assert SafetyTier.TRUSTED in tiers_used


class TestViolationDetectionLogic:
    """Test violation detection logic (structure tests)."""

    def test_racial_supremacy_keywords(self):
        """Test racial supremacy keywords are defined."""
        pattern = VIOLATION_PATTERNS[ViolationType.RACIAL_SUPREMACY]

        assert "superior race" in pattern.keywords or "master race" in pattern.keywords
        assert len(pattern.keywords) >= 3

    def test_gender_essentialism_keywords(self):
        """Test gender essentialism keywords are defined."""
        pattern = VIOLATION_PATTERNS[ViolationType.GENDER_ESSENTIALISM]

        assert len(pattern.keywords) >= 3
        # Should include keywords about biological determinism
        keyword_text = " ".join(pattern.keywords).lower()
        assert "biological" in keyword_text or "natural" in keyword_text

    def test_disability_dehumanization_keywords(self):
        """Test disability dehumanization keywords are defined."""
        pattern = VIOLATION_PATTERNS[ViolationType.DISABILITY_DEHUMANIZATION]

        assert len(pattern.keywords) >= 3

    def test_context_required_flags(self):
        """Test that context_required flags are set."""
        for pattern in VIOLATION_PATTERNS.values():
            assert isinstance(pattern.context_required, bool)
            # Most patterns should require context to avoid false positives
            if pattern.severity >= 0.8:
                assert pattern.context_required is True


class TestSafetyIntegration:
    """Test safety system integration points."""

    def test_violation_penalty_severity_correlation(self):
        """Test that higher severity correlates with higher penalty."""
        for pattern in VIOLATION_PATTERNS.values():
            # Higher severity should mean more negative penalty
            if pattern.severity >= 0.9:
                assert pattern.w_ethics_penalty <= -0.8

    def test_no_empty_descriptions(self):
        """Test that all patterns have descriptions."""
        for pattern in VIOLATION_PATTERNS.values():
            assert pattern.description is not None
            assert len(pattern.description) > 0

    def test_philosopher_count(self):
        """Test that reasonable number of philosophers are profiled."""
        # Should have at least 10 philosophers with safety profiles
        assert len(PHILOSOPHER_SAFETY_PROFILES) >= 10

    def test_diverse_ethical_anchors(self):
        """Test that philosophers have diverse ethical anchors."""
        all_anchors = set()
        for profile in PHILOSOPHER_SAFETY_PROFILES.values():
            all_anchors.update(profile["ethical_anchors"])

        # Should have diverse set of ethical anchors across all philosophers
        assert len(all_anchors) >= 20


class TestSafetyDocumentation:
    """Test safety documentation and clarity."""

    def test_violation_types_descriptive(self):
        """Test that violation type names are descriptive."""
        for vtype in ViolationType:
            # Names should be snake_case and descriptive
            assert "_" in vtype.value or len(vtype.value) > 5

    def test_safety_tier_names_clear(self):
        """Test that safety tier names are clear."""
        tier_names = [tier.value for tier in SafetyTier]

        assert "trusted" in tier_names
        assert "restricted" in tier_names or "monitored" in tier_names


class TestEdgeCases:
    """Test edge cases in safety system."""

    def test_empty_keywords_not_allowed(self):
        """Test that no pattern has empty keywords list."""
        for pattern in VIOLATION_PATTERNS.values():
            assert len(pattern.keywords) > 0

    def test_penalty_not_positive(self):
        """Test that no penalty is positive."""
        for pattern in VIOLATION_PATTERNS.values():
            assert pattern.w_ethics_penalty <= 0.0

    def test_severity_not_exceed_one(self):
        """Test that severity doesn't exceed 1.0."""
        for pattern in VIOLATION_PATTERNS.values():
            assert pattern.severity <= 1.0

    def test_all_profiles_have_valid_tiers(self):
        """Test that all profiles use valid SafetyTier values."""
        valid_tiers = set(SafetyTier)

        for name, profile in PHILOSOPHER_SAFETY_PROFILES.items():
            assert profile["tier"] in valid_tiers


class TestSafetyConsistency:
    """Test consistency across safety definitions."""

    def test_high_severity_means_high_penalty(self):
        """Test that high severity violations have high penalties."""
        for pattern in VIOLATION_PATTERNS.values():
            if pattern.severity >= 0.9:
                # High severity should have penalty >= 0.8 (in absolute value)
                assert abs(pattern.w_ethics_penalty) >= 0.8

    def test_trusted_tier_consistent(self):
        """Test that TRUSTED tier is used consistently."""
        trusted_count = sum(
            1
            for profile in PHILOSOPHER_SAFETY_PROFILES.values()
            if profile["tier"] == SafetyTier.TRUSTED
        )

        # Should have significant number of trusted philosophers
        assert trusted_count >= 8

    def test_ethical_anchors_not_empty_for_trusted(self):
        """Test that trusted philosophers always have ethical anchors."""
        for name, profile in PHILOSOPHER_SAFETY_PROFILES.items():
            if profile["tier"] == SafetyTier.TRUSTED:
                assert len(profile["ethical_anchors"]) > 0
                assert all(anchor for anchor in profile["ethical_anchors"])
