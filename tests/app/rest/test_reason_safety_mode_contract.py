from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.server import create_app


def test_reason_does_not_fabricate_safety_mode_when_absent(tmp_path):
    app = create_app(
        APISettings(
            skip_auth=True,
            api_key="",
            trace_store_backend="sqlite",
            trace_db_path=str(tmp_path / "trace.sqlite3"),
        )
    )
    client = TestClient(app, raise_server_exceptions=True)

    with patch(
        "po_core.app.rest.routers.reason.po_run",
        return_value={
            "request_id": "req-1",
            "status": "ok",
            "proposal": {"content": "x"},
        },
    ):
        response = client.post("/v1/reason", json={"input": "hello"})

    assert response.status_code == 200
    assert response.json()["safety_mode"] is None
