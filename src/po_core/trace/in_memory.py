from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence

from po_core.domain.trace_event import TraceEvent
from po_core.ports.trace import TracePort


@dataclass
class InMemoryTracer(TracePort):
    events: List[TraceEvent] = field(default_factory=list)
    max_events: int = 10_000

    def emit(self, event: TraceEvent) -> None:
        if len(self.events) < self.max_events:
            self.events.append(event)

    def emit_many(self, events: Sequence[TraceEvent]) -> None:
        for e in events:
            self.emit(e)
