from __future__ import annotations

import json
import sqlite3
from abc import ABC, abstractmethod
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import List, TypedDict

from po_core.app.rest.config import get_api_settings
from po_core.domain.trace_event import TraceEvent


class TraceHistorySummary(TypedDict):
    session_id: str
    event_count: int
    last_occurred_at: datetime


class TraceStore(ABC):
    """Abstract storage backend for trace events."""

    @abstractmethod
    def get(self, session_id: str) -> List[TraceEvent] | None:
        """Return trace events for a session, or None when missing."""

    @abstractmethod
    def save(self, session_id: str, events: List[TraceEvent]) -> None:
        """Persist trace events for a session."""

    @abstractmethod
    def history(self, limit: int = 50) -> List[TraceHistorySummary]:
        """Return recent session summaries sorted by newest first."""


class InMemoryTraceStore(TraceStore):
    """In-process LRU-bounded trace store (legacy backend)."""

    def __init__(self) -> None:
        self._store: OrderedDict[str, List[TraceEvent]] = OrderedDict()
        self._sessions: OrderedDict[str, datetime] = OrderedDict()

    def clear(self) -> None:
        self._store.clear()
        self._sessions.clear()

    def get(self, session_id: str) -> List[TraceEvent] | None:
        if session_id in self._store:
            return list(self._store[session_id])
        if session_id in self._sessions:
            return []
        return None

    def save(self, session_id: str, events: List[TraceEvent]) -> None:
        settings = get_api_settings()
        if session_id in self._store:
            del self._store[session_id]
        if session_id in self._sessions:
            del self._sessions[session_id]
        self._store[session_id] = list(events)
        updated_at = events[-1].occurred_at if events else datetime.utcnow()
        self._sessions[session_id] = updated_at
        while len(self._sessions) > settings.max_trace_sessions:
            stale_id, _ = self._sessions.popitem(last=False)
            self._store.pop(stale_id, None)

    def history(self, limit: int = 50) -> List[TraceHistorySummary]:
        items = list(self._sessions.items())[-limit:]
        summaries: List[TraceHistorySummary] = []
        for session_id, updated_at in reversed(items):
            events = self._store.get(session_id, [])
            summaries.append(
                {
                    "session_id": session_id,
                    "event_count": len(events),
                    "last_occurred_at": (
                        events[-1].occurred_at if events else updated_at
                    ),
                }
            )
        return summaries


class SQLiteTraceStore(TraceStore):
    """SQLite-backed persistent trace store."""

    def __init__(self, db_path: str) -> None:
        self._db_path = Path(db_path)
        if self._db_path.parent != Path(""):
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path), detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trace_sessions (
                    session_id TEXT PRIMARY KEY,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trace_events (
                    session_id TEXT NOT NULL,
                    event_idx INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    correlation_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    PRIMARY KEY (session_id, event_idx)
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_trace_events_session ON trace_events(session_id)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_trace_events_occurred ON trace_events(occurred_at DESC)"
            )
            conn.commit()

    def get(self, session_id: str) -> List[TraceEvent] | None:
        with self._connect() as conn:
            session_exists = conn.execute(
                "SELECT 1 FROM trace_sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
            rows = conn.execute(
                """
                SELECT event_type, occurred_at, correlation_id, payload_json
                FROM trace_events
                WHERE session_id = ?
                ORDER BY event_idx ASC
                """,
                (session_id,),
            ).fetchall()
        if not rows:
            return [] if session_exists else None
        return [
            TraceEvent(
                event_type=row["event_type"],
                occurred_at=datetime.fromisoformat(row["occurred_at"]),
                correlation_id=row["correlation_id"],
                payload=json.loads(row["payload_json"]),
            )
            for row in rows
        ]

    def save(self, session_id: str, events: List[TraceEvent]) -> None:
        settings = get_api_settings()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO trace_sessions(session_id, updated_at) VALUES (?, ?)",
                    (
                        session_id,
                        (
                            events[-1].occurred_at.isoformat()
                            if events
                            else datetime.utcnow().isoformat()
                        ),
                    ),
                )
                conn.execute(
                    "DELETE FROM trace_events WHERE session_id = ?", (session_id,)
                )
                conn.executemany(
                    """
                    INSERT INTO trace_events (
                        session_id, event_idx, event_type, occurred_at, correlation_id, payload_json
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            session_id,
                            idx,
                            event.event_type,
                            event.occurred_at.isoformat(),
                            event.correlation_id,
                            json.dumps(
                                dict(event.payload), ensure_ascii=False, sort_keys=True
                            ),
                        )
                        for idx, event in enumerate(events)
                    ],
                )
                self._evict_if_needed(conn, settings.max_trace_sessions)
                conn.commit()

    def _evict_if_needed(self, conn: sqlite3.Connection, max_sessions: int) -> None:
        if max_sessions <= 0:
            return
        rows = conn.execute(
            """
            SELECT session_id
            FROM trace_sessions
            ORDER BY updated_at DESC
            """
        ).fetchall()
        stale_session_ids = [row["session_id"] for row in rows[max_sessions:]]
        if stale_session_ids:
            conn.executemany(
                "DELETE FROM trace_events WHERE session_id = ?",
                [(sid,) for sid in stale_session_ids],
            )
            conn.executemany(
                "DELETE FROM trace_sessions WHERE session_id = ?",
                [(sid,) for sid in stale_session_ids],
            )

    def history(self, limit: int = 50) -> List[TraceHistorySummary]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT s.session_id AS session_id,
                       COUNT(e.event_idx) AS event_count,
                       COALESCE(MAX(e.occurred_at), s.updated_at) AS last_occurred_at
                FROM trace_sessions s
                LEFT JOIN trace_events e ON e.session_id = s.session_id
                GROUP BY s.session_id, s.updated_at
                ORDER BY s.updated_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [
            TraceHistorySummary(
                session_id=str(row["session_id"]),
                event_count=int(row["event_count"]),
                last_occurred_at=datetime.fromisoformat(str(row["last_occurred_at"])),
            )
            for row in rows
        ]


_trace_store_singleton: TraceStore | None = None


def _build_store() -> TraceStore:
    settings = get_api_settings()
    backend = settings.trace_store_backend.strip().lower()
    if backend == "memory":
        return InMemoryTraceStore()
    return SQLiteTraceStore(settings.trace_db_path)


def get_trace_store() -> TraceStore:
    """FastAPI dependency returning the configured trace store."""
    global _trace_store_singleton
    if _trace_store_singleton is None:
        _trace_store_singleton = _build_store()
    return _trace_store_singleton


def reset_trace_store() -> None:
    """Reset module-level trace store singleton (used in tests)."""
    global _trace_store_singleton
    _trace_store_singleton = None


class _LegacyStoreCompat:
    """Compatibility shim for tests importing module-level _store."""

    def clear(self) -> None:
        store = get_trace_store()
        if isinstance(store, InMemoryTraceStore):
            store.clear()
        reset_trace_store()


_store = _LegacyStoreCompat()


def save_trace(session_id: str, events: List[TraceEvent]) -> None:
    """Persist trace events for a session via configured store backend."""
    get_trace_store().save(session_id, events)


def append_trace_event(session_id: str, event: TraceEvent) -> None:
    """Append a single trace event to an existing session."""
    store = get_trace_store()
    existing = store.get(session_id) or []
    store.save(session_id, existing + [event])
