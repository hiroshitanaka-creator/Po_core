from __future__ import annotations

import json
from copy import deepcopy

from po_core.domain.trace_event import TraceEvent
from po_core.po_self import PoSelfResponse
from po_core.viewer.tradeoff_map import build_tradeoff_map, validate_tradeoff_map_v1


class _FakeTracer:
    def __init__(self, events):
        self.events = events


def test_build_tradeoff_map_serializable_and_keys(monkeypatch) -> None:
    monkeypatch.setenv("PO_AXIS_SCORING_CALIBRATION_PARAMS", "/tmp/calibration.json")
    response = PoSelfResponse(
        prompt="How should I choose?",
        text="result",
        philosophers=["kant", "aristotle"],
        metrics={},
        responses=[],
        log={},
        consensus_leader="kant",
        metadata={
            "request_id": "req-1",
            "status": "ok",
            "degraded": False,
            "synthesis_report": {
                "axis_name": "decision_axis",
                "axis_spec_version": "axis_spec_v1",
                "scoreboard": {"safety": {"mean": 0.7, "variance": 0.02, "samples": 2}},
                "disagreements": [{"axis": "safety", "spread": 0.3}],
                "stance_distribution": {"pro": 1, "con": 1},
            },
        },
    )

    events = [
        TraceEvent.now(
            "PhilosophersSelected",
            "req-1",
            {"ids": ["kant", "aristotle"], "mode": "NORMAL", "workers": 2},
        ),
        TraceEvent.now(
            "DeliberationCompleted",
            "req-1",
            {
                "influence_graph": [{"from": "kant", "to": "aristotle", "weight": 0.23}],
                "top_influencers": [{"philosopher": "kant", "influence": 0.23}],
                "rounds": [{"round": 1, "n_proposals": 2, "n_revised": 0}],
                "interaction_summary": {"mean_harmony": 0.8},
                "n_rounds": 1,
                "total_proposals": 2,
            },
        ),
    ]

    tradeoff_map = build_tradeoff_map(response=response, tracer=_FakeTracer(events))

    assert set(tradeoff_map.keys()) == {
        "schema_version",
        "meta",
        "axis",
        "influence",
        "timeline",
    }
    assert tradeoff_map["schema_version"] == "tradeoff_map_v1"
    assert tradeoff_map["meta"]["request_id"] == "req-1"
    assert tradeoff_map["meta"]["axis_name"] == "decision_axis"
    assert tradeoff_map["meta"]["axis_spec_version"] == "axis_spec_v1"
    assert tradeoff_map["meta"]["axis_scoring_calibration_enabled"] is True
    assert tradeoff_map["axis"]["scoreboard"]["safety"]["samples"] == 2
    assert tradeoff_map["influence"]["influence_graph"][0]["from"] == "kant"
    assert tradeoff_map["timeline"][0]["event_type"] == "PhilosophersSelected"

    # Must be JSON serializable
    json.dumps(tradeoff_map, ensure_ascii=False)


def test_validate_tradeoff_map_v1_accepts_minimal_valid_payload() -> None:
    tradeoff_map = {
        "schema_version": "tradeoff_map_v1",
        "meta": {},
        "axis": {},
        "influence": {},
        "timeline": [],
    }

    validate_tradeoff_map_v1(tradeoff_map)


def test_validate_tradeoff_map_v1_rejects_missing_or_invalid_required_keys() -> None:
    valid = {
        "schema_version": "tradeoff_map_v1",
        "meta": {},
        "axis": {},
        "influence": {},
        "timeline": [],
    }
    required = {
        "schema_version": 1,
        "meta": [],
        "axis": [],
        "influence": [],
        "timeline": {},
    }

    for key, bad_value in required.items():
        missing = deepcopy(valid)
        missing.pop(key)
        try:
            validate_tradeoff_map_v1(missing)
            raise AssertionError(f"expected ValueError for missing key: {key}")
        except ValueError as exc:
            assert key in str(exc)

        wrong_type = deepcopy(valid)
        wrong_type[key] = bad_value
        try:
            validate_tradeoff_map_v1(wrong_type)
            raise AssertionError(f"expected ValueError for wrong type: {key}")
        except ValueError as exc:
            assert key in str(exc)
