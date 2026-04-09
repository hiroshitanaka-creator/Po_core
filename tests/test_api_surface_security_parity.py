from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.server import create_app


class _FakeResponse(dict):
    pass


@pytest.fixture
def legacy_api_module(monkeypatch):
    def _load(*, skip_auth: bool, api_key: str, cors_origins: str = "*"):
        monkeypatch.setenv("PO_SKIP_AUTH", "true" if skip_auth else "false")
        monkeypatch.setenv("PO_API_KEY", api_key)
        monkeypatch.setenv("PO_CORS_ORIGINS", cors_origins)
        monkeypatch.delenv("PO_CORE_API_KEY", raising=False)
        monkeypatch.delenv("PO_CORE_CORS_ORIGINS", raising=False)
        import po_core.app.api as api_module

        return importlib.reload(api_module)

    return _load


def test_legacy_generate_rejects_missing_api_key_when_auth_enforced(
    legacy_api_module, monkeypatch
) -> None:
    api = legacy_api_module(skip_auth=False, api_key="secret")

    async def _fake_async_run(user_input: str, *, philosophers=None):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    with TestClient(api.app) as client:
        response = client.post("/generate", json={"user_input": "hello"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API key"}
    assert response.headers["www-authenticate"] == "ApiKey"


def test_legacy_generate_rejects_invalid_api_key_when_auth_enforced(
    legacy_api_module, monkeypatch
) -> None:
    api = legacy_api_module(skip_auth=False, api_key="secret")

    async def _fake_async_run(user_input: str, *, philosophers=None):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    with TestClient(api.app) as client:
        response = client.post(
            "/generate",
            json={"user_input": "hello"},
            headers={"X-API-Key": "wrong"},
        )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API key"}


def test_legacy_generate_fails_closed_on_auth_misconfiguration(
    legacy_api_module, monkeypatch
) -> None:
    api = legacy_api_module(skip_auth=False, api_key="   ")

    async def _fake_async_run(user_input: str, *, philosophers=None):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    with TestClient(api.app) as client:
        response = client.post(
            "/generate",
            json={"user_input": "hello"},
            headers={"X-API-Key": "secret"},
        )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Server misconfigured: PO_API_KEY must be set when PO_SKIP_AUTH=false"
    }


def test_legacy_generate_matches_rest_auth_response_shape() -> None:
    app = create_app(
        APISettings(
            skip_auth=False,
            api_key="secret",
            trace_store_backend="memory",
            review_store_backend="memory",
        )
    )

    with TestClient(app) as client:
        rest_response = client.post("/v1/reason", json={"input": "hello"})

    assert rest_response.status_code == 401
    assert rest_response.json() == {"detail": "Invalid or missing API key"}
    assert rest_response.headers["www-authenticate"] == "ApiKey"


def test_legacy_generate_honors_configured_api_key_header_like_rest(
    legacy_api_module, monkeypatch
) -> None:
    api = legacy_api_module(skip_auth=False, api_key="secret")
    monkeypatch.setattr(
        api,
        "_legacy_api_settings",
        APISettings(skip_auth=False, api_key="secret", api_key_header="X-Custom-Key"),
    )

    async def _fake_async_run(user_input: str, *, philosophers=None):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    with TestClient(api.app) as client:
        response = client.post(
            "/generate",
            json={"user_input": "hello"},
            headers={"X-Custom-Key": "secret"},
        )

    assert response.status_code == 200
