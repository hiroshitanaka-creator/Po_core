"""GET /v1/tradeoff-map/{session_id} — Trade-off map retrieval."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from po_core.app.rest.scopes import Scope, require_scope
from po_core.app.rest.store import get_trace_store
from po_core.axis.preferences import parse_weights_str
from po_core.viewer.preference_view import apply_preference_view
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
    weights: str | None = Query(
        default=None,
        description=(
            "Optional preference weights as comma-separated pairs, e.g. "
            "'safety:0.5,benefit:0.3,feasibility:0.2'"
        ),
    ),
    _: None = Depends(require_scope(Scope.TRACE_READ)),
    store: dict = Depends(get_trace_store),
) -> dict[str, Any]:
    """Return trade-off map generated from trace events for ``session_id``."""
    events = store.get(session_id)
    if events is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No trace found for session_id={session_id!r}",
        )

    tradeoff_map = build_tradeoff_map(response=None, tracer=events)
    if weights is None:
        return tradeoff_map

    parsed_weights = parse_weights_str(weights)
    return apply_preference_view(tradeoff_map, weights=parsed_weights)
