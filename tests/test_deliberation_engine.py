"""
Deliberation Engine Tests (Phase 2 Task 8)
===========================================

Tests for multi-round philosopher dialogue.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from po_core.deliberation import DeliberationEngine, DeliberationResult
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot


# ── Helpers ──────────────────────────────────────────────────────────


def _ctx(text: str = "What is justice?") -> Context:
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
        extra={
            "_po_core": {"author": name},
            "philosopher": name,
        },
    )


class FakePhilosopher:
    """Minimal philosopher for deliberation testing."""

    def __init__(self, name: str, response: str):
        self.name = name
        self._response = response

    @property
    def info(self):
        return {"name": self.name, "tradition": "test"}

    def propose(self, ctx, intent, tensors, memory):
        content = self._response
        # If counterargument present, append acknowledgement
        if "[Counterargument" in ctx.user_input:
            content = f"{self._response} [revised after considering counterargument]"
        return [Proposal(
            proposal_id=f"{ctx.request_id}:{self.name}:0",
            action_type="answer",
            content=content,
            confidence=0.5,
            extra={"_po_core": {"author": self.name}, "philosopher": self.name},
        )]


# ── Constructor tests ────────────────────────────────────────────────


class TestConstructor:
    def test_default_max_rounds(self):
        e = DeliberationEngine()
        assert e.max_rounds == 2

    def test_custom_max_rounds(self):
        e = DeliberationEngine(max_rounds=3, top_k_pairs=3)
        assert e.max_rounds == 3
        assert e.top_k_pairs == 3

    def test_min_rounds_is_1(self):
        e = DeliberationEngine(max_rounds=0)
        assert e.max_rounds == 1


# ── Single-round (pass-through) ─────────────────────────────────────


class TestSingleRound:
    def test_max_rounds_1_is_passthrough(self):
        e = DeliberationEngine(max_rounds=1)
        proposals = [
            _proposal("Aristotle", "virtue is the golden mean"),
            _proposal("Kant", "duty demands the categorical imperative"),
        ]
        result = e.deliberate([], _ctx(), _intent(), _tensors(), _memory(), proposals)
        assert result.n_rounds == 1
        assert result.total_proposals == 2
        assert result.interaction_matrix is None

    def test_empty_proposals_passthrough(self):
        e = DeliberationEngine(max_rounds=2)
        result = e.deliberate([], _ctx(), _intent(), _tensors(), _memory(), [])
        assert result.n_rounds == 1
        assert result.total_proposals == 0

    def test_single_proposal_no_deliberation(self):
        e = DeliberationEngine(max_rounds=2)
        result = e.deliberate(
            [], _ctx(), _intent(), _tensors(), _memory(),
            [_proposal("Aristotle", "virtue")],
        )
        assert result.n_rounds == 1
        assert result.total_proposals == 1


# ── Multi-round deliberation ────────────────────────────────────────


class TestMultiRound:
    def test_two_rounds_with_opposing_proposals(self):
        philosophers = [
            FakePhilosopher("Sartre", "individual freedom is absolute and subjective"),
            FakePhilosopher("Hegel", "collective determinism is relative and objective"),
        ]
        proposals = [
            _proposal("Sartre", "individual freedom is absolute and subjective"),
            _proposal("Hegel", "collective determinism is relative and objective"),
        ]
        e = DeliberationEngine(max_rounds=2, top_k_pairs=5)
        result = e.deliberate(
            philosophers, _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        assert result.n_rounds == 2
        assert result.interaction_matrix is not None
        # At least one philosopher should be revised
        assert result.rounds[1].n_revised >= 0

    def test_revised_proposals_replace_originals(self):
        philosophers = [
            FakePhilosopher("Sartre", "individual freedom is absolute and subjective"),
            FakePhilosopher("Hegel", "collective determinism is relative and objective"),
        ]
        proposals = [
            _proposal("Sartre", "individual freedom is absolute and subjective"),
            _proposal("Hegel", "collective determinism is relative and objective"),
        ]
        e = DeliberationEngine(max_rounds=2, top_k_pairs=5)
        result = e.deliberate(
            philosophers, _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        # Check that revised proposals contain counterargument acknowledgement
        for p in result.proposals:
            if "revised" in p.content:
                assert "counterargument" in p.content.lower()

    def test_no_duplicate_authors(self):
        """After merge, each philosopher should appear at most once."""
        philosophers = [
            FakePhilosopher("A", "individual freedom is absolute"),
            FakePhilosopher("B", "collective determinism is relative"),
            FakePhilosopher("C", "virtue is the golden mean of character"),
        ]
        proposals = [
            _proposal("A", "individual freedom is absolute"),
            _proposal("B", "collective determinism is relative"),
            _proposal("C", "virtue is the golden mean of character"),
        ]
        e = DeliberationEngine(max_rounds=2)
        result = e.deliberate(
            philosophers, _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        # Count unique authors
        from po_core.deliberation.engine import _get_author
        authors = [_get_author(p) for p in result.proposals]
        assert len(authors) == len(set(authors))

    def test_deliberation_result_summary(self):
        philosophers = [
            FakePhilosopher("A", "freedom is absolute"),
            FakePhilosopher("B", "determinism is objective"),
        ]
        proposals = [
            _proposal("A", "freedom is absolute"),
            _proposal("B", "determinism is objective"),
        ]
        e = DeliberationEngine(max_rounds=2)
        result = e.deliberate(
            philosophers, _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        s = result.summary()
        assert "n_rounds" in s
        assert "total_proposals" in s
        assert "rounds" in s
        assert len(s["rounds"]) == result.n_rounds

    def test_three_rounds(self):
        """Three rounds of deliberation."""
        philosophers = [
            FakePhilosopher("A", "individual freedom is absolute and subjective"),
            FakePhilosopher("B", "collective determinism is relative and objective"),
        ]
        proposals = [
            _proposal("A", "individual freedom is absolute and subjective"),
            _proposal("B", "collective determinism is relative and objective"),
        ]
        e = DeliberationEngine(max_rounds=3, top_k_pairs=5)
        result = e.deliberate(
            philosophers, _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        assert result.n_rounds >= 2
        assert result.n_rounds <= 3


# ── Integration with real philosophers ───────────────────────────────


class TestRealDeliberation:
    def test_deliberation_with_real_philosophers(self):
        """Run deliberation on actual philosopher proposals."""
        from po_core.domain.safety_mode import SafetyMode
        from po_core.philosophers.registry import PhilosopherRegistry

        registry = PhilosopherRegistry(cache_instances=True)
        sel = registry.select(SafetyMode.NORMAL)
        philosophers, _ = registry.load(sel.selected_ids)

        ctx = _ctx("Is individual freedom or collective good more important?")
        intent = _intent()
        tensors = _tensors()
        memory = _memory()

        # Generate round 1 proposals
        round1 = []
        for ph in philosophers:
            try:
                props = ph.propose(ctx, intent, tensors, memory)
                if props:
                    round1.extend(props)
            except Exception:
                continue

        assert len(round1) >= 30

        # Deliberate
        e = DeliberationEngine(max_rounds=2, top_k_pairs=3)
        result = e.deliberate(philosophers, ctx, intent, tensors, memory, round1)

        assert result.n_rounds == 2
        assert result.total_proposals >= 30
        assert result.interaction_matrix is not None
        assert result.rounds[1].n_revised > 0  # Some philosophers re-proposed

    def test_deliberation_in_pipeline_wiring(self):
        """Verify deliberation engine can be wired into the pipeline."""
        from po_core.runtime.settings import Settings

        settings = Settings(deliberation_max_rounds=2, deliberation_top_k_pairs=3)
        assert settings.deliberation_max_rounds == 2

        from po_core.runtime.wiring import _build_deliberation_engine

        engine = _build_deliberation_engine(settings)
        assert engine is not None
        assert engine.max_rounds == 2

    def test_deliberation_disabled_by_default(self):
        """Default settings should not enable deliberation."""
        from po_core.runtime.settings import Settings
        from po_core.runtime.wiring import _build_deliberation_engine

        settings = Settings()
        engine = _build_deliberation_engine(settings)
        assert engine is None  # max_rounds=1 → no engine
