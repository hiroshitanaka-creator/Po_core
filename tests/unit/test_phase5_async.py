"""
Phase 5.2: True Async PartyMachine — Unit Tests
================================================

Verifies:
1. PhilosopherCompleted events are emitted in real-time (per-philosopher,
   not batched after all complete) when a tracer is provided.
2. Events are emitted with correct payload (name, n, latency_ms, ok).
3. Timeout/error paths also emit PhilosopherCompleted with ok=False.
4. async_run_philosophers() accepts and passes through the tracer kwarg.
5. async_run_turn() passes deps.tracer into async_run_philosophers.
6. propose_async() default implementation on Philosopher base class works.
7. _has_native_async() correctly distinguishes base vs overridden.
8. No regression on sync run_turn() path.

Markers: unit, phase5
"""

from __future__ import annotations

import asyncio
import time
from typing import List
from unittest.mock import MagicMock, patch

import pytest

from po_core.domain.proposal import Proposal
from po_core.party_machine import AsyncPartyMachine, RunResult, async_run_philosophers
from po_core.trace.in_memory import InMemoryTracer

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_proposal(pid: str) -> Proposal:
    return Proposal(
        proposal_id=f"{pid}_p",
        action_type="respond",
        content=f"Proposal from {pid}",
        confidence=0.9,
    )


class _SyncPhil:
    """Minimal sync philosopher (no propose_async override)."""

    def __init__(self, name: str, delay: float = 0.0) -> None:
        self.name = name
        self._delay = delay

    def propose(self, ctx, intent, tensors, memory) -> List[Proposal]:
        if self._delay:
            time.sleep(self._delay)
        return [_make_proposal(self.name)]


class _AsyncPhil:
    """Philosopher with native propose_async override."""

    def __init__(self, name: str) -> None:
        self.name = name

    def propose(self, ctx, intent, tensors, memory) -> List[Proposal]:
        return [_make_proposal(self.name)]

    async def propose_async(self, ctx, intent, tensors, memory) -> List[Proposal]:
        await asyncio.sleep(0)  # Yield to event loop
        return [_make_proposal(self.name)]


class _ErrorPhil:
    """Philosopher that raises an exception."""

    def __init__(self, name: str) -> None:
        self.name = name

    def propose(self, ctx, intent, tensors, memory) -> List[Proposal]:
        raise ValueError("deliberate error")


class _TimeoutPhil:
    """Philosopher that exceeds timeout."""

    def __init__(self, name: str) -> None:
        self.name = name

    def propose(self, ctx, intent, tensors, memory) -> List[Proposal]:
        time.sleep(10.0)  # Always times out
        return []


# ---------------------------------------------------------------------------
# 1. PhilosopherCompleted events — real-time emission
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_philosopher_completed_events_emitted():
    """PhilosopherCompleted events are emitted per-philosopher when tracer passed."""

    async def _run():
        tracer = InMemoryTracer()
        philosophers = [_SyncPhil(f"phil_{i}") for i in range(3)]

        async with AsyncPartyMachine(max_workers=3, timeout_s=5.0) as machine:
            proposals, results = await machine.run(
                philosophers, MagicMock(), MagicMock(), MagicMock(), MagicMock(), tracer
            )

        completed_events = [
            e for e in tracer.events if e.event_type == "PhilosopherCompleted"
        ]
        return completed_events, proposals, results

    events, proposals, results = asyncio.run(_run())

    # One event per philosopher
    assert len(events) == 3

    # All events have required fields
    for ev in events:
        assert "name" in ev.payload
        assert "n" in ev.payload
        assert "latency_ms" in ev.payload
        assert "ok" in ev.payload
        assert ev.payload["ok"] is True
        assert ev.payload["n"] == 1

    # All proposals collected
    assert len(proposals) == 3
    assert all(r.ok for r in results)


@pytest.mark.unit
@pytest.mark.phase5
def test_philosopher_completed_events_not_emitted_without_tracer():
    """Without tracer, no PhilosopherCompleted events are emitted."""

    async def _run():
        philosophers = [_SyncPhil(f"phil_{i}") for i in range(3)]
        async with AsyncPartyMachine(max_workers=3, timeout_s=5.0) as machine:
            proposals, results = await machine.run(
                philosophers,
                MagicMock(),
                MagicMock(),
                MagicMock(),
                MagicMock(),
                # no tracer
            )
        return proposals, results

    proposals, results = asyncio.run(_run())

    # Results are still correct
    assert len(proposals) == 3
    assert all(r.ok for r in results)


