"""Po_self: Philosophical Ensemble Module.

Provides a minimal ensemble that loads philosophers and generates a blended
response with freedom pressure metadata.
"""

from __future__ import annotations

from importlib import import_module
from typing import Dict, Iterable, List, Sequence

import click
from rich.console import Console
from rich.table import Table

from po_core.philosophers.base import Philosopher

console = Console()


class PoSelf:
    """Minimal orchestrator that coordinates a small ensemble of philosophers."""

    def __init__(self, philosopher_names: Sequence[str] | None = None) -> None:
        default = ["Sartre", "Jung", "Derrida"]
        self.philosopher_names = list(philosopher_names or default)
        self.philosophers = self._load_philosophers(self.philosopher_names)

    def _load_philosophers(self, names: Iterable[str]) -> List[Philosopher]:
        philosophers: List[Philosopher] = []
        for name in names:
            module = import_module(f"po_core.philosophers.{name.lower()}")
            philosopher_cls = getattr(module, name)
            philosophers.append(philosopher_cls())
        return philosophers

    def generate(self, prompt: str) -> Dict[str, object]:
        """Generate reasoning output using the available philosophers."""

        contributions = []
        tensions: List[float] = []
        for philosopher in self.philosophers:
            result = philosopher.reason(prompt, context={"mode": "ensemble"})
            contributions.append(
                {
                    "philosopher": philosopher.name,
                    "perspective": result.get("perspective"),
                    "excerpt": result.get("reasoning"),
                }
            )
            tension_value = result.get("tension") or len(result.get("reasoning", "")) % 10 / 10
            tensions.append(float(tension_value))

        freedom_pressure = round(sum(tensions) / max(len(tensions), 1), 2)
        commentary = (
            " | ".join(entry["perspective"] or "Perspective" for entry in contributions)
            + " synthesis"
        )

        return {
            "prompt": prompt,
            "freedom_pressure": freedom_pressure,
            "commentary": commentary,
            "contributions": contributions,
        }


def render_response(response: Dict[str, object]) -> None:
    """Render the generate() output as a rich table."""

    console.print(f"[bold magenta]🧠 Po_self[/bold magenta] responded to: [cyan]{response['prompt']}[/cyan]\n")

    table = Table(title="Philosopher Contributions", show_header=True, header_style="bold")
    table.add_column("Philosopher")
    table.add_column("Perspective")
    table.add_column("Excerpt")

    for contribution in response.get("contributions", []):
        table.add_row(
            str(contribution.get("philosopher", "Unknown")),
            str(contribution.get("perspective", "")),
            str(contribution.get("excerpt", "")),
        )

    console.print(table)
    console.print(
        f"Freedom pressure: [bold yellow]{response.get('freedom_pressure', 'N/A')}[/bold yellow]",
    )
    console.print(f"Commentary: {response.get('commentary', '')}\n")


@click.command()
@click.option("--prompt", required=True, help="Prompt to send to the philosophical ensemble.")
def cli(prompt: str) -> None:
    """Run the minimal Po_self ensemble for a given prompt."""

    engine = PoSelf()
    response = engine.generate(prompt)
    render_response(response)


__all__ = ["PoSelf", "render_response"]

