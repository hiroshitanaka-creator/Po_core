import json

from click.testing import CliRunner

from po_core import cli
from po_core.po_self import PoSelf
from po_core.po_trace import PoTrace


def test_run_and_trace_commands(monkeypatch, tmp_path):
    tracer = PoTrace(path=tmp_path / "traces.jsonl")
    engine = PoSelf(tracer=tracer)

    def build_services():
        return {"tracer": tracer, "engine": engine}

    monkeypatch.setattr(cli, "_build_services", build_services)

    runner = CliRunner()
    with runner.isolated_filesystem():
        run_result = runner.invoke(cli.main, ["run", "Test prompt", "--context", json.dumps({"foo": "bar"})])
        assert run_result.exit_code == 0
        assert "Aggregate reasoning" in run_result.output

        list_result = runner.invoke(cli.main, ["trace", "list"])
        assert list_result.exit_code == 0
        assert "Recent traces" in list_result.output

        show_result = runner.invoke(cli.main, ["trace", "show", "0"])
        assert show_result.exit_code == 0
        assert "Test prompt" in show_result.output


def test_status_command(monkeypatch, tmp_path):
    tracer = PoTrace(path=tmp_path / "traces.jsonl")
    engine = PoSelf(tracer=tracer)

    def build_services():
        return {"tracer": tracer, "engine": engine}

    monkeypatch.setattr(cli, "_build_services", build_services)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["status"])
    assert result.exit_code == 0
    assert "Philosophers implemented" in result.output
