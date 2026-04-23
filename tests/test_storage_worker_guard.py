from __future__ import annotations

import sqlite3

import pytest
from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.review_store import SQLiteReviewStore
from po_core.app.rest.server import create_app
from po_core.app.rest.store import InMemoryTraceStore, SQLiteTraceStore
from po_core.domain.trace_event import TraceEvent

EXPECTED_STARTUP_MESSAGE = (
    "Startup aborted: workers > 1 is not supported with sqlite storage backends. "
    "workers=2, sqlite_backends=trace, review. "
    "Use PO_WORKERS=1, or switch PO_TRACE_STORE_BACKEND / PO_REVIEW_STORE_BACKEND to memory "
    "or another multi-worker-safe backend."
)


def test_startup_fails_fast_when_multiple_workers_use_sqlite_backends(tmp_path) -> None:
    app = create_app(
        APISettings(
            skip_auth=True,
            api_key="",
            workers=2,
            trace_store_backend="sqlite",
            trace_db_path=str(tmp_path / "trace_store.sqlite3"),
            review_store_backend="sqlite",
            review_db_path=str(tmp_path / "review_store.sqlite3"),
        )
    )

    with pytest.raises(
        RuntimeError, match="workers > 1 is not supported with sqlite"
    ) as excinfo:
        with TestClient(app, raise_server_exceptions=True):
            pass

    assert str(excinfo.value) == EXPECTED_STARTUP_MESSAGE


def test_trace_store_applies_sqlite_pragmas(tmp_path) -> None:
    db_path = tmp_path / "trace_store.sqlite3"
    store = SQLiteTraceStore(str(db_path))

    with store._connect() as conn:
        journal_mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        busy_timeout = conn.execute("PRAGMA busy_timeout").fetchone()[0]

    assert journal_mode.lower() == "wal"
    assert busy_timeout == 5000

    raw_conn = sqlite3.connect(str(db_path))
    try:
        raw_conn.row_factory = sqlite3.Row
        journal_mode = raw_conn.execute("PRAGMA journal_mode").fetchone()[0]
        assert str(journal_mode).lower() == "wal"
    finally:
        raw_conn.close()


def test_review_store_applies_sqlite_pragmas(tmp_path) -> None:
    db_path = tmp_path / "review_store.sqlite3"
    store = SQLiteReviewStore(str(db_path))

    with store._connect() as conn:
        journal_mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        busy_timeout = conn.execute("PRAGMA busy_timeout").fetchone()[0]

    assert journal_mode.lower() == "wal"
    assert busy_timeout == 5000


def test_sqlite_trace_store_append_persists_incrementally(tmp_path) -> None:
    store = SQLiteTraceStore(str(tmp_path / "trace_store.sqlite3"))
    session_id = "s-append"
    first = TraceEvent.now("EventA", session_id, {"n": 1})
    second = TraceEvent.now("EventB", session_id, {"n": 2})

    store.append(session_id, first)
    store.append(session_id, second)

    events = store.get(session_id)
    assert events is not None
    assert [e.event_type for e in events] == ["EventA", "EventB"]
    assert [e.payload["n"] for e in events] == [1, 2]

    with store._connect() as conn:
        cnt = conn.execute(
            "SELECT COUNT(*) FROM trace_events WHERE session_id = ?",
            (session_id,),
        ).fetchone()[0]
    assert cnt == 2


def test_inmemory_trace_store_append_keeps_existing_events() -> None:
    store = InMemoryTraceStore()
    session_id = "mem-append"
    first = TraceEvent.now("EventA", session_id, {"n": 1})
    second = TraceEvent.now("EventB", session_id, {"n": 2})

    store.append(session_id, first)
    store.append(session_id, second)

    events = store.get(session_id)
    assert events is not None
    assert [e.event_type for e in events] == ["EventA", "EventB"]
