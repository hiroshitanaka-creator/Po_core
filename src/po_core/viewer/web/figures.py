"""
Plotly figure builders for Po_core Viewer WebUI.

Pure functions: TraceEvent data → Plotly Figure objects.
No side effects, no Dash dependencies — just data → visualization.

Used by viewer/web/app.py callbacks and also usable standalone.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

import plotly.graph_objects as go

from po_core.domain.trace_event import TraceEvent
from po_core.viewer.philosopher_view import extract_philosopher_data
from po_core.viewer.pipeline_view import PIPELINE_STEPS
from po_core.viewer.tensor_view import extract_tensor_values

# ── Color constants ──────────────────────────────────────────────

_COLORS = {
    "bg": "#1a1a2e",
    "surface": "#16213e",
    "accent": "#0f3460",
    "highlight": "#e94560",
    "text": "#e0e0e0",
    "ok": "#00d26a",
    "warn": "#f5a623",
    "danger": "#e94560",
    "low": "#4ecdc4",
    "med": "#f5a623",
    "high": "#e94560",
}


def _level_color(value: float) -> str:
    if value > 0.7:
        return _COLORS["high"]
    elif value > 0.3:
        return _COLORS["med"]
    return _COLORS["low"]


# ── Tensor bar chart ─────────────────────────────────────────────


def build_tensor_chart(events: Sequence[TraceEvent]) -> go.Figure:
    """
    Horizontal bar chart of tensor metric values.

    Each bar is colored by level (LOW/MED/HIGH).
    """
    values = extract_tensor_values(events)

    if not values:
        fig = go.Figure()
        fig.add_annotation(text="No tensor data", showarrow=False, font_size=16)
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=_COLORS["bg"],
            plot_bgcolor=_COLORS["surface"],
            height=200,
        )
        return fig

    names = list(values.keys())
    vals = list(values.values())
    colors = [_level_color(v) for v in vals]

    fig = go.Figure(
        go.Bar(
            x=vals,
            y=names,
            orientation="h",
            marker_color=colors,
            text=[f"{v:.3f}" for v in vals],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Tensor Metrics",
        xaxis_title="Value",
        xaxis_range=[0, 1.15],
        template="plotly_dark",
        paper_bgcolor=_COLORS["bg"],
        plot_bgcolor=_COLORS["surface"],
        height=max(200, len(names) * 60 + 80),
        margin=dict(l=160, r=40, t=50, b=40),
    )
    return fig


# ── Philosopher latency chart ────────────────────────────────────


def build_philosopher_chart(events: Sequence[TraceEvent]) -> go.Figure:
    """
    Bar chart of philosopher latency with proposal count annotations.
    """
    data = extract_philosopher_data(events)

    if not data:
        fig = go.Figure()
        fig.add_annotation(text="No philosopher data", showarrow=False, font_size=16)
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=_COLORS["bg"],
            plot_bgcolor=_COLORS["surface"],
            height=200,
        )
        return fig

    names = [d["name"] for d in data]
    latencies = [d["latency_ms"] if d["latency_ms"] >= 0 else 0 for d in data]
    proposals = [d["n_proposals"] for d in data]
    colors = []
    for d in data:
        if d["error"]:
            colors.append(_COLORS["danger"])
        elif d["timed_out"]:
            colors.append(_COLORS["warn"])
        else:
            colors.append(_COLORS["ok"])

    fig = go.Figure(
        go.Bar(
            x=latencies,
            y=names,
            orientation="h",
            marker_color=colors,
            text=[f"{p} proposals" for p in proposals],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Philosopher Latency (ms)",
        xaxis_title="Latency (ms)",
        template="plotly_dark",
        paper_bgcolor=_COLORS["bg"],
        plot_bgcolor=_COLORS["surface"],
        height=max(250, len(names) * 35 + 100),
        margin=dict(l=160, r=80, t=50, b=40),
    )
    return fig


# ── Pipeline step chart ──────────────────────────────────────────


def build_pipeline_chart(events: Sequence[TraceEvent]) -> go.Figure:
    """
    Pipeline 10-step waterfall: green = completed, red = blocked, grey = skipped.
    """
    event_types_present = {e.event_type for e in events}

    labels = []
    statuses = []  # 1=ok, 0=skipped, -1=blocked
    colors = []

    for step_num, event_type, label in PIPELINE_STEPS:
        labels.append(f"{step_num}. {label}")
        if event_type in event_types_present:
            # Check for blocking / degradation
            if event_type == "SafetyJudged:Intention":
                ev = next((e for e in events if e.event_type == event_type), None)
                if ev and ev.payload.get("decision") != "allow":
                    statuses.append(-1)
                    colors.append(_COLORS["danger"])
                    continue
            statuses.append(1)
            colors.append(_COLORS["ok"])
        else:
            statuses.append(0)
            colors.append("#555555")

    fig = go.Figure(
        go.Bar(
            x=[1] * len(labels),
            y=labels,
            orientation="h",
            marker_color=colors,
            hovertext=[
                "completed" if s == 1 else "blocked" if s == -1 else "skipped"
                for s in statuses
            ],
        )
    )
    fig.update_layout(
        title="Pipeline Steps",
        xaxis=dict(showticklabels=False, range=[0, 1.2]),
        template="plotly_dark",
        paper_bgcolor=_COLORS["bg"],
        plot_bgcolor=_COLORS["surface"],
        height=max(300, len(labels) * 35 + 80),
        margin=dict(l=200, r=40, t=50, b=40),
        showlegend=False,
    )
    return fig


# ── Drift gauge ──────────────────────────────────────────────────


def build_drift_gauge(
    drift_score: Optional[float],
    threshold_escalate: float = 0.4,
    threshold_reject: float = 0.7,
) -> go.Figure:
    """
    Gauge indicator for semantic drift score.

    Green (0-0.4) → Yellow (0.4-0.7) → Red (0.7-1.0)
    """
    if drift_score is None:
        fig = go.Figure()
        fig.add_annotation(text="No drift data", showarrow=False, font_size=16)
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=_COLORS["bg"],
            plot_bgcolor=_COLORS["surface"],
            height=250,
        )
        return fig

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=drift_score,
            title={"text": "Semantic Drift"},
            gauge=dict(
                axis=dict(range=[0, 1]),
                bar=dict(color="#4ecdc4"),
                steps=[
                    dict(range=[0, threshold_escalate], color="#00d26a"),
                    dict(range=[threshold_escalate, threshold_reject], color="#f5a623"),
                    dict(range=[threshold_reject, 1], color="#e94560"),
                ],
                threshold=dict(
                    line=dict(color="white", width=2),
                    thickness=0.8,
                    value=drift_score,
                ),
            ),
        )
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=_COLORS["bg"],
        plot_bgcolor=_COLORS["surface"],
        height=250,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


# ── Decision badge (HTML-ready text) ─────────────────────────────

_DECISION_STYLES = {
    "allow": {"color": "#00d26a", "label": "ALLOW"},
    "allow_with_repair": {"color": "#f5a623", "label": "ALLOW WITH REPAIR"},
    "reject": {"color": "#e94560", "label": "REJECT"},
    "escalate": {"color": "#9b59b6", "label": "ESCALATE"},
}


def decision_badge_style(decision: str) -> Dict[str, str]:
    """Return style dict and label for a gate decision badge."""
    info = _DECISION_STYLES.get(decision, {"color": "#888", "label": decision.upper()})
    return {
        "label": info["label"],
        "color": info["color"],
    }


__all__ = [
    "build_tensor_chart",
    "build_philosopher_chart",
    "build_pipeline_chart",
    "build_drift_gauge",
    "decision_badge_style",
]
