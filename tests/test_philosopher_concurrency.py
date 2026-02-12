"""
39-Philosopher Concurrent Operation Tests
==========================================

Phase 1, Task 3: Validate that all 39 philosophers execute correctly
in parallel without deadlocks, memory corruption, or excessive latency.

Tests:
- Full parallel execution with ThreadPoolExecutor
- Timeout enforcement for slow philosophers
- No duplicate or missing proposals
- Latency distribution within bounds
- Memory footprint within bounds
- SafetyMode scaling (39 → 5 → 1)
"""

from __future__ import annotations

import time
import tracemalloc
import uuid
from unittest.mock import patch

import pytest

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.party_machine import RunResult, run_philosophers
from po_core.philosophers.base import Philosopher
from po_core.philosophers.registry import PhilosopherRegistry

# ── Helpers ──


def _ctx(text: str = "What is the nature of consciousness?") -> Context:
    return Context.now(request_id=str(uuid.uuid4()), user_input=text)


def _intent() -> Intent:
    return Intent.neutral()


def _tensors(fp: float = 0.0) -> TensorSnapshot:
    return TensorSnapshot.now({"freedom_pressure": fp})


def _memory() -> MemorySnapshot:
    return MemorySnapshot(items=[], summary=None, meta={})


@pytest.fixture
def registry():
    return PhilosopherRegistry(cache_instances=True)


@pytest.fixture
def all_philosophers(registry):
    """Load all philosophers for NORMAL mode."""
    sel = registry.select(SafetyMode.NORMAL)
    philosophers, errors = registry.load(sel.selected_ids)
    assert len(errors) == 0, f"Load errors: {errors}"
    return philosophers


# ══════════════════════════════════════════════════════════════════════════
# 1. Full Parallel Execution
# ══════════════════════════════════════════════════════════════════════════


class TestParallelExecution:
    """Verify all 39 philosophers execute in parallel without issues."""

    def test_all_philosophers_produce_proposals(self, all_philosophers):
        """Every loaded philosopher should produce at least one proposal."""
        proposals, results = run_philosophers(
            all_philosophers,
            _ctx(),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=12,
            timeout_s=2.0,
        )

        # Check counts
        ok_results = [r for r in results if r.ok]
        failed = [r for r in results if not r.ok]

        assert len(ok_results) == len(
            all_philosophers
        ), f"{len(failed)} philosopher(s) failed: " + ", ".join(
            f"{r.philosopher_id}: {r.error}" for r in failed
        )
        assert len(proposals) == len(all_philosophers)

    def test_no_duplicate_proposals(self, all_philosophers):
        """Each philosopher should produce exactly one distinct proposal."""
        proposals, results = run_philosophers(
            all_philosophers,
            _ctx(),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=12,
            timeout_s=2.0,
        )

        proposal_ids = [p.proposal_id for p in proposals]
        assert len(proposal_ids) == len(set(proposal_ids)), "Duplicate proposal IDs"

    def test_all_proposals_are_valid(self, all_philosophers):
        """All proposals should have required fields."""
        proposals, _ = run_philosophers(
            all_philosophers,
            _ctx("Is free will an illusion?"),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=12,
            timeout_s=2.0,
        )

        for p in proposals:
            assert isinstance(p, Proposal)
            assert p.proposal_id
            assert p.action_type == "answer"
            assert len(p.content) > 0
            assert 0.0 <= p.confidence <= 1.0

    def test_results_track_all_philosophers(self, all_philosophers):
        """RunResult should be recorded for every philosopher."""
        _, results = run_philosophers(
            all_philosophers,
            _ctx(),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=12,
            timeout_s=2.0,
        )

        assert len(results) == len(all_philosophers)
        for r in results:
            assert r.philosopher_id
            assert r.latency_ms is not None or r.timed_out


# ══════════════════════════════════════════════════════════════════════════
# 2. Timeout Enforcement
# ══════════════════════════════════════════════════════════════════════════


