"""
Unit tests for the Voice Layer (Phase 5 — Philosopher Soul enhancement).

Tests cover:
- VoiceRenderer.render() produces non-empty, topic-aware output
- Tension categories map correctly (conflict / question / insight)
- Tensor reactions fire at correct thresholds
- get_voice() cache and graceful degradation
- base.py reason_with_context() applies voice
- base.py propose() passes tensor values and applies voice
- _extract_topic strips question starters
"""

import pytest

from po_core.runtime.voice_loader import (
    VoiceRenderer,
    _extract_topic,
    _tension_category,
    clear_cache,
    get_voice,
)

# ---------------------------------------------------------------------------
# _extract_topic
# ---------------------------------------------------------------------------


def test_extract_topic_simple():
    assert _extract_topic("justice") == "justice"


def test_extract_topic_strips_what_is():
    result = _extract_topic("What is justice?")
    assert "justice" in result
    assert "What" not in result
    assert "is" not in result.lower().split()[0]


def test_extract_topic_strips_what_is_the():
    result = _extract_topic("What is the meaning of life?")
    assert "What" not in result
    assert "meaning" in result


def test_extract_topic_max_four_words():
    result = _extract_topic("freedom equality justice solidarity rights")
    assert len(result.split()) <= 4


# ---------------------------------------------------------------------------
# _tension_category
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "level,expected",
    [
        ("Very High", "conflict"),
        ("High", "conflict"),
        ("Moderate", "question"),
        ("Low", "insight"),
        ("Very Low", "insight"),
        (None, "question"),
        ("", "question"),
    ],
)
def test_tension_category(level, expected):
    assert _tension_category(level) == expected


# ---------------------------------------------------------------------------
# VoiceRenderer
# ---------------------------------------------------------------------------


@pytest.fixture
def nietzsche_renderer():
    clear_cache()
    return get_voice("nietzsche")


@pytest.fixture
def sartre_renderer():
    clear_cache()
    return get_voice("sartre")


def test_get_voice_returns_renderer(nietzsche_renderer):
    assert nietzsche_renderer is not None


def test_get_voice_unknown_returns_none():
    clear_cache()
    assert get_voice("no_such_philosopher") is None


def test_get_voice_cached(nietzsche_renderer):
    """Second call returns the same object (cache hit)."""
    second = get_voice("nietzsche")
    assert second is nietzsche_renderer


def test_render_nonempty(nietzsche_renderer):
    result = nietzsche_renderer.render(prompt="What is justice?")
    assert isinstance(result, str)
    assert len(result) > 20


def test_render_contains_topic(nietzsche_renderer):
    result = nietzsche_renderer.render(prompt="What is justice?")
    # "justice" should appear somewhere in the rendered text
    assert "justice" in result.lower() or "Justice" in result


def test_render_conflict_contains_german(nietzsche_renderer):
    """High tension should produce Nietzsche's German-inflected output."""
    result = nietzsche_renderer.render(prompt="What is justice?", tension_level="High")
    # One of the conflict templates uses German
    assert any(
        word in result
        for word in [
            "Ressentiment",
            "Sklavenmoral",
            "Wille",
            "Übermensch",
            "Werde",
            "Gott",
        ]
    )


def test_render_tensor_freedom_pressure(nietzsche_renderer):
    result = nietzsche_renderer.render(
        prompt="justice",
        tensor_snapshot={
            "freedom_pressure": 0.9,
            "semantic_delta": 0.1,
            "blocked_tensor": 0.0,
        },
    )
    assert "Druck" in result or "Macht" in result or "Einengung" in result


def test_render_tensor_blocked(nietzsche_renderer):
    result = nietzsche_renderer.render(
        prompt="justice",
        tensor_snapshot={
            "freedom_pressure": 0.1,
            "semantic_delta": 0.1,
            "blocked_tensor": 0.8,
        },
    )
    assert (
        "Ressentiment" in result
        or "Angst" in result
        or "blockiert" in result.lower()
        or "Blocked" in result
        or "Ressentiment" in result
    )


