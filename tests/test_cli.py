import json
from pathlib import Path

from click.testing import CliRunner

from po_core import __version__
from po_core.cli import main


def test_cli_basics():
    runner = CliRunner()

    hello = runner.invoke(main, ["hello"])
    status = runner.invoke(main, ["status"])
    version = runner.invoke(main, ["version"])

    assert hello.exit_code == 0
    assert status.exit_code == 0
    assert version.exit_code == 0

    assert "Po_core" in hello.output
    assert "Project Status" in status.output
    assert __version__ in version.output


def test_prompt_command_matches_snapshot(sample_prompt, ensemble_snapshot):
    runner = CliRunner()
    result = runner.invoke(main, ["prompt", sample_prompt, "--format", "json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload == ensemble_snapshot


def test_log_command_exposes_trace(sample_prompt, ensemble_snapshot):
    runner = CliRunner()
    result = runner.invoke(main, ["log", sample_prompt])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload == ensemble_snapshot["log"]
    assert payload["created_at"].endswith("Z")


def test_po_trace_command_writes_file(sample_prompt):
    runner = CliRunner()
    with runner.isolated_filesystem():
        path = Path("trace.json")
        result = runner.invoke(main, ["po-trace", sample_prompt, "--output", str(path)])

        assert result.exit_code == 0
        assert path.exists()
        saved = json.loads(path.read_text())
        assert saved["prompt"] == sample_prompt
        assert saved["events"]


def test_view_log_command_renders(sample_prompt, ensemble_snapshot):
    runner = CliRunner()
    with runner.isolated_filesystem():
        fixture_path = Path("snapshot.json")
        fixture_path.write_text(json.dumps(ensemble_snapshot))

        result = runner.invoke(main, ["view-log", "--file", str(fixture_path)])

        assert result.exit_code == 0
        assert "Philosopher Scores" in result.output
        assert "Event Timeline" in result.output