class _SlowPhilosopher(Philosopher):
    """A philosopher that sleeps for a configurable duration."""

    def __init__(self, sleep_s: float = 5.0):
        super().__init__(
            name="SlowPhilosopher",
            description="Deliberately slow for testing",
        )
        self._sleep_s = sleep_s
        self.tradition = "Testing"
        self.key_concepts = ["slowness"]

    def reason(self, prompt, context=None):
        time.sleep(self._sleep_s)
        return {"reasoning": "slow", "perspective": "slow"}


class TestTimeoutEnforcement:
    """Verify that slow philosophers time out without blocking others."""

    def test_slow_philosopher_times_out(self):
        """A philosopher exceeding timeout should be marked timed_out."""
        slow = _SlowPhilosopher(sleep_s=5.0)
        proposals, results = run_philosophers(
            [slow],
            _ctx(),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=1,
            timeout_s=0.1,
        )

        assert len(results) == 1
        assert results[0].timed_out is True
        assert results[0].ok is False
        assert len(proposals) == 0

    def test_timeout_does_not_block_others(self, all_philosophers):
        """One slow philosopher should not prevent others from completing."""
        slow = _SlowPhilosopher(sleep_s=5.0)
        mixed = list(all_philosophers) + [slow]

        proposals, results = run_philosophers(
            mixed,
            _ctx(),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=12,
            timeout_s=2.0,
        )

        timed_out = [r for r in results if r.timed_out]
        ok_results = [r for r in results if r.ok]

        # The slow philosopher should time out
        assert len(timed_out) >= 1
        # All real philosophers should complete
        assert len(ok_results) >= len(all_philosophers) - 1


# ══════════════════════════════════════════════════════════════════════════
# 3. Latency Distribution
# ══════════════════════════════════════════════════════════════════════════


