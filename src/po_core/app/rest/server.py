"""
FastAPI Application Factory
============================

Creates and configures the Po_core REST API application.

Usage:
    from po_core.app.rest.server import create_app
    app = create_app()

    # Or run directly:
    uvicorn po_core.app.rest.server:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from po_core.app.rest.config import get_api_settings
from po_core.app.rest.routers import health, philosophers, reason, trace

logger = logging.getLogger(__name__)

# Module-level app instance (for uvicorn direct invocation)
app: FastAPI | None = None


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI instance with all routers registered.
    """
    settings = get_api_settings()

    application = FastAPI(
        title="Po_core REST API",
        summary="Philosophy-driven AI deliberation via 39 philosopher personas",
        description="""
## Po_core REST API

A production REST API for the **Po_core** philosophical deliberation engine.

### Architecture
39 philosopher AI personas deliberate via tensor calculations
(Freedom Pressure, Semantic Delta, Blocked Tensor) and a 3-layer **W_Ethics Gate**
to generate ethically responsible responses.

### Authentication
Include your API key in the `X-API-Key` header for all requests.
Set `PO_API_KEY` environment variable to enable authentication.
Leave empty or set `PO_SKIP_AUTH=true` for development mode.

### Pipeline
```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine → ParetoAggregate → ShadowPareto → ActionGate → MemoryWrite
```
        """,
        version="0.2.0-beta",
        contact={
            "name": "Flying Pig Project",
            "url": "https://github.com/hiroshitanaka-creator/Po_core",
            "email": "flyingpig0229+github@gmail.com",
        },
        license_info={"name": "MIT"},
        openapi_tags=[
            {
                "name": "reason",
                "description": "Philosophical reasoning endpoints",
            },
            {
                "name": "philosophers",
                "description": "Philosopher metadata and manifest",
            },
            {
                "name": "trace",
                "description": "Audit trail and trace event retrieval",
            },
            {
                "name": "health",
                "description": "Server health and status",
            },
        ],
    )

    # CORS — allow all origins by default (restrict in production via env)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    application.include_router(reason.router)
    application.include_router(philosophers.router)
    application.include_router(trace.router)
    application.include_router(health.router)

    @application.on_event("startup")
    async def _startup() -> None:
        logger.info(
            "Po_core REST API starting",
            extra={
                "host": settings.host,
                "port": settings.port,
                "auth_enabled": bool(settings.api_key) and not settings.skip_auth,
            },
        )

    return application


# Module-level instance for ``uvicorn po_core.app.rest.server:app``
app = create_app()
