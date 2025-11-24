import pytest
from click.testing import CliRunner

from po_core import __version__
from po_core.cli import main


@pytest.mark.unit
def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Po_core: Philosophy-Driven AI System" in result.output
    assert "hello" in result.output


@pytest.mark.unit
def test_cli_version_option():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output


@pytest.mark.unit
def test_cli_hello_command():
    runner = CliRunner()
    result = runner.invoke(main, ["hello"])

    assert result.exit_code == 0
    assert "Po_core へようこそ" in result.output
    assert "Po_core へようこそ" in result.stdout
