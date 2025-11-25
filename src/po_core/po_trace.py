"""Po_trace: Reasoning Audit Log Module.

This module provides structured auditing for the reasoning process. It tracks
what was explicitly surfaced ("said") and which candidate thoughts were
suppressed ("not said") along with transparency metadata such as philosopher
weights, freedom pressure, semantic deltas, and blocked tensor rationales.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, MutableMapping, Optional

import click
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass(slots=True)
class TraceStatement:
    """An explicit statement surfaced during reasoning."""

    content: str
    channel: str = "said"
    philosopher_annotations: List[str] = field(default_factory=list)
    semantic_focus: Optional[str] = None


@dataclass(slots=True)
class NotSaidReason:
    """An idea or fragment intentionally withheld from the final answer."""

    content: str
    rationale: str
    blocked_tensor: Optional[str] = None
    policy_reference: Optional[str] = None


@dataclass(slots=True)
class SemanticDelta:
    """Describes how the answer shifted semantically during deliberation."""

    dimension: str
    before: str
    after: str
    delta: Optional[str] = None


@dataclass(slots=True)
class BlockedTensorRationale:
    """Captures why a tensor or pathway was inhibited."""

    tensor: str
    rationale: str
    severity: str = "moderate"


@dataclass(slots=True)
class ReasoningResult:
    """Container for a single reasoning cycle."""

    prompt: str
    said: List[TraceStatement]
    not_said: List[NotSaidReason]
    philosopher_weights: Mapping[str, float]
    freedom_pressure: Mapping[str, float]
    semantic_deltas: List[SemanticDelta] = field(default_factory=list)
    blocked_tensors: List[BlockedTensorRationale] = field(default_factory=list)
    rejection_log: Optional[str] = None
    philosophical_annotations: List[str] = field(default_factory=list)
    metadata: MutableMapping[str, Any] = field(default_factory=dict)


def serialize_reasoning_result(result: ReasoningResult) -> Dict[str, Any]:
    """Convert a :class:`ReasoningResult` into a JSON-friendly schema.

    The schema highlights both articulated and withheld content and carries the
    transparency metadata required by Po_trace consumers.
    """

    timestamp = datetime.now(timezone.utc).isoformat()

    return {
        "schema_version": "1.0",
        "recorded_at": timestamp,
        "prompt": result.prompt,
        "analysis": {
            "philosopher_weights": dict(result.philosopher_weights),
            "freedom_pressure": dict(result.freedom_pressure),
            "semantic_deltas": [
                {
                    "dimension": delta.dimension,
                    "before": delta.before,
                    "after": delta.after,
                    "delta": delta.delta,
                }
                for delta in result.semantic_deltas
            ],
            "blocked_tensors": [
                {
                    "tensor": block.tensor,
                    "rationale": block.rationale,
                    "severity": block.severity,
                }
                for block in result.blocked_tensors
            ],
            "rejection_log": result.rejection_log,
            "philosophical_annotations": result.philosophical_annotations,
        },
        "transparency": {
            "said": [
                {
                    "content": statement.content,
                    "channel": statement.channel,
                    "philosopher_annotations": statement.philosopher_annotations,
                    "semantic_focus": statement.semantic_focus,
                }
                for statement in result.said
            ],
            "not_said": [
                {
                    "content": withheld.content,
                    "rationale": withheld.rationale,
                    "blocked_tensor": withheld.blocked_tensor,
                    "policy_reference": withheld.policy_reference,
                }
                for withheld in result.not_said
            ],
        },
        "metadata": result.metadata,
    }


def format_trace_markdown(log: Mapping[str, Any]) -> str:
    """Render the log dictionary into a human-readable markdown string."""

    lines: List[str] = []
    lines.append(f"# Po_trace Audit Log (v{log.get('schema_version', '1.0')})")
    lines.append("")
    lines.append(f"Recorded at: {log.get('recorded_at', 'unknown')}")
    lines.append(f"Prompt: {log.get('prompt', 'N/A')}")
    lines.append("")

    analysis = log.get("analysis", {})
    lines.append("## Analysis")
    lines.append("### Philosopher Weights")
    for philosopher, weight in analysis.get("philosopher_weights", {}).items():
        lines.append(f"- **{philosopher}**: {weight}")

    lines.append("\n### Freedom Pressure")
    for key, value in analysis.get("freedom_pressure", {}).items():
        lines.append(f"- **{key}**: {value}")

    lines.append("\n### Semantic Deltas")
    for delta in analysis.get("semantic_deltas", []):
        lines.append(
            f"- {delta.get('dimension')}: '{delta.get('before')}' -> "
            f"'{delta.get('after')}' ({delta.get('delta') or 'n/a'})"
        )

    lines.append("\n### Blocked Tensors")
    for block in analysis.get("blocked_tensors", []):
        lines.append(
            f"- {block.get('tensor')}: {block.get('rationale')} "
            f"(severity: {block.get('severity')})"
        )

    rejection_log = analysis.get("rejection_log")
    if rejection_log:
        lines.append("\n### Rejection Log")
        lines.append(f"- {rejection_log}")

    annotations = analysis.get("philosophical_annotations", [])
    if annotations:
        lines.append("\n### Philosophical Annotations")
        for note in annotations:
            lines.append(f"- {note}")

    transparency = log.get("transparency", {})
    lines.append("\n## Transparency")
    lines.append("### Said")
    for statement in transparency.get("said", []):
        focus = statement.get("semantic_focus")
        focus_suffix = f" (focus: {focus})" if focus else ""
        lines.append(
            f"- {statement.get('content')} [channel: {statement.get('channel')}]"
            f"{focus_suffix}"
        )
        for annotation in statement.get("philosopher_annotations", []):
            lines.append(f"  - Philosopher note: {annotation}")

    lines.append("\n### Not Said")
    for withheld in transparency.get("not_said", []):
        reason_suffix = (
            f" (blocked tensor: {withheld.get('blocked_tensor')})"
            if withheld.get("blocked_tensor")
            else ""
        )
        lines.append(
            f"- {withheld.get('content')} — rationale: {withheld.get('rationale')}"
            f"{reason_suffix}"
        )
        if withheld.get("policy_reference"):
            lines.append(f"  - Policy: {withheld['policy_reference']}")

    metadata = log.get("metadata", {})
    if metadata:
        lines.append("\n## Metadata")
        for key, value in metadata.items():
            lines.append(f"- {key}: {value}")

    return "\n".join(lines)


def render_trace_log(log: Mapping[str, Any]) -> None:
    """Pretty print a Po_trace audit log using Rich tables."""

    console.print("[bold green]🔍 Po_trace - Reasoning Audit Log[/bold green]")
    console.print(
        f"Schema version: {log.get('schema_version', '1.0')}  |  "
        f"Recorded at: {log.get('recorded_at', 'unknown')}",
        style="dim",
    )

    summary_table = Table(title="Said vs Not Said", show_header=True, header_style="bold magenta")
    summary_table.add_column("Type")
    summary_table.add_column("Content")
    summary_table.add_column("Details")

    transparency = log.get("transparency", {})
    for statement in transparency.get("said", []):
        details = ", ".join(statement.get("philosopher_annotations", [])) or "—"
        focus = statement.get("semantic_focus")
        if focus:
            details = f"{details} | focus: {focus}" if details != "—" else f"focus: {focus}"
        summary_table.add_row("Said", statement.get("content", ""), details)

    for withheld in transparency.get("not_said", []):
        reason_parts = [withheld.get("rationale", "")] if withheld.get("rationale") else []
        if withheld.get("blocked_tensor"):
            reason_parts.append(f"blocked tensor: {withheld['blocked_tensor']}")
        if withheld.get("policy_reference"):
            reason_parts.append(f"policy: {withheld['policy_reference']}")
        summary_table.add_row("Not Said", withheld.get("content", ""), " | ".join(reason_parts))

    console.print(summary_table)

    analysis_table = Table(title="Analysis", show_header=True, header_style="bold cyan")
    analysis_table.add_column("Aspect")
    analysis_table.add_column("Details")

    analysis = log.get("analysis", {})
    philosopher_weights = analysis.get("philosopher_weights", {})
    if philosopher_weights:
        weights = ", ".join(f"{name}: {weight}" for name, weight in philosopher_weights.items())
        analysis_table.add_row("Philosopher Weights", weights)

    freedom_pressure = analysis.get("freedom_pressure", {})
    if freedom_pressure:
        pressure = ", ".join(
            f"{dimension}: {value}" for dimension, value in freedom_pressure.items()
        )
        analysis_table.add_row("Freedom Pressure", pressure)

    semantic_deltas = analysis.get("semantic_deltas", [])
    if semantic_deltas:
        deltas = [
            f"{delta.get('dimension')}: {delta.get('before')} -> {delta.get('after')}"
            + (f" ({delta.get('delta')})" if delta.get("delta") else "")
            for delta in semantic_deltas
        ]
        analysis_table.add_row("Semantic Deltas", "\n".join(deltas))

    blocked_tensors = analysis.get("blocked_tensors", [])
    if blocked_tensors:
        blocked = [
            f"{block.get('tensor')}: {block.get('rationale')} (severity: {block.get('severity')})"
            for block in blocked_tensors
        ]
        analysis_table.add_row("Blocked Tensors", "\n".join(blocked))

    rejection_log = analysis.get("rejection_log")
    if rejection_log:
        analysis_table.add_row("Rejection Log", rejection_log)

    annotations = analysis.get("philosophical_annotations", [])
    if annotations:
        analysis_table.add_row("Philosophical Annotations", "\n".join(annotations))

    metadata = log.get("metadata", {})
    if metadata:
        meta_entries = "\n".join(f"{k}: {v}" for k, v in metadata.items())
        analysis_table.add_row("Metadata", meta_entries)

    console.print(analysis_table)


def _load_trace_file(input_path: pathlib.Path) -> Dict[str, Any]:
    if not input_path.exists():
        raise FileNotFoundError(f"Trace file not found: {input_path}")
    with input_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@click.command()
@click.option(
    "input_path",
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=pathlib.Path),
    help="Path to a Po_trace JSON log file.",
)
@click.option(
    "--markdown",
    is_flag=True,
    help="Render the trace as markdown instead of Rich tables.",
)
def cli(input_path: pathlib.Path, markdown: bool) -> None:
    """Po_trace CLI entry point.

    Example:
        po-trace --input sample.json
    """

    log = _load_trace_file(input_path)
    if markdown:
        console.print(format_trace_markdown(log))
    else:
        render_trace_log(log)


if __name__ == "__main__":
    cli()
