"""
GET /v1/trace/{session_id} — Trace Retrieval
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from po_core.app.rest.auth import require_api_key
from po_core.app.rest.models import TraceEventOut, TraceResponse
from po_core.app.rest.store import get_trace_store

router = APIRouter(tags=["trace"])


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
    store: dict = Depends(get_trace_store),
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
