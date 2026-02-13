"""
Dash application factory for Po_core Viewer WebUI.

Creates a Dash app with four tabs:
1. Pipeline & Tensors — step chart + tensor bar chart
2. Philosophers — latency chart + participation table + interaction heatmap
3. W_Ethics Gate Decisions — explanation chain + drift gauge
4. Event Log — filterable event stream with type selector

All figures are generated at app creation time from TraceEvents.
Callbacks enable interactive filtering without full-page refresh.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

try:
    import dash
    from dash import Input, Output, callback, dcc, html
except ImportError:
    raise ImportError(
        "Dash is required for Viewer WebUI. Install with: pip install dash>=2.14.0"
    )

from po_core.domain.trace_event import TraceEvent
from po_core.safety.wethics_gate.explanation import ExplanationChain
from po_core.viewer.web.figures import (
    build_drift_gauge,
    build_evolution_timeline,
    build_philosopher_chart,
    build_pipeline_chart,
    build_tensor_chart,
    build_tension_heatmap,
    decision_badge_style,
)

# ── Tab builders ─────────────────────────────────────────────────


def _build_pipeline_tab(
    viewer: Optional[Any], events: Sequence[TraceEvent]
) -> html.Div:
    """Pipeline & Tensors tab layout with charts."""
    tensor_fig = build_tensor_chart(events) if events else None
    pipeline_fig = build_pipeline_chart(events) if events else None

    children = [
        html.H3("Pipeline Progression"),
    ]

    if pipeline_fig:
        children.append(dcc.Graph(id="pipeline-chart", figure=pipeline_fig))
    else:
        children.append(html.P("No pipeline data loaded."))

    children.extend(
        [
            html.Hr(),
            html.H3("Tensor Metrics"),
        ]
    )

    if tensor_fig:
        children.append(dcc.Graph(id="tensor-chart", figure=tensor_fig))
    else:
        children.append(html.P("No tensor data loaded."))

    # Text details (collapsible)
    children.extend(
        [
            html.Hr(),
            html.Details(
                [
                    html.Summary("Raw Pipeline Text"),
                    html.Pre(
                        viewer.pipeline_text() if viewer else "No data.",
                        style={
                            "whiteSpace": "pre-wrap",
                            "fontFamily": "monospace",
                            "backgroundColor": "#16213e",
                            "padding": "12px",
                            "borderRadius": "4px",
                            "color": "#e0e0e0",
                        },
                    ),
                ],
            ),
            html.Details(
                [
                    html.Summary("Raw Tensor Text"),
                    html.Pre(
                        viewer.tensor_text() if viewer else "No data.",
                        style={
                            "whiteSpace": "pre-wrap",
                            "fontFamily": "monospace",
                            "backgroundColor": "#16213e",
                            "padding": "12px",
                            "borderRadius": "4px",
                            "color": "#e0e0e0",
                        },
                    ),
                ],
            ),
        ]
    )

    return html.Div(children, style={"padding": "20px"})


def _build_philosopher_tab(
    viewer: Optional[Any], events: Sequence[TraceEvent]
) -> html.Div:
    """Philosophers tab layout with charts."""
    ph_fig = build_philosopher_chart(events) if events else None

    children = [
        html.H3("Philosopher Participation"),
    ]

    if ph_fig:
        children.append(dcc.Graph(id="philosopher-chart", figure=ph_fig))
    else:
        children.append(html.P("No philosopher data loaded."))

    # Battalion info
    if viewer:
        battalion = viewer.battalion_info()
        if battalion:
            children.extend(
                [
                    html.Hr(),
                    html.H4("Battalion Selection"),
                    html.Ul(
                        [
                            html.Li(f"Mode: {battalion.get('mode', '?')}"),
                            html.Li(f"Selected: {battalion.get('n', 0)} philosophers"),
                            html.Li(f"Cost: {battalion.get('cost_total', 0)}"),
                        ]
                    ),
                ]
            )

    # Raw text
    children.extend(
        [
            html.Hr(),
            html.Details(
                [
                    html.Summary("Raw Philosopher Text"),
                    html.Pre(
                        viewer.philosopher_text() if viewer else "No data.",
                        style={
                            "whiteSpace": "pre-wrap",
                            "fontFamily": "monospace",
                            "backgroundColor": "#16213e",
                            "padding": "12px",
                            "borderRadius": "4px",
                            "color": "#e0e0e0",
                        },
                    ),
                ],
            ),
        ]
    )

    return html.Div(children, style={"padding": "20px"})


def _build_ethics_tab(
    explanation: Optional[ExplanationChain] = None,
) -> html.Div:
    """W_Ethics Gate Decisions tab layout with explanation chain rendering."""
    children = [html.H3("W_Ethics Gate Decision")]

    if explanation is None:
        children.append(html.P("No W_Ethics Gate data loaded."))
        children.append(dcc.Graph(id="drift-gauge", figure=build_drift_gauge(None)))
        return html.Div(children, style={"padding": "20px"})

    # Decision badge
    badge = decision_badge_style(explanation.decision)
    children.append(
        html.Div(
            badge["label"],
            style={
                "display": "inline-block",
                "padding": "8px 24px",
                "borderRadius": "4px",
                "backgroundColor": badge["color"],
                "color": "white",
                "fontWeight": "bold",
                "fontSize": "18px",
                "marginBottom": "12px",
            },
        )
    )
    children.append(html.P(f"Reason: {explanation.decision_reason}"))

    # Violations
    if explanation.violations:
        children.append(html.Hr())
        children.append(html.H4("Violations Detected"))
        for v in explanation.violations:
            repair_tag = "repairable" if v.repairable else "hard reject"
            header = f"{v.code} ({v.code_label}) — impact={v.impact_score:.2f} [{repair_tag}]"
            evidence_items = [
                html.Li(f"[{e.detector_id}] {e.message} (strength={e.strength:.2f})")
                for e in v.evidence
            ]
            children.append(
                html.Details(
                    [
                        html.Summary(
                            header,
                            style={"fontWeight": "bold", "cursor": "pointer"},
                        ),
                        (
                            html.Ul(evidence_items)
                            if evidence_items
                            else html.P("No evidence details.")
                        ),
                    ],
                    open=True,
                    style={"marginBottom": "8px"},
                )
            )

    # Repairs
    if explanation.repairs:
        children.append(html.Hr())
        children.append(html.H4("Repairs Applied"))
        children.append(html.Ol([html.Li(r.description) for r in explanation.repairs]))

    # Drift gauge
    children.append(html.Hr())
    children.append(html.H4("Semantic Drift"))
    drift_score = explanation.drift.drift_score if explanation.drift else None
    children.append(dcc.Graph(id="drift-gauge", figure=build_drift_gauge(drift_score)))

    if explanation.drift and explanation.drift.notes:
        children.append(html.P(f"Notes: {explanation.drift.notes}"))

    # Summary
    children.append(html.Hr())
    children.append(html.P(explanation.summary, style={"fontWeight": "bold"}))

    # Raw markdown
    children.append(
        html.Details(
            [
                html.Summary("Raw Markdown"),
                html.Pre(
                    explanation.to_markdown(),
                    style={
                        "whiteSpace": "pre-wrap",
                        "fontFamily": "monospace",
                        "backgroundColor": "#16213e",
                        "padding": "12px",
                        "borderRadius": "4px",
                        "color": "#e0e0e0",
                    },
                ),
            ],
        )
    )

    return html.Div(children, style={"padding": "20px"})


# ── Event Log tab (Phase 3: interactive filtering) ───────────────

_PRE_STYLE = {
    "whiteSpace": "pre-wrap",
    "fontFamily": "monospace",
    "backgroundColor": "#16213e",
    "padding": "12px",
    "borderRadius": "4px",
    "color": "#e0e0e0",
    "maxHeight": "600px",
    "overflow": "auto",
}


def _build_event_log_tab(events: Sequence[TraceEvent]) -> html.Div:
    """Event Log tab with type-filter dropdown (callback-driven)."""
    event_types = sorted({e.event_type for e in events}) if events else []

    children = [
        html.H3("Event Log"),
        html.Label("Filter by event type:", style={"color": "#e0e0e0"}),
        dcc.Dropdown(
            id="event-type-filter",
            options=[{"label": "All", "value": "__all__"}]
            + [{"label": t, "value": t} for t in event_types],
            value="__all__",
            clearable=False,
            style={"marginBottom": "12px"},
        ),
        html.Div(id="event-log-content"),
    ]
    return html.Div(children, style={"padding": "20px"})


def _render_event_rows(
    events: Sequence[TraceEvent], type_filter: str = "__all__"
) -> List[Any]:
    """Render filtered event rows as HTML."""
    filtered = (
        events
        if type_filter == "__all__"
        else [e for e in events if e.event_type == type_filter]
    )

    if not filtered:
        return [html.P("No events match the filter.")]

    rows = []
    for e in filtered:
        ts = e.occurred_at.strftime("%H:%M:%S.%f")[:-3] if e.occurred_at else "?"
        payload_str = ", ".join(
            f"{k}={v}" for k, v in (e.payload or {}).items()
        )[:200]
        rows.append(
            html.Div(
                [
                    html.Span(
                        f"[{ts}] ",
                        style={"color": "#888", "fontFamily": "monospace"},
                    ),
                    html.Span(
                        e.event_type,
                        style={
                            "fontWeight": "bold",
                            "color": "#4ecdc4",
                            "fontFamily": "monospace",
                        },
                    ),
                    html.Span(
                        f"  {payload_str}" if payload_str else "",
                        style={"color": "#aaa", "fontFamily": "monospace"},
                    ),
                ],
                style={"marginBottom": "4px"},
            )
        )
    return rows


# ── App factory ──────────────────────────────────────────────────


def create_app(
    events: Optional[Sequence[TraceEvent]] = None,
    explanation: Optional[ExplanationChain] = None,
    title: str = "Po_core Viewer",
    debug: bool = False,
) -> dash.Dash:
    """
    Create the Dash application for Po_core Viewer WebUI.

    Args:
        events: Optional TraceEvents to display on startup.
        explanation: Optional ExplanationChain for W_Ethics tab.
        title: Browser tab title.
        debug: Enable Dash debug mode.

    Returns:
        Configured Dash application instance.
    """
    app = dash.Dash(
        __name__,
        title=title,
        suppress_callback_exceptions=True,
    )

    # Late import to break circular dependency:
    # po_viewer -> viewer.web -> viewer.web.app -> po_viewer
    if events:
        import importlib

        _pv = importlib.import_module("po_core.po_viewer")
        viewer = _pv.PoViewer(events)
    else:
        viewer = None
    ev_list: Sequence[TraceEvent] = events or []

    app.layout = html.Div(
        [
            # Header
            html.Div(
                [
                    html.H1("Po_core Viewer"),
                    html.P(
                        viewer.summary() if viewer else "No session loaded.",
                        id="session-summary",
                    ),
                ],
                style={
                    "padding": "20px",
                    "backgroundColor": "#1a1a2e",
                    "color": "#e0e0e0",
                },
            ),
            # Tabs
            dcc.Tabs(
                id="main-tabs",
                value="tab-pipeline",
                children=[
                    dcc.Tab(
                        label="Pipeline & Tensors",
                        value="tab-pipeline",
                        children=_build_pipeline_tab(viewer, ev_list),
                    ),
                    dcc.Tab(
                        label="Philosophers",
                        value="tab-philosophers",
                        children=_build_philosopher_tab(viewer, ev_list),
                    ),
                    dcc.Tab(
                        label="W_Ethics Gate",
                        value="tab-ethics",
                        children=_build_ethics_tab(explanation),
                    ),
                    dcc.Tab(
                        label="Event Log",
                        value="tab-events",
                        children=_build_event_log_tab(ev_list),
                    ),
                ],
            ),
        ]
    )

    # ── Callbacks (interactive filtering) ────────────────────────
    @app.callback(
        Output("event-log-content", "children"),
        Input("event-type-filter", "value"),
    )
    def _update_event_log(type_filter: str) -> List[Any]:
        return _render_event_rows(ev_list, type_filter)

    return app


__all__ = ["create_app"]
