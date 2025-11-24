"""Orchestration logic for Po_self philosopher ensembles."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable, List, Sequence

from po_core.po_self.philosophers import PhilosopherAdapter, adapter_names, build_default_adapters
from po_core.po_self.philosophers.adapter import normalize_semantic_profile
from po_core.po_self.schemas import AggregationResult, AggregationTensors, PhilosopherContribution


@dataclass
class PoSelfManager:
    """Coordinate philosopher adapters and aggregate their contributions."""

    philosopher_adapters: List[PhilosopherAdapter]

    def __init__(self, philosopher_adapters: Iterable[PhilosopherAdapter] | None = None) -> None:
        self.philosopher_adapters = list(philosopher_adapters or build_default_adapters())

    def aggregate(self, prompt: str, seed: int | None = None) -> AggregationResult:
        contributions = self._collect_contributions(prompt=prompt, seed=seed)
        tensors = self._compose_tensors(contributions)
        return AggregationResult(contributions=contributions, tensors=tensors, prompt=prompt, seed=seed)

    def _collect_contributions(self, prompt: str, seed: int | None) -> List[PhilosopherContribution]:
        contributions: List[PhilosopherContribution] = []
        for idx, adapter in enumerate(self.philosopher_adapters):
            adapter_seed = None if seed is None else seed + idx
            contribution = adapter.evaluate(prompt, seed=adapter_seed)
            contributions.append(contribution)
        return contributions

    def _compose_tensors(self, contributions: Sequence[PhilosopherContribution]) -> AggregationTensors:
        if not contributions:
            return AggregationTensors(freedom_pressure=0.0, semantic_profile=[], blocked_tensor=0.0)

        freedom_values = [contribution.freedom_scalar for contribution in contributions]
        blocked_values = [contribution.blocked_scalar for contribution in contributions]
        semantic_vectors = list(normalize_semantic_profile(contributions))

        semantic_profile: List[float] = []
        if semantic_vectors:
            vector_length = len(semantic_vectors[0])
            for position in range(vector_length):
                semantic_profile.append(mean(vector[position] for vector in semantic_vectors))

        return AggregationTensors(
            freedom_pressure=mean(freedom_values),
            semantic_profile=semantic_profile,
            blocked_tensor=mean(blocked_values),
        )

    def describe(self) -> str:
        return ", ".join(adapter_names(self.philosopher_adapters))
