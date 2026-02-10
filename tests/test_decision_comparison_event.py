"""
test_decision_comparison_event.py
==================================

Shadow Pareto A/B comparison event のテスト:
- DecisionComparisonComputed が正しく吐かれる
- raw content がログに載らない（漏洩耐性）
- diff フィールドが正しく計算される
"""

from datetime import datetime, timezone

from po_core.domain.context import Context
from po_core.domain.keys import PARETO_DEBUG, PO_CORE
from po_core.domain.proposal import Proposal
from po_core.trace.decision_compare import emit_decision_comparison


class DummyTracer:
    """テスト用の簡易 Tracer"""

    def __init__(self):
        self.events = []

    def emit(self, ev):
        self.events.append(ev)


def test_emit_decision_comparison_emits_event():
    """emit_decision_comparison が DecisionComparisonComputed を吐く"""
    tr = DummyTracer()
    ctx = Context("r1", datetime.now(timezone.utc), "x")

    main_cand = Proposal(
        "p1_main",
        "answer",
        "Main answer",
        0.9,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {"config_version": "1", "config_source": "defaults"}
            }
        },
    )
    main_final = Proposal(
        "p1_main",
        "answer",
        "Main answer",
        0.9,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {"config_version": "1", "config_source": "defaults"}
            }
        },
    )
    shadow_cand = Proposal(
        "p2_shadow",
        "refuse",
        "Shadow refuse",
        1.0,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    "config_version": "2",
                    "config_source": "file:/shadow.yaml",
                }
            }
        },
    )
    shadow_final = Proposal(
        "p2_shadow",
        "refuse",
        "Shadow refuse",
        1.0,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    "config_version": "2",
                    "config_source": "file:/shadow.yaml",
                }
            }
        },
    )

    emit_decision_comparison(
        tr,
        ctx,
        main_candidate=main_cand,
        main_final=main_final,
        shadow_candidate=shadow_cand,
        shadow_final=shadow_final,
    )

    assert len(tr.events) == 1
    ev = tr.events[0]
    assert ev.event_type == "DecisionComparisonComputed"
    assert ev.correlation_id == "r1"


def test_decision_comparison_does_not_log_raw_content():
    """DecisionComparisonComputed が raw content を載せない"""
    tr = DummyTracer()
    ctx = Context("r2", datetime.now(timezone.utc), "x")

    main_cand = Proposal(
        "p1", "answer", "SECRET_MAIN_CONTENT_SHOULD_NOT_BE_LOGGED", 0.9
    )
    main_final = Proposal(
        "p1", "answer", "SECRET_MAIN_CONTENT_SHOULD_NOT_BE_LOGGED", 0.9
    )
    shadow_cand = Proposal(
        "p2", "refuse", "SECRET_SHADOW_CONTENT_SHOULD_NOT_BE_LOGGED", 1.0
    )
    shadow_final = Proposal(
        "p2", "refuse", "SECRET_SHADOW_CONTENT_SHOULD_NOT_BE_LOGGED", 1.0
    )

    emit_decision_comparison(
        tr,
        ctx,
        main_candidate=main_cand,
        main_final=main_final,
        shadow_candidate=shadow_cand,
        shadow_final=shadow_final,
    )

    ev = tr.events[0]
    s = str(ev.payload)
    assert "SECRET_MAIN_CONTENT_SHOULD_NOT_BE_LOGGED" not in s
    assert "SECRET_SHADOW_CONTENT_SHOULD_NOT_BE_LOGGED" not in s


def test_decision_comparison_diff_fields():
    """DecisionComparisonComputed の diff フィールドが正しく計算される"""
    tr = DummyTracer()
    ctx = Context("r3", datetime.now(timezone.utc), "x")

    main_cand = Proposal(
        "p1",
        "answer",
        "Main",
        0.9,
        extra={
            PO_CORE: {
                PARETO_DEBUG: {"config_version": "1", "config_source": "defaults"}
            }
        },
    )
    main_final = Proposal("p1", "answer", "Main", 0.9)
    shadow_cand = Proposal(
        "p2",
        "refuse",
        "Shadow",
        1.0,  # action_type が異なる
        extra={
            PO_CORE: {
                PARETO_DEBUG: {
                    "config_version": "99",
                    "config_source": "file:/shadow.yaml",
                }
            }
        },
    )
    shadow_final = Proposal("p2", "refuse", "Shadow", 1.0)

    emit_decision_comparison(
        tr,
        ctx,
        main_candidate=main_cand,
        main_final=main_final,
        shadow_candidate=shadow_cand,
        shadow_final=shadow_final,
    )

    ev = tr.events[0]
    diff = ev.payload.get("diff", {})

    # action_type が異なるので changed=True
    assert diff.get("candidate_action_changed") is True
    assert diff.get("final_action_changed") is True

    # config が異なる
    assert diff.get("main_config_version") == "1"
    assert diff.get("shadow_config_version") == "99"
    assert diff.get("main_config_source") == "defaults"
    assert diff.get("shadow_config_source") == "file:/shadow.yaml"


def test_decision_comparison_same_proposals():
    """main と shadow が同じ Proposal を選んだ場合"""
    tr = DummyTracer()
    ctx = Context("r4", datetime.now(timezone.utc), "x")

    # 同じ proposal_id, action_type, content
    main_cand = Proposal("p1", "answer", "Same", 0.9)
    main_final = Proposal("p1", "answer", "Same", 0.9)
    shadow_cand = Proposal("p1", "answer", "Same", 0.9)
    shadow_final = Proposal("p1", "answer", "Same", 0.9)

    emit_decision_comparison(
        tr,
        ctx,
        main_candidate=main_cand,
        main_final=main_final,
        shadow_candidate=shadow_cand,
        shadow_final=shadow_final,
    )

    ev = tr.events[0]
    diff = ev.payload.get("diff", {})

    # すべて同じなので changed=False
    assert diff.get("candidate_action_changed") is False
    assert diff.get("candidate_content_changed") is False
    assert diff.get("final_action_changed") is False
    assert diff.get("final_content_changed") is False


def test_decision_comparison_contains_main_and_shadow():
    """DecisionComparisonComputed が main/shadow の情報を含む"""
    tr = DummyTracer()
    ctx = Context("r5", datetime.now(timezone.utc), "x")

    main_cand = Proposal("p1_main", "answer", "Main", 0.9)
    main_final = Proposal("p1_main", "answer", "Main", 0.9)
    shadow_cand = Proposal("p2_shadow", "refuse", "Shadow", 1.0)
    shadow_final = Proposal("p2_shadow", "refuse", "Shadow", 1.0)

    emit_decision_comparison(
        tr,
        ctx,
        main_candidate=main_cand,
        main_final=main_final,
        shadow_candidate=shadow_cand,
        shadow_final=shadow_final,
    )

    ev = tr.events[0]
    payload = ev.payload

    # main/shadow キーが存在
    assert "main" in payload
    assert "shadow" in payload

    # candidate/final が含まれる
    assert "candidate" in payload["main"]
    assert "final" in payload["main"]
    assert "candidate" in payload["shadow"]
    assert "final" in payload["shadow"]

    # proposal_id が正しい
    assert payload["main"]["candidate"]["proposal_id"] == "p1_main"
    assert payload["shadow"]["candidate"]["proposal_id"] == "p2_shadow"
