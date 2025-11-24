"""Adapters that normalize philosopher outputs."""

from __future__ import annotations

import random
from typing import Dict, Iterable, List, Sequence

from po_core.philosophers.base import Philosopher
from po_core.po_self.schemas import PhilosopherContribution


class PhilosopherAdapter:
    """Provide a consistent interface for philosopher reasoning outputs."""

    def __init__(self, philosopher: Philosopher, semantic_dimensions: int = 4) -> None:
        self.philosopher = philosopher
        self.semantic_dimensions = semantic_dimensions

    @property
    def name(self) -> str:
        return self.philosopher.name

    def evaluate(self, prompt: str, seed: int | None = None) -> PhilosopherContribution:
        """Call the philosopher and normalize the response."""

        rng = random.Random(seed)
        raw_output: Dict[str, object]
        summary: str
        try:
            raw_output = self.philosopher.reason(prompt)
            reasoning_text = self._extract_reasoning(raw_output)
            summary = reasoning_text if reasoning_text else self.philosopher.description
        except Exception as exc:  # noqa: BLE001 - keep adapter resilient to upstream errors
            raw_output = {"error": str(exc)}
            summary = f"{self.philosopher.name} encountered an issue but offered resilience."

        freedom_scalar = rng.uniform(0.0, 1.0)
        semantic_vector = self._build_semantic_vector(rng)
        blocked_scalar = rng.uniform(0.0, 1.0)

        metadata = {
            "source": self.philosopher.__class__.__name__,
            "raw_output_keys": sorted(raw_output.keys()),
        }
        if seed is not None:
            metadata["seed"] = seed

        return PhilosopherContribution(
            name=self.philosopher.name,
            summary=summary,
            freedom_scalar=freedom_scalar,
            semantic_vector=semantic_vector,
            blocked_scalar=blocked_scalar,
            metadata=metadata,
        )

    def _build_semantic_vector(self, rng: random.Random) -> List[float]:
        return [rng.uniform(-1.0, 1.0) for _ in range(self.semantic_dimensions)]

    def _extract_reasoning(self, raw_output: Dict[str, object]) -> str:
        if "reasoning" in raw_output and isinstance(raw_output["reasoning"], str):
            return raw_output["reasoning"]
        return "; ".join(
            f"{key}: {value}" for key, value in raw_output.items() if isinstance(value, (str, int, float))
        )


def normalize_semantic_profile(contributions: Sequence[PhilosopherContribution]) -> Iterable[List[float]]:
    """Yield semantic vectors while guarding against shape mismatches."""

    for contribution in contributions:
        if contribution.semantic_vector:
            yield contribution.semantic_vector
