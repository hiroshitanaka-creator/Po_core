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
            "- {case}: unknowns_count={unknowns}, days_to_deadline={days}, "
            "stakeholders_count={stakeholders}".format(
                case=row["case_stem"],
                unknowns=features.get("unknowns_count"),
                days=features.get("days_to_deadline"),
                stakeholders=features.get("stakeholders_count"),
            )
        )
    return "\n".join(lines)


def test_golden_has_unknowns_deadline_conflict_boundary_case() -> None:
    records = _load_case_features()
    matched = [
        row
        for row in records
        if row["features"].get("days_to_deadline") is not None
        and row["features"].get("unknowns_count", 0) >= UNKNOWN_SOFT
        and row["features"].get("days_to_deadline") <= TIME_PRESSURE_DAYS
    ]

    assert matched, (
        "No *_expected.json-backed case satisfies unknowns×deadline boundary: "
        f"unknowns_count >= UNKNOWN_SOFT({UNKNOWN_SOFT}) and "
        f"days_to_deadline <= TIME_PRESSURE_DAYS({TIME_PRESSURE_DAYS}).\n"
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
