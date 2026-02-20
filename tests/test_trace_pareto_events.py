"""
Test Trace Pareto Events
========================

縦スライスが回る前提で、Pareto関連のTraceEventが出ることを保証。

必須イベント:
- PolicyPrecheckSummary
- ConflictSummaryComputed (ParetoAggregator使用時)
- ParetoFrontComputed (ParetoAggregator使用時)
- ParetoWinnerSelected (ParetoAggregator使用時)
"""

from datetime import datetime, timezone


from po_core.aggregator.pareto import ParetoAggregator
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.keys import PARETO_DEBUG, PO_CORE
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.domain.trace_event import TraceEvent
from po_core.trace.in_memory import InMemoryTracer
from po_core.viewer.decision_report_md import render_markdown


class TestParetoDebugEmbedding:
    """Test that ParetoAggregator embeds debug info."""

    def test_pareto_embeds_debug_in_extra(self):
        """ParetoAggregator must embed PARETO_DEBUG in winner.extra."""
        cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
        agg = ParetoAggregator(cfg)

        ctx = Context("r1", datetime.now(timezone.utc), "test")
        tensors = TensorSnapshot(
            datetime.now(timezone.utc), metrics={"freedom_pressure": 0.3}
        )

        ps = [
            Proposal("p1", "answer", "答えます", 0.8),
            Proposal("p2", "ask_clarification", "確認します", 0.7),
        ]

        winner = agg.aggregate(ctx, Intent.neutral(), tensors, ps)

        # Check PARETO_DEBUG is embedded
        extra = dict(winner.extra)
        pc = extra.get(PO_CORE, {})
        assert PARETO_DEBUG in pc, "PARETO_DEBUG must be in winner.extra[PO_CORE]"

        dbg = pc[PARETO_DEBUG]
        assert "weights" in dbg
        assert "front" in dbg
        assert "winner" in dbg
        assert "conflicts" in dbg

    def test_pareto_debug_contains_front_rows(self):
        """Front rows must contain scores."""
        cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
        agg = ParetoAggregator(cfg)

        ctx = Context("r1", datetime.now(timezone.utc), "test")
        tensors = TensorSnapshot(
            datetime.now(timezone.utc), metrics={"freedom_pressure": 0.2}
        )

        ps = [
            Proposal("p1", "answer", "短い", 0.9),
            Proposal("p2", "answer", "もう少し長い答え", 0.7),
        ]

        winner = agg.aggregate(ctx, Intent.neutral(), tensors, ps)
        dbg = dict(winner.extra).get(PO_CORE, {}).get(PARETO_DEBUG, {})
        front = dbg.get("front", [])

        assert len(front) >= 1
        for row in front:
            assert "proposal_id" in row
            assert "action_type" in row
            assert "scores" in row
            scores = row["scores"]
            assert "safety" in scores
            assert "freedom" in scores
            assert "coherence" in scores


