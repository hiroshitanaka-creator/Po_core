"""
Po_trace: Reasoning Audit Log Module

Tracks and logs the complete reasoning process,
including what was said and what was not said.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Optional

from rich.console import Console

console = Console()


def log_trace(prompt: str, analyses: Mapping[str, Mapping[str, Any]], log_path: Optional[Path] = None) -> Path:
    """Persist a reasoning trace to disk as a JSONL entry."""

    target_path = log_path or Path("po_trace.log")
    target_path.parent.mkdir(parents=True, exist_ok=True)

    entry: MutableMapping[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "prompt": prompt,
        "analyses": analyses,
    }

    with target_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False))
        handle.write("\n")

    return target_path


def cli() -> None:
    """Po_trace CLI entry point for manual invocation."""

    console.print("[bold green]🔍 Po_trace - Reasoning Audit Log[/bold green]")
    console.print("This module is designed to be orchestrated through the main Po_core CLI.")


if __name__ == "__main__":
    cli()
