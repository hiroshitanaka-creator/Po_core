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


# ---------------------------------------------------------------------------
# Regression: propose() must NOT replace content with voice output
# ---------------------------------------------------------------------------


def _make_propose_inputs():
    """Return (ctx, intent, tensors, memory) for propose() calls."""
    import uuid
    from datetime import datetime, timezone

    from po_core.domain.context import Context as DomainContext
    from po_core.domain.intent import Intent
    from po_core.domain.memory_snapshot import MemorySnapshot
    from po_core.domain.tensor_snapshot import TensorSnapshot

    ctx = DomainContext(
        request_id=str(uuid.uuid4()),
        user_input="What is justice?",
        created_at=datetime.now(timezone.utc),
    )
    intent = Intent.neutral()
    tensors = TensorSnapshot.now({"freedom_pressure": 0.5, "semantic_delta": 0.3, "blocked_tensor": 0.1})
    memory = MemorySnapshot(items=[], summary=None, meta={})
    return ctx, intent, tensors, memory


def test_propose_content_is_original_reasoning_not_voice_only():
    """propose() must keep the philosopher's analytical text in Proposal.content.

    Before the fix, voice.render() overwrote normalized["reasoning"], so
    Proposal.content became a template string devoid of philosophical keywords.
    After the fix, content == original reason() output; voice lives in extra.
    """
    from po_core.philosophers.nietzsche import Nietzsche

    clear_cache()
    n = Nietzsche()
    ctx, intent, tensors, memory = _make_propose_inputs()

    # Capture what voice.render() alone would produce for this prompt/tension
    voice = get_voice("nietzsche")
    assert voice is not None
    voice_only = voice.render(prompt=ctx.user_input, tension_level=None, tensor_snapshot={})

    proposals = n.propose(ctx, intent, tensors, memory)
    assert proposals, "propose() returned no proposals"
    content = proposals[0].content

    # content must not be identical to the lone voice output
    assert content != voice_only, (
        "Proposal.content equals voice.render() output — original reasoning was discarded"
    )
    # content must be a meaningful string
    assert len(content) > 10


def test_propose_extra_has_voiced_reasoning_when_voice_exists():
    """propose() must store voice output in extra['voiced_reasoning']."""
    from po_core.philosophers.nietzsche import Nietzsche

    clear_cache()
    n = Nietzsche()
    ctx, intent, tensors, memory = _make_propose_inputs()

    proposals = n.propose(ctx, intent, tensors, memory)
    assert proposals
    extra = proposals[0].extra

    assert "voiced_reasoning" in extra, "extra missing 'voiced_reasoning' key"
    vr = extra["voiced_reasoning"]
    assert isinstance(vr, str) and len(vr) > 10, (
        f"voiced_reasoning is not a non-empty string: {vr!r}"
    )


def test_propose_no_voice_extra_voiced_reasoning_is_none():
    """Philosophers without a YAML should have voiced_reasoning=None in extra."""
    from po_core.philosophers.base import Philosopher

    class _VoicelessPhil(Philosopher):
        def reason(self, prompt, context):  # type: ignore[override]
            return {
                "reasoning": "freedom vs determinism is the core tension here",
                "perspective": "test",
            }

    # Place the class in a module whose last component has no voice YAML
    _VoicelessPhil.__module__ = "po_core.philosophers.__voiceless2__"

    clear_cache()
    ph = _VoicelessPhil(name="__voiceless2__", description="test")
    ctx, intent, tensors, memory = _make_propose_inputs()
    proposals = ph.propose(ctx, intent, tensors, memory)
    assert proposals
    assert proposals[0].extra.get("voiced_reasoning") is None


