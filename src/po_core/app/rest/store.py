"""
In-process Trace Store
=======================

Maintains an LRU-bounded dict mapping session_id → list[TraceEvent].
Used by the trace router and populated by the reason endpoint.

This is intentionally simple (in-memory, single-process).
For multi-process deployments swap this out with a Redis adapter.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Dict, List

from po_core.app.rest.config import get_api_settings
from po_core.domain.trace_event import TraceEvent

# Module-level singleton
_store: OrderedDict[str, List[TraceEvent]] = OrderedDict()


def get_trace_store() -> Dict[str, List[TraceEvent]]:
    """FastAPI dependency returning the trace store dict."""
    return _store


def save_trace(session_id: str, events: List[TraceEvent]) -> None:
    """Persist trace events for a session, evicting oldest when full."""
    settings = get_api_settings()
    if session_id in _store:
        del _store[session_id]
    _store[session_id] = events
    # LRU eviction
    while len(_store) > settings.max_trace_sessions:
        _store.popitem(last=False)
