from __future__ import annotations

import pytest

from po_core.adapters.llm_adapter import LLMAdapter
from po_core.philosophers.llm_philosopher import (
    _load_llm_philosopher_map,
    build_llm_philosopher_registry,
)
from po_core.philosophers.manifest import PhilosopherSpec


def _spec(philosopher_id: str) -> PhilosopherSpec:
    return PhilosopherSpec(
        philosopher_id=philosopher_id,
        module=f"po_core.philosophers.{philosopher_id}",
        symbol="Unused",
        enabled=True,
    )


def test_build_registry_uses_provider_map_for_each_philosopher() -> None:
    shared = LLMAdapter(provider="gemini", model="gemini-2.0-flash-lite", timeout=7.5)
    specs = [_spec("kant"), _spec("nietzsche"), _spec("hegel")]
    llm_map = {
        "kant": {"provider": "openai", "model": "gpt-4o-mini"},
        "nietzsche": {"provider": "claude", "model": "claude-haiku-4-5"},
        "hegel": {"provider": "grok", "model": "grok-3-mini"},
    }

    registry = build_llm_philosopher_registry(
        adapter=shared,
        specs=specs,
        llm_philosopher_map=llm_map,
    )

    assert registry._instances["kant"]._adapter.provider.value == "openai"
    assert registry._instances["nietzsche"]._adapter.provider.value == "claude"
    assert registry._instances["hegel"]._adapter.provider.value == "grok"

    assert registry._instances["kant"]._adapter.model == "gpt-4o-mini"
    assert registry._instances["nietzsche"]._adapter.model == "claude-haiku-4-5"
    assert registry._instances["hegel"]._adapter.model == "grok-3-mini"


def test_build_registry_falls_back_to_shared_adapter_for_unmapped() -> None:
    shared = LLMAdapter(provider="gemini", model="gemini-2.0-flash-lite", timeout=6.0)
    specs = [_spec("kant"), _spec("aristotle")]

    registry = build_llm_philosopher_registry(
        adapter=shared,
        specs=specs,
        llm_philosopher_map={"kant": {"provider": "openai", "model": "gpt-4o-mini"}},
    )

    assert registry._instances["kant"]._adapter is not shared
    assert registry._instances["aristotle"]._adapter is shared


def test_load_llm_philosopher_map_parses_yaml(tmp_path) -> None:
    mapping_file = tmp_path / "llm_map.yaml"
    mapping_file.write_text(
        """
philosophers:
  kant:
    provider: openai
    model: gpt-4o-mini
  aristotle:
    provider: gemini
""".strip(),
        encoding="utf-8",
    )

    loaded = _load_llm_philosopher_map(mapping_file)

    assert loaded == {
        "kant": {"provider": "openai", "model": "gpt-4o-mini"},
        "aristotle": {"provider": "gemini"},
    }


def test_load_llm_philosopher_map_returns_empty_for_malformed_yaml(tmp_path) -> None:
    mapping_file = tmp_path / "llm_map.yaml"
    mapping_file.write_text("philosophers: [invalid", encoding="utf-8")

    loaded = _load_llm_philosopher_map(mapping_file)

    assert loaded == {}


def test_load_llm_philosopher_map_uses_env_override_path(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mapping_file = tmp_path / "custom_map.yaml"
    mapping_file.write_text(
        """
philosophers:
  spinoza:
    provider: openai
    model: gpt-4o-mini
""".strip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", str(mapping_file))

    loaded = _load_llm_philosopher_map()

    assert loaded == {"spinoza": {"provider": "openai", "model": "gpt-4o-mini"}}


def test_load_llm_philosopher_map_returns_empty_for_missing_env_override_path(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing = tmp_path / "missing_map.yaml"
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", str(missing))

    loaded = _load_llm_philosopher_map()

    assert loaded == {}


def test_load_llm_philosopher_map_returns_empty_for_malformed_env_override_yaml(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mapping_file = tmp_path / "malformed_map.yaml"
    mapping_file.write_text("philosophers: [invalid", encoding="utf-8")
    monkeypatch.setenv("PO_LLM_PHILOSOPHER_MAP_PATH", str(mapping_file))

    loaded = _load_llm_philosopher_map()

    assert loaded == {}


def test_build_registry_with_explicit_empty_map_does_not_read_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shared = LLMAdapter(provider="gemini", model="gemini-2.0-flash-lite", timeout=6.0)
    specs = [_spec("kant"), _spec("aristotle")]

    def _should_not_be_called(*args, **kwargs):
        raise AssertionError("default map loader should not be called")

    monkeypatch.setattr(
        "po_core.philosophers.llm_philosopher._load_llm_philosopher_map",
        _should_not_be_called,
    )

    registry = build_llm_philosopher_registry(
        adapter=shared,
        specs=specs,
        llm_philosopher_map={},
    )

    assert registry._instances["kant"]._adapter is shared
    assert registry._instances["aristotle"]._adapter is shared
