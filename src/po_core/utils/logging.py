"""Logging utilities for Po_core CLI tools."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from rich.console import Console

console = Console()


def iso_timestamp() -> str:
    """Return an ISO-8601 timestamp with UTC timezone."""
    return datetime.now(timezone.utc).isoformat()


def append_lines(path: Path, lines: Iterable[str]) -> None:
    """Append a collection of lines to a file, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        for line in lines:
            file.write(f"{line}\n")


def echo_info(message: str) -> None:
    """Display an informational message."""
    console.print(f"[cyan]{message}[/cyan]")


def echo_success(message: str) -> None:
    """Display a success message."""
    console.print(f"[bold green]{message}[/bold green]")


def echo_warning(message: str) -> None:
    """Display a warning message."""
    console.print(f"[yellow]{message}[/yellow]")


def echo_error(message: str) -> None:
    """Display an error message."""
    console.print(f"[bold red]{message}[/bold red]")
