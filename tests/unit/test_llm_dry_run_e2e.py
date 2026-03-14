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

        # Backward-compatible env toggle for tests without touching production code.
        import os

        forced_provider = os.getenv("PO_TEST_FAKE_LLM_EMPTY_PROVIDER")
        forced_user_contains = os.getenv("PO_TEST_FAKE_LLM_EMPTY_USER_CONTAINS")
        forced_system_contains = os.getenv("PO_TEST_FAKE_LLM_EMPTY_SYSTEM_CONTAINS")

        if (
            forced_provider
            and provider == forced_provider
            and (not forced_user_contains or forced_user_contains in user)
            and (not forced_system_contains or forced_system_contains in system)
        ):
            return ""

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


def _enable_forced_llm_unavailable_for_openai(
    monkeypatch: pytest.MonkeyPatch, marker: str
) -> None:
    monkeypatch.setenv("PO_TEST_FAKE_LLM_EMPTY_PROVIDER", "openai")
    monkeypatch.setenv("PO_TEST_FAKE_LLM_EMPTY_USER_CONTAINS", marker)
    monkeypatch.setenv("PO_TEST_FAKE_LLM_EMPTY_SYSTEM_CONTAINS", "You are")


def _create_rest_client() -> TestClient:
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
    return TestClient(app, raise_server_exceptions=True)


def _parse_sse_chunks(response_text: str) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []
    for line in response_text.splitlines():
        if line.startswith("data: "):
            chunks.append(json.loads(line[6:]))
    return chunks


def _collect_ws_chunks(ws, *, max_chunks: int = 256) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []
    for _ in range(max_chunks):
        chunk = ws.receive_json()
        chunks.append(chunk)
        if chunk.get("chunk_type") in {"done", "error"}:
            break
    return chunks


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

    proposals = result.get("proposals", [])
    assert proposals
    assert all("philosopher_id" in proposal for proposal in proposals)
    assert all("content" in proposal for proposal in proposals)
    assert all("weight" in proposal for proposal in proposals)


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
    client = _create_rest_client()

    response = client.post("/v1/reason", json={"input": "dry run rest"})

    providers = {call["provider"] for call in fake_llm_generate}

    assert response.status_code == 200
    body = response.json()
    assert fake_llm_generate
    assert "openai" in providers
    assert "gemini" in providers

    philosophers = body.get("philosophers", [])
    assert philosophers

    observed_providers = {p.get("provider") for p in philosophers if p.get("provider")}
    observed_models = {p.get("model") for p in philosophers if p.get("model")}

    assert observed_providers
    assert observed_models
    assert "openai" in observed_providers
    assert "gemini" in observed_providers

    trace_resp = client.get(f"/v1/trace/{body['session_id']}")
    assert trace_resp.status_code == 200
    trace_events = trace_resp.json().get("events", [])
    assert any(
        "llm_provider" in json.dumps(event.get("payload", {}), ensure_ascii=False)
        and "llm_model" in json.dumps(event.get("payload", {}), ensure_ascii=False)
        for event in trace_events
    )


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


