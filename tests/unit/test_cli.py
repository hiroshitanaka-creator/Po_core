"""CLI smoke tests using Click's runner."""

from click.testing import CliRunner

from po_core import __version__
from po_core.cli import main


def test_hello_command() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["hello"])

    assert result.exit_code == 0
    assert "Po_core" in result.output
    assert __version__ in result.output


def test_status_command() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["status"])

    assert result.exit_code == 0
    assert "Philosophers loaded" in result.output


def test_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.output

