from __future__ import annotations

import json

from po_core.domain.trace_event import TraceEvent
from po_core.po_self import PoSelfResponse
from po_core.viewer.tradeoff_map import build_tradeoff_map


class _FakeTracer:
    def __init__(self, events):
        self.events = events


def test_build_tradeoff_map_serializable_and_keys() -> None:
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
                "influence_graph": [
                    {"from": "kant", "to": "aristotle", "weight": 0.23}
                ],
                "top_influencers": [{"philosopher": "kant", "influence": 0.23}],
                "rounds": [{"round": 1, "n_proposals": 2, "n_revised": 0}],
                "interaction_summary": {"mean_harmony": 0.8},
                "n_rounds": 1,
                "total_proposals": 2,
            },
        ),
    ]

    tradeoff_map = build_tradeoff_map(response=response, tracer=_FakeTracer(events))

    assert set(tradeoff_map.keys()) == {"meta", "axis", "influence", "timeline"}
    assert tradeoff_map["meta"]["request_id"] == "req-1"
    assert tradeoff_map["axis"]["scoreboard"]["safety"]["samples"] == 2
    assert tradeoff_map["influence"]["influence_graph"][0]["from"] == "kant"
    assert tradeoff_map["timeline"][0]["event_type"] == "PhilosophersSelected"

    # Must be JSON serializable
    json.dumps(tradeoff_map, ensure_ascii=False)
