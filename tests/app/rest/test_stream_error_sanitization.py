from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.server import create_app


RAW_ERROR = "database password leaked"


def _build_client(tmp_path) -> TestClient:
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
    return TestClient(app, raise_server_exceptions=True)


def _parse_sse_chunks(raw_text: str) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []
    for line in raw_text.splitlines():
        if line.startswith("data: "):
            chunks.append(json.loads(line[6:]))
    return chunks


def test_sse_stream_errors_are_sanitized(tmp_path) -> None:
    client = _build_client(tmp_path)

    with patch(
        "po_core.app.rest.routers.reason.po_async_run",
        new=AsyncMock(side_effect=RuntimeError(RAW_ERROR)),
    ):
        response = client.post("/v1/reason/stream", json={"input": "trigger"})

    assert response.status_code == 200
    error_chunk = next(
        chunk for chunk in _parse_sse_chunks(response.text) if chunk["chunk_type"] == "error"
    )
    assert error_chunk["payload"] == {
        "code": "internal_error",
        "message": "internal server error",
    }
    assert RAW_ERROR not in response.text


def test_websocket_stream_errors_are_sanitized(tmp_path) -> None:
    client = _build_client(tmp_path)

    with patch(
        "po_core.app.rest.routers.reason.po_async_run",
        new=AsyncMock(side_effect=RuntimeError(RAW_ERROR)),
    ):
        with client.websocket_connect("/v1/ws/reason") as websocket:
            websocket.send_json({"input": "trigger"})
            chunks: list[dict[str, object]] = []
            while True:
                chunk = websocket.receive_json()
                chunks.append(chunk)
                if chunk["chunk_type"] == "error":
                    break

    error_chunk = chunks[-1]
    assert error_chunk == {
        "chunk_type": "error",
        "payload": {
            "code": "internal_error",
            "message": "internal server error",
        },
    }
    assert RAW_ERROR not in json.dumps(chunks)
