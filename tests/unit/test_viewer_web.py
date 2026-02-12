"""
Tests for Viewer WebUI scaffold (Phase 3).

Validates that the Dash app can be created and has the expected structure.
These are unit tests that don't require a running server.
"""

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.observability]


class TestViewerWebAppCreation:
    """Test Dash app factory."""

    def test_create_app_no_events(self):
        """App can be created without events."""
        from po_core.viewer.web import create_app

        app = create_app()
        assert app is not None
        assert app.title == "Po_core Viewer"

    def test_create_app_custom_title(self):
        """App respects custom title."""
        from po_core.viewer.web import create_app

        app = create_app(title="Test Viewer")
        assert app.title == "Test Viewer"

    def test_create_app_with_events(self):
        """App can be created with trace events."""
        from po_core.domain.trace_event import TraceEvent
        from po_core.viewer.web import create_app

        events = [
            TraceEvent.now("MemorySnapshotted", "req-1", {"items": 0}),
            TraceEvent.now("TensorComputed", "req-1", {"metrics": []}),
        ]
        app = create_app(events=events)
        assert app is not None

    def test_app_has_layout(self):
        """App has a layout with tabs."""
        from po_core.viewer.web import create_app

        app = create_app()
        assert app.layout is not None


class TestViewerWebModuleImport:
    """Test that viewer.web module can be imported cleanly."""

    def test_import_create_app(self):
        from po_core.viewer.web import create_app

        assert callable(create_app)

    def test_import_app_module(self):
        from po_core.viewer.web.app import create_app

        assert callable(create_app)
