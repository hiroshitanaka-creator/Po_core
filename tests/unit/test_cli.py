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


def test_cli_prompt_command_returns_json(sample_prompt):
    runner = CliRunner()
    result = runner.invoke(main, ["prompt", sample_prompt, "--format", "json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["prompt"] == sample_prompt
    assert payload["responses"]


def test_cli_log_command_exposes_log(sample_prompt):
    runner = CliRunner()
    result = runner.invoke(main, ["log", sample_prompt])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["prompt"] == sample_prompt
    assert "events" in payload


def test_cli_sample_flags_show_attribution():
    runner = CliRunner()
    result = runner.invoke(main, ["hello", "--sample"])

    assert result.exit_code == 0
    assert "Consensus Lead" in result.output
