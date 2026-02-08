"""
test_emit_pareto_debug_events.py
================================

emit_pareto_debug_events helper が必ず 3 イベントを吐くことを検証する。
"""

from datetime import datetime, timezone

from po_core.domain.context import Context
from po_core.domain.keys import (
    CONFLICTS,
    FREEDOM_PRESSURE,
    FRONT,
    MODE,
    PARETO_DEBUG,
    PO_CORE,
    WEIGHTS,
    WINNER,
)
from po_core.domain.proposal import Proposal
from po_core.trace.pareto_events import emit_pareto_debug_events


class DummyTracer:
    """テスト用の簡易 Tracer"""

    def __init__(self):
        self.events = []

    def emit(self, ev):
        self.events.append(ev)


def test_emit_pareto_debug_events_emits_three_events():
    """emit_pareto_debug_events が 3 イベントを吐く"""
    ctx = Context("r1", datetime.now(timezone.utc), "x")

    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="ok",
        confidence=0.8,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    MODE: "normal",
                    FREEDOM_PRESSURE: "0.2",
                    WEIGHTS: {"safety": 0.25, "freedom": 0.30},
                    "front_size": 2,
                    FRONT: [
                        {
                            "proposal_id": "p1",
                            "action_type": "answer",
                            "scores": {"safety": 1.0},
                            "content_len": 2,
                            "content_hash": "abcd123456",
                        },
                        {
                            "proposal_id": "p2",
                            "action_type": "ask_clarification",
                            "scores": {"safety": 0.8},
                            "content_len": 3,
                            "content_hash": "efgh789012",
                        },
                    ],
                    WINNER: {
                        "proposal_id": "p1",
                        "action_type": "answer",
                        "scores": {"safety": 1.0},
                    },
                    CONFLICTS: {
                        "n": 0,
                        "kinds": "",
                        "suggested_forced_action": "",
                        "top": [],
                    },
                }
            }
        },
    )

    tr = DummyTracer()
    emit_pareto_debug_events(tr, ctx, winner)

    types = [e.event_type for e in tr.events]
    assert "ConflictSummaryComputed" in types
    assert "ParetoFrontComputed" in types
    assert "ParetoWinnerSelected" in types
    assert len(tr.events) == 3


def test_emit_pareto_debug_events_no_payload():
    """pareto_debug が無い場合はイベントを吐かない"""
    ctx = Context("r2", datetime.now(timezone.utc), "x")

    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="ok",
        confidence=0.8,
        extra={},
    )

    tr = DummyTracer()
    emit_pareto_debug_events(tr, ctx, winner)

    assert len(tr.events) == 0


def test_emit_pareto_debug_events_conflict_summary_content():
    """ConflictSummaryComputed に conflicts 情報が含まれる"""
    ctx = Context("r3", datetime.now(timezone.utc), "x")

    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="ok",
        confidence=0.8,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    MODE: "warn",
                    FREEDOM_PRESSURE: "0.7",
                    WEIGHTS: {},
                    "front_size": 1,
                    FRONT: [],
                    WINNER: {},
                    CONFLICTS: {
                        "n": 2,
                        "kinds": "action_divergence",
                        "suggested_forced_action": "refuse",
                        "top": [{"id": "c1"}],
                    },
                }
            }
        },
    )

    tr = DummyTracer()
    emit_pareto_debug_events(tr, ctx, winner)

    conflict_ev = next(
        e for e in tr.events if e.event_type == "ConflictSummaryComputed"
    )
    assert conflict_ev.payload.get("n") == 2
    assert conflict_ev.payload.get("kinds") == "action_divergence"
    assert conflict_ev.payload.get(MODE) == "warn"


