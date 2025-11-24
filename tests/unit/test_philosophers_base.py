"""Tests for philosopher base class behavior."""

import pytest

from po_core.philosophers.base import Philosopher


class ExamplePhilosopher(Philosopher):
    def __init__(self) -> None:
        super().__init__(name="Example", description="Example description")

    def reason(self, prompt: str, context=None):
        self.update_context(context)
        return {"reasoning": f"Echo: {prompt}", "perspective": "Example"}


def test_cannot_instantiate_base_class() -> None:
    with pytest.raises(TypeError):
        Philosopher(name="Invalid", description="Should not instantiate")  # type: ignore


def test_context_management_merges_values() -> None:
    philosopher = ExamplePhilosopher()
    philosopher.set_context({"foo": "bar"})
    philosopher.update_context({"bar": "baz"})

    assert philosopher.context == {"foo": "bar", "bar": "baz"}


def test_reason_receives_context() -> None:
    philosopher = ExamplePhilosopher()
    response = philosopher.reason("test prompt", context={"a": 1})

    assert response["reasoning"].startswith("Echo: test prompt")
    assert philosopher.context["a"] == 1

