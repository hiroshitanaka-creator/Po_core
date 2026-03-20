from __future__ import annotations

import pytest

from po_core.app.rest.config import APISettings
from po_core.runtime.settings import Settings


def _apply_env(monkeypatch: pytest.MonkeyPatch, env: dict[str, str]) -> None:
    for key, value in env.items():
        monkeypatch.setenv(key, value)


@pytest.mark.unit
def test_settings_from_env_reads_runtime_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    env = {
        "PO_ENABLE_SOLARWILL": "false",
        "PO_ENABLE_INTENTION_GATE": "0",
        "PO_ENABLE_ACTION_GATE": "off",
        "PO_ENABLE_PARETO_SHADOW": "yes",
        "PO_FREEDOM_PRESSURE_V2": "on",
        "PO_DELIBERATION_MAX_ROUNDS": "4",
        "PO_ROLES": "systems,red_team",
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
        "PO_PHILOSOPHER_EXECUTION_MODE": "process",
    }
    _apply_env(monkeypatch, env)

    settings = Settings.from_env()

    assert settings.enable_solarwill is False
    assert settings.enable_intention_gate is False
    assert settings.enable_action_gate is False
    assert settings.enable_pareto_shadow is True
    assert settings.use_freedom_pressure_v2 is True
    assert tuple(role.value for role in settings.philosopher_roles) == (
        "RED_TEAM",
        "SYSTEMS",
    )
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
    assert settings.philosopher_execution_mode == "process"
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
def test_settings_from_env_preserves_llm_aliases(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
        "PO_ENABLE_PARETO_SHADOW": "true",
        "PO_FREEDOM_PRESSURE_V2": "true",
        "PO_DELIBERATION_MAX_ROUNDS": "4",
        "PO_ROLES": "systems,red_team",
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
        "PO_PHILOSOPHER_EXECUTION_MODE": "process",
    }
    _apply_env(monkeypatch, env)

    assert Settings.from_env() == Settings.from_api_settings(APISettings())


@pytest.mark.unit
@pytest.mark.parametrize("raw", ["1", "true", "yes", "on", "0", "false", "no", "off"])
def test_rest_and_direct_paths_match_boolean_semantics(
    monkeypatch: pytest.MonkeyPatch, raw: str
) -> None:
    env = {
        "PO_ENABLE_SOLARWILL": raw,
        "PO_ENABLE_INTENTION_GATE": raw,
        "PO_ENABLE_ACTION_GATE": raw,
        "PO_ENABLE_PARETO_SHADOW": raw,
        "PO_FREEDOM_PRESSURE_V2": raw,
        "PO_LLM_ENABLED": raw,
    }
    _apply_env(monkeypatch, env)

    assert Settings.from_env() == Settings.from_api_settings(APISettings())
