"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers
as interacting tensors.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import click
from rich.console import Console

from po_core.po_trace import PoTrace, TraceLevel

console = Console()


DEFAULT_CHANNELS: List[str] = ["analysis", "counterpoint"]


def run_po_self(
    prompt: str,
    *,
    trace_level: str = TraceLevel.CONCISE.value,
    trace_output: Optional[str] = None,
) -> Dict[str, Any]:
    """Deterministic Po_self reasoning flow that emits and suppresses content."""

    tracer = PoTrace(prompt=prompt)
    tracer.record_event("po_self_started", channels=len(DEFAULT_CHANNELS))
    level_enum = TraceLevel(trace_level)

    emitted = []
    suppressed = []

    for channel in DEFAULT_CHANNELS:
        content = f"[{channel}] Reflecting on '{prompt}' with structured reasoning."
        tracer.record_emission(channel, content, channel=channel)
        tracer.log_reason(channel, f"Baseline {channel} pass over the prompt.", channel=channel)
        tracer.attribute(channel, weight=0.5, note="Equal channel weighting for deterministic flow.")
        emitted.append({"channel": channel, "content": content})

        suppressed_content = (
            f"[{channel}] Speculative extension about '{prompt}' intentionally held back."
        )
        tracer.log_rejection(
            channel,
            content=suppressed_content,
            rationale="Speculative expansion suppressed for safety preview.",
        )
        suppressed.append({"channel": channel, "content": suppressed_content})

    tracer.record_event("po_self_completed", emitted=len(emitted), suppressed=len(suppressed))

    trace_data = tracer.to_dict(level=level_enum)
    tracer.export(trace_output, level=level_enum)

    return {
        "prompt": prompt,
        "emitted": emitted,
        "suppressed": suppressed,
        "trace": trace_data,
    }


@click.command()
@click.argument("prompt")
@click.option(
    "--trace-level",
    type=click.Choice([member.value for member in TraceLevel]),
    default=TraceLevel.CONCISE.value,
    show_default=True,
    help="Detail level for Po_trace output.",
)
@click.option(
    "--trace-output",
    type=click.Path(dir_okay=False, writable=True, path_type=str),
    help="Optional file path to persist the trace JSON.",
)
def cli(prompt: str, trace_level: str, trace_output: Optional[str]) -> None:
    """Po_self CLI entry point"""

    console.print("[bold magenta]\n🧠 Po_self - Philosophical Ensemble\n[/bold magenta]")
    result = run_po_self(prompt, trace_level=trace_level, trace_output=trace_output)
    console.print("[bold]Emitted Channels:[/bold]")
    for item in result["emitted"]:
        console.print(f"- {item['channel']}: {item['content']}")

    console.print("\n[dim]Suppressed content recorded in trace.[/dim]")
    console.print_json(data=result["trace"])


if __name__ == "__main__":
    cli()
