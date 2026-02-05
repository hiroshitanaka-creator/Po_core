"""
Test that Pareto trace events include config_version and config_source
======================================================================

Verify that pareto_debug contains config_version/config_source,
and that TraceEvents emitted by emit_pareto_debug_events also contain them.
"""

from __future__ import annotations

from datetime import datetime, timezone

from po_core.domain.context import Context
from po_core.domain.keys import PO_CORE, PARETO_DEBUG
from po_core.domain.pareto_config import ParetoConfig
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.aggregator.pareto import ParetoAggregator
from po_core.trace.in_memory import InMemoryTracer
from po_core.trace.pareto_events import emit_pareto_debug_events


def _make_ctx(request_id: str = "test-123") -> Context:
    """Helper to create a Context for testing."""
    return Context(
        request_id=request_id,
        created_at=datetime.now(timezone.utc),
        user_input="test input",
    )


def test_pareto_debug_contains_config_version_and_source():
    """ParetoAggregator embeds config_version and config_source in pareto_debug."""
    cfg = SafetyModeConfig(warn=0.6, critical=0.9, missing_mode=SafetyMode.WARN)
    pareto_cfg = ParetoConfig.defaults()

    agg = ParetoAggregator(mode_config=cfg, config=pareto_cfg)

    ctx = _make_ctx("test-123")
    tensors = TensorSnapshot(version="v1", metrics={"freedom_pressure": 0.3})
    proposals = [
        Proposal(
            proposal_id="p1",
            action_type="answer",
            content="Hello world",
            confidence=0.8,
        ),
    ]

    winner = agg.aggregate(ctx, None, tensors, proposals)
    pc = winner.extra.get(PO_CORE, {})
    dbg = pc.get(PARETO_DEBUG, {})

    assert "config_version" in dbg
    assert dbg["config_version"] == "1"
    assert "config_source" in dbg
    assert dbg["config_source"] == "defaults"


def test_emit_pareto_debug_events_includes_config_version_source():
    """emit_pareto_debug_events emits config_version and config_source in all 3 events."""
    tracer = InMemoryTracer()
    ctx = _make_ctx("test-456")

    # Create a winner with pareto_debug
    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="Test",
        confidence=0.9,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    "mode": "normal",
                    "freedom_pressure": "0.3",
                    "config_version": "42",
                    "config_source": "file:/path/to/table.yaml",
                    "weights": {"safety": 0.25},
                    "front_size": 1,
                    "front": [{"proposal_id": "p1", "action_type": "answer", "scores": {}}],
                    "winner": {"proposal_id": "p1", "action_type": "answer"},
                    "conflicts": {"n": 0},
                },
            },
        },
    )

    emit_pareto_debug_events(tracer, ctx, winner)

    events = tracer.events
    assert len(events) == 3

    # All 3 events should have config_version and config_source
    for ev in events:
        assert ev.payload.get("config_version") == "42"
        assert ev.payload.get("config_source") == "file:/path/to/table.yaml"


def test_custom_pareto_config_version_propagates():
    """Custom ParetoConfig version propagates through to trace events."""
    from po_core.domain.pareto_config import ParetoWeights, ParetoTuning

    custom_cfg = ParetoConfig(
        weights_by_mode={
            SafetyMode.NORMAL: ParetoWeights(0.3, 0.3, 0.2, 0.1, 0.1),
            SafetyMode.WARN: ParetoWeights(0.5, 0.1, 0.2, 0.1, 0.1),
            SafetyMode.CRITICAL: ParetoWeights(0.7, 0.0, 0.2, 0.05, 0.05),
            SafetyMode.UNKNOWN: ParetoWeights(0.5, 0.1, 0.2, 0.1, 0.1),
        },
        tuning=ParetoTuning(brevity_max_len=1000),
        version=99,
        source="test:custom",
    )

    cfg = SafetyModeConfig(warn=0.6, critical=0.9, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(mode_config=cfg, config=custom_cfg)

    ctx = _make_ctx("test-789")
    tensors = TensorSnapshot(version="v1", metrics={"freedom_pressure": 0.3})
    proposals = [
        Proposal(
            proposal_id="p1",
            action_type="answer",
            content="Test content",
            confidence=0.8,
        ),
    ]

    winner = agg.aggregate(ctx, None, tensors, proposals)
    pc = winner.extra.get(PO_CORE, {})
    dbg = pc.get(PARETO_DEBUG, {})

    assert dbg["config_version"] == "99"
    assert dbg["config_source"] == "test:custom"
