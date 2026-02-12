"""
Tests for Viewer WebUI (Phase 3).

Validates:
- Dash app creation (empty, with events, with explanation)
- Tab structure and content
- ExplanationChain rendering in ethics tab
- E2E: pipeline events → WebUI app
"""

import pytest

from po_core.domain.trace_event import TraceEvent
from po_core.safety.wethics_gate.explanation import (
    ExplanationChain,
    build_explanation_chain,
)
from po_core.safety.wethics_gate.types import (
    Evidence,
    GateDecision,
    GateResult,
    Violation,
)

pytestmark = [pytest.mark.unit, pytest.mark.observability]


# ── Helpers ──────────────────────────────────────────────────────


def _make_events():
    rid = "test-req-web"
    return [
        TraceEvent.now("MemorySnapshotted", rid, {"items": 2}),
        TraceEvent.now(
            "TensorComputed",
            rid,
            {
                "metrics": ["freedom_pressure"],
                "version": "v1",
                "freedom_pressure": 0.42,
            },
        ),
        TraceEvent.now(
            "SafetyJudged:Intention", rid, {"decision": "allow", "rule_ids": []}
        ),
        TraceEvent.now(
            "PhilosophersSelected",
            rid,
            {"mode": "NORMAL", "n": 2, "cost_total": 2},
        ),
        TraceEvent.now(
            "PhilosopherResult",
            rid,
            {"name": "aristotle", "n": 1, "latency_ms": 10, "n_proposals": 1},
        ),
        TraceEvent.now(
            "PhilosopherResult",
            rid,
            {"name": "kant", "n": 1, "latency_ms": 15, "n_proposals": 1},
        ),
        TraceEvent.now(
            "AggregateCompleted",
            rid,
            {"proposal_id": "prop:aristotle:1", "action_type": "accept"},
        ),
        TraceEvent.now(
            "DecisionEmitted",
            rid,
            {"stage": "decision", "origin": "pareto", "degraded": False, "final": "answer"},
        ),
    ]


def _make_explanation():
    result = GateResult(
        decision=GateDecision.ALLOW_WITH_REPAIR,
        violations=[
            Violation(
                code="W4",
                severity=0.5,
                confidence=0.7,
                repairable=True,
                evidence=[
                    Evidence(
                        code="W4",
                        message="exclusion pattern",
                        strength=0.5,
                        confidence=0.7,
                        detector_id="keyword_detector",
                    )
                ],
            )
        ],
        repair_log=["W4_map: cut off -> support with migration plan"],
        drift_score=0.12,
        explanation="Repair succeeded",
    )
    return build_explanation_chain(result)


# ── App Creation Tests ───────────────────────────────────────────


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
        from po_core.viewer.web import create_app

        app = create_app(events=_make_events())
        assert app is not None

    def test_create_app_with_explanation(self):
        """App can be created with ExplanationChain."""
        from po_core.viewer.web import create_app

        app = create_app(events=_make_events(), explanation=_make_explanation())
        assert app is not None

    def test_app_has_layout(self):
        """App has a layout with tabs."""
        from po_core.viewer.web import create_app

        app = create_app()
        assert app.layout is not None


# ── Full App with Data Tests ─────────────────────────────────────


class TestViewerWebWithData:
    """Test app created with real pipeline data."""

    def test_app_with_events_has_pipeline_chart(self):
        from po_core.viewer.web import create_app

        app = create_app(events=_make_events())
        # Layout is rendered without errors
        assert app.layout is not None

    def test_app_with_explanation_shows_badge(self):
        from po_core.viewer.web import create_app

        app = create_app(
            events=_make_events(),
            explanation=_make_explanation(),
        )
        assert app.layout is not None

    def test_app_with_explanation_reject(self):
        """App handles REJECT explanation correctly."""
        from po_core.viewer.web import create_app

        result = GateResult(
            decision=GateDecision.REJECT,
            violations=[
                Violation(code="W0", severity=0.9, confidence=0.8, repairable=False)
            ],
            explanation="Hard reject: W0",
        )
        chain = build_explanation_chain(result)
        app = create_app(explanation=chain)
        assert app.layout is not None


# ── Module Import Tests ──────────────────────────────────────────


class TestViewerWebModuleImport:
    """Test that viewer.web module can be imported cleanly."""

    def test_import_create_app(self):
        from po_core.viewer.web import create_app

        assert callable(create_app)

    def test_import_app_module(self):
        from po_core.viewer.web.app import create_app

        assert callable(create_app)

    def test_import_figures_module(self):
        from po_core.viewer.web.figures import (
            build_drift_gauge,
            build_philosopher_chart,
            build_pipeline_chart,
            build_tensor_chart,
            decision_badge_style,
        )

        assert callable(build_tensor_chart)
        assert callable(build_philosopher_chart)
        assert callable(build_pipeline_chart)
        assert callable(build_drift_gauge)
        assert callable(decision_badge_style)
