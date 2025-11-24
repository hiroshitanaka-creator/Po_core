"""Philosophical ensemble reasoning engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from po_core.philosophers import (
    Aristotle,
    Confucius,
    Derrida,
    Heidegger,
    Nietzsche,
    Philosopher,
)
from po_core.po_trace import PoTrace, TraceEntry


@dataclass
class PhilosopherResult:
    """Structured output for a single philosopher run."""

    name: str
    perspective: str
    reasoning: str
    tension: Optional[str]
    raw: Dict[str, Any]


class PoSelf:
    """Coordinate multiple philosophers and aggregate their perspectives."""

    def __init__(
        self,
        philosophers: Optional[List[Philosopher]] = None,
        tracer: Optional[PoTrace] = None,
    ) -> None:
        self.philosophers = philosophers or self._default_philosophers()
        self.tracer = tracer or PoTrace()

    @staticmethod
    def _default_philosophers() -> List[Philosopher]:
        return [Aristotle(), Nietzsche(), Confucius(), Derrida(), Heidegger()]

    def run(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the ensemble reasoning flow.

        Args:
            prompt: A non-empty prompt to analyze.
            context: Optional dictionary with additional metadata.

        Returns:
            Structured dictionary containing merged reasoning, individual
            perspectives, tensions, and metadata describing the run.
        """

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        if context is not None and not isinstance(context, dict):
            raise TypeError("context must be a mapping if provided")

        resolved_context = context or {}
        individual_results: List[PhilosopherResult] = []
        tensions: List[Dict[str, str]] = []

        for philosopher in self.philosophers:
            output = philosopher.reason(prompt, resolved_context)
            result = PhilosopherResult(
                name=philosopher.name,
                perspective=output.get("perspective", ""),
                reasoning=output.get("reasoning", ""),
                tension=output.get("tension"),
                raw=output,
            )
            individual_results.append(result)
            if result.tension:
                tensions.append({"source": result.name, "tension": result.tension})

        aggregated_reasoning = self._merge_reasoning(individual_results)
        response = {
            "prompt": prompt,
            "reasoning": aggregated_reasoning,
            "perspectives": [r.__dict__ for r in individual_results],
            "tensions": tensions,
            "metadata": {
                "philosophers": [p.name for p in self.philosophers],
                "context_used": bool(resolved_context),
            },
        }

        if self.tracer:
            self.tracer.record(prompt=prompt, context=resolved_context, result=response)

        return response

    def _merge_reasoning(self, results: List[PhilosopherResult]) -> str:
        """Combine individual perspectives into a coherent summary."""

        lines = []
        for result in results:
            lines.append(f"{result.name}: {result.reasoning}")
        return "\n".join(lines)


__all__ = ["PoSelf", "PhilosopherResult", "TraceEntry"]
