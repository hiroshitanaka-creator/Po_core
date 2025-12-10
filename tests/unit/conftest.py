import json
import pytest

from po_core.philosophers.heidegger import Heidegger
from po_core.philosophers.sartre import Sartre

@pytest.fixture()
def sample_prompt() -> str:
    return "What does it mean to live authentically?"


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

    long_prompt = " ".join([
        "Freedom presses on every decision we make, even when we pretend otherwise.",
        "I was once convinced my path was fixed, but tomorrow I will choose again.",
        "In this moment, I feel the weight of time and responsibility intertwining."
    ])

    return {
        "basic": "I choose my own path now, and I will shape tomorrow.",
        "empty": "",
        "long": long_prompt,
        "inauthentic": "Everyone says I must do this because that's just how life is."
    }
