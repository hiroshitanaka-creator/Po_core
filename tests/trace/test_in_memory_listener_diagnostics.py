from __future__ import annotations

import logging

from po_core.domain.trace_event import TraceEvent
from po_core.trace.in_memory import InMemoryTracer


def test_in_memory_tracer_logs_listener_failures(caplog):
    tracer = InMemoryTracer()

    def _broken_listener(_event):
        raise ValueError("listener failed")

    tracer.add_listener(_broken_listener)

    with caplog.at_level(logging.WARNING):
        tracer.emit(TraceEvent.now("TestEvent", "req-1", {}))

    assert any("Trace listener failed" in message for message in caplog.messages)
