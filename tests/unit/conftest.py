import json
import pytest


@pytest.fixture()
def sample_prompt() -> str:
    return "What does it mean to live authentically?"


@pytest.fixture()
def load_json_output():
    def _loader(result) -> dict:
        return json.loads(result.output.strip())

    return _loader


# ==========================================
# Philosopher Test Fixtures
# ==========================================


@pytest.fixture()
def simple_prompt() -> str:
    """Simple prompt for basic philosopher tests."""
    return "What is the meaning of life?"


@pytest.fixture()
def existential_prompt() -> str:
    """Prompt with existential themes."""
    return "Should I choose freedom or accept my fate?"


@pytest.fixture()
def temporal_prompt() -> str:
    """Prompt with temporal dimensions (past, present, future)."""
    return "I was lost in the past, but now I am free to create my future."


@pytest.fixture()
def empty_prompt() -> str:
    """Empty prompt for edge case testing."""
    return ""


@pytest.fixture()
def long_prompt() -> str:
    """Long prompt for stress testing."""
    return " ".join(["This is a very long philosophical question about existence and meaning."] * 50)


@pytest.fixture()
def authentic_prompt() -> str:
    """Prompt suggesting authentic existence."""
    return "I take full responsibility for my choices and freely decide my own path."


@pytest.fixture()
def bad_faith_prompt() -> str:
    """Prompt suggesting bad faith / inauthenticity."""
    return "I am just following what everyone else does because that's how things are supposed to be."
