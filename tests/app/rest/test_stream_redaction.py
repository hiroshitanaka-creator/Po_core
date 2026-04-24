"""Regression tests: /v1/reason/stream and /v1/ws/reason honour
``redact_trace_responses`` so that PII-shaped values and sensitive keys never
leave the server alongside raw trace payloads. The spec requires SSE,
WebSocket, and GET /v1/trace to share the same redaction behaviour
(per CLAUDE.md + redaction-auth-scope-fixes plan).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.redaction import REDACTED_PLACEHOLDER
from po_core.app.rest.server import create_app
from po_core.domain.trace_event import TraceEvent

SENSITIVE_VALUES = {
    "api_key": "sk-live-abc123-should-not-leak",
    "authorization": "Bearer supersecrettoken-should-not-leak",
    "password": "hunter2-should-not-leak",
    "token": "eyJhbGciOi-should-not-leak",
}
SENSITIVE_FREETEXT = "contact me at alice+pii@example.com or +1-555-123-4567"


def _build_client(tmp_path, *, redact: bool) -> TestClient:
    app = create_app(
        APISettings(
            skip_auth=True,
            api_key="",
            trace_store_backend="sqlite",
            trace_db_path=str(tmp_path / "trace_store.sqlite3"),
            review_store_backend="sqlite",
            review_db_path=str(tmp_path / "review_store.sqlite3"),
            redact_trace_responses=redact,
        )
    )
    return TestClient(app, raise_server_exceptions=True)


def _sensitive_payload() -> dict[str, Any]:
    return {
        **SENSITIVE_VALUES,
        "message": SENSITIVE_FREETEXT,
    }


def _make_async_run_side_effect() -> AsyncMock:
    """Return an AsyncMock that emits a sensitive trace event via the caller's tracer."""

    async def _side_effect(**kwargs: Any) -> dict[str, Any]:
        tracer = kwargs.get("tracer")
        assert tracer is not None, "stream must pass tracer to async_run"
        tracer.emit(
            TraceEvent(
                event_type="SensitiveEvent",
                occurred_at=datetime.now(timezone.utc),
                correlation_id="corr-1",
                payload=_sensitive_payload(),
            )
        )
        return {
            "status": "ok",
            "proposal": {"content": "benign response"},
            "proposals": [],
            "tensors": {},
            "safety_mode": "NORMAL",
            "request_id": "req-1",
        }

    return AsyncMock(side_effect=_side_effect)


def _parse_sse_chunks(raw_text: str) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for line in raw_text.splitlines():
        if line.startswith("data: "):
            chunks.append(json.loads(line[6:]))
    return chunks


def _first_event_chunk(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    for chunk in chunks:
        if chunk["chunk_type"] == "event":
            return chunk
    raise AssertionError("no event chunk found in stream")


def _assert_no_raw_secrets(serialized: str) -> None:
    for raw in SENSITIVE_VALUES.values():
        assert raw not in serialized, f"raw secret leaked into stream: {raw!r}"
    assert "alice+pii@example.com" not in serialized
    assert "555-123-4567" not in serialized


# ---------------------------------------------------------------------------
# SSE
# ---------------------------------------------------------------------------


def test_sse_stream_redacts_sensitive_trace_payload_by_default(tmp_path) -> None:
    client = _build_client(tmp_path, redact=True)

    with patch(
        "po_core.app.rest.routers.reason.po_async_run",
        new=_make_async_run_side_effect(),
    ):
        response = client.post("/v1/reason/stream", json={"input": "trigger"})

    assert response.status_code == 200
    _assert_no_raw_secrets(response.text)

    chunks = _parse_sse_chunks(response.text)
    event_chunk = _first_event_chunk(chunks)
    inner = event_chunk["payload"]["payload"]
    for key in ("api_key", "authorization", "password", "token"):
        assert inner[key] == REDACTED_PLACEHOLDER, (
            f"expected {key} to be redacted, got {inner[key]!r}"
        )
    assert REDACTED_PLACEHOLDER in inner["message"]


def test_sse_stream_leaves_payload_intact_when_redaction_disabled(tmp_path) -> None:
    client = _build_client(tmp_path, redact=False)

    with patch(
        "po_core.app.rest.routers.reason.po_async_run",
        new=_make_async_run_side_effect(),
    ):
        response = client.post("/v1/reason/stream", json={"input": "trigger"})

    assert response.status_code == 200
    chunks = _parse_sse_chunks(response.text)
    event_chunk = _first_event_chunk(chunks)
    inner = event_chunk["payload"]["payload"]
    # When redaction is OFF, the raw payload passes through — this guards
    # against accidentally making redaction unconditional and silently
    # breaking consumers that depend on raw fields.
    assert inner["api_key"] == SENSITIVE_VALUES["api_key"]
    assert inner["authorization"] == SENSITIVE_VALUES["authorization"]


# ---------------------------------------------------------------------------
# WebSocket
# ---------------------------------------------------------------------------


def test_websocket_stream_redacts_sensitive_trace_payload_by_default(tmp_path) -> None:
    client = _build_client(tmp_path, redact=True)

    with patch(
        "po_core.app.rest.routers.reason.po_async_run",
        new=_make_async_run_side_effect(),
    ):
        with client.websocket_connect("/v1/ws/reason") as websocket:
            websocket.send_json({"input": "trigger"})
            chunks: list[dict[str, Any]] = []
            while True:
                chunk = websocket.receive_json()
                chunks.append(chunk)
                if chunk["chunk_type"] in {"done", "error"}:
                    break

    serialized = json.dumps(chunks)
    _assert_no_raw_secrets(serialized)

    event_chunk = _first_event_chunk(chunks)
    inner = event_chunk["payload"]["payload"]
    for key in ("api_key", "authorization", "password", "token"):
        assert inner[key] == REDACTED_PLACEHOLDER
    assert REDACTED_PLACEHOLDER in inner["message"]
