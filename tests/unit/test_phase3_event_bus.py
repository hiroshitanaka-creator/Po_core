"""
Tests for InMemoryTracer event bus (Phase 3).

Validates subscribe, unsubscribe, type filtering, and query helpers.
"""

import pytest

from po_core.domain.trace_event import TraceEvent
from po_core.trace.in_memory import InMemoryTracer

pytestmark = [pytest.mark.unit, pytest.mark.observability]


def _make_event(event_type: str = "TestEvent", cid: str = "req-1") -> TraceEvent:
    return TraceEvent.now(event_type, cid, {"key": "val"})


class TestEventBusSubscribe:
    """Listener receives events after subscribing."""

    def test_wildcard_listener_receives_all(self):
        tracer = InMemoryTracer()
        received = []
        tracer.subscribe(received.append)

        tracer.emit(_make_event("A"))
        tracer.emit(_make_event("B"))

        assert len(received) == 2
        assert received[0].event_type == "A"
        assert received[1].event_type == "B"

    def test_typed_listener_receives_matching_only(self):
        tracer = InMemoryTracer()
        received = []
        tracer.subscribe(received.append, event_types=["TensorComputed"])

        tracer.emit(_make_event("TensorComputed"))
        tracer.emit(_make_event("MemorySnapshotted"))
        tracer.emit(_make_event("TensorComputed"))

        assert len(received) == 2
        assert all(e.event_type == "TensorComputed" for e in received)

    def test_multiple_type_subscription(self):
        tracer = InMemoryTracer()
        received = []
        tracer.subscribe(received.append, event_types=["A", "C"])

        tracer.emit(_make_event("A"))
        tracer.emit(_make_event("B"))
        tracer.emit(_make_event("C"))

        assert len(received) == 2
        assert received[0].event_type == "A"
        assert received[1].event_type == "C"


class TestEventBusUnsubscribe:
    """Listener stops receiving after unsubscribe."""

    def test_unsubscribe_wildcard(self):
        tracer = InMemoryTracer()
        received = []

        def listener(e):
            received.append(e)

        tracer.subscribe(listener)

        tracer.emit(_make_event("A"))
        tracer.unsubscribe(listener)
        tracer.emit(_make_event("B"))

        assert len(received) == 1

    def test_unsubscribe_typed(self):
        tracer = InMemoryTracer()
        received = []

        def listener(e):
            received.append(e)

        tracer.subscribe(listener, event_types=["X"])

        tracer.emit(_make_event("X"))
        tracer.unsubscribe(listener)
        tracer.emit(_make_event("X"))

        assert len(received) == 1


class TestEventBusErrorResilience:
    """Listener errors must not break the pipeline."""

    def test_failing_listener_does_not_break_emit(self):
        tracer = InMemoryTracer()
        good_received = []

        def bad_listener(e):
            raise RuntimeError("boom")

        tracer.subscribe(bad_listener)
        tracer.subscribe(good_received.append)

        tracer.emit(_make_event("A"))

        # Event still stored and good listener still called
        assert len(tracer.events) == 1
        assert len(good_received) == 1


class TestTracerQueryHelpers:
    """filter_by_type and event_types helpers."""

    def test_filter_by_type(self):
        tracer = InMemoryTracer()
        tracer.emit(_make_event("A"))
        tracer.emit(_make_event("B"))
        tracer.emit(_make_event("A"))

        result = tracer.filter_by_type("A")
        assert len(result) == 2

    def test_filter_by_type_empty(self):
        tracer = InMemoryTracer()
        tracer.emit(_make_event("A"))

        assert tracer.filter_by_type("Z") == []

    def test_event_types(self):
        tracer = InMemoryTracer()
        tracer.emit(_make_event("A"))
        tracer.emit(_make_event("B"))
        tracer.emit(_make_event("A"))

        assert tracer.event_types() == {"A", "B"}

    def test_event_types_empty(self):
        tracer = InMemoryTracer()
        assert tracer.event_types() == set()
