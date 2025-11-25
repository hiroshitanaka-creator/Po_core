import json

import pytest

pytest.importorskip("rich")

from po_core import __version__
from po_core.cli import main


def test_cli_hello_command(cli_runner):
    result = cli_runner.invoke(main, ["hello"])

    assert result.exit_code == 0
    assert "Po_core" in result.output


def test_cli_status_command(cli_runner):
    result = cli_runner.invoke(main, ["status"])

    assert result.exit_code == 0
    assert "Project Status" in result.output


def test_cli_version_command(cli_runner):
    result = cli_runner.invoke(main, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_prompt_command_returns_json(cli_runner, sample_prompt):
    result = cli_runner.invoke(main, ["prompt", sample_prompt, "--format", "json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["prompt"] == sample_prompt
    assert payload["results"]


def test_cli_log_command_exposes_log(cli_runner, sample_prompt):
    result = cli_runner.invoke(main, ["log", sample_prompt])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["prompt"] == sample_prompt
    assert "events" in payload
