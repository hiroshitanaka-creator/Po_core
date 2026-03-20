"""
POST /v1/reason          — Synchronous reasoning
POST /v1/reason/stream   — Streaming reasoning via SSE
"""

from __future__ import annotations

import asyncio
import functools
import json
import logging
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict, TypedDict

from fastapi import APIRouter, Depends, HTTPException, Request, WebSocket
from fastapi.exceptions import WebSocketException
from fastapi.responses import StreamingResponse

from po_core.app.api import async_run as po_async_run
from po_core.app.api import run as po_run
from po_core.app.rest.auth import (
    evaluate_auth_policy,
    extract_api_key_from_header_map,
    require_api_key,
)
from po_core.app.rest.config import APISettings, get_api_settings, is_rate_limit_enabled
from po_core.app.rest.models import (
    PhilosopherContribution,
    ReasonRequest,
    ReasonResponse,
    TensorSnapshot,
)
from po_core.app.rest.rate_limit import _extract_forwarded_ip, limiter
from po_core.app.rest.review_store import enqueue_review
from po_core.app.rest.store import save_trace
from po_core.runtime.settings import APISettingsLike, Settings
from po_core.trace.in_memory import InMemoryTracer

logger = logging.getLogger(__name__)

router = APIRouter(tags=["reason"])

# Best-effort in-memory limiter for WebSocket handshake requests.
# Uses monotonic timestamps to avoid wall-clock jumps.
_WS_WINDOW_SECONDS = 60.0
_WS_LOG_RETENTION_SECONDS = _WS_WINDOW_SECONDS * 2
_ws_rate_log: dict[str, deque[float]] = defaultdict(deque)


def _client_host(client: Any) -> str:
    """Return a stable client host string for HTTP/WS connections."""
    host = getattr(client, "host", None)
    if isinstance(host, str) and host:
        return host
    return "unknown"


def _client_ip_from_headers(headers: Any, settings: APISettings, client: Any) -> str:
    """Resolve the effective client IP, trusting X-Forwarded-For only when enabled."""
    if settings.trust_proxy_headers:
        forwarded_ip = _extract_forwarded_ip(headers)
        if forwarded_ip:
            return forwarded_ip
    return _client_host(client)


def _prune_ws_rate_log(now: float) -> None:
    """Drop stale or empty WS limiter buckets to cap memory growth."""
    stale_keys = [
        client_ip
        for client_ip, timestamps in _ws_rate_log.items()
        if not timestamps or now - timestamps[-1] > _WS_LOG_RETENTION_SECONDS
    ]
    for client_ip in stale_keys:
        _ws_rate_log.pop(client_ip, None)


def _sanitized_stream_error_payload() -> dict[str, str]:
    """Return the stable client-facing streaming error payload."""
    return {"code": "internal_error", "message": "internal server error"}


def _reason_limit() -> str:
    """Return the SlowAPI limit string derived from the current APISettings.

    SlowAPI 0.1.x callable limits are invoked with no arguments (or with the
    remote key when the parameter is named ``key``).  Using a zero-arg callable
    that reads from ``get_api_settings()`` — the singleton that
    ``create_app(settings=...)`` updates via ``set_api_settings`` — ensures
    that .env configuration and test overrides are honoured instead of a value
    frozen in ``os.environ`` at import time.
    """
    rpm: int = get_api_settings().rate_limit_per_minute
    return f"{rpm}/minute"


def _http_rate_limit_exempt() -> bool:
    """Return True when HTTP rate limiting is disabled by configuration."""
    return not is_rate_limit_enabled(get_api_settings().rate_limit_per_minute)


def _resolve_ws_auth_key(
    websocket: WebSocket, *, allow_query_api_key: bool
) -> str | None:
    """Resolve API key for WebSocket handshake.

    By default, the configured API-key header is accepted, with ``X-API-Key``
    retained as a backwards-compatible alias unless it is already configured.
    Query-string secrets are still rejected by default because they are easier
    to leak via logs/history/referers.

    If ``allow_query_api_key`` is explicitly enabled, ``?api_key=...`` is accepted
    as a browser-compatibility fallback for environments that cannot set custom
    WebSocket headers.
    """
    header_key = extract_api_key_from_header_map(
        websocket.headers,
        configured_header_name=get_api_settings().api_key_header,
    )
    if header_key:
        return header_key
    if allow_query_api_key:
        return (
            str(websocket.query_params["api_key"])
            if "api_key" in websocket.query_params
            else None
        )
    return None


