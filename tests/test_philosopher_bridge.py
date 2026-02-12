"""
Philosopher Protocol Tests (Native propose())
===============================================

Tests that all Philosopher subclasses implement PhilosopherProtocol natively
via the base class — no bridge adapter needed.

Previously tested PhilosopherBridge, which has been removed in Phase 1.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.pipeline

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.philosophers.base import Philosopher, PhilosopherInfo
from po_core.philosophers.manifest import SPECS
from po_core.philosophers.registry import PhilosopherRegistry


def _make_ctx(user_input: str = "test input") -> Context:
    return Context.now(request_id="test-001", user_input=user_input)


def _make_intent() -> Intent:
    return Intent.neutral()


def _make_tensors() -> TensorSnapshot:
    return TensorSnapshot.empty()


def _make_memory() -> MemorySnapshot:
    return MemorySnapshot.empty()


# ── Native PhilosopherProtocol tests ──────────────────────────────────


class TestNativeProtocol:
    """Test that Philosopher subclasses implement PhilosopherProtocol natively."""

    def test_philosopher_has_info(self):
        from po_core.philosophers.aristotle import Aristotle

        ph = Aristotle()
        assert isinstance(ph.info, PhilosopherInfo)
        assert "Aristotle" in ph.info.name

    def test_philosopher_has_propose(self):
        from po_core.philosophers.kant import Kant

        ph = Kant()
        assert hasattr(ph, "propose")
        assert callable(ph.propose)

    def test_philosopher_has_name(self):
        from po_core.philosophers.confucius import Confucius

        ph = Confucius()
        assert hasattr(ph, "name")
        assert isinstance(ph.name, str)
        assert len(ph.name) > 0

    def test_philosopher_is_not_wrapped(self):
        """Philosophers should NOT be wrapped — they implement propose() natively."""
        from po_core.philosophers.sartre import Sartre

        ph = Sartre()
        # Should be the actual philosopher class, not a wrapper
        assert isinstance(ph, Philosopher)
        assert hasattr(ph, "propose")
        assert hasattr(ph, "info")


class TestNativePropose:
    """Test that native propose() returns valid Proposal objects."""

    def test_propose_returns_list(self):
        from po_core.philosophers.aristotle import Aristotle

        ph = Aristotle()
        result = ph.propose(
            _make_ctx(), _make_intent(), _make_tensors(), _make_memory()
        )
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_propose_returns_proposals(self):
        from po_core.philosophers.kant import Kant

        ph = Kant()
        result = ph.propose(
            _make_ctx(), _make_intent(), _make_tensors(), _make_memory()
        )
        for p in result:
            assert isinstance(p, Proposal)

    def test_proposal_has_required_fields(self):
        from po_core.philosophers.nietzsche import Nietzsche

        ph = Nietzsche()
        result = ph.propose(
            _make_ctx("What is power?"), _make_intent(), _make_tensors(), _make_memory()
        )
        p = result[0]
        assert p.proposal_id
        assert p.action_type == "answer"
        assert len(p.content) > 0
        assert 0.0 <= p.confidence <= 1.0

    def test_proposal_id_contains_request_id(self):
        from po_core.philosophers.heidegger import Heidegger

        ctx = _make_ctx("What is being?")
        ph = Heidegger()
        result = ph.propose(ctx, _make_intent(), _make_tensors(), _make_memory())
        assert ctx.request_id in result[0].proposal_id

    def test_proposal_content_is_reasoning(self):
        from po_core.philosophers.dewey import Dewey

        ph = Dewey()
        result = ph.propose(
            _make_ctx("What is education?"),
            _make_intent(),
            _make_tensors(),
            _make_memory(),
        )
        assert len(result[0].content) > 10

    def test_proposal_extra_has_philosopher_info(self):
        from po_core.philosophers.wittgenstein import Wittgenstein

        ph = Wittgenstein()
        result = ph.propose(
            _make_ctx(), _make_intent(), _make_tensors(), _make_memory()
        )
        extra = result[0].extra
        assert "philosopher" in extra
        assert "perspective" in extra


class TestNonStandardReason:
    """Confucius returns analysis/summary instead of reasoning.
    Native propose() must handle this via normalize_response()."""

    def test_confucius_propose_works(self):
        from po_core.philosophers.confucius import Confucius

        ph = Confucius()
        result = ph.propose(
            _make_ctx("What is virtue?"),
            _make_intent(),
            _make_tensors(),
            _make_memory(),
        )
        assert len(result) == 1
        p = result[0]
        assert len(p.content) > 0
        assert p.action_type == "answer"


# ── Registry loading tests ──────────────────────────────────────────


class TestRegistryNativeLoading:
    """Test that PhilosopherRegistry loads native PhilosopherProtocol instances."""

    def test_registry_loads_all(self):
        """All 39 philosophers should load successfully."""
        registry = PhilosopherRegistry(cache_instances=False)
        sel = registry.select(SafetyMode.NORMAL)
        philosophers, errors = registry.load(sel.selected_ids)
        assert len(errors) == 0, f"Load errors: {errors}"
        assert len(philosophers) > 0

    def test_loaded_philosophers_have_propose(self):
        """All loaded philosophers should have propose() method."""
        registry = PhilosopherRegistry(cache_instances=False)
        sel = registry.select(SafetyMode.NORMAL)
        philosophers, _ = registry.load(sel.selected_ids)
        for ph in philosophers:
            assert hasattr(ph, "propose"), f"{ph} missing propose()"
            assert hasattr(ph, "info"), f"{ph} missing info"

    def test_loaded_philosophers_can_propose(self):
        """All loaded philosophers should produce proposals."""
        registry = PhilosopherRegistry(cache_instances=False)
        sel = registry.select(SafetyMode.NORMAL)
        philosophers, _ = registry.load(sel.selected_ids)

        ctx = _make_ctx("What is justice?")
        intent = _make_intent()
        tensors = _make_tensors()
        memory = _make_memory()

        for ph in philosophers:
            result = ph.propose(ctx, intent, tensors, memory)
            assert isinstance(result, list), f"{ph.info.name} returned {type(result)}"
            assert len(result) >= 1, f"{ph.info.name} returned empty list"
            assert isinstance(
                result[0], Proposal
            ), f"{ph.info.name} returned non-Proposal"

    def test_warn_mode_loads_subset(self):
        """WARN mode should load fewer philosophers."""
        registry = PhilosopherRegistry(cache_instances=False)
        sel = registry.select(SafetyMode.WARN)
        philosophers, errors = registry.load(sel.selected_ids)
        assert len(errors) == 0
        assert len(philosophers) <= 5
        for ph in philosophers:
            assert hasattr(ph, "propose")

    def test_critical_mode_loads_one(self):
        """CRITICAL mode should load exactly 1 philosopher."""
        registry = PhilosopherRegistry(cache_instances=False)
        sel = registry.select(SafetyMode.CRITICAL)
        philosophers, errors = registry.load(sel.selected_ids)
        assert len(errors) == 0
        assert len(philosophers) == 1
        assert hasattr(philosophers[0], "propose")

    def test_no_philosopher_needs_adapter(self):
        """All philosophers should implement PhilosopherProtocol natively."""
        registry = PhilosopherRegistry(cache_instances=False)
        sel = registry.select(SafetyMode.NORMAL)
        philosophers, _ = registry.load(sel.selected_ids)
        for ph in philosophers:
            # Must have propose() and info — either via Philosopher base or native impl
            assert hasattr(ph, "propose") and hasattr(
                ph, "info"
            ), f"{ph.info.name} does not implement PhilosopherProtocol"


# ── Full pipeline smoke test ──────────────────────────────────────────


class TestNativeInPipeline:
    """Test that native philosophers work in the full run_turn pipeline."""

    def test_run_with_native_philosophers(self):
        """Full pipeline should work with native PhilosopherProtocol."""
        from po_core.app.api import run

        result = run("What is the meaning of life?")
        assert result["status"] in ("ok", "blocked")
        if result["status"] == "ok":
            assert "proposal" in result
            assert len(result["proposal"]["content"]) > 0

    def test_run_proposal_not_dummy(self):
        """Proposals should contain real philosopher reasoning."""
        from po_core.app.api import run

        result = run("Is AI conscious?")
        if result["status"] == "ok":
            content = result["proposal"]["content"]
            assert not content.startswith("[dummy]")
