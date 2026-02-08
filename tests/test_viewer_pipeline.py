"""
Tests for Viewer Integration with new TraceEvent format (Task 7)
================================================================

Tests for:
- PoViewer (high-level viewer)
- Pipeline view (10-step progression)
- Tensor view (metric display)
- Integration with live pipeline events
"""
from __future__ import annotations

import uuid

import pytest

pytestmark = pytest.mark.pipeline

from po_core.domain.context import Context
from po_core.domain.trace_event import TraceEvent


# ── Helpers ──


def _ctx(text: str = "What is truth?") -> Context:
    return Context.now(request_id=str(uuid.uuid4()), user_input=text, meta={})


def _make_events() -> list[TraceEvent]:
    """Create a minimal but realistic set of pipeline events."""
    rid = "test-req-123"
    return [
        TraceEvent.now("MemorySnapshotted", rid, {"items": 0}),
        TraceEvent.now("TensorComputed", rid, {
            "metrics": ["freedom_pressure", "semantic_delta", "blocked_tensor", "interaction_tensor"],
            "version": "v1",
        }),
        TraceEvent.now("IntentGenerated", rid, {"goals": ["understand"]}),
        TraceEvent.now("SafetyJudged:Intention", rid, {"decision": "allow", "rule_ids": []}),
        TraceEvent.now("PhilosophersSelected", rid, {
            "mode": "NORMAL", "n": 5, "cost_total": 25, "covered_tags": ["ethics"],
            "ids": ["aristotle", "kant", "confucius", "nietzsche", "wittgenstein"],
            "workers": 4,
        }),
        TraceEvent.now("PhilosopherResult", rid, {"name": "aristotle", "n": 1, "timed_out": False, "error": "", "latency_ms": 10}),
        TraceEvent.now("PhilosopherResult", rid, {"name": "kant", "n": 1, "timed_out": False, "error": "", "latency_ms": 12}),
        TraceEvent.now("PhilosopherResult", rid, {"name": "confucius", "n": 1, "timed_out": False, "error": "", "latency_ms": 8}),
        TraceEvent.now("PolicyPrecheckSummary", rid, {"allow": 3, "revise": 0, "reject": 0}),
        TraceEvent.now("AggregateCompleted", rid, {"proposal_id": "test-prop-1", "action_type": "answer"}),
        TraceEvent.now("DecisionEmitted", rid, {
            "variant": "main", "stage": "action", "origin": "pareto",
            "degraded": False,
            "final": {"proposal_id": "test-prop-1", "action_type": "answer", "content_len": 100, "content_hash": "abc"},
            "candidate": {"proposal_id": "test-prop-1", "action_type": "answer", "content_len": 100, "content_hash": "abc"},
            "gate": {"decision": "allow", "rule_ids": []},
        }),
    ]


# ══════════════════════════════════════════════════════════════════════════
# 1. Pipeline View
# ══════════════════════════════════════════════════════════════════════════


