"""
Tests for Deleuze Philosopher Module

Tests Deleuze's philosophy focusing on:
- Rhizome vs Tree structures
- Difference and repetition
- Becoming and transformation
- Lines of flight
"""

from po_core.philosophers.deleuze import Deleuze


class TestDeleuzeBasicFunctionality:
    """Test basic functionality of Deleuze philosopher."""

    def test_deleuze_initialization(self):
        """Test that Deleuze initializes correctly."""
        deleuze = Deleuze()
        assert deleuze.name == "Gilles Deleuze"
        assert (
            "difference" in deleuze.description.lower()
            or "rhizome" in deleuze.description.lower()
        )

    def test_deleuze_repr(self):
        """Test string representation."""
        deleuze = Deleuze()
        repr_str = repr(deleuze)
        assert "Deleuze" in repr_str

    def test_deleuze_str(self):
        """Test human-readable string."""
        deleuze = Deleuze()
        str_output = str(deleuze)
        assert "Gilles Deleuze" in str_output


class TestDeleuzeReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "rhizome_vs_tree" in result
        assert "difference_repetition" in result
        assert "becoming" in result
        assert "body_without_organs" in result
        assert "lines_of_flight" in result
        assert "territorialization" in result
        assert "smooth_striated" in result
        assert "desire" in result
        assert "virtuality" in result
        assert "metadata" in result


class TestDeleuzeRhizome:
    """Test rhizome vs tree structure analysis."""

    def test_rhizome_structure(self, simple_prompt):
        """Test that rhizome has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        rhizome = result["rhizome_vs_tree"]
        assert isinstance(rhizome, dict)
        assert "structure" in rhizome
        assert "description" in rhizome

    def test_rhizome_detection(self):
        """Test detection of rhizomatic structure."""
        deleuze = Deleuze()
        result = deleuze.reason(
            "Multiple connections branching everywhere without center or hierarchy"
        )

        rhizome = result["rhizome_vs_tree"]
        assert (
            "Rhizome" in rhizome["structure"]
            or "rhizome" in rhizome["description"].lower()
        )

    def test_tree_detection(self):
        """Test detection of tree structure."""
        deleuze = Deleuze()
        result = deleuze.reason(
            "Hierarchical structure with roots, trunk, and linear branches"
        )

        rhizome = result["rhizome_vs_tree"]
        assert "structure" in rhizome


class TestDeleuzeDifference:
    """Test difference and repetition analysis."""

    def test_difference_structure(self, simple_prompt):
        """Test that difference has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        difference = result["difference_repetition"]
        assert isinstance(difference, dict)
        assert "orientation" in difference
        assert "description" in difference

    def test_difference_in_itself_detection(self):
        """Test detection of difference in itself."""
        deleuze = Deleuze()
        result = deleuze.reason(
            "Each thing differs from itself in becoming and variation"
        )

        difference = result["difference_repetition"]
        assert "orientation" in difference


class TestDeleuzeBecoming:
    """Test becoming analysis."""

    def test_becoming_structure(self, simple_prompt):
        """Test that becoming has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        becoming = result["becoming"]
        assert isinstance(becoming, dict)
        assert "presence" in becoming
        assert "description" in becoming

    def test_becoming_detection(self):
        """Test detection of becoming."""
        deleuze = Deleuze()
        result = deleuze.reason("I am becoming other, in flux and transformation")

        becoming = result["becoming"]
        assert (
            "Becoming" in becoming["presence"]
            or "becoming" in becoming["description"].lower()
        )


class TestDeleuzeBodyWithoutOrgans:
    """Test body without organs analysis."""

    def test_bwo_structure(self, simple_prompt):
        """Test that BwO has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        bwo = result["body_without_organs"]
        assert isinstance(bwo, dict)
        assert "status" in bwo
        assert "description" in bwo

    def test_bwo_detection(self):
        """Test detection of body without organs."""
        deleuze = Deleuze()
        result = deleuze.reason("Pure intensities without organization or structure")

        bwo = result["body_without_organs"]
        assert "status" in bwo


class TestDeleuzeLinesOfFlight:
    """Test lines of flight analysis."""

    def test_lines_structure(self, simple_prompt):
        """Test that lines of flight has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        lines = result["lines_of_flight"]
        assert isinstance(lines, dict)
        assert "presence" in lines
        assert "description" in lines

    def test_escape_detection(self):
        """Test detection of lines of flight."""
        deleuze = Deleuze()
        result = deleuze.reason("Breaking free and escaping the system")

        lines = result["lines_of_flight"]
        assert "presence" in lines


class TestDeleuzeTerritorialization:
    """Test territorialization analysis."""

    def test_territorialization_structure(self, simple_prompt):
        """Test that territorialization has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        territory = result["territorialization"]
        assert isinstance(territory, dict)
        assert "process" in territory
        assert "description" in territory

    def test_deterritorialization_detection(self):
        """Test detection of deterritorialization."""
        deleuze = Deleuze()
        result = deleuze.reason("Escaping and breaking down established territories")

        territory = result["territorialization"]
        assert "process" in territory


class TestDeleuzeSmoothStriated:
    """Test smooth vs striated space analysis."""

    def test_smooth_striated_structure(self, simple_prompt):
        """Test that smooth/striated has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        space = result["smooth_striated"]
        assert isinstance(space, dict)
        assert "type" in space
        assert "description" in space

    def test_smooth_space_detection(self):
        """Test detection of smooth space."""
        deleuze = Deleuze()
        result = deleuze.reason("Open nomadic wandering without fixed paths or rules")

        space = result["smooth_striated"]
        assert "type" in space


class TestDeleuzeDesire:
    """Test desire analysis."""

    def test_desire_structure(self, simple_prompt):
        """Test that desire has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        desire = result["desire"]
        assert isinstance(desire, dict)
        assert "conception" in desire
        assert "description" in desire

    def test_productive_desire_detection(self):
        """Test detection of productive desire."""
        deleuze = Deleuze()
        result = deleuze.reason("Desire produces and creates reality")

        desire = result["desire"]
        assert "conception" in desire


class TestDeleuzeVirtuality:
    """Test virtuality analysis."""

    def test_virtuality_structure(self, simple_prompt):
        """Test that virtuality has correct structure."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        virtuality = result["virtuality"]
        assert isinstance(virtuality, dict)
        assert "status" in virtuality
        assert "description" in virtuality

    def test_virtual_detection(self):
        """Test detection of virtuality."""
        deleuze = Deleuze()
        result = deleuze.reason("Potential realities waiting to actualize")

        virtuality = result["virtuality"]
        assert "status" in virtuality


class TestDeleuzeReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_deleuze(self, simple_prompt):
        """Test that reasoning mentions Deleuzian concepts."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert (
            "Deleuze" in reasoning
            or "difference" in reasoning.lower()
            or "rhizome" in reasoning.lower()
        )


class TestDeleuzeEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        deleuze = Deleuze()
        result = deleuze.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestDeleuzeTensionField:
    """Test Deleuze's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        deleuze = Deleuze()
        result = deleuze.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
