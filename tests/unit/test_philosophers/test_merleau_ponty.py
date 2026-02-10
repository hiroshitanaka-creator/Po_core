"""
Tests for Merleau-Ponty Philosopher Module

Tests Merleau-Ponty's phenomenology focusing on:
- Lived body
- Perception
- Flesh and reversibility
- Being-in-the-world
"""

import pytest

from po_core.philosophers.merleau_ponty import MerleauPonty


class TestMerleauPontyBasicFunctionality:
    """Test basic functionality of Merleau-Ponty philosopher."""

    def test_merleau_ponty_initialization(self):
        """Test that Merleau-Ponty initializes correctly."""
        merleau_ponty = MerleauPonty()
        assert merleau_ponty.name == "Maurice Merleau-Ponty"
        assert (
            "embodiment" in merleau_ponty.description.lower()
            or "perception" in merleau_ponty.description.lower()
        )

    def test_merleau_ponty_repr(self):
        """Test string representation."""
        merleau_ponty = MerleauPonty()
        repr_str = repr(merleau_ponty)
        assert "MerleauPonty" in repr_str

    def test_merleau_ponty_str(self):
        """Test human-readable string."""
        merleau_ponty = MerleauPonty()
        str_output = str(merleau_ponty)
        assert "🧠" in str_output
        assert "Merleau-Ponty" in str_output


class TestMerleauPontyReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "lived_body" in result
        assert "perception" in result
        assert "flesh" in result
        assert "chiasm" in result
        assert "ambiguity" in result
        assert "being_in_world" in result
        assert "gestalt" in result
        assert "reversibility" in result
        assert "intersubjectivity" in result
        assert "metadata" in result


class TestMerleauPontyLivedBody:
    """Test lived body analysis."""

    def test_lived_body_structure(self, simple_prompt):
        """Test that lived_body has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        lived_body = result["lived_body"]
        assert isinstance(lived_body, dict)
        assert "status" in lived_body
        assert "description" in lived_body

    def test_body_subject_detection(self):
        """Test detection of body as subject."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason("My body knows how to grasp and move")

        lived_body = result["lived_body"]
        assert (
            "Body" in lived_body["status"]
            or "body" in lived_body["description"].lower()
        )


class TestMerleauPontyPerception:
    """Test perception analysis."""

    def test_perception_structure(self, simple_prompt):
        """Test that perception has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        perception = result["perception"]
        assert isinstance(perception, dict)
        assert "status" in perception
        assert "description" in perception

    def test_direct_perception_detection(self):
        """Test detection of direct perception."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(
            "I directly perceive the world immediately present"
        )

        perception = result["perception"]
        assert (
            "Perception" in perception["status"]
            or "perception" in perception["description"].lower()
        )


class TestMerleauPontyFlesh:
    """Test flesh analysis."""

    def test_flesh_structure(self, simple_prompt):
        """Test that flesh has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        flesh = result["flesh"]
        assert isinstance(flesh, dict)
        assert "presence" in flesh
        assert "description" in flesh

    def test_flesh_detection(self):
        """Test detection of the flesh."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(
            "The flesh is both sensible and sentient, sensing and sensed"
        )

        flesh = result["flesh"]
        assert "presence" in flesh


class TestMerleauPontyChiasm:
    """Test chiasm analysis."""

    def test_chiasm_structure(self, simple_prompt):
        """Test that chiasm has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        chiasm = result["chiasm"]
        assert isinstance(chiasm, dict)
        assert "status" in chiasm
        assert "description" in chiasm

    def test_chiasm_detection(self):
        """Test detection of chiasmic intertwining."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason("The seer and seen intertwine and cross over")

        chiasm = result["chiasm"]
        assert "status" in chiasm


class TestMerleauPontyAmbiguity:
    """Test ambiguity analysis."""

    def test_ambiguity_structure(self, simple_prompt):
        """Test that ambiguity has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        ambiguity = result["ambiguity"]
        assert isinstance(ambiguity, dict)
        assert "presence" in ambiguity
        assert "description" in ambiguity

    def test_ambiguity_detection(self):
        """Test detection of fundamental ambiguity."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(
            "Both and neither, ambiguous and indeterminate at once"
        )

        ambiguity = result["ambiguity"]
        assert (
            "Ambiguity" in ambiguity["presence"]
            or "ambiguity" in ambiguity["description"].lower()
        )


class TestMerleauPontyBeingInWorld:
    """Test being-in-the-world analysis."""

    def test_being_in_world_structure(self, simple_prompt):
        """Test that being_in_world has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        being_in_world = result["being_in_world"]
        assert isinstance(being_in_world, dict)
        assert "status" in being_in_world
        assert "description" in being_in_world

    def test_being_in_world_detection(self):
        """Test detection of being-in-the-world."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(
            "I am situated and immersed in the world around me"
        )

        being_in_world = result["being_in_world"]
        assert "status" in being_in_world


class TestMerleauPontyGestalt:
    """Test gestalt analysis."""

    def test_gestalt_structure(self, simple_prompt):
        """Test that gestalt has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        gestalt = result["gestalt"]
        assert isinstance(gestalt, dict)
        assert "presence" in gestalt
        assert "description" in gestalt

    def test_gestalt_detection(self):
        """Test detection of gestalt structures."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(
            "The whole structure and pattern with figure and ground"
        )

        gestalt = result["gestalt"]
        assert (
            "Gestalt" in gestalt["presence"]
            or "gestalt" in gestalt["description"].lower()
        )


class TestMerleauPontyReversibility:
    """Test reversibility analysis."""

    def test_reversibility_structure(self, simple_prompt):
        """Test that reversibility has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        reversibility = result["reversibility"]
        assert isinstance(reversibility, dict)
        assert "status" in reversibility
        assert "description" in reversibility

    def test_reversibility_detection(self):
        """Test detection of reversibility."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(
            "Touching and touched, my hand touches my other hand"
        )

        reversibility = result["reversibility"]
        assert (
            "Reversibility" in reversibility["status"]
            or "reversib" in reversibility["description"].lower()
        )


class TestMerleauPontyIntersubjectivity:
    """Test intersubjectivity analysis."""

    def test_intersubjectivity_structure(self, simple_prompt):
        """Test that intersubjectivity has correct structure."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        intersubjectivity = result["intersubjectivity"]
        assert isinstance(intersubjectivity, dict)
        assert "status" in intersubjectivity
        assert "description" in intersubjectivity

    def test_intersubjectivity_detection(self):
        """Test detection of intersubjectivity."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(
            "I perceive other bodies and share the world with others"
        )

        intersubjectivity = result["intersubjectivity"]
        assert "status" in intersubjectivity


class TestMerleauPontyReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_phenomenology(self, simple_prompt):
        """Test that reasoning mentions phenomenological concepts."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert (
            "Merleau-Pont" in reasoning
            or "body" in reasoning.lower()
            or "perception" in reasoning.lower()
        )


class TestMerleauPontyEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestMerleauPontyTensionField:
    """Test Merleau-Ponty's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        merleau_ponty = MerleauPonty()
        result = merleau_ponty.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
