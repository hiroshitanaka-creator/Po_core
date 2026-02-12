"""
Po_core Viewer WebUI — Phase 3 Observability Dashboard
======================================================

Dash-based browser dashboard for observing the run_turn pipeline.

Three tabs:
1. Pipeline & Tensors — 10-step pipeline progression + tensor metrics
2. Philosophers — Philosopher participation, debate, interaction heatmap
3. W_Ethics Gate — Explanation chain, violations, repairs, drift

Architecture:
    PoViewer (data) → web.app (Dash layout + callbacks) → Browser

Entry point:
    from po_core.viewer.web import create_app
    app = create_app()
    app.run(debug=True, port=8050)

Or via CLI:
    po-viewer --port 8050
"""

from po_core.viewer.web.app import create_app

__all__ = ["create_app"]
