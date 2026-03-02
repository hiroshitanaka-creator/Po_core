"""
Dash application factory for Po_core Viewer WebUI.

Creates a Dash app with four tabs:
1. Pipeline & Tensors — step chart + tensor bar chart
2. Philosophers — latency chart + participation table
3. W_Ethics Gate Decisions — explanation chain + drift gauge
4. Deliberation — round progression + interaction summary

All figures are generated at app creation time from TraceEvents.
For live updates, call create_app() with new events.
"""

from __future__ import annotations

from typing import Any, Optional, Sequence

try:
    import dash
    from dash import dcc, html
except ImportError:
    raise ImportError(
        "Dash is required for Viewer WebUI. Install with: pip install dash>=2.14.0"
    )

from po_core.domain.trace_event import TraceEvent
from po_core.safety.wethics_gate.explanation import ExplanationChain
from po_core.viewer.tradeoff_map import build_tradeoff_map
from po_core.viewer.web.figures import (
    build_deliberation_round_chart,
    build_drift_gauge,
    build_influence_heatmap,
    build_interaction_heatmap,
    build_philosopher_chart,
    build_pipeline_chart,
    build_tensor_chart,
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


def _build_deliberation_tab(
    events: Sequence[TraceEvent],
) -> html.Div:
    """Deliberation tab layout with round progression and interaction charts."""
    children = [html.H3("Deliberation Engine")]

    # Round progression chart
    round_fig = build_deliberation_round_chart(events) if events else None
    if round_fig:
        children.append(dcc.Graph(id="deliberation-rounds", figure=round_fig))
    else:
        children.append(html.P("No deliberation data loaded."))

    # Interaction summary chart
    children.extend([html.Hr(), html.H3("Philosopher Interactions")])
    interaction_fig = build_interaction_heatmap(events) if events else None
    if interaction_fig:
        children.append(dcc.Graph(id="interaction-summary", figure=interaction_fig))
    else:
        children.append(html.P("No interaction data loaded."))

    # Key interaction pairs
    delib_data = None
    for e in events:
        if e.event_type == "DeliberationCompleted":
            delib_data = e.payload
            break

    if delib_data:
        summary = delib_data.get("interaction_summary") or {}
        max_tension = summary.get("max_tension_pair")
        max_harmony = summary.get("max_harmony_pair")

        if max_tension or max_harmony:
            children.extend([html.Hr(), html.H4("Key Pairs")])
            pair_items = []
            if max_tension:
                pair_items.append(
                    html.Li(
                        f"Highest Tension: {max_tension.get('philosopher_a', '?')} "
                        f"vs {max_tension.get('philosopher_b', '?')} "
                        f"(tension={max_tension.get('tension', 0):.3f})",
                        style={"color": "#e94560"},
                    )
                )
            if max_harmony:
                pair_items.append(
                    html.Li(
                        f"Highest Harmony: {max_harmony.get('philosopher_a', '?')} "
                        f"& {max_harmony.get('philosopher_b', '?')} "
                        f"(harmony={max_harmony.get('harmony', 0):.3f})",
                        style={"color": "#00d26a"},
                    )
                )
            children.append(html.Ul(pair_items))

    return html.Div(children, style={"padding": "20px"})


def _build_tradeoff_tab(events: Sequence[TraceEvent]) -> html.Div:
    """Trade-off map tab with axis scoreboards, disagreements and influence edges."""
    tradeoff_map = build_tradeoff_map(response=None, tracer=events)
    axis = tradeoff_map.get("axis") if isinstance(tradeoff_map, dict) else None
    influence = (
        tradeoff_map.get("influence") if isinstance(tradeoff_map, dict) else None
    )

    scoreboard = axis.get("scoreboard") if isinstance(axis, dict) else None
    disagreements = axis.get("disagreements") if isinstance(axis, dict) else None
    influence_edges = (
        influence.get("influence_edges") if isinstance(influence, dict) else None
    )

    children = [html.H3("Trade-off Map")]

    if not scoreboard and not disagreements and not influence_edges:
        children.append(html.P("No tradeoff data available"))
        return html.Div(children, style={"padding": "20px"})

    children.append(html.H4("Axis Scoreboard"))
    if isinstance(scoreboard, dict) and scoreboard:
        rows = []
        for axis_name, values in scoreboard.items():
            value_dict = values if isinstance(values, dict) else {}
            rows.append(
                html.Tr(
                    [
                        html.Td(str(axis_name)),
                        html.Td(f"{value_dict.get('mean', 0.0):.3f}"),
                        html.Td(f"{value_dict.get('variance', 0.0):.3f}"),
                        html.Td(str(value_dict.get("samples", 0))),
                    ]
                )
            )
        children.append(
            html.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Axis"),
                                html.Th("Mean"),
                                html.Th("Variance"),
                                html.Th("Samples"),
                            ]
                        )
                    ),
                    html.Tbody(rows),
                ]
            )
        )
    else:
        children.append(html.P("No tradeoff data available"))

    children.extend([html.Hr(), html.H4("Disagreements")])
    if isinstance(disagreements, list) and disagreements:
        children.append(
            html.Ul([html.Li(str(item)) for item in disagreements]),
        )
    else:
        children.append(html.P("No tradeoff data available"))

    children.extend([html.Hr(), html.H4("Influence Edges")])
    if isinstance(influence_edges, list) and influence_edges:
        edge_rows = []
        for edge in influence_edges:
            if not isinstance(edge, dict):
                continue
            edge_rows.append(
                html.Tr(
                    [
                        html.Td(str(edge.get("from", "?"))),
                        html.Td(str(edge.get("to", "?"))),
                        html.Td(f"{float(edge.get('weight', 0.0)):.3f}"),
                    ]
                )
            )
        children.append(
            html.Table(
                [
                    html.Thead(
                        html.Tr([html.Th("From"), html.Th("To"), html.Th("Weight")])
                    ),
                    html.Tbody(edge_rows),
                ]
            )
        )
        children.append(
            dcc.Graph(
                id="influence-edges-figure",
                figure=build_influence_heatmap(tradeoff_map),
            )
        )
    else:
        children.append(html.P("No tradeoff data available"))

    return html.Div(children, style={"padding": "20px"})


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
                        label="Deliberation",
                        value="tab-deliberation",
                        children=_build_deliberation_tab(ev_list),
                    ),
                    dcc.Tab(
                        label="Trade-off Map",
                        value="tab-tradeoff",
                        children=_build_tradeoff_tab(ev_list),
                    ),
                ],
            ),
        ]
    )

    return app


__all__ = ["create_app"]