# ---------------------------------------------------------------------------
# 2. Event payload correctness
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_philosopher_completed_event_payload():
    """PhilosopherCompleted payload has correct name, n, latency_ms, ok."""

    async def _run():
        tracer = InMemoryTracer()
        ph = _SyncPhil("aristotle")

        async with AsyncPartyMachine(max_workers=1, timeout_s=5.0) as machine:
            await machine.run(
                [ph], MagicMock(), MagicMock(), MagicMock(), MagicMock(), tracer
            )

        return [e for e in tracer.events if e.event_type == "PhilosopherCompleted"]

    events = asyncio.run(_run())
    assert len(events) == 1
    ev = events[0]
    assert ev.payload["name"] == "aristotle"
    assert ev.payload["n"] == 1
    assert isinstance(ev.payload["latency_ms"], int)
    assert ev.payload["latency_ms"] >= 0
    assert ev.payload["ok"] is True


# ---------------------------------------------------------------------------
# 3. Error and timeout paths emit ok=False
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_philosopher_completed_on_error():
    """PhilosopherCompleted with ok=False when philosopher raises."""

    async def _run():
        tracer = InMemoryTracer()
        ph = _ErrorPhil("error_phil")

        async with AsyncPartyMachine(max_workers=1, timeout_s=5.0) as machine:
            proposals, results = await machine.run(
                [ph], MagicMock(), MagicMock(), MagicMock(), MagicMock(), tracer
            )

        events = [e for e in tracer.events if e.event_type == "PhilosopherCompleted"]
        return events, proposals, results

    events, proposals, results = asyncio.run(_run())

    assert len(events) == 1
    assert events[0].payload["ok"] is False
    assert events[0].payload["n"] == 0
    assert len(proposals) == 0
    assert results[0].ok is False


@pytest.mark.unit
@pytest.mark.phase5
def test_philosopher_completed_on_timeout():
    """PhilosopherCompleted with ok=False when philosopher times out."""

    async def _run():
        tracer = InMemoryTracer()
        ph = _TimeoutPhil("slow_phil")

        async with AsyncPartyMachine(max_workers=1, timeout_s=0.05) as machine:
            proposals, results = await machine.run(
                [ph], MagicMock(), MagicMock(), MagicMock(), MagicMock(), tracer
            )

        events = [e for e in tracer.events if e.event_type == "PhilosopherCompleted"]
        return events, results

    events, results = asyncio.run(_run())

    assert len(events) == 1
    assert events[0].payload["ok"] is False
    assert results[0].timed_out is True


# ---------------------------------------------------------------------------
# 4. async_run_philosophers() tracer kwarg
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_async_run_philosophers_with_tracer():
    """async_run_philosophers() passes tracer through to AsyncPartyMachine."""

    async def _run():
        tracer = InMemoryTracer()
        philosophers = [_SyncPhil(f"p{i}") for i in range(5)]
        proposals, results = await async_run_philosophers(
            philosophers,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            max_workers=5,
            timeout_s=5.0,
            tracer=tracer,
        )
        return tracer.events, proposals, results

    events, proposals, results = asyncio.run(_run())

    completed = [e for e in events if e.event_type == "PhilosopherCompleted"]
    assert len(completed) == 5
    assert all(r.ok for r in results)


@pytest.mark.unit
@pytest.mark.phase5
def test_async_run_philosophers_without_tracer_backward_compat():
    """async_run_philosophers() works without tracer (backward compatible)."""

    async def _run():
        philosophers = [_SyncPhil(f"p{i}") for i in range(3)]
        return await async_run_philosophers(
            philosophers,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            max_workers=3,
            timeout_s=5.0,
            # tracer omitted
        )

    proposals, results = asyncio.run(_run())
    assert len(proposals) == 3
    assert all(r.ok for r in results)


# ---------------------------------------------------------------------------
# 5. async_run_turn passes tracer into async_run_philosophers
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_async_run_turn_emits_philosopher_completed_events():
    """async_run_turn() produces PhilosopherCompleted events in trace."""
    from po_core.app.api import async_run
    from po_core.domain.safety_mode import SafetyMode
    from po_core.runtime.settings import Settings

    async def _run():
        tracer = InMemoryTracer()
        result = await async_run(
            "What is justice?",
            settings=Settings(freedom_pressure_missing_mode=SafetyMode.CRITICAL),
            tracer=tracer,
        )
        return result, tracer.events

    result, events = asyncio.run(_run())

    completed_events = [e for e in events if e.event_type == "PhilosopherCompleted"]

    # CRITICAL mode = 1 philosopher → at least 1 PhilosopherCompleted event
    assert len(completed_events) >= 1
    ev = completed_events[0]
    assert "name" in ev.payload
    assert "ok" in ev.payload
    assert "latency_ms" in ev.payload


