"""
Po_core CLI - Main Command Line Interface

Entry point for the po-core command.
"""

import json
from pathlib import Path
from typing import Iterable

import click
from rich.console import Console
from rich.table import Table

from po_core import __author__, __email__, __version__
from po_core.po_self import PoSelf
from po_core.po_trace import PoTrace

console = Console()
SAMPLE_PROMPT = "What does it mean to live authentically?"


@click.group()
@click.version_option(version="0.1.0-alpha", prog_name="po-core")
def main() -> None:
    """
    Po_core: Philosophy-Driven AI System 🐷🎈

    A system that integrates philosophers as dynamic tensors
    for responsible meaning generation.
    """
    pass


def _format_prompt_output(data: dict, *, keys: Iterable[str]) -> str:
    """Render a compact text view for prompt results."""

    lines = []
    for key in keys:
        value = data.get(key, "")
        lines.append(f"{key.capitalize()}: {value}")
    return "\n".join(lines)


def _render_sample_generation(prompt: str) -> str:
    response = PoSelf().generate(prompt)
    attributions = ", ".join(response.philosophers)
    metrics = ", ".join(f"{k}={v}" for k, v in response.metrics.items())
    leader = response.consensus_leader or "Unknown"
    return (
        f"Prompt: {prompt}\n"
        f"Consensus Lead: {leader}\n"
        f"Philosophers: {attributions}\n"
        f"Metrics: {metrics}\n"
    )


@main.command()
@click.option("--sample/--no-sample", default=False, help="Run a Po_self sample generation")
def hello(sample: bool) -> None:
    """Say hello from Po_core"""
    console.print("[bold blue]🐷🎈 Po_core へようこそ![/bold blue]")
    console.print("Philosophy-Driven AI System - Alpha v0.1.0")
    console.print("\n[italic]A frog in a well may not know the ocean, but it can know the sky.[/italic]")
    if sample:
        console.print("\n[dim]Running Po_self sample...[/dim]")
        console.print(_render_sample_generation(SAMPLE_PROMPT))


@main.command()
@click.option("--sample/--no-sample", default=False, help="Run a Po_self sample generation")
def status(sample: bool) -> None:
    """Show project status"""
    console.print("[bold]📊 Po_core Project Status[/bold]\n")
    console.print("✅ Philosophical Framework: 100%")
    console.print("✅ Documentation: 100%")
    console.print("✅ Architecture Design: 100%")
    console.print("🔄 Implementation: 60% (ensemble + Po_trace)")
    console.print("🔄 Testing: 20% (unit coverage for ensemble/CLI)")
    console.print("⏳ Visualization: 10% (CLI stub, visuals pending)")
    if sample:
        console.print("\n[dim]Running Po_self sample...[/dim]")
        console.print(_render_sample_generation(SAMPLE_PROMPT))


@main.command()
@click.option("--sample/--no-sample", default=False, help="Run a Po_self sample generation")
def version(sample: bool) -> None:
    """Show version information"""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()

    table.add_row("🐷🎈 Po_core", f"v{__version__}")
    table.add_row("Author", __author__)
    table.add_row("Email", __email__)
    table.add_row("Philosophy", "Flying Pig - When Pigs Fly")
    table.add_row("Motto", "井の中の蛙、大海は知らずとも、大空を知る")

    console.print("\n")
    console.print(table)
    console.print("\n[dim]A frog in a well may not know the ocean, but it can know the sky.[/dim]")
    if sample:
        console.print("\n[dim]Running Po_self sample...[/dim]")
        console.print(_render_sample_generation(SAMPLE_PROMPT))


@main.command()
@click.argument("prompt")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="json",
    help="Choose between text or JSON output.",
)
def prompt(prompt: str, output_format: str) -> None:
    """Run the deterministic ensemble against a prompt."""

    response = PoSelf().generate(prompt)
    if output_format.lower() == "json":
        # 余計なprint等は一切禁止
        click.echo(json.dumps(response.to_dict(), ensure_ascii=False))
    else:
        # 非JSON出力の場合のみconsole.printを使用
        console.print(
            _format_prompt_output(
                response.to_dict(),
                keys=["prompt", "text", "philosophers"],
            )
        )


@main.command()
@click.argument("prompt")
def log(prompt: str) -> None:
    """Display the audit log for a deterministic ensemble run."""

    run_data = PoSelf().generate(prompt)
    # 余計なprint等は一切禁止
    click.echo(json.dumps(run_data.log, ensure_ascii=False))


