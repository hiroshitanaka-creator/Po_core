"""
Structured trace logger for Po_trace.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from po_core.po_trace.models import TraceEntry, TraceSession
from po_core.utils.trace_store import TraceStore


class TraceLogger:
    """Accumulates trace entries for a single execution."""

    def __init__(
        self,
        store: Optional[TraceStore] = None,
        session_id: Optional[str] = None,
    ) -> None:
        self.store = store
        self.session_id = session_id or str(uuid4())
        self._entries: List[TraceEntry] = []
        self._prompt: Optional[str] = None
        self._started_at: Optional[datetime] = None

    def start_session(self, prompt: str) -> None:
        self._prompt = prompt
        self._started_at = datetime.utcnow()

    def record(self, entry: TraceEntry) -> None:
        self._entries.append(entry)

    def finish(self, spoken_text: str) -> TraceSession:
        if self._prompt is None or self._started_at is None:
            raise RuntimeError("Trace session has not been started")

        session = TraceSession(
            session_id=self.session_id,
            prompt=self._prompt,
            spoken_summary=spoken_text,
            created_at=self._started_at,
            completed_at=datetime.utcnow(),
            entries=list(self._entries),
        )

        if self.store:
            self.store.append(session)

        return session


__all__ = [
    "TraceLogger",
]
