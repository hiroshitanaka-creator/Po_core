"""
Po_core Viewer - TraceEvent visualization
=========================================

Viewers consume TraceEvents and produce human-readable reports.
"""

from po_core.viewer.decision_report_md import render_markdown
from po_core.viewer.evolution_graph import EvolutionGraphVisualizer
from po_core.viewer.philosopher_view import (
    render_philosopher_markdown,
    render_philosopher_text,
)
from po_core.viewer.pipeline_view import render_pipeline_markdown, render_pipeline_text
from po_core.viewer.pressure_display import PressureDisplayVisualizer
from po_core.viewer.tension_map import TensionMapVisualizer
from po_core.viewer.tensor_view import render_tensor_markdown, render_tensor_text

__all__ = [
    "render_markdown",
    "render_philosopher_markdown",
    "render_philosopher_text",
    "render_pipeline_markdown",
    "render_pipeline_text",
    "render_tensor_markdown",
    "render_tensor_text",
    "EvolutionGraphVisualizer",
    "PressureDisplayVisualizer",
    "TensionMapVisualizer",
]
