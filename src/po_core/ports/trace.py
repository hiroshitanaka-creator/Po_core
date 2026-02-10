from __future__ import annotations

from typing import Protocol, Sequence

from po_core.domain.trace_event import TraceEvent


class TracePort(Protocol):
    def emit(self, event: TraceEvent) -> None: ...

    def emit_many(self, events: Sequence[TraceEvent]) -> None: ...
