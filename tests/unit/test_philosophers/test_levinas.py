"""
Tests for Levinas Philosopher Module

Tests Levinas's ethical philosophy focusing on:
- The Other and the Face
- Responsibility
- Totality vs Infinity
- Substitution and ethics
"""

import pytest

from po_core.philosophers.levinas import Levinas


class TestLevinasBasicFunctionality:
    """Test basic functionality of Levinas philosopher."""

    def test_levinas_initialization(self):
        """Test that Levinas initializes correctly."""
        levinas = Levinas()
        assert levinas.name == "Emmanuel Levinas"
        assert (
            "ethical" in levinas.description.lower() or "Other" in levinas.description
        )

    def test_levinas_repr(self):
        """Test string representation."""
        levinas = Levinas()
        repr_str = repr(levinas)
        assert "Levinas" in repr_str

    def test_levinas_str(self):
        """Test human-readable string."""
        levinas = Levinas()
        str_output = str(levinas)
        assert "🧠" in str_output
        assert "Emmanuel Levinas" in str_output


class TestLevinasReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "the_other" in result
        assert "face" in result
        assert "responsibility" in result
        assert "totality_vs_infinity" in result
        assert "same_vs_other" in result
        assert "substitution" in result
        assert "third_party" in result
        assert "saying_vs_said" in result
        assert "il_y_a" in result
        assert "metadata" in result


class TestLevinasTheOther:
    """Test analysis of the Other."""

    def test_other_structure(self, simple_prompt):
        """Test that the_other has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        other = result["the_other"]
        assert isinstance(other, dict)
        assert "presence" in other
        assert "description" in other

    def test_other_detection(self):
        """Test detection of the Other."""
        levinas = Levinas()
        result = levinas.reason(
            "I encounter the other person who calls me to responsibility"
        )

        other = result["the_other"]
        assert "Other" in other["presence"] or "other" in other["description"].lower()


class TestLevinasFace:
    """Test analysis of the Face."""

    def test_face_structure(self, simple_prompt):
        """Test that face has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        face = result["face"]
        assert isinstance(face, dict)
        assert "status" in face
        assert "description" in face

    def test_face_encounter_detection(self):
        """Test detection of face-to-face encounter."""
        levinas = Levinas()
        result = levinas.reason("The face of the other calls out thou shalt not kill")

        face = result["face"]
        assert "status" in face


class TestLevinasResponsibility:
    """Test responsibility analysis."""

    def test_responsibility_structure(self, simple_prompt):
        """Test that responsibility has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        responsibility = result["responsibility"]
        assert isinstance(responsibility, dict)
        assert "level" in responsibility
        assert "description" in responsibility

    def test_responsibility_detection(self):
        """Test detection of ethical responsibility."""
        levinas = Levinas()
        result = levinas.reason("I am responsible for the other before myself")

        responsibility = result["responsibility"]
        assert (
            "Responsibility" in responsibility["level"]
            or "responsible" in responsibility["description"].lower()
        )


class TestLevinasTotalityInfinity:
    """Test totality vs infinity analysis."""

    def test_totality_infinity_structure(self, simple_prompt):
        """Test that totality_vs_infinity has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        totality = result["totality_vs_infinity"]
        assert isinstance(totality, dict)
        assert "orientation" in totality
        assert "description" in totality

    def test_totality_detection(self):
        """Test detection of totality orientation."""
        levinas = Levinas()
        result = levinas.reason("Everything is encompassed in a complete system")

        totality = result["totality_vs_infinity"]
        assert (
            "Totality" in totality["orientation"]
            or "totality" in totality["description"].lower()
        )


class TestLevinasSameOther:
    """Test Same vs Other dialectic."""

    def test_same_other_structure(self, simple_prompt):
        """Test that same_vs_other has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        same_other = result["same_vs_other"]
        assert isinstance(same_other, dict)
        assert "relation" in same_other
        assert "description" in same_other

    def test_alterity_detection(self):
        """Test detection of radical alterity."""
        levinas = Levinas()
        result = levinas.reason("The other is absolutely other and different")

        same_other = result["same_vs_other"]
        assert "relation" in same_other


class TestLevinasSubstitution:
    """Test substitution analysis."""

    def test_substitution_structure(self, simple_prompt):
        """Test that substitution has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        substitution = result["substitution"]
        assert isinstance(substitution, dict)
        assert "presence" in substitution
        assert "description" in substitution

    def test_substitution_detection(self):
        """Test detection of substitution."""
        levinas = Levinas()
        result = levinas.reason("I take the place of the other and answer for them")

        substitution = result["substitution"]
        assert "presence" in substitution


class TestLevinasThirdParty:
    """Test third party (justice) analysis."""

    def test_third_party_structure(self, simple_prompt):
        """Test that third_party has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        third = result["third_party"]
        assert isinstance(third, dict)
        assert "presence" in third
        assert "description" in third

    def test_justice_detection(self):
        """Test detection of justice and third party."""
        levinas = Levinas()
        result = levinas.reason(
            "Justice requires comparing and weighing between many others"
        )

        third = result["third_party"]
        assert "presence" in third


class TestLevinasSayingSaid:
    """Test Saying vs Said analysis."""

    def test_saying_said_structure(self, simple_prompt):
        """Test that saying_vs_said has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        saying = result["saying_vs_said"]
        assert isinstance(saying, dict)
        assert "mode" in saying
        assert "description" in saying

    def test_saying_detection(self):
        """Test detection of the Saying."""
        levinas = Levinas()
        result = levinas.reason("The ethical event of speaking itself before content")

        saying = result["saying_vs_said"]
        assert "mode" in saying


class TestLevinasIlYA:
    """Test il y a (there is) analysis."""

    def test_il_y_a_structure(self, simple_prompt):
        """Test that il_y_a has correct structure."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        il_y_a = result["il_y_a"]
        assert isinstance(il_y_a, dict)
        assert "presence" in il_y_a
        assert "description" in il_y_a

    def test_il_y_a_detection(self):
        """Test detection of il y a."""
        levinas = Levinas()
        result = levinas.reason("Anonymous being, impersonal existence, there is")

        il_y_a = result["il_y_a"]
        assert "presence" in il_y_a


class TestLevinasReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_ethics(self, simple_prompt):
        """Test that reasoning mentions ethical concepts."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert (
            "Levinas" in reasoning
            or "Other" in reasoning
            or "responsibility" in reasoning.lower()
        )


class TestLevinasEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        levinas = Levinas()
        result = levinas.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestLevinasTensionField:
    """Test Levinas's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        levinas = Levinas()
        result = levinas.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
