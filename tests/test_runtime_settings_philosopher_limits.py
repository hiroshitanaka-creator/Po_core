from __future__ import annotations

from po_core.domain.safety_mode import SafetyMode
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.runtime.settings import Settings


def _selected_count_from_settings(settings: Settings, mode: SafetyMode) -> int:
    registry = PhilosopherRegistry(
        max_normal=settings.philosophers_max_normal,
        max_warn=settings.philosophers_max_warn,
        max_critical=settings.philosophers_max_critical,
        budget_normal=settings.philosopher_cost_budget_normal,
        budget_warn=settings.philosopher_cost_budget_warn,
        budget_critical=settings.philosopher_cost_budget_critical,
        cache_instances=False,
    )
    return len(registry.select(mode).selected_ids)


def test_settings_from_env_reads_philosopher_limits_and_budgets(monkeypatch):
    monkeypatch.setenv("PO_PHILOSOPHERS_MAX_NORMAL", "42")
    monkeypatch.setenv("PO_PHILOSOPHERS_MAX_WARN", "7")
    monkeypatch.setenv("PO_PHILOSOPHERS_MAX_CRITICAL", "2")
    monkeypatch.setenv("PO_PHILOSOPHER_COST_BUDGET_NORMAL", "90")
    monkeypatch.setenv("PO_PHILOSOPHER_COST_BUDGET_WARN", "15")
    monkeypatch.setenv("PO_PHILOSOPHER_COST_BUDGET_CRITICAL", "4")

    settings = Settings.from_env()

    assert settings.philosophers_max_normal == 42
    assert settings.philosophers_max_warn == 7
    assert settings.philosophers_max_critical == 2
    assert settings.philosopher_cost_budget_normal == 90
    assert settings.philosopher_cost_budget_warn == 15
    assert settings.philosopher_cost_budget_critical == 4


def test_raising_normal_limit_and_budget_increases_selection_count():
    baseline = Settings()
    expanded = Settings(philosophers_max_normal=42, philosopher_cost_budget_normal=80)

    baseline_count = _selected_count_from_settings(baseline, SafetyMode.NORMAL)
    expanded_count = _selected_count_from_settings(expanded, SafetyMode.NORMAL)

    assert baseline_count == 39
    assert expanded_count == 42
    assert expanded_count > baseline_count


def test_budget_control_is_effective_under_same_limit():
    generous_budget = Settings(
        philosophers_max_normal=42, philosopher_cost_budget_normal=80
    )
    tight_budget = Settings(
        philosophers_max_normal=42, philosopher_cost_budget_normal=20
    )

    generous_count = _selected_count_from_settings(generous_budget, SafetyMode.NORMAL)
    tight_count = _selected_count_from_settings(tight_budget, SafetyMode.NORMAL)

    assert generous_count == 42
    assert tight_count < generous_count
