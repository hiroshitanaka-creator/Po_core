"""
test_decision_events.py
=======================

decision_events helper のテスト:
- DecisionEmitted / SafetyOverrideApplied が正しく吐かれる
- raw content がログに載らない（漏洩耐性）
"""

from datetime import datetime, timezone

from po_core.domain.context import Context
from po_core.domain.keys import AUTHOR, PARETO_DEBUG, PO_CORE
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.trace.decision_events import (
    emit_decision_emitted,
    emit_safety_override_applied,
    proposal_fingerprint,
    verdict_summary,
)


class DummyTracer:
    """テスト用の簡易 Tracer"""

    def __init__(self):
        self.events = []

    def emit(self, ev):
        self.events.append(ev)


def test_decision_events_emit_and_do_not_log_raw_content():
    """DecisionEmitted / SafetyOverrideApplied が吐かれ、raw content は載らない"""
    tr = DummyTracer()
    ctx = Context("r1", datetime.now(timezone.utc), "x")

    cand = Proposal(
        "p1",
        "answer",
        "SECRET_SHOULD_NOT_BE_LOGGED",
        0.9,
        extra={PO_CORE: {AUTHOR: "A"}},
    )
    final = Proposal("p2", "refuse", "ok", 1.0, extra={PO_CORE: {AUTHOR: "system"}})

    v = SafetyVerdict(
        decision=Decision.REVISE,
        rule_ids=["WG.ACT.OUTGUARD.001"],
        reasons=["x"],
        required_changes=["y"],
        meta={"forced_action": "refuse"},
    )

    emit_safety_override_applied(
        tr,
        ctx,
        stage="action",
        reason="gate_revise",
        from_proposal=cand,
        to_proposal=final,
        verdict=v,
    )
    emit_decision_emitted(
        tr,
        ctx,
        stage="action",
        origin="safety_fallback",
        final=final,
        candidate=cand,
        gate_verdict=v,
        degraded=True,
    )

    types = [e.event_type for e in tr.events]
    assert "SafetyOverrideApplied" in types
    assert "DecisionEmitted" in types

    # raw content をpayloadに載せない（hash/lenのみ）
    for ev in tr.events:
        s = str(ev.payload)
        assert "SECRET_SHOULD_NOT_BE_LOGGED" not in s


def test_proposal_fingerprint_contains_required_fields():
    """proposal_fingerprint が必要なフィールドを含む"""
    p = Proposal(
        "p1",
        "answer",
        "テスト回答",
        0.85,
        extra={
            PO_CORE: {
                AUTHOR: "aristotle",
                "freedom_pressure": "0.3",
                "policy": {"decision": "allow", "score": "1.000"},
                "trace_quality": {"author_reliability": "0.950"},
            }
        },
    )

    fp = proposal_fingerprint(p)

    assert fp["proposal_id"] == "p1"
    assert fp["action_type"] == "answer"
    assert fp["confidence"] == 0.85
    assert fp["content_len"] > 0
    assert len(fp["content_hash"]) == 10
    assert fp["author"] == "aristotle"
    assert fp["policy_score"] == "1.000"
    assert fp["author_reliability"] == "0.950"
    # raw content は含まれない
    assert "テスト回答" not in str(fp)


def test_verdict_summary_contains_required_fields():
    """verdict_summary が必要なフィールドを含む"""
    v = SafetyVerdict(
        decision=Decision.REJECT,
        rule_ids=["R1", "R2", "R3"],
        reasons=["reason1", "reason2"],
        required_changes=["change1"],
        meta={"key": "value"},
    )

    s = verdict_summary(v)

    assert s["decision"] == "reject"
    assert s["rule_ids"] == ["R1", "R2", "R3"]
    assert s["required_changes_n"] == 1
    assert s["reasons_n"] == 2
    assert s["meta"] == {"key": "value"}


def test_emit_decision_emitted_without_candidate():
    """candidate なしでも DecisionEmitted が吐ける（intent gate fallback 用）"""
    tr = DummyTracer()
    ctx = Context("r2", datetime.now(timezone.utc), "x")

    final = Proposal("p1", "refuse", "blocked", 1.0)

    emit_decision_emitted(
        tr,
        ctx,
        stage="intent",
        origin="intent_gate_fallback",
        final=final,
        candidate=None,
        gate_verdict=None,
        degraded=True,
    )

    assert len(tr.events) == 1
    ev = tr.events[0]
    assert ev.event_type == "DecisionEmitted"
    assert ev.payload["candidate"] is None
    assert ev.payload["stage"] == "intent"
    assert ev.payload["degraded"] is True


