"""
Tests for Kierkegaard Philosopher Module

Tests Kierkegaard's existentialist philosophy focusing on:
- Life stages (aesthetic, ethical, religious)
- Anxiety and despair
- Faith and the leap
- Subjectivity and individuality
"""

from po_core.philosophers.kierkegaard import Kierkegaard


class TestKierkegaardBasicFunctionality:
    """Test basic functionality of Kierkegaard philosopher."""

    def test_kierkegaard_initialization(self):
        """Test that Kierkegaard initializes correctly."""
        kierkegaard = Kierkegaard()
        assert kierkegaard.name == "Søren Kierkegaard"
        assert (
            "existentialist" in kierkegaard.description.lower()
            or "existence" in kierkegaard.description.lower()
        )

    def test_kierkegaard_repr(self):
        """Test string representation."""
        kierkegaard = Kierkegaard()
        repr_str = repr(kierkegaard)
        assert "Kierkegaard" in repr_str

    def test_kierkegaard_str(self):
        """Test human-readable string."""
        kierkegaard = Kierkegaard()
        str_output = str(kierkegaard)
        assert "Kierkegaard" in str_output


class TestKierkegaardReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "life_stage" in result
        assert "anxiety" in result
        assert "despair" in result
        assert "faith" in result
        assert "subjectivity" in result
        assert "individuality" in result
        assert "paradox" in result
        assert "leap" in result
        assert "moment" in result
        assert "metadata" in result


class TestKierkegaardLifeStages:
    """Test life stage identification."""

    def test_life_stage_structure(self, simple_prompt):
        """Test that life stage has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        life_stage = result["life_stage"]
        assert isinstance(life_stage, dict)
        assert "stage" in life_stage
        assert "description" in life_stage

    def test_aesthetic_stage_detection(self):
        """Test detection of aesthetic stage."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("I seek pleasure and immediate enjoyment")

        life_stage = result["life_stage"]
        assert (
            "Aesthetic" in life_stage["stage"]
            or "aesthetic" in life_stage["description"].lower()
        )

    def test_ethical_stage_detection(self):
        """Test detection of ethical stage."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(
            "I choose to commit to duty and moral responsibility"
        )

        life_stage = result["life_stage"]
        assert "stage" in life_stage

    def test_religious_stage_detection(self):
        """Test detection of religious stage."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("I have faith in the absolute and trust in God")

        life_stage = result["life_stage"]
        assert "stage" in life_stage


class TestKierkegaardAnxiety:
    """Test anxiety analysis."""

    def test_anxiety_structure(self, simple_prompt):
        """Test that anxiety has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        anxiety = result["anxiety"]
        assert isinstance(anxiety, dict)
        assert "intensity" in anxiety
        assert "description" in anxiety

    def test_anxiety_detection(self):
        """Test detection of anxiety."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(
            "I feel anxious about infinite possibilities and freedom"
        )

        anxiety = result["anxiety"]
        assert (
            "anxiety" in anxiety["description"].lower()
            or "Anxiety" in anxiety["presence"]
        )


class TestKierkegaardDespair:
    """Test despair analysis."""

    def test_despair_structure(self, simple_prompt):
        """Test that despair has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        despair = result["despair"]
        assert isinstance(despair, dict)
        assert "depth" in despair
        assert "description" in despair

    def test_despair_detection(self):
        """Test detection of despair."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("I despair and am not myself")

        despair = result["despair"]
        assert "depth" in despair


class TestKierkegaardFaith:
    """Test faith assessment."""

    def test_faith_structure(self, simple_prompt):
        """Test that faith has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        faith = result["faith"]
        assert isinstance(faith, dict)
        assert "type" in faith
        assert "description" in faith

    def test_faith_detection(self):
        """Test detection of faith."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("I have faith and trust in what transcends reason")

        faith = result["faith"]
        assert "type" in faith


class TestKierkegaardSubjectivity:
    """Test subjectivity evaluation."""

    def test_subjectivity_structure(self, simple_prompt):
        """Test that subjectivity has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        subjectivity = result["subjectivity"]
        assert isinstance(subjectivity, dict)
        assert "orientation" in subjectivity
        assert "description" in subjectivity

    def test_subjective_truth_detection(self):
        """Test detection of subjective truth."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("Truth is subjective and personal to my existence")

        subjectivity = result["subjectivity"]
        assert "orientation" in subjectivity


class TestKierkegaardIndividuality:
    """Test individuality assessment."""

    def test_individuality_structure(self, simple_prompt):
        """Test that individuality has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        individuality = result["individuality"]
        assert isinstance(individuality, dict)
        assert "status" in individuality
        assert "description" in individuality

    def test_individual_emphasis_detection(self):
        """Test detection of individual emphasis."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("I am a unique individual before God")

        individuality = result["individuality"]
        assert "status" in individuality


class TestKierkegaardParadox:
    """Test paradox detection."""

    def test_paradox_structure(self, simple_prompt):
        """Test that paradox has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        paradox = result["paradox"]
        assert isinstance(paradox, dict)
        assert "presence" in paradox
        assert "description" in paradox

    def test_paradox_detection(self):
        """Test detection of paradox."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("This absurd paradox defies all reason")

        paradox = result["paradox"]
        assert "presence" in paradox


class TestKierkegaardLeap:
    """Test leap of faith analysis."""

    def test_leap_structure(self, simple_prompt):
        """Test that leap has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        leap = result["leap"]
        assert isinstance(leap, dict)
        assert "status" in leap
        assert "description" in leap

    def test_leap_detection(self):
        """Test detection of leap of faith."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("I must leap beyond reason and choose")

        leap = result["leap"]
        assert "status" in leap


class TestKierkegaardMoment:
    """Test moment/instant analysis."""

    def test_moment_structure(self, simple_prompt):
        """Test that moment has correct structure."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        moment = result["moment"]
        assert isinstance(moment, dict)
        assert "significance" in moment
        assert "description" in moment

    def test_moment_detection(self):
        """Test detection of decisive moment."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason("In this moment I must choose and decide now")

        moment = result["moment"]
        assert "significance" in moment


class TestKierkegaardReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_existence(self, simple_prompt):
        """Test that reasoning mentions existential themes."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert (
            "Kierkegaard" in reasoning
            or "existence" in reasoning.lower()
            or "individual" in reasoning.lower()
        )


class TestKierkegaardEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestKierkegaardTensionField:
    """Test Kierkegaard's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        kierkegaard = Kierkegaard()
        result = kierkegaard.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
