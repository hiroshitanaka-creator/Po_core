import pytest

from po_core.po_self import PoSelf


def test_po_self_validates_prompt():
    engine = PoSelf()
    with pytest.raises(ValueError):
        engine.run("")


def test_po_self_runs_and_aggregates():
    engine = PoSelf()
    result = engine.run("How should we live?", context={"audience": "student"})

    assert "Aggregate" not in result["reasoning"]  # ensure string built by merge
    assert len(result["perspectives"]) == len(engine.philosophers)
    for perspective in result["perspectives"]:
        assert perspective["name"]
        assert isinstance(perspective["reasoning"], str)
    assert result["metadata"]["context_used"] is True


def test_po_self_context_validation():
    engine = PoSelf()
    with pytest.raises(TypeError):
        engine.run("Test", context=["not", "a", "dict"])  # type: ignore[arg-type]
