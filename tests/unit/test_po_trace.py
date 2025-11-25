import pytest
from click.testing import CliRunner

pytest.importorskip("rich")

from po_core.po_trace import cli


def test_po_trace_cli_announces_logging_module():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert "Po_trace - Reasoning Audit Log" in result.output
    assert "Implementation coming soon" in result.output
