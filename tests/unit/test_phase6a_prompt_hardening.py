"""
Phase 6-A: Prompt Hardening Tests
===================================

Tests for the structured debate prompt (_build_debate_prompt) and
the updated _re_propose() / DeliberationEngine interface.

Markers: phase6a
"""

from __future__ import annotations

import uuid
from typing import List

import pytest

from po_core.deliberation.engine import DeliberationEngine, _build_debate_prompt
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot

pytestmark = pytest.mark.phase6a


# ── Helpers ─────────────────────────────────────────────────────────────────


def _ctx(text: str = "Is free will real?") -> Context:
    return Context.now(request_id=str(uuid.uuid4()), user_input=text)


def _intent() -> Intent:
    return Intent.neutral()


def _tensors() -> TensorSnapshot:
    return TensorSnapshot.now({"freedom_pressure": 0.0})


def _memory() -> MemorySnapshot:
    return MemorySnapshot(items=[], summary=None, meta={})


def _proposal(name: str, content: str) -> Proposal:
    return Proposal(
        proposal_id=f"test:{name}:0",
        action_type="answer",
        content=content,
        confidence=0.5,
        extra={"_po_core": {"author": name}, "philosopher": name},
    )


class DebateAwarePhilosopher:
    """Philosopher that records the prompt it receives for assertion."""

    def __init__(self, name: str, response: str):
        self.name = name
        self._response = response
        self.last_received_input: str = ""

    @property
    def info(self):
        return {"name": self.name, "tradition": "test"}

    def propose(self, ctx, intent, tensors, memory) -> List[Proposal]:
        self.last_received_input = ctx.user_input
        return [
            Proposal(
                proposal_id=f"{ctx.request_id}:{self.name}:0",
                action_type="answer",
                content=self._response,
                confidence=0.5,
                extra={"_po_core": {"author": self.name}, "philosopher": self.name},
            )
        ]


# ── _build_debate_prompt tests ───────────────────────────────────────────────


class TestBuildDebatePrompt:
    def test_basic_mode_contains_counterargument_tag(self):
        result = _build_debate_prompt(
            user_input="What is justice?",
            counter_text="Justice is subjective.",
            sender_name="Thrasymachus",
            round_num=2,
            prompt_mode="basic",
        )
        assert "[Counterargument from a fellow philosopher:" in result
        assert "Justice is subjective." in result

    def test_debate_mode_has_structured_sections(self):
        result = _build_debate_prompt(
            user_input="What is justice?",
            counter_text="Justice is the advantage of the stronger.",
            sender_name="Thrasymachus",
            round_num=2,
            prompt_mode="debate",
        )
        assert "PHILOSOPHICAL CHALLENGE" in result
        assert "Round 2" in result
        assert "Thrasymachus" in result
        assert "Steelman" in result
        assert "Refutation" in result
        assert "Defense" in result

    def test_debate_mode_includes_round_number(self):
        for r in (2, 3, 4):
            result = _build_debate_prompt(
                user_input="Q",
                counter_text="C",
                sender_name="Kant",
                round_num=r,
                prompt_mode="debate",
            )
            assert f"Round {r}" in result

    def test_debate_mode_truncates_long_counter_at_600(self):
        long_counter = "x" * 900
        result = _build_debate_prompt(
            user_input="Q",
            counter_text=long_counter,
            sender_name="Hegel",
            round_num=2,
            prompt_mode="debate",
        )
        assert "x" * 600 in result
        assert "x" * 601 not in result

    def test_basic_mode_truncates_long_counter_at_500(self):
        long_counter = "y" * 700
        result = _build_debate_prompt(
            user_input="Q",
            counter_text=long_counter,
            sender_name="Hegel",
            round_num=2,
            prompt_mode="basic",
        )
        assert "y" * 500 in result
        assert "y" * 501 not in result

    def test_unknown_sender_name_handled_gracefully(self):
        result = _build_debate_prompt(
            user_input="Q",
            counter_text="C",
            sender_name="",
            round_num=2,
            prompt_mode="debate",
        )
        # Should not crash; still contains structure
        assert "PHILOSOPHICAL CHALLENGE" in result


# ── DeliberationEngine constructor tests ─────────────────────────────────────


class TestDeliberationEnginePromptMode:
    def test_default_prompt_mode_is_debate(self):
        engine = DeliberationEngine(max_rounds=2)
        assert engine.prompt_mode == "debate"

    def test_basic_mode_accepted(self):
        engine = DeliberationEngine(max_rounds=2, prompt_mode="basic")
        assert engine.prompt_mode == "basic"

    def test_invalid_mode_falls_back_to_debate(self):
        engine = DeliberationEngine(max_rounds=2, prompt_mode="turbo")
        assert engine.prompt_mode == "debate"

    def test_max_rounds_stored(self):
        engine = DeliberationEngine(max_rounds=3, prompt_mode="debate")
        assert engine.max_rounds == 3


# ── Integration: deliberation metadata in revised proposals ─────────────────


class TestDeliberationMetadata:
    """Verify extra metadata is correctly set on re-proposed Proposals."""

    def _run_deliberation(self, prompt_mode: str = "debate", round_num: int = 2):
        sartre = DebateAwarePhilosopher("sartre", "individual freedom is absolute")
        hegel = DebateAwarePhilosopher(
            "hegel", "collective determinism is foundational"
        )

        proposals = [
            _proposal("sartre", "individual freedom is absolute"),
            _proposal("hegel", "collective determinism is foundational"),
        ]

        engine = DeliberationEngine(
            max_rounds=round_num,
            top_k_pairs=5,
            prompt_mode=prompt_mode,
        )
        result = engine.deliberate(
            [sartre, hegel],
            _ctx(),
            _intent(),
            _tensors(),
            _memory(),
            proposals,
        )
        return result, sartre, hegel

    def test_debate_mode_prompt_reaches_philosopher(self):
        _, sartre, hegel = self._run_deliberation(prompt_mode="debate")
        # At least one of them should have received the debate prompt
        combined = sartre.last_received_input + hegel.last_received_input
        assert "PHILOSOPHICAL CHALLENGE" in combined

    def test_basic_mode_prompt_reaches_philosopher(self):
        _, sartre, hegel = self._run_deliberation(prompt_mode="basic")
        combined = sartre.last_received_input + hegel.last_received_input
        assert "Counterargument from a fellow philosopher" in combined

    def test_revised_proposals_have_deliberation_round_metadata(self):
        result, _, _ = self._run_deliberation()
        revised = [p for p in result.proposals if p.extra.get("deliberation_round")]
        assert len(revised) > 0
        for p in revised:
            assert p.extra["deliberation_round"] == 2

    def test_revised_proposals_have_debate_sender(self):
        result, _, _ = self._run_deliberation(prompt_mode="debate")
        revised = [p for p in result.proposals if p.extra.get("debate_sender")]
        assert len(revised) > 0
        for p in revised:
            assert p.extra["debate_sender"] in (
                "sartre",
                "hegel",
                "a fellow philosopher",
            )

    def test_revised_proposals_have_prompt_mode_metadata(self):
        result, _, _ = self._run_deliberation(prompt_mode="debate")
        revised = [p for p in result.proposals if "prompt_mode" in p.extra]
        assert len(revised) > 0
        for p in revised:
            assert p.extra["prompt_mode"] == "debate"

    def test_proposal_id_suffix_reflects_round(self):
        result, _, _ = self._run_deliberation(prompt_mode="debate", round_num=2)
        revised_ids = [
            p.proposal_id for p in result.proposals if p.extra.get("deliberation_round")
        ]
        assert all(":d2" in pid for pid in revised_ids)
