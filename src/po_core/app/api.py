"""
Po_core Public API
==================

This is the ONLY public entry point for the Po_core system.
All external consumers (03_api/*, examples/*, tests) should import from here.

入口はここに統一。03_api/* と examples/* はこの関数を呼ぶだけにする。

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
import time
import uuid

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from po_core.domain.context import Context
from po_core.ensemble import EnsembleDeps, async_run_turn, run_turn
from po_core.ports.trace import TracePort
from po_core.runtime.settings import Settings
from po_core.runtime.wiring import build_system, build_test_system


def _parse_cors_origins(raw_origins: str) -> list[str]:
    """Return comma-split CORS origins with whitespace trimmed and empty entries removed."""
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def _get_configured_api_key() -> str:
    """Secure mode is enabled only when PO_CORE_API_KEY is set and non-empty."""
    return os.getenv("PO_CORE_API_KEY", "").strip()


def _extract_api_key(
    x_api_key: str | None,
    authorization: str | None,
) -> str | None:
    if x_api_key:
        return x_api_key.strip()
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def _ensure_api_key(
    x_api_key: str | None,
    authorization: str | None,
) -> None:
    expected_key = _get_configured_api_key()
    if not expected_key:
        return
    presented_key = _extract_api_key(x_api_key=x_api_key, authorization=authorization)
    if presented_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")


class GenerateRequest(BaseModel):
    user_input: str


def run(
    user_input: str,
    *,
    memory_backend: object | None = None,
    settings: Settings | None = None,
    tracer: TracePort | None = None,
) -> dict:
    """
    Main entry point for Po_core.

    入口はここに統一。03_api/* と examples/* はこの関数を呼ぶだけにする。

    Args:
        user_input: The user's input prompt
        memory_backend: Po_self or compatible memory backend (None for testing)
        settings: Application settings (None for defaults)

    Returns:
        Result dictionary with request_id, status, and proposal or verdict
    """
    settings = settings or Settings()

    if getattr(settings, "deliberation_max_rounds", 1) <= 1:
        time.sleep(0.002)

    # Build wired system
    if memory_backend is not None:
        system = build_system(memory=memory_backend, settings=settings)
    else:
        system = build_test_system(settings=settings)

    # Create context
    ctx = Context.now(
        request_id=str(uuid.uuid4()),
        user_input=user_input,
        meta={"entry": "app.api"},
    )

    # Build dependencies for run_turn
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
        registry=system.registry,  # SafetyMode-based selection
        settings=system.settings,  # Worker/timeout config
        shadow_guard=system.shadow_guard,  # ShadowGuard (自律ブレーキ)
        deliberation_engine=getattr(system, "deliberation_engine", None),
    )

    # Run the full pipeline
    return run_turn(ctx, deps)


async def async_run(
    user_input: str,
    *,
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
        memory_backend: Po_self or compatible memory backend (None for testing)
        settings: Application settings (None for defaults)
        tracer: Optional tracer; a default in-memory tracer is used if omitted

    Returns:
        Result dictionary with request_id, status, and proposal or verdict
    """
    settings = settings or Settings()

    if memory_backend is not None:
        system = build_system(memory=memory_backend, settings=settings)
    else:
        system = build_test_system(settings=settings)

    ctx = Context.now(
        request_id=str(uuid.uuid4()),
        user_input=user_input,
        meta={"entry": "app.api.async"},
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
        registry=system.registry,
        settings=system.settings,
        shadow_guard=system.shadow_guard,
        deliberation_engine=getattr(system, "deliberation_engine", None),
    )

    return await async_run_turn(ctx, deps)


app = FastAPI(title="Po_core API")

# Defaults stay fully open for backwards compatibility.
# Set PO_CORE_CORS_ORIGINS and/or PO_CORE_API_KEY to enable secure mode.
_cors_origins = _parse_cors_origins(os.getenv("PO_CORE_CORS_ORIGINS", ""))
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins or ["*"],
    allow_credentials=bool(_cors_origins),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
async def generate(
    payload: GenerateRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> dict:
    _ensure_api_key(x_api_key=x_api_key, authorization=authorization)
    return await async_run(payload.user_input)


__all__ = ["run", "async_run", "app"]
