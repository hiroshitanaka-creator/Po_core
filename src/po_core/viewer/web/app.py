"""
Dash application factory for Po_core Viewer WebUI.

Creates a Dash app with three tabs:
1. Pipeline & Tensors
2. Philosophers
3. W_Ethics Gate Decisions

This is the Phase 3 scaffold — layouts defined, callbacks to be wired.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

try:
    import dash
    from dash import dcc, html
except ImportError:
    raise ImportError(
        "Dash is required for Viewer WebUI. Install with: pip install dash>=2.14.0"
    )

from po_core.domain.trace_event import TraceEvent
from po_core.po_viewer import PoViewer


def _build_pipeline_tab(viewer: Optional[PoViewer] = None) -> html.Div:
    """Pipeline & Tensors tab layout."""
    return html.Div(
        [
            html.H3("Pipeline Progression"),
            html.Pre(
                viewer.pipeline_text() if viewer else "No data loaded.",
                id="pipeline-text",
                style={"whiteSpace": "pre-wrap", "fontFamily": "monospace"},
            ),
            html.Hr(),
            html.H3("Tensor Metrics"),
            html.Pre(
                viewer.tensor_text() if viewer else "No data loaded.",
                id="tensor-text",
                style={"whiteSpace": "pre-wrap", "fontFamily": "monospace"},
            ),
            html.Hr(),
            html.H3("Tensor Chart"),
            dcc.Graph(id="tensor-chart"),
        ],
        style={"padding": "20px"},
    )


def _build_philosopher_tab(viewer: Optional[PoViewer] = None) -> html.Div:
    """Philosophers tab layout."""
    return html.Div(
        [
            html.H3("Philosopher Participation"),
            html.Pre(
                viewer.philosopher_text() if viewer else "No data loaded.",
                id="philosopher-text",
                style={"whiteSpace": "pre-wrap", "fontFamily": "monospace"},
            ),
            html.Hr(),
            html.H3("Interaction Heatmap"),
            dcc.Graph(id="interaction-heatmap"),
        ],
        style={"padding": "20px"},
    )


def _build_ethics_tab() -> html.Div:
    """W_Ethics Gate Decisions tab layout."""
    return html.Div(
        [
            html.H3("W_Ethics Gate Decision"),
            html.Div(id="ethics-decision-badge"),
            html.Hr(),
            html.H3("Explanation Chain"),
            html.Div(id="explanation-chain", children="No decision data loaded."),
            html.Hr(),
            html.H3("Violation Details"),
            html.Div(id="violation-details"),
            html.Hr(),
            html.H3("Repair Log"),
            html.Pre(id="repair-log"),
            html.Hr(),
            html.H3("Semantic Drift"),
            dcc.Graph(id="drift-gauge"),
        ],
        style={"padding": "20px"},
    )


def create_app(
    events: Optional[Sequence[TraceEvent]] = None,
    title: str = "Po_core Viewer",
    debug: bool = False,
) -> dash.Dash:
    """
    Create the Dash application for Po_core Viewer WebUI.

    Args:
        events: Optional TraceEvents to display on startup.
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

    viewer = PoViewer(events) if events else None

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
                        children=_build_pipeline_tab(viewer),
                    ),
                    dcc.Tab(
                        label="Philosophers",
                        value="tab-philosophers",
                        children=_build_philosopher_tab(viewer),
                    ),
                    dcc.Tab(
                        label="W_Ethics Gate",
                        value="tab-ethics",
                        children=_build_ethics_tab(),
                    ),
                ],
            ),
        ]
    )

    return app


__all__ = ["create_app"]
