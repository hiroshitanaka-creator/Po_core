"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers
as interacting tensors.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import click

from po_core.philosophy_tensor import PhilosophyResponse, synthesize
from po_core.utils.logging import echo_error, echo_info, echo_success


@click.group()
def cli() -> None:
    """Po_self CLI entry point."""
    echo_info("🧠 Po_self - Philosophical Ensemble")


@cli.command(name="synthesize")
@click.option("prompt", "--prompt", required=True, help="Prompt to synthesize.")
@click.option(
    "mode",
    "--mode",
    type=click.Choice(["demo"], case_sensitive=False),
    default="demo",
    show_default=True,
    help="Synthesis mode.",
)
@click.option("seed", "--seed", default=42, show_default=True, help="Random seed.")
@click.option(
    "output_path",
    "--output",
    type=click.Path(path_type=Path),
    help="Optional path to write JSON output.",
)
def synthesize_prompt(prompt: str, mode: str, seed: int, output_path: Optional[Path]) -> None:
    """Generate a mock philosophy tensor response."""
    if mode.lower() != "demo":
        echo_error(f"Unsupported mode: {mode}")
        raise click.Abort()

    result = synthesize(prompt, seed)
    payload = _as_dict(result)
    output = json.dumps(payload, ensure_ascii=False, indent=2)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        echo_success(f"Response written to {output_path}")
    else:
        click.echo(output)


def _as_dict(response: PhilosophyResponse) -> dict[str, object]:
    return {
        "prompt": response.prompt,
        "response": response.response,
        "confidence": response.confidence,
    }


if __name__ == "__main__":
    cli()