def _is_ws_rate_limited(websocket: WebSocket, rpm: int, settings: APISettings) -> bool:
    """Return True when the client exceeded the per-minute WS request budget."""
    if not is_rate_limit_enabled(rpm):
        return False

    now = time.monotonic()
    _prune_ws_rate_log(now)

    client_ip = _client_ip_from_headers(websocket.headers, settings, websocket.client)
    timestamps = _ws_rate_log[client_ip]
    while timestamps and now - timestamps[0] > _WS_WINDOW_SECONDS:
        timestamps.popleft()
    if not timestamps:
        _ws_rate_log.pop(client_ip, None)
        timestamps = _ws_rate_log[client_ip]
    if len(timestamps) >= rpm:
        return True
    timestamps.append(now)
    return False


# Internal run() returns "ok" on success; map to the published API contract.
_STATUS_MAP: dict[str, str] = {
    "ok": "approved",
    "approved": "approved",
    "blocked": "blocked",
    "fallback": "fallback",
}


class _FinalizedReasonPayload(TypedDict):
    request_id: str
    session_id: str
    status: str
    response: str
    safety_mode: str
    processing_time_ms: float
    philosophers: list[dict[str, Any]]
    tensors: dict[str, Any]
    degraded: bool
    llm_fallback: bool
    fallback_reasons: list[str]


def _normalize_status(raw: str) -> str:
    """Map internal run() status values to the documented API contract."""
    normalized = _STATUS_MAP.get(raw)
    if normalized is not None:
        return normalized

    logger.warning(
        "Unknown internal status received from reasoning engine",
        extra={"raw_status": raw},
    )
    return "fallback"


def _build_po_settings(api_settings: APISettingsLike) -> Settings:
    """Map API settings to core Settings."""
    return Settings.from_api_settings(api_settings)


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
    """Extract philosopher contributions and LLM routing metadata from result."""
    contribs: list[PhilosopherContribution] = []
    proposals = result.get("proposals", [])
    if not proposals:
        return contribs

    for p in proposals[:5]:  # top 5
        if not isinstance(p, dict):
            continue

        name: str = str(p.get("philosopher_id") or p.get("name") or "unknown")
        weight_raw = (
            p.get("weight") if p.get("weight") is not None else p.get("score", 0.0)
        )

        normalized = p.get("normalized_response")
        normalized_dict = normalized if isinstance(normalized, dict) else {}
        normalized_meta = normalized_dict.get("metadata")
        normalized_meta_dict = (
            normalized_meta if isinstance(normalized_meta, dict) else {}
        )

        proposal_meta = p.get("metadata")
        proposal_meta_dict = proposal_meta if isinstance(proposal_meta, dict) else {}

        provider = (
            p.get("llm_provider")
            or normalized_meta_dict.get("llm_provider")
            or proposal_meta_dict.get("llm_provider")
        )
        model = (
            p.get("llm_model")
            or normalized_meta_dict.get("llm_model")
            or proposal_meta_dict.get("llm_model")
        )

        llm_fallback_val = (
            p.get("llm_fallback")
            if p.get("llm_fallback") is not None
            else normalized_meta_dict.get("llm_fallback")
        )
        if llm_fallback_val is None:
            llm_fallback_val = proposal_meta_dict.get("llm_fallback")

        fallback_reason = _extract_fallback_reason(
            normalized_meta_dict,
            proposal_meta_dict,
            proposal=p,
        )

        contribs.append(
            PhilosopherContribution(
                name=name,
                proposal=str(p.get("content") or p.get("proposal") or ""),
                weight=float(weight_raw if weight_raw is not None else 0.0),
                provider=str(provider) if provider not in (None, "") else None,
                model=str(model) if model not in (None, "") else None,
                llm_fallback=(
                    bool(llm_fallback_val) if llm_fallback_val is not None else None
                ),
                fallback_reason=(
                    str(fallback_reason) if fallback_reason not in (None, "") else None
                ),
            )
        )
    return contribs


