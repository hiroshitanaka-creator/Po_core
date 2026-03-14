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

from fastapi import APIRouter, Depends, Request, WebSocket
from fastapi.exceptions import WebSocketException
from fastapi.responses import StreamingResponse

from po_core.app.api import async_run as po_async_run
from po_core.app.api import run as po_run
from po_core.app.rest.auth import require_api_key
from po_core.app.rest.models import (
    PhilosopherContribution,
    ReasonRequest,
    ReasonResponse,
    TensorSnapshot,
)
from po_core.app.rest.rate_limit import limiter
from po_core.app.rest.review_store import enqueue_review
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
        philosophers_max_normal=api_settings.philosophers_max_normal,
        philosophers_max_warn=api_settings.philosophers_max_warn,
        philosophers_max_critical=api_settings.philosophers_max_critical,
        philosopher_cost_budget_normal=api_settings.philosopher_cost_budget_normal,
        philosopher_cost_budget_warn=api_settings.philosopher_cost_budget_warn,
        philosopher_cost_budget_critical=api_settings.philosopher_cost_budget_critical,
        enable_llm_philosophers=api_settings.enable_llm_philosophers,
        llm_provider=api_settings.llm_provider,
        llm_model=api_settings.llm_model,
        llm_timeout_s=api_settings.llm_timeout_s,
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


def _detect_escalate(result: dict, tracer: InMemoryTracer) -> tuple[bool, str]:
    """Return (is_escalated, reason) derived from result and trace events."""
    verdict = result.get("verdict")
    if isinstance(verdict, dict):
        decision = str(verdict.get("decision") or "").lower()
        if decision == "escalate":
            return True, "verdict.decision=escalate"

    for event in tracer.events:
        payload = dict(event.payload)
        if event.event_type == "DecisionEmitted":
            gate = payload.get("gate")
            gate_dict = dict(gate) if isinstance(gate, dict) else {}
            if str(gate_dict.get("decision") or "").lower() == "escalate":
                return True, "DecisionEmitted.gate.decision=escalate"
        if event.event_type == "ExplanationEmitted":
            if str(payload.get("decision") or "").lower() == "escalate":
                return True, "ExplanationEmitted.decision=escalate"

    return False, ""


def _enqueue_escalated_review(
    session_id: str, result: dict, tracer: InMemoryTracer
) -> None:
    """Queue human review item when an ESCALATE decision is observed."""
    escalated, reason = _detect_escalate(result, tracer)
    if not escalated:
        return

    request_id = str(result.get("request_id") or session_id)
    review_id = f"{session_id}:{request_id}"
    enqueue_review(
        review_id=review_id,
        session_id=session_id,
        request_id=request_id,
        reason=reason,
        source="/v1/reason",
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
        "A configurable philosopher ensemble (up to 42) deliberates, passes through the "
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
    _enqueue_escalated_review(session_id, result, tracer)

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
    """
    Async generator yielding SSE-formatted event strings in real-time.

    Architecture:
    - ``async_run_turn`` (via ``po_async_run``) executes the pipeline in the
      event loop, using ``async_run_philosophers`` for step 6.
    - Each ``tracer.emit()`` call triggers a listener that puts the event into
      an ``asyncio.Queue`` immediately, so SSE chunks arrive at the client as
      each pipeline step (and each philosopher) completes.
    - A sentinel object signals queue drain completion after the pipeline exits.

    This replaces the old threadpool-batch approach where all events were
    collected and emitted only after the full pipeline finished.
    """

    def _fmt(event_type: str, payload: Dict[str, Any]) -> str:
        data = json.dumps({"chunk_type": event_type, "payload": payload})
        return f"data: {data}\n\n"

    try:
        async for chunk in _stream_reasoning_chunks(body, api_settings):
            yield _fmt(str(chunk["chunk_type"]), dict(chunk.get("payload") or {}))

    except Exception as exc:
        yield _fmt("error", {"message": str(exc)})


async def _stream_reasoning_chunks(
    body: ReasonRequest, api_settings: Any
) -> AsyncGenerator[Dict[str, Any], None]:
    """Shared real-time chunk stream for SSE and WebSocket transports."""
    session_id = body.session_id or str(uuid.uuid4())
    yield {"chunk_type": "started", "payload": {"session_id": session_id}}

    queue: asyncio.Queue = asyncio.Queue()
    _DONE = object()
    tracer = InMemoryTracer()

    def _on_event(event: Any) -> None:
        queue.put_nowait(event)

    tracer.add_listener(_on_event)
    po_settings = _build_po_settings(api_settings)
    t0 = time.perf_counter()

    result_box: list = []
    exc_box: list = []

    async def _run_and_signal() -> None:
        try:
            res = await po_async_run(
                user_input=body.input,
                settings=po_settings,
                tracer=tracer,
            )
            result_box.append(res)
        except Exception as e:
            exc_box.append(e)
        finally:
            await queue.put(_DONE)

    asyncio.create_task(_run_and_signal())

    while True:
        item = await queue.get()
        if item is _DONE:
            break
        yield {
            "chunk_type": "event",
            "payload": {
                "event_type": item.event_type,
                "occurred_at": item.occurred_at.isoformat(),
                "payload": dict(item.payload),
            },
        }

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    save_trace(session_id, list(tracer.events))

    if exc_box:
        yield {"chunk_type": "error", "payload": {"message": str(exc_box[0])}}
        return

    result = result_box[0]
    yield {
        "chunk_type": "result",
        "payload": {
            "request_id": result.get("request_id", str(uuid.uuid4())),
            "session_id": session_id,
            "status": _normalize_status(str(result.get("status") or "")),
            "response": _extract_response_text(result),
            "safety_mode": str(result.get("safety_mode", "NORMAL")),
            "processing_time_ms": round(elapsed_ms, 2),
            "philosophers": [p.model_dump() for p in _extract_philosophers(result)],
            "tensors": _extract_tensors(result).model_dump(),
        },
    }
    yield {"chunk_type": "done", "payload": {}}


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


@router.websocket("/v1/ws/reason")
async def reason_ws(websocket: WebSocket) -> None:
    """WebSocket reasoning stream: client sends one ReasonRequest JSON payload."""
    from po_core.app.rest.config import get_api_settings

    await websocket.accept()
    try:
        raw_body = await websocket.receive_json()
        body = ReasonRequest.model_validate(raw_body)
    except Exception as exc:
        await websocket.send_json(
            {"chunk_type": "error", "payload": {"message": str(exc)}}
        )
        await websocket.close(code=1003)
        return

    api_settings = get_api_settings()

    try:
        async for chunk in _stream_reasoning_chunks(body, api_settings):
            await websocket.send_json(chunk)
            if chunk.get("chunk_type") in {"done", "error"}:
                break
    except WebSocketException:
        return
    except Exception as exc:
        await websocket.send_json(
            {"chunk_type": "error", "payload": {"message": str(exc)}}
        )
    finally:
        await websocket.close()
