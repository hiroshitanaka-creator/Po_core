from __future__ import annotations

from po_core.philosophers.llm_personas import LLM_PERSONAS
from po_core.philosophers.llm_philosopher import LLMPhilosopher
from po_core.philosophers.manifest import SPECS


class _StubProvider:
    value = "stub"


class _StubAdapter:
    provider = _StubProvider()
    actual_model = "stub-model"

    def generate(self, system: str, user: str):  # pragma: no cover - not used here
        raise AssertionError("not used")


RUNTIME_JSON_PHRASES = [
    '"reasoning"',
    '"perspective"',
    '"tension"',
    '"confidence"',
    '"action_type"',
    '"citations"',
]


def test_llm_persona_prompts_enforce_one_runtime_json_contract() -> None:
    for persona_id, persona in LLM_PERSONAS.items():
        prompt = persona["system_prompt"]
        for phrase in RUNTIME_JSON_PHRASES:
            assert phrase in prompt, f"{persona_id} missing {phrase} in system prompt"


def test_llm_philosopher_normalizes_to_runtime_json_contract() -> None:
    philosopher = LLMPhilosopher("kant", _StubAdapter())

    parsed = philosopher._normalize_parsed(
        {
            "reasoning": "Duty before inclination.",
            "perspective": "Deontology",
            "tension": {
                "level": "high",
                "description": "duty versus desire",
                "elements": ["duty", "desire"],
            },
            "confidence": "0.7",
            "action_type": "defer",
            "citations": ["Groundwork"],
        }
    )

    assert parsed == {
        "reasoning": "Duty before inclination.",
        "perspective": "Deontology",
        "tension": {
            "level": "high",
            "description": "duty versus desire",
            "elements": ["duty", "desire"],
        },
        "confidence": 0.7,
        "action_type": "defer",
        "citations": ["Groundwork"],
    }


def test_llm_philosopher_raw_text_fallback_still_emits_full_contract() -> None:
    philosopher = LLMPhilosopher("kant", _StubAdapter())

    parsed = philosopher._parse_llm_response("plain text response")

    assert parsed == {
        "reasoning": "plain text response",
        "perspective": philosopher.description,
        "tension": None,
        "confidence": 0.5,
        "action_type": "answer",
        "citations": [],
    }


def test_runtime_roster_count_semantics_are_explicit() -> None:
    non_dummy_specs = [spec for spec in SPECS if spec.philosopher_id != "dummy"]

    assert len(non_dummy_specs) == 42
    assert len(SPECS) == 43
    assert "dummy" in LLM_PERSONAS
    assert len(LLM_PERSONAS) == len(SPECS)