def _extract_fallback_reason(
    *metadata_dicts: dict[str, Any], proposal: dict[str, Any]
) -> str | None:
    direct_reason = proposal.get("fallback_reason")
    if direct_reason not in (None, ""):
        return str(direct_reason)

    for metadata_dict in metadata_dicts:
        nested = metadata_dict.get("fallback")
        if isinstance(nested, dict):
            nested_reason = nested.get("reason")
            if nested_reason not in (None, ""):
                return str(nested_reason)
        reason = metadata_dict.get("fallback_reason")
        if reason not in (None, ""):
            return str(reason)
    return None


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


def _run_reasoning(
    request: ReasonRequest, api_settings: Any
) -> tuple[str, dict, InMemoryTracer]:
    """Execute po_core reasoning and return (session_id, result, tracer)."""
    session_id = request.session_id or str(uuid.uuid4())
    tracer = InMemoryTracer()
    po_settings = _build_po_settings(api_settings)
    result = po_run(
        user_input=request.input,
        philosophers=request.philosophers,
        settings=po_settings,
        tracer=tracer,
    )
    return session_id, result, tracer


def _persist_and_finalize_result(
    *,
    session_id: str,
    result: dict[str, Any],
    tracer: InMemoryTracer,
    elapsed_ms: float,
    source: str,
) -> _FinalizedReasonPayload:
    """Persist trace/review side effects and build the transport-neutral result payload."""
    save_trace(session_id, list(tracer.events))

    escalated, reason = _detect_escalate(result, tracer)
    request_id = str(result.get("request_id") or session_id)
    if escalated:
        enqueue_review(
            review_id=f"{session_id}:{request_id}",
            session_id=session_id,
            request_id=request_id,
            reason=reason,
            source=source,
        )

    llm_fallback, fallback_reasons = _fallback_summary(result)
    degraded = bool(result.get("degraded", False) or llm_fallback)

    return {
        "request_id": request_id,
        "session_id": session_id,
        "status": _normalize_status(str(result.get("status") or "")),
        "response": _extract_response_text(result),
        "safety_mode": str(result.get("safety_mode", "NORMAL")),
        "processing_time_ms": round(elapsed_ms, 2),
        "philosophers": [p.model_dump() for p in _extract_philosophers(result)],
        "tensors": _extract_tensors(result).model_dump(),
        "degraded": degraded,
        "llm_fallback": llm_fallback,
        "fallback_reasons": fallback_reasons,
    }


async def _cancel_stream_task(task: asyncio.Task[Any] | None) -> None:
    """Cancel and await a streaming worker task, suppressing expected cancellation only."""
    if task is None:
        return
    if not task.done():
        task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        return


