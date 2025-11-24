import json

from click.testing import CliRunner

from po_core import __author__, __email__, __version__
from po_core.cli import main


def test_cli_hello_command():
    runner = CliRunner()
    result = runner.invoke(main, ["hello"])

    assert result.exit_code == 0
    assert "Po_core" in result.output
    assert "Welcome" not in result.output  # ensure original greeting kept


def test_cli_status_command():
    runner = CliRunner()
    result = runner.invoke(main, ["status"])

    assert result.exit_code == 0
    assert "Po_core Project Status" in result.output
    for check in ["Philosophical Framework", "Documentation", "Implementation", "Testing"]:
        assert check in result.output


def test_cli_version_command():
    runner = CliRunner()
    result = runner.invoke(main, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.output
    assert __author__ in result.output
    assert __email__ in result.output


def test_cli_prompt_command_returns_json(sample_prompt):
    runner = CliRunner()
    result = runner.invoke(main, ["prompt", sample_prompt, "--format", "json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["prompt"] == sample_prompt
    assert payload["philosophers"]
    assert len(payload["results"]) == len(payload["philosophers"])


def test_cli_prompt_command_returns_text(sample_prompt):
    runner = CliRunner()
    result = runner.invoke(main, ["prompt", sample_prompt, "--format", "text"])

    assert result.exit_code == 0
    assert "Prompt:" in result.output
    assert sample_prompt in result.output


def test_cli_log_command_exposes_log(sample_prompt, load_json_output):
    runner = CliRunner()
    result = runner.invoke(main, ["log", sample_prompt])

    assert result.exit_code == 0
    payload = load_json_output(result)
    assert payload["prompt"] == sample_prompt
    assert payload["events"][0]["event"] == "ensemble_started"
