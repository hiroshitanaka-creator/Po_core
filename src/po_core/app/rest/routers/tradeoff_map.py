"""GET /v1/tradeoff-map/{session_id} — Trade-off map retrieval."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from po_core.app.rest.auth import require_api_key
from po_core.app.rest.store import get_trace_store
from po_core.viewer.tradeoff_map import build_tradeoff_map

router = APIRouter(tags=["tradeoff-map"])


@router.get(
    "/v1/tradeoff-map/{session_id}",
    summary="Retrieve trade-off map for a session",
    description=(
        "Builds and returns a trade-off map artifact from stored trace events "
        "for the specified session."
    ),
)
async def get_tradeoff_map(
    session_id: str,
    _: None = Depends(require_api_key),
    store: dict = Depends(get_trace_store),
) -> dict[str, Any]:
    """Return trade-off map generated from trace events for ``session_id``."""
    events = store.get(session_id)
    if events is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No trace found for session_id={session_id!r}",
        )

    return build_tradeoff_map(response=None, tracer=events)
