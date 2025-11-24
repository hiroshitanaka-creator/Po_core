from click.testing import CliRunner

from po_core import __version__
from po_core.cli import hello, status, version


def test_hello() -> None:
    runner = CliRunner()
    result = runner.invoke(hello)
    assert result.exit_code == 0
    assert "Po_core" in result.output


def test_status() -> None:
    runner = CliRunner()
    result = runner.invoke(status)
    assert result.exit_code == 0
    assert "Project Status" in result.output


def test_version() -> None:
    runner = CliRunner()
    result = runner.invoke(version)
    assert result.exit_code == 0
    assert __version__ in result.output
