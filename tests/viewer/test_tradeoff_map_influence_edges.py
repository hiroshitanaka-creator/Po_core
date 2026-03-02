from __future__ import annotations

from datetime import datetime, timezone

from po_core.domain.trace_event import TraceEvent
from po_core.po_self import PoSelfResponse
from po_core.viewer.tradeoff_map import build_tradeoff_map
import importlib.util
from pathlib import Path


def _load_render_markdown():
    module_path = (
        Path(__file__).resolve().parents[2] / "scripts" / "export_tradeoff_map.py"
    )
    spec = importlib.util.spec_from_file_location("export_tradeoff_map", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module._render_markdown


_render_markdown = _load_render_markdown()


def _event(event_type: str, payload: dict) -> TraceEvent:
    return TraceEvent(
        event_type=event_type,
        occurred_at=datetime(2026, 2, 22, 0, 0, 0, tzinfo=timezone.utc),
        correlation_id="req-17",
        payload=payload,
    )


def test_build_tradeoff_map_adds_influence_edges_from_graph_dict() -> None:
    response = PoSelfResponse(
        prompt="test",
        text="result",
        philosophers=["kant", "aristotle"],
        metrics={},
        responses=[],
        log={},
        consensus_leader="kant",
        metadata={"request_id": "req-17", "synthesis_report": {}},
    )
    events = [
        _event(
            "DeliberationCompleted",
            {
                "influence_graph": {
                    "kant": {"influenced": {"aristotle": 0.23, "mill": 0.11}},
                    "aristotle": {"influenced": {"kant": 0.04}},
                },
                "interference_pairs_top": [["kant", "aristotle", 0.2]],
            },
        )
    ]

    tradeoff_map = build_tradeoff_map(response=response, tracer=events)

    assert (
        tradeoff_map["influence"]["influence_graph"]["kant"]["influenced"]["mill"]
        == 0.11
    )
    assert tradeoff_map["influence"]["interference_pairs_top"] == [
        ["kant", "aristotle", 0.2]
    ]
    assert {edge["to"] for edge in tradeoff_map["influence"]["influence_edges"]} == {
        "aristotle",
        "mill",
        "kant",
    }


def test_render_markdown_uses_influence_edges_for_mermaid() -> None:
    tradeoff_map = {
        "meta": {},
        "axis": {"scoreboard": {}, "disagreements": []},
        "influence": {
            "influence_graph": {
                "kant": {"influenced": {"aristotle": 0.23}},
            },
            "influence_edges": [
                {"from": "kant", "to": "aristotle", "weight": 0.23},
            ],
        },
        "timeline": [],
    }

    markdown = _render_markdown(tradeoff_map)

    assert "-->" in markdown
    assert "kant" in markdown
    assert "aristotle" in markdown
