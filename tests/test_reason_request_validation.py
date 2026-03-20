from __future__ import annotations

import re
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.server import create_app


@pytest.fixture()
def client(tmp_path) -> TestClient:
    app = create_app(
        APISettings(
            skip_auth=True,
            api_key="",
            trace_store_backend="sqlite",
            trace_db_path=str(tmp_path / "trace_store.sqlite3"),
        )
    )
    from po_core.app.rest import auth

    app.dependency_overrides[auth.require_api_key] = lambda: None
    return TestClient(app, raise_server_exceptions=True)


@pytest.mark.parametrize(
    "session_id",
    [
        "bad space",
        "slash/not-allowed",
        "unicode-雪",
        "x" * 129,
    ],
)
def test_invalid_session_id_returns_422(client: TestClient, session_id: str) -> None:
    response = client.post(
        "/v1/reason",
        json={"input": "Validate session", "session_id": session_id},
    )

    assert response.status_code == 422


def test_omitted_session_id_still_generates_uuid(client: TestClient) -> None:
    with patch(
        "po_core.app.rest.routers.reason.po_run",
        return_value={
            "request_id": "req-validation-001",
            "status": "ok",
            "proposal": {"content": "Generated session id."},
            "proposals": [],
            "tensors": {},
            "safety_mode": "NORMAL",
        },
    ):
        response = client.post("/v1/reason", json={"input": "Generate session"})

    assert response.status_code == 200
    payload = response.json()
    assert re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        payload["session_id"],
    )


def test_metadata_rejects_too_many_properties(client: TestClient) -> None:
    metadata = {f"k{i}": i for i in range(17)}

    response = client.post(
        "/v1/reason",
        json={"input": "Validate metadata", "metadata": metadata},
    )

    assert response.status_code == 422
    assert "metadata must contain at most 16 top-level properties" in str(response.json()["detail"])


def test_metadata_rejects_oversized_json_payload(client: TestClient) -> None:
    response = client.post(
        "/v1/reason",
        json={"input": "Validate metadata", "metadata": {"blob": "x" * 2050}},
    )

    assert response.status_code == 422
    assert "metadata must serialize to at most 2048 UTF-8 bytes" in str(response.json()["detail"])


def test_philosophers_rejects_too_many_items(client: TestClient) -> None:
    response = client.post(
        "/v1/reason",
        json={
            "input": "Validate philosophers",
            "philosophers": [f"phil_{i}" for i in range(9)],
        },
    )

    assert response.status_code == 422
    assert "philosophers must contain at most 8 items" in str(response.json()["detail"])


def test_philosophers_rejects_invalid_identifier_format(client: TestClient) -> None:
    response = client.post(
        "/v1/reason",
        json={"input": "Validate philosophers", "philosophers": ["bad space"]},
    )

    assert response.status_code == 422
    assert "each philosopher ID must match pattern" in str(response.json()["detail"])


def test_philosophers_rejects_duplicate_identifiers(client: TestClient) -> None:
    response = client.post(
        "/v1/reason",
        json={"input": "Validate philosophers", "philosophers": ["kant", "kant"]},
    )

    assert response.status_code == 422
    assert "philosopher IDs must be unique" in str(response.json()["detail"])
