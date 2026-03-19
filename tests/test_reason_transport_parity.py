from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.server import create_app
from po_core.domain.trace_event import TraceEvent


@pytest.fixture()
def client(tmp_path) -> TestClient:
    app = create_app(
        APISettings(
            skip_auth=True,
            api_key="",
            trace_store_backend="sqlite",
            trace_db_path=str(tmp_path / "trace_store.sqlite3"),
            review_store_backend="sqlite",
            review_db_path=str(tmp_path / "review_store.sqlite3"),
        )
    )
    from po_core.app.rest import auth

    app.dependency_overrides[auth.require_api_key] = lambda: None
    return TestClient(app, raise_server_exceptions=True)


ESCALATE_RESULT: dict[str, Any] = {
    "request_id": "req-escalate-001",
    "status": "ok",
    "verdict": {"decision": "escalate", "reason": "need human review"},
    "proposal": {"content": "Escalate to operator."},
    "proposals": [],
    "tensors": {},
    "safety_mode": "WARN",
}

UNKNOWN_STATUS_RESULT: dict[str, Any] = {
    "request_id": "req-unknown-001",
    "status": "mystery-status",
    "proposal": {"content": "Need safe fallback."},
    "proposals": [],
    "tensors": {},
    "safety_mode": "WARN",
}


def _parse_sse_chunks(raw_text: str) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for line in raw_text.splitlines():
        if line.startswith("data: "):
            chunks.append(json.loads(line[6:]))
    return chunks


def _collect_ws_chunks(client: TestClient, payload: dict[str, Any]) -> list[dict[str, Any]]:
    with client.websocket_connect("/v1/ws/reason") as ws:
        ws.send_json(payload)
        chunks: list[dict[str, Any]] = []
        while True:
            chunk = ws.receive_json()
            chunks.append(chunk)
            if chunk["chunk_type"] in {"done", "error"}:
                break
    return chunks


@pytest.mark.parametrize(
    ("transport", "invoke"),
    [
        (
            "sync",
            lambda client: client.post(
                "/v1/reason",
                json={"input": "Need escalation", "session_id": "session-sync"},
            ).json(),
        ),
        (
            "sse",
            lambda client: next(
                chunk["payload"]
                for chunk in _parse_sse_chunks(
                    client.post(
                        "/v1/reason/stream",
                        json={"input": "Need escalation", "session_id": "session-sse"},
                    ).text
                )
                if chunk["chunk_type"] == "result"
            ),
        ),
        (
            "websocket",
            lambda client: next(
                chunk["payload"]
                for chunk in _collect_ws_chunks(
                    client,
                    {"input": "Need escalation", "session_id": "session-ws"},
                )
                if chunk["chunk_type"] == "result"
            ),
        ),
    ],
)
def test_reason_transports_enqueue_escalations_exactly_once(
    client: TestClient,
    transport: str,
    invoke: Callable[[TestClient], dict[str, Any]],
) -> None:
    async def _fake_async_run(*, user_input, settings, tracer, philosophers=None):
        tracer.emit(
            TraceEvent.now(
                "DecisionEmitted",
                correlation_id=ESCALATE_RESULT["request_id"],
                payload={"gate": {"decision": "escalate"}},
            )
        )
        return dict(ESCALATE_RESULT)

    with (
        patch("po_core.app.rest.routers.reason.po_run", return_value=dict(ESCALATE_RESULT)),
        patch("po_core.app.rest.routers.reason.po_async_run", new=AsyncMock(side_effect=_fake_async_run)),
        patch("po_core.app.rest.routers.reason.enqueue_review") as enqueue_mock,
    ):
        payload = invoke(client)

    assert payload["status"] == "approved"
    assert enqueue_mock.call_count == 1
    kwargs = enqueue_mock.call_args.kwargs
    assert kwargs["session_id"] == payload["session_id"]
    assert kwargs["request_id"] == ESCALATE_RESULT["request_id"]
    assert kwargs["review_id"] == f"{payload['session_id']}:{ESCALATE_RESULT['request_id']}"
    expected_source = {
        "sync": "/v1/reason",
        "sse": "/v1/reason/stream",
        "websocket": "/v1/ws/reason",
    }[transport]
    assert kwargs["source"] == expected_source


@pytest.mark.parametrize("transport", ["sync", "sse", "websocket"])
def test_unknown_internal_status_never_surfaces_as_approved(
    client: TestClient,
    transport: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    async def _fake_async_run(*, user_input, settings, tracer, philosophers=None):
        return dict(UNKNOWN_STATUS_RESULT)

    caplog.set_level("WARNING", logger="po_core.app.rest.routers.reason")
    with (
        patch(
            "po_core.app.rest.routers.reason.po_run",
            return_value=dict(UNKNOWN_STATUS_RESULT),
        ),
        patch(
            "po_core.app.rest.routers.reason.po_async_run",
            new=AsyncMock(side_effect=_fake_async_run),
        ),
    ):
        if transport == "sync":
            payload = client.post(
                "/v1/reason",
                json={"input": "Unknown status", "session_id": "status-sync"},
            ).json()
        elif transport == "sse":
            payload = next(
                chunk["payload"]
                for chunk in _parse_sse_chunks(
                    client.post(
                        "/v1/reason/stream",
                        json={"input": "Unknown status", "session_id": "status-sse"},
                    ).text
                )
                if chunk["chunk_type"] == "result"
            )
        else:
            payload = next(
                chunk["payload"]
                for chunk in _collect_ws_chunks(
                    client,
                    {"input": "Unknown status", "session_id": "status-ws"},
                )
                if chunk["chunk_type"] == "result"
            )

    assert payload["status"] == "fallback"
    assert "Unknown internal status received from reasoning engine" in caplog.text
