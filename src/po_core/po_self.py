"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers
as interacting tensors.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Sequence, Type

from rich.console import Console

from po_core import philosophers

console = Console()

PHILOSOPHER_REGISTRY: Mapping[str, Type[philosophers.Philosopher]] = {
    "arendt": philosophers.Arendt,
    "aristotle": philosophers.Aristotle,
    "badiou": philosophers.Badiou,
    "confucius": philosophers.Confucius,
    "deleuze": philosophers.Deleuze,
    "derrida": philosophers.Derrida,
    "dewey": philosophers.Dewey,
    "heidegger": philosophers.Heidegger,
    "jung": philosophers.Jung,
    "kierkegaard": philosophers.Kierkegaard,
    "lacan": philosophers.Lacan,
    "levinas": philosophers.Levinas,
    "merleau_ponty": philosophers.MerleauPonty,
    "nietzsche": philosophers.Nietzsche,
    "peirce": philosophers.Peirce,
    "sartre": philosophers.Sartre,
    "wabi_sabi": philosophers.WabiSabi,
    "watsuji": philosophers.Watsuji,
    "wittgenstein": philosophers.Wittgenstein,
    "zhuangzi": philosophers.Zhuangzi,
}


def available_philosophers() -> List[str]:
    """Return a sorted list of available philosopher keys."""

    return sorted(PHILOSOPHER_REGISTRY.keys())


def _normalize_selection(selection: Iterable[str]) -> List[str]:
    """Normalize user-provided philosopher names to registry keys."""

    normalized: List[str] = []
    for name in selection:
        key = name.lower().replace("-", "_").replace(" ", "_")
        if key not in PHILOSOPHER_REGISTRY:
            raise KeyError(f"Unknown philosopher '{name}'. Try one of: {', '.join(available_philosophers())}")
        normalized.append(key)
    return normalized


def run_po_self(prompt: str, selection: Sequence[str]) -> Dict[str, Dict[str, Any]]:
    """Run the Po_self reasoning ensemble for the given prompt."""

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    normalized_selection = _normalize_selection(selection) if selection else available_philosophers()[:3]
    results: Dict[str, Dict[str, Any]] = {}

    for key in normalized_selection:
        philosopher_cls = PHILOSOPHER_REGISTRY[key]
        thinker = philosopher_cls()
        analysis = thinker.reason(prompt)

        display_name = thinker.name
        results[display_name] = {
            "reasoning": analysis.get("reasoning", ""),
            "perspective": analysis.get("perspective", ""),
            "metadata": analysis.get("metadata", {}),
        }

    return results


def render_po_self_summary(prompt: str, results: Mapping[str, Mapping[str, Any]]) -> None:
    """Render a Rich table summarizing Po_self analyses."""

    console.print("[bold magenta]\n🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    console.print(f"[dim]Prompt:[/dim] {prompt}\n")

    from rich.table import Table

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Philosopher", style="bold")
    table.add_column("Perspective")
    table.add_column("Reasoning")

    for name, analysis in results.items():
        table.add_row(name, analysis.get("perspective", ""), analysis.get("reasoning", ""))

    console.print(table)


def cli() -> None:
    """Po_self CLI entry point for manual invocation."""

    console.print("[bold magenta]🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    console.print("This module is designed to be orchestrated through the main Po_core CLI.")


if __name__ == "__main__":
    cli()
