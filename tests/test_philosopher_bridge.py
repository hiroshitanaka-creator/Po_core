"""
PhilosopherBridge Tests
========================

Tests that the bridge adapter correctly converts legacy Philosopher.reason()
to PhilosopherProtocol.propose(), enabling the run_turn pipeline.
"""
from __future__ import annotations

from datetime import datetime, timezone

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.philosophers.base import Philosopher, PhilosopherInfo
from po_core.philosophers.bridge import PhilosopherBridge, bridge
from po_core.philosophers.manifest import SPECS
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.domain.safety_mode import SafetyMode


def _make_ctx(user_input: str = "test input") -> Context:
    return Context.now(request_id="test-001", user_input=user_input)


def _make_intent() -> Intent:
    return Intent.neutral()


def _make_tensors() -> TensorSnapshot:
    return TensorSnapshot.empty()


def _make_memory() -> MemorySnapshot:
    return MemorySnapshot.empty()


# ── Bridge wrapping tests ──────────────────────────────────────────────


class TestBridgeBasics:
    """Test that PhilosopherBridge correctly wraps a legacy philosopher."""

    def test_bridge_has_info(self):
        from po_core.philosophers.aristotle import Aristotle
        bridged = PhilosopherBridge(Aristotle())
        assert isinstance(bridged.info, PhilosopherInfo)
        assert "Aristotle" in bridged.info.name

    def test_bridge_has_propose(self):
        from po_core.philosophers.kant import Kant
        bridged = PhilosopherBridge(Kant())
        assert hasattr(bridged, "propose")
        assert callable(bridged.propose)

    def test_bridge_has_name(self):
        from po_core.philosophers.confucius import Confucius
        bridged = PhilosopherBridge(Confucius())
        assert hasattr(bridged, "name")
        assert isinstance(bridged.name, str)
        assert len(bridged.name) > 0

    def test_bridge_factory_function(self):
        from po_core.philosophers.sartre import Sartre
        bridged = bridge(Sartre())
        assert isinstance(bridged, PhilosopherBridge)
        assert hasattr(bridged, "propose")
        assert hasattr(bridged, "info")


class TestBridgePropose:
    """Test that propose() returns valid Proposal objects."""

    def test_propose_returns_list(self):
        from po_core.philosophers.aristotle import Aristotle
        bridged = PhilosopherBridge(Aristotle())
        result = bridged.propose(_make_ctx(), _make_intent(), _make_tensors(), _make_memory())
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_propose_returns_proposals(self):
        from po_core.philosophers.kant import Kant
        bridged = PhilosopherBridge(Kant())
        result = bridged.propose(_make_ctx(), _make_intent(), _make_tensors(), _make_memory())
        for p in result:
            assert isinstance(p, Proposal)

    def test_proposal_has_required_fields(self):
        from po_core.philosophers.nietzsche import Nietzsche
        bridged = PhilosopherBridge(Nietzsche())
        result = bridged.propose(_make_ctx("What is power?"), _make_intent(), _make_tensors(), _make_memory())
        p = result[0]
        assert p.proposal_id
        assert p.action_type == "answer"
        assert len(p.content) > 0
        assert 0.0 <= p.confidence <= 1.0

    def test_proposal_id_contains_request_id(self):
        from po_core.philosophers.heidegger import Heidegger
        ctx = _make_ctx("What is being?")
        bridged = PhilosopherBridge(Heidegger())
        result = bridged.propose(ctx, _make_intent(), _make_tensors(), _make_memory())
        assert ctx.request_id in result[0].proposal_id

    def test_proposal_content_is_reasoning(self):
        from po_core.philosophers.dewey import Dewey
        bridged = PhilosopherBridge(Dewey())
        result = bridged.propose(_make_ctx("What is education?"), _make_intent(), _make_tensors(), _make_memory())
        # Content should come from the philosopher's reasoning
        assert len(result[0].content) > 10

    def test_proposal_extra_has_philosopher_info(self):
        from po_core.philosophers.wittgenstein import Wittgenstein
        bridged = PhilosopherBridge(Wittgenstein())
        result = bridged.propose(_make_ctx(), _make_intent(), _make_tensors(), _make_memory())
        extra = result[0].extra
        assert "philosopher" in extra
        assert "perspective" in extra


class TestBridgeWithConfucius:
    """Confucius returns a non-standard dict (analysis/summary instead of reasoning).
    Bridge must handle this via normalize_response()."""

    def test_confucius_bridge_works(self):
        from po_core.philosophers.confucius import Confucius
        bridged = PhilosopherBridge(Confucius())
        result = bridged.propose(_make_ctx("What is virtue?"), _make_intent(), _make_tensors(), _make_memory())
        assert len(result) == 1
        p = result[0]
        assert len(p.content) > 0
        assert p.action_type == "answer"


# ── Registry auto-bridge tests ──────────────────────────────────────────


class TestRegistryAutoBridge:
    """Test that PhilosopherRegistry.load() auto-bridges legacy philosophers."""

    def test_registry_loads_with_bridge(self):
        """All 39 philosophers should load successfully via auto-bridge."""
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
            assert isinstance(result[0], Proposal), f"{ph.info.name} returned non-Proposal"

    def test_warn_mode_loads_subset(self):
        """WARN mode should load fewer philosophers, all bridged."""
        registry = PhilosopherRegistry(cache_instances=False)
        sel = registry.select(SafetyMode.WARN)
        philosophers, errors = registry.load(sel.selected_ids)
        assert len(errors) == 0
        assert len(philosophers) <= 5
        for ph in philosophers:
            assert hasattr(ph, "propose")

    def test_critical_mode_loads_one(self):
        """CRITICAL mode should load exactly 1 philosopher, bridged."""
        registry = PhilosopherRegistry(cache_instances=False)
        sel = registry.select(SafetyMode.CRITICAL)
        philosophers, errors = registry.load(sel.selected_ids)
        assert len(errors) == 0
        assert len(philosophers) == 1
        assert hasattr(philosophers[0], "propose")

    def test_dummy_philosopher_not_bridged(self):
        """DummyPhilosopher already implements PhilosopherProtocol natively."""
        registry = PhilosopherRegistry(cache_instances=False)
        philosophers, errors = registry.load(["dummy"])
        assert len(errors) == 0
        assert len(philosophers) == 1
        # DummyPhilosopher should NOT be wrapped in a bridge
        assert not isinstance(philosophers[0], PhilosopherBridge)


# ── Full pipeline smoke test ──────────────────────────────────────────


class TestBridgeInPipeline:
    """Test that bridged philosophers work in the full run_turn pipeline."""

    def test_run_with_bridged_philosophers(self):
        """Full pipeline should work with bridged philosophers."""
        from po_core.app.api import run
        result = run("What is the meaning of life?")
        assert result["status"] in ("ok", "blocked")
        if result["status"] == "ok":
            assert "proposal" in result
            assert len(result["proposal"]["content"]) > 0

    def test_run_proposal_not_dummy(self):
        """With bridge, proposals should contain real philosopher reasoning."""
        from po_core.app.api import run
        result = run("Is AI conscious?")
        if result["status"] == "ok":
            content = result["proposal"]["content"]
            # Should NOT be dummy stub "[dummy]..."
            assert not content.startswith("[dummy]")
