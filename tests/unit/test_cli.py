import json

from click.testing import CliRunner

from po_core import __version__
from po_core.cli import main


def test_cli_hello_command():
    runner = CliRunner()
    result = runner.invoke(main, ["hello"])

    assert result.exit_code == 0
    assert "Po_core" in result.output


def test_cli_status_command():
    runner = CliRunner()
    result = runner.invoke(main, ["status"])

    assert result.exit_code == 0
    assert "Project Status" in result.output


def test_cli_version_command():
    runner = CliRunner()
    result = runner.invoke(main, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_prompt_command_returns_json(sample_prompt, trace_sink):
    runner = CliRunner()
    result = runner.invoke(main, ["prompt", sample_prompt, "--format", "json"], env={"PO_TRACE_PATH": str(trace_sink)})

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["prompt"] == sample_prompt
    assert payload["results"]


def test_cli_log_command_exposes_log(sample_prompt, trace_sink):
    runner = CliRunner()
    result = runner.invoke(main, ["log", sample_prompt], env={"PO_TRACE_PATH": str(trace_sink)})

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["prompt"] == sample_prompt
    assert "events" in payload


def test_cli_trace_show_filters_latest_trace(sample_prompt, trace_sink):
    runner = CliRunner()
    # Run once to create a trace
    runner.invoke(main, ["prompt", sample_prompt], env={"PO_TRACE_PATH": str(trace_sink)})

    result = runner.invoke(
        main,
        ["trace", "show", "--philosopher", "aristotle"],
        env={"PO_TRACE_PATH": str(trace_sink)},
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["steps"]
    assert all(step["philosopher"] == "aristotle" for step in payload["steps"])
