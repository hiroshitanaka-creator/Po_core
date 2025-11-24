from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure the project src directory is importable when running tests locally
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from po_core.po_viewer import (  # noqa: E402  # isort:skip
    export_visualization_data,
    load_po_trace,
    render_trace_summary,
)


def test_render_trace_snapshot() -> None:
    trace_path = ROOT / "examples/po_trace_sample.json"
    trace = load_po_trace(trace_path)
    output = render_trace_summary(trace)

    expected = """🎨 Po_trace Viewer — Socratic dialogue on courage
Trace ID: trace-sample-001

                 Tension Map
 Step ┃ Philosopher ┃ Tension ┃ Level
━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━
    1 │ Aristotle   │    0.44 │ █████·······
    1 │ Nietzsche   │    0.76 │ █████████···
    1 │ Socrates    │    0.32 │ ████········
    2 │ Aristotle   │    0.58 │ ███████·····
    2 │ Nietzsche   │    0.64 │ ████████····
    2 │ Socrates    │    0.28 │ ███·········


      Philosopher Contributions
 Philosopher ┃ Weight ┃ Share
━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━
 Aristotle   │   0.65 │ ████········
 Nietzsche   │   0.60 │ ████········
 Socrates    │   0.75 │ ████········
"""

    output_lines = [line.rstrip() for line in output.strip().splitlines()]
    expected_lines = [line.rstrip() for line in expected.strip().splitlines()]

    assert output_lines == expected_lines


def test_export_visualization_data() -> None:
    trace_path = ROOT / "examples/po_trace_sample.json"
    trace = load_po_trace(trace_path)

    payload = json.loads(export_visualization_data(trace))

    assert payload["trace_id"] == "trace-sample-001"
    assert payload["theme"] == "Socratic dialogue on courage"
    assert payload["contributions"]["Socrates"] == 0.75
    assert payload["tension_map"][0]["tension"]["Aristotle"] == 0.44
