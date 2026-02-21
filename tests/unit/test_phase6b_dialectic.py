"""
Phase 6-B: Dialectic Roles Tests
==================================

Tests for Hegelian 3-round dialectic structure:
  Round 1 (Thesis)     — all philosophers propose normally
  Round 2 (Antithesis) — high-interference pairs REFUTE each other
  Round 3 (Synthesis)  — Synthesizer philosophers integrate the debate

Markers: phase6b
"""

from __future__ import annotations

import uuid
from typing import List

import pytest

from po_core.deliberation.engine import (
    DeliberationEngine,
    DeliberationResult,
    RoundTrace,
    _collect_synthesis_counterarguments,
)
from po_core.deliberation.roles import (
    SYNTHESIZER_PHILOSOPHERS,
    DebateRole,
    assign_role,
    get_role_prompt_prefix,
)
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot

pytestmark = pytest.mark.phase6b


# ── Helpers ─────────────────────────────────────────────────────────────────


def _ctx(text: str = "What is freedom?") -> Context:
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


class RecordingPhilosopher:
    """Philosopher that records the last received prompt and returns a fixed response."""

    def __init__(self, name: str, response: str = ""):
        self.name = name
        self._response = response or f"{name}'s response"
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


# ── TestDebateRole ───────────────────────────────────────────────────────────


class TestDebateRole:
    def test_debate_role_values(self):
        assert DebateRole.THESIS.value == "thesis"
        assert DebateRole.ANTITHESIS.value == "antithesis"
        assert DebateRole.SYNTHESIS.value == "synthesis"
        assert DebateRole.STANDARD.value == "standard"

    def test_assign_role_standard_mode_always_returns_standard(self):
        for round_num in [1, 2, 3, 4, 10]:
            assert assign_role(round_num, dialectic_mode=False) == DebateRole.STANDARD

    def test_assign_role_dialectic_round1_is_thesis(self):
        assert assign_role(1, dialectic_mode=True) == DebateRole.THESIS

    def test_assign_role_dialectic_round2_is_antithesis(self):
        assert assign_role(2, dialectic_mode=True) == DebateRole.ANTITHESIS

    def test_assign_role_dialectic_round3_is_synthesis(self):
        assert assign_role(3, dialectic_mode=True) == DebateRole.SYNTHESIS

    def test_assign_role_dialectic_round4_plus_is_synthesis(self):
        assert assign_role(4, dialectic_mode=True) == DebateRole.SYNTHESIS
        assert assign_role(10, dialectic_mode=True) == DebateRole.SYNTHESIS


# ── TestRolePromptPrefix ─────────────────────────────────────────────────────


class TestRolePromptPrefix:
    def test_thesis_has_empty_prefix(self):
        prefix = get_role_prompt_prefix(DebateRole.THESIS)
        assert prefix == ""

    def test_standard_has_empty_prefix(self):
        prefix = get_role_prompt_prefix(DebateRole.STANDARD)
        assert prefix == ""

    def test_antithesis_prefix_contains_refute(self):
        prefix = get_role_prompt_prefix(DebateRole.ANTITHESIS)
        assert "REFUTE" in prefix

    def test_antithesis_prefix_contains_antithesis_role_label(self):
        prefix = get_role_prompt_prefix(DebateRole.ANTITHESIS)
        assert "ANTITHESIS" in prefix

    def test_synthesis_prefix_contains_aufhebung(self):
        prefix = get_role_prompt_prefix(DebateRole.SYNTHESIS)
        assert "Aufhebung" in prefix

    def test_synthesis_prefix_contains_synthesis_role_label(self):
        prefix = get_role_prompt_prefix(DebateRole.SYNTHESIS)
        assert "SYNTHESIS" in prefix


# ── TestRoundTraceRole ───────────────────────────────────────────────────────


