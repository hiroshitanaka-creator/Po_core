from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Set

from po_core.domain.trace_event import TraceEvent
from po_core.ports.trace import TracePort

# Listener callback: receives a TraceEvent.
EventListener = Callable[[TraceEvent], None]


@dataclass
class InMemoryTracer(TracePort):
    """In-memory tracer with event-bus listener support.

    Listeners can subscribe to specific event types or to all events.
    This enables push-style delivery for the Viewer WebUI and any
    future streaming consumers.
    """

    events: List[TraceEvent] = field(default_factory=list)
    max_events: int = 10_000
    _listeners: Dict[Optional[str], List[EventListener]] = field(
        default_factory=dict, repr=False
    )

    # ── Core TracePort interface ────────────────────────────────

    def emit(self, event: TraceEvent) -> None:
        if len(self.events) < self.max_events:
            self.events.append(event)
        self._notify(event)

    def emit_many(self, events: Sequence[TraceEvent]) -> None:
        for e in events:
            self.emit(e)

    # ── Event bus: subscribe / unsubscribe ──────────────────────

    def subscribe(
        self,
        listener: EventListener,
        event_types: Optional[Sequence[str]] = None,
    ) -> None:
        """Register *listener* for push-style event delivery.

        Args:
            listener: Callback invoked with each matching ``TraceEvent``.
            event_types: If given, the listener is called only for these
                event types.  ``None`` means "all events".
        """
        if event_types is None:
            self._listeners.setdefault(None, []).append(listener)
        else:
            for et in event_types:
                self._listeners.setdefault(et, []).append(listener)

    def unsubscribe(self, listener: EventListener) -> None:
        """Remove *listener* from all subscriptions."""
        for key in list(self._listeners):
            lst = self._listeners[key]
            self._listeners[key] = [fn for fn in lst if fn is not listener]
            if not self._listeners[key]:
                del self._listeners[key]

    # ── Query helpers ───────────────────────────────────────────

    def filter_by_type(self, event_type: str) -> List[TraceEvent]:
        """Return events matching *event_type*."""
        return [e for e in self.events if e.event_type == event_type]

    def event_types(self) -> Set[str]:
        """Return the set of distinct event types recorded so far."""
        return {e.event_type for e in self.events}

    # ── Internal ────────────────────────────────────────────────

    def _notify(self, event: TraceEvent) -> None:
        """Dispatch *event* to all matching listeners."""
        # Wildcard listeners (subscribed to all events)
        for fn in self._listeners.get(None, ()):
            try:
                fn(event)
            except Exception:
                pass  # listener failures must not break the pipeline
        # Type-specific listeners
        for fn in self._listeners.get(event.event_type, ()):
            try:
                fn(event)
            except Exception:
                pass
