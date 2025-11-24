"""Self-reflective Po_core package utilities."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import click
from rich.console import Console

from po_core.po_self.manager import PoSelfManager
from po_core.po_self.schemas import AggregationResult, AggregationTensors, PhilosopherContribution

if TYPE_CHECKING:  # pragma: no cover - used for type checking only
    from po_core.core.response import PoCoreResponse

console = Console()


def generate(prompt: str, seed: int | None = None, manager: Optional[PoSelfManager] = None) -> "PoCoreResponse":
    """Generate a Po_core response using the Po_self ensemble."""

    from po_core.core.response import PoCoreResponse

    active_manager = manager or PoSelfManager()
    aggregation = active_manager.aggregate(prompt=prompt, seed=seed)
    generated_text = f"Synthetic reflection for '{prompt}' via {active_manager.describe()}"
    trace_meta = {"prompt": prompt, "seed": seed}
    return PoCoreResponse(
        text=generated_text,
        tensors=aggregation.tensors,
        contributions=aggregation.contributions,
        trace_meta=trace_meta,
    )


def cli() -> None:
    """Po_self CLI entry point"""

    console.print("[bold magenta]🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    console.print("Implementation coming soon...")


__all__ = [
    "AggregationResult",
    "AggregationTensors",
    "PhilosopherContribution",
    "PoSelfManager",
    "cli",
    "generate",
]
