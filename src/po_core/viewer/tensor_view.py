"""
Tensor View — Tensor metric display from TraceEvents
=====================================================

Renders tensor metrics (freedom_pressure, semantic_delta,
blocked_tensor, interaction_tensor) from TensorComputed events.
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence

from po_core.domain.trace_event import TraceEvent


def _find_tensor_event(events: Sequence[TraceEvent]) -> TraceEvent | None:
    """Find the TensorComputed event."""
    for e in events:
        if e.event_type == "TensorComputed":
            return e
    return None


def _bar(value: float, width: int = 20) -> str:
    """Create an ASCII bar for a value in [0, 1]."""
    filled = int(value * width)
    return "#" * filled + "." * (width - filled)


def _level(value: float) -> str:
    """Classify a metric value."""
    if value > 0.7:
        return "HIGH"
    elif value > 0.3:
        return "MED"
    return "LOW"


def render_tensor_markdown(events: Sequence[TraceEvent]) -> str:
    """
    Render tensor metrics as Markdown.

    Reads TensorComputed event and displays metric values
    with bar visualization.

    Args:
        events: TraceEvents from a pipeline run

    Returns:
        Markdown string showing tensor metrics
    """
    ev = _find_tensor_event(events)
    if ev is None:
        return "## Tensor Metrics\n\nNo TensorComputed event found."

    metric_keys = ev.payload.get("metrics", [])
    version = ev.payload.get("version", "unknown")

    lines: List[str] = []
    lines.append("## Tensor Metrics")
    lines.append(f"- version: `{version}`")
    lines.append("")
    lines.append("| Metric | Value | Level | Bar |")
    lines.append("|---|---:|---|---|")

    # Try to get actual values from a PoSelf metrics dict or tensor snapshot
    # The TensorComputed event only has metric key names, not values.
    # The actual values come from the pipeline's tensor snapshot.
    # We need to look at PhilosopherResult or DecisionEmitted for enriched data.
    # For now, display available metric keys.

    # Check if there's tensor data embedded in the payload
    for key in metric_keys:
        # In the current pipeline, TensorComputed only stores key names
        # Look for per-metric value in payload
        val = ev.payload.get(key)
        if val is not None and isinstance(val, (int, float)):
            fval = float(val)
            lines.append(f"| {key} | {fval:.4f} | {_level(fval)} | `{_bar(fval)}` |")
        else:
            lines.append(f"| {key} | - | - | registered |")

    lines.append("")
    return "\n".join(lines)


def render_tensor_text(events: Sequence[TraceEvent]) -> str:
    """
    Render tensor metrics as plain text with bars.

    Args:
        events: TraceEvents from a pipeline run

    Returns:
        Plain text string showing tensor metrics
    """
    ev = _find_tensor_event(events)
    if ev is None:
        return "Tensor Metrics: No data."

    metric_keys = ev.payload.get("metrics", [])
    version = ev.payload.get("version", "unknown")

    lines: List[str] = []
    lines.append("Tensor Metrics")
    lines.append(f"  version: {version}")

    for key in metric_keys:
        val = ev.payload.get(key)
        if val is not None and isinstance(val, (int, float)):
            fval = float(val)
            lines.append(f"  {key:<24s} {fval:.4f}  [{_bar(fval)}]  {_level(fval)}")
        else:
            lines.append(f"  {key:<24s} (registered)")

    return "\n".join(lines)


def extract_tensor_values(events: Sequence[TraceEvent]) -> Dict[str, float]:
    """
    Extract tensor metric values from events.

    Looks at TensorComputed payload for actual numeric values.

    Args:
        events: TraceEvents from a pipeline run

    Returns:
        Dict mapping metric name to float value
    """
    ev = _find_tensor_event(events)
    if ev is None:
        return {}

    result: Dict[str, float] = {}
    metric_keys = ev.payload.get("metrics", [])
    for key in metric_keys:
        val = ev.payload.get(key)
        if val is not None and isinstance(val, (int, float)):
            result[key] = float(val)
    return result


__all__ = ["render_tensor_markdown", "render_tensor_text", "extract_tensor_values"]
