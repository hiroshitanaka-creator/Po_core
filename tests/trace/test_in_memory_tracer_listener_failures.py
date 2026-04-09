from __future__ import annotations

from po_core.domain.trace_event import TraceEvent
from po_core.trace.in_memory import InMemoryTracer


def test_in_memory_tracer_swallow_listener_exception_and_keeps_emitting() -> None:
    tracer = InMemoryTracer()
    observed = []

    def _broken_listener(event):
        raise RuntimeError("listener boom")

    def _ok_listener(event):
        observed.append(event.event_type)

    tracer.add_listener(_broken_listener)
    tracer.add_listener(_ok_listener)

    tracer.emit(TraceEvent.now("TestEvent", correlation_id="req-1", payload={}))

    assert [event.event_type for event in tracer.events] == ["TestEvent"]
    assert observed == ["TestEvent"]
