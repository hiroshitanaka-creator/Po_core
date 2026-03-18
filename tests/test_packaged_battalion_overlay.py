from __future__ import annotations

from po_core.domain.safety_mode import SafetyMode
from po_core.runtime.settings import Settings
from po_core.runtime.wiring import build_test_system


def test_packaged_battalion_defaults_preserve_settings_overrides() -> None:
    settings = Settings(
        philosophers_max_normal=17,
        philosophers_max_warn=3,
        philosophers_max_critical=1,
        philosopher_cost_budget_normal=21,
        philosopher_cost_budget_warn=8,
        philosopher_cost_budget_critical=2,
    )

    system = build_test_system(settings=settings)
    plans = system.registry._plans

    assert plans[SafetyMode.NORMAL].limit == 17
    assert plans[SafetyMode.NORMAL].cost_budget == 21
    assert plans[SafetyMode.WARN].limit == 3
    assert plans[SafetyMode.WARN].cost_budget == 8
    assert plans[SafetyMode.CRITICAL].limit == 1
    assert plans[SafetyMode.CRITICAL].cost_budget == 2

    # Packaged policy semantics still come from battalion defaults.
    assert plans[SafetyMode.NORMAL].require_tags == (
        "planner",
        "critic",
        "compliance",
        "creative",
        "redteam",
    )
