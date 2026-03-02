from __future__ import annotations

from datetime import datetime, timezone

from po_core.domain.trace_event import TraceEvent
from po_core.viewer.web.app import create_app


def test_create_app_includes_tradeoff_tab_and_builds_layout() -> None:
    events = [
        TraceEvent(
            event_type="DeliberationCompleted",
            occurred_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
            correlation_id="req-1",
            payload={
                "influence_graph": {
                    "kant": {"influenced": {"mill": 0.2}},
                }
            },
        )
    ]

    app = create_app(events=events)

    tabs = app.layout.children[1]
    labels = [tab.label for tab in tabs.children]
    assert "Trade-off Map" in labels


def test_create_app_tradeoff_tab_shows_axis_no_signal_warning() -> None:
    events = [
        TraceEvent(
            event_type="SynthesisReportBuilt",
            occurred_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
            correlation_id="req-2",
            payload={
                "scoreboard": {"safety": {"mean": 0.5, "variance": 0.0, "samples": 1}},
                "axis_scoring_diagnostics": {
                    "n_vectors": 1,
                    "hit_rate": 0.0,
                    "mean_total_hits": 0.0,
                    "warn_no_signal": True,
                },
            },
        )
    ]

    app = create_app(events=events)

    tabs = app.layout.children[1]
    tradeoff_tab = next(tab for tab in tabs.children if tab.value == "tab-tradeoff")
    tab_text = str(tradeoff_tab.children)
    assert "low-signal" in tab_text
