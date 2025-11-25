"""Philosopher tensor emitters for the Po_self ensemble."""
from __future__ import annotations

from dataclasses import dataclass

from .tensor import TensorState


@dataclass
class Philosopher:
    """Base philosopher interface."""

    name: str
    focus: str

    def evaluate(self, prompt: str, base_tensor: TensorState) -> TensorState:
        raise NotImplementedError


class SartrePhilosopher(Philosopher):
    """Existential weight based on choice density."""

    def __init__(self) -> None:
        super().__init__(name="sartre", focus="freedom")

    def evaluate(self, prompt: str, base_tensor: TensorState) -> TensorState:
        words = len(prompt.split())
        choices = prompt.count(" or ") + 1
        intensity = min(1.0, choices / max(1, words))
        value = round(intensity * (0.6 + (words % 5) * 0.05), 3)
        return TensorState(
            name=self.name,
            value=value,
            description="Existential tension between options and commitment.",
            metadata={"choices": choices, "word_count": words, "weight": 0.37},
        )


class JungPhilosopher(Philosopher):
    """Archetypal resonance derived from imagery density."""

    def __init__(self) -> None:
        super().__init__(name="jung", focus="archetypes")

    def evaluate(self, prompt: str, base_tensor: TensorState) -> TensorState:
        symbols = sum(1 for token in prompt.split() if token.istitle())
        resonance = round(min(1.0, symbols / (base_tensor.metadata["word_count"] or 1)), 3)
        return TensorState(
            name=self.name,
            value=resonance,
            description="Archetypal symbols resonating within the prompt.",
            metadata={"symbols": symbols, "weight": 0.33},
        )


class DerridaPhilosopher(Philosopher):
    """Deconstructive drift measured via contrast markers."""

    def __init__(self) -> None:
        super().__init__(name="derrida", focus="différance")

    def evaluate(self, prompt: str, base_tensor: TensorState) -> TensorState:
        binary_pairs = prompt.count(" vs ") + prompt.count(" versus ")
        punctuation = sum(prompt.count(ch) for ch in ["?", "!"])
        trace = round(min(1.0, (binary_pairs + punctuation) / (1 + base_tensor.metadata["word_count"])), 3)
        return TensorState(
            name=self.name,
            value=trace,
            description="Instability detected in textual oppositions.",
            metadata={"binary_pairs": binary_pairs, "punctuation": punctuation, "weight": 0.3},
        )
