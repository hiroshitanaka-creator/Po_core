from io import StringIO

from rich.console import Console

from po_core.po_viewer import render_reason_log


def test_render_reason_log_outputs_sections(ensemble_snapshot):
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True, color_system=None, width=120)

    render_reason_log(ensemble_snapshot, console=console)

    output = buffer.getvalue()
    assert "Philosopher Scores" in output
    assert "Event Timeline" in output
    assert "Aristotle" in output
    assert "ensemble_started" in output
