"""
Po_core Public API
==================

This module exposes the programmatic facade used by public callers.
It also carries a legacy FastAPI compatibility surface (`app`) that remains for
backward compatibility, but the canonical HTTP surface is `po_core.app.rest`.

Programmatic callers should use `run()` / `async_run()`. New HTTP integrations should use `po_core.app.rest.server:create_app`.

Usage:
    from po_core.app.api import run

    result = run(
        user_input="What is justice?",
        memory_backend=poself_instance,
        settings=Settings(),
    )

Architecture:
    ┌─────────────────────────────────────────────────────────┐
    │  External (03_api/, examples/*, tests)                  │
    │  ↓ ONLY imports po_core.app.api                         │
    ├─────────────────────────────────────────────────────────┤
    │  po_core.app.api  ← THIS FILE (facade)                  │
    │  ↓ uses runtime/wiring.py → ensemble.run_turn           │
    ├─────────────────────────────────────────────────────────┤
    │  Internal (philosophers, tensors, safety, autonomy)     │
    │  ↓ never imported directly from outside                 │
    └─────────────────────────────────────────────────────────┘
"""

from __future__ import annotations

import os
import uuid
import warnings

from fastapi import FastAPI, Header, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from po_core.app.rest.auth import evaluate_auth_policy, extract_api_key_from_headers
from po_core.app.rest.config import APISettings, parse_cors_origins
from po_core.domain.context import Context
from po_core.ensemble import EnsembleDeps, async_run_turn, run_turn
from po_core.philosophers.allowlist import AllowlistRegistry
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.ports.trace import TracePort
from po_core.runtime.settings import Settings
from po_core.runtime.wiring import build_default_system, build_system


def _ensure_api_key(
    settings: APISettings,
    x_api_key: str | None,
    authorization: str | None,
) -> None:
    decision = evaluate_auth_policy(
        skip_auth=settings.skip_auth,
        configured_api_key=settings.api_key,
        presented_api_key=extract_api_key_from_headers(
            x_api_key=x_api_key,
            authorization=authorization,
        ),
    )
    if decision.allowed:
        return
    if decision.is_misconfigured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=decision.message,
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=decision.message,
        headers={"WWW-Authenticate": "ApiKey"},
    )


class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_input: str
    philosophers: list[str] | None = None


def run(
    user_input: str,
    *,
    philosophers: list[str] | None = None,
    memory_backend: object | None = None,
    settings: Settings | None = None,
    tracer: TracePort | None = None,
) -> dict:
    """
    Main entry point for Po_core.

    Programmatic callers should use `run()` / `async_run()`. New HTTP integrations should use `po_core.app.rest.server:create_app`.

    Args:
        user_input: The user's input prompt
        philosophers: Optional allowlist of philosopher IDs.
        memory_backend: Optional external memory backend (None uses default in-process wiring)
        settings: Application settings (None for defaults)

    Returns:
        Result dictionary with request_id, status, and proposal or verdict
    """
    settings = settings or Settings.from_env()

    # Build wired system
    if memory_backend is not None:
        system = build_system(memory=memory_backend, settings=settings)
    else:
        system = build_default_system(settings=settings)

    # Create context
    ctx = Context.now(
        request_id=str(uuid.uuid4()),
        user_input=user_input,
        meta={"entry": "app.api"},
    )

    # Build dependencies for run_turn
    registry: PhilosopherRegistry | AllowlistRegistry = (
        AllowlistRegistry(system.registry, philosophers)
        if philosophers is not None
        else system.registry
    )

    deps = EnsembleDeps(
        memory_read=system.memory_read,
        memory_write=system.memory_write,
        tracer=tracer if tracer is not None else system.tracer,
        tensors=system.tensor_engine,
        solarwill=system.solarwill,
        gate=system.gate,
        philosophers=system.philosophers,  # Backward compat
        aggregator=system.aggregator,
        aggregator_shadow=system.aggregator_shadow,  # Shadow Pareto A/B
        registry=registry,  # SafetyMode-based selection (+ optional allowlist)
        settings=system.settings,  # Worker/timeout config
        shadow_guard=system.shadow_guard,  # ShadowGuard (自律ブレーキ)
        deliberation_engine=getattr(system, "deliberation_engine", None),
    )

    # Run the full pipeline
    return run_turn(ctx, deps)


