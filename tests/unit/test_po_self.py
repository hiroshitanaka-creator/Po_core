"""Tests for the PoSelf reasoning orchestrator."""

from po_core.po_self import PoSelf, run_ensemble


def test_loads_philosophers() -> None:
    engine = PoSelf()

    assert len(engine.available_names()) > 0


def test_run_prompt_returns_outputs() -> None:
    engine = PoSelf()
    result = engine.run_prompt("What is justice?", selected=engine.available_names()[:2])

    assert result.outputs
    assert result.summary
    assert len(result.influences) == len(result.outputs)


def test_helper_run_ensemble() -> None:
    result = run_ensemble("How do we live well?", context={"tone": "reflective"})

    assert result.prompt.startswith("How")
    assert result.outputs

