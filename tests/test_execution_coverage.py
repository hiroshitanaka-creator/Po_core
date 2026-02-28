from __future__ import annotations

from pathlib import Path
from typing import Set, Tuple

from pocore.runner import run_case_file

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "scenarios"
FIXED_NOW = "2026-02-22T00:00:00Z"

BASE_ARBITRATION_CODES = {
    "DEFAULT_RECOMMEND",
    "CONSTRAINT_CONFLICT",
}
MUST_COVER_ETHICS_RULE_IDS = {
    "ETH_NO_OVERCLAIM_UNKNOWN",
    "ETH_STAKEHOLDER_CONSENT",
}
MUST_COVER_PLANNING_RULE_IDS = {
    "PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN",
}


def _collect_execution_coverage() -> Tuple[Set[str], Set[str], Set[str]]:
    arbitration_codes: Set[str] = set()
    ethics_rule_ids: Set[str] = set()
    planning_rule_ids: Set[str] = set()

    for yaml_path in sorted(SCENARIOS.glob("*.yaml")):
        output = run_case_file(
            yaml_path,
            seed=0,
            deterministic=True,
            now=FIXED_NOW,
        )
        for step in output.get("trace", {}).get("steps", []):
            metrics = step.get("metrics", {})
            arbitration_code = metrics.get("arbitration_code")
            if arbitration_code:
                arbitration_codes.add(arbitration_code)

            rules_fired = metrics.get("rules_fired")
            if isinstance(rules_fired, list):
                ethics_rule_ids.update(
                    rule for rule in rules_fired if isinstance(rule, str)
                )

            rules_fired_planning = metrics.get("rules_fired_planning")
            if isinstance(rules_fired_planning, list):
                planning_rule_ids.update(
                    rule for rule in rules_fired_planning if isinstance(rule, str)
                )

    return arbitration_codes, ethics_rule_ids, planning_rule_ids


def test_execution_covers_minimum_arbitration_codes_and_ethics_rules() -> None:
    arbitration_codes, ethics_rule_ids, planning_rule_ids = _collect_execution_coverage()

    required_arbitration = set(BASE_ARBITRATION_CODES)
    if (
        run_case_file(
            SCENARIOS / "case_005.yaml", seed=0, deterministic=True, now=FIXED_NOW
        )
        .get("trace", {})
        .get("steps", [{}])[-1]
        .get("metrics", {})
        .get("policy_snapshot", {})
        .get("TIME_PRESSURE_DAYS", 0)
        >= 0
    ):
        required_arbitration.add("TIME_PRESSURE_LOW_CONF")

    missing_arbitration = required_arbitration - arbitration_codes
    missing_rules = MUST_COVER_ETHICS_RULE_IDS - ethics_rule_ids
    missing_planning_rules = MUST_COVER_PLANNING_RULE_IDS - planning_rule_ids

    assert not missing_arbitration, (
        "Missing required arbitration_code coverage from scenarios/*.yaml execution: "
        f"{sorted(missing_arbitration)}\n"
        f"covered={sorted(arbitration_codes)}"
    )
    assert not missing_rules, (
        "Missing required ethics rule_id coverage from scenarios/*.yaml execution: "
        f"{sorted(missing_rules)}\n"
        f"covered={sorted(ethics_rule_ids)}"
    )
    assert not missing_planning_rules, (
        "Missing required planning rule_id coverage from scenarios/*.yaml execution: "
        f"{sorted(missing_planning_rules)}\n"
        f"covered={sorted(planning_rule_ids)}"
    )
