"""
Tests for Phase 3 Observability features.

Covers:
- build_explanation_from_verdict() — SafetyVerdict → ExplanationChain
- extract_explanation_from_events() — TraceEvent → ExplanationChain
- InMemoryTracer listener callbacks
- Deliberation chart builders
- Interaction heatmap builder
- ExplanationEmitted trace event in schema
- PoViewer explanation/deliberation extraction
"""

import pytest

from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.trace_event import TraceEvent
from po_core.safety.wethics_gate.explanation import (
    build_explanation_from_verdict,
    extract_explanation_from_events,
)
from po_core.trace.in_memory import InMemoryTracer
from po_core.trace.schema import SPECS, validate_event

pytestmark = [pytest.mark.unit, pytest.mark.observability]


# ── Helpers ──────────────────────────────────────────────────────


def _make_allow_verdict():
    return SafetyVerdict(
        decision=Decision.ALLOW,
        rule_ids=[],
        reasons=[],
        required_changes=[],
        meta={"stage": "action"},
    )


def _make_reject_verdict():
    return SafetyVerdict(
        decision=Decision.REJECT,
        rule_ids=["outguard_001", "mode_001"],
        reasons=["Output contains harmful pattern", "Safety mode violation"],
        required_changes=[],
        meta={"stage": "action"},
    )


def _make_revise_verdict():
    return SafetyVerdict(
        decision=Decision.REVISE,
        rule_ids=["acttype_001"],
        reasons=["Action type requires revision"],
        required_changes=["Change action to suggestion", "Add safety disclaimer"],
        meta={"stage": "action"},
    )


def _make_explanation_event(decision="allow"):
    """Create a minimal ExplanationEmitted trace event."""
    return TraceEvent.now(
        "ExplanationEmitted",
        "test-req-001",
        {
            "decision": decision,
            "decision_reason": "test reason",
            "violations": [
                {
                    "code": "W2",
                    "severity": 0.6,
                    "confidence": 0.8,
                    "repairable": True,
                    "evidence": [
                        {
                            "detector_id": "policy:test_rule",
                            "message": "test evidence",
                            "strength": 0.6,
                            "confidence": 0.8,
                            "tags": ["test"],
                        }
                    ],
                    "suggested_repairs": ["fix it"],
                }
            ],
            "repairs": [{"description": "applied fix", "stage": "action"}],
            "drift": {
                "drift_score": 0.3,
                "threshold_escalate": 0.4,
                "threshold_reject": 0.7,
                "notes": "acceptable",
            },
            "summary": "Gate passed after 1 repair(s).",
        },
    )


def _make_deliberation_event():
    """Create a DeliberationCompleted trace event."""
    return TraceEvent.now(
        "DeliberationCompleted",
        "test-req-001",
        {
            "n_rounds": 2,
            "total_proposals": 8,
            "rounds": [
                {"round": 1, "n_proposals": 5, "n_revised": 0},
                {"round": 2, "n_proposals": 8, "n_revised": 3},
            ],
            "interaction_summary": {
                "n_philosophers": 5,
                "mean_harmony": 0.65,
                "mean_tension": 0.22,
                "mean_synthesis": 0.51,
                "max_tension_pair": {
                    "philosopher_a": "nietzsche",
                    "philosopher_b": "kant",
                    "tension": 0.45,
                },
                "max_harmony_pair": {
                    "philosopher_a": "aristotle",
                    "philosopher_b": "confucius",
                    "harmony": 0.82,
                },
            },
        },
    )


# ── build_explanation_from_verdict tests ─────────────────────────


class TestBuildExplanationFromVerdict:
    """Tests for build_explanation_from_verdict()."""

    def test_allow_verdict(self):
        verdict = _make_allow_verdict()
        chain = build_explanation_from_verdict(verdict)

        assert chain.decision == "allow"
        assert chain.violations == []
        assert chain.repairs == []
        assert chain.drift is None
        assert "passed" in chain.summary.lower()

    def test_reject_verdict(self):
        verdict = _make_reject_verdict()
        chain = build_explanation_from_verdict(verdict)

        assert chain.decision == "reject"
        assert len(chain.violations) == 2
        assert chain.violations[0].severity == 1.0  # REJECT → severity=1.0
        assert not chain.violations[0].repairable
        assert "rejected" in chain.summary.lower()

    def test_revise_verdict_maps_to_allow_with_repair(self):
        verdict = _make_revise_verdict()
        chain = build_explanation_from_verdict(verdict)

        assert chain.decision == "allow_with_repair"
        assert len(chain.violations) == 1
        assert chain.violations[0].repairable
        assert len(chain.repairs) == 2
        assert "repair" in chain.summary.lower()

    def test_verdict_reasons_in_decision_reason(self):
        verdict = _make_reject_verdict()
        chain = build_explanation_from_verdict(verdict)

        assert "harmful" in chain.decision_reason.lower()
        assert "mode" in chain.decision_reason.lower()

    def test_allow_default_decision_reason(self):
        verdict = _make_allow_verdict()
        chain = build_explanation_from_verdict(verdict, stage="action")

        assert "action" in chain.decision_reason.lower()

    def test_to_dict_serializable(self):
        verdict = _make_reject_verdict()
        chain = build_explanation_from_verdict(verdict)
        d = chain.to_dict()

        assert d["decision"] == "reject"
        assert isinstance(d["violations"], list)
        assert len(d["violations"]) == 2

    def test_to_markdown(self):
        verdict = _make_reject_verdict()
        chain = build_explanation_from_verdict(verdict)
        md = chain.to_markdown()

        assert "reject" in md.lower()
        assert "outguard" in md.lower() or "OUTGUARD" in md


