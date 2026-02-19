"""
POST /v1/reason          — Synchronous reasoning
POST /v1/reason/stream   — Streaming reasoning via SSE
"""

from __future__ import annotations

import asyncio
import functools
import json
import time
import uuid
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from po_core.app.api import run as po_run
from po_core.app.rest.auth import require_api_key
from po_core.app.rest.models import (
    PhilosopherContribution,
    ReasonRequest,
    ReasonResponse,
    TensorSnapshot,
)
from po_core.app.rest.rate_limit import limiter
from po_core.app.rest.store import save_trace
from po_core.runtime.settings import Settings
from po_core.trace.in_memory import InMemoryTracer

router = APIRouter(tags=["reason"])


def _reason_limit() -> str:
    """Return the SlowAPI limit string derived from the current APISettings.

    SlowAPI 0.1.x callable limits are invoked with no arguments (or with the
    remote key when the parameter is named ``key``).  Using a zero-arg callable
    that reads from ``get_api_settings()`` — the singleton that
    ``create_app(settings=...)`` updates via ``set_api_settings`` — ensures
    that .env configuration and test overrides are honoured instead of a value
    frozen in ``os.environ`` at import time.
    """
    from po_core.app.rest.config import get_api_settings

    rpm: int = get_api_settings().rate_limit_per_minute
    return f"{rpm}/minute"


# Internal run() returns "ok" on success; map to the published API contract.
_STATUS_MAP: dict[str, str] = {
    "ok": "approved",
    "blocked": "blocked",
    "fallback": "fallback",
}


def _normalize_status(raw: str) -> str:
    """Map internal run() status values to the documented API contract."""
    return _STATUS_MAP.get(raw, "approved")


def _build_po_settings(api_settings: Any) -> Settings:
    """Map API settings to core Settings."""
    return Settings(
        enable_solarwill=api_settings.enable_solarwill,
        enable_intention_gate=api_settings.enable_intention_gate,
        enable_action_gate=api_settings.enable_action_gate,
    )


def _extract_response_text(result: dict) -> str:
    """Extract a human-readable response string from run() result."""
    if "proposal" in result and result["proposal"]:
        proposal = result["proposal"]
        if isinstance(proposal, dict):
            return str(proposal.get("content") or str(proposal))
        return str(proposal)
    if "verdict" in result and result["verdict"]:
        verdict = result["verdict"]
        if isinstance(verdict, dict):
            return str(verdict.get("reason") or str(verdict))
        return str(verdict)
    return str(result.get("status") or "No response generated.")


def _extract_philosophers(result: dict) -> list[PhilosopherContribution]:
    """Extract philosopher contributions from result."""
    contribs: list[PhilosopherContribution] = []
    proposals = result.get("proposals", [])
    if not proposals:
        return contribs
    for p in proposals[:5]:  # top 5
        if isinstance(p, dict):
            name: str = str(p.get("philosopher_id") or p.get("name") or "unknown")
            weight_raw = (
                p.get("weight") if p.get("weight") is not None else p.get("score", 0.0)
            )
            contribs.append(
                PhilosopherContribution(
                    name=name,
                    proposal=str(p.get("content") or p.get("proposal") or ""),
                    weight=float(weight_raw if weight_raw is not None else 0.0),
                )
            )
    return contribs


def _extract_tensors(result: dict) -> TensorSnapshot:
    """Extract tensor metrics from result."""
    tensors = result.get("tensors", {}) or {}
    return TensorSnapshot(
        freedom_pressure=tensors.get("freedom_pressure"),
        semantic_delta=tensors.get("semantic_delta"),
        blocked_tensor=tensors.get("blocked_tensor"),
    )


def _run_reasoning(
    request: ReasonRequest, api_settings: Any
) -> tuple[str, dict, InMemoryTracer]:
    """Execute po_core reasoning and return (session_id, result, tracer)."""
    session_id = request.session_id or str(uuid.uuid4())
    tracer = InMemoryTracer()
    po_settings = _build_po_settings(api_settings)
    result = po_run(
        user_input=request.input,
        settings=po_settings,
        tracer=tracer,
    )
    return session_id, result, tracer


