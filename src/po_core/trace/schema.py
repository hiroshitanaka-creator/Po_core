"""
schema.py - TraceEvent スキーマ検証（契約凍結）
==============================================

イベントが増えても viewer/監査が壊れないための契約。
CIで折る（"思想"じゃなく工学で守る）。

Usage:
    from po_core.trace.schema import validate_events

    problems = validate_events(events)
    assert problems == {}, f"Schema violations: {problems}"

DEPENDENCY RULES:
- domain.trace_event のみ依存
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, Sequence

from po_core.domain.trace_event import TraceEvent


@dataclass(frozen=True)
class EventSpec:
    """TraceEvent の required keys 仕様"""

    event_type: str
    required_keys: Sequence[str]


# 主要イベントの契約（これを崩したら CI が折る）
SPECS: List[EventSpec] = [
    # Decision events
    EventSpec("DecisionEmitted", ["stage", "origin", "degraded", "final"]),
    EventSpec("SafetyOverrideApplied", ["stage", "reason", "from", "to", "gate"]),
    # Pareto events
    EventSpec("ParetoFrontComputed", ["mode", "weights", "front_size", "front"]),
    EventSpec("ParetoWinnerSelected", ["mode", "winner"]),
    EventSpec("ConflictSummaryComputed", ["n", "kinds"]),
    # Policy events
    EventSpec("PolicyPrecheckSummary", ["allow", "revise", "reject"]),
    # Safety events
    EventSpec("SafetyJudged:Intention", ["decision", "rule_ids"]),
    EventSpec("SafetyJudged:Action", ["decision", "rule_ids"]),
    # Pipeline events
    EventSpec("MemorySnapshotted", ["items"]),
    EventSpec("TensorComputed", ["metrics"]),
    EventSpec("IntentGenerated", []),  # payload は任意
    EventSpec("AggregateCompleted", ["proposal_id", "action_type"]),
]


def _get_spec(event_type: str) -> EventSpec | None:
    """Get spec for event type (or None if not registered)."""
    for s in SPECS:
        if s.event_type == event_type:
            return s
    return None


def validate_event(ev: TraceEvent) -> List[str]:
    """
    Validate a single TraceEvent against its spec.

    Args:
        ev: TraceEvent to validate

    Returns:
        List of issues (empty if valid)
    """
    issues: List[str] = []
    spec = _get_spec(ev.event_type)
    if spec is None:
        # 未登録イベントは一旦許す（増やしながら凍結していく）
        return issues

    payload = ev.payload if isinstance(ev.payload, Mapping) else {}
    for k in spec.required_keys:
        if k not in payload:
            issues.append(f"missing '{k}'")

    return issues


def validate_events(events: Sequence[TraceEvent]) -> Dict[str, List[str]]:
    """
    Validate multiple TraceEvents.

    Args:
        events: Sequence of TraceEvents to validate

    Returns:
        Dict of {event_id: issues} for events with issues (empty if all valid)
    """
    out: Dict[str, List[str]] = {}
    for e in events:
        iss = validate_event(e)
        if iss:
            key = f"{e.event_type}@{e.correlation_id}"
            out[key] = iss
    return out


__all__ = ["EventSpec", "SPECS", "validate_event", "validate_events"]
