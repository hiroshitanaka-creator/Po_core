import json

import pytest

from po_core.philosophers.heidegger import Heidegger
from po_core.philosophers.sartre import Sartre


@pytest.fixture()
def sample_prompt() -> str:
    return "What does it mean to live authentically?"


@pytest.fixture()
def simple_prompt() -> str:
    """Simple prompt for philosopher tests."""
    return "What is the meaning of life?"


@pytest.fixture()
def existential_prompt() -> str:
    """Existential prompt for philosopher tests."""
    return "I stand before an abyss of choices, wondering if any path leads to authentic existence."


@pytest.fixture()
def ethical_prompt() -> str:
    """Ethical prompt for philosopher tests."""
    return "Should I act for the greater good, even if it means sacrificing my own happiness?"


@pytest.fixture()
def complex_prompt() -> str:
    """Complex multi-layered prompt for philosopher tests."""
    return "In a world where technology shapes our reality, how do we maintain our humanity while embracing progress, and what does it mean to live authentically in such a context?"


@pytest.fixture()
def empty_prompt() -> str:
    """Empty prompt for edge case tests."""
    return ""


@pytest.fixture()
def long_prompt() -> str:
    """Long prompt for testing philosopher reasoning with extended input."""
    return " ".join(
        [
            "Freedom presses on every decision we make, even when we pretend otherwise.",
            "I was once convinced my path was fixed, but tomorrow I will choose again.",
            "In this moment, I feel the weight of time and responsibility intertwining.",
            "The world around me seems predetermined, yet I sense the possibility of authentic choice.",
            "How can I navigate between social expectations and genuine self-determination?",
            "Each moment presents a new opportunity to affirm or deny my essential freedom.",
        ]
    )


@pytest.fixture()
def load_json_output():
    def _loader(result) -> dict:
        return json.loads(result.output.strip())

    return _loader


@pytest.fixture()
def heidegger():
    return Heidegger()


@pytest.fixture()
def sartre():
    return Sartre()


@pytest.fixture()
def philosopher_prompts():
    """Common prompts used across philosopher tests."""

    long_prompt = " ".join(
        [
            "Freedom presses on every decision we make, even when we pretend otherwise.",
            "I was once convinced my path was fixed, but tomorrow I will choose again.",
            "In this moment, I feel the weight of time and responsibility intertwining.",
        ]
    )

    return {
        "basic": "I choose my own path now, and I will shape tomorrow.",
        "empty": "",
        "long": long_prompt,
        "inauthentic": "Everyone says I must do this because that's just how life is.",
    }