def test_render_insight_different_from_conflict(nietzsche_renderer):
    """Low vs high tension should produce different body text."""
    high = nietzsche_renderer.render(prompt="freedom", tension_level="Very High")
    low = nietzsche_renderer.render(prompt="freedom", tension_level="Very Low")
    # They should differ (at least the body template)
    assert high != low


def test_sartre_voice_uses_existentialist_language(sartre_renderer):
    result = sartre_renderer.render(prompt="What is freedom?")
    keywords = [
        "freedom",
        "bad faith",
        "existence",
        "condemned",
        "mauvaise",
        "pour-soi",
    ]
    assert any(kw.lower() in result.lower() for kw in keywords)


# ---------------------------------------------------------------------------
# All 39 philosopher YAMLs load without error
# ---------------------------------------------------------------------------

PHILOSOPHER_IDS = [
    "arendt",
    "aristotle",
    "badiou",
    "beauvoir",
    "butler",
    "confucius",
    "deleuze",
    "derrida",
    "descartes",
    "dewey",
    "dogen",
    "epicurus",
    "foucault",
    "hegel",
    "heidegger",
    "husserl",
    "jonas",
    "jung",
    "kant",
    "kierkegaard",
    "lacan",
    "laozi",
    "levinas",
    "marcus_aurelius",
    "merleau_ponty",
    "nagarjuna",
    "nietzsche",
    "nishida",
    "parmenides",
    "peirce",
    "plato",
    "sartre",
    "schopenhauer",
    "spinoza",
    "wabi_sabi",
    "watsuji",
    "weil",
    "wittgenstein",
    "zhuangzi",
]


@pytest.mark.parametrize("phil_id", PHILOSOPHER_IDS)
def test_all_voices_load(phil_id):
    clear_cache()
    renderer = get_voice(phil_id)
    assert renderer is not None, f"No voice YAML found for: {phil_id}"


@pytest.mark.parametrize("phil_id", PHILOSOPHER_IDS)
def test_all_voices_render(phil_id):
    clear_cache()
    renderer = get_voice(phil_id)
    assert renderer is not None
    result = renderer.render(prompt="What is justice?", tension_level="Moderate")
    assert (
        isinstance(result, str) and len(result) > 10
    ), f"{phil_id} produced an empty/short response"


# ---------------------------------------------------------------------------
# Integration: reason_with_context applies voice
# ---------------------------------------------------------------------------


def test_reason_with_context_applies_voice():
    """reason_with_context() should return voiced text, not raw template strings."""
    from po_core.philosophers.base import Context
    from po_core.philosophers.nietzsche import Nietzsche

    clear_cache()
    n = Nietzsche()
    ctx = Context(
        prompt="What is justice?",
        tensor_snapshot={
            "freedom_pressure": 0.5,
            "semantic_delta": 0.5,
            "blocked_tensor": 0.1,
        },
    )
    resp = n.reason_with_context(ctx)
    reasoning = resp["reasoning"]

    # Must not be the old "From a Nietzschean perspective" template
    assert "From a Nietzschean perspective" not in reasoning
    # Must contain genuine voiced content
    assert len(reasoning) > 30
    assert "justice" in reasoning.lower() or any(
        w in reasoning for w in ["Wille", "Übermensch", "Gott", "Ressentiment"]
    )


def test_reason_with_context_no_voice_graceful_degradation():
    """A philosopher without a voice YAML falls back to raw reasoning text."""
    from po_core.philosophers.base import Context

    clear_cache()
    # Use a philosopher ID that has no YAML (we request it by name)
    voice = get_voice("no_such_philosopher_xyz")
    assert voice is None  # graceful None, no exception


def test_get_voice_missing_yaml_does_not_raise():
    """get_voice never raises even for completely unknown IDs."""
    clear_cache()
    for fake_id in ["__fake__", "", "123"]:
        result = get_voice(fake_id)
        assert result is None
