"""
test_trace_schema_contract.py
=============================

TraceEvent スキーマ契約のテスト。
CI で折る（契約違反は即検出）。
"""

from datetime import datetime, timezone

from po_core.domain.trace_event import TraceEvent
from po_core.trace.schema import validate_event, validate_events, SPECS


def test_decision_emitted_valid():
    """DecisionEmitted が必須キーを持っていれば valid"""
    ev = TraceEvent.now("DecisionEmitted", "r1", {
        "stage": "action",
        "origin": "pareto",
        "degraded": False,
        "final": {"proposal_id": "p1"},
    })
    issues = validate_event(ev)
    assert issues == []


def test_decision_emitted_missing_keys():
    """DecisionEmitted に必須キーが欠けていれば検出"""
    ev = TraceEvent.now("DecisionEmitted", "r1", {
        "stage": "action",
        # missing: origin, degraded, final
    })
    issues = validate_event(ev)
    assert "missing 'origin'" in issues
    assert "missing 'degraded'" in issues
    assert "missing 'final'" in issues


def test_safety_override_applied_valid():
    """SafetyOverrideApplied が必須キーを持っていれば valid"""
    ev = TraceEvent.now("SafetyOverrideApplied", "r1", {
        "stage": "action",
        "reason": "gate_revise",
        "from": {"proposal_id": "p1"},
        "to": {"proposal_id": "p2"},
        "gate": {"decision": "revise"},
    })
    issues = validate_event(ev)
    assert issues == []


def test_pareto_front_computed_valid():
    """ParetoFrontComputed が必須キーを持っていれば valid"""
    ev = TraceEvent.now("ParetoFrontComputed", "r1", {
        "mode": "normal",
        "weights": {"safety": 0.25},
        "front_size": 3,
        "front": [],
    })
    issues = validate_event(ev)
    assert issues == []


def test_pareto_winner_selected_valid():
    """ParetoWinnerSelected が必須キーを持っていれば valid"""
    ev = TraceEvent.now("ParetoWinnerSelected", "r1", {
        "mode": "normal",
        "winner": {"proposal_id": "p1"},
    })
    issues = validate_event(ev)
    assert issues == []


def test_conflict_summary_computed_valid():
    """ConflictSummaryComputed が必須キーを持っていれば valid"""
    ev = TraceEvent.now("ConflictSummaryComputed", "r1", {
        "n": 0,
        "kinds": "",
    })
    issues = validate_event(ev)
    assert issues == []


def test_policy_precheck_summary_valid():
    """PolicyPrecheckSummary が必須キーを持っていれば valid"""
    ev = TraceEvent.now("PolicyPrecheckSummary", "r1", {
        "allow": 3,
        "revise": 1,
        "reject": 0,
    })
    issues = validate_event(ev)
    assert issues == []


def test_unregistered_event_passes():
    """未登録イベントは許可される（増やしながら凍結していく）"""
    ev = TraceEvent.now("CustomEvent", "r1", {
        "anything": "goes",
    })
    issues = validate_event(ev)
    assert issues == []


def test_validate_events_multiple():
    """複数イベントをまとめて検証"""
    events = [
        TraceEvent.now("DecisionEmitted", "r1", {
            "stage": "action",
            "origin": "pareto",
            "degraded": False,
            "final": {},
        }),
        TraceEvent.now("ParetoFrontComputed", "r1", {
            # missing: mode, weights
            "front_size": 2,
            "front": [],
        }),
        TraceEvent.now("SafetyJudged:Intention", "r1", {
            "decision": "allow",
            "rule_ids": [],
        }),
    ]
    problems = validate_events(events)
    assert "ParetoFrontComputed@r1" in problems
    assert "missing 'mode'" in problems["ParetoFrontComputed@r1"]
    assert "missing 'weights'" in problems["ParetoFrontComputed@r1"]
    assert "DecisionEmitted@r1" not in problems
    assert "SafetyJudged:Intention@r1" not in problems


def test_all_specs_have_event_type():
    """全ての SPECS が event_type を持っている"""
    for spec in SPECS:
        assert spec.event_type != ""


def test_specs_cover_main_events():
    """主要イベントが SPECS でカバーされている"""
    event_types = {s.event_type for s in SPECS}
    assert "DecisionEmitted" in event_types
    assert "SafetyOverrideApplied" in event_types
    assert "ParetoFrontComputed" in event_types
    assert "ParetoWinnerSelected" in event_types
    assert "ConflictSummaryComputed" in event_types
