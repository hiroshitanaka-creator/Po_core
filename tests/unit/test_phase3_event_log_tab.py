"""
Tests for Phase 3 Event Log tab and interactive callbacks.
"""

import pytest

from po_core.domain.trace_event import TraceEvent
from po_core.viewer.web.app import _build_event_log_tab, _render_event_rows, create_app

pytestmark = [pytest.mark.unit, pytest.mark.observability]


def _make_events():
    return [
        TraceEvent.now("MemorySnapshotted", "r1", {"items": 3}),
        TraceEvent.now("TensorComputed", "r1", {"metrics": ["fp"]}),
        TraceEvent.now("PhilosopherResult", "r1", {"name": "Kant"}),
        TraceEvent.now("TensorComputed", "r1", {"metrics": ["sd"]}),
    ]


class TestEventLogTab:
    """Event log tab renders correctly."""

    def test_build_with_events(self):
        events = _make_events()
        tab = _build_event_log_tab(events)
        assert tab is not None
        # Should have dropdown + content div
        children = tab.children
        assert any(hasattr(c, "id") and getattr(c, "id", None) == "event-type-filter" for c in children)

    def test_build_empty(self):
        tab = _build_event_log_tab([])
        assert tab is not None


class TestRenderEventRows:
    """_render_event_rows filters and renders events."""

    def test_all_events(self):
        events = _make_events()
        rows = _render_event_rows(events, "__all__")
        assert len(rows) == 4

    def test_filter_by_type(self):
        events = _make_events()
        rows = _render_event_rows(events, "TensorComputed")
        assert len(rows) == 2

    def test_filter_no_match(self):
        events = _make_events()
        rows = _render_event_rows(events, "NonExistent")
        assert len(rows) == 1  # "No events match" message

    def test_empty_events(self):
        rows = _render_event_rows([], "__all__")
        assert len(rows) == 1  # "No events match" message


class TestAppWithEventLogTab:
    """create_app includes Event Log tab."""

    def test_app_has_four_tabs(self):
        events = _make_events()
        app = create_app(events=events)
        # Find the Tabs component
        tabs = app.layout.children[1]  # Second child is dcc.Tabs
        assert len(tabs.children) == 4
        labels = [t.label for t in tabs.children]
        assert "Event Log" in labels

    def test_app_callback_registered(self):
        events = _make_events()
        app = create_app(events=events)
        # App should have at least one callback
        assert len(app.callback_map) >= 1
