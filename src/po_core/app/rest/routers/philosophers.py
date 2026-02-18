"""
GET /v1/philosophers — Philosopher List
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from po_core.app.rest.auth import require_api_key
from po_core.app.rest.models import PhilosopherInfo, PhilosophersResponse
from po_core.philosophers.manifest import SPECS

router = APIRouter(tags=["philosophers"])


@router.get(
    "/v1/philosophers",
    response_model=PhilosophersResponse,
    summary="List all philosophers",
    description=(
        "Returns metadata for all registered philosophers including "
        "their name, module path, risk level, tags, and compute cost."
    ),
)
async def list_philosophers(
    _: None = Depends(require_api_key),
) -> PhilosophersResponse:
    """Return the full philosopher manifest."""
    infos = [
        PhilosopherInfo(
            philosopher_id=spec.philosopher_id,
            module=spec.module,
            symbol=spec.symbol,
            risk_level=spec.risk_level,
            weight=spec.weight,
            enabled=spec.enabled,
            tags=list(spec.tags),
            cost=spec.cost,
        )
        for spec in SPECS
    ]
    return PhilosophersResponse(total=len(infos), philosophers=infos)
