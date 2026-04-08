from __future__ import annotations

import importlib

from fastapi.testclient import TestClient


def _load_api(monkeypatch, **env):
    defaults = {
        "PO_SKIP_AUTH": "false",
        "PO_API_KEY": "test-key",
        "PO_PHILOSOPHER_EXECUTION_MODE": "process",
    }
    defaults.update(env)
    for key, value in defaults.items():
        monkeypatch.setenv(key, value)
    import po_core.app.api as api_module

    return importlib.reload(api_module)


def test_legacy_generate_uses_same_auth_policy_as_rest(monkeypatch):
    api = _load_api(monkeypatch)
    client = TestClient(api.app)

    no_key = client.post("/generate", json={"user_input": "hello"})
    assert no_key.status_code == 401


def test_legacy_generate_reuses_runtime_settings_path(monkeypatch):
    api = _load_api(monkeypatch, PO_SKIP_AUTH="true")

    captured = {}

    async def _fake_async_run(
        user_input, *, philosophers=None, settings=None, tracer=None
    ):
        captured["settings"] = settings
        return {"request_id": "r1", "status": "ok", "proposal": {"content": "ok"}}

    monkeypatch.setattr(api, "async_run", _fake_async_run)

    client = TestClient(api.app)
    response = client.post("/generate", json={"user_input": "hello"})
    assert response.status_code == 200
    assert captured["settings"] is not None