class TestRoundTraceRole:
    def test_roundtrace_default_role_is_standard(self):
        trace = RoundTrace(round_number=1, n_proposals=5, n_revised=0)
        assert trace.role == "standard"

    def test_roundtrace_can_be_set_to_thesis(self):
        trace = RoundTrace(round_number=1, n_proposals=5, n_revised=0, role="thesis")
        assert trace.role == "thesis"

    def test_roundtrace_can_be_set_to_antithesis(self):
        trace = RoundTrace(
            round_number=2, n_proposals=5, n_revised=3, role="antithesis"
        )
        assert trace.role == "antithesis"

    def test_roundtrace_can_be_set_to_synthesis(self):
        trace = RoundTrace(round_number=3, n_proposals=6, n_revised=2, role="synthesis")
        assert trace.role == "synthesis"


# ── TestDeliberationEngineDialecticMode ─────────────────────────────────────


class TestDeliberationEngineDialecticMode:
    def test_standard_mode_is_default(self):
        engine = DeliberationEngine()
        assert engine.dialectic_mode == "standard"

    def test_dialectic_mode_is_accepted(self):
        engine = DeliberationEngine(dialectic_mode="dialectic")
        assert engine.dialectic_mode == "dialectic"

    def test_invalid_mode_falls_back_to_standard(self):
        engine = DeliberationEngine(dialectic_mode="invalid_mode")
        assert engine.dialectic_mode == "standard"

    def test_dialectic_mode_forces_min_3_rounds(self):
        # Even if caller passes max_rounds=1, dialectic needs at least 3
        engine = DeliberationEngine(max_rounds=1, dialectic_mode="dialectic")
        assert engine.max_rounds >= 3

    def test_dialectic_mode_preserves_higher_max_rounds(self):
        engine = DeliberationEngine(max_rounds=5, dialectic_mode="dialectic")
        assert engine.max_rounds == 5

    def test_standard_mode_preserves_max_rounds(self):
        engine = DeliberationEngine(max_rounds=2, dialectic_mode="standard")
        assert engine.max_rounds == 2


# ── TestSynthesizerPhilosophers ──────────────────────────────────────────────


class TestSynthesizerPhilosophers:
    def test_synthesizer_list_is_nonempty(self):
        assert len(SYNTHESIZER_PHILOSOPHERS) > 0

    def test_hegel_is_a_synthesizer(self):
        assert "Hegel" in SYNTHESIZER_PHILOSOPHERS

    def test_all_synthesizer_names_are_strings(self):
        for name in SYNTHESIZER_PHILOSOPHERS:
            assert isinstance(name, str)


# ── TestCollectSynthesisCounterarguments ─────────────────────────────────────


class TestCollectSynthesisCounterarguments:
    def _ph_lookup(self, names):
        return {n: object() for n in names}

    def test_synthesizers_in_lookup_receive_counterarguments(self):
        proposals = [
            _proposal("Nietzsche", "Power is the only truth."),
            _proposal("Kant", "Duty is the foundation of morality."),
        ]
        lookup = self._ph_lookup(["Hegel", "Kant"])
        result = _collect_synthesis_counterarguments(
            proposals, ["Hegel", "Kant"], lookup
        )
        assert "Hegel" in result
        assert "Kant" in result

    def test_synthesizers_not_in_lookup_are_excluded(self):
        proposals = [_proposal("Aristotle", "Virtue leads to flourishing.")]
        lookup = self._ph_lookup(["Hegel"])  # Only Hegel is loaded
        result = _collect_synthesis_counterarguments(
            proposals, ["Hegel", "Kant", "Dewey"], lookup
        )
        assert "Hegel" in result
        assert "Kant" not in result
        assert "Dewey" not in result

    def test_combined_text_includes_proposal_content(self):
        proposals = [
            _proposal("Nietzsche", "Beyond good and evil."),
            _proposal("Kant", "The categorical imperative."),
        ]
        lookup = self._ph_lookup(["Hegel"])
        result = _collect_synthesis_counterarguments(proposals, ["Hegel"], lookup)
        combined = result["Hegel"]
        assert "Nietzsche" in combined
        assert "Kant" in combined
        assert "Beyond good and evil" in combined
        assert "categorical imperative" in combined

    def test_empty_proposals_gives_empty_combined(self):
        lookup = self._ph_lookup(["Hegel"])
        result = _collect_synthesis_counterarguments([], ["Hegel"], lookup)
        assert result["Hegel"] == ""

    def test_max_10_proposals_aggregated(self):
        proposals = [_proposal(f"Ph{i}", f"Position {i}") for i in range(20)]
        lookup = self._ph_lookup(["Hegel"])
        result = _collect_synthesis_counterarguments(proposals, ["Hegel"], lookup)
        # Should not include all 20 — check at most 10 are present
        combined = result["Hegel"]
        count = sum(1 for i in range(20) if f"Position {i}" in combined)
        assert count <= 10


