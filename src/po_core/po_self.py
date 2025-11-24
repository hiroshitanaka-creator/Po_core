"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers
as interacting tensors.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Sequence

import click
from rich.console import Console

console = Console()


@dataclass
class PhilosopherModule:
    """Represents a philosopher's contribution as a tensor component.

    Attributes map to the README architecture:
    - ``weighting`` mirrors the philosopher's influence within the Freedom Pressure tensor (F_P).
    - ``stance`` captures the directional semantic pull that shapes the Semantic Delta (Δs).
    - ``generator`` allows future replacement with tensor math or LLM hooks while keeping a stable API.
    """

    name: str
    stance: str
    weighting: float
    generator: Callable[[str, "PhilosopherModule"], "PhilosopherContribution"]

    def contribute(self, prompt: str) -> "PhilosopherContribution":
        """Generate a structured contribution for the given prompt."""

        return self.generator(prompt, self)


@dataclass
class PhilosopherContribution:
    """Structured output from a philosopher module.

    Each contribution carries an interpretable slice of the ensemble tensors:
    - ``freedom_pressure``: localized pressure before aggregation into F_P.
    - ``semantic_delta``: movement proposed by this philosopher for Δs.
    - ``blocked_tensor``: concerns intentionally held back (B), tracing absence as in the README diagram.
    - ``narrative``: human-readable reasoning that can later be replaced by numeric tensors.
    """

    philosopher: str
    narrative: str
    freedom_pressure: float
    semantic_delta: float
    blocked_tensor: str


@dataclass
class ReasoningResult:
    """Aggregate reasoning output from the Po_self ensemble.

    The result stitches together per-philosopher contributions into the three
    architectural tensors (Freedom Pressure, Semantic Delta, Blocked Tensor).
    """

    prompt: str
    contributions: Sequence[PhilosopherContribution]
    total_freedom_pressure: float
    aggregate_semantic_delta: float
    blocked_tensor_notes: List[str] = field(default_factory=list)

    def to_text(self) -> str:
        """Render a console-friendly representation of the reasoning."""

        lines = [f"Prompt: {self.prompt}"]
        lines.append(f"Total Freedom Pressure: {self.total_freedom_pressure:.2f}")
        lines.append(f"Aggregate Semantic Delta: {self.aggregate_semantic_delta:.2f}")
        if self.blocked_tensor_notes:
            lines.append("Blocked Tensor Signals:")
            lines.extend(f"- {note}" for note in self.blocked_tensor_notes)
        lines.append("Philosopher Contributions:")
        for contribution in self.contributions:
            lines.append(
                f"  * {contribution.philosopher}: {contribution.narrative}"
                f" (F_P={contribution.freedom_pressure:.2f}, Δs={contribution.semantic_delta:.2f})"
            )
        return "\n".join(lines)


class EnsembleCoordinator:
    """Coordinates philosopher modules and aggregates their tensor slices.

    This class is intentionally lightweight; the goal is to provide a stable
    orchestration surface for future tensor operations or LLM integrations.
    """

    def __init__(self, modules: Iterable[PhilosopherModule]):
        self.modules: List[PhilosopherModule] = list(modules)

    def run_ensemble(self, prompt: str) -> ReasoningResult:
        """Collect contributions and assemble the ensemble tensors."""

        contributions = [module.contribute(prompt) for module in self.modules]
        total_freedom_pressure = sum(c.freedom_pressure for c in contributions)
        aggregate_semantic_delta = sum(c.semantic_delta for c in contributions) / max(
            len(contributions), 1
        )
        blocked_tensor_notes = [c.blocked_tensor for c in contributions if c.blocked_tensor]

        return ReasoningResult(
            prompt=prompt,
            contributions=contributions,
            total_freedom_pressure=total_freedom_pressure,
            aggregate_semantic_delta=aggregate_semantic_delta,
            blocked_tensor_notes=blocked_tensor_notes,
        )


def _default_generator(prompt: str, module: PhilosopherModule) -> PhilosopherContribution:
    """Baseline contribution template.

    This callable stands in for more advanced tensor or LLM-based reasoning. It
    lightly processes the prompt to keep the API usable while remaining fully
    deterministic for testing and downstream module consumption.
    """

    prompt_length = len(prompt.split()) or 1
    semantic_delta = min(len(set(prompt.lower().split())) / prompt_length, 1.0)
    freedom_pressure = max(module.weighting, 0.1) * (1 + semantic_delta / 2)
    blocked_tensor = f"{module.name} withholds edge cases around {module.stance}" if prompt_length > 8 else ""
    narrative = (
        f"Interprets the prompt through {module.stance}, emphasizing agency while"
        f" tracking meaning drift."
    )

    return PhilosopherContribution(
        philosopher=module.name,
        narrative=narrative,
        freedom_pressure=freedom_pressure,
        semantic_delta=semantic_delta * module.weighting,
        blocked_tensor=blocked_tensor,
    )


def default_ensemble() -> EnsembleCoordinator:
    """Create a coordinator with representative philosopher modules.

    The defaults mirror the "philosophers as interacting tensors" vision by
    providing varied stances and weights, ready for replacement with richer
    mathematical or LLM-driven behaviors.
    """

    modules = [
        PhilosopherModule("Heidegger", "Dasein and Being-in-the-world", 1.1, _default_generator),
        PhilosopherModule("Derrida", "trace and différance", 0.9, _default_generator),
        PhilosopherModule("Confucius", "harmonious ethics", 1.0, _default_generator),
        PhilosopherModule("Nietzsche", "will to power", 1.2, _default_generator),
    ]
    return EnsembleCoordinator(modules)


@click.command()
@click.option("--prompt", "prompt", prompt=True, help="User prompt to feed Po_self")
def cli(prompt: str | None = None) -> None:
    """Po_self CLI entry point."""

    prompt = prompt or "How should we navigate uncertainty?"
    ensemble = default_ensemble()
    result = ensemble.run_ensemble(prompt)
    console.print("[bold magenta]🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    console.print(result.to_text())


if __name__ == "__main__":
    cli()
