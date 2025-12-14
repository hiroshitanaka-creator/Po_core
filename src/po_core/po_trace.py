"""
Po_trace: Reasoning Audit Log Module

Tracks and logs the complete reasoning process,
including what was said and what was not said.
"""

from po_core.trace.tracer import ReasoningTracer, TraceEntry, TraceLevel
from po_core.trace.annotator import PhilosophicalAnnotator


# Re-export for convenience
__all__ = [
    "ReasoningTracer",
    "TraceEntry",
    "TraceLevel",
    "PhilosophicalAnnotator",
]


def cli() -> None:
    """Po_trace CLI entry point."""
    from rich.console import Console

    console = Console()
    console.print("[bold green]🔍 Po_trace - Reasoning Audit Log[/bold green]")
    console.print("Full reasoning trace implementation is now active!")
    console.print("\nFeatures:")
    console.print("  ✓ Complete reasoning process logging")
    console.print("  ✓ Philosopher reasoning traces")
    console.print("  ✓ Blocked/rejected content tracking (Derrida's trace)")
    console.print("  ✓ Decision point logging")
    console.print("  ✓ Tensor computation tracking")
    console.print("  ✓ Philosophical concept annotations")
    console.print("  ✓ JSON export for audit trails")


if __name__ == "__main__":
    cli()