def _fallback_summary(result: dict) -> tuple[bool, list[str]]:
    proposals = result.get("proposals", [])
    reasons: set[str] = set()
    llm_fallback = False
    if isinstance(proposals, list):
        for p in proposals:
            if not isinstance(p, dict):
                continue
            normalized = p.get("normalized_response")
            normalized_dict = normalized if isinstance(normalized, dict) else {}
            normalized_meta = normalized_dict.get("metadata")
            normalized_meta_dict = (
                normalized_meta if isinstance(normalized_meta, dict) else {}
            )
            proposal_meta = p.get("metadata")
            proposal_meta_dict = (
                proposal_meta if isinstance(proposal_meta, dict) else {}
            )

            fallback_val = (
                p.get("llm_fallback")
                if p.get("llm_fallback") is not None
                else normalized_meta_dict.get("llm_fallback")
            )
            if fallback_val is None:
                fallback_val = proposal_meta_dict.get("llm_fallback")
            if bool(fallback_val):
                llm_fallback = True

            reason = _extract_fallback_reason(
                normalized_meta_dict,
                proposal_meta_dict,
                proposal=p,
            )
            if reason:
                reasons.add(reason)

    return llm_fallback, sorted(reasons)


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
@limiter.limit(_reason_limit, exempt_when=_http_rate_limit_exempt)
async def reason(
    body: ReasonRequest,
    request: Request,
    _: None = Depends(require_api_key),
) -> ReasonResponse:
    """Synchronous reasoning endpoint (non-blocking: offloaded to thread pool)."""
    api_settings = get_api_settings()
    t0 = time.perf_counter()

    loop = asyncio.get_running_loop()
    try:
        session_id, result, tracer = await asyncio.wait_for(
            loop.run_in_executor(
                None, functools.partial(_run_reasoning, body, api_settings)
            ),
            timeout=api_settings.request_timeout_s,
        )
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504, detail="reasoning request timed out"
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    response_payload = _persist_and_finalize_result(
        session_id=session_id,
        result=result,
        tracer=tracer,
        elapsed_ms=elapsed_ms,
        source="/v1/reason",
    )

    return ReasonResponse(
        request_id=response_payload["request_id"],
        session_id=response_payload["session_id"],
        status=response_payload["status"],
        response=response_payload["response"],
        philosophers=[
            PhilosopherContribution.model_validate(item)
            for item in response_payload["philosophers"]
        ],
        tensors=TensorSnapshot.model_validate(response_payload["tensors"]),
        safety_mode=response_payload["safety_mode"],
        processing_time_ms=response_payload["processing_time_ms"],
        created_at=datetime.now(timezone.utc),
        degraded=response_payload["degraded"],
        llm_fallback=response_payload["llm_fallback"],
        fallback_reasons=response_payload["fallback_reasons"],
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
        async for chunk in _stream_reasoning_chunks(
            body, api_settings, source="/v1/reason/stream"
        ):
            yield _fmt(str(chunk["chunk_type"]), dict(chunk.get("payload") or {}))

    except Exception:
        logger.exception("Unhandled SSE streaming error")
        yield _fmt("error", _sanitized_stream_error_payload())


async def _stream_reasoning_chunks(
    body: ReasonRequest, api_settings: Any, *, source: str
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
            res = await asyncio.wait_for(
                po_async_run(
                    user_input=body.input,
                    philosophers=body.philosophers,
                    settings=po_settings,
                    tracer=tracer,
                ),
                timeout=api_settings.request_timeout_s,
            )
            result_box.append(res)
        except Exception as e:
            exc_box.append(e)
        finally:
            await queue.put(_DONE)

    task: asyncio.Task[Any] | None = asyncio.create_task(_run_and_signal())

    try:
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

        if exc_box:
            if isinstance(exc_box[0], asyncio.TimeoutError):
                yield {
                    "chunk_type": "error",
                    "payload": {
                        "code": "timeout",
                        "message": "reasoning request timed out",
                    },
                }
                return
            logger.exception("Unhandled streaming pipeline error", exc_info=exc_box[0])
            yield {"chunk_type": "error", "payload": _sanitized_stream_error_payload()}
            return

        result = result_box[0]
        response_payload = _persist_and_finalize_result(
            session_id=session_id,
            result=result,
            tracer=tracer,
            elapsed_ms=elapsed_ms,
            source=source,
        )
        yield {"chunk_type": "result", "payload": response_payload}
        yield {"chunk_type": "done", "payload": {}}
    finally:
        await _cancel_stream_task(task)


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
@limiter.limit(_reason_limit, exempt_when=_http_rate_limit_exempt)
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

    api_settings = get_api_settings()

    auth_decision = evaluate_auth_policy(
        skip_auth=api_settings.skip_auth,
        configured_api_key=api_settings.api_key,
        presented_api_key=_resolve_ws_auth_key(
            websocket, allow_query_api_key=api_settings.ws_allow_query_api_key
        ),
    )
    if not auth_decision.allowed:
        await websocket.close(code=1008, reason=auth_decision.message)
        return

    if _is_ws_rate_limited(websocket, api_settings.rate_limit_per_minute, api_settings):
        await websocket.close(code=1008, reason="Rate limit exceeded")
        return

    await websocket.accept()
    try:
        raw_body = await websocket.receive_json()
        body = ReasonRequest.model_validate(raw_body)
    except Exception:
        logger.exception("Invalid WebSocket request payload")
        await websocket.send_json(
            {"chunk_type": "error", "payload": _sanitized_stream_error_payload()}
        )
        await websocket.close(code=1003)
        return

    try:
        async for chunk in _stream_reasoning_chunks(
            body, api_settings, source="/v1/ws/reason"
        ):
            await websocket.send_json(chunk)
            if chunk.get("chunk_type") in {"done", "error"}:
                break
    except WebSocketException:
        return
    except Exception:
        logger.exception("Unhandled WebSocket streaming error")
        await websocket.send_json(
            {"chunk_type": "error", "payload": _sanitized_stream_error_payload()}
        )
    finally:
        await websocket.close()
