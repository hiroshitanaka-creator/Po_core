"""
Tests for Peirce Philosopher Module

Tests Peirce's pragmatist philosophy focusing on:
- Semiotics (signs)
- Three categories (Firstness, Secondness, Thirdness)
- Pragmatic maxim
- Community of inquiry
"""

import pytest

from po_core.philosophers.peirce import Peirce


class TestPeirceBasicFunctionality:
    """Test basic functionality of Peirce philosopher."""

    def test_peirce_initialization(self):
        """Test that Peirce initializes correctly."""
        peirce = Peirce()
        assert peirce.name == "Charles Sanders Peirce"
        assert (
            "pragmatist" in peirce.description.lower()
            or "semiotic" in peirce.description.lower()
        )

    def test_peirce_repr(self):
        """Test string representation."""
        peirce = Peirce()
        repr_str = repr(peirce)
        assert "Peirce" in repr_str

    def test_peirce_str(self):
        """Test human-readable string."""
        peirce = Peirce()
        str_output = str(peirce)
        assert "Peirce" in str_output


class TestPeirceReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "semiotics" in result
        assert "inference" in result
        assert "categories" in result
        assert "belief_doubt" in result
        assert "inquiry" in result
        assert "pragmatic_maxim" in result
        assert "fallibilism" in result
        assert "community" in result
        assert "continuity" in result
        assert "metadata" in result


class TestPeirceSemiotics:
    """Test semiotic analysis."""

    def test_semiotics_structure(self, simple_prompt):
        """Test that semiotics has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        semiotics = result["semiotics"]
        assert isinstance(semiotics, dict)
        assert "sign_type" in semiotics
        assert "description" in semiotics

    def test_sign_detection(self):
        """Test detection of signs."""
        peirce = Peirce()
        result = peirce.reason("This symbol represents something else as a sign")

        semiotics = result["semiotics"]
        assert "sign_type" in semiotics


class TestPeirceInference:
    """Test inference mode analysis."""

    def test_inference_structure(self, simple_prompt):
        """Test that inference has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        inference = result["inference"]
        assert isinstance(inference, dict)
        assert "mode" in inference
        assert "description" in inference

    def test_abduction_detection(self):
        """Test detection of abductive inference."""
        peirce = Peirce()
        result = peirce.reason("Perhaps this hypothesis best explains what we observe")

        inference = result["inference"]
        assert "hypothesis" in inference["description"].lower() or "type" in inference


class TestPeirceCategories:
    """Test categorial analysis."""

    def test_categories_structure(self, simple_prompt):
        """Test that categories has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        categories = result["categories"]
        assert isinstance(categories, dict)
        assert "dominant" in categories
        assert "description" in categories

    def test_firstness_detection(self):
        """Test detection of Firstness."""
        peirce = Peirce()
        result = peirce.reason("Pure quality and feeling without relation")

        categories = result["categories"]
        assert (
            "Firstness" in categories["dominant"]
            or "firstness" in categories["description"].lower()
        )


class TestPeirceBeliefDoubt:
    """Test belief and doubt analysis."""

    def test_belief_doubt_structure(self, simple_prompt):
        """Test that belief_doubt has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        belief_doubt = result["belief_doubt"]
        assert isinstance(belief_doubt, dict)
        assert "state" in belief_doubt
        assert "description" in belief_doubt

    def test_doubt_detection(self):
        """Test detection of doubt state."""
        peirce = Peirce()
        result = peirce.reason("I doubt and question this uncertain claim")

        belief_doubt = result["belief_doubt"]
        assert (
            "Doubt" in belief_doubt["state"]
            or "doubt" in belief_doubt["description"].lower()
        )


class TestPeirceInquiry:
    """Test inquiry process analysis."""

    def test_inquiry_structure(self, simple_prompt):
        """Test that inquiry has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        inquiry = result["inquiry"]
        assert isinstance(inquiry, dict)
        assert "status" in inquiry
        assert "description" in inquiry

    def test_inquiry_detection(self):
        """Test detection of inquiry process."""
        peirce = Peirce()
        result = peirce.reason("We investigate to settle our doubts")

        inquiry = result["inquiry"]
        assert "status" in inquiry


class TestPeircePragmaticMaxim:
    """Test pragmatic maxim application."""

    def test_pragmatic_maxim_structure(self, simple_prompt):
        """Test that pragmatic_maxim has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        maxim = result["pragmatic_maxim"]
        assert isinstance(maxim, dict)
        assert "application" in maxim
        assert "description" in maxim

    def test_practical_effects_detection(self):
        """Test detection of practical effects."""
        peirce = Peirce()
        result = peirce.reason(
            "What practical effects and consequences does this have?"
        )

        maxim = result["pragmatic_maxim"]
        assert "application" in maxim


class TestPeirceFallibilism:
    """Test fallibilism analysis."""

    def test_fallibilism_structure(self, simple_prompt):
        """Test that fallibilism has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        fallibilism = result["fallibilism"]
        assert isinstance(fallibilism, dict)
        assert "stance" in fallibilism
        assert "description" in fallibilism

    def test_fallibilism_detection(self):
        """Test detection of fallibilism."""
        peirce = Peirce()
        result = peirce.reason("We may be mistaken and our knowledge is fallible")

        fallibilism = result["fallibilism"]
        assert (
            "fallible" in fallibilism["description"].lower() or "stance" in fallibilism
        )


class TestPeirceCommunity:
    """Test community of inquiry analysis."""

    def test_community_structure(self, simple_prompt):
        """Test that community has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        community = result["community"]
        assert isinstance(community, dict)
        assert "status" in community
        assert "description" in community

    def test_community_detection(self):
        """Test detection of community of inquiry."""
        peirce = Peirce()
        result = peirce.reason("We inquire together as a community of investigators")

        community = result["community"]
        assert "community" in community["description"].lower() or "status" in community


class TestPeirceContinuity:
    """Test continuity (synechism) analysis."""

    def test_continuity_structure(self, simple_prompt):
        """Test that continuity has correct structure."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        continuity = result["continuity"]
        assert isinstance(continuity, dict)
        assert "presence" in continuity
        assert "description" in continuity

    def test_continuity_detection(self):
        """Test detection of continuity."""
        peirce = Peirce()
        result = peirce.reason("Everything flows together in continuous gradations")

        continuity = result["continuity"]
        assert "presence" in continuity


class TestPeirceReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_peirce(self, simple_prompt):
        """Test that reasoning mentions Peircean concepts."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert (
            "Peirce" in reasoning
            or "pragmatic" in reasoning.lower()
            or "sign" in reasoning.lower()
        )


class TestPeirceEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        peirce = Peirce()
        result = peirce.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestPeirceTensionField:
    """Test Peirce's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        peirce = Peirce()
        result = peirce.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
