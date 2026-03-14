from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from po_core.adapters.llm_adapter import LLMAdapter
from po_core.app.rest.config import APISettings
from po_core.app.rest.server import create_app
from po_core.runtime.settings import Settings


@pytest.fixture
def fake_llm_generate(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, str]]:
    calls: list[dict[str, str]] = []

    def _fake_generate(self: LLMAdapter, system: str, user: str) -> str:
        provider = self.provider.value
        model = self.model
        self.actual_model = model
        calls.append(
            {
                "provider": provider,
                "model": model,
                "system": system,
                "user": user,
            }
        )
        return json.dumps(
            {
                "reasoning": f"[DRYRUN provider={provider} model={model}] {user}",
                "perspective": "dry-run",
                "confidence": 0.77,
                "action_type": "answer",
                "citations": [],
            }
        )

    monkeypatch.setattr(LLMAdapter, "generate", _fake_generate)
    return calls


def _write_map_file(tmp_path) -> str:
    map_file = tmp_path / "llm_map.yaml"
    map_file.write_text(
        """
philosophers:
  aristotle:
    provider: openai
    model: gpt-4o-mini
  kant:
    provider: openai
    model: gpt-4o-mini
  confucius:
    provider: openai
    model: gpt-4o-mini
""".strip(),
        encoding="utf-8",
    )
    return str(map_file)


def _runtime_settings() -> Settings:
    return Settings(
        enable_llm_philosophers=True,
        llm_provider="gemini",
        philosophers_max_normal=5,
        philosopher_cost_budget_normal=10,
        freedom_pressure_warn=1.0,
        freedom_pressure_critical=2.0,
        philosopher_timeout_s_normal=30.0,
        philosopher_workers_normal=1,
        deliberation_max_rounds=1,
    )


def _disable_external_battalion_table(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    monkeypatch.setenv(
        "PO_CORE_BATTALION_TABLE", str(tmp_path / "missing_battalion.yaml")
    )


@pytest.mark.unit
@pytest.mark.phase5
def test_public_run_dry_run_e2e_uses_mapped_and_shared_providers(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    from po_core.app import api

    _disable_external_battalion_table(monkeypatch, tmp_path)
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", _write_map_file(tmp_path))

    result = api.run("dry run public api", settings=_runtime_settings())

    providers = {call["provider"] for call in fake_llm_generate}

    assert result["status"] in {"ok", "blocked", "fallback"}
    assert fake_llm_generate
    assert "openai" in providers
    assert "gemini" in providers


@pytest.mark.unit
@pytest.mark.phase5
@pytest.mark.asyncio
async def test_public_async_run_dry_run_e2e_uses_mapped_and_shared_providers(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    from po_core.app import api

    _disable_external_battalion_table(monkeypatch, tmp_path)
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", _write_map_file(tmp_path))

    result = await api.async_run(
        "dry run public api async", settings=_runtime_settings()
    )

    providers = {call["provider"] for call in fake_llm_generate}

    assert result["status"] in {"ok", "blocked", "fallback"}
    assert fake_llm_generate
    assert "openai" in providers
    assert "gemini" in providers


@pytest.mark.unit
@pytest.mark.phase5
def test_rest_reason_dry_run_e2e_records_fake_llm_calls(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    _disable_external_battalion_table(monkeypatch, tmp_path)
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", _write_map_file(tmp_path))

    app = create_app(
        APISettings(
            skip_auth=True,
            enable_llm_philosophers=True,
            llm_provider="gemini",
            philosophers_max_normal=5,
            philosopher_cost_budget_normal=10,
        )
    )
    from po_core.app.rest import auth

    app.dependency_overrides[auth.require_api_key] = lambda: None
    client = TestClient(app, raise_server_exceptions=True)

    response = client.post("/v1/reason", json={"input": "dry run rest"})

    providers = {call["provider"] for call in fake_llm_generate}

    assert response.status_code == 200
    assert fake_llm_generate
    assert "openai" in providers
    assert "gemini" in providers


@pytest.mark.unit
@pytest.mark.phase5
def test_public_run_dry_run_e2e_falls_back_to_shared_provider_on_malformed_map(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    from po_core.app import api

    _disable_external_battalion_table(monkeypatch, tmp_path)
    malformed = tmp_path / "llm_map_malformed.yaml"
    malformed.write_text("philosophers: [invalid", encoding="utf-8")
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", str(malformed))

    result = api.run("dry run malformed map", settings=_runtime_settings())

    providers = {call["provider"] for call in fake_llm_generate}

    assert result["status"] in {"ok", "blocked", "fallback"}
    assert fake_llm_generate
    assert providers == {"gemini"}