# ── TestDialecticDeliberation (integration-lite) ────────────────────────────


class TestDialecticRound1HasThesisRole:
    """In dialectic mode, round-1 trace must carry role='thesis'."""

    def test_round1_role_is_thesis_in_dialectic_mode(self):
        philosophers = [
            RecordingPhilosopher("Alpha", "Free will exists."),
            RecordingPhilosopher("Beta", "Free will is an illusion."),
        ]
        proposals = [
            _proposal("Alpha", "Free will exists."),
            _proposal("Beta", "Free will is an illusion."),
        ]
        engine = DeliberationEngine(
            max_rounds=3,
            dialectic_mode="dialectic",
            detect_emergence=False,
            track_influence=False,
        )
        result = engine.deliberate(
            philosophers, _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        assert result.rounds[0].role == "thesis"

    def test_round1_role_is_standard_in_standard_mode(self):
        proposals = [
            _proposal("Alpha", "Free will exists."),
            _proposal("Beta", "Determinism is true."),
        ]
        engine = DeliberationEngine(
            max_rounds=1,
            dialectic_mode="standard",
            detect_emergence=False,
            track_influence=False,
        )
        result = engine.deliberate(
            [], _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        assert result.rounds[0].role == "standard"

    def test_summary_includes_role_field(self):
        proposals = [
            _proposal("Alpha", "First position."),
            _proposal("Beta", "Second position."),
        ]
        engine = DeliberationEngine(
            max_rounds=1,
            dialectic_mode="dialectic",
            detect_emergence=False,
            track_influence=False,
        )
        result = engine.deliberate(
            [], _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        summary = result.summary()
        for round_entry in summary["rounds"]:
            assert "role" in round_entry

    def test_dialectic_mode_round2_has_antithesis_role(self):
        """When 2 philosophers run 2 rounds in dialectic mode, round 2 role = antithesis."""
        philosophers = [
            RecordingPhilosopher("Alpha", "Position A."),
            RecordingPhilosopher("Beta", "Position B."),
        ]
        proposals = [
            _proposal("Alpha", "Position A."),
            _proposal("Beta", "Position B."),
        ]
        engine = DeliberationEngine(
            max_rounds=3,
            dialectic_mode="dialectic",
            detect_emergence=False,
            track_influence=False,
        )
        result = engine.deliberate(
            philosophers, _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        # Find the antithesis round
        antithesis_rounds = [r for r in result.rounds if r.role == "antithesis"]
        assert len(antithesis_rounds) >= 1
        assert antithesis_rounds[0].round_number == 2

    def test_antithesis_prompt_contains_refute_instruction(self):
        """_build_debate_prompt with ANTITHESIS role prefix must contain REFUTE."""
        from po_core.deliberation.engine import _build_debate_prompt

        role_prefix = get_role_prompt_prefix(DebateRole.ANTITHESIS)
        prompt = _build_debate_prompt(
            "What is freedom?",
            "Freedom is a social construct with no absolute foundation.",
            "Nietzsche",
            round_num=2,
            prompt_mode="debate",
            role_prefix=role_prefix,
        )
        assert "REFUTE" in prompt or "ANTITHESIS" in prompt
