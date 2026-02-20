import pytest


@pytest.fixture()
def sartre_instance(sartre):
    return sartre


def test_reason_returns_expected_structure(sartre_instance, philosopher_prompts):
    result = sartre_instance.reason(philosopher_prompts["basic"])

    assert set(result.keys()) >= {
        "reasoning",
        "perspective",
        "tension",
        "freedom_assessment",
        "responsibility_check",
        "bad_faith_indicators",
        "mode_of_being",
        "engagement_level",
        "anguish_present",
        "metadata",
    }
    assert result["perspective"] == "Existentialist"
    assert result["metadata"]["philosopher"] == "Jean-Paul Sartre"
    assert result["metadata"]["approach"] == "Existentialist analysis"


def test_freedom_and_responsibility_detection(sartre_instance):
    prompt = "I choose to act and feel responsible for the consequences of my freedom."
    result = sartre_instance.reason(prompt)

    assert result["freedom_assessment"]["level"] == "High"
    assert result["responsibility_check"]["level"] == "High"
    assert result["mode_of_being"].startswith("For-itself")


def test_bad_faith_detection(sartre_instance, philosopher_prompts):
    prompt = "They made me do it; I had no choice and was supposed to follow the rules."
    result = sartre_instance.reason(prompt)

    indicators = result["bad_faith_indicators"]
    assert any("denying agency" in item for item in indicators)
    assert any("Role-playing" in item for item in indicators)


def test_edge_case_empty_prompt(sartre_instance, philosopher_prompts):
    result = sartre_instance.reason(philosopher_prompts["empty"])

    assert result["freedom_assessment"]["level"] == "Medium"
    assert result["responsibility_check"]["level"] == "Low"
    assert "No obvious bad faith detected" in result["bad_faith_indicators"][0]


def test_long_prompt_handles_multiple_signals(sartre_instance, philosopher_prompts):
    result = sartre_instance.reason(philosopher_prompts["long"])

    assert result["freedom_assessment"]["level"] != "Low"
    assert isinstance(result["reasoning"], str)
    assert len(result["reasoning"]) > 0


class TestSartreTensionField:
    """Test Sartre's tension field structure and content."""

    def test_tension_field_exists(self, sartre):
        """Test that tension field is present in result."""
        result = sartre.reason("What does it mean to be free?")

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, sartre):
        """Test that tension field is a dictionary."""
        result = sartre.reason("What does it mean to be free?")

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, sartre):
        """Test that tension dict has all required keys."""
        result = sartre.reason("What does it mean to be free?")

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, sartre):
        """Test that tension level is one of the valid values."""
        result = sartre.reason("What does it mean to be free?")

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, sartre):
        """Test that tension description is a non-empty string."""
        result = sartre.reason("What does it mean to be free?")

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, sartre):
        """Test that tension elements is a list."""
        result = sartre.reason("What does it mean to be free?")

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, sartre):
        """Test that all tension elements are strings."""
        result = sartre.reason("What does it mean to be free?")

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