@main.command()
@click.option(
    "--limit",
    type=int,
    default=None,
    help="Limit the number of sessions to display",
)
@click.option(
    "--trace-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Custom trace directory (defaults to ~/.po_trace)",
)
def list(limit: int, trace_dir: Path) -> None:
    """
    📋 List all Po_trace sessions.

    Shows session summaries sorted by most recent first.
    Use --limit to restrict the number of sessions shown.

    Examples:
        po-core list
        po-core list --limit 10
        po-core list --trace-dir /custom/trace/path
    """
    tracer = PoTrace(trace_dir=trace_dir) if trace_dir else PoTrace()
    sessions = tracer.list_sessions(limit=limit)

    if not sessions:
        console.print("[yellow]No sessions found.[/yellow]")
        return

    table = Table(title="Po_trace Sessions", show_header=True)
    table.add_column("Session ID", style="cyan")
    table.add_column("Created At", style="green")
    table.add_column("Prompt", style="white")
    table.add_column("Events", justify="right", style="magenta")

    for session in sessions:
        session_id = session["session_id"][:8] + "..."  # Truncate for display
        created_at = session["created_at"][:19]  # Remove timezone
        prompt = session["prompt"][:50] + "..." if len(session["prompt"]) > 50 else session["prompt"]
        event_count = str(len(session.get("events", [])))

        table.add_row(session_id, created_at, prompt, event_count)

    console.print(table)
    console.print(f"\n[dim]Total sessions: {len(sessions)}[/dim]")


@main.command()
@click.argument("session_id")
@click.option(
    "--trace-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Custom trace directory (defaults to ~/.po_trace)",
)
def view(session_id: str, trace_dir: Path) -> None:
    """
    🔍 View details of a specific Po_trace session.

    Displays the full session information including all events,
    philosopher responses, and metrics.

    Examples:
        po-core view abc123def456
        po-core view abc123def456 --trace-dir /custom/trace/path
    """
    tracer = PoTrace(trace_dir=trace_dir) if trace_dir else PoTrace()
    session = tracer.get_session(session_id)

    if not session:
        console.print(f"[red]Session not found: {session_id}[/red]")
        return

    # Display session info
    console.print(f"[bold cyan]Session: {session.session_id}[/bold cyan]")
    console.print(f"[dim]Created: {session.created_at}[/dim]\n")
    console.print(f"[bold]Prompt:[/bold] {session.prompt}\n")
    console.print(f"[bold]Philosophers:[/bold] {', '.join(session.philosophers)}\n")

    # Display response text if stored in metadata
    if "response" in session.metadata:
        console.print(f"[bold]Response Text:[/bold]\n{session.metadata['response']}\n")

    # Display metrics
    if session.metrics:
        console.print(f"[bold green]Metrics:[/bold green]")
        for key, value in session.metrics.items():
            console.print(f"  {key}: {value}")

    # Display events
    if session.events:
        console.print(f"\n[bold yellow]Events ({len(session.events)}):[/bold yellow]")
        for i, event in enumerate(session.events, 1):
            console.print(f"  {i}. [{event.event_type.value}] {event.source} at {event.timestamp[:19]}")
            if event.data:
                console.print(f"     Data: {event.data}")

    # Display metadata
    if session.metadata:
        console.print(f"\n[bold magenta]Metadata:[/bold magenta]")
        console.print(json.dumps(session.metadata, indent=2))


@main.command()
@click.argument("session_id")
@click.option(
    "--format",
    "export_format",
    type=click.Choice(["json", "text"], case_sensitive=False),
    default="json",
    help="Export format (json or text)",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    default=None,
    help="Output file path (defaults to stdout)",
)
@click.option(
    "--trace-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Custom trace directory (defaults to ~/.po_trace)",
)
def export(session_id: str, export_format: str, output: Path, trace_dir: Path) -> None:
    """
    📤 Export a Po_trace session.

    Exports session data in JSON or human-readable text format.
    By default, outputs to stdout. Use --output to save to a file.

    Examples:
        po-core export abc123def456
        po-core export abc123def456 --format text
        po-core export abc123def456 --format json --output session.json
    """
    tracer = PoTrace(trace_dir=trace_dir) if trace_dir else PoTrace()

    try:
        exported_data = tracer.export_session(session_id, format=export_format)

        if output:
            output.write_text(exported_data, encoding="utf-8")
            console.print(f"[green]✓ Exported to {output}[/green]")
        else:
            click.echo(exported_data)

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


