"""Reasoning audit logging utilities for Po_core."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4

import click
from rich.console import Console
from rich.table import Table


def _now() -> datetime:
    return datetime.utcnow().replace(microsecond=0)


@dataclass(slots=True)
class ReasonLog:
    """Structured record of a reasoning step.

    The schema is aligned with ``docs/specs/reason_log.md`` and is designed to be
    stable for CLI serialization in JSON and Markdown formats.
    """

    id: str
    version: str
    created_at: datetime
    actor: str
    prompt: str
    conclusion: str
    rationale: str
    influences: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.5
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.confidence = max(0.0, min(1.0, float(self.confidence)))
        self.tags = sorted(set(self.tags))
        self.influences = list(self.influences)
        self.evidence = list(self.evidence)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)

    @classmethod
    def new(
        cls,
        prompt: str,
        conclusion: str,
        rationale: str,
        *,
        actor: str = "po-trace",
        influences: Optional[Iterable[str]] = None,
        evidence: Optional[Iterable[str]] = None,
        confidence: float = 0.5,
        tags: Optional[Iterable[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        version: str = "1.0",
    ) -> "ReasonLog":
        """Create a new ``ReasonLog`` with generated identifiers and timestamp."""

        return cls(
            id=str(uuid4()),
            version=version,
            created_at=_now(),
            actor=actor,
            prompt=prompt,
            conclusion=conclusion,
            rationale=rationale,
            influences=list(influences or []),
            evidence=list(evidence or []),
            confidence=confidence,
            tags=list(tags or []),
            metadata=metadata or {},
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReasonLog":
        return cls(
            id=data["id"],
            version=data.get("version", "1.0"),
            created_at=data.get("created_at", _now().isoformat()),
            actor=data["actor"],
            prompt=data["prompt"],
            conclusion=data["conclusion"],
            rationale=data["rationale"],
            influences=data.get("influences", []),
            evidence=data.get("evidence", []),
            confidence=data.get("confidence", 0.5),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "actor": self.actor,
            "prompt": self.prompt,
            "conclusion": self.conclusion,
            "rationale": self.rationale,
            "influences": self.influences,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_markdown(self) -> str:
        lines = [
            f"# Reason Log {self.id}",
            f"- Version: {self.version}",
            f"- Created At: {self.created_at.isoformat()}",
            f"- Actor: {self.actor}",
            f"- Confidence: {self.confidence:.2f}",
            f"- Tags: {', '.join(self.tags) if self.tags else 'none'}",
            "\n## Prompt",
            self.prompt,
            "\n## Conclusion",
            self.conclusion,
            "\n## Rationale",
            self.rationale,
        ]
        if self.influences:
            lines.append("\n## Influences")
            lines.extend(f"- {item}" for item in self.influences)
        if self.evidence:
            lines.append("\n## Evidence")
            lines.extend(f"- {item}" for item in self.evidence)
        if self.metadata:
            lines.append("\n## Metadata")
            lines.extend(f"- {k}: {v}" for k, v in sorted(self.metadata.items()))
        return "\n".join(lines)

    @classmethod
    def from_json(cls, content: str) -> "ReasonLog":
        return cls.from_dict(json.loads(content))

    @classmethod
    def load(cls, path: Path) -> "ReasonLog":
        data = path.read_text(encoding="utf-8")
        return cls.from_json(data)

    def save(self, path: Path, fmt: str = "json") -> None:
        if fmt == "markdown":
            path.write_text(self.to_markdown(), encoding="utf-8")
        else:
            path.write_text(self.to_json(), encoding="utf-8")


console = Console()


@click.group()
def cli() -> None:
    """Po_trace CLI entry point."""


@cli.command(name="log")
@click.option("prompt", "--prompt", required=False, help="Input prompt to record")
@click.option("conclusion", "--conclusion", required=False, help="Outcome or decision")
@click.option("rationale", "--rationale", required=False, help="Explanation of the decision")
@click.option("actor", "--actor", default="po-trace", show_default=True, help="Source actor")
@click.option("tags", "--tag", multiple=True, help="Tags to attach to the log")
@click.option("confidence", "--confidence", type=float, default=0.5, show_default=True)
@click.option("influence", "--influence", multiple=True, help="Influence references")
@click.option("evidence", "--evidence", multiple=True, help="Evidence references")
@click.option(
    "fmt",
    "--format",
    type=click.Choice(["json", "markdown"], case_sensitive=False),
    default="json",
    show_default=True,
    help="Serialization format",
)
@click.option(
    "load_path",
    "--load",
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
    help="Load and display an existing log",
)
@click.option(
    "save_path",
    "--save",
    type=click.Path(path_type=Path, dir_okay=False),
    help="Save the generated log to a file",
)
def log_command(
    *,
    prompt: Optional[str],
    conclusion: Optional[str],
    rationale: Optional[str],
    actor: str,
    tags: Iterable[str],
    confidence: float,
    influence: Iterable[str],
    evidence: Iterable[str],
    fmt: str,
    load_path: Optional[Path],
    save_path: Optional[Path],
) -> None:
    """Create or view reasoning logs.

    Without ``--load`` the command generates a new log from the provided prompt,
    conclusion, and rationale. When ``--load`` is used the CLI renders the
    existing log in a human-readable table.
    """

    if load_path:
        log = ReasonLog.load(load_path)
        _display_log(log)
        return

    if not prompt or not conclusion or not rationale:
        raise click.UsageError("prompt, conclusion, and rationale are required when creating a log")

    log = ReasonLog.new(
        prompt=prompt,
        conclusion=conclusion,
        rationale=rationale,
        actor=actor,
        influences=influence,
        evidence=evidence,
        confidence=confidence,
        tags=tags,
    )

    if save_path:
        log.save(save_path, fmt=fmt)
        console.print(f"[green]Saved reason log to {save_path} ({fmt}).[/green]")
    else:
        console.print(log.to_markdown() if fmt == "markdown" else log.to_json())


def _display_log(log: ReasonLog) -> None:
    table = Table(title=f"Reason Log {log.id}")
    table.add_column("Field", style="cyan")
    table.add_column("Value")

    table.add_row("Version", log.version)
    table.add_row("Created At", log.created_at.isoformat())
    table.add_row("Actor", log.actor)
    table.add_row("Prompt", log.prompt)
    table.add_row("Conclusion", log.conclusion)
    table.add_row("Rationale", log.rationale)
    table.add_row("Confidence", f"{log.confidence:.2f}")
    table.add_row("Tags", ", ".join(log.tags) if log.tags else "-")
    table.add_row("Influences", ", ".join(log.influences) if log.influences else "-")
    table.add_row("Evidence", ", ".join(log.evidence) if log.evidence else "-")
    table.add_row("Metadata", json.dumps(log.metadata, ensure_ascii=False))

    console.print(table)


if __name__ == "__main__":
    cli()