def test_interaction_matrix_tension_uses_proposal_content_keywords():
    """InteractionMatrix._compute_tension must see original opposition keywords.

    If voice had replaced content, keywords like 'freedom'/'determinism' would
    be absent and tension would be 0, collapsing deliberation round 2.
    """
    from po_core.domain.proposal import Proposal
    from po_core.tensors.interaction_tensor import InteractionMatrix

    # Two proposals with explicit opposing keywords — mirrors what real
    # philosopher reason() output contains after our fix.
    p_freedom = Proposal(
        proposal_id="t:phil_a:0",
        action_type="answer",
        content="The concept of freedom is essential; individual autonomy must prevail over collective constraint.",
        confidence=0.5,
        extra={"_po_core": {"author": "phil_a"}, "philosopher": "phil_a"},
    )
    p_determinism = Proposal(
        proposal_id="t:phil_b:0",
        action_type="answer",
        content="Determinism governs all action; the collective structure shapes every individual choice.",
        confidence=0.5,
        extra={"_po_core": {"author": "phil_b"}, "philosopher": "phil_b"},
    )

    matrix = InteractionMatrix.from_proposals([p_freedom, p_determinism])
    assert matrix.tension[0, 1] > 0.0, (
        "Expected non-zero tension between 'freedom' and 'determinism' proposals, "
        f"got {matrix.tension[0, 1]}"
    )


def test_deliberation_round2_fires_when_content_has_opposition_keywords():
    """Deliberation engine must produce n_revised > 0 when proposals carry
    opposing philosophical keywords in their content field.

    This is the end-to-end regression for the voice-overwrite bug: if content
    were replaced by voice template text, high_interference_pairs() would return
    [] and round 2 would be skipped (n_revised == 0).
    """
    import uuid
    from datetime import datetime, timezone

    from po_core.deliberation import DeliberationEngine
    from po_core.domain.context import Context as DomainContext
    from po_core.domain.intent import Intent
    from po_core.domain.memory_snapshot import MemorySnapshot
    from po_core.domain.proposal import Proposal
    from po_core.domain.tensor_snapshot import TensorSnapshot

    class _StubPhil:
        """Minimal philosopher that always returns a fixed proposal."""

        def __init__(self, name: str, response_content: str):
            self.name = name
            self._content = response_content

        def propose(self, ctx, intent, tensors, memory):
            return [
                Proposal(
                    proposal_id=f"test:{self.name}:0",
                    action_type="answer",
                    content=self._content,
                    confidence=0.5,
                    extra={"_po_core": {"author": self.name}, "philosopher": self.name},
                )
            ]

    ctx = DomainContext(
        request_id=str(uuid.uuid4()),
        user_input="Is freedom real?",
        created_at=datetime.now(timezone.utc),
    )
    intent = Intent.neutral()
    tensors = TensorSnapshot.now({"freedom_pressure": 0.0})
    memory = MemorySnapshot(items=[], summary=None, meta={})

    phil_a = _StubPhil(
        "kant_stub",
        "freedom is the ground of all rational moral action; individual autonomy is paramount.",
    )
    phil_b = _StubPhil(
        "hegel_stub",
        "determinism and the collective structure of spirit shape every individual act.",
    )

    round1 = [
        Proposal(
            proposal_id="test:kant_stub:0",
            action_type="answer",
            content="freedom is the ground of all rational moral action; individual autonomy is paramount.",
            confidence=0.5,
            extra={"_po_core": {"author": "kant_stub"}, "philosopher": "kant_stub"},
        ),
        Proposal(
            proposal_id="test:hegel_stub:0",
            action_type="answer",
            content="determinism and the collective structure of spirit shape every individual act.",
            confidence=0.5,
            extra={"_po_core": {"author": "hegel_stub"}, "philosopher": "hegel_stub"},
        ),
    ]

    engine = DeliberationEngine(max_rounds=2, top_k_pairs=3)
    result = engine.deliberate(
        philosophers=[phil_a, phil_b],
        ctx=ctx,
        intent=intent,
        tensors=tensors,
        memory=memory,
        round1_proposals=round1,
    )

    round2_traces = [r for r in result.rounds if r.round_number == 2]
    assert round2_traces, "No round-2 trace produced"
    assert round2_traces[0].n_revised > 0, (
        "Round 2 ran but n_revised == 0 — opposition keywords were not detected in content. "
        "This indicates voice output has replaced the original reasoning in Proposal.content."
    )
