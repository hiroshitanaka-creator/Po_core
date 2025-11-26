"""
Po_viewer: Visualization Module

Visualizes the reasoning process, tension maps,
and philosophical interactions.
"""
from __future__ import annotations

from typing import Dict, List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.progress import Progress, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.layout import Layout
from rich import box
import json

from po_core.po_trace import PoTrace, Session

console = Console()


class PoViewer:
    """Po_viewer visualization system."""

    def __init__(self, po_trace: Optional[PoTrace] = None):
        """Initialize Po_viewer with optional PoTrace instance."""
        self.po_trace = po_trace or PoTrace()

    def render_sessions_table(self, limit: int = 10) -> Table:
        """Render sessions list as a table."""
        sessions = self.po_trace.list_sessions(limit=limit)

        table = Table(
            title=f"[bold magenta]🎨 Po_viewer - Recent Sessions[/bold magenta]",
            show_header=True,
            header_style="bold cyan",
            border_style="blue",
            box=box.ROUNDED,
        )

        table.add_column("Session ID", style="cyan", no_wrap=True, width=12)
        table.add_column("Created", style="green", width=20)
        table.add_column("Philosophers", style="yellow", justify="right", width=5)
        table.add_column("Prompt", style="white")

        for session in sessions:
            table.add_row(
                session["session_id"][:8] + "...",
                session["created_at"][:19],
                str(session["philosophers_count"]),
                (session["prompt"][:50] + "...")
                if len(session["prompt"]) > 50
                else session["prompt"],
            )

        return table

    def render_session_detail(self, session_id: str) -> Panel:
        """Render detailed session information."""
        session = self.po_trace.get_session(session_id)
        if session is None:
            return Panel(
                f"[red]Session {session_id} not found[/red]",
                title="Error",
                border_style="red",
            )

        # Build content
        lines = []
        lines.append(f"[bold cyan]Session ID:[/bold cyan] {session.session_id}")
        lines.append(f"[bold cyan]Created:[/bold cyan] {session.created_at}")
        lines.append(f"[bold cyan]Prompt:[/bold cyan] {session.prompt}")
        lines.append(
            f"[bold cyan]Philosophers:[/bold cyan] {', '.join(session.philosophers)}"
        )

        if session.metrics:
            lines.append("\n[bold yellow]Metrics:[/bold yellow]")
            for key, value in session.metrics.items():
                lines.append(f"  • {key}: {value:.3f}")

        lines.append(f"\n[bold green]Events:[/bold green] {len(session.events)} recorded")

        content = "\n".join(lines)

        return Panel(
            content,
            title="[bold magenta]Session Details[/bold magenta]",
            border_style="magenta",
            box=box.DOUBLE,
        )

    def render_metrics_bars(self, session_id: str) -> Panel:
        """Render metrics as progress bars."""
        session = self.po_trace.get_session(session_id)
        if session is None:
            return Panel(
                f"[red]Session {session_id} not found[/red]",
                title="Error",
                border_style="red",
            )

        lines = []
        lines.append("[bold cyan]Session Metrics Visualization[/bold cyan]\n")

        if not session.metrics:
            lines.append("[yellow]No metrics available[/yellow]")
        else:
            # Create visual bars for each metric
            for key, value in session.metrics.items():
                # Normalize to 0-100 scale
                normalized = int(value * 100)
                bar_length = 40
                filled = int((normalized / 100) * bar_length)
                bar = "█" * filled + "░" * (bar_length - filled)

                # Color based on value
                if value >= 0.7:
                    color = "green"
                elif value >= 0.4:
                    color = "yellow"
                else:
                    color = "red"

                lines.append(f"[bold]{key}:[/bold]")
                lines.append(f"[{color}]{bar}[/{color}] {value:.3f}")
                lines.append("")

        content = "\n".join(lines)

        return Panel(
            content,
            title="[bold yellow]📊 Metrics Visualization[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED,
        )

    def render_event_flow(self, session_id: str) -> Tree:
        """Render event flow as a tree."""
        session = self.po_trace.get_session(session_id)
        if session is None:
            tree = Tree("[red]Session not found[/red]")
            return tree

        tree = Tree(
            f"[bold magenta]🔄 Event Flow - {session.prompt[:40]}...[/bold magenta]"
        )

        for i, event in enumerate(session.events):
            # Format timestamp
            time = event.timestamp.split("T")[1][:8] if "T" in event.timestamp else event.timestamp[:8]

            # Event node
            event_label = f"[cyan]{time}[/cyan] [{event.event_type.value}] [yellow]{event.source}[/yellow]"
            event_node = tree.add(event_label)

            # Add event data
            if "message" in event.data:
                event_node.add(f"💬 {event.data['message']}")

            if "philosopher" in event.data:
                event_node.add(f"🧠 Philosopher: {event.data['philosopher']}")

            # Add metrics if available
            metrics = []
            for key in ["freedom_pressure", "semantic_delta", "blocked_tensor"]:
                if key in event.data:
                    metrics.append(f"{key}: {event.data[key]:.3f}")

            if metrics:
                event_node.add(f"📊 {', '.join(metrics)}")

        return tree

    def render_philosopher_interaction(self, session_id: str) -> Panel:
        """Render philosopher interaction analysis."""
        session = self.po_trace.get_session(session_id)
        if session is None:
            return Panel(
                f"[red]Session {session_id} not found[/red]",
                title="Error",
                border_style="red",
            )

        lines = []
        lines.append("[bold cyan]Philosopher Interaction Analysis[/bold cyan]\n")

        # Extract philosopher events
        philosopher_events = [
            e for e in session.events if "philosopher" in e.data
        ]

        if not philosopher_events:
            lines.append("[yellow]No philosopher interactions recorded[/yellow]")
        else:
            # Create interaction summary
            philosophers = {}
            for event in philosopher_events:
                name = event.data["philosopher"]
                if name not in philosophers:
                    philosophers[name] = {
                        "freedom_pressure": event.data.get("freedom_pressure", 0.0),
                        "semantic_delta": event.data.get("semantic_delta", 0.0),
                        "blocked_tensor": event.data.get("blocked_tensor", 0.0),
                        "perspective": event.data.get("perspective", ""),
                    }

            # Rank by freedom_pressure
            ranked = sorted(
                philosophers.items(),
                key=lambda x: x[1]["freedom_pressure"],
                reverse=True,
            )

            lines.append(f"[bold]Total Philosophers:[/bold] {len(philosophers)}")
            lines.append("")

            for i, (name, data) in enumerate(ranked):
                rank_emoji = ["🥇", "🥈", "🥉"][i] if i < 3 else "  "
                lines.append(f"{rank_emoji} [bold yellow]{name}[/bold yellow]")
                lines.append(f"   Freedom Pressure: {data['freedom_pressure']:.3f}")
                lines.append(f"   Semantic Delta: {data['semantic_delta']:.3f}")
                lines.append(f"   Blocked Tensor: {data['blocked_tensor']:.3f}")
                if data["perspective"]:
                    lines.append(f"   Perspective: {data['perspective']}")
                lines.append("")

        content = "\n".join(lines)

        return Panel(
            content,
            title="[bold green]👥 Philosopher Interactions[/bold green]",
            border_style="green",
            box=box.ROUNDED,
        )

    def render_session_json(self, session_id: str) -> Syntax:
        """Render session data as formatted JSON."""
        session = self.po_trace.get_session(session_id)
        if session is None:
            return Syntax("", "json")

        json_str = json.dumps(session.to_dict(), indent=2, ensure_ascii=False)
        return Syntax(json_str, "json", theme="monokai", line_numbers=True)

    def compare_sessions(self, session_id1: str, session_id2: str) -> Panel:
        """Compare two sessions side by side."""
        session1 = self.po_trace.get_session(session_id1)
        session2 = self.po_trace.get_session(session_id2)

        if session1 is None or session2 is None:
            return Panel(
                "[red]One or both sessions not found[/red]",
                title="Error",
                border_style="red",
            )

        lines = []
        lines.append("[bold magenta]Session Comparison[/bold magenta]\n")

        # Compare basic info
        lines.append(f"[bold]Session 1:[/bold] {session_id1[:8]}...")
        lines.append(f"  Prompt: {session1.prompt[:50]}...")
        lines.append(f"  Philosophers: {len(session1.philosophers)}")
        lines.append(f"  Events: {len(session1.events)}")
        lines.append("")

        lines.append(f"[bold]Session 2:[/bold] {session_id2[:8]}...")
        lines.append(f"  Prompt: {session2.prompt[:50]}...")
        lines.append(f"  Philosophers: {len(session2.philosophers)}")
        lines.append(f"  Events: {len(session2.events)}")
        lines.append("")

        # Compare metrics
        if session1.metrics and session2.metrics:
            lines.append("[bold yellow]Metrics Comparison:[/bold yellow]")
            all_keys = set(session1.metrics.keys()) | set(session2.metrics.keys())
            for key in sorted(all_keys):
                val1 = session1.metrics.get(key, 0.0)
                val2 = session2.metrics.get(key, 0.0)
                diff = val2 - val1

                diff_str = f"{diff:+.3f}"
                if diff > 0:
                    diff_color = "green"
                    arrow = "↑"
                elif diff < 0:
                    diff_color = "red"
                    arrow = "↓"
                else:
                    diff_color = "white"
                    arrow = "→"

                lines.append(
                    f"  {key}: {val1:.3f} → {val2:.3f} "
                    f"[{diff_color}]{arrow} {diff_str}[/{diff_color}]"
                )

        content = "\n".join(lines)

        return Panel(
            content,
            title="[bold cyan]⚖️  Session Comparison[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE,
        )