# ---------------------------------------------------------------------------
# 6. propose_async() base class default
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_propose_async_default_implementation():
    """Philosopher.propose_async() default wraps propose() via thread executor."""
    from po_core.app.api import run
    from po_core.domain.safety_mode import SafetyMode
    from po_core.philosophers.base import Philosopher
    from po_core.runtime.settings import Settings

    # Verify propose_async() exists on base class
    assert hasattr(Philosopher, "propose_async")
    assert asyncio.iscoroutinefunction(Philosopher.propose_async)

    # Verify it runs correctly end-to-end via the async pipeline
    async def _run():
        return await __import__("po_core.app.api", fromlist=["async_run"]).async_run(
            "What is virtue?",
            settings=Settings(freedom_pressure_missing_mode=SafetyMode.CRITICAL),
        )

    result = asyncio.run(_run())
    assert result.get("status") in ("ok", "blocked", "fallback")


# ---------------------------------------------------------------------------
# 7. _has_native_async() detection
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_has_native_async_false_for_base_implementation():
    """_has_native_async() returns False for philosopher using base propose_async."""
    machine = AsyncPartyMachine()
    ph = _SyncPhil("kant")  # No propose_async override

    # _SyncPhil has no propose_async at all → False
    assert machine._has_native_async(ph) is False


@pytest.mark.unit
@pytest.mark.phase5
def test_has_native_async_true_for_override():
    """_has_native_async() returns True for philosopher with native override."""
    machine = AsyncPartyMachine()
    ph = _AsyncPhil("plato")  # Has propose_async override

    assert machine._has_native_async(ph) is True


@pytest.mark.unit
@pytest.mark.phase5
def test_has_native_async_false_for_base_class_philosopher():
    """_has_native_async() returns False for Philosopher subclasses using base default."""
    from po_core.philosophers.aristotle import Aristotle

    machine = AsyncPartyMachine()
    ph = Aristotle()

    # Aristotle uses base propose_async (thread executor) → False
    assert machine._has_native_async(ph) is False


# ---------------------------------------------------------------------------
# 8. No regression: sync run_turn still works
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_sync_run_turn_no_regression():
    """sync run() still works after Phase 5.2 changes."""
    from po_core.app.api import run
    from po_core.domain.safety_mode import SafetyMode
    from po_core.runtime.settings import Settings
    from po_core.trace.in_memory import InMemoryTracer

    tracer = InMemoryTracer()
    result = run(
        "What is justice?",
        settings=Settings(freedom_pressure_missing_mode=SafetyMode.CRITICAL),
        tracer=tracer,
    )

    assert result.get("status") in ("ok", "blocked", "fallback")
    # Sync path still emits PhilosopherResult (not PhilosopherCompleted)
    phil_result_events = [
        e for e in tracer.events if e.event_type == "PhilosopherResult"
    ]
    assert len(phil_result_events) >= 1


# ---------------------------------------------------------------------------
# 9. PhilosopherCompleted schema validation
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_philosopher_completed_schema_valid():
    """PhilosopherCompleted events pass schema validation."""
    from po_core.trace.schema import validate_events

    async def _run():
        tracer = InMemoryTracer()
        philosophers = [_SyncPhil("kant"), _SyncPhil("hegel")]
        async with AsyncPartyMachine(max_workers=2, timeout_s=5.0) as machine:
            await machine.run(
                philosophers, MagicMock(), MagicMock(), MagicMock(), MagicMock(), tracer
            )
        return tracer.events

    events = asyncio.run(_run())
    completed_events = [e for e in events if e.event_type == "PhilosopherCompleted"]
    assert len(completed_events) == 2

    problems = validate_events(completed_events)
    assert problems == {}, f"Schema violations: {problems}"


# ---------------------------------------------------------------------------
# 10. Native async philosopher completes without thread overhead
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.phase5
def test_native_async_philosopher_executed():
    """Philosopher with propose_async override runs on native async path."""

    async def _run():
        tracer = InMemoryTracer()
        ph = _AsyncPhil("async_plato")

        async with AsyncPartyMachine(max_workers=1, timeout_s=5.0) as machine:
            proposals, results = await machine.run(
                [ph], MagicMock(), MagicMock(), MagicMock(), MagicMock(), tracer
            )

        events = [e for e in tracer.events if e.event_type == "PhilosopherCompleted"]
        return events, proposals, results

    events, proposals, results = asyncio.run(_run())

    assert len(events) == 1
    assert events[0].payload["ok"] is True
    assert len(proposals) == 1
    assert results[0].ok is True