# ── extract_explanation_from_events tests ────────────────────────


class TestExtractExplanationFromEvents:
    """Tests for extract_explanation_from_events()."""

    def test_extract_from_events(self):
        events = [
            TraceEvent.now("MemorySnapshotted", "test", {"items": 3}),
            _make_explanation_event("allow_with_repair"),
        ]
        chain = extract_explanation_from_events(events)

        assert chain is not None
        assert chain.decision == "allow_with_repair"
        assert len(chain.violations) == 1
        assert chain.violations[0].code == "W2"
        assert len(chain.repairs) == 1
        assert chain.drift is not None
        assert chain.drift.drift_score == 0.3

    def test_extract_no_explanation_returns_none(self):
        events = [
            TraceEvent.now("MemorySnapshotted", "test", {"items": 3}),
        ]
        assert extract_explanation_from_events(events) is None

    def test_extract_empty_events(self):
        assert extract_explanation_from_events([]) is None

    def test_extract_picks_last_explanation(self):
        events = [
            _make_explanation_event("allow"),
            _make_explanation_event("reject"),
        ]
        chain = extract_explanation_from_events(events)
        assert chain is not None
        assert chain.decision == "reject"

    def test_extract_no_drift(self):
        event = TraceEvent.now(
            "ExplanationEmitted",
            "test",
            {
                "decision": "allow",
                "decision_reason": "ok",
                "violations": [],
                "repairs": [],
                "drift": None,
                "summary": "ok",
            },
        )
        chain = extract_explanation_from_events([event])
        assert chain is not None
        assert chain.drift is None


# ── InMemoryTracer listener tests ────────────────────────────────


class TestInMemoryTracerListeners:
    """Tests for InMemoryTracer listener/callback mechanism."""

    def test_add_listener(self):
        tracer = InMemoryTracer()
        received = []
        tracer.add_listener(lambda e: received.append(e))

        event = TraceEvent.now("TestEvent", "req-1", {})
        tracer.emit(event)

        assert len(received) == 1
        assert received[0].event_type == "TestEvent"

    def test_multiple_listeners(self):
        tracer = InMemoryTracer()
        count_a = []
        count_b = []
        tracer.add_listener(lambda e: count_a.append(1))
        tracer.add_listener(lambda e: count_b.append(1))

        tracer.emit(TraceEvent.now("TestEvent", "req-1", {}))

        assert len(count_a) == 1
        assert len(count_b) == 1

    def test_remove_listener(self):
        tracer = InMemoryTracer()
        received = []

        def listener(e):
            return received.append(e)

        tracer.add_listener(listener)
        tracer.remove_listener(listener)

        tracer.emit(TraceEvent.now("TestEvent", "req-1", {}))
        assert len(received) == 0

    def test_listener_count(self):
        tracer = InMemoryTracer()
        assert tracer.listener_count == 0

        def listener(e):
            return None

        tracer.add_listener(listener)
        assert tracer.listener_count == 1
        tracer.remove_listener(listener)
        assert tracer.listener_count == 0

    def test_listener_exception_does_not_break_tracing(self):
        tracer = InMemoryTracer()
        tracer.add_listener(lambda e: 1 / 0)  # Will raise ZeroDivisionError

        event = TraceEvent.now("TestEvent", "req-1", {})
        tracer.emit(event)  # Should not raise

        assert len(tracer.events) == 1

    def test_emit_many_notifies_listeners(self):
        tracer = InMemoryTracer()
        received = []
        tracer.add_listener(lambda e: received.append(e.event_type))

        events = [
            TraceEvent.now("A", "req-1", {}),
            TraceEvent.now("B", "req-1", {}),
        ]
        tracer.emit_many(events)

        assert received == ["A", "B"]

    def test_remove_nonexistent_listener_is_noop(self):
        tracer = InMemoryTracer()
        tracer.remove_listener(lambda e: None)  # Should not raise


