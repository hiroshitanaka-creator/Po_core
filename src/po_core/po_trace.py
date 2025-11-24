"""
Po_trace: Reasoning Audit Log Module

Tracks and logs the complete reasoning process,
including what was said and what was not said.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import click

from po_core.utils.logging import append_lines, echo_error, echo_info, echo_success, iso_timestamp


@click.group()
def cli() -> None:
    """Po_trace CLI entry point."""
    echo_info("🔍 Po_trace - Reasoning Audit Log")


@cli.command()
@click.option(
    "input_path",
    "--input",
    "-i",
    required=True,
    type=click.Path(path_type=Path),
    help="Path to input events file (JSON array or CSV).",
)
@click.option(
    "output_path",
    "--output",
    "-o",
    default=Path("logs/trace.log"),
    type=click.Path(path_type=Path),
    show_default=True,
    help="Destination log file.",
)
def log(input_path: Path, output_path: Path) -> None:
    """Append audit log entries from an input file."""
    if not input_path.exists():
        echo_error(f"Input file not found: {input_path}")
        sys.exit(1)

    events = _load_events(input_path)
    normalized = [_normalize_event(event) for event in events]
    serialized = [json.dumps(entry, ensure_ascii=False) for entry in normalized]

    append_lines(output_path, serialized)
    echo_success(f"Logged {len(serialized)} event(s) to {output_path}")


def _load_events(path: Path) -> List[Dict[str, Any]]:
    if path.suffix.lower() == ".json":
        content = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(content, list):
            raise click.ClickException("JSON input must be an array of event objects.")
        return [event for event in content if isinstance(event, dict)]

    if path.suffix.lower() == ".csv":
        import csv

        with path.open(encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    raise click.ClickException("Unsupported input format. Use JSON or CSV.")


def _normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    if "event" not in event or "timestamp" not in event:
        raise click.ClickException("Each record must include 'event' and 'timestamp'.")

    name = str(event["event"])
    timestamp_raw = str(event["timestamp"])
    timestamp = _parse_timestamp(timestamp_raw)
    metadata = {key: value for key, value in event.items() if key not in {"event", "timestamp"}}

    return {
        "event": name,
        "timestamp": timestamp,
        "metadata": metadata,
        "recorded_at": iso_timestamp(),
    }


def _parse_timestamp(value: str) -> str:
    try:
        cleaned = value.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned).isoformat()
    except ValueError as error:
        raise click.ClickException(f"Invalid timestamp format: {value}") from error


if __name__ == "__main__":
    cli()
