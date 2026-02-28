from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

from pocore.parse_input import extract_features
from pocore.policy_v1 import TIME_PRESSURE_DAYS, UNKNOWN_SOFT

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "scenarios"
EXPECTED_FILES = sorted(SCENARIOS.glob("*_expected.json"))
PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN = "PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN"


def _load_case_features() -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for expected_path in EXPECTED_FILES:
        case_stem = expected_path.stem.replace("_expected", "")
        yaml_path = SCENARIOS / f"{case_stem}.yaml"
        if not yaml_path.exists():
            continue

        with expected_path.open("r", encoding="utf-8") as f:
            expected = json.load(f)
        with yaml_path.open("r", encoding="utf-8") as f:
            case = yaml.safe_load(f)

        now = expected.get("meta", {}).get("created_at", "2026-02-22T00:00:00Z")
        features = extract_features(case, now=now)
        records.append(
            {
                "case_stem": case_stem,
                "now": now,
                "features": features,
                "planning_rules_fired": [
                    rule
                    for step in expected.get("trace", {}).get("steps", [])
                    for rule in step.get("metrics", {}).get("rules_fired_planning", [])
                    if isinstance(rule, str)
                ],
            }
        )

    return records


def _format_records(records: List[Dict[str, Any]]) -> str:
    if not records:
        return "(none)"

    lines = []
    for row in records:
        features = row["features"]
        lines.append(
            "- {case}: values_empty={values_empty}, constraint_conflict={conflict}, "
            "unknowns_count={unknowns}, days_to_deadline={days}, stakeholders_count={stakeholders}".format(
                case=row["case_stem"],
                values_empty=features.get("values_empty"),
                conflict=features.get("constraint_conflict"),
                unknowns=features.get("unknowns_count"),
                days=features.get("days_to_deadline"),
                stakeholders=features.get("stakeholders_count"),
            )
        )
    return "\n".join(lines)


def test_golden_has_unknowns_deadline_conflict_boundary_case() -> None:
    records = _load_case_features()
    threshold_matched = [
        row
        for row in records
        if row["features"].get("days_to_deadline") is not None
        and row["features"].get("unknowns_count", 0) >= UNKNOWN_SOFT
        and row["features"].get("days_to_deadline") <= TIME_PRESSURE_DAYS
    ]

    if TIME_PRESSURE_DAYS >= 0:
        assert threshold_matched, (
            "No *_expected.json-backed case satisfies unknowns×deadline boundary: "
            f"unknowns_count >= UNKNOWN_SOFT({UNKNOWN_SOFT}) and "
            f"days_to_deadline <= TIME_PRESSURE_DAYS({TIME_PRESSURE_DAYS}).\n"
            "Scanned cases:\n"
            f"{_format_records(records)}"
        )
        return

    near_deadline_matched = [
        row
        for row in records
        if row["features"].get("days_to_deadline") is not None
        and row["features"].get("unknowns_count", 0) >= UNKNOWN_SOFT
    ]
    assert near_deadline_matched, (
        "No *_expected.json-backed case satisfies unknowns+deadline observability when "
        f"TIME_PRESSURE_DAYS={TIME_PRESSURE_DAYS}.\n"
        "Scanned cases:\n"
        f"{_format_records(records)}"
    )


def test_golden_has_externality_stakeholders_boundary_case() -> None:
    records = _load_case_features()
    matched = [
        row for row in records if row["features"].get("stakeholders_count", 0) >= 2
    ]

    assert matched, (
        "No *_expected.json-backed case satisfies stakeholders externality boundary: "
        "stakeholders_count >= 2.\n"
        "Scanned cases:\n"
        f"{_format_records(records)}"
    )


def test_golden_has_two_track_planning_under_time_pressure_unknowns() -> None:
    records = _load_case_features()
    matched = [
        row
        for row in records
        if row["features"].get("days_to_deadline") is not None
        and row["features"].get("unknowns_count", 0) > 0
        and row["features"].get("days_to_deadline") <= TIME_PRESSURE_DAYS
        and PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN
        in row.get("planning_rules_fired", [])
    ]

    if TIME_PRESSURE_DAYS >= 0:
        assert matched, (
            "No *_expected.json-backed case validates Two-Track Plan firing under "
            "unknowns/time-pressure condition: unknowns_count > 0 and "
            f"days_to_deadline <= TIME_PRESSURE_DAYS({TIME_PRESSURE_DAYS}) with "
            f"planning rule {PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN}.\n"
            "Scanned cases:\n"
            f"{_format_records(records)}"
        )
        return

    unknowns_present = [
        row
        for row in records
        if row["features"].get("days_to_deadline") is not None
        and row["features"].get("unknowns_count", 0) > 0
        and PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN
        in row.get("planning_rules_fired", [])
    ]
    assert unknowns_present, (
        "No *_expected.json-backed case validates Two-Track Plan observability with "
        f"planning rule {PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN} when "
        f"TIME_PRESSURE_DAYS={TIME_PRESSURE_DAYS}.\n"
        "Scanned cases:\n"
        f"{_format_records(records)}"
    )


def test_golden_has_values_empty_with_near_deadline_case() -> None:
    records = _load_case_features()
    matched = [
        row
        for row in records
        if row["features"].get("values_empty") is True
        and row["features"].get("days_to_deadline") is not None
        and row["features"].get("days_to_deadline") <= 1
    ]

    assert matched, (
        "No *_expected.json-backed case satisfies values_empty + near deadline boundary: "
        "values_empty == True and days_to_deadline <= 1.\n"
        "Scanned cases:\n"
        f"{_format_records(records)}"
    )


def test_golden_has_constraint_conflict_with_multiple_stakeholders_case() -> None:
    records = _load_case_features()
    matched = [
        row
        for row in records
        if row["features"].get("constraint_conflict") is True
        and row["features"].get("stakeholders_count", 0) >= 2
    ]

    assert matched, (
        "No *_expected.json-backed case satisfies constraint_conflict + multiple stakeholders boundary: "
        "constraint_conflict == True and stakeholders_count >= 2.\n"
        "Scanned cases:\n"
        f"{_format_records(records)}"
    )