async def async_run(
    user_input: str,
    *,
    philosophers: list[str] | None = None,
    memory_backend: object | None = None,
    settings: Settings | None = None,
    tracer: TracePort | None = None,
) -> dict:
    """
    Async entry point for Po_core — mirrors ``run()`` but uses
    ``async_run_turn`` so the FastAPI event loop is freed during philosopher
    execution (step 6).

    Suitable for use inside ``async def`` endpoints and SSE generators.

    Args:
        user_input: The user's input prompt
        philosophers: Optional allowlist of philosopher IDs.
        memory_backend: Optional external memory backend (None uses default in-process wiring)
        settings: Application settings (None for defaults)
        tracer: Optional tracer; a default in-memory tracer is used if omitted

    Returns:
        Result dictionary with request_id, status, and proposal or verdict
    """
    settings = settings or Settings.from_env()

    if memory_backend is not None:
        system = build_system(memory=memory_backend, settings=settings)
    else:
        system = build_default_system(settings=settings)

    ctx = Context.now(
        request_id=str(uuid.uuid4()),
        user_input=user_input,
        meta={"entry": "app.api.async"},
    )

    registry: PhilosopherRegistry | AllowlistRegistry = (
        AllowlistRegistry(system.registry, philosophers)
        if philosophers is not None
        else system.registry
    )

    deps = EnsembleDeps(
        memory_read=system.memory_read,
        memory_write=system.memory_write,
        tracer=tracer if tracer is not None else system.tracer,
        tensors=system.tensor_engine,
        solarwill=system.solarwill,
        gate=system.gate,
        philosophers=system.philosophers,
        aggregator=system.aggregator,
        aggregator_shadow=system.aggregator_shadow,
        registry=registry,
        settings=system.settings,
        shadow_guard=system.shadow_guard,
        deliberation_engine=getattr(system, "deliberation_engine", None),
    )

    return await async_run_turn(ctx, deps)


_legacy_api_settings = APISettings()

# ---------------------------------------------------------------------------
# DEPRECATED legacy FastAPI surface.
#
# This ``app`` object and the ``/generate`` endpoint are retained ONLY for
# backward-compatibility.  New deployments MUST use:
#   po_core.app.rest.server:create_app
#
# The legacy surface will be removed in a future release (planned: v2.0.0).
# See docs/legacy/api_migration.md for migration instructions.
# ---------------------------------------------------------------------------
warnings.warn(
    "po_core.app.api.app (the legacy FastAPI surface with /generate) is deprecated. "
    "Use po_core.app.rest.server:create_app instead. "
    "This surface will be removed in v2.0.0.",
    DeprecationWarning,
    stacklevel=1,
)

app = FastAPI(
    title="Po_core Legacy Compatibility API [DEPRECATED]",
    description=(
        "**DEPRECATED** — Use `po_core.app.rest.server:create_app` for new deployments. "
        "This surface will be removed in v2.0.0."
    ),
    deprecated=True,
)

_cors_origins = parse_cors_origins(_legacy_api_settings.cors_origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=_cors_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_DEPRECATION_HEADER = (
    "POST /generate is deprecated. Use POST /v1/reason via po_core.app.rest."
)


@app.post(
    "/generate",
    deprecated=True,
    summary="[DEPRECATED] Generate philosophical response",
    description=(
        "**DEPRECATED** — Use `POST /v1/reason` on the canonical REST server instead. "
        "This endpoint will be removed in v2.0.0."
    ),
)
async def generate(
    payload: GenerateRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> Response:
    _ensure_api_key(
        settings=_legacy_api_settings,
        x_api_key=x_api_key,
        authorization=authorization,
    )
    try:
        result = await async_run(payload.user_input, philosophers=payload.philosophers)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    import json

    return Response(
        content=json.dumps(result),
        media_type="application/json",
        headers={"Deprecation": "true", "Sunset": "v2.0.0", "Link": _DEPRECATION_HEADER},
    )


__all__ = ["run", "async_run", "app"]
