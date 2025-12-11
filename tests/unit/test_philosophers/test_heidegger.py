import pytest

from po_core.philosophers.heidegger import Heidegger


@pytest.fixture()
def heidegger_instance(heidegger):
    return heidegger


def test_reason_returns_expected_structure(heidegger_instance, philosopher_prompts):
    result = heidegger_instance.reason(philosopher_prompts["basic"])

    assert set(result.keys()) >= {
        "reasoning",
        "perspective",
        "tension",
        "key_concepts",
        "questions",
        "temporal_dimension",
        "authenticity_check",
        "metadata",
    }
    assert result["perspective"] == "Phenomenological / Existential"
    assert result["metadata"]["philosopher"] == "Martin Heidegger"
    assert result["metadata"]["approach"] == "Being and Time analysis"


def test_temporality_detection(heidegger_instance):
    prompt = "I was lost in the past, but I will find meaning tomorrow while I am choosing now."
    result = heidegger_instance.reason(prompt)

    temporality = result["temporal_dimension"]
    assert temporality["past_present"] is True
    assert temporality["future_oriented"] is True
    assert temporality["present_focused"] is True
    assert temporality["temporal_awareness"] == "Multi-temporal"


def test_authenticity_and_concepts_default(heidegger_instance, philosopher_prompts):
    empty_prompt = philosopher_prompts["empty"]
    result = heidegger_instance.reason(empty_prompt)

    assert "Being-in-the-world" in result["key_concepts"]
    assert "What is the mode of being here?" in result["questions"]
    assert result["authenticity_check"] == "Neutral - requires deeper analysis"


def test_inauthentic_mode_detection(heidegger_instance, philosopher_prompts):
    result = heidegger_instance.reason(philosopher_prompts["inauthentic"])

    assert result["authenticity_check"] == "Shows signs of 'Das Man' (they-self)"
    assert result["key_concepts"]


def test_handles_long_prompt(heidegger_instance, philosopher_prompts):
    result = heidegger_instance.reason(philosopher_prompts["long"])

    assert isinstance(result["reasoning"], str)
    assert len(result["reasoning"]) > 0
    assert isinstance(result["temporal_dimension"], dict)


class TestHeideggerTensionField:
    """Test Heidegger's tension field structure and content."""

    def test_tension_field_exists(self, heidegger):
        """Test that tension field is present in result."""
        result = heidegger.reason("What is the meaning of my existence?")

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, heidegger):
        """Test that tension field is a dictionary."""
        result = heidegger.reason("What is the meaning of my existence?")

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, heidegger):
        """Test that tension dict has all required keys."""
        result = heidegger.reason("What is the meaning of my existence?")

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, heidegger):
        """Test that tension level is one of the valid values."""
        result = heidegger.reason("What is the meaning of my existence?")

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, heidegger):
        """Test that tension description is a non-empty string."""
        result = heidegger.reason("What is the meaning of my existence?")

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, heidegger):
        """Test that tension elements is a list."""
        result = heidegger.reason("What is the meaning of my existence?")

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, heidegger):
        """Test that all tension elements are strings."""
        result = heidegger.reason("What is the meaning of my existence?")

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
