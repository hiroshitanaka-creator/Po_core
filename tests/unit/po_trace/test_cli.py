from click.testing import CliRunner

from po_core.cli import main


def test_trace_command_outputs_summary() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["trace", "hello world", "--steps", "2"])

    assert result.exit_code == 0
    assert "Trace Steps" in result.output
    assert "hello world" in result.output
    assert "Δ Semantic" in result.output
