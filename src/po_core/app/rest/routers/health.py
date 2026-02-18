"""
GET /v1/health — Health Check
"""

from __future__ import annotations

import time

from fastapi import APIRouter

from po_core.app.rest.models import HealthResponse
from po_core.philosophers.manifest import SPECS

router = APIRouter(tags=["health"])

# Server start time for uptime calculation
_start_time = time.monotonic()


@router.get(
    "/v1/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns server health status and basic system information.",
)
async def health() -> HealthResponse:
    """Health check endpoint — no authentication required."""
    try:
        from po_core import __version__

        version = __version__
    except (ImportError, AttributeError):
        version = "unknown"

    return HealthResponse(
        status="ok",
        version=version,
        philosophers_loaded=len(SPECS),
        uptime_seconds=round(time.monotonic() - _start_time, 2),
    )
