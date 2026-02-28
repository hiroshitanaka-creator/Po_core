from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def policy_lab_module():
    script_path = Path("scripts/policy_lab.py")
    spec = importlib.util.spec_from_file_location("policy_lab", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["policy_lab"] = module
    spec.loader.exec_module(module)
    return module


def test_temporary_policy_override_restores_values(policy_lab_module) -> None:
    from pocore import policy_v1

    before_unknown = policy_v1.UNKNOWN_BLOCK
    before_days = policy_v1.TIME_PRESSURE_DAYS

    with policy_lab_module.temporary_policy_override(
        unknown_block=before_unknown + 2,
        time_pressure_days=before_days - 1,
    ) as snapshot:
        assert policy_v1.UNKNOWN_BLOCK == before_unknown + 2
        assert policy_v1.TIME_PRESSURE_DAYS == before_days - 1
        assert snapshot.to_dict()["UNKNOWN_BLOCK"] == before_unknown + 2

    assert policy_v1.UNKNOWN_BLOCK == before_unknown
    assert policy_v1.TIME_PRESSURE_DAYS == before_days


def test_policy_lab_compare_baseline_generates_impacted_requirements(
    tmp_path: Path, policy_lab_module
) -> None:
    parser = policy_lab_module.build_arg_parser()
    args = parser.parse_args(
        [
            "--unknown-block",
            "1",
            "--time-pressure-days",
            "7",
            "--now",
            "2026-02-22T00:00:00Z",
            "--seed",
            "0",
            "--scenarios-dir",
            "scenarios",
            "--output-dir",
            str(tmp_path),
            "--compare-baseline",
        ]
    )

    out = policy_lab_module.run_policy_lab(args)
    result = out["result"]

    assert Path(out["json"]).exists()
    assert Path(out["md"]).exists()
    assert result["meta"]["compare_baseline"] is True
    assert result["summary"]["changed_cases"] >= 1
    assert "REQ-ARB-001" in result["summary"]["impacted_requirements"]
    assert "REQ-ARB" in result["summary"]["impacted_requirements"]
    assert "REQ-VALUES-001" in result["summary"]["impacted_requirements"]
    assert "REQ-VALUES" in result["summary"]["impacted_requirements"]
    assert "REQ-CONSTRAINT" in result["summary"]["impacted_requirements"]
    assert (
        result["summary"]["two_track_rule_id"] == "PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN"
    )
    assert result["summary"]["two_track_triggered_cases"] >= 1
    assert result["summary"]["planning_rule_frequency_top"]
    assert result["summary"]["planning_rule_frequency_top"][0]["rule_id"]

    md_text = Path(out["md"]).read_text(encoding="utf-8")
    assert "planning two-track triggered cases" in md_text
    assert "Planning rule frequency (top)" in md_text
    assert "Values Pack rule frequency" in md_text
    assert "Conflict Pack baseline delta (--compare-baseline)" in md_text

    assert result["summary"]["values_pack"]["variant"]["rule_case_counts"]
    assert result["summary"]["conflict_pack"]["variant"]["rule_case_counts"]
    assert result["summary"]["values_pack"]["delta"]["rule_deltas"]
    assert result["summary"]["conflict_pack"]["delta"]["rule_deltas"]
    assert result["summary"]["values_pack"]["delta_summary"]
    assert result["summary"]["conflict_pack"]["delta_summary"]
    assert "change summary:" in md_text
