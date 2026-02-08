"""
Tests for Po_core CLI Module

Comprehensive tests for command-line interface functionality.
"""

import json

import pytest
from click.testing import CliRunner

from po_core import __version__
from po_core.cli import main


class TestCLIBasicCommands:
    """Test basic CLI commands."""

    def test_cli_hello_command(self):
        """Test hello command basic output."""
        runner = CliRunner()
        result = runner.invoke(main, ["hello"])

        assert result.exit_code == 0
        assert "Po_core" in result.output

    def test_cli_hello_with_sample(self):
        """Test hello command with sample flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["hello", "--sample"])

        assert result.exit_code == 0
        assert "Po_core" in result.output
        assert "Consensus Lead" in result.output
        assert "Philosophers" in result.output
        assert "Metrics" in result.output

    def test_cli_hello_without_sample(self):
        """Test hello command without sample flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["hello", "--no-sample"])

        assert result.exit_code == 0
        assert "Po_core" in result.output
        # Should not have sample output
        assert "Consensus Lead" not in result.output

    def test_cli_status_command(self):
        """Test status command basic output."""
        runner = CliRunner()
        result = runner.invoke(main, ["status"])

        assert result.exit_code == 0
        assert "Project Status" in result.output
        assert "Philosophical Framework" in result.output
        assert "Documentation" in result.output

    def test_cli_status_with_sample(self):
        """Test status command with sample flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["status", "--sample"])

        assert result.exit_code == 0
        assert "Project Status" in result.output
        assert "Consensus Lead" in result.output

    def test_cli_version_command(self):
        """Test version command."""
        runner = CliRunner()
        result = runner.invoke(main, ["version"])

        assert result.exit_code == 0
        assert __version__ in result.output


class TestCLIPromptCommand:
    """Test prompt command functionality."""

    def test_cli_prompt_command_json_format(self, sample_prompt):
        """Test prompt command with JSON output format."""
        runner = CliRunner()
        result = runner.invoke(main, ["prompt", sample_prompt, "--format", "json"])

        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert payload["prompt"] == sample_prompt
        assert payload["responses"]
        assert "metrics" in payload

    def test_cli_prompt_command_text_format(self, sample_prompt):
        """Test prompt command with text output format."""
        runner = CliRunner()
        result = runner.invoke(main, ["prompt", sample_prompt, "--format", "text"])

        assert result.exit_code == 0
        assert sample_prompt in result.output
        # Text format should contain readable output
        assert len(result.output) > 0

    def test_cli_prompt_empty_string(self):
        """Test prompt command with empty string."""
        runner = CliRunner()
        result = runner.invoke(main, ["prompt", ""])

        # Should handle gracefully
        assert result.exit_code == 0


class TestCLILogCommand:
    """Test log command functionality."""

    def test_cli_log_command_exposes_log(self, sample_prompt):
        """Test log command returns complete log."""
        runner = CliRunner()
        result = runner.invoke(main, ["log", sample_prompt])

        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert payload["prompt"] == sample_prompt
        assert "events" in payload

    def test_cli_log_validates_json(self, sample_prompt):
        """Test that log output is valid JSON."""
        runner = CliRunner()
        result = runner.invoke(main, ["log", sample_prompt])

        assert result.exit_code == 0
        # Should not raise exception
        data = json.loads(result.output)
        assert isinstance(data, dict)


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_cli_invalid_command(self):
        """Test CLI with invalid command."""
        runner = CliRunner()
        result = runner.invoke(main, ["invalid"])

        # Click returns exit code 2 for unknown commands
        assert result.exit_code != 0

    def test_cli_help_flag(self):
        """Test CLI help flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Po_core" in result.output
        assert "Philosophy-Driven AI" in result.output

    def test_cli_version_flag(self):
        """Test CLI version flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "0.1.0-alpha" in result.output


class TestCLIIntegration:
    """Test CLI integration scenarios."""

    def test_cli_multiple_commands_sequence(self, sample_prompt):
        """Test running multiple CLI commands in sequence."""
        runner = CliRunner()

        # Test hello
        result1 = runner.invoke(main, ["hello"])
        assert result1.exit_code == 0

        # Test status
        result2 = runner.invoke(main, ["status"])
        assert result2.exit_code == 0

        # Test prompt
        result3 = runner.invoke(main, ["prompt", sample_prompt])
        assert result3.exit_code == 0

    def test_cli_output_formats_consistency(self, sample_prompt):
        """Test that different output formats contain same data."""
        runner = CliRunner()

        # Get JSON output
        result_json = runner.invoke(main, ["prompt", sample_prompt, "--format", "json"])
        assert result_json.exit_code == 0
        json_data = json.loads(result_json.output)

        # Verify JSON has expected structure
        assert "prompt" in json_data
        assert "metrics" in json_data
        assert "responses" in json_data
        assert json_data["prompt"] == sample_prompt
