from __future__ import annotations

import pytest

from po_core.app.rest.config import APISettings
from po_core.runtime.settings import Settings


@pytest.mark.unit
def test_settings_from_env_reads_runtime_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    env = {
        "PO_ENABLE_SOLARWILL": "false",
        "PO_ENABLE_INTENTION_GATE": "0",
        "PO_ENABLE_ACTION_GATE": "off",
        "PO_ENABLE_PARETO_SHADOW": "yes",
        "PO_FREEDOM_PRESSURE_V2": "on",
        "PO_PHILOSOPHERS_MAX_NORMAL": "41",
        "PO_PHILOSOPHERS_MAX_WARN": "7",
        "PO_PHILOSOPHERS_MAX_CRITICAL": "2",
        "PO_PHILOSOPHER_COST_BUDGET_NORMAL": "81",
        "PO_PHILOSOPHER_COST_BUDGET_WARN": "13",
        "PO_PHILOSOPHER_COST_BUDGET_CRITICAL": "4",
        "PO_LLM_ENABLED": "true",
        "PO_LLM_PROVIDER": "openai",
        "PO_LLM_MODEL": "gpt-4o-mini",
        "PO_LLM_TIMEOUT": "3.25",
        "PO_DELIBERATION_MAX_ROUNDS": "4",
    }
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    settings = Settings.from_env()

    assert settings.enable_solarwill is False
    assert settings.enable_intention_gate is False
    assert settings.enable_action_gate is False
    assert settings.enable_pareto_shadow is True
    assert settings.use_freedom_pressure_v2 is True
    assert settings.philosophers_max_normal == 41
    assert settings.philosophers_max_warn == 7
    assert settings.philosophers_max_critical == 2
    assert settings.philosopher_cost_budget_normal == 81
    assert settings.philosopher_cost_budget_warn == 13
    assert settings.philosopher_cost_budget_critical == 4
    assert settings.enable_llm_philosophers is True
    assert settings.llm_provider == "openai"
    assert settings.llm_model == "gpt-4o-mini"
    assert settings.llm_timeout_s == pytest.approx(3.25)
    assert settings.deliberation_max_rounds == 4


@pytest.mark.unit
@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1", True),
        ("true", True),
        ("yes", True),
        ("on", True),
        ("0", False),
        ("false", False),
        ("no", False),
        ("off", False),
        ("unexpected", False),
    ],
)
def test_settings_from_env_boolean_parsing_is_explicit(
    monkeypatch: pytest.MonkeyPatch, raw: str, expected: bool
) -> None:
    monkeypatch.setenv("PO_ENABLE_SOLARWILL", raw)

    settings = Settings.from_env()

    assert settings.enable_solarwill is expected


@pytest.mark.unit
def test_settings_from_env_preserves_llm_aliases(monkeypatch: pytest.MonkeyPatch) -> None:
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
def test_rest_and_direct_paths_build_same_effective_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env = {
        "PO_ENABLE_SOLARWILL": "false",
        "PO_ENABLE_INTENTION_GATE": "true",
        "PO_ENABLE_ACTION_GATE": "false",
        "PO_PHILOSOPHERS_MAX_NORMAL": "44",
        "PO_PHILOSOPHERS_MAX_WARN": "6",
        "PO_PHILOSOPHERS_MAX_CRITICAL": "2",
        "PO_PHILOSOPHER_COST_BUDGET_NORMAL": "82",
        "PO_PHILOSOPHER_COST_BUDGET_WARN": "14",
        "PO_PHILOSOPHER_COST_BUDGET_CRITICAL": "5",
        "PO_LLM_ENABLED": "true",
        "PO_LLM_PROVIDER": "grok",
        "PO_LLM_MODEL": "grok-3-mini",
        "PO_LLM_TIMEOUT": "5.5",
    }
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    direct = Settings.from_env()
    via_rest = Settings.from_api_settings(APISettings())

    assert via_rest == Settings(
        enable_solarwill=direct.enable_solarwill,
        enable_intention_gate=direct.enable_intention_gate,
        enable_action_gate=direct.enable_action_gate,
        philosophers_max_normal=direct.philosophers_max_normal,
        philosophers_max_warn=direct.philosophers_max_warn,
        philosophers_max_critical=direct.philosophers_max_critical,
        philosopher_cost_budget_normal=direct.philosopher_cost_budget_normal,
        philosopher_cost_budget_warn=direct.philosopher_cost_budget_warn,
        philosopher_cost_budget_critical=direct.philosopher_cost_budget_critical,
        enable_llm_philosophers=direct.enable_llm_philosophers,
        llm_provider=direct.llm_provider,
        llm_model=direct.llm_model,
        llm_timeout_s=direct.llm_timeout_s,
    )
