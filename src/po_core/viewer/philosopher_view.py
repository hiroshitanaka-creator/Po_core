"""
Philosopher View — Per-philosopher participation & results from TraceEvents
============================================================================

Renders philosopher participation details from PhilosopherResult events,
PhilosophersSelected events, and the aggregate pipeline data.

DEPENDENCY RULES:
- domain.trace_event only
- No ensemble/aggregator implementation dependencies
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence

from po_core.domain.trace_event import TraceEvent


def _find(events: Sequence[TraceEvent], event_type: str) -> List[TraceEvent]:
    """Filter events by type."""
    return [e for e in events if e.event_type == event_type]


def extract_philosopher_data(events: Sequence[TraceEvent]) -> List[Dict[str, Any]]:
    """
    Extract philosopher participation data from trace events.

    Returns list of dicts with: name, n_proposals, latency_ms, timed_out, error
    """
    results = _find(events, "PhilosopherResult")
    return [
        {
            "name": e.payload.get("name", "unknown"),
            "n_proposals": e.payload.get("n", 0),
            "latency_ms": e.payload.get("latency_ms", -1),
            "timed_out": e.payload.get("timed_out", False),
            "error": e.payload.get("error", ""),
        }
        for e in results
    ]


def extract_battalion_info(events: Sequence[TraceEvent]) -> Dict[str, Any]:
    """
    Extract battalion (philosopher selection) data from trace events.

    Returns dict with: mode, n, cost_total, covered_tags, ids
    """
    sel = _find(events, "PhilosophersSelected")
    if not sel:
        return {}
    p = sel[-1].payload
    return {
        "mode": p.get("mode", "unknown"),
        "n": p.get("n", 0),
        "cost_total": p.get("cost_total", 0),
        "covered_tags": p.get("covered_tags", []),
        "ids": p.get("ids", []),
    }


def render_philosopher_markdown(events: Sequence[TraceEvent]) -> str:
    """
    Render philosopher participation as Markdown.

    Shows battalion selection info and per-philosopher results
    with latency, proposal count, and status.
    """
    ev = list(events)
    lines: List[str] = []

    # Battalion section
    battalion = extract_battalion_info(ev)
    if battalion:
        lines.append("## Philosopher Battalion")
        lines.append(f"- mode: `{battalion['mode']}`")
        lines.append(f"- selected: {battalion['n']} philosophers")
        lines.append(f"- cost_total: {battalion['cost_total']}")
        tags = battalion.get("covered_tags", [])
        if tags:
            lines.append(f"- tags: {', '.join(str(t) for t in tags[:10])}")
        lines.append("")

    # Per-philosopher results
    philosophers = extract_philosopher_data(ev)
    if not philosophers:
        lines.append("## Philosopher Results")
        lines.append("_No philosopher results recorded._")
        lines.append("")
        return "\n".join(lines)

    lines.append("## Philosopher Results")
    lines.append("")
    lines.append("| Philosopher | Proposals | Latency (ms) | Status |")
    lines.append("|---|---:|---:|---|")

    for ph in philosophers:
        name = ph["name"]
        n = ph["n_proposals"]
        lat = ph["latency_ms"]
        lat_str = f"{lat}" if lat >= 0 else "-"

        if ph["error"]:
            status = f"error: {ph['error'][:40]}"
        elif ph["timed_out"]:
            status = "timed out"
        elif n == 0:
            status = "no proposals"
        else:
            status = "ok"

        lines.append(f"| {name} | {n} | {lat_str} | {status} |")

    # Summary stats
    total = len(philosophers)
    total_proposals = sum(ph["n_proposals"] for ph in philosophers)
    errors = sum(1 for ph in philosophers if ph["error"])
    timeouts = sum(1 for ph in philosophers if ph["timed_out"])
    latencies = [ph["latency_ms"] for ph in philosophers if ph["latency_ms"] >= 0]

    lines.append("")
    lines.append(f"**Summary**: {total} philosophers, {total_proposals} proposals")
    if errors:
        lines.append(f"- errors: {errors}")
    if timeouts:
        lines.append(f"- timeouts: {timeouts}")
    if latencies:
        avg_lat = sum(latencies) / len(latencies)
        max_lat = max(latencies)
        lines.append(f"- avg latency: {avg_lat:.0f}ms, max: {max_lat:.0f}ms")
    lines.append("")

    return "\n".join(lines)


def render_philosopher_text(events: Sequence[TraceEvent]) -> str:
    """
    Render philosopher participation as plain text.

    Compact one-line-per-philosopher format.
    """
    ev = list(events)
    lines: List[str] = []

    battalion = extract_battalion_info(ev)
    if battalion:
        lines.append(
            f"Battalion: {battalion['n']} philosophers "
            f"(mode={battalion['mode']}, cost={battalion['cost_total']})"
        )

    philosophers = extract_philosopher_data(ev)
    if not philosophers:
        lines.append("No philosopher results.")
        return "\n".join(lines)

    lines.append(f"Philosophers ({len(philosophers)}):")
    for ph in philosophers:
        name = ph["name"]
        n = ph["n_proposals"]
        lat = ph["latency_ms"]
        lat_str = f"{lat}ms" if lat >= 0 else "?"

        if ph["error"]:
            flag = " [ERROR]"
        elif ph["timed_out"]:
            flag = " [TIMEOUT]"
        else:
            flag = ""

        lines.append(f"  {name:20s} proposals={n} latency={lat_str}{flag}")

    return "\n".join(lines)


__all__ = [
    "extract_philosopher_data",
    "extract_battalion_info",
    "render_philosopher_markdown",
    "render_philosopher_text",
]
