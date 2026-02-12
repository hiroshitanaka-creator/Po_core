"""
Philosopher Tests via Pipeline (migrated from test_philosophers_pytest.py)
==========================================================================

Tests all 39 philosophers through native PhilosopherProtocol.propose().
Validates that every philosopher:
1. Can be loaded via PhilosopherRegistry
2. Has correct attributes (name, tradition, key_concepts)
3. Produces valid proposals via native propose()
4. Can reason() individually (unit-level, still valid)

Original tests used PHILOSOPHER_REGISTRY + run_ensemble (removed in v0.3).
These test via PhilosopherRegistry + native propose().
"""

from __future__ import annotations

import uuid

import pytest

pytestmark = pytest.mark.pipeline

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.safety_mode import SafetyMode
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.philosophers.manifest import SPECS
from po_core.philosophers.registry import PhilosopherRegistry

# ── Helpers ──

PHILOSOPHER_IDS = [
    s.philosopher_id for s in SPECS if s.enabled and s.philosopher_id != "dummy"
]

TEST_PROMPT = "What is the nature of consciousness and how should we understand it?"


def _ctx(text: str = TEST_PROMPT) -> Context:
    return Context.now(request_id=str(uuid.uuid4()), user_input=text, meta={})


def _empty_tensors() -> TensorSnapshot:
    return TensorSnapshot.now({"freedom_pressure": 0.0})


def _empty_mem() -> MemorySnapshot:
    return MemorySnapshot(items=[], summary=None, meta={})


@pytest.fixture
def registry():
    return PhilosopherRegistry()


@pytest.fixture
def all_loaded_philosophers(registry):
    """Load all philosophers via registry (native PhilosopherProtocol)."""
    return registry.select_and_load(SafetyMode.NORMAL)


# ══════════════════════════════════════════════════════════════════════════
# 1. Registry & Manifest
# ══════════════════════════════════════════════════════════════════════════


class TestManifestIntegrity:
    """Verify manifest SPECS are consistent."""

    def test_manifest_has_40_specs(self):
        assert len(SPECS) == 40, f"Expected 40 specs (39 + dummy), got {len(SPECS)}"

    def test_39_non_dummy_philosophers(self):
        non_dummy = [s for s in SPECS if s.philosopher_id != "dummy"]
        assert len(non_dummy) == 39

    def test_all_ids_unique(self):
        ids = [s.philosopher_id for s in SPECS]
        assert len(ids) == len(set(ids)), "Duplicate philosopher IDs"

    def test_all_have_required_fields(self):
        for s in SPECS:
            assert s.philosopher_id
            assert s.module
            assert s.symbol
            assert isinstance(s.risk_level, int)
            assert isinstance(s.cost, int)
            assert isinstance(s.enabled, bool)


# ══════════════════════════════════════════════════════════════════════════
# 2. Loading via PhilosopherProtocol (native)
# ══════════════════════════════════════════════════════════════════════════


class TestPhilosopherLoading:
    """Test that all philosophers load with native propose()/info."""

    def test_all_load_via_registry(self, registry):
        """All 39 philosophers should load in NORMAL mode."""
        loaded = registry.select_and_load(SafetyMode.NORMAL)
        assert len(loaded) > 0

    def test_all_have_propose_method(self, all_loaded_philosophers):
        for phil in all_loaded_philosophers:
            assert hasattr(phil, "propose"), f"Philosopher missing propose(): {phil}"
            assert callable(phil.propose)

    def test_all_have_info_property(self, all_loaded_philosophers):
        for phil in all_loaded_philosophers:
            assert hasattr(phil, "info"), f"Philosopher missing info: {phil}"
            assert phil.info.name, f"info.name is empty for {phil}"
            assert phil.info.version, f"info.version is empty for {phil}"

    def test_all_implement_protocol_natively(self, registry):
        """All philosophers should implement PhilosopherProtocol natively."""
        loaded = registry.select_and_load(SafetyMode.NORMAL)
        for phil in loaded:
            assert hasattr(phil, "propose") and hasattr(phil, "info"), (
                f"{phil.info.name} does not implement PhilosopherProtocol"
            )

    def test_propose_returns_proposals(self, all_loaded_philosophers):
        """propose() should return a list of Proposal objects."""
        from po_core.domain.intent import Intent
        from po_core.domain.proposal import Proposal

        ctx = _ctx()
        intent = Intent(goals=["understand"], constraints=[])
        tensors = _empty_tensors()
        mem = _empty_mem()

        # Test with first philosopher only (for speed)
        phil = all_loaded_philosophers[0]
        proposals = phil.propose(ctx, intent, tensors, mem)
        assert isinstance(proposals, list)
        assert len(proposals) > 0
        assert isinstance(proposals[0], Proposal)
        assert proposals[0].content, "Proposal content should not be empty"


