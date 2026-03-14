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
from typing import cast

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from po_core.app.rest.auth import evaluate_auth_policy
from po_core.app.rest.config import APISettings, get_api_settings, set_api_settings
from po_core.app.rest.rate_limit import limiter
from po_core.app.rest.routers import (
    health,
    philosophers,
    reason,
    review,
    trace,
    tradeoff_map,
)

logger = logging.getLogger(__name__)

# Module-level app instance (for uvicorn direct invocation)
app: FastAPI | None = None


def _rate_limit_handler(request: Request, exc: Exception) -> Response:
    """Typed wrapper so mypy accepts the handler signature for add_exception_handler."""
    return _rate_limit_exceeded_handler(request, cast(RateLimitExceeded, exc))


def _parse_cors_origins(cors_origins: str) -> list[str]:
    """
    Parse a comma-separated CORS origins string into a list.

    "*" is returned as-is (allow all).  Whitespace around each entry is stripped.
    """
    if cors_origins.strip() == "*":
        return ["*"]
    return [o.strip() for o in cors_origins.split(",") if o.strip()]


def _validate_startup_auth_configuration(settings: APISettings) -> None:
    """Fail fast on startup when production auth is misconfigured."""
    auth_state = evaluate_auth_policy(
        skip_auth=settings.skip_auth,
        configured_api_key=settings.api_key,
        presented_api_key=settings.api_key,
    )
    if auth_state.allowed:
        return
    if auth_state.is_misconfigured:
        raise RuntimeError(
            "Startup aborted: authentication is enabled (PO_SKIP_AUTH=false) "
            "but PO_API_KEY is unset or blank. "
            "Set PO_API_KEY to a non-empty value, or set PO_SKIP_AUTH=true for development only."
        )


def create_app(settings: APISettings | None = None) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Args:
        settings: Optional APISettings override (useful for testing).
                  Defaults to the singleton returned by get_api_settings().

    Returns:
        Configured FastAPI instance with all routers registered.
    """
    if settings is not None:
        set_api_settings(settings)
    settings = get_api_settings()

    application = FastAPI(
        title="Po_core REST API",
        summary="Philosophy-driven AI deliberation via 42 philosopher personas",
        description="""
## Po_core REST API

A production REST API for the **Po_core** philosophical deliberation engine.

### Architecture
42 philosopher AI personas deliberate via tensor calculations
(Freedom Pressure, Semantic Delta, Blocked Tensor) and a 3-layer **W_Ethics Gate**
to generate ethically responsible responses.

### Authentication
Include your API key in the `X-API-Key` header for all requests.
Set `PO_API_KEY` and keep `PO_SKIP_AUTH=false` to enforce authentication.
If `PO_SKIP_AUTH=false` and `PO_API_KEY` is empty/blank, startup fails fast by design.
Set `PO_SKIP_AUTH=true` only for development mode.

### Pipeline
```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine → ParetoAggregate → ShadowPareto → ActionGate → MemoryWrite
```

### License
- Open source: [AGPL-3.0-or-later](https://github.com/hiroshitanaka-creator/Po_core/blob/main/LICENSE)
- Commercial: [Commercial License Terms](https://github.com/hiroshitanaka-creator/Po_core/blob/main/COMMERCIAL_LICENSE.md)
        """,
        version="1.0.0",
        contact={
            "name": "Flying Pig Project",
            "url": "https://github.com/hiroshitanaka-creator/Po_core",
            "email": "flyingpig0229+github@gmail.com",
        },
        license_info={
            "name": "AGPL-3.0-or-later + Commercial",
            "url": "https://github.com/hiroshitanaka-creator/Po_core/blob/main/LICENSE",
        },
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
                "name": "tradeoff-map",
                "description": "Trade-off map retrieval for recorded sessions",
            },
            {
                "name": "health",
                "description": "Server health and status",
            },
            {
                "name": "review",
                "description": "Human-in-the-loop review queue",
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
    # settings is stored on app.state so the dynamic limit callable in
    # reason.py can read rate_limit_per_minute at request time rather than
    # from a frozen os.environ value.
    application.state.limiter = limiter
    application.state.settings = settings
    application.add_exception_handler(RateLimitExceeded, _rate_limit_handler)

    # Register routers
    application.include_router(reason.router)
    application.include_router(philosophers.router)
    application.include_router(trace.router)
    application.include_router(tradeoff_map.router)
    application.include_router(health.router)
    application.include_router(review.router)

    @application.on_event("startup")
    async def _startup() -> None:
        logger.info(
            "Po_core REST API starting",
            extra={
                "host": settings.host,
                "port": settings.port,
                "auth_enabled": bool(settings.api_key) and not settings.skip_auth,
                "skip_auth": settings.skip_auth,
                "cors_origins": settings.cors_origins,
                "rate_limit_per_minute": settings.rate_limit_per_minute,
            },
        )

        _validate_startup_auth_configuration(settings)

    return application


# Module-level instance for ``uvicorn po_core.app.rest.server:app``
app = create_app()