# CLI Commands
@click.group()
def cli() -> None:
    """Po_viewer - Reasoning Visualization System"""
    pass


@cli.command()
@click.option("--limit", type=int, default=10, help="Limit number of sessions to show")
def sessions(limit: int) -> None:
    """List recent sessions with visual table."""
    viewer = PoViewer()
    table = viewer.render_sessions_table(limit=limit)
    console.print(table)


@cli.command()
@click.argument("session_id")
def show(session_id: str) -> None:
    """Show detailed session visualization."""
    viewer = PoViewer()

    # Render detail panel
    detail = viewer.render_session_detail(session_id)
    console.print(detail)

    console.print()

    # Render metrics
    metrics = viewer.render_metrics_bars(session_id)
    console.print(metrics)


@cli.command()
@click.argument("session_id")
def metrics(session_id: str) -> None:
    """Visualize session metrics as bars."""
    viewer = PoViewer()
    panel = viewer.render_metrics_bars(session_id)
    console.print(panel)


@cli.command()
@click.argument("session_id")
def flow(session_id: str) -> None:
    """Visualize event flow as a tree."""
    viewer = PoViewer()
    tree = viewer.render_event_flow(session_id)
    console.print(tree)


@cli.command()
@click.argument("session_id")
def interactions(session_id: str) -> None:
    """Visualize philosopher interactions."""
    viewer = PoViewer()
    panel = viewer.render_philosopher_interaction(session_id)
    console.print(panel)


@cli.command()
@click.argument("session_id1")
@click.argument("session_id2")
def compare(session_id1: str, session_id2: str) -> None:
    """Compare two sessions."""
    viewer = PoViewer()
    panel = viewer.compare_sessions(session_id1, session_id2)
    console.print(panel)


@cli.command(name="json")
@click.argument("session_id")
def show_json(session_id: str) -> None:
    """Show session data as formatted JSON."""
    viewer = PoViewer()
    syntax = viewer.render_session_json(session_id)
    console.print(syntax)


@cli.command()
@click.argument("session_id")
def full(session_id: str) -> None:
    """Show full session visualization (all views)."""
    viewer = PoViewer()

    # Detail
    console.print(viewer.render_session_detail(session_id))
    console.print()

    # Metrics
    console.print(viewer.render_metrics_bars(session_id))
    console.print()

    # Interactions
    console.print(viewer.render_philosopher_interaction(session_id))
    console.print()

    # Event flow
    console.print(viewer.render_event_flow(session_id))


if __name__ == "__main__":
    cli()