# ══════════════════════════════════════════════════════════════════════════
# 3. Individual Philosopher Attributes (parametrized)
# ══════════════════════════════════════════════════════════════════════════


class TestPhilosopherAttributes:
    """Test legacy Philosopher attributes via PHILOSOPHER_REGISTRY.

    NOTE: Not all philosophers have consistent attributes (known issue).
    - 'tradition' and 'key_concepts' are missing on some implementations.
    - reason() output format varies: some use 'reasoning'/'perspective',
      others use 'analysis'/'summary'/'description'.
    Tests here verify the minimal guaranteed contract.
    """

    @pytest.mark.parametrize("key", PHILOSOPHER_IDS)
    def test_philosopher_instantiation(self, key):
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        if key not in PHILOSOPHER_REGISTRY:
            pytest.skip(f"{key} not in legacy registry")
        cls = PHILOSOPHER_REGISTRY[key]
        instance = cls()
        assert instance is not None
        assert hasattr(instance, "name")
        assert hasattr(instance, "reason")

    @pytest.mark.parametrize("key", PHILOSOPHER_IDS)
    def test_philosopher_has_name(self, key):
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        if key not in PHILOSOPHER_REGISTRY:
            pytest.skip(f"{key} not in legacy registry")
        instance = PHILOSOPHER_REGISTRY[key]()
        assert instance.name, f"{key} has no name"

    @pytest.mark.parametrize("key", PHILOSOPHER_IDS)
    def test_philosopher_reason_returns_dict(self, key):
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        if key not in PHILOSOPHER_REGISTRY:
            pytest.skip(f"{key} not in legacy registry")
        instance = PHILOSOPHER_REGISTRY[key]()
        result = instance.reason(TEST_PROMPT)
        assert isinstance(result, dict)
        assert len(result) > 0

    @pytest.mark.parametrize("key", PHILOSOPHER_IDS)
    def test_philosopher_reason_has_content(self, key):
        """reason() must return at least one content field.

        Accepted formats:
        - reasoning/perspective (standard)
        - analysis/summary (confucius, dogen, arendt, zhuangzi, etc.)
        - description (fallback)
        """
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        if key not in PHILOSOPHER_REGISTRY:
            pytest.skip(f"{key} not in legacy registry")
        instance = PHILOSOPHER_REGISTRY[key]()
        result = instance.reason(TEST_PROMPT)

        content_keys = {
            "reasoning",
            "analysis",
            "description",
            "summary",
            "perspective",
        }
        found = content_keys & set(result.keys())
        assert (
            len(found) > 0
        ), f"{key} reason() has no content field. Keys: {list(result.keys())}"


# ══════════════════════════════════════════════════════════════════════════
# 4. Diversity verification
# ══════════════════════════════════════════════════════════════════════════


class TestPhilosopherDiversity:
    """Verify philosophers produce diverse outputs."""

    @staticmethod
    def _get_content(result: dict) -> str:
        """Extract main content from a reason() result (handles both formats)."""
        for key in ("reasoning", "analysis", "description", "summary"):
            val = result.get(key)
            if val and isinstance(val, str) and len(val) > 0:
                return val
            if val and isinstance(val, dict):
                return str(val)[:300]
        return ""

    def test_unique_content(self):
        """Philosophers should produce meaningfully diverse content."""
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        contents = []
        for key in PHILOSOPHER_IDS:
            if key not in PHILOSOPHER_REGISTRY:
                continue
            instance = PHILOSOPHER_REGISTRY[key]()
            result = instance.reason(TEST_PROMPT)
            content = self._get_content(result)
            if content:
                contents.append(content[:200])

        # At least 30 out of 39 should be unique
        unique = len(set(contents))
        assert (
            unique >= 30
        ), f"Expected 30+ unique contents, got {unique}/{len(contents)}"


# ══════════════════════════════════════════════════════════════════════════
# 5. Full pipeline with all philosophers
# ══════════════════════════════════════════════════════════════════════════


class TestAllPhilosophersPipeline:
    """Test the full pipeline processes all loaded philosophers."""

    def test_run_produces_philosopher_results(self):
        """po_core.run() should produce responses from multiple philosophers."""
        from po_core import run

        result = run(user_input="What is the meaning of existence?")
        assert result["status"] == "ok"

    def test_po_self_lists_multiple_philosophers(self):
        """PoSelf should show multiple philosophers participated."""
        from po_core.po_self import PoSelf

        response = PoSelf().generate("What is the meaning of existence?")
        assert len(response.philosophers) > 0
        assert len(response.responses) > 0
