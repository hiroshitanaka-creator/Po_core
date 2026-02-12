"""
Tests for Plotly figure builders (Phase 3 Viewer WebUI).

Validates that TraceEvent data → Plotly figures works correctly,
including edge cases (empty events, missing data, etc.).
"""

import pytest

from po_core.domain.trace_event import TraceEvent
from po_core.viewer.web.figures import (
    build_drift_gauge,
    build_philosopher_chart,
    build_pipeline_chart,
    build_tensor_chart,
    decision_badge_style,
)

pytestmark = [pytest.mark.unit, pytest.mark.observability]


# ── Helpers ──────────────────────────────────────────────────────


def _make_pipeline_events():
    """Create a minimal set of pipeline trace events."""
    rid = "test-req-001"
    return [
        TraceEvent.now("MemorySnapshotted", rid, {"items": 3}),
        TraceEvent.now(
            "TensorComputed",
            rid,
            {
                "metrics": ["freedom_pressure", "semantic_delta", "blocked_tensor"],
                "version": "v1",
                "freedom_pressure": 0.25,
                "semantic_delta": 0.55,
                "blocked_tensor": 0.10,
            },
        ),
        TraceEvent.now("IntentGenerated", rid, {}),
        TraceEvent.now(
            "SafetyJudged:Intention", rid, {"decision": "allow", "rule_ids": []}
        ),
        TraceEvent.now(
            "PhilosophersSelected",
            rid,
            {"mode": "NORMAL", "n": 3, "cost_total": 3, "ids": ["a", "b", "c"]},
        ),
        TraceEvent.now(
            "PhilosopherResult",
            rid,
            {"name": "aristotle", "n": 1, "latency_ms": 12, "n_proposals": 1},
        ),
        TraceEvent.now(
            "PhilosopherResult",
            rid,
            {"name": "kant", "n": 1, "latency_ms": 18, "n_proposals": 1},
        ),
        TraceEvent.now(
            "PhilosopherResult",
            rid,
            {"name": "nietzsche", "n": 1, "latency_ms": 8, "n_proposals": 1},
        ),
        TraceEvent.now(
            "PolicyPrecheckSummary", rid, {"allow": 3, "revise": 0, "reject": 0}
        ),
        TraceEvent.now(
            "AggregateCompleted",
            rid,
            {"proposal_id": "prop:aristotle:1", "action_type": "accept"},
        ),
        TraceEvent.now(
            "DecisionEmitted",
            rid,
            {
                "stage": "decision",
                "origin": "pareto",
                "degraded": False,
                "final": "Wisdom is...",
            },
        ),
    ]


# ── Tensor Chart Tests ───────────────────────────────────────────


class TestTensorChart:
    def test_with_data(self):
        events = _make_pipeline_events()
        fig = build_tensor_chart(events)

        assert fig is not None
        assert len(fig.data) == 1
        assert fig.data[0].orientation == "h"
        # 3 metrics
        assert len(fig.data[0].x) == 3

    def test_empty_events(self):
        fig = build_tensor_chart([])
        assert fig is not None
        # Should have annotation for "No tensor data"
        assert len(fig.layout.annotations) > 0

    def test_no_tensor_event(self):
        events = [TraceEvent.now("MemorySnapshotted", "r1", {"items": 0})]
        fig = build_tensor_chart(events)
        assert len(fig.layout.annotations) > 0


# ── Pipeline Chart Tests ─────────────────────────────────────────


class TestPipelineChart:
    def test_full_pipeline(self):
        events = _make_pipeline_events()
        fig = build_pipeline_chart(events)

        assert fig is not None
        assert len(fig.data) == 1
        # 10 pipeline steps
        assert len(fig.data[0].y) == 10

    def test_blocked_pipeline(self):
        """Pipeline chart shows blocked step in red."""
        events = [
            TraceEvent.now("MemorySnapshotted", "r1", {"items": 0}),
            TraceEvent.now(
                "SafetyJudged:Intention",
                "r1",
                {"decision": "reject", "rule_ids": ["W0"]},
            ),
        ]
        fig = build_pipeline_chart(events)
        # Find the blocked step's color
        colors = fig.data[0].marker.color
        # Step 4 (index 3) should be red (#e94560)
        assert "#e94560" in colors

    def test_empty_events(self):
        events = []
        fig = build_pipeline_chart(events)
        assert fig is not None


# ── Philosopher Chart Tests ──────────────────────────────────────


class TestPhilosopherChart:
    def test_with_data(self):
        events = _make_pipeline_events()
        fig = build_philosopher_chart(events)

        assert fig is not None
        assert len(fig.data) == 1
        # 3 philosophers
        assert len(fig.data[0].y) == 3

    def test_error_philosopher_red(self):
        events = [
            TraceEvent.now(
                "PhilosopherResult",
                "r1",
                {
                    "name": "broken",
                    "n": 0,
                    "latency_ms": -1,
                    "n_proposals": 0,
                    "error": "timeout",
                },
            ),
        ]
        fig = build_philosopher_chart(events)
        colors = fig.data[0].marker.color
        assert "#e94560" in colors

    def test_empty_events(self):
        fig = build_philosopher_chart([])
        assert len(fig.layout.annotations) > 0


# ── Drift Gauge Tests ────────────────────────────────────────────


class TestDriftGauge:
    def test_with_value(self):
        fig = build_drift_gauge(0.35)
        assert fig is not None
        assert fig.data[0].value == 0.35

    def test_high_drift(self):
        fig = build_drift_gauge(0.85)
        assert fig.data[0].value == 0.85

    def test_none_drift(self):
        fig = build_drift_gauge(None)
        assert len(fig.layout.annotations) > 0

    def test_custom_thresholds(self):
        fig = build_drift_gauge(0.5, threshold_escalate=0.3, threshold_reject=0.6)
        assert fig is not None


# ── Decision Badge Tests ─────────────────────────────────────────


class TestDecisionBadge:
    @pytest.mark.parametrize(
        "decision,expected_label",
        [
            ("allow", "ALLOW"),
            ("allow_with_repair", "ALLOW WITH REPAIR"),
            ("reject", "REJECT"),
            ("escalate", "ESCALATE"),
        ],
    )
    def test_known_decisions(self, decision, expected_label):
        badge = decision_badge_style(decision)
        assert badge["label"] == expected_label
        assert "color" in badge

    def test_unknown_decision(self):
        badge = decision_badge_style("custom")
        assert badge["label"] == "CUSTOM"
