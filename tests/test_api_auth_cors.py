from __future__ import annotations

import importlib

from fastapi.testclient import TestClient


class _FakeResponse(dict):
    pass


def _load_api_module(monkeypatch, api_key: str = "", cors_origins: str = ""):
    monkeypatch.setenv("PO_CORE_API_KEY", api_key)
    monkeypatch.setenv("PO_CORE_CORS_ORIGINS", cors_origins)
    import po_core.app.api as api_module

    return importlib.reload(api_module)


def test_generate_requires_api_key_when_secure_mode_enabled(monkeypatch):
    api = _load_api_module(monkeypatch, api_key="secret")
    async def _fake_async_run(user_input):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.post("/generate", json={"user_input": "hello"})

    assert response.status_code == 403


def test_generate_accepts_valid_bearer_api_key(monkeypatch):
    api = _load_api_module(monkeypatch, api_key="secret")
    async def _fake_async_run(user_input):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.post(
        "/generate",
        json={"user_input": "hello"},
        headers={"Authorization": "Bearer secret"},
    )

    assert response.status_code != 403


def test_options_preflight_not_blocked_in_secure_mode(monkeypatch):
    api = _load_api_module(monkeypatch, api_key="secret", cors_origins="https://example.com")
    async def _fake_async_run(user_input):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.options(
        "/generate",
        headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code != 403
