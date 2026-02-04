"""
Decision Report (Markdown) - TraceEvent からレポート生成
=========================================================

viewer は TraceEvent のみを入力にする（実装依存を絶つ）。
Markdown で出力（CI でも差分が見える）。

DEPENDENCY RULES:
- domain.trace_event のみ依存
- ensemble/aggregator の実装詳細は見ない
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping

from po_core.domain.trace_event import TraceEvent


def _find(events: Iterable[TraceEvent], event_type: str) -> List[TraceEvent]:
    """Filter events by type."""
    return [e for e in events if e.event_type == event_type]


def render_markdown(events: Iterable[TraceEvent]) -> str:
    """
    Render TraceEvents as Markdown report.

    Args:
        events: Iterable of TraceEvents from a pipeline run

    Returns:
        Markdown-formatted decision report
    """
    ev = list(events)
    if not ev:
        return "# Po_core Decision Report\n\nNo events recorded."

    # Find specific event types
    sel = _find(ev, "ParetoWinnerSelected")
    front = _find(ev, "ParetoFrontComputed")
    conf = _find(ev, "ConflictSummaryComputed")
    pol = _find(ev, "PolicyPrecheckSummary")
    intent = _find(ev, "IntentGenerated")
    tensors = _find(ev, "TensorComputed")
    phsel = _find(ev, "PhilosophersSelected")
    aggr = _find(ev, "AggregateCompleted")

    lines: List[str] = []
    rid = ev[0].correlation_id if ev else "unknown"
    lines.append("# Po_core Decision Report")
    lines.append(f"- request_id: `{rid}`")
    lines.append("")

    # Tensors section
    if tensors:
        lines.append("## Tensors")
        payload = tensors[-1].payload
        lines.append(f"- metrics: {payload.get('metrics', [])}")
        lines.append(f"- version: {payload.get('version', 'unknown')}")
        lines.append("")

    # Intent section
    if intent:
        lines.append("## Solar Will / Intent")
        payload = intent[-1].payload
        lines.append(f"- meta: {payload}")
        lines.append("")

    # Battalion section
    if phsel:
        lines.append("## Battalion")
        p = phsel[-1].payload
        lines.append(f"- mode: {p.get('mode')}, n: {p.get('n')}, cost_total: {p.get('cost_total')}")
        lines.append(f"- covered_tags: {p.get('covered_tags')}")
        ids = p.get('ids', [])
        if ids:
            lines.append(f"- ids: {', '.join(str(i) for i in ids[:10])}{'...' if len(ids) > 10 else ''}")
        lines.append("")

    # Policy Precheck section
    if pol:
        lines.append("## Policy Precheck Summary")
        payload = pol[-1].payload
        lines.append(f"- allow: {payload.get('allow', 0)}")
        lines.append(f"- revise: {payload.get('revise', 0)}")
        lines.append(f"- reject: {payload.get('reject', 0)}")
        lines.append("")

    # Conflict Summary section
    if conf:
        lines.append("## Conflict Summary")
        c = conf[-1].payload
        lines.append(f"- n: {c.get('n')}, kinds: {c.get('kinds')}, suggested: {c.get('suggested_forced_action')}")
        top = c.get("top", [])
        if top:
            lines.append("")
            lines.append("| id | kind | severity | proposal_ids |")
            lines.append("|---|---:|---:|---|")
            for t in top:
                pids = t.get('proposal_ids', [])
                pids_str = ', '.join(str(p) for p in pids[:4])
                lines.append(f"| {t.get('id', '')} | {t.get('kind', '')} | {t.get('severity', '')} | {pids_str} |")
        lines.append("")

    # Pareto Front section
    if front:
        lines.append("## Pareto Front")
        f = front[-1].payload
        w = f.get("weights", {})
        lines.append(f"- weights: safety={w.get('safety', 0):.2f}, freedom={w.get('freedom', 0):.2f}, "
                     f"explain={w.get('explain', 0):.2f}, brevity={w.get('brevity', 0):.2f}, "
                     f"coherence={w.get('coherence', 0):.2f}")
        rows = f.get("front", [])
        if rows:
            lines.append("")
            lines.append("| proposal_id | action | safety | freedom | explain | brevity | coherence |")
            lines.append("|---|---|---:|---:|---:|---:|---:|")
            for r in rows[:10]:  # limit to 10 rows
                s = r.get("scores", {})
                lines.append(
                    f"| {r.get('proposal_id', '')[:20]} | {r.get('action_type', '')} | "
                    f"{s.get('safety', 0):.3f} | {s.get('freedom', 0):.3f} | "
                    f"{s.get('explain', 0):.3f} | {s.get('brevity', 0):.3f} | "
                    f"{s.get('coherence', 0):.3f} |"
                )
        lines.append("")

    # Winner section
    if sel:
        lines.append("## Winner")
        w = sel[-1].payload.get("winner", {})
        lines.append(f"- proposal_id: `{w.get('proposal_id', 'unknown')}`")
        lines.append(f"- action_type: `{w.get('action_type', 'unknown')}`")
        lines.append("")
    elif aggr:
        # Fallback to AggregateCompleted if no ParetoWinnerSelected
        lines.append("## Winner (from AggregateCompleted)")
        a = aggr[-1].payload
        lines.append(f"- proposal_id: `{a.get('proposal_id', 'unknown')}`")
        lines.append(f"- action_type: `{a.get('action_type', 'unknown')}`")
        lines.append("")

    return "\n".join(lines)


__all__ = ["render_markdown"]
