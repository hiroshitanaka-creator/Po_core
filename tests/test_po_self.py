from click.testing import CliRunner

from po_core.po_self import PhilosopherEngine, PhilosopherRegistry, cli as self_cli


def test_registry_has_entries() -> None:
    registry = PhilosopherRegistry()
    assert len(registry.names) > 3


def test_engine_combines_reasoning() -> None:
    engine = PhilosopherEngine()
    result = engine.run("What is courage?", selected=list(engine.registry.names)[:2])
    assert result["combined_reasoning"]
    assert result["responses"]


def test_po_self_cli_run() -> None:
    runner = CliRunner()
    result = runner.invoke(self_cli, ["run", "--prompt", "Test prompt", "--philosopher", "Friedrich Nietzsche"])
    assert result.exit_code == 0
    assert "Combined Reasoning" in result.output
