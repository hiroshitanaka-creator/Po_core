"""Text renderer for Po_core traces."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from rich.console import Console


def _format_bar(score: float, width: int = 20) -> str:
    clamped = max(0.0, min(score, 1.0))
    filled = int(round(clamped * width))
    return "█" * filled + "░" * (width - filled)


def _render_section(title: str) -> str:
    return f"\n{title}\n" + "-" * len(title)


def _render_tension_map(tension_map: Dict[str, float]) -> str:
    lines = [_render_section("Tension Map")]
    for dimension, score in sorted(tension_map.items()):
        lines.append(f"{dimension:24} {_format_bar(score)} {score:.2f}")
    return "\n".join(lines)


def _render_ethical_pressures(pressures: Dict[str, float]) -> str:
    lines = [_render_section("Ethical Pressure Summary")]
    for axis, score in sorted(pressures.items()):
        lines.append(f"{axis:24} {_format_bar(score)} {score:.2f}")
    return "\n".join(lines)


def _render_segments(segments: Iterable[Dict[str, Any]]) -> str:
    lines: List[str] = [_render_section("Segments")]
    for segment in segments:
        philosopher = segment.get("philosopher", "Unknown")
        stance = segment.get("stance") or segment.get("summary") or "(no summary)"
        lines.append(f"- {philosopher}: {stance}")
        if "ethical_pressure" in segment:
            score = segment["ethical_pressure"]
            lines.append(f"  ethical pressure: {_format_bar(float(score))} {float(score):.2f}")
        if segment.get("tension"):
            tensions = segment["tension"]
            rendered = ", ".join(f"{k}={v:.2f}" for k, v in tensions.items())
            lines.append(f"  tensions: {rendered}")
    return "\n".join(lines)


def render_trace(trace: Dict[str, Any], philosopher_filter: Optional[str] = None, *, console: Optional[Console] = None) -> str:
    """Render a trace to human-readable ASCII text.

    Args:
        trace: Loaded trace dictionary.
        philosopher_filter: Optional philosopher name to filter segments.
        console: Optional Rich console for styling.
    """

    header_lines = [
        f"Trace: {trace.get('trace_id', 'unknown')}",
        f"Title: {trace.get('title', 'Untitled Trace')}",
        f"Created: {trace.get('created_at', 'unknown')}",
    ]

    segments = trace.get("segments", [])
    if philosopher_filter:
        segments = [s for s in segments if s.get("philosopher") == philosopher_filter]
        header_lines.append(f"Filter: philosopher == '{philosopher_filter}'")

    body_parts: List[str] = ["\n".join(header_lines)]

    if tension_map := trace.get("tension_map"):
        body_parts.append(_render_tension_map(tension_map))

    if ethical_pressures := trace.get("ethical_pressure_summary"):
        body_parts.append(_render_ethical_pressures(ethical_pressures))

    if segments:
        body_parts.append(_render_segments(segments))
    else:
        body_parts.append(_render_section("Segments") + "\n(no segments found)")

    rendered = "\n\n".join(body_parts).rstrip() + "\n"

    if console:
        console.print(rendered)

    return rendered
