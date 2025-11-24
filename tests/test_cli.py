from pathlib import Path

from click.testing import CliRunner

from po_core import cli
from po_core.po_trace import demo_trace_events, load_trace, save_trace


def test_hello_status_version_commands() -> None:
    runner = CliRunner()

    hello = runner.invoke(cli.main, ["hello"])
    assert hello.exit_code == 0
    assert "Po_core" in hello.output

    status = runner.invoke(cli.main, ["status"])
    assert status.exit_code == 0
    assert "Project Status" in status.output

    version = runner.invoke(cli.main, ["version"])
    assert version.exit_code == 0
    assert "Po_core" in version.output


def test_trace_command_writes_log(tmp_path: Path) -> None:
    runner = CliRunner()
    log_path = tmp_path / "demo.jsonl"

    result = runner.invoke(cli.main, ["trace", "--log", str(log_path)])
    assert result.exit_code == 0
    assert log_path.exists()

    events = load_trace(log_path)
    assert len(events) == len(demo_trace_events())
    assert any(not event.accepted for event in events)


def test_self_command_generates_output() -> None:
    runner = CliRunner()
    result = runner.invoke(cli.main, ["self", "--prompt", "What is freedom?"])

    assert result.exit_code == 0
    assert "Freedom pressure" in result.output
    assert "Philosopher" in result.output


def test_view_command_renders_trace(tmp_path: Path) -> None:
    runner = CliRunner()
    trace_path = tmp_path / "trace.jsonl"
    save_trace(demo_trace_events(), trace_path)

    result = runner.invoke(cli.main, ["view", "--trace", str(trace_path)])
    assert result.exit_code == 0
    assert "Philosopher Contributions" in result.output
    assert "Tension trend" in result.output
