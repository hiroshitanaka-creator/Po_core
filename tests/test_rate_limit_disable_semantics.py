from __future__ import annotations

from fastapi.testclient import TestClient

from po_core.app.rest import auth
from po_core.app.rest.config import APISettings
from po_core.app.rest.routers import reason as reason_router
from po_core.app.rest.server import create_app


def _stub_result(request_id: str) -> dict[str, object]:
    return {
        "request_id": request_id,
        "status": "approved",
        "proposal": {"content": "ok"},
        "safety_mode": "NORMAL",
        "proposals": [],
        "tensors": {},
    }


def test_http_rate_limit_zero_disables_limiter(monkeypatch) -> None:
    monkeypatch.setattr(
        reason_router, "po_run", lambda *args, **kwargs: _stub_result("req-1")
    )

    app = create_app(
        APISettings(
            skip_auth=True,
            api_key="",
            rate_limit_per_minute=0,
            trace_store_backend="memory",
            review_store_backend="memory",
        )
    )
    app.dependency_overrides[auth.require_api_key] = lambda: None
    client = TestClient(app, raise_server_exceptions=True)

    calls = {"count": 0}

    def _never_limit(_item, *identifiers, cost=1):
        calls["count"] += 1
        raise AssertionError(
            "rate limiter storage should not be consulted when disabled"
        )

    monkeypatch.setattr(app.state.limiter._limiter, "hit", _never_limit)

    for _ in range(3):
        response = client.post("/v1/reason", json={"input": "What is justice?"})
        assert response.status_code == 200
        assert response.json()["response"] == "ok"

    assert calls["count"] == 0


def test_websocket_rate_limit_zero_disables_limiter(monkeypatch) -> None:
    monkeypatch.setattr(
        reason_router, "po_run", lambda *args, **kwargs: _stub_result("req-ws")
    )

    async def _fake_async_run(*args, **kwargs):
        return _stub_result("req-ws")

    monkeypatch.setattr(reason_router, "po_async_run", _fake_async_run)

    app = create_app(
        APISettings(
            skip_auth=True,
            api_key="",
            rate_limit_per_minute=0,
            trace_store_backend="memory",
            review_store_backend="memory",
        )
    )
    app.dependency_overrides[auth.require_api_key] = lambda: None
    client = TestClient(app, raise_server_exceptions=True)

    for expected_input in ("first", "second", "third"):
        with client.websocket_connect("/v1/ws/reason") as websocket:
            websocket.send_json({"input": expected_input})
            chunk_types: list[str] = []
            response_payload: dict[str, object] | None = None
            while True:
                message = websocket.receive_json()
                chunk_types.append(message["chunk_type"])
                if message["chunk_type"] == "result":
                    response_payload = message["payload"]
                if message["chunk_type"] == "done":
                    break

            assert chunk_types[0] == "started"
            assert response_payload is not None
            assert response_payload["response"] == "ok"
