"""
Trace Formatter

Formats reasoning traces in various output formats for display and export.
"""

import json
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree


class TraceFormatter:
    """
    Formatter for reasoning traces.

    Supports multiple output formats:
    - Rich console (colored terminal output)
    - JSON (structured data)
    - Markdown (documentation)
    - Plain text (simple export)
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize formatter.

        Args:
            console: Rich console for output
        """
        self.console = console or Console()

    def format_trace_rich(self, trace_data: Dict[str, Any]) -> None:
        """
        Format trace with rich terminal output.

        Args:
            trace_data: Trace data from ReasoningTracer
        """
        self.console.rule("[bold magenta]🔍 Reasoning Trace[/bold magenta]")

        # Session info
        session_id = trace_data.get("session_id", "unknown")
        start_time = trace_data.get("start_time", "unknown")
        self.console.print(f"\n[bold]Session ID:[/bold] {session_id}")
        self.console.print(f"[bold]Started:[/bold] {start_time}")

        # Metadata
        metadata = trace_data.get("metadata", {})
        if metadata:
            self.console.print(f"\n[bold cyan]Metadata:[/bold cyan]")
            for key, value in metadata.items():
                self.console.print(f"  {key}: {value}")

        # Entries
        entries = trace_data.get("entries", [])
        self.console.print(
            f"\n[bold yellow]Trace Entries:[/bold yellow] {len(entries)} events"
        )

        # Group entries by level
        by_level = {}
        for entry in entries:
            level = entry.get("level", "unknown")
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(entry)

        # Display summary
        self.console.print("\n[bold]Entry Summary:[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Level", style="cyan")
        table.add_column("Count", justify="right")

        for level, level_entries in sorted(by_level.items()):
            table.add_row(level, str(len(level_entries)))

        self.console.print(table)

        # Display entries as tree
        if entries:
            self._display_trace_tree(entries)

    def _display_trace_tree(self, entries: List[Dict[str, Any]]) -> None:
        """
        Display trace entries as a tree.

        Args:
            entries: List of trace entries
        """
        self.console.print("\n[bold]Trace Timeline:[/bold]")

        tree = Tree("🌳 Reasoning Process")

        for i, entry in enumerate(entries):
            timestamp = entry.get("timestamp", "")
            level = entry.get("level", "info")
            event = entry.get("event", "")
            message = entry.get("message", "")
            philosopher = entry.get("philosopher")

            # Format node
            if philosopher:
                node_label = f"[{level}] {event} - {philosopher}: {message[:50]}"
            else:
                node_label = f"[{level}] {event}: {message[:50]}"

            # Add color based on level
            if level == "error":
                node_label = f"[red]{node_label}[/red]"
            elif level == "warning":
                node_label = f"[yellow]{node_label}[/yellow]"
            elif level == "reasoning":
                node_label = f"[cyan]{node_label}[/cyan]"
            elif level == "decision":
                node_label = f"[green]{node_label}[/green]"
            elif level == "blocked":
                node_label = f"[magenta]{node_label}[/magenta]"
            else:
                node_label = f"[dim]{node_label}[/dim]"

            tree.add(node_label)

        self.console.print(tree)

    def format_trace_json(self, trace_data: Dict[str, Any], indent: int = 2) -> str:
        """
        Format trace as JSON.

        Args:
            trace_data: Trace data
            indent: JSON indentation

        Returns:
            JSON string
        """
        return json.dumps(trace_data, indent=indent, default=str)

    def format_trace_markdown(self, trace_data: Dict[str, Any]) -> str:
        """
        Format trace as Markdown.

        Args:
            trace_data: Trace data

        Returns:
            Markdown string
        """
        lines = []

        # Header
        lines.append("# Reasoning Trace")
        lines.append("")

        # Session info
        session_id = trace_data.get("session_id", "unknown")
        start_time = trace_data.get("start_time", "unknown")
        lines.append("## Session Information")
        lines.append("")
        lines.append(f"- **Session ID**: `{session_id}`")
        lines.append(f"- **Start Time**: {start_time}")
        lines.append("")

        # Metadata
        metadata = trace_data.get("metadata", {})
        if metadata:
            lines.append("## Metadata")
            lines.append("")
            for key, value in metadata.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")

        # Entries
        entries = trace_data.get("entries", [])
        lines.append(f"## Trace Entries ({len(entries)} events)")
        lines.append("")

        for i, entry in enumerate(entries, 1):
            level = entry.get("level", "info")
            event = entry.get("event", "")
            message = entry.get("message", "")
            philosopher = entry.get("philosopher")
            timestamp = entry.get("timestamp", "")

            lines.append(f"### Entry {i}: {event}")
            lines.append("")
            lines.append(f"- **Level**: `{level}`")
            lines.append(f"- **Timestamp**: {timestamp}")
            if philosopher:
                lines.append(f"- **Philosopher**: {philosopher}")
            lines.append(f"- **Message**: {message}")
            lines.append("")

        return "\n".join(lines)

    def format_trace_text(self, trace_data: Dict[str, Any]) -> str:
        """
        Format trace as plain text.

        Args:
            trace_data: Trace data

        Returns:
            Plain text string
        """
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("REASONING TRACE")
        lines.append("=" * 80)
        lines.append("")

        # Session info
        session_id = trace_data.get("session_id", "unknown")
        start_time = trace_data.get("start_time", "unknown")
        lines.append(f"Session ID: {session_id}")
        lines.append(f"Start Time: {start_time}")
        lines.append("")

        # Metadata
        metadata = trace_data.get("metadata", {})
        if metadata:
            lines.append("Metadata:")
            for key, value in metadata.items():
                lines.append(f"  {key}: {value}")
            lines.append("")

        # Entries
        entries = trace_data.get("entries", [])
        lines.append(f"Trace Entries: {len(entries)} events")
        lines.append("-" * 80)
        lines.append("")

        for i, entry in enumerate(entries, 1):
            level = entry.get("level", "info").upper()
            event = entry.get("event", "")
            message = entry.get("message", "")
            philosopher = entry.get("philosopher")
            timestamp = entry.get("timestamp", "")

            lines.append(f"[{i}] {timestamp} | {level} | {event}")
            if philosopher:
                lines.append(f"    Philosopher: {philosopher}")
            lines.append(f"    Message: {message}")
            lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)

    def display_trace(self, trace_data: Dict[str, Any], format: str = "rich") -> None:
        """
        Display trace in specified format.

        Args:
            trace_data: Trace data
            format: Output format ('rich', 'json', 'markdown', 'text')
        """
        if format == "rich":
            self.format_trace_rich(trace_data)
        elif format == "json":
            json_output = self.format_trace_json(trace_data)
            syntax = Syntax(json_output, "json", theme="monokai")
            self.console.print(syntax)
        elif format == "markdown":
            md_output = self.format_trace_markdown(trace_data)
            self.console.print(
                Panel(md_output, title="Markdown Output", border_style="green")
            )
        elif format == "text":
            text_output = self.format_trace_text(trace_data)
            self.console.print(text_output)
        else:
            self.console.print(f"[red]Unknown format: {format}[/red]")

    def export_trace(
        self, trace_data: Dict[str, Any], filename: str, format: str = "json"
    ) -> None:
        """
        Export trace to file.

        Args:
            trace_data: Trace data
            filename: Output filename
            format: Output format ('json', 'markdown', 'text')
        """
        try:
            if format == "json":
                content = self.format_trace_json(trace_data)
            elif format == "markdown":
                content = self.format_trace_markdown(trace_data)
            elif format == "text":
                content = self.format_trace_text(trace_data)
            else:
                self.console.print(f"[red]Unknown format: {format}[/red]")
                return

            with open(filename, "w") as f:
                f.write(content)

            self.console.print(f"[green]✓ Trace exported to {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting trace: {e}[/red]")
