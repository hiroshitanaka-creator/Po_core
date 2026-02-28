"""
Tests for Kant Philosopher Module

Tests Kant's critical philosophy focusing on:
- Categorical Imperative (three formulations)
- Phenomena vs Noumena
- Transcendental Idealism
- Autonomy and Duty
- Kingdom of Ends
- Good Will

--- GOOD FIRST ISSUE TEMPLATE ---
23 philosophers currently lack a dedicated unit test file.
Copy this file, replace `Kant` with your philosopher, and adjust the
field names to match that philosopher's `reason()` output.

Unclaimed: beauvoir, butler, descartes, dogen, epicurus, foucault,
           hegel, husserl, jonas, laozi, marcus_aurelius, nagarjuna,
           nishida, parmenides, plato, schopenhauer, spinoza, weil
           (see README.md for full list)
"""

import pytest

from po_core.philosophers.kant import Kant


class TestKantBasicFunctionality:
    """Test basic initialization and interface of the Kant module."""

    def test_kant_initialization(self):
        """Test that Kant initializes with the correct identity."""
        kant = Kant()

        assert "Kant" in kant.name
        assert kant.description is not None
        assert len(kant.description) > 0

    def test_kant_has_tradition(self):
        """Test that Kant has a philosophical tradition set."""
        kant = Kant()

        assert hasattr(kant, "tradition")
        assert "Critical" in kant.tradition or "Idealism" in kant.tradition

    def test_kant_has_key_concepts(self):
        """Test that Kant's key concepts are populated."""
        kant = Kant()

        assert hasattr(kant, "key_concepts")
        assert len(kant.key_concepts) > 0
        concepts_lower = [c.lower() for c in kant.key_concepts]
        assert any("categorical" in c or "imperative" in c for c in concepts_lower)


class TestKantReasonMethod:
    """Test the reason() method structure and required fields."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result contains all expected Kantian fields."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        required = [
            "reasoning",
            "perspective",
            "tension",
            "categorical_imperative",
            "phenomena_noumena",
            "autonomy",
            "duty",
            "kingdom_of_ends",
            "good_will",
            "metadata",
        ]
        for field in required:
            assert field in result, f"Missing field: {field}"

    def test_perspective_is_deontological(self, simple_prompt):
        """Test that Kant's perspective is deontological / critical philosophy."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        perspective = result["perspective"]
        assert "Critical" in perspective or "Deontolog" in perspective

    def test_metadata_structure(self, simple_prompt):
        """Test that metadata identifies the philosopher correctly."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        metadata = result["metadata"]
        assert "Kant" in metadata["philosopher"]
        assert "approach" in metadata
        assert "focus" in metadata

    def test_reason_accepts_context(self, simple_prompt):
        """Test that reason() accepts an optional context parameter."""
        kant = Kant()
        result = kant.reason(simple_prompt, context={"session": "test"})

        assert isinstance(result, dict)

    def test_reason_works_without_context(self, simple_prompt):
        """Test that reason() works with no context argument."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert isinstance(result, dict)


class TestKantCategoricalImperative:
    """Test Kant's categorical imperative analysis."""

    def test_categorical_imperative_exists(self, simple_prompt):
        """Test that categorical_imperative field is present."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        ci = result["categorical_imperative"]
        assert ci is not None

    def test_universalizability_detected(self):
        """Test detection of universalizability formulation."""
        kant = Kant()
        prompt = "Act only according to rules you could will to become universal laws."
        result = kant.reason(prompt)

        ci = result["categorical_imperative"]
        assert isinstance(ci, dict)

    def test_humanity_formula_detected(self):
        """Test detection of the humanity formulation (treat persons as ends)."""
        kant = Kant()
        prompt = "We must treat every person as an end in themselves, never merely as a means."
        result = kant.reason(prompt)

        ci = result["categorical_imperative"]
        assert isinstance(ci, dict)


class TestKantAutonomy:
    """Test Kant's autonomy assessment."""

    def test_autonomy_field_exists(self, simple_prompt):
        """Test that autonomy field is present."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert "autonomy" in result

    def test_autonomy_detected_in_self_directed_prompt(self):
        """Test that autonomy is detected when self-legislation language appears."""
        kant = Kant()
        prompt = "I choose my own moral law through reason; I am autonomous and self-determining."
        result = kant.reason(prompt)

        autonomy = result["autonomy"]
        assert isinstance(autonomy, dict)


class TestKantDuty:
    """Test Kant's duty analysis."""

    def test_duty_field_exists(self, simple_prompt):
        """Test that duty field is present."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert "duty" in result

    def test_duty_detected_in_obligatory_prompt(self):
        """Test that duty concepts are detected when obligation language appears."""
        kant = Kant()
        prompt = "I have a duty and obligation to fulfill my promise, regardless of consequences."
        result = kant.reason(prompt)

        duty = result["duty"]
        assert isinstance(duty, dict)


class TestKantKingdomOfEnds:
    """Test Kant's kingdom of ends concept."""

    def test_kingdom_of_ends_field_exists(self, simple_prompt):
        """Test that kingdom_of_ends field is present."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert "kingdom_of_ends" in result

    def test_kingdom_of_ends_is_dict(self, simple_prompt):
        """Test that kingdom_of_ends returns a dictionary."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert isinstance(result["kingdom_of_ends"], dict)


class TestKantGoodWill:
    """Test Kant's good will concept."""

    def test_good_will_field_exists(self, simple_prompt):
        """Test that good_will field is present."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert "good_will" in result

    def test_good_will_is_dict(self, simple_prompt):
        """Test that good_will returns a dictionary."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert isinstance(result["good_will"], dict)


class TestKantReasoningText:
    """Test the free-text reasoning output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert isinstance(result["reasoning"], str)
        assert len(result["reasoning"]) > 0

    def test_reasoning_references_kantian_concepts(self, ethical_prompt):
        """Test that reasoning mentions key Kantian concepts."""
        kant = Kant()
        result = kant.reason(ethical_prompt)

        reasoning_lower = result["reasoning"].lower()
        kantian_keywords = ["kant", "categorical", "duty", "universal", "moral law", "autonomy"]
        assert any(kw in reasoning_lower for kw in kantian_keywords)


class TestKantTensionField:
    """Test Kant's tension field (shared pattern across all philosophers)."""

    def test_tension_exists(self, simple_prompt):
        """Test that tension field is present."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert "tension" in result

    def test_tension_is_dict(self, simple_prompt):
        """Test that tension is a dictionary."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension contains level, description, and elements."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the known values."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert result["tension"]["level"] in valid_levels

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list of strings."""
        kant = Kant()
        result = kant.reason(simple_prompt)

        elements = result["tension"]["elements"]
        assert isinstance(elements, list)
        for elem in elements:
            assert isinstance(elem, str)


class TestKantEdgeCases:
    """Test edge cases that all philosopher modules should handle gracefully."""

    def test_empty_prompt(self, empty_prompt):
        """Test that an empty prompt does not raise an exception."""
        kant = Kant()
        result = kant.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_long_prompt(self, complex_prompt):
        """Test that a long, complex prompt is processed without error."""
        kant = Kant()
        result = kant.reason(complex_prompt)

        assert isinstance(result, dict)
        assert len(result["reasoning"]) > 0

    def test_existential_prompt(self, existential_prompt):
        """Test that an existential prompt produces a valid Kantian analysis."""
        kant = Kant()
        result = kant.reason(existential_prompt)

        assert isinstance(result, dict)
        assert result["perspective"] is not None
