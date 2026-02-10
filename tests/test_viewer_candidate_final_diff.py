"""
test_viewer_candidate_final_diff.py
===================================

viewer が DecisionEmitted / SafetyOverrideApplied を正しくレンダリングするかのテスト
"""

from datetime import datetime, timezone

from po_core.domain.trace_event import TraceEvent
from po_core.viewer.decision_report_md import render_markdown


def test_viewer_renders_candidate_to_final_section():
    """DecisionEmitted から Candidate → Emitted セクションが生成される"""
    rid = "r1"
    events = [
        TraceEvent.now(
            "DecisionEmitted",
            rid,
            {
                "stage": "action",
                "origin": "safety_fallback",
                "degraded": True,
                "candidate": {
                    "proposal_id": "p1",
                    "action_type": "answer",
                    "content_len": 100,
                    "content_hash": "aaaa123456",
                    "policy_score": "0.100",
                    "author_reliability": "0.900",
                },
                "final": {
                    "proposal_id": "p2",
                    "action_type": "refuse",
                    "content_len": 20,
                    "content_hash": "bbbb789012",
                    "policy_score": "1.000",
                    "author_reliability": "1.000",
                },
                "gate": {
                    "decision": "allow",
                    "rule_ids": [],
                },
            },
        ),
        TraceEvent.now(
            "SafetyOverrideApplied",
            rid,
            {
                "stage": "action",
                "reason": "gate_revise",
                "gate": {
                    "decision": "revise",
                    "rule_ids": ["WG.ACT.OUTGUARD.001"],
                },
            },
        ),
    ]

    md = render_markdown(events)

    assert "Candidate → Emitted" in md
    assert "SafetyOverrideApplied" in md
    assert "p1" in md
    assert "p2" in md
    assert "answer" in md
    assert "refuse" in md


def test_viewer_renders_without_override():
    """SafetyOverrideApplied がなくても DecisionEmitted がレンダリングされる"""
    rid = "r2"
    events = [
        TraceEvent.now(
            "DecisionEmitted",
            rid,
            {
                "stage": "action",
                "origin": "pareto",
                "degraded": False,
                "candidate": {
                    "proposal_id": "p1",
                    "action_type": "answer",
                    "content_len": 50,
                    "content_hash": "cccc",
                },
                "final": {
                    "proposal_id": "p1",
                    "action_type": "answer",
                    "content_len": 50,
                    "content_hash": "cccc",
                },
                "gate": {
                    "decision": "allow",
                    "rule_ids": [],
                },
            },
        ),
    ]

    md = render_markdown(events)

    assert "Candidate → Emitted" in md
    assert "pareto" in md
    assert "degraded: `False`" in md
    assert "SafetyOverrideApplied" not in md


def test_viewer_renders_intent_fallback():
    """意図段階の fallback でも DecisionEmitted がレンダリングされる"""
    rid = "r3"
    events = [
        TraceEvent.now(
            "DecisionEmitted",
            rid,
            {
                "stage": "intent",
                "origin": "intent_gate_fallback",
                "degraded": True,
                "candidate": None,
                "final": {
                    "proposal_id": "fb1",
                    "action_type": "refuse",
                    "content_len": 30,
                    "content_hash": "dddd",
                },
                "gate": {
                    "decision": "allow",
                    "rule_ids": [],
                },
            },
        ),
    ]

    md = render_markdown(events)

    assert "Candidate → Emitted" in md
    assert "intent_gate_fallback" in md
    assert "fb1" in md


def test_viewer_renders_gate_info():
    """gate情報（decision/rule_ids）がレンダリングされる"""
    rid = "r4"
    events = [
        TraceEvent.now(
            "DecisionEmitted",
            rid,
            {
                "stage": "action",
                "origin": "safety_fallback",
                "degraded": True,
                "candidate": {"proposal_id": "p1"},
                "final": {"proposal_id": "p2"},
                "gate": {
                    "decision": "allow",
                    "rule_ids": ["R1", "R2"],
                },
            },
        ),
        TraceEvent.now(
            "SafetyOverrideApplied",
            rid,
            {
                "stage": "action",
                "reason": "gate_reject",
                "gate": {
                    "decision": "reject",
                    "rule_ids": ["WG.ACT.001", "WG.ACT.002"],
                },
            },
        ),
    ]

    md = render_markdown(events)

    assert "gate.decision: `allow`" in md
    assert "gate.decision: `reject`" in md
    assert "WG.ACT.001" in md


def test_viewer_renders_policy_score_and_author_rel():
    """policy_score と author_reliability がテーブルに含まれる"""
    rid = "r5"
    events = [
        TraceEvent.now(
            "DecisionEmitted",
            rid,
            {
                "stage": "action",
                "origin": "pareto",
                "degraded": False,
                "candidate": {
                    "proposal_id": "p1",
                    "action_type": "answer",
                    "content_len": 100,
                    "content_hash": "aaaa",
                    "policy_score": "0.850",
                    "author_reliability": "0.920",
                },
                "final": {
                    "proposal_id": "p1",
                    "action_type": "answer",
                    "content_len": 100,
                    "content_hash": "aaaa",
                    "policy_score": "0.850",
                    "author_reliability": "0.920",
                },
            },
        ),
    ]

    md = render_markdown(events)

    assert "0.850" in md
    assert "0.920" in md
