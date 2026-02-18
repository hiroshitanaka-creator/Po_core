"""
FastAPI Application Factory
============================

Creates and configures the Po_core REST API application.

Usage:
    from po_core.app.rest.server import create_app
    app = create_app()

    # Or run directly:
    uvicorn po_core.app.rest.server:app --host 0.0.0.0 --port 8000

Security:
    CORS origins  — PO_CORS_ORIGINS (default: "*" for local dev)
    Rate limiting — PO_RATE_LIMIT_PER_MINUTE (default: 60/min per IP)
    API key auth  — PO_API_KEY + X-API-Key header
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from po_core.app.rest.config import APISettings, get_api_settings
from po_core.app.rest.rate_limit import limiter
from po_core.app.rest.routers import health, philosophers, reason, trace

logger = logging.getLogger(__name__)

# Module-level app instance (for uvicorn direct invocation)
app: FastAPI | None = None


def _rate_limit_handler(request: Request, exc: Exception) -> Response:
    """Typed wrapper so mypy accepts the handler signature for add_exception_handler."""
    return _rate_limit_exceeded_handler(request, exc)  # type: ignore[arg-type]


def _parse_cors_origins(cors_origins: str) -> list[str]:
    """
    Parse a comma-separated CORS origins string into a list.

    "*" is returned as-is (allow all).  Whitespace around each entry is stripped.
    """
    if cors_origins.strip() == "*":
        return ["*"]
    return [o.strip() for o in cors_origins.split(",") if o.strip()]


def create_app(settings: APISettings | None = None) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Args:
        settings: Optional APISettings override (useful for testing).
                  Defaults to the singleton returned by get_api_settings().

    Returns:
        Configured FastAPI instance with all routers registered.
    """
    settings = settings or get_api_settings()

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

    # CORS — restrict origins in production via PO_CORS_ORIGINS.
    # Default "*" allows all origins (convenient for local dev).
    # When specific origins are set, credentials are also allowed.
    allowed_origins = _parse_cors_origins(settings.cors_origins)
    allow_credentials = allowed_origins != ["*"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting — SlowAPI per-IP limiter.
    # Limit is configured via PO_RATE_LIMIT_PER_MINUTE (default: 60/min).
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_handler)

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
                "cors_origins": settings.cors_origins,
                "rate_limit_per_minute": settings.rate_limit_per_minute,
            },
        )

    return application


# Module-level instance for ``uvicorn po_core.app.rest.server:app``
app = create_app()
