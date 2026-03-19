from __future__ import annotations

import pytest

from po_core.runtime.settings import Settings


@pytest.mark.unit
@pytest.mark.phase5
def test_runtime_settings_accepts_legacy_llm_env_aliases(monkeypatch):
    monkeypatch.delenv("PO_LLM_ENABLED", raising=False)
    monkeypatch.delenv("PO_LLM_TIMEOUT", raising=False)
    monkeypatch.setenv("PO_ENABLE_LLM_PHILOSOPHERS", "1")
    monkeypatch.setenv("PO_LLM_PROVIDER", "claude")
    monkeypatch.setenv("PO_LLM_MODEL", "claude-haiku-4-5")
    monkeypatch.setenv("PO_LLM_TIMEOUT_S", "7.0")

    settings = Settings.from_env()

    assert settings.enable_llm_philosophers is True
    assert settings.llm_provider == "claude"
    assert settings.llm_model == "claude-haiku-4-5"
    assert settings.llm_timeout_s == pytest.approx(7.0)


@pytest.mark.unit
def test_runtime_settings_reads_core_feature_flags_from_env(monkeypatch):
    monkeypatch.setenv("PO_ENABLE_SOLARWILL", "off")
    monkeypatch.setenv("PO_ENABLE_INTENTION_GATE", "0")
    monkeypatch.setenv("PO_ENABLE_ACTION_GATE", "no")
    monkeypatch.setenv("PO_ENABLE_PARETO_SHADOW", "on")
    monkeypatch.setenv("PO_FREEDOM_PRESSURE_V2", "yes")
    monkeypatch.setenv("PO_DELIBERATION_MAX_ROUNDS", "4")

    settings = Settings.from_env()

    assert settings.enable_solarwill is False
    assert settings.enable_intention_gate is False
    assert settings.enable_action_gate is False
    assert settings.enable_pareto_shadow is True
    assert settings.use_freedom_pressure_v2 is True
    assert settings.deliberation_max_rounds == 4