@pytest.mark.unit
@pytest.mark.phase5
def test_rest_stream_sse_dry_run_exposes_llm_routing_observability(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    _disable_external_battalion_table(monkeypatch, tmp_path)
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", _write_map_file(tmp_path))
    client = _create_rest_client()

    response = client.post("/v1/reason/stream", json={"input": "dry run sse"})

    assert response.status_code == 200
    chunks = _parse_sse_chunks(response.text)

    chunk_types = {chunk.get("chunk_type") for chunk in chunks}
    assert {"started", "event", "result", "done"}.issubset(chunk_types)

    philosopher_events = [
        chunk
        for chunk in chunks
        if chunk.get("chunk_type") == "event"
        and isinstance(chunk.get("payload"), dict)
        and chunk["payload"].get("event_type") == "PhilosopherResult"
    ]
    assert philosopher_events

    philosopher_payloads = [
        event["payload"].get("payload")
        for event in philosopher_events
        if isinstance(event["payload"].get("payload"), dict)
    ]
    assert any("llm_provider" in payload for payload in philosopher_payloads)
    assert any("llm_model" in payload for payload in philosopher_payloads)

    result_chunk = next(chunk for chunk in chunks if chunk.get("chunk_type") == "result")
    philosophers = result_chunk.get("payload", {}).get("philosophers", [])
    assert philosophers
    assert any(p.get("provider") for p in philosophers)
    assert any(p.get("model") for p in philosophers)

    recorder_providers = {call["provider"] for call in fake_llm_generate}
    assert "openai" in recorder_providers
    assert "gemini" in recorder_providers


@pytest.mark.unit
@pytest.mark.phase5
def test_rest_ws_dry_run_exposes_llm_routing_observability(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    _disable_external_battalion_table(monkeypatch, tmp_path)
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", _write_map_file(tmp_path))
    client = _create_rest_client()

    with client.websocket_connect("/v1/ws/reason") as ws:
        ws.send_json({"input": "dry run websocket"})
        chunks = _collect_ws_chunks(ws)

    chunk_types = {chunk.get("chunk_type") for chunk in chunks}
    assert "started" in chunk_types
    assert "result" in chunk_types
    assert "done" in chunk_types

    philosopher_events = [
        chunk
        for chunk in chunks
        if chunk.get("chunk_type") == "event"
        and isinstance(chunk.get("payload"), dict)
        and chunk["payload"].get("event_type") == "PhilosopherResult"
    ]
    assert philosopher_events

    philosopher_payloads = [
        event["payload"].get("payload")
        for event in philosopher_events
        if isinstance(event["payload"].get("payload"), dict)
    ]
    assert any("llm_provider" in payload for payload in philosopher_payloads)
    assert any("llm_model" in payload for payload in philosopher_payloads)

    result_chunk = next(chunk for chunk in chunks if chunk.get("chunk_type") == "result")
    philosophers = result_chunk.get("payload", {}).get("philosophers", [])
    assert philosophers
    assert any(p.get("provider") for p in philosophers)
    assert any(p.get("model") for p in philosophers)

    recorder_providers = {call["provider"] for call in fake_llm_generate}
    assert "openai" in recorder_providers
    assert "gemini" in recorder_providers




@pytest.mark.unit
@pytest.mark.phase5
def test_rest_stream_sse_dry_run_exposes_llm_fallback_observability(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    _disable_external_battalion_table(monkeypatch, tmp_path)
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", _write_map_file(tmp_path))
    marker = "force stream fallback sse"
    _enable_forced_llm_unavailable_for_openai(monkeypatch, marker)
    client = _create_rest_client()

    response = client.post("/v1/reason/stream", json={"input": marker})

    assert response.status_code == 200
    chunks = _parse_sse_chunks(response.text)

    philosopher_events = [
        chunk
        for chunk in chunks
        if chunk.get("chunk_type") == "event"
        and isinstance(chunk.get("payload"), dict)
        and chunk["payload"].get("event_type") == "PhilosopherResult"
    ]
    assert philosopher_events

    philosopher_payloads = [
        event["payload"].get("payload")
        for event in philosopher_events
        if isinstance(event["payload"].get("payload"), dict)
    ]
    assert any(payload.get("llm_fallback") is True for payload in philosopher_payloads)
    assert any(
        payload.get("llm_fallback") is True
        and payload.get("fallback_reason") == "llm_unavailable"
        for payload in philosopher_payloads
    )

    result_chunk = next(chunk for chunk in chunks if chunk.get("chunk_type") == "result")
    philosophers = result_chunk.get("payload", {}).get("philosophers", [])
    assert philosophers
    assert any(p.get("llm_fallback") is True for p in philosophers)
    assert any(
        p.get("llm_fallback") is True
        and p.get("fallback_reason") == "llm_unavailable"
        for p in philosophers
    )

    recorder_providers = {call["provider"] for call in fake_llm_generate}
    assert "openai" in recorder_providers
    assert "gemini" in recorder_providers


@pytest.mark.unit
@pytest.mark.phase5
def test_rest_ws_dry_run_exposes_llm_fallback_observability(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    _disable_external_battalion_table(monkeypatch, tmp_path)
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", _write_map_file(tmp_path))
    marker = "force stream fallback ws"
    _enable_forced_llm_unavailable_for_openai(monkeypatch, marker)
    client = _create_rest_client()

    with client.websocket_connect("/v1/ws/reason") as ws:
        ws.send_json({"input": marker})
        chunks = _collect_ws_chunks(ws)

    philosopher_events = [
        chunk
        for chunk in chunks
        if chunk.get("chunk_type") == "event"
        and isinstance(chunk.get("payload"), dict)
        and chunk["payload"].get("event_type") == "PhilosopherResult"
    ]
    assert philosopher_events

    philosopher_payloads = [
        event["payload"].get("payload")
        for event in philosopher_events
        if isinstance(event["payload"].get("payload"), dict)
    ]
    assert any(payload.get("llm_fallback") is True for payload in philosopher_payloads)
    assert any(
        payload.get("llm_fallback") is True
        and payload.get("fallback_reason") == "llm_unavailable"
        for payload in philosopher_payloads
    )

    result_chunk = next(chunk for chunk in chunks if chunk.get("chunk_type") == "result")
    philosophers = result_chunk.get("payload", {}).get("philosophers", [])
    assert philosophers
    assert any(p.get("llm_fallback") is True for p in philosophers)
    assert any(
        p.get("llm_fallback") is True
        and p.get("fallback_reason") == "llm_unavailable"
        for p in philosophers
    )

    recorder_providers = {call["provider"] for call in fake_llm_generate}
    assert "openai" in recorder_providers
    assert "gemini" in recorder_providers


@pytest.mark.unit
@pytest.mark.phase5
def test_rest_stream_sse_dry_run_uses_shared_fallback_on_malformed_map(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    fake_llm_generate: list[dict[str, str]],
) -> None:
    _disable_external_battalion_table(monkeypatch, tmp_path)
    malformed = tmp_path / "llm_map_malformed.yaml"
    malformed.write_text("philosophers: [invalid", encoding="utf-8")
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", str(malformed))
    client = _create_rest_client()

    response = client.post(
        "/v1/reason/stream", json={"input": "dry run sse malformed map"}
    )

    assert response.status_code == 200
    chunks = _parse_sse_chunks(response.text)
    philosopher_events = [
        chunk
        for chunk in chunks
        if chunk.get("chunk_type") == "event"
        and isinstance(chunk.get("payload"), dict)
        and chunk["payload"].get("event_type") == "PhilosopherResult"
    ]
    assert philosopher_events

    result_chunk = next(chunk for chunk in chunks if chunk.get("chunk_type") == "result")
    philosophers = result_chunk.get("payload", {}).get("philosophers", [])
    assert philosophers
    assert {p.get("provider") for p in philosophers if p.get("provider")} == {
        "gemini"
    }

    recorder_providers = {call["provider"] for call in fake_llm_generate}
    assert recorder_providers == {"gemini"}
