"""Philosophical ensemble orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional

import click
from rich.console import Console
from rich.table import Table

from po_core.philosophers import Philosopher
from po_core.philosophers import (  # type: ignore
    Arendt,
    Aristotle,
    Badiou,
    Confucius,
    Deleuze,
    Derrida,
    Dewey,
    Heidegger,
    Jung,
    Kierkegaard,
    Lacan,
    Levinas,
    MerleauPonty,
    Nietzsche,
    Peirce,
    Sartre,
    WabiSabi,
    Watsuji,
    Wittgenstein,
    Zhuangzi,
)


console = Console()


@dataclass
class PhilosopherResponse:
    name: str
    reasoning: str
    perspective: str
    metadata: Mapping[str, object]
    score: float


class PhilosopherRegistry:
    """Lightweight registry for philosopher implementations."""

    def __init__(self) -> None:
        self._registry: Dict[str, Philosopher] = {}
        self._populate_defaults()

    def _populate_defaults(self) -> None:
        for philo in [
            Arendt(),
            Aristotle(),
            Badiou(),
            Confucius(),
            Deleuze(),
            Derrida(),
            Dewey(),
            Heidegger(),
            Jung(),
            Kierkegaard(),
            Lacan(),
            Levinas(),
            MerleauPonty(),
            Nietzsche(),
            Peirce(),
            Sartre(),
            WabiSabi(),
            Watsuji(),
            Wittgenstein(),
            Zhuangzi(),
        ]:
            self._registry[philo.name] = philo

    @property
    def names(self) -> List[str]:
        return sorted(self._registry.keys())

    def get_selected(self, selected: Optional[Iterable[str]]) -> List[Philosopher]:
        if not selected:
            return list(self._registry.values())
        chosen = []
        for name in selected:
            philosopher = self._registry.get(name)
            if philosopher:
                chosen.append(philosopher)
        return chosen


class PhilosopherEngine:
    """Broadcast prompts to philosophers and aggregate their perspectives."""

    def __init__(self, registry: Optional[PhilosopherRegistry] = None) -> None:
        self.registry = registry or PhilosopherRegistry()

    def run(
        self, prompt: str, *, selected: Optional[Iterable[str]] = None
    ) -> Dict[str, object]:
        philosophers = self.registry.get_selected(selected)
        responses: List[PhilosopherResponse] = []
        if not philosophers:
            return {"combined_reasoning": "", "responses": responses, "score": 0.0}

        for philosopher in philosophers:
            payload = philosopher.reason(prompt, context={"prompt": prompt})
            reasoning = str(payload.get("reasoning", ""))
            perspective = str(payload.get("perspective", philosopher.description))
            metadata = payload.get("metadata", {"philosopher": philosopher.name})
            score = float(payload.get("score", 1.0 / len(philosophers)))
            responses.append(
                PhilosopherResponse(
                    name=philosopher.name,
                    reasoning=reasoning,
                    perspective=perspective,
                    metadata=metadata,
                    score=score,
                )
            )

        combined = self._combine(responses)
        return {
            "combined_reasoning": combined,
            "responses": responses,
            "score": sum(r.score for r in responses) / len(responses),
        }

    @staticmethod
    def _combine(responses: List[PhilosopherResponse]) -> str:
        summaries = [
            f"[{resp.name}] {resp.perspective}: {resp.reasoning} (score={resp.score:.2f})"
            for resp in responses
        ]
        return "\n".join(summaries)


@click.group()
def cli() -> None:
    """Po_self CLI entry point."""


@cli.command()
@click.option("--prompt", required=True, help="Prompt to broadcast to philosophers")
@click.option(
    "--philosopher",
    multiple=True,
    help="Optional philosopher names to restrict the ensemble",
)
def run(prompt: str, philosopher: Iterable[str]) -> None:
    """Execute the mini philosopher ensemble and display merged reasoning."""

    engine = PhilosopherEngine()
    result = engine.run(prompt, selected=philosopher)
    table = Table(title="Po_self Ensemble Result")
    table.add_column("Philosopher")
    table.add_column("Perspective")
    table.add_column("Reasoning")
    table.add_column("Score")

    for resp in result["responses"]:
        table.add_row(resp.name, resp.perspective, resp.reasoning, f"{resp.score:.2f}")

    console.print(table)
    console.print("\n[bold]Combined Reasoning[/bold]")
    console.print(result["combined_reasoning"])


if __name__ == "__main__":
    cli()
