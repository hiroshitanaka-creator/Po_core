"""
Po_self: Philosophical Ensemble Module

Coordinates philosopher instances to provide collective reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence

import po_core.philosophers as philosophers
from po_core.philosophers import Philosopher


@dataclass
class PhilosopherResponse:
    """Normalized response structure for a single philosopher."""

    name: str
    perspective: str
    reasoning: str
    metadata: Dict[str, Any]
    raw: Dict[str, Any]


@dataclass
class EnsembleResult:
    """Combined response from the philosopher ensemble."""

    prompt: str
    summary: str
    influences: List[Dict[str, Any]]
    outputs: List[PhilosopherResponse]
    failed: List[str]


class PoSelf:
    """Orchestrates philosopher reasoning and aggregates responses."""

    def __init__(self, selected: Optional[Sequence[str]] = None) -> None:
        self._philosophers = self._load_philosophers(selected)

    def _load_philosophers(
        self, selected: Optional[Sequence[str]] = None
    ) -> MutableMapping[str, Philosopher]:
        available: MutableMapping[str, Philosopher] = {}
        wanted = {name.lower() for name in selected} if selected else None

        for name in getattr(philosophers, "__all__", []):
            if name == "Philosopher":
                continue
            cls = getattr(philosophers, name, None)
            if not cls or not issubclass(cls, Philosopher):
                continue
            instance = cls()
            if wanted and instance.name.lower() not in wanted and name.lower() not in wanted:
                continue
            available[instance.name] = instance
        return available

    @property
    def philosophers(self) -> Mapping[str, Philosopher]:
        return dict(self._philosophers)

    def available_names(self) -> List[str]:
        return sorted(self._philosophers.keys())

    def run_prompt(
        self,
        prompt: str,
        context: Optional[Mapping[str, Any]] = None,
        selected: Optional[Sequence[str]] = None,
    ) -> EnsembleResult:
        context = dict(context) if context else {}
        outputs: List[PhilosopherResponse] = []
        failed: List[str] = []

        chosen = {name.lower() for name in selected} if selected else None

        for name, philosopher in sorted(self._philosophers.items()):
            if chosen and name.lower() not in chosen:
                continue
            philosopher.set_context(context)
            try:
                raw = philosopher.reason(prompt, context=context)
                outputs.append(
                    PhilosopherResponse(
                        name=philosopher.name,
                        perspective=str(raw.get("perspective", philosopher.__class__.__name__)),
                        reasoning=str(raw.get("reasoning", "")),
                        metadata={"philosopher": philosopher.name, **raw.get("metadata", {})},
                        raw=raw,
                    )
                )
            except Exception:
                failed.append(philosopher.name)

        influences = self._calculate_influences(outputs)
        summary = self.combine_reasoning(outputs)

        return EnsembleResult(
            prompt=prompt,
            summary=summary,
            influences=influences,
            outputs=outputs,
            failed=failed,
        )

    def _calculate_influences(self, outputs: Iterable[PhilosopherResponse]) -> List[Dict[str, Any]]:
        outputs_list = list(outputs)
        total = len(outputs_list) or 1
        weight = 1 / total
        return [
            {
                "name": response.name,
                "perspective": response.perspective,
                "weight": round(weight, 3),
            }
            for response in outputs_list
        ]

    def combine_reasoning(self, outputs: Iterable[PhilosopherResponse]) -> str:
        thoughts = [f"{response.name}: {response.reasoning}" for response in outputs if response.reasoning]
        if not thoughts:
            return "No philosophical responses were generated."
        return " \n---\n".join(thoughts)


def run_ensemble(prompt: str, context: Optional[Mapping[str, Any]] = None) -> EnsembleResult:
    """Helper for quickly running the ensemble from external callers."""

    engine = PoSelf()
    return engine.run_prompt(prompt=prompt, context=context)