class TestPipelineView:
    """Test pipeline progression rendering."""

    def test_pipeline_markdown_has_table(self):
        from po_core.viewer.pipeline_view import render_pipeline_markdown

        md = render_pipeline_markdown(_make_events())
        assert "## Pipeline Progression" in md
        assert "| Step |" in md

    def test_pipeline_markdown_shows_all_steps(self):
        from po_core.viewer.pipeline_view import render_pipeline_markdown

        md = render_pipeline_markdown(_make_events())
        assert "Memory Read" in md
        assert "Tensor Compute" in md
        assert "Solar Will" in md
        assert "Intention Gate" in md
        assert "Philosopher Select" in md
        assert "Party Machine" in md
        assert "Policy Precheck" in md
        assert "Pareto Aggregate" in md
        assert "Action Gate" in md

    def test_pipeline_markdown_shows_ok_status(self):
        from po_core.viewer.pipeline_view import render_pipeline_markdown

        md = render_pipeline_markdown(_make_events())
        assert "| ok |" in md

    def test_pipeline_markdown_shows_details(self):
        from po_core.viewer.pipeline_view import render_pipeline_markdown

        md = render_pipeline_markdown(_make_events())
        assert "mode=NORMAL" in md
        assert "n=5" in md
        assert "allow=3" in md

    def test_pipeline_text_rendering(self):
        from po_core.viewer.pipeline_view import render_pipeline_text

        text = render_pipeline_text(_make_events())
        assert "Pipeline Progression" in text
        assert "[ok]" in text
        assert "Memory Read" in text

    def test_pipeline_empty_events(self):
        from po_core.viewer.pipeline_view import render_pipeline_markdown

        md = render_pipeline_markdown([])
        assert "No events" in md

    def test_pipeline_shadow_skipped(self):
        from po_core.viewer.pipeline_view import render_pipeline_markdown

        md = render_pipeline_markdown(_make_events())
        assert "skipped" in md  # Shadow A/B step not present

    def test_pipeline_blocked_status(self):
        from po_core.viewer.pipeline_view import render_pipeline_markdown

        events = [
            TraceEvent.now("MemorySnapshotted", "r1", {"items": 0}),
            TraceEvent.now("TensorComputed", "r1", {"metrics": [], "version": "v1"}),
            TraceEvent.now("IntentGenerated", "r1", {}),
            TraceEvent.now("SafetyJudged:Intention", "r1", {"decision": "reject", "rule_ids": ["W0"]}),
        ]
        md = render_pipeline_markdown(events)
        assert "blocked" in md

    def test_pipeline_degraded_status(self):
        from po_core.viewer.pipeline_view import render_pipeline_markdown

        events = _make_events()
        # Replace last DecisionEmitted with degraded one
        events[-1] = TraceEvent.now("DecisionEmitted", "test-req-123", {
            "variant": "main", "stage": "action", "origin": "pareto_fallback",
            "degraded": True,
            "final": {"proposal_id": "fb-1"}, "candidate": {"proposal_id": "orig-1"},
            "gate": {"decision": "revise"},
        })
        md = render_pipeline_markdown(events)
        assert "degraded" in md


# ══════════════════════════════════════════════════════════════════════════
# 2. Tensor View
# ══════════════════════════════════════════════════════════════════════════


class TestTensorView:
    """Test tensor metric display."""

    def test_tensor_markdown_header(self):
        from po_core.viewer.tensor_view import render_tensor_markdown

        md = render_tensor_markdown(_make_events())
        assert "## Tensor Metrics" in md
        assert "version" in md

    def test_tensor_markdown_lists_metrics(self):
        from po_core.viewer.tensor_view import render_tensor_markdown

        md = render_tensor_markdown(_make_events())
        assert "freedom_pressure" in md
        assert "semantic_delta" in md
        assert "blocked_tensor" in md
        assert "interaction_tensor" in md

    def test_tensor_text_rendering(self):
        from po_core.viewer.tensor_view import render_tensor_text

        text = render_tensor_text(_make_events())
        assert "Tensor Metrics" in text
        assert "freedom_pressure" in text

    def test_tensor_empty_events(self):
        from po_core.viewer.tensor_view import render_tensor_markdown

        md = render_tensor_markdown([])
        assert "No TensorComputed" in md

    def test_extract_tensor_values_empty(self):
        from po_core.viewer.tensor_view import extract_tensor_values

        assert extract_tensor_values([]) == {}

    def test_extract_tensor_values_with_data(self):
        from po_core.viewer.tensor_view import extract_tensor_values

        events = [
            TraceEvent.now("TensorComputed", "r1", {
                "metrics": ["freedom_pressure", "semantic_delta"],
                "version": "v1",
                "freedom_pressure": 0.15,
                "semantic_delta": 0.72,
            }),
        ]
        vals = extract_tensor_values(events)
        assert vals["freedom_pressure"] == 0.15
        assert vals["semantic_delta"] == 0.72


# ══════════════════════════════════════════════════════════════════════════
# 3. PoViewer (high-level)
# ══════════════════════════════════════════════════════════════════════════


