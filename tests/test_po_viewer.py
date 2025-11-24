from pathlib import Path

import pytest
from rich.console import Console

from po_core import po_viewer


def test_load_trace(sample_trace_path: Path) -> None:
    log = po_viewer.load_trace(sample_trace_path)

    assert log.session == "Sample Po_trace Session"
    assert [event.philosopher for event in log.events] == [
        "Aristotle",
        "Confucius",
        "Simone de Beauvoir",
        "Aristotle",
    ]
    assert log.philosopher_contributions[0].name == "Aristotle"


def test_export_visualization(sample_trace_path: Path) -> None:
    log = po_viewer.load_trace(sample_trace_path)
    payload = po_viewer.export_visualization(log)

    assert payload["session"] == "Sample Po_trace Session"
    assert payload["timeline"][0]["step"] == 1
    assert payload["philosophers"][0]["name"] == "Aristotle"
    assert payload["philosophers"][0]["turns"] == 2


def test_render_trace_snapshot(sample_trace_path: Path) -> None:
    log = po_viewer.load_trace(sample_trace_path)
    console = Console(record=True, width=100, color_system=None)

    po_viewer.render_trace(log, console=console)
    output = console.export_text()

    snapshot_path = Path("tests/snapshots/po_viewer_render.txt")
    assert output == snapshot_path.read_text(encoding="utf-8")


@pytest.fixture()
def sample_trace_path() -> Path:
    return Path("tests/data/sample_po_trace.json")