def test_emit_pareto_debug_events_pareto_front_content():
    """ParetoFrontComputed に front/weights 情報が含まれる"""
    ctx = Context("r4", datetime.now(timezone.utc), "x")

    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="ok",
        confidence=0.8,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    MODE: "critical",
                    FREEDOM_PRESSURE: "0.95",
                    WEIGHTS: {"safety": 0.55, "freedom": 0.00},
                    "front_size": 3,
                    FRONT: [
                        {"proposal_id": "p1"},
                        {"proposal_id": "p2"},
                        {"proposal_id": "p3"},
                    ],
                    WINNER: {},
                    CONFLICTS: {},
                }
            }
        },
    )

    tr = DummyTracer()
    emit_pareto_debug_events(tr, ctx, winner)

    front_ev = next(e for e in tr.events if e.event_type == "ParetoFrontComputed")
    assert front_ev.payload.get("front_size") == 3
    assert len(front_ev.payload.get(FRONT, [])) == 3
    assert front_ev.payload.get(WEIGHTS, {}).get("safety") == 0.55


def test_emit_pareto_debug_events_winner_selected_content():
    """ParetoWinnerSelected に winner 情報が含まれる"""
    ctx = Context("r5", datetime.now(timezone.utc), "x")

    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="ok",
        confidence=0.8,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    MODE: "normal",
                    FREEDOM_PRESSURE: "0.1",
                    WEIGHTS: {},
                    "front_size": 1,
                    FRONT: [],
                    WINNER: {
                        "proposal_id": "p1",
                        "action_type": "answer",
                        "content_hash": "abc1234567",
                    },
                    CONFLICTS: {},
                }
            }
        },
    )

    tr = DummyTracer()
    emit_pareto_debug_events(tr, ctx, winner)

    winner_ev = next(e for e in tr.events if e.event_type == "ParetoWinnerSelected")
    assert winner_ev.payload.get(WINNER, {}).get("proposal_id") == "p1"
    assert winner_ev.payload.get(WINNER, {}).get("action_type") == "answer"
    assert winner_ev.payload.get(MODE) == "normal"


def test_emit_pareto_debug_events_request_id_propagated():
    """各イベントに request_id が正しく伝播される"""
    ctx = Context("unique-request-123", datetime.now(timezone.utc), "x")

    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="ok",
        confidence=0.8,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    MODE: "normal",
                    FREEDOM_PRESSURE: "0.2",
                    WEIGHTS: {},
                    "front_size": 1,
                    FRONT: [],
                    WINNER: {},
                    CONFLICTS: {},
                }
            }
        },
    )

    tr = DummyTracer()
    emit_pareto_debug_events(tr, ctx, winner)

    for ev in tr.events:
        assert ev.correlation_id == "unique-request-123"


def test_emit_pareto_debug_events_variant_main():
    """variant='main' が全イベントに含まれる"""
    ctx = Context("r6", datetime.now(timezone.utc), "x")

    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="ok",
        confidence=0.8,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    MODE: "normal",
                    FREEDOM_PRESSURE: "0.2",
                    WEIGHTS: {},
                    "front_size": 1,
                    FRONT: [],
                    WINNER: {},
                    CONFLICTS: {},
                }
            }
        },
    )

    tr = DummyTracer()
    emit_pareto_debug_events(tr, ctx, winner, variant="main")

    assert len(tr.events) == 3
    for ev in tr.events:
        assert ev.payload.get("variant") == "main"


def test_emit_pareto_debug_events_variant_shadow():
    """variant='shadow' が全イベントに含まれる"""
    ctx = Context("r7", datetime.now(timezone.utc), "x")

    winner = Proposal(
        proposal_id="p1",
        action_type="answer",
        content="ok",
        confidence=0.8,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    MODE: "warn",
                    FREEDOM_PRESSURE: "0.6",
                    WEIGHTS: {"safety": 0.40},
                    "front_size": 1,
                    FRONT: [],
                    WINNER: {},
                    CONFLICTS: {},
                }
            }
        },
    )

    tr = DummyTracer()
    emit_pareto_debug_events(tr, ctx, winner, variant="shadow")

    assert len(tr.events) == 3
    for ev in tr.events:
        assert ev.payload.get("variant") == "shadow"
