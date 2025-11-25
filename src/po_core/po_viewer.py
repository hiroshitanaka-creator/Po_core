"""Visualization scaffolding for Po_core traces.

The viewer module converts deterministic Po_core traces into lightweight payloads
that can be consumed by future UI surfaces. Structures are intentionally
minimal—focused on the *shape* of the data rather than rendering concerns.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List

import click
from rich.console import Console

from po_core.ensemble import run_ensemble

console = Console()


@dataclass
class TensionPoint:
    """Represents the relative agreement between philosophers.

    The ``tension`` field is inverted from confidence to highlight where the
    ensemble diverges. Values near ``1.0`` indicate strong disagreement.
    """

    philosopher: str
    confidence: float
    tension: float
    drivers: List[str]


@dataclass
class EthicalPressure:
    """Captures how each dimension constrains or nudges the output."""

    dimension: str
    pressure: float
    narrative: str


@dataclass
class SemanticShift:
    """Describes semantic changes through the reasoning lifecycle."""

    stage: str
    signal: str
    influence: List[str]
    cumulative_meaning: str


@dataclass
class ViewerPayload:
    """View-ready payload consumed by the Po_core viewer."""

    prompt: str
    generated_at: str
    tension_map: List[TensionPoint]
    ethical_pressure: List[EthicalPressure]
    semantic_evolution: List[SemanticShift]
    source_trace: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert payload to a JSON-serializable dict."""

        return asdict(self)


def _build_tension_map(results: Iterable[Dict[str, Any]]) -> List[TensionPoint]:
    """Translate ensemble results into a normalized tension map."""

    tension_map = []
    for record in results:
        confidence = float(record.get("confidence", 0))
        tension_value = round(1 - confidence, 2)
        drivers = [record.get("summary", ""), *record.get("tags", [])]
        tension_map.append(
            TensionPoint(
                philosopher=record.get("name", "unknown"),
                confidence=confidence,
                tension=tension_value,
                drivers=[driver for driver in drivers if driver],
            )
        )
    return tension_map


def _build_ethical_pressure(results: Iterable[Dict[str, Any]]) -> List[EthicalPressure]:
    """Derive simple ethical pressure markers from deterministic results."""

    pressures = []
    for record in results:
        confidence = float(record.get("confidence", 0))
        normalized_pressure = round(confidence * 0.75, 2)
        pressures.append(
            EthicalPressure(
                dimension=record.get("name", "unknown"),
                pressure=normalized_pressure,
                narrative=f"Confidence-weighted ethical guard from {record.get('name', 'unknown')}",
            )
        )
    return pressures


def _build_semantic_evolution(
    prompt: str, results: Iterable[Dict[str, Any]], events: Iterable[Dict[str, Any]]
) -> List[SemanticShift]:
    """Capture semantic changes across the reasoning process."""

    contributors = [record.get("name", "unknown") for record in results]
    summaries = [record.get("summary", "") for record in results]
    event_labels = [event.get("event", "") for event in events]

    return [
        SemanticShift(
            stage="prompt",
            signal=prompt,
            influence=["user"],
            cumulative_meaning="User intent seeds the reasoning graph.",
        ),
        SemanticShift(
            stage="ensemble",
            signal=" | ".join(filter(None, summaries)),
            influence=contributors,
            cumulative_meaning="Deterministic philosophers contribute weighted reflections.",
        ),
        SemanticShift(
            stage="trace",
            signal=" → ".join(filter(None, event_labels)),
            influence=["system"],
            cumulative_meaning="System-level lifecycle ready for visualization layers.",
        ),
    ]


def build_viewer_payload(trace: Dict[str, Any]) -> ViewerPayload:
    """Map a Po_core trace record into a viewer payload."""

    prompt = trace.get("prompt", "")
    results = trace.get("results", [])
    log = trace.get("log", {})
    events = log.get("events", [])
    generated_at = log.get("created_at", datetime.utcnow().isoformat() + "Z")

    return ViewerPayload(
        prompt=prompt,
        generated_at=generated_at,
        tension_map=_build_tension_map(results),
        ethical_pressure=_build_ethical_pressure(results),
        semantic_evolution=_build_semantic_evolution(prompt, results, events),
        source_trace=log,
    )


@click.group()
def cli() -> None:
    """Po_viewer CLI entry point."""

    # Group entrypoint intentionally quiet to keep JSON output clean for
    # downstream consumers.


@cli.command()
@click.argument("prompt")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json"], case_sensitive=False),
    default="json",
    help="Output format for viewer payloads.",
)
def export(prompt: str, output_format: str) -> None:
    """Export a Po_core trace into a viewer-friendly schema."""

    trace = run_ensemble(prompt)
    payload = build_viewer_payload(trace)
    if output_format.lower() == "json":
        console.print_json(data=payload.to_dict())


if __name__ == "__main__":
    cli()
