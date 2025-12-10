import pytest

from po_core.philosophers.sartre import Sartre


@pytest.fixture()
def sartre_instance(sartre):
    return sartre


def test_reason_returns_expected_structure(sartre_instance, philosopher_prompts):
    result = sartre_instance.reason(philosopher_prompts["basic"])

    assert set(result.keys()) >= {
        "reasoning",
        "perspective",
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
