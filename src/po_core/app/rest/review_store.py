"""In-process human review queue store for ESCALATE decisions."""

from __future__ import annotations

from collections import OrderedDict
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from po_core.app.rest.config import get_api_settings

_review_store: OrderedDict[str, Dict[str, Any]] = OrderedDict()


def get_review_store() -> Dict[str, Dict[str, Any]]:
    """FastAPI dependency returning review queue records."""
    return _review_store


def enqueue_review(
    *,
    review_id: str,
    session_id: str,
    request_id: str,
    reason: str,
    source: str,
) -> Dict[str, Any]:
    """Create/update a pending review item and apply LRU-style eviction."""
    now = datetime.now(timezone.utc)
    if review_id in _review_store:
        current = _review_store.pop(review_id)
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

    _review_store[review_id] = item

    settings = get_api_settings()
    while len(_review_store) > settings.max_trace_sessions:
        _review_store.popitem(last=False)

    return item


def get_pending_reviews() -> list[Dict[str, Any]]:
    """Return pending reviews in insertion order."""
    return [item for item in _review_store.values() if item.get("status") == "pending"]


def apply_review_decision(
    review_id: str,
    *,
    decision: str,
    reviewer: str,
    comment: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Apply a human decision to a pending review item."""
    item = _review_store.get(review_id)
    if item is None:
        return None

    now = datetime.now(timezone.utc)
    item["status"] = "decided"
    item["decision"] = decision
    item["reviewer"] = reviewer
    item["comment"] = comment or ""
    item["updated_at"] = now
    item["decided_at"] = now

    _review_store[review_id] = _review_store.pop(review_id)
    return item
