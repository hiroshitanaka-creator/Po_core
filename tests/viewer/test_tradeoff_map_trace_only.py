from __future__ import annotations

from datetime import datetime, timezone

from po_core.domain.trace_event import TraceEvent
from po_core.viewer.tradeoff_map import build_tradeoff_map

TS = datetime(2026, 2, 22, 0, 0, 0, tzinfo=timezone.utc)


def _event(event_type: str, payload: dict) -> TraceEvent:
    return TraceEvent(
        event_type=event_type,
        occurred_at=TS,
        correlation_id="req-trace-only",
        payload=payload,
    )


def test_build_tradeoff_map_supports_trace_only_mode() -> None:
    events = [
        _event(
            "SynthesisReportBuilt",
            {
                "scoreboard": {"kant": 0.6, "aristotle": 0.4},
                "disagreements": ["duty-vs-virtue"],
                "axis_vectors": [{"axis": "duty", "kant": 0.9, "aristotle": 0.3}],
            },
        ),
        _event(
            "DeliberationCompleted",
            {
                "influence_graph": {
                    "kant": {"influenced": {"aristotle": 0.2}},
                }
            },
        ),
        _event(
            "DecisionEmitted",
            {
                "degraded": True,
                "final": {"author": "aristotle"},
            },
        ),
    ]

    tradeoff_map = build_tradeoff_map(response=None, tracer=events)

    assert set(tradeoff_map["axis"]["scoreboard"].keys()) == {"kant", "aristotle"}
    assert tradeoff_map["axis"]["axis_vectors"] == [
        {"axis": "duty", "kant": 0.9, "aristotle": 0.3}
    ]
    assert tradeoff_map["meta"]["consensus_leader"] == "aristotle"
    assert tradeoff_map["meta"]["request_id"] == "req-trace-only"
    assert tradeoff_map["meta"]["degraded"] is True
