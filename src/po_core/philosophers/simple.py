"""Simple philosopher profiles used by Po_self.

Each profile exposes a deterministic scoring helper so the ensemble output
remains stable for testing and documentation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


@dataclass(frozen=True)
class SimplePhilosopher:
    key: str
    name: str
    weight: float
    description: str
    keywords: Tuple[str, ...]

    def score(self, prompt: str) -> float:
        """Return a deterministic confidence score for the prompt."""

        normalized = prompt.lower()
        matches = sum(normalized.count(keyword) for keyword in self.keywords)
        return round(self.weight + 0.02 * matches, 2)

    def summary(self, prompt: str) -> str:
        return f"{self.name} reflects on '{prompt}'."

    def rationale(self, prompt: str) -> str:
        if any(keyword in prompt.lower() for keyword in self.keywords):
            return "Keyword resonance boosts confidence"
        return "Baseline philosophical weight applied"


DEFAULT_PHILOSOPHERS = (
    SimplePhilosopher(
        key="aristotle",
        name="Aristotle",
        weight=0.9,
        description="Virtue ethics and golden mean perspective",
        keywords=("virtue", "ethic", "mean"),
    ),
    SimplePhilosopher(
        key="nietzsche",
        name="Friedrich Nietzsche",
        weight=0.84,
        description="Will to power and authenticity",
        keywords=("power", "authentic", "will"),
    ),
    SimplePhilosopher(
        key="wittgenstein",
        name="Ludwig Wittgenstein",
        weight=0.8,
        description="Language games and meaning formation",
        keywords=("language", "meaning", "game"),
    ),
)

DEFAULT_PHILOSOPHER_KEYS = [profile.key for profile in DEFAULT_PHILOSOPHERS]


__all__ = ["SimplePhilosopher", "DEFAULT_PHILOSOPHERS", "DEFAULT_PHILOSOPHER_KEYS"]
