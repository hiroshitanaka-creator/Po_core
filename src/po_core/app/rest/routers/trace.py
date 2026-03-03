"""
GET /v1/trace/{session_id} — Trace Retrieval
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from po_core.app.rest.auth import require_api_key
from po_core.app.rest.models import (
    TraceEventOut,
    TraceHistoryItem,
    TraceHistoryResponse,
    TraceResponse,
)
from po_core.app.rest.store import TraceHistorySummary, TraceStore, get_trace_store

router = APIRouter(tags=["trace"])


@router.get(
    "/v1/trace/history",
    response_model=TraceHistoryResponse,
    summary="Retrieve persisted trace history",
    description="Returns recent trace sessions with event counts.",
)
async def get_trace_history(
    limit: int = Query(default=50, ge=1, le=500),
    _: None = Depends(require_api_key),
    store: TraceStore = Depends(get_trace_store),
) -> TraceHistoryResponse:
    """Return recent trace session summaries in descending recency order."""
    summaries: list[TraceHistorySummary] = store.history(limit=limit)
    items = [
        TraceHistoryItem(
            session_id=s["session_id"],
            event_count=s["event_count"],
            last_occurred_at=s["last_occurred_at"],
        )
        for s in summaries
    ]
    return TraceHistoryResponse(total=len(items), items=items)


@router.get(
    "/v1/trace/{session_id}",
    response_model=TraceResponse,
    summary="Retrieve trace events for a session",
    description=(
        "Returns all trace events recorded during a reasoning session. "
        "Events include tensor computations, philosopher deliberations, "
        "safety gate decisions, and the final proposal."
    ),
)
async def get_trace(
    session_id: str,
    _: None = Depends(require_api_key),
    store: TraceStore = Depends(get_trace_store),
) -> TraceResponse:
    """Return trace events for the given session_id."""
    events = store.get(session_id)
    if events is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No trace found for session_id={session_id!r}",
        )

    out_events = [
        TraceEventOut(
            event_type=e.event_type,
            occurred_at=e.occurred_at,
            correlation_id=e.correlation_id,
            payload=dict(e.payload),
        )
        for e in events
    ]
    return TraceResponse(
        session_id=session_id,
        event_count=len(out_events),
        events=out_events,
    )