@router.post(
    "/v1/reason",
    response_model=ReasonResponse,
    summary="Synchronous philosophical reasoning",
    description=(
        "Submit a prompt for philosophical deliberation. "
        "The 39-philosopher ensemble deliberates, passes through the "
        "W_Ethics Gate, and returns a synthesised response. "
        "Blocks until the full pipeline completes."
    ),
    responses={
        200: {"description": "Successful reasoning response"},
        401: {"description": "Invalid or missing API key"},
        422: {"description": "Validation error in request body"},
        429: {"description": "Rate limit exceeded"},
    },
)
@limiter.limit(_reason_limit)
async def reason(
    body: ReasonRequest,
    request: Request,
    _: None = Depends(require_api_key),
) -> ReasonResponse:
    """Synchronous reasoning endpoint (non-blocking: offloaded to thread pool)."""
    from po_core.app.rest.config import get_api_settings

    api_settings = get_api_settings()
    t0 = time.perf_counter()

    loop = asyncio.get_running_loop()
    session_id, result, tracer = await loop.run_in_executor(
        None, functools.partial(_run_reasoning, body, api_settings)
    )

    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    # Persist trace
    save_trace(session_id, list(tracer.events))

    return ReasonResponse(
        request_id=result.get("request_id", str(uuid.uuid4())),
        session_id=session_id,
        status=_normalize_status(str(result.get("status") or "")),
        response=_extract_response_text(result),
        philosophers=_extract_philosophers(result),
        tensors=_extract_tensors(result),
        safety_mode=str(result.get("safety_mode", "NORMAL")),
        processing_time_ms=round(elapsed_ms, 2),
        created_at=datetime.now(timezone.utc),
    )


async def _sse_generator(
    body: ReasonRequest, api_settings: Any
) -> AsyncGenerator[str, None]:
    """Async generator yielding SSE-formatted event strings."""

    def _fmt(event_type: str, payload: Dict[str, Any]) -> str:
        data = json.dumps({"chunk_type": event_type, "payload": payload})
        return f"data: {data}\n\n"

    try:
        yield _fmt("started", {"session_id": body.session_id or "pending"})

        tracer = InMemoryTracer()
        collected: list = []

        def _on_event(event: Any) -> None:
            collected.append(event)

        tracer.add_listener(_on_event)

        t0 = time.perf_counter()
        po_settings = _build_po_settings(api_settings)
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None,
            functools.partial(
                po_run, user_input=body.input, settings=po_settings, tracer=tracer
            ),
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        session_id = body.session_id or str(uuid.uuid4())
        save_trace(session_id, list(tracer.events))

        # Emit collected trace events
        for ev in collected:
            yield _fmt(
                "event",
                {
                    "event_type": ev.event_type,
                    "occurred_at": ev.occurred_at.isoformat(),
                    "payload": dict(ev.payload),
                },
            )

        # Final result chunk
        yield _fmt(
            "result",
            {
                "request_id": result.get("request_id", str(uuid.uuid4())),
                "session_id": session_id,
                "status": _normalize_status(str(result.get("status") or "")),
                "response": _extract_response_text(result),
                "safety_mode": str(result.get("safety_mode", "NORMAL")),
                "processing_time_ms": round(elapsed_ms, 2),
            },
        )
        yield _fmt("done", {})

    except Exception as exc:
        yield _fmt("error", {"message": str(exc)})


@router.post(
    "/v1/reason/stream",
    summary="Streaming philosophical reasoning (SSE)",
    description=(
        "Submit a prompt for philosophical deliberation. "
        "Returns a text/event-stream (SSE) response that emits trace events "
        "in real-time as the pipeline executes, followed by a final 'result' "
        "chunk and a 'done' sentinel. "
        "Connect with EventSource or any SSE-capable client."
    ),
    responses={
        200: {
            "content": {"text/event-stream": {}},
            "description": "SSE stream of reasoning events",
        },
        401: {"description": "Invalid or missing API key"},
        429: {"description": "Rate limit exceeded"},
    },
)
@limiter.limit(_reason_limit)
async def reason_stream(
    body: ReasonRequest,
    request: Request,
    _: None = Depends(require_api_key),
) -> StreamingResponse:
    """Streaming reasoning endpoint (SSE)."""
    from po_core.app.rest.config import get_api_settings

    api_settings = get_api_settings()
    return StreamingResponse(
        _sse_generator(body, api_settings),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
