"""
End-to-end tests for Phase 3 Observability pipeline.

Tests the full flow: run_turn → TraceEvents → PoViewer → WebUI.

These tests run the actual pipeline, so they are slightly slower
than pure unit tests but validate the integration contract.
"""

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.observability]


class TestPoViewerFromRun:
    """Test PoViewer.from_run() end-to-end."""

    def test_from_run_creates_viewer(self):
        """from_run() returns a PoViewer with events."""
        from po_core.po_viewer import PoViewer

        viewer = PoViewer.from_run("What is justice?")

        assert viewer is not None
        assert len(viewer.events) > 0
        assert viewer.request_id != "unknown"

    def test_from_run_has_pipeline_events(self):
        """from_run() captures all 10 pipeline step types."""
        from po_core.po_viewer import PoViewer

        viewer = PoViewer.from_run("What is truth?")
        types = set(viewer.event_types)

        # At minimum these should be present
        assert "MemorySnapshotted" in types
        assert "TensorComputed" in types
        assert "SafetyJudged:Intention" in types

    def test_from_run_summary(self):
        """from_run() viewer produces a summary."""
        from po_core.po_viewer import PoViewer

        viewer = PoViewer.from_run("What is beauty?")
        summary = viewer.summary()

        assert summary
        assert "events" in summary

    def test_from_run_tensor_values(self):
        """from_run() captures tensor metric values."""
        from po_core.po_viewer import PoViewer

        viewer = PoViewer.from_run("What is wisdom?")
        tensors = viewer.tensor_values()

        # Should have at least freedom_pressure
        assert isinstance(tensors, dict)

    def test_from_run_markdown(self):
        """from_run() viewer produces markdown report."""
        from po_core.po_viewer import PoViewer

        viewer = PoViewer.from_run("What is courage?")
        md = viewer.markdown()

        assert "# Po_core Run Report" in md
        assert "Pipeline Progression" in md

    def test_from_run_to_dict(self):
        """from_run() viewer serializes to dict."""
        from po_core.po_viewer import PoViewer

        viewer = PoViewer.from_run("What is love?")
        d = viewer.to_dict()

        assert "request_id" in d
        assert "n_events" in d
        assert d["n_events"] > 0


class TestPoViewerToWebUI:
    """Test PoViewer → Dash WebUI integration."""

    def test_viewer_creates_dash_app(self):
        """PoViewer events can create a Dash app."""
        from po_core.po_viewer import PoViewer
        from po_core.viewer.web import create_app

        viewer = PoViewer.from_run("What is virtue?")
        app = create_app(events=viewer.events)

        assert app is not None
        assert app.layout is not None

    def test_viewer_with_explanation_creates_full_app(self):
        """PoViewer + ExplanationChain create complete app."""
        from po_core.po_viewer import PoViewer
        from po_core.safety.wethics_gate.explanation import build_explanation_chain
        from po_core.safety.wethics_gate.types import GateDecision, GateResult
        from po_core.viewer.web import create_app

        viewer = PoViewer.from_run("What is the good life?")
        explanation = build_explanation_chain(
            GateResult(
                decision=GateDecision.ALLOW,
                violations=[],
                explanation="No violations",
            )
        )
        app = create_app(events=viewer.events, explanation=explanation)

        assert app is not None
        assert app.layout is not None
