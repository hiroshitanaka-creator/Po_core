"""
Pipeline View — 10-step pipeline progression from TraceEvents
==============================================================

Renders a clear step-by-step view of the run_turn pipeline using
only TraceEvent data (no implementation dependencies).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from po_core.domain.trace_event import TraceEvent


# Pipeline step definitions: (step_number, event_type, label)
PIPELINE_STEPS = [
    (1, "MemorySnapshotted", "Memory Read"),
    (2, "TensorComputed", "Tensor Compute"),
    (3, "IntentGenerated", "Solar Will"),
    (4, "SafetyJudged:Intention", "Intention Gate"),
    (5, "PhilosophersSelected", "Philosopher Select"),
    (6, "PhilosopherResult", "Party Machine"),
    (7, "PolicyPrecheckSummary", "Policy Precheck"),
    (8, "AggregateCompleted", "Pareto Aggregate"),
    (9, "DecisionEmitted", "Action Gate / Decision"),
    (10, "DecisionComparisonComputed", "Shadow A/B (optional)"),
]


def _find_all(events: Sequence[TraceEvent], event_type: str) -> List[TraceEvent]:
    return [e for e in events if e.event_type == event_type]


def _find_first(events: Sequence[TraceEvent], event_type: str) -> Optional[TraceEvent]:
    for e in events:
        if e.event_type == event_type:
            return e
    return None


def _step_detail(step_num: int, event_type: str, events: Sequence[TraceEvent]) -> str:
    """Extract a one-line detail string for a pipeline step."""
    found = _find_all(events, event_type)
    if not found:
        return ""

    ev = found[0]
    p = ev.payload

    if event_type == "MemorySnapshotted":
        return f"items={p.get('items', 0)}"
    elif event_type == "TensorComputed":
        metrics = p.get("metrics", [])
        return f"metrics=[{', '.join(str(m) for m in metrics)}]"
    elif event_type == "IntentGenerated":
        goals = p.get("goals", [])
        return f"goals={goals}" if goals else ""
    elif event_type == "SafetyJudged:Intention":
        return f"decision={p.get('decision', '?')}"
    elif event_type == "PhilosophersSelected":
        return f"mode={p.get('mode')}, n={p.get('n')}, cost={p.get('cost_total')}"
    elif event_type == "PhilosopherResult":
        n = len(found)
        timed_out = sum(1 for e in found if e.payload.get("timed_out"))
        errors = sum(1 for e in found if e.payload.get("error"))
        detail = f"n={n}"
        if timed_out:
            detail += f", timed_out={timed_out}"
        if errors:
            detail += f", errors={errors}"
        return detail
    elif event_type == "PolicyPrecheckSummary":
        return f"allow={p.get('allow', 0)}, revise={p.get('revise', 0)}, reject={p.get('reject', 0)}"
    elif event_type == "AggregateCompleted":
        return f"winner={p.get('proposal_id', '?')[:24]}"
    elif event_type == "DecisionEmitted":
        last = found[-1]
        lp = last.payload
        degraded = lp.get("degraded", False)
        origin = lp.get("origin", "?")
        return f"origin={origin}, degraded={degraded}"
    elif event_type == "DecisionComparisonComputed":
        diff = p.get("diff", {})
        changed = diff.get("final_content_changed", False)
        return f"content_changed={changed}"
    return ""


def render_pipeline_markdown(events: Sequence[TraceEvent]) -> str:
    """
    Render 10-step pipeline progression as Markdown.

    Args:
        events: TraceEvents from a pipeline run

    Returns:
        Markdown string showing pipeline step status
    """
    ev = list(events)
    if not ev:
        return "## Pipeline\n\nNo events."

    lines: List[str] = []
    lines.append("## Pipeline Progression")
    lines.append("")
    lines.append("| Step | Stage | Status | Detail |")
    lines.append("|---:|---|---|---|")

    event_types_present = {e.event_type for e in ev}

    for step_num, event_type, label in PIPELINE_STEPS:
        if event_type in event_types_present:
            detail = _step_detail(step_num, event_type, ev)
            status = "ok"
            # Check for degradation or blocking
            if event_type == "SafetyJudged:Intention":
                e = _find_first(ev, event_type)
                if e and e.payload.get("decision") != "allow":
                    status = "blocked"
            elif event_type == "DecisionEmitted":
                last = _find_all(ev, event_type)[-1]
                if last.payload.get("degraded"):
                    status = "degraded"
            lines.append(f"| {step_num} | {label} | {status} | {detail} |")
        else:
            # Step 10 (shadow) is optional
            if step_num == 10:
                lines.append(f"| {step_num} | {label} | skipped | |")
            else:
                lines.append(f"| {step_num} | {label} | - | |")

    lines.append("")
    return "\n".join(lines)


def render_pipeline_text(events: Sequence[TraceEvent]) -> str:
    """
    Render 10-step pipeline progression as plain text with box-drawing.

    Args:
        events: TraceEvents from a pipeline run

    Returns:
        Text string showing pipeline step status
    """
    ev = list(events)
    if not ev:
        return "Pipeline: No events."

    event_types_present = {e.event_type for e in ev}
    lines: List[str] = []
    lines.append("Pipeline Progression")
    lines.append("=" * 60)

    for step_num, event_type, label in PIPELINE_STEPS:
        if event_type in event_types_present:
            detail = _step_detail(step_num, event_type, ev)
            marker = "[ok]"
            if event_type == "SafetyJudged:Intention":
                e = _find_first(ev, event_type)
                if e and e.payload.get("decision") != "allow":
                    marker = "[BLOCKED]"
            elif event_type == "DecisionEmitted":
                last = _find_all(ev, event_type)[-1]
                if last.payload.get("degraded"):
                    marker = "[DEGRADED]"
            detail_str = f"  ({detail})" if detail else ""
            lines.append(f"  {step_num:2d}. {label:<24s} {marker}{detail_str}")
        else:
            if step_num == 10:
                lines.append(f"  {step_num:2d}. {label:<24s} [skipped]")
            else:
                lines.append(f"  {step_num:2d}. {label:<24s} [-]")

    return "\n".join(lines)


__all__ = ["render_pipeline_markdown", "render_pipeline_text", "PIPELINE_STEPS"]
