"""
Po_trace: Reasoning Audit Log Module

Tracks and logs the complete reasoning process, including what was
said and what was held back.
"""

from __future__ import annotations

import click
from rich.console import Console

from po_core.po_trace.present import render_summary
from po_core.po_trace.runner import run_trace

console = Console()


@click.command()
@click.argument("prompt")
@click.option("--steps", default=3, show_default=True, help="Number of reasoning steps")
def cli(prompt: str, steps: int) -> None:
    """Po_trace CLI entry point."""

    session = run_trace(prompt=prompt, steps=steps)
    render_summary(console, session)


__all__ = [
    "cli",
    "run_trace",
]
