from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence

from po_core.domain.trace_event import TraceEvent
from po_core.ports.trace import TracePort

# Listener callback type: receives a TraceEvent, returns nothing.
TraceListener = Callable[[TraceEvent], None]


@dataclass
class InMemoryTracer(TracePort):
    """
    In-memory tracer with optional listener callbacks.

    Stores events in a list (up to max_events) and notifies
    registered listeners on each emit. Listeners enable
    real-time streaming to Viewer WebUI (Phase 3.4 foundation).

    Usage::

        tracer = InMemoryTracer()

        # Register a listener for real-time updates
        tracer.add_listener(lambda e: print(f"Event: {e.event_type}"))

        tracer.emit(TraceEvent.now("TestEvent", "req-1", {}))
    """

    events: List[TraceEvent] = field(default_factory=list)
    max_events: int = 10_000
    _listeners: List[TraceListener] = field(default_factory=list)

    def emit(self, event: TraceEvent) -> None:
        if len(self.events) < self.max_events:
            self.events.append(event)
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                pass  # Listener failure must not break tracing

    def emit_many(self, events: Sequence[TraceEvent]) -> None:
        for e in events:
            self.emit(e)

    def add_listener(self, listener: TraceListener) -> None:
        """Register a callback invoked on every emit()."""
        self._listeners.append(listener)

    def remove_listener(self, listener: TraceListener) -> None:
        """Unregister a previously registered listener."""
        try:
            self._listeners.remove(listener)
        except ValueError:
            pass

    @property
    def listener_count(self) -> int:
        """Number of registered listeners."""
        return len(self._listeners)