@main.command(name="show-rejections")
@click.option(
    "--session-id",
    "-s",
    type=str,
    default=None,
    help="Session ID to filter rejections (shows all if not specified)",
)
@click.option(
    "--trace-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Custom trace directory (defaults to ~/.po_trace)",
)
def show_rejections(session_id: str, trace_dir: Path) -> None:
    """
    🚫 View rejection logs for a session.

    Displays all rejected or blocked philosophical reasoning attempts
    for the specified session, or all rejections if no session is specified.

    Examples:
        po-core rejections abc123def456
        po-core rejections  # Show all rejections
    """
    tracer = PoTrace(trace_dir=trace_dir) if trace_dir else PoTrace()

    if session_id:
        # Show rejections for specific session
        rejection_logs = tracer.get_session_rejections(session_id)
        title = f"Rejections for Session {session_id[:8]}..."
    else:
        # Show all rejections (load from disk first)
        tracer._load_all_rejections()
        # Store rejections dict to avoid potential name conflicts
        rejections_dict = tracer.rejections
        rejection_logs = [r for r in rejections_dict.values()]
        title = "All Rejection Logs"

    if not rejection_logs:
        console.print("[yellow]No rejections found.[/yellow]")
        return

    table = Table(title=title, show_header=True)
    table.add_column("Rejection ID", style="red")
    table.add_column("Philosopher", style="cyan")
    table.add_column("Type", style="yellow")
    table.add_column("Timestamp", style="green")
    table.add_column("Reason", style="white")

    for rejection in rejection_logs:
        rejection_id = rejection.rejection_id[:8] + "..."
        philosopher = rejection.philosopher
        rejection_type = rejection.rejection_type
        timestamp = rejection.timestamp[:19]
        reason = rejection.reason[:40] + "..." if len(rejection.reason) > 40 else rejection.reason

        table.add_row(rejection_id, philosopher, rejection_type, timestamp, reason)

    console.print(table)
    console.print(f"\n[dim]Total rejections: {len(rejection_logs)}[/dim]")

    # Show detailed info for first rejection
    if rejection_logs and len(rejection_logs) > 0:
        console.print("\n[bold]Most Recent Rejection Details:[/bold]")
        first = rejection_logs[0]
        console.print(f"  Philosopher: {first.philosopher}")
        console.print(f"  Type: {first.rejection_type}")
        console.print(f"  Reason: {first.reason}")
        if first.blocked_tensor_value is not None:
            console.print(f"  Blocked Tensor: {first.blocked_tensor_value}")
        if first.freedom_pressure_value is not None:
            console.print(f"  Freedom Pressure: {first.freedom_pressure_value}")


@main.command()
@click.option(
    "--theme",
    type=str,
    help="Philosophical theme (ethics, existence, knowledge, etc.)",
)
@click.option(
    "--mood",
    type=click.Choice(["calm", "balanced", "chaotic", "critical"], case_sensitive=False),
    default="balanced",
    help="Party atmosphere/mood",
)
@click.option(
    "--quick",
    is_flag=True,
    help="Quick demo mode (non-interactive)",
)
def party(theme: str, mood: str, quick: bool) -> None:
    """
    🎉 Start an interactive philosopher party!

    Automatically assembles optimal philosopher combinations based on
    research findings. Select a theme and mood, watch philosophy come alive!

    Examples:
        po-core party --theme ethics --mood balanced
        po-core party --quick
        po-core party  (interactive mode)
    """
    import subprocess
    import sys
    from pathlib import Path

    # Find the po_party_demo.py script
    demo_script = Path(__file__).parent.parent.parent / "examples" / "po_party_demo.py"

    if not demo_script.exists():
        console.print("[red]Error: po_party_demo.py not found[/red]")
        console.print(f"[dim]Expected location: {demo_script}[/dim]")
        return

    # Build command
    cmd = [sys.executable, str(demo_script)]

    if quick:
        cmd.append("--quick")
    elif theme:
        # For now, just run interactive mode
        # Future: pass theme and mood as args
        console.print(f"[yellow]Note: Starting interactive mode (theme/mood options coming soon)[/yellow]")

    # Run the demo
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error running party: {e}[/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Party interrupted. Goodbye! 👋[/yellow]")


if __name__ == "__main__":
    main()