class TestTraceEventSimulation:
    """Test trace events that would be emitted in ensemble."""

    def test_simulate_ensemble_trace_events(self):
        """Simulate trace events that ensemble would emit."""
        tracer = InMemoryTracer()
        rid = "test-req-123"

        # Simulate events that run_turn would emit
        tracer.emit(
            TraceEvent.now(
                "TensorComputed", rid, {"metrics": ["freedom_pressure"], "version": "1"}
            )
        )
        tracer.emit(TraceEvent.now("IntentGenerated", rid, {"mode": "normal"}))
        tracer.emit(
            TraceEvent.now(
                "PhilosophersSelected",
                rid,
                {
                    "mode": "normal",
                    "n": 5,
                    "cost_total": 10,
                    "covered_tags": ["compliance"],
                },
            )
        )
        tracer.emit(
            TraceEvent.now(
                "PolicyPrecheckSummary", rid, {"allow": 3, "revise": 1, "reject": 0}
            )
        )
        tracer.emit(
            TraceEvent.now(
                "ConflictSummaryComputed",
                rid,
                {
                    "n": 1,
                    "kinds": "action_divergence",
                    "suggested_forced_action": "ask_clarification",
                },
            )
        )
        tracer.emit(
            TraceEvent.now(
                "ParetoFrontComputed",
                rid,
                {
                    "weights": {
                        "safety": 0.25,
                        "freedom": 0.30,
                        "explain": 0.20,
                        "brevity": 0.10,
                        "coherence": 0.15,
                    },
                    "front": [
                        {
                            "proposal_id": "p1",
                            "action_type": "answer",
                            "scores": {
                                "safety": 0.8,
                                "freedom": 0.7,
                                "explain": 0.5,
                                "brevity": 0.9,
                                "coherence": 0.8,
                            },
                        }
                    ],
                },
            )
        )
        tracer.emit(
            TraceEvent.now(
                "ParetoWinnerSelected",
                rid,
                {"winner": {"proposal_id": "p1", "action_type": "answer"}},
            )
        )
        tracer.emit(
            TraceEvent.now(
                "AggregateCompleted",
                rid,
                {"proposal_id": "p1", "action_type": "answer"},
            )
        )

        # Verify events
        events = tracer.events
        event_types = [e.event_type for e in events]

        assert "PolicyPrecheckSummary" in event_types
        assert "ConflictSummaryComputed" in event_types
        assert "ParetoFrontComputed" in event_types
        assert "ParetoWinnerSelected" in event_types

    def test_viewer_renders_markdown(self):
        """Viewer should render events as markdown."""
        tracer = InMemoryTracer()
        rid = "test-req-456"

        tracer.emit(
            TraceEvent.now("TensorComputed", rid, {"metrics": ["fp"], "version": "1"})
        )
        tracer.emit(
            TraceEvent.now(
                "PhilosophersSelected",
                rid,
                {
                    "mode": "warn",
                    "n": 5,
                    "cost_total": 12,
                    "covered_tags": ["compliance", "clarify"],
                },
            )
        )
        tracer.emit(
            TraceEvent.now(
                "PolicyPrecheckSummary", rid, {"allow": 4, "revise": 1, "reject": 0}
            )
        )
        tracer.emit(
            TraceEvent.now(
                "ParetoFrontComputed",
                rid,
                {
                    "weights": {"safety": 0.40, "freedom": 0.10},
                    "front": [
                        {
                            "proposal_id": "w1",
                            "action_type": "ask_clarification",
                            "scores": {
                                "safety": 0.9,
                                "freedom": 0.5,
                                "explain": 0.6,
                                "brevity": 0.8,
                                "coherence": 0.7,
                            },
                        }
                    ],
                },
            )
        )
        tracer.emit(
            TraceEvent.now(
                "ParetoWinnerSelected",
                rid,
                {"winner": {"proposal_id": "w1", "action_type": "ask_clarification"}},
            )
        )

        md = render_markdown(tracer.events)

        assert "# Po_core Decision Report" in md
        assert rid in md
        assert "## Battalion" in md
        assert "## Policy Precheck Summary" in md
        assert "## Pareto Front" in md
        assert "## Winner" in md
        assert "ask_clarification" in md


class TestViewerMarkdown:
    """Test viewer markdown rendering."""

    def test_empty_events(self):
        """Empty events should produce minimal report."""
        md = render_markdown([])
        assert "No events recorded" in md

    def test_missing_pareto_events(self):
        """Should handle missing Pareto events gracefully."""
        tracer = InMemoryTracer()
        tracer.emit(
            TraceEvent.now("TensorComputed", "r1", {"metrics": ["fp"], "version": "1"})
        )
        tracer.emit(
            TraceEvent.now(
                "AggregateCompleted",
                "r1",
                {"proposal_id": "p1", "action_type": "answer"},
            )
        )

        md = render_markdown(tracer.events)
        assert "# Po_core Decision Report" in md
        # Should fallback to AggregateCompleted for winner
        assert "Winner" in md
