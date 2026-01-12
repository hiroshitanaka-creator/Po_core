from click.testing import CliRunner

from po_core.cli import main


def test_hello_command_outputs_welcome_message() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["hello"])

    assert result.exit_code == 0
    assert "Po_core" in result.output
    assert "Philosophy-Driven AI System" in result.output


def test_status_command_reports_project_progress() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["status"])

    assert result.exit_code == 0
    assert "Project Status" in result.output
    assert "Testing" in result.output
    assert "Visualization" in result.output


def test_version_command_displays_project_metadata() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["version"])

    assert result.exit_code == 0
    assert "Po_core" in result.output
    assert "Author" in result.output
    assert "Email" in result.output
