"""Human review queue storage for ESCALATE decisions."""

from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

from po_core.app.rest.config import get_api_settings


class ReviewStore(ABC):
    """Abstract backend for human-review queue records."""

    @abstractmethod
    def clear(self) -> None:
        """Clear all records (used for tests)."""

    @abstractmethod
    def enqueue(
        self,
        *,
        review_id: str,
        session_id: str,
        request_id: str,
        reason: str,
        source: str,
    ) -> Dict[str, Any]:
        """Create/update a pending review item."""

    @abstractmethod
    def get_pending(self) -> list[Dict[str, Any]]:
        """Return pending reviews in deterministic order."""

    @abstractmethod
    def apply_decision(
        self,
        review_id: str,
        *,
        decision: str,
        reviewer: str,
        comment: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Apply a decision to an existing review item."""


class InMemoryReviewStore(ReviewStore):
    """Legacy in-process queue backend."""

    def __init__(self) -> None:
        self._store: OrderedDict[str, Dict[str, Any]] = OrderedDict()

    def clear(self) -> None:
        self._store.clear()

    def enqueue(
        self,
        *,
        review_id: str,
        session_id: str,
        request_id: str,
        reason: str,
        source: str,
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        if review_id in self._store:
            current = self._store.pop(review_id)
            item = {
                **current,
                "status": "pending",
                "reason": reason,
                "source": source,
                "updated_at": now,
            }
        else:
            item = {
                "id": review_id,
                "session_id": session_id,
                "request_id": request_id,
                "status": "pending",
                "reason": reason,
                "source": source,
                "decision": None,
                "reviewer": None,
                "comment": None,
                "created_at": now,
                "updated_at": now,
                "decided_at": None,
            }

        self._store[review_id] = item
        settings = get_api_settings()
        while len(self._store) > settings.max_trace_sessions:
            self._store.popitem(last=False)
        return dict(item)

    def get_pending(self) -> list[Dict[str, Any]]:
        return [
            dict(item)
            for item in self._store.values()
            if item.get("status") == "pending"
        ]

    def apply_decision(
        self,
        review_id: str,
        *,
        decision: str,
        reviewer: str,
        comment: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        item = self._store.get(review_id)
        if item is None:
            return None

        now = datetime.now(timezone.utc)
        item["status"] = "decided"
        item["decision"] = decision
        item["reviewer"] = reviewer
        item["comment"] = comment or ""
        item["updated_at"] = now
        item["decided_at"] = now
        self._store[review_id] = self._store.pop(review_id)
        return dict(item)


class SQLiteReviewStore(ReviewStore):
    """SQLite-backed restart-safe review queue backend."""

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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS review_queue (
                    review_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    request_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    source TEXT NOT NULL,
                    decision TEXT,
                    reviewer TEXT,
                    comment TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    decided_at TEXT
                )
                """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_review_queue_status_updated ON review_queue(status, updated_at DESC)"
            )
            conn.commit()

    def clear(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM review_queue")
            conn.commit()

    def enqueue(
        self,
        *,
        review_id: str,
        session_id: str,
        request_id: str,
        reason: str,
        source: str,
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        with self._lock:
            with self._connect() as conn:
                existing = conn.execute(
                    "SELECT * FROM review_queue WHERE review_id = ?", (review_id,)
                ).fetchone()
                if existing is None:
                    created_at = now
                    conn.execute(
                        """
                        INSERT INTO review_queue (
                            review_id, session_id, request_id, status, reason, source,
                            decision, reviewer, comment, created_at, updated_at, decided_at
                        ) VALUES (?, ?, ?, 'pending', ?, ?, NULL, NULL, NULL, ?, ?, NULL)
                        """,
                        (
                            review_id,
                            session_id,
                            request_id,
                            reason,
                            source,
                            created_at.isoformat(),
                            now.isoformat(),
                        ),
                    )
                else:
                    created_at = datetime.fromisoformat(str(existing["created_at"]))
                    conn.execute(
                        """
                        UPDATE review_queue
                        SET status='pending', reason=?, source=?, decision=NULL,
                            reviewer=NULL, comment=NULL, updated_at=?, decided_at=NULL
                        WHERE review_id = ?
                        """,
                        (reason, source, now.isoformat(), review_id),
                    )

                self._evict_if_needed(conn)
                row = conn.execute(
                    "SELECT * FROM review_queue WHERE review_id = ?", (review_id,)
                ).fetchone()
                conn.commit()

        if row is None:
            return {
                "id": review_id,
                "session_id": session_id,
                "request_id": request_id,
                "status": "pending",
                "reason": reason,
                "source": source,
                "decision": None,
                "reviewer": None,
                "comment": None,
                "created_at": created_at,
                "updated_at": now,
                "decided_at": None,
            }
        return _row_to_item(row)

    def _evict_if_needed(self, conn: sqlite3.Connection) -> None:
        settings = get_api_settings()
        max_sessions = settings.max_trace_sessions
        if max_sessions <= 0:
            return
        rows = conn.execute(
            "SELECT review_id FROM review_queue ORDER BY updated_at DESC"
        ).fetchall()
        stale_ids = [row["review_id"] for row in rows[max_sessions:]]
        if stale_ids:
            conn.executemany(
                "DELETE FROM review_queue WHERE review_id = ?",
                [(review_id,) for review_id in stale_ids],
            )

    def get_pending(self) -> list[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT *
                FROM review_queue
                WHERE status = 'pending'
                ORDER BY created_at ASC, review_id ASC
                """).fetchall()
        return [_row_to_item(row) for row in rows]

    def apply_decision(
        self,
        review_id: str,
        *,
        decision: str,
        reviewer: str,
        comment: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        now = datetime.now(timezone.utc)
        with self._lock:
            with self._connect() as conn:
                exists = conn.execute(
                    "SELECT 1 FROM review_queue WHERE review_id = ?", (review_id,)
                ).fetchone()
                if exists is None:
                    return None

                conn.execute(
                    """
                    UPDATE review_queue
                    SET status='decided', decision=?, reviewer=?, comment=?,
                        updated_at=?, decided_at=?
                    WHERE review_id = ?
                    """,
                    (
                        decision,
                        reviewer,
                        comment or "",
                        now.isoformat(),
                        now.isoformat(),
                        review_id,
                    ),
                )
                row = conn.execute(
                    "SELECT * FROM review_queue WHERE review_id = ?", (review_id,)
                ).fetchone()
                conn.commit()
        return _row_to_item(row) if row is not None else None


def _row_to_item(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": str(row["review_id"]),
        "session_id": str(row["session_id"]),
        "request_id": str(row["request_id"]),
        "status": str(row["status"]),
        "reason": str(row["reason"]),
        "source": str(row["source"]),
        "decision": row["decision"],
        "reviewer": row["reviewer"],
        "comment": row["comment"],
        "created_at": datetime.fromisoformat(str(row["created_at"])),
        "updated_at": datetime.fromisoformat(str(row["updated_at"])),
        "decided_at": (
            datetime.fromisoformat(str(row["decided_at"]))
            if row["decided_at"]
            else None
        ),
    }


_review_store_singleton: ReviewStore | None = None


def _build_store() -> ReviewStore:
    settings = get_api_settings()
    backend = settings.review_store_backend.strip().lower()
    if backend == "memory":
        return InMemoryReviewStore()
    return SQLiteReviewStore(settings.review_db_path or settings.trace_db_path)


def get_review_store() -> ReviewStore:
    """FastAPI dependency returning the configured review store backend."""
    global _review_store_singleton
    if _review_store_singleton is None:
        _review_store_singleton = _build_store()
    return _review_store_singleton


def reset_review_store() -> None:
    """Reset module-level review store singleton (used in tests)."""
    global _review_store_singleton
    _review_store_singleton = None


class _LegacyReviewStoreCompat:
    """Compatibility shim for tests importing module-level _review_store."""

    def clear(self) -> None:
        store = get_review_store()
        store.clear()
        reset_review_store()


_review_store = _LegacyReviewStoreCompat()


def enqueue_review(
    *,
    review_id: str,
    session_id: str,
    request_id: str,
    reason: str,
    source: str,
) -> Dict[str, Any]:
    """Create/update a pending review item and apply configured eviction."""
    return get_review_store().enqueue(
        review_id=review_id,
        session_id=session_id,
        request_id=request_id,
        reason=reason,
        source=source,
    )


def get_pending_reviews() -> list[Dict[str, Any]]:
    """Return pending reviews in deterministic order."""
    return get_review_store().get_pending()


def apply_review_decision(
    review_id: str,
    *,
    decision: str,
    reviewer: str,
    comment: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Apply a human decision to a queued review item."""
    return get_review_store().apply_decision(
        review_id,
        decision=decision,
        reviewer=reviewer,
        comment=comment,
    )
