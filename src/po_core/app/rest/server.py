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
    CORS origins  — PO_CORS_ORIGINS (default: localhost-only allowlist)
    Rate limiting — PO_RATE_LIMIT_PER_MINUTE (default: 60/min per IP)
    API key auth  — PO_API_KEY with fail-closed defaults; primary header defaults to X-API-Key
"""

from __future__ import annotations

import logging
from typing import cast

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from po_core import __version__
from po_core.app.rest.auth import evaluate_auth_policy
from po_core.app.rest.config import (
    APISettings,
    get_api_settings,
    parse_cors_origins,
    set_api_settings,
)
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
    """Backward-compatible wrapper around shared CORS parsing settings."""
    return parse_cors_origins(cors_origins)


def _validate_execution_mode_configuration(settings: APISettings) -> None:
    """Reject unsafe cooperative timeout mode on the REST server unless explicitly allowed."""
    mode = settings.philosopher_execution_mode.strip().lower()
    if mode != "thread":
        return
    if settings.allow_unsafe_thread_execution:
        logger.warning(
            "Po_core REST API running with unsafe thread execution mode override",
            extra={"execution_mode": mode},
        )
        return
    raise RuntimeError(
        "Startup aborted: PO_PHILOSOPHER_EXECUTION_MODE=thread is refused by the REST server "
        "because cooperative timeouts are not fail-closed. "
        "Use PO_PHILOSOPHER_EXECUTION_MODE=process, or set "
        "PO_ALLOW_UNSAFE_THREAD_EXECUTION=true for short-lived development only."
    )


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


def _validate_worker_storage_configuration(settings: APISettings) -> None:
    """Fail fast when sqlite backends are configured for multi-worker deployment."""
    sqlite_backends: list[str] = []
    if settings.trace_store_backend.strip().lower() == "sqlite":
        sqlite_backends.append("trace")
    if settings.review_store_backend.strip().lower() == "sqlite":
        sqlite_backends.append("review")

    if settings.workers <= 1 or not sqlite_backends:
        return

    backend_list = ", ".join(sqlite_backends)
    raise RuntimeError(
        "Startup aborted: workers > 1 is not supported with sqlite storage backends. "
        f"workers={settings.workers}, sqlite_backends={backend_list}. "
        "Use PO_WORKERS=1, or switch PO_TRACE_STORE_BACKEND / PO_REVIEW_STORE_BACKEND to memory "
        "or another multi-worker-safe backend."
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
        from po_core.app.rest.review_store import reset_review_store
        from po_core.app.rest.store import reset_trace_store

        reset_trace_store()
        reset_review_store()
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
Recommended default in every environment: keep `PO_SKIP_AUTH=false` and set a non-empty `PO_API_KEY`.
If `PO_SKIP_AUTH=false` and `PO_API_KEY` is empty/blank, startup fails fast by design.
Use `PO_SKIP_AUTH=true` only for short-lived local development when you intentionally want no auth.
Clients should send the API key in `X-API-Key` by default.
The public REST path also defaults to `PO_PHILOSOPHER_EXECUTION_MODE=process` and refuses `thread` mode unless `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` is explicitly set for development.
`PO_API_KEY_HEADER` is an optional advanced override for deployments that need a different primary header name, and `X-API-Key` remains accepted for backwards compatibility.

### Pipeline
```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine → ParetoAggregate → ShadowPareto → ActionGate → MemoryWrite
```

### License
- Open source: [AGPL-3.0-or-later](https://github.com/hiroshitanaka-creator/Po_core/blob/main/LICENSE)
- Commercial: [Commercial License Terms](https://github.com/hiroshitanaka-creator/Po_core/blob/main/COMMERCIAL_LICENSE.md)
        """,
        version=__version__,
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

    # CORS — default to localhost-only origins for safer package defaults.
    # Use PO_CORS_ORIGINS="*" only when you intentionally want permissive dev CORS.
    # When specific origins are set, credentials are also allowed.
    allowed_origins = parse_cors_origins(settings.cors_origins)
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
        _validate_execution_mode_configuration(settings)
        _validate_worker_storage_configuration(settings)

    return application


# Module-level instance for ``uvicorn po_core.app.rest.server:app``
app = create_app()