class TestPoViewer:
    """Test high-level PoViewer class."""

    def test_viewer_init(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer(_make_events())
        assert len(viewer.events) == len(_make_events())

    def test_viewer_request_id(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer(_make_events())
        assert viewer.request_id == "test-req-123"

    def test_viewer_event_types(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer(_make_events())
        types = viewer.event_types
        assert "MemorySnapshotted" in types
        assert "TensorComputed" in types
        assert "DecisionEmitted" in types

    def test_viewer_markdown_contains_all_sections(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer(_make_events())
        md = viewer.markdown()
        assert "# Po_core Run Report" in md
        assert "## Pipeline Progression" in md
        assert "## Tensor Metrics" in md
        assert "# Po_core Decision Report" in md

    def test_viewer_summary_ok(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer(_make_events())
        s = viewer.summary()
        assert "ok" in s
        assert "events" in s
        assert "philosophers" in s

    def test_viewer_summary_blocked(self):
        from po_core.po_viewer import PoViewer

        events = [
            TraceEvent.now("SafetyJudged:Intention", "r1", {"decision": "reject", "rule_ids": ["W0"]}),
        ]
        viewer = PoViewer(events)
        assert "blocked" in viewer.summary()

    def test_viewer_to_dict(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer(_make_events())
        d = viewer.to_dict()
        assert d["request_id"] == "test-req-123"
        assert d["n_events"] == len(_make_events())
        assert isinstance(d["event_types"], list)
        assert isinstance(d["summary"], str)

    def test_viewer_pipeline_text(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer(_make_events())
        text = viewer.pipeline_text()
        assert "Pipeline Progression" in text

    def test_viewer_tensor_text(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer(_make_events())
        text = viewer.tensor_text()
        assert "Tensor Metrics" in text

    def test_viewer_empty_events(self):
        from po_core.po_viewer import PoViewer

        viewer = PoViewer([])
        assert viewer.request_id == "unknown"
        assert "unknown" in viewer.summary()


# ══════════════════════════════════════════════════════════════════════════
# 4. Integration: PoViewer with live pipeline events
# ══════════════════════════════════════════════════════════════════════════


class TestViewerIntegration:
    """Integration tests: PoViewer with real pipeline events."""

    def test_viewer_from_posself(self):
        """PoSelf.generate() → get_trace() → PoViewer."""
        from po_core.po_self import PoSelf
        from po_core.po_viewer import PoViewer

        po = PoSelf()
        po.generate("What is the meaning of life?")
        tracer = po.get_trace()

        viewer = PoViewer(tracer.events)
        assert len(viewer.events) >= 5
        assert "ok" in viewer.summary()

    def test_viewer_markdown_from_live_run(self):
        """Full Markdown report from live pipeline."""
        from po_core.po_self import PoSelf
        from po_core.po_viewer import PoViewer

        po = PoSelf()
        po.generate("What is justice?")
        tracer = po.get_trace()

        viewer = PoViewer(tracer.events)
        md = viewer.markdown()

        assert "# Po_core Run Report" in md
        assert "## Pipeline Progression" in md
        assert "Memory Read" in md
        assert "Tensor Compute" in md

    def test_viewer_event_types_from_live_run(self):
        """Live pipeline should produce expected event types."""
        from po_core.po_self import PoSelf
        from po_core.po_viewer import PoViewer

        po = PoSelf()
        po.generate("What is truth?")
        tracer = po.get_trace()

        viewer = PoViewer(tracer.events)
        types = viewer.event_types

        assert "MemorySnapshotted" in types
        assert "TensorComputed" in types
        assert "DecisionEmitted" in types

    def test_viewer_summary_has_philosopher_count(self):
        """Summary should include philosopher count from live run."""
        from po_core.po_self import PoSelf
        from po_core.po_viewer import PoViewer

        po = PoSelf()
        po.generate("What is beauty?")
        tracer = po.get_trace()

        viewer = PoViewer(tracer.events)
        s = viewer.summary()
        assert "philosophers" in s

    def test_viewer_to_dict_from_live_run(self):
        """to_dict() should work with live pipeline events."""
        from po_core.po_self import PoSelf
        from po_core.po_viewer import PoViewer

        po = PoSelf()
        po.generate("What is freedom?")
        tracer = po.get_trace()

        viewer = PoViewer(tracer.events)
        d = viewer.to_dict()
        assert d["n_events"] > 0
        assert len(d["event_types"]) >= 5
