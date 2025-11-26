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
