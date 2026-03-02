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
