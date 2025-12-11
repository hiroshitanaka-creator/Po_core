"""
Tests for Dewey Philosopher Module

Tests Dewey's pragmatist philosophy focusing on:
- Experience (educative vs mis-educative)
- Inquiry process
- Growth and education
- Democratic quality
"""

import pytest

from po_core.philosophers.dewey import Dewey


class TestDeweyBasicFunctionality:
    """Test basic functionality of Dewey philosopher."""

    def test_dewey_initialization(self):
        """Test that Dewey initializes correctly."""
        dewey = Dewey()
        assert dewey.name == "John Dewey"
        assert "pragmatist" in dewey.description.lower()
        assert "experience" in dewey.description.lower()

    def test_dewey_repr(self):
        """Test string representation."""
        dewey = Dewey()
        repr_str = repr(dewey)
        assert "Dewey" in repr_str

    def test_dewey_str(self):
        """Test human-readable string."""
        dewey = Dewey()
        str_output = str(dewey)
        assert "🧠" in str_output
        assert "John Dewey" in str_output


class TestDeweyReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "experience_quality" in result
        assert "inquiry_stage" in result
        assert "growth_potential" in result
        assert "democratic_quality" in result
        assert "reflective_thinking" in result
        assert "habit_formation" in result
        assert "instrumentalism" in result
        assert "continuity_interaction" in result
        assert "metadata" in result


class TestDeweyExperience:
    """Test experience quality assessment."""

    def test_experience_structure(self, simple_prompt):
        """Test that experience has correct structure."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        experience = result["experience_quality"]
        assert isinstance(experience, dict)
        assert "quality" in experience
        assert "description" in experience
        assert "type" in experience

    def test_active_experience_detection(self):
        """Test detection of active experience."""
        dewey = Dewey()
        result = dewey.reason("I actively engage and interact with the world around me")

        experience = result["experience_quality"]
        assert "Active" in experience["quality"] or "Rich" in experience["quality"]

    def test_passive_experience_detection(self):
        """Test detection of passive reception."""
        dewey = Dewey()
        result = dewey.reason("I receive information and watch others")

        experience = result["experience_quality"]
        # Should detect some form of experience
        assert "quality" in experience


class TestDeweyInquiry:
    """Test inquiry stage evaluation."""

    def test_inquiry_structure(self, simple_prompt):
        """Test that inquiry has correct structure."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        inquiry = result["inquiry_stage"]
        assert isinstance(inquiry, dict)
        assert "stage" in inquiry
        assert "description" in inquiry
        assert "status" in inquiry

    def test_problem_recognition(self):
        """Test detection of problem recognition stage."""
        dewey = Dewey()
        result = dewey.reason("There is a problem that needs to be addressed")

        inquiry = result["inquiry_stage"]
        assert "Problem" in inquiry["stage"] or len(inquiry["stages_present"]) > 0

    def test_hypothesis_formation(self):
        """Test detection of hypothesis formation."""
        dewey = Dewey()
        result = dewey.reason("Perhaps if we try this hypothesis, it might work")

        inquiry = result["inquiry_stage"]
        assert "stages_present" in inquiry


class TestDeweyGrowth:
    """Test growth potential assessment."""

    def test_growth_structure(self, simple_prompt):
        """Test that growth has correct structure."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        growth = result["growth_potential"]
        assert isinstance(growth, dict)
        assert "potential" in growth
        assert "description" in growth
        assert "orientation" in growth

    def test_growth_oriented_detection(self):
        """Test detection of growth orientation."""
        dewey = Dewey()
        result = dewey.reason("I continue to grow, develop, and learn more")

        growth = result["growth_potential"]
        assert "Growth" in growth["potential"] or "growth" in growth["orientation"].lower()

    def test_static_mindset_detection(self):
        """Test detection of static mindset."""
        dewey = Dewey()
        result = dewey.reason("This is fixed and final, completely finished")

        growth = result["growth_potential"]
        assert "potential" in growth


class TestDeweyDemocracy:
    """Test democratic quality evaluation."""

    def test_democracy_structure(self, simple_prompt):
        """Test that democracy has correct structure."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        democracy = result["democratic_quality"]
        assert isinstance(democracy, dict)
        assert "quality" in democracy
        assert "description" in democracy
        assert "mode" in democracy

    def test_democratic_detection(self):
        """Test detection of democratic qualities."""
        dewey = Dewey()
        result = dewey.reason("We share, collaborate, and communicate together with mutual respect")

        democracy = result["democratic_quality"]
        assert "Democratic" in democracy["quality"] or "democratic" in democracy["mode"].lower()


class TestDeweyReflectiveThinking:
    """Test reflective thinking assessment."""

    def test_reflection_structure(self, simple_prompt):
        """Test that reflective thinking has correct structure."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        reflection = result["reflective_thinking"]
        assert isinstance(reflection, dict)
        assert "level" in reflection
        assert "description" in reflection

    def test_reflective_thinking_detection(self):
        """Test detection of reflective thinking."""
        dewey = Dewey()
        result = dewey.reason("I carefully reflect and consider the evidence to learn")

        reflection = result["reflective_thinking"]
        assert "Reflective" in reflection["level"] or "reflective" in reflection["type"].lower()


class TestDeweyHabitFormation:
    """Test habit formation assessment."""

    def test_habit_structure(self, simple_prompt):
        """Test that habit formation has correct structure."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        habit = result["habit_formation"]
        assert isinstance(habit, dict)
        assert "formation" in habit
        assert "description" in habit
        assert "quality" in habit

    def test_intelligent_habits_detection(self):
        """Test detection of intelligent habits."""
        dewey = Dewey()
        result = dewey.reason("I have flexible, adaptive habits that adjust thoughtfully")

        habit = result["habit_formation"]
        assert "habit" in habit["formation"].lower() or "quality" in habit


class TestDeweyInstrumentalism:
    """Test instrumentalism evaluation."""

    def test_instrumentalism_structure(self, simple_prompt):
        """Test that instrumentalism has correct structure."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        instrumentalism = result["instrumentalism"]
        assert isinstance(instrumentalism, dict)
        assert "level" in instrumentalism
        assert "description" in instrumentalism

    def test_pragmatic_orientation(self):
        """Test detection of pragmatic orientation."""
        dewey = Dewey()
        result = dewey.reason("This tool is useful and practical for solving problems")

        instrumentalism = result["instrumentalism"]
        assert "level" in instrumentalism


class TestDeweyContinuityInteraction:
    """Test continuity and interaction assessment."""

    def test_continuity_interaction_structure(self, simple_prompt):
        """Test that continuity_interaction has correct structure."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        continuity = result["continuity_interaction"]
        assert isinstance(continuity, dict)
        assert "quality" in continuity
        assert "description" in continuity

    def test_continuity_detection(self):
        """Test detection of continuity."""
        dewey = Dewey()
        result = dewey.reason("The past connects to the future and builds on what came before")

        continuity = result["continuity_interaction"]
        assert "Continuity" in continuity["quality"] or "continuity" in continuity["description"].lower()


class TestDeweyReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_dewey(self, simple_prompt):
        """Test that reasoning mentions Deweyan perspective."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert "Dewey" in reasoning or "pragmatist" in reasoning.lower()


class TestDeweyEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        dewey = Dewey()
        result = dewey.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestDeweyTensionField:
    """Test Dewey's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        dewey = Dewey()
        result = dewey.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
