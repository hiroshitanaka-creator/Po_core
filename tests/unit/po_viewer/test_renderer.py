import json
from pathlib import Path

from click.testing import CliRunner

from po_core.cli import main
from po_core.po_viewer import load_trace, render_trace


SAMPLE_TRACE = {
    "trace_id": "demo-001",
    "title": "Sample Reasoning Trace",
    "created_at": "2024-06-01T12:00:00Z",
    "tension_map": {
        "autonomy_vs_care": 0.65,
        "law_vs_mercy": 0.45,
    },
    "ethical_pressure_summary": {
        "deontological": 0.7,
        "care": 0.5,
    },
    "segments": [
        {
            "philosopher": "Kant",
            "stance": "Duty-driven reasoning about the act",
            "ethical_pressure": 0.7,
            "tension": {"law_vs_mercy": 0.4},
        },
        {
            "philosopher": "Gilligan",
            "summary": "Care perspective centering relationships",
            "ethical_pressure": 0.5,
            "tension": {"autonomy_vs_care": 0.6},
        },
    ],
}


def test_render_trace_includes_sections() -> None:
    rendered = render_trace(SAMPLE_TRACE)

    assert "Tension Map" in rendered
    assert "Ethical Pressure Summary" in rendered
    assert "Segments" in rendered
    assert "Kant" in rendered and "Gilligan" in rendered
    assert "autonomy_vs_care" in rendered


def test_render_trace_filters_philosopher() -> None:
    rendered = render_trace(SAMPLE_TRACE, philosopher_filter="Kant")

    assert "Kant" in rendered
    assert "Gilligan" not in rendered
    assert "Filter: philosopher == 'Kant'" in rendered


def test_load_trace_reads_json(tmp_path: Path) -> None:
    traces_dir = tmp_path / "data" / "traces"
    traces_dir.mkdir(parents=True)
    trace_path = traces_dir / "demo-001.json"
    trace_path.write_text(json.dumps(SAMPLE_TRACE), encoding="utf-8")

    loaded = load_trace("demo-001", traces_dir=traces_dir)

    assert loaded["trace_id"] == SAMPLE_TRACE["trace_id"]
    assert len(loaded["segments"]) == 2


def test_cli_view_outputs_trace(tmp_path: Path) -> None:
    traces_dir = tmp_path / "traces"
    traces_dir.mkdir(parents=True)
    (traces_dir / "demo-001.json").write_text(json.dumps(SAMPLE_TRACE), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, ["view", "demo-001", "--traces-dir", str(traces_dir), "--philosopher", "Kant"])

    assert result.exit_code == 0
    assert "Trace: demo-001" in result.output
    assert "Kant" in result.output
    assert "Gilligan" not in result.output