class TestLatencyProfile:
    """Verify latency distribution is within acceptable bounds."""

    def test_all_within_timeout(self, all_philosophers):
        """All philosopher latencies should be under the timeout."""
        _, results = run_philosophers(
            all_philosophers,
            _ctx(),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=12,
            timeout_s=2.0,
        )

        for r in results:
            if r.ok and r.latency_ms is not None:
                assert (
                    r.latency_ms < 2000
                ), f"{r.philosopher_id} took {r.latency_ms}ms (> 2000ms timeout)"

    def test_median_latency_reasonable(self, all_philosophers):
        """Median latency should be well under timeout."""
        _, results = run_philosophers(
            all_philosophers,
            _ctx(),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=12,
            timeout_s=2.0,
        )

        latencies = sorted(
            r.latency_ms for r in results if r.ok and r.latency_ms is not None
        )
        if latencies:
            median = latencies[len(latencies) // 2]
            assert median < 500, f"Median latency {median}ms is too high"


# ══════════════════════════════════════════════════════════════════════════
# 4. Memory Footprint
# ══════════════════════════════════════════════════════════════════════════


class TestMemoryFootprint:
    """Verify memory usage stays within bounds."""

    def test_loading_39_philosophers_memory(self):
        """Loading 39 philosophers should use reasonable memory."""
        tracemalloc.start()
        snapshot_before = tracemalloc.take_snapshot()

        registry = PhilosopherRegistry(cache_instances=True)
        sel = registry.select(SafetyMode.NORMAL)
        philosophers, _ = registry.load(sel.selected_ids)

        snapshot_after = tracemalloc.take_snapshot()
        tracemalloc.stop()

        # Calculate memory delta
        stats = snapshot_after.compare_to(snapshot_before, "lineno")
        total_increase = sum(s.size_diff for s in stats if s.size_diff > 0)

        # Loading 39 philosophers should use < 10 MB
        assert (
            total_increase < 10 * 1024 * 1024
        ), f"Memory increase {total_increase / 1024 / 1024:.1f}MB exceeds 10MB limit"

    def test_execution_memory_stable(self, all_philosophers):
        """Running 39 philosophers should not leak memory significantly."""
        tracemalloc.start()

        # Run 3 times to check for growth
        for _ in range(3):
            run_philosophers(
                all_philosophers,
                _ctx(),
                _intent(),
                _tensors(),
                _memory(),
                max_workers=12,
                timeout_s=2.0,
            )

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Peak memory during execution should be < 20 MB
        assert (
            peak < 20 * 1024 * 1024
        ), f"Peak memory {peak / 1024 / 1024:.1f}MB exceeds 20MB limit"


# ══════════════════════════════════════════════════════════════════════════
# 5. SafetyMode Scaling
# ══════════════════════════════════════════════════════════════════════════


class TestSafetyModeScaling:
    """Verify correct philosopher counts per SafetyMode."""

    def test_normal_mode_selects_many(self, registry):
        """NORMAL mode should select many philosophers (up to 39)."""
        sel = registry.select(SafetyMode.NORMAL)
        assert len(sel.selected_ids) > 10

    def test_warn_mode_selects_few(self, registry):
        """WARN mode should select at most 5 philosophers."""
        sel = registry.select(SafetyMode.WARN)
        assert 1 <= len(sel.selected_ids) <= 5

    def test_critical_mode_selects_one(self, registry):
        """CRITICAL mode should select exactly 1 philosopher."""
        sel = registry.select(SafetyMode.CRITICAL)
        assert len(sel.selected_ids) == 1

    def test_warn_mode_excludes_risky(self, registry):
        """WARN mode should not include risk_level=2 philosophers."""
        from po_core.philosophers.manifest import SPECS

        spec_map = {s.philosopher_id: s for s in SPECS}
        sel = registry.select(SafetyMode.WARN)
        for pid in sel.selected_ids:
            if pid in spec_map:
                assert (
                    spec_map[pid].risk_level <= 1
                ), f"{pid} has risk_level={spec_map[pid].risk_level} in WARN mode"

    def test_critical_mode_only_safe(self, registry):
        """CRITICAL mode should only include risk_level=0 philosophers."""
        from po_core.philosophers.manifest import SPECS

        spec_map = {s.philosopher_id: s for s in SPECS}
        sel = registry.select(SafetyMode.CRITICAL)
        for pid in sel.selected_ids:
            if pid in spec_map:
                assert (
                    spec_map[pid].risk_level == 0
                ), f"{pid} has risk_level={spec_map[pid].risk_level} in CRITICAL mode"

    def test_all_modes_produce_proposals(self, registry):
        """Every SafetyMode should produce at least one proposal."""
        for mode in (SafetyMode.NORMAL, SafetyMode.WARN, SafetyMode.CRITICAL):
            sel = registry.select(mode)
            philosophers, errors = registry.load(sel.selected_ids)
            assert len(errors) == 0, f"{mode}: {errors}"

            proposals, results = run_philosophers(
                philosophers,
                _ctx(),
                _intent(),
                _tensors(),
                _memory(),
                max_workers=12,
                timeout_s=2.0,
            )

            ok = [r for r in results if r.ok]
            assert len(ok) > 0, f"{mode} produced 0 successful results"
            assert len(proposals) > 0, f"{mode} produced 0 proposals"


# ══════════════════════════════════════════════════════════════════════════
# 6. Diverse Prompts
# ══════════════════════════════════════════════════════════════════════════


class TestDiversePrompts:
    """Verify 39 philosophers handle diverse prompt types."""

    PROMPTS = [
        "What is the nature of consciousness?",
        "Should AI systems have rights?",
        "How should we balance freedom and security?",
        "Is there an objective morality?",
        "人工知能に倫理は必要か？",  # Japanese
    ]

    @pytest.mark.parametrize("prompt", PROMPTS)
    def test_all_succeed_with_prompt(self, all_philosophers, prompt):
        """All philosophers should produce proposals for each prompt type."""
        proposals, results = run_philosophers(
            all_philosophers,
            _ctx(prompt),
            _intent(),
            _tensors(),
            _memory(),
            max_workers=12,
            timeout_s=2.0,
        )

        failed = [r for r in results if not r.ok]
        assert (
            len(failed) == 0
        ), f"Prompt '{prompt[:30]}...': {len(failed)} failed: " + ", ".join(
            r.philosopher_id for r in failed
        )
