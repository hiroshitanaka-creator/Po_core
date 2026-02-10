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


def _last(events: Iterable[TraceEvent], event_type: str) -> TraceEvent | None:
    """Get last event of specified type."""
    xs = [e for e in events if e.event_type == event_type]
    return xs[-1] if xs else None


def _last_by_variant(
    events: Iterable[TraceEvent], event_type: str, variant: str
) -> TraceEvent | None:
    """Get last event of specified type and variant."""
    xs = [
        e
        for e in events
        if e.event_type == event_type and e.payload.get("variant") == variant
    ]
    return xs[-1] if xs else None


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
        lines.append(
            f"- mode: {p.get('mode')}, n: {p.get('n')}, cost_total: {p.get('cost_total')}"
        )
        lines.append(f"- covered_tags: {p.get('covered_tags')}")
        ids = p.get("ids", [])
        if ids:
            lines.append(
                f"- ids: {', '.join(str(i) for i in ids[:10])}{'...' if len(ids) > 10 else ''}"
            )
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
        lines.append(
            f"- n: {c.get('n')}, kinds: {c.get('kinds')}, suggested: {c.get('suggested_forced_action')}"
        )
        top = c.get("top", [])
        if top:
            lines.append("")
            lines.append("| id | kind | severity | proposal_ids |")
            lines.append("|---|---:|---:|---|")
            for t in top:
                pids = t.get("proposal_ids", [])
                pids_str = ", ".join(str(p) for p in pids[:4])
                lines.append(
                    f"| {t.get('id', '')} | {t.get('kind', '')} | {t.get('severity', '')} | {pids_str} |"
                )
        lines.append("")

    # Pareto Front section
    if front:
        lines.append("## Pareto Front")
        f = front[-1].payload
        lines.append(f"- config_version: `{f.get('config_version', '')}`")
        lines.append(f"- config_source: `{f.get('config_source', '')}`")
        w = f.get("weights", {})
        lines.append(
            f"- weights: safety={w.get('safety', 0):.2f}, freedom={w.get('freedom', 0):.2f}, "
            f"explain={w.get('explain', 0):.2f}, brevity={w.get('brevity', 0):.2f}, "
            f"coherence={w.get('coherence', 0):.2f}"
        )
        rows = f.get("front", [])
        if rows:
            lines.append("")
            lines.append(
                "| proposal_id | action | safety | freedom | explain | brevity | coherence |"
            )
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

    # Candidate → Final (emitted decision) section
    de = _find(ev, "DecisionEmitted")
    ov = _find(ev, "SafetyOverrideApplied")

    if de:
        lines.append("## Candidate → Emitted（候補→最終）")
        p = de[-1].payload
        cand = p.get("candidate")
        final = p.get("final")
        gate = p.get("gate", {})
        lines.append(
            f"- stage: `{p.get('stage')}`, origin: `{p.get('origin')}`, degraded: `{p.get('degraded')}`"
        )
        if gate:
            lines.append(
                f"- gate.decision: `{gate.get('decision')}`, rules: {gate.get('rule_ids', [])[:5]}"
            )
        lines.append("")

        def _fp_row(kind: str, d: Any) -> str:
            if not isinstance(d, dict):
                return f"| {kind} | - | - | - | - | - | - |"
            return (
                f"| {kind} | {d.get('proposal_id', '')} | {d.get('action_type', '')} | "
                f"{d.get('content_len', '')} | {d.get('content_hash', '')} | "
                f"{d.get('policy_score', '')} | {d.get('author_reliability', '')} |"
            )

        lines.append(
            "| kind | proposal_id | action | len | hash | policy_score | author_rel |"
        )
        lines.append("|---|---|---|---:|---|---|---|")
        lines.append(_fp_row("candidate", cand))
        lines.append(_fp_row("final", final))
        lines.append("")

    if ov:
        lines.append("### SafetyOverrideApplied（安全上書き）")
        o = ov[-1].payload
        gate = o.get("gate", {})
        lines.append(f"- reason: `{o.get('reason')}`, stage: `{o.get('stage')}`")
        lines.append(
            f"- gate.decision: `{gate.get('decision')}`, rules: {gate.get('rule_ids', [])[:5]}"
        )
        lines.append("")

    # Pareto A/B Comparison section (Shadow評価)
    cmp = _last(ev, "DecisionComparisonComputed")
    if cmp:
        lines.append("## Pareto A/B Comparison（main vs shadow）")
        d = cmp.payload.get("diff", {})
        lines.append(
            f"- main config: `{d.get('main_config_version', '')}` / `{d.get('main_config_source', '')}`"
        )
        lines.append(
            f"- shadow config: `{d.get('shadow_config_version', '')}` / `{d.get('shadow_config_source', '')}`"
        )
        lines.append("")
        lines.append(
            f"- candidate_action_changed: `{d.get('candidate_action_changed', False)}`"
        )
        lines.append(
            f"- candidate_content_changed: `{d.get('candidate_content_changed', False)}`"
        )
        lines.append(
            f"- final_action_changed: `{d.get('final_action_changed', False)}`"
        )
        lines.append(
            f"- final_content_changed: `{d.get('final_content_changed', False)}`"
        )
        if "final_policy_score_delta" in d:
            delta = d.get("final_policy_score_delta", 0.0)
            lines.append(f"- final_policy_score_delta (shadow-main): `{delta:.4f}`")
        lines.append("")

        # main/shadow の詳細を表に表示
        main_data = cmp.payload.get("main", {})
        shadow_data = cmp.payload.get("shadow", {})

        lines.append("### Main vs Shadow (Candidate)")
        lines.append("| variant | proposal_id | action | len | hash | config |")
        lines.append("|---|---|---|---:|---|---|")

        mc = main_data.get("candidate", {})
        sc = shadow_data.get("candidate", {})
        lines.append(
            f"| main | {mc.get('proposal_id', '')[:20]} | {mc.get('action_type', '')} | "
            f"{mc.get('content_len', '')} | {mc.get('content_hash', '')} | "
            f"{mc.get('pareto_config_version', '')} |"
        )
        lines.append(
            f"| shadow | {sc.get('proposal_id', '')[:20]} | {sc.get('action_type', '')} | "
            f"{sc.get('content_len', '')} | {sc.get('content_hash', '')} | "
            f"{sc.get('pareto_config_version', '')} |"
        )
        lines.append("")

        lines.append("### Main vs Shadow (Final)")
        lines.append("| variant | proposal_id | action | len | hash | config |")
        lines.append("|---|---|---:|---|---|---|")

        mf = main_data.get("final", {})
        sf = shadow_data.get("final", {})
        lines.append(
            f"| main | {mf.get('proposal_id', '')[:20]} | {mf.get('action_type', '')} | "
            f"{mf.get('content_len', '')} | {mf.get('content_hash', '')} | "
            f"{mf.get('pareto_config_version', '')} |"
        )
        lines.append(
            f"| shadow | {sf.get('proposal_id', '')[:20]} | {sf.get('action_type', '')} | "
            f"{sf.get('content_len', '')} | {sf.get('content_hash', '')} | "
            f"{sf.get('pareto_config_version', '')} |"
        )
        lines.append("")

    return "\n".join(lines)


__all__ = ["render_markdown"]