def test_emit_decision_emitted_pareto_origin():
    """Pareto origin で DecisionEmitted が吐ける（正常経路）"""
    tr = DummyTracer()
    ctx = Context("r3", datetime.now(timezone.utc), "x")

    final = Proposal("p1", "answer", "回答", 0.9)
    v = SafetyVerdict(
        decision=Decision.ALLOW, rule_ids=[], reasons=[], required_changes=[], meta={}
    )

    emit_decision_emitted(
        tr,
        ctx,
        stage="action",
        origin="pareto",
        final=final,
        candidate=final,
        gate_verdict=v,
        degraded=False,
    )

    assert len(tr.events) == 1
    ev = tr.events[0]
    assert ev.event_type == "DecisionEmitted"
    assert ev.payload["origin"] == "pareto"
    assert ev.payload["degraded"] is False
    assert ev.payload["gate"]["decision"] == "allow"


def test_safety_override_applied_contains_from_to():
    """SafetyOverrideApplied が from/to を含む"""
    tr = DummyTracer()
    ctx = Context("r4", datetime.now(timezone.utc), "x")

    from_p = Proposal("p1", "answer", "危険な回答", 0.9)
    to_p = Proposal("p2", "refuse", "拒否", 1.0)
    v = SafetyVerdict(
        decision=Decision.REJECT,
        rule_ids=["R1"],
        reasons=["危険"],
        required_changes=[],
        meta={},
    )

    emit_safety_override_applied(
        tr,
        ctx,
        stage="action",
        reason="gate_reject",
        from_proposal=from_p,
        to_proposal=to_p,
        verdict=v,
    )

    assert len(tr.events) == 1
    ev = tr.events[0]
    assert ev.event_type == "SafetyOverrideApplied"
    assert ev.payload["from"]["proposal_id"] == "p1"
    assert ev.payload["to"]["proposal_id"] == "p2"
    assert ev.payload["gate"]["decision"] == "reject"
    assert ev.payload["reason"] == "gate_reject"


def test_emit_decision_emitted_variant_main():
    """variant='main' が DecisionEmitted に含まれる"""
    tr = DummyTracer()
    ctx = Context("r5", datetime.now(timezone.utc), "x")

    final = Proposal("p1", "answer", "回答", 0.9)

    emit_decision_emitted(
        tr,
        ctx,
        variant="main",
        stage="action",
        origin="pareto",
        final=final,
        candidate=final,
        degraded=False,
    )

    assert len(tr.events) == 1
    ev = tr.events[0]
    assert ev.payload["variant"] == "main"


def test_emit_decision_emitted_variant_shadow():
    """variant='shadow' が DecisionEmitted に含まれる"""
    tr = DummyTracer()
    ctx = Context("r6", datetime.now(timezone.utc), "x")

    final = Proposal("p1", "answer", "回答", 0.9)

    emit_decision_emitted(
        tr,
        ctx,
        variant="shadow",
        stage="action",
        origin="pareto_shadow",
        final=final,
        candidate=final,
        degraded=False,
    )

    assert len(tr.events) == 1
    ev = tr.events[0]
    assert ev.payload["variant"] == "shadow"


def test_emit_safety_override_applied_variant():
    """variant が SafetyOverrideApplied に含まれる"""
    tr = DummyTracer()
    ctx = Context("r7", datetime.now(timezone.utc), "x")

    from_p = Proposal("p1", "answer", "回答", 0.9)
    to_p = Proposal("p2", "refuse", "拒否", 1.0)
    v = SafetyVerdict(
        decision=Decision.REJECT,
        rule_ids=["R1"],
        reasons=[],
        required_changes=[],
        meta={},
    )

    emit_safety_override_applied(
        tr,
        ctx,
        variant="shadow",
        stage="action",
        reason="gate_reject",
        from_proposal=from_p,
        to_proposal=to_p,
        verdict=v,
    )

    assert len(tr.events) == 1
    ev = tr.events[0]
    assert ev.payload["variant"] == "shadow"


def test_proposal_fingerprint_includes_pareto_config():
    """proposal_fingerprint に pareto_config_version/source が含まれる"""
    p = Proposal(
        "p1",
        "answer",
        "回答",
        0.9,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    "config_version": "42",
                    "config_source": "file:/path/to/shadow.yaml",
                }
            }
        },
    )

    fp = proposal_fingerprint(p)

    assert fp["pareto_config_version"] == "42"
    assert fp["pareto_config_source"] == "file:/path/to/shadow.yaml"


def test_emit_decision_emitted_pareto_config_from_candidate():
    """DecisionEmitted が candidate から pareto config を抽出する"""
    tr = DummyTracer()
    ctx = Context("r8", datetime.now(timezone.utc), "x")

    candidate = Proposal(
        "p1",
        "answer",
        "回答",
        0.9,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    "config_version": "99",
                    "config_source": "test:source",
                }
            }
        },
    )
    final = Proposal("p2", "answer", "最終", 1.0)

    emit_decision_emitted(
        tr,
        ctx,
        variant="main",
        stage="action",
        origin="pareto",
        final=final,
        candidate=candidate,
        degraded=False,
    )

    assert len(tr.events) == 1
    ev = tr.events[0]
    assert ev.payload["pareto_config_version"] == "99"
    assert ev.payload["pareto_config_source"] == "test:source"
