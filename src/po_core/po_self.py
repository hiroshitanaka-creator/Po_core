"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers as
interacting tensors.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

import click
from rich.console import Console

from po_core.po_trace.logger import TraceLogger
from po_core.po_trace.models import TraceEntry, TensorSnapshot, TraceSession

console = Console()

PHILOSOPHER_NAMES: List[str] = [
    "Sartre",
    "Nietzsche",
    "Confucius",
    "Wittgenstein",
]


def _mock_tensor_summary(prompt: str, weight: float) -> List[float]:
    length_factor = max(1, len(prompt) % 5 + 1)
    return [round(length_factor * weight * i, 3) for i in range(1, 4)]


def _philosopher_weights(step: int) -> Dict[str, float]:
    base = 1.0 / (step + 1)
    return {
        name: round(base * (index + 1) / len(PHILOSOPHER_NAMES), 3)
        for index, name in enumerate(PHILOSOPHER_NAMES)
    }


def execute_prompt(
    *, prompt: str, steps: int = 3, trace_logger: Optional[TraceLogger] = None
) -> TraceSession:
    """Execute a prompt while emitting structured trace events."""

    logger = trace_logger or TraceLogger()
    logger.start_session(prompt)

    spoken_fragments: List[str] = []
    semantic_accumulator = 0.05

    for step in range(steps):
        weights = _philosopher_weights(step)
        freedom_pressure = max(0.0, 1.0 - (step * 0.2))
        semantic_delta = round(semantic_accumulator + 0.05 * step, 3)
        tensor = TensorSnapshot(
            name="meaning_vector",
            shape=[3],
            summary=_mock_tensor_summary(prompt, semantic_delta + 1),
        )
        spoken_text = f"{prompt} -> reflection {step + 1}"
        suppressed_text = f"unspoken nuance {step + 1}"

        entry = TraceEntry(
            step=step + 1,
            spoken_text=spoken_text,
            suppressed_text=suppressed_text,
            philosopher_weights=weights,
            tensors=[tensor],
            freedom_pressure=freedom_pressure,
            semantic_delta=semantic_delta,
            timestamp=datetime.utcnow(),
        )
        logger.record(entry)
        spoken_fragments.append(spoken_text)

    return logger.finish(spoken_text=" ".join(spoken_fragments))


@click.command()
@click.argument("prompt")
@click.option("--steps", default=3, show_default=True, help="Number of reasoning steps")
def cli(prompt: str, steps: int) -> None:
    """Po_self CLI entry point."""

    session = execute_prompt(prompt=prompt, steps=steps)
    console.print("[bold magenta]\n🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    console.print(f"Prompt: [italic]{prompt}[/italic]")
    console.print(f"Captured {len(session.entries)} trace events.\n")


if __name__ == "__main__":
    cli()
