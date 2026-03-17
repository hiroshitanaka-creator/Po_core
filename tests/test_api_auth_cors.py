from __future__ import annotations

import importlib

from fastapi.testclient import TestClient


class _FakeResponse(dict):
    pass


def _load_api_module(monkeypatch, api_key: str = "", cors_origins: str = ""):
    monkeypatch.setenv("PO_API_KEY", api_key)
    monkeypatch.setenv("PO_CORS_ORIGINS", cors_origins)
    # legacy aliases are still supported; canonical keys are preferred.
    monkeypatch.delenv("PO_CORE_API_KEY", raising=False)
    monkeypatch.delenv("PO_CORE_CORS_ORIGINS", raising=False)
    import po_core.app.api as api_module

    return importlib.reload(api_module)


def test_generate_requires_api_key_when_secure_mode_enabled(monkeypatch):
    api = _load_api_module(monkeypatch, api_key="secret")

    async def _fake_async_run(user_input, *, philosophers=None):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.post("/generate", json={"user_input": "hello"})

    assert response.status_code == 403


def test_generate_accepts_valid_bearer_api_key(monkeypatch):
    api = _load_api_module(monkeypatch, api_key="secret")

    async def _fake_async_run(user_input, *, philosophers=None):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.post(
        "/generate",
        json={"user_input": "hello"},
        headers={"Authorization": "Bearer secret"},
    )

    assert response.status_code != 403


def test_generate_forwards_philosophers_allowlist(monkeypatch):
    api = _load_api_module(monkeypatch)
    captured = {}

    async def _fake_async_run(user_input, *, philosophers=None):
        captured["user_input"] = user_input
        captured["philosophers"] = philosophers
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.post(
        "/generate",
        json={"user_input": "hello", "philosophers": ["kant"]},
    )

    assert response.status_code == 200
    assert captured["user_input"] == "hello"
    assert captured["philosophers"] == ["kant"]


def test_generate_rejects_unknown_fields(monkeypatch):
    api = _load_api_module(monkeypatch)

    async def _fake_async_run(user_input, *, philosophers=None):
        return _FakeResponse(ok=True)

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.post(
        "/generate",
        json={"user_input": "hello", "unexpected": 1},
    )

    assert response.status_code == 422


def test_generate_allowlist_no_overlap_returns_422_with_detail(monkeypatch):
    api = _load_api_module(monkeypatch)

    async def _fake_async_run(user_input, *, philosophers=None):
        raise ValueError(
            "philosophers allowlist ['kant'] has no overlap with SafetyMode-'normal' selection ['aristotle']"
        )

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.post(
        "/generate",
        json={"user_input": "hello", "philosophers": ["kant"]},
    )

    assert response.status_code == 422
    assert "allowlist" in str(response.json()["detail"])
    assert "no overlap" in str(response.json()["detail"])


def test_options_preflight_not_blocked_in_secure_mode(monkeypatch):
    api = _load_api_module(
        monkeypatch, api_key="secret", cors_origins="https://example.com"
    )

    async def _fake_async_run(user_input, *, philosophers=None):
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
