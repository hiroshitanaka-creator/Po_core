"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers
as interacting tensors.
"""

import click
from rich.console import Console

from po_core.po_trace import record_trace_event

console = Console()


def record_self_trace(
    prompt: str,
    response: str,
    philosophers: list[str],
    refusal_reason: str | None = None,
    metadata: dict | None = None,
    backend: str = "file",
    location: str | None = None,
) -> None:
    """Hook for generation pipelines to persist traces."""

    record_trace_event(
        input_text=prompt,
        response_text=response,
        philosophers=philosophers,
        refusal_reason=refusal_reason,
        metadata=metadata,
        backend=backend,
        location=location,
    )


def cli() -> None:
    """Po_self CLI entry point"""
    console.print("[bold magenta]🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    console.print(
        "Use record_self_trace(prompt, response, philosophers, ...) to hook into the tracing pipeline."
    )


if __name__ == "__main__":
    cli()
