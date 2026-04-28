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

import datetime as dt
import hashlib
import json
import os
import uuid
import warnings

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from po_core.app.rest.auth import evaluate_auth_policy, extract_api_key_from_header_map
from po_core.app.rest.config import APISettings, parse_cors_origins
from po_core.domain.case_signals import CaseSignals, from_case_dict
from po_core.domain.context import Context
from po_core.ensemble import EnsembleDeps, async_run_turn, run_turn
from po_core.philosophers.allowlist import AllowlistRegistry
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.ports.trace import TracePort
from po_core.runtime.settings import Settings
from po_core.runtime.wiring import build_default_system, build_system


def _resolve_presented_key(settings: APISettings, request: Request) -> str | None:
    key = extract_api_key_from_header_map(
        request.headers, configured_header_name=settings.api_key_header
    )
    if key:
        return key
    auth = request.headers.get("Authorization") or request.headers.get("authorization")
    if auth:
        scheme, _, token = auth.partition(" ")
        if scheme.lower() == "bearer" and token.strip():
            return token.strip()
    return None


def _ensure_api_key(settings: APISettings, request: Request) -> None:
    decision = evaluate_auth_policy(
        skip_auth=settings.skip_auth,
        configured_api_key=settings.api_key,
        presented_api_key=_resolve_presented_key(settings, request),
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
    case_signals: CaseSignals | None = None,
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
    return run_turn(ctx, deps, case_signals=case_signals)


async def async_run(
    user_input: str,
    *,
    case_signals: CaseSignals | None = None,
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

    return await async_run_turn(ctx, deps, case_signals=case_signals)


# ── run_case / async_run_case ─────────────────────────────────────────────────


def _case_metadata(
    case: dict, seed: int, now: str | None
) -> tuple[str, str, str]:
    """Return (now_str, run_id, input_digest) for run_case variants."""
    if now is not None:
        now_str = now
    else:
        case_now = case.get("now")
        now_str = (
            case_now.strip()
            if isinstance(case_now, str) and case_now.strip()
            else dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        )
    case_id = str(case.get("case_id", "case_unknown"))
    run_id = str(
        uuid.UUID(
            int=int(hashlib.sha256(f"{case_id}:{seed}".encode()).hexdigest(), 16)
            % (2**128)
        )
    )
    input_digest = hashlib.sha256(
        json.dumps(case, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    return now_str, run_id, input_digest


def run_case(
    case: dict,
    *,
    settings: Settings | None = None,
    philosophers: list[str] | None = None,
    memory_backend: object | None = None,
    tracer: TracePort | None = None,
    seed: int = 42,
    now: str | None = None,
) -> dict:
    """Run the deliberation pipeline for a structured case dict.

    Returns a dict conforming to output_schema_v1.json, closing RT-GAP-004.
    ``run(user_input: str)`` is unchanged for plain-text callers.

    Args:
        case: Structured case dict (title, problem, values, constraints, …).
              See docs/spec/input_schema_v1.json.
        settings: Optional Settings override; falls back to env defaults.
        philosophers: Optional allowlist of philosopher IDs.
        memory_backend: Optional external memory backend.
        tracer: Optional trace collector.
        seed: Seed for deterministic run_id derivation (default 42).
        now: ISO-8601 UTC timestamp override for trace timestamps.

    Returns:
        Dict conforming to output_schema_v1.json.
    """
    from po_core.app.output_adapter import adapt_to_schema, build_user_input

    now_str, run_id, input_digest = _case_metadata(case, seed, now)
    user_input = build_user_input(case)
    signals = from_case_dict(case)

    run_result = run(
        user_input,
        case_signals=signals,
        settings=settings,
        philosophers=philosophers,
        memory_backend=memory_backend,
        tracer=tracer,
    )

    return adapt_to_schema(
        case,
        run_result,
        run_id=run_id,
        digest=input_digest,
        now=now_str,
        seed=seed,
        deterministic=True,
    )


async def async_run_case(
    case: dict,
    *,
    settings: Settings | None = None,
    philosophers: list[str] | None = None,
    memory_backend: object | None = None,
    tracer: TracePort | None = None,
    seed: int = 42,
    now: str | None = None,
) -> dict:
    """Async variant of ``run_case()`` — delegates to ``async_run()``."""
    from po_core.app.output_adapter import adapt_to_schema, build_user_input

    now_str, run_id, input_digest = _case_metadata(case, seed, now)
    user_input = build_user_input(case)
    signals = from_case_dict(case)

    run_result = await async_run(
        user_input,
        case_signals=signals,
        settings=settings,
        philosophers=philosophers,
        memory_backend=memory_backend,
        tracer=tracer,
    )

    return adapt_to_schema(
        case,
        run_result,
        run_id=run_id,
        digest=input_digest,
        now=now_str,
        seed=seed,
        deterministic=True,
    )


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


def _legacy_generate_disabled() -> bool:
    """Return True when the deployment has explicitly disabled /generate.

    The legacy endpoint remains reachable by default as an explicit
    backward-compatibility shim for existing clients.  Deployments that want
    to ensure /generate is gone (for example, because they have already
    migrated to ``po_core.app.rest``) can set
    ``PO_DISABLE_LEGACY_GENERATE=true`` — the route will then return HTTP
    410 Gone.  The switch itself is temporary; /generate will be removed
    outright in v2.0.0.
    """
    flag = os.getenv("PO_DISABLE_LEGACY_GENERATE", "false").strip().lower()
    return flag in {"1", "true", "yes", "on"}


@app.post(
    "/generate",
    deprecated=True,
    summary="[DEPRECATED] Generate philosophical response",
    description=(
        "**DEPRECATED** — Use `POST /v1/reason` on the canonical REST server instead. "
        "Explicit compat shim; set `PO_DISABLE_LEGACY_GENERATE=true` to return "
        "HTTP 410 Gone for new deployments.  The route will be removed in v2.0.0."
    ),
)
async def generate(
    payload: GenerateRequest,
    request: Request,
) -> Response:
    if _legacy_generate_disabled():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=(
                "POST /generate is disabled by this deployment.  Migrate to "
                "POST /v1/reason via po_core.app.rest.server:create_app.  "
                "The route will be removed outright in v2.0.0."
            ),
            headers={
                "Deprecation": "true",
                "Sunset": "v2.0.0",
                "Link": _DEPRECATION_HEADER,
            },
        )

    _ensure_api_key(_legacy_api_settings, request)
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


__all__ = ["run", "async_run", "run_case", "async_run_case", "app"]
