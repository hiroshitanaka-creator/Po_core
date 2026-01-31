from __future__ import annotations

from typing import Sequence

from po_core.domain.trace_event import TraceEvent
from po_core.ports.trace import TracePort


class NoopTracer(TracePort):
    def emit(self, event: TraceEvent) -> None:
        return

    def emit_many(self, events: Sequence[TraceEvent]) -> None:
        return