# ── Schema validation tests ──────────────────────────────────────


class TestSchemaNewEventTypes:
    """Tests for new Phase 3 event types in schema."""

    def test_explanation_emitted_registered(self):
        types = [s.event_type for s in SPECS]
        assert "ExplanationEmitted" in types

    def test_deliberation_completed_registered(self):
        types = [s.event_type for s in SPECS]
        assert "DeliberationCompleted" in types

    def test_explanation_emitted_valid_event(self):
        event = _make_explanation_event()
        issues = validate_event(event)
        assert issues == []

    def test_explanation_emitted_missing_key(self):
        event = TraceEvent.now(
            "ExplanationEmitted",
            "test",
            {"decision": "allow"},  # missing "summary"
        )
        issues = validate_event(event)
        assert len(issues) > 0

    def test_deliberation_completed_valid(self):
        event = _make_deliberation_event()
        issues = validate_event(event)
        assert issues == []


# ── Deliberation chart tests ─────────────────────────────────────


class TestDeliberationCharts:
    """Tests for deliberation Plotly figure builders."""

    def test_round_chart_with_data(self):
        from po_core.viewer.web.figures import build_deliberation_round_chart

        events = [_make_deliberation_event()]
        fig = build_deliberation_round_chart(events)
        assert fig is not None
        assert len(fig.data) == 2  # Total + Revised bars

    def test_round_chart_no_data(self):
        from po_core.viewer.web.figures import build_deliberation_round_chart

        fig = build_deliberation_round_chart([])
        assert fig is not None
        # Should have annotation about no data
        assert len(fig.layout.annotations) > 0

    def test_interaction_heatmap_with_data(self):
        from po_core.viewer.web.figures import build_interaction_heatmap

        events = [_make_deliberation_event()]
        fig = build_interaction_heatmap(events)
        assert fig is not None
        assert len(fig.data) > 0

    def test_interaction_heatmap_no_data(self):
        from po_core.viewer.web.figures import build_interaction_heatmap

        fig = build_interaction_heatmap([])
        assert fig is not None
        assert len(fig.layout.annotations) > 0


# ── PoViewer extraction tests ────────────────────────────────────


class TestPoViewerExtraction:
    """Tests for PoViewer explanation/deliberation extraction."""

    def test_explanation_extracted(self):
        from po_core.po_viewer import PoViewer

        events = [
            TraceEvent.now("MemorySnapshotted", "test", {"items": 3}),
            _make_explanation_event("allow"),
        ]
        viewer = PoViewer(events)
        expl = viewer.explanation()

        assert expl is not None
        assert expl.decision == "allow"

    def test_deliberation_data_extracted(self):
        from po_core.po_viewer import PoViewer

        events = [
            TraceEvent.now("MemorySnapshotted", "test", {"items": 3}),
            _make_deliberation_event(),
        ]
        viewer = PoViewer(events)
        delib = viewer.deliberation_data()

        assert delib is not None
        assert delib["n_rounds"] == 2
        assert delib["total_proposals"] == 8

    def test_to_dict_includes_explanation(self):
        from po_core.po_viewer import PoViewer

        events = [
            TraceEvent.now("MemorySnapshotted", "test", {"items": 3}),
            _make_explanation_event("reject"),
        ]
        viewer = PoViewer(events)
        d = viewer.to_dict()

        assert "explanation" in d
        assert d["explanation"]["decision"] == "reject"

    def test_to_dict_includes_deliberation(self):
        from po_core.po_viewer import PoViewer

        events = [
            TraceEvent.now("MemorySnapshotted", "test", {"items": 3}),
            _make_deliberation_event(),
        ]
        viewer = PoViewer(events)
        d = viewer.to_dict()

        assert "deliberation" in d
        assert d["deliberation"]["n_rounds"] == 2

    def test_markdown_includes_explanation(self):
        from po_core.po_viewer import PoViewer

        events = [
            TraceEvent.now("MemorySnapshotted", "test", {"items": 3}),
            _make_explanation_event("reject"),
        ]
        viewer = PoViewer(events)
        md = viewer.markdown()

        assert "W_Ethics Gate" in md

    def test_no_explanation_returns_none(self):
        from po_core.po_viewer import PoViewer

        events = [TraceEvent.now("MemorySnapshotted", "test", {"items": 3})]
        viewer = PoViewer(events)
        assert viewer.explanation() is None
        assert viewer.deliberation_data() is None
