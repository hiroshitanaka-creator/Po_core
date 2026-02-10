#!/usr/bin/env python3
"""
Po_viewer Demo - Visualization System Demonstration

Demonstrates all visualization features of Po_viewer:
- Session tables
- Metrics visualization
- Event flow
- Philosopher interactions
- Session comparison
"""

from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

from po_core.po_self import PoSelf
from po_core.po_viewer import PoViewer

console = Console()


def print_section_header(title: str):
    """Print a section header."""
    console.print()
    console.print(
        Panel(
            f"[bold cyan]{title}[/bold cyan]",
            style="cyan",
            expand=False,
        )
    )
    console.print()


def demo_basic_visualization():
    """Demo 1: Basic session visualization."""
    print_section_header("Demo 1: Basic Session Visualization")

    # Create a philosophical session
    console.print("[yellow]Creating a philosophical reasoning session...[/yellow]")
    po = PoSelf(enable_trace=True)
    response = po.generate("What is the meaning of wisdom?")

    session_id = response.log["session_id"]
    console.print(f"[green]✓ Session created: {session_id[:8]}...[/green]")
    console.print()

    # Visualize with Po_viewer
    viewer = PoViewer(po_trace=po.po_trace)

    # Show session detail
    console.print("[bold]📋 Session Details:[/bold]")
    console.print(viewer.render_session_detail(session_id))
    console.print()

    # Show metrics
    console.print("[bold]📊 Metrics Visualization:[/bold]")
    console.print(viewer.render_metrics_bars(session_id))


def demo_event_flow():
    """Demo 2: Event flow visualization."""
    print_section_header("Demo 2: Event Flow Visualization")

    console.print("[yellow]Creating session with multiple philosophers...[/yellow]")
    po = PoSelf(philosophers=["aristotle", "nietzsche", "sartre"], enable_trace=True)
    response = po.generate("What is authentic freedom?")

    session_id = response.log["session_id"]
    viewer = PoViewer(po_trace=po.po_trace)

    # Show event flow
    console.print("[bold]🔄 Event Flow Tree:[/bold]")
    console.print(viewer.render_event_flow(session_id))


def demo_philosopher_interactions():
    """Demo 3: Philosopher interaction analysis."""
    print_section_header("Demo 3: Philosopher Interaction Analysis")

    console.print("[yellow]Creating session with diverse philosophers...[/yellow]")
    po = PoSelf(
        philosophers=["aristotle", "confucius", "nietzsche", "wabi_sabi"],
        enable_trace=True,
    )
    response = po.generate("What is the essence of beauty?")

    session_id = response.log["session_id"]
    viewer = PoViewer(po_trace=po.po_trace)

    # Show philosopher interactions
    console.print("[bold]👥 Philosopher Interactions:[/bold]")
    console.print(viewer.render_philosopher_interaction(session_id))


def demo_session_comparison():
    """Demo 4: Session comparison."""
    print_section_header("Demo 4: Session Comparison")

    console.print("[yellow]Creating two sessions with different approaches...[/yellow]")

    # Session 1: Western philosophers
    po = PoSelf(philosophers=["aristotle", "nietzsche", "sartre"], enable_trace=True)
    response1 = po.generate("What is justice?")
    session_id1 = response1.log["session_id"]
    console.print(f"[green]✓ Session 1 (Western): {session_id1[:8]}...[/green]")

    # Session 2: Eastern philosophers
    response2 = PoSelf(
        philosophers=["confucius", "zhuangzi", "watsuji"], enable_trace=True
    ).generate("What is justice?")
    session_id2 = response2.log["session_id"]
    console.print(f"[green]✓ Session 2 (Eastern): {session_id2[:8]}...[/green]")
    console.print()

    # Compare sessions
    viewer = PoViewer(po_trace=po.po_trace)
    console.print("[bold]⚖️  Comparing Western vs Eastern Perspectives:[/bold]")
    console.print(viewer.compare_sessions(session_id1, session_id2))


def demo_sessions_table():
    """Demo 5: Sessions table overview."""
    print_section_header("Demo 5: Sessions Table Overview")

    console.print("[yellow]Creating multiple sessions...[/yellow]")

    questions = [
        "What is truth?",
        "What is beauty?",
        "What is virtue?",
        "What is freedom?",
        "What is wisdom?",
    ]

    po = PoSelf(enable_trace=True)
    for i, question in enumerate(questions, 1):
        po.generate(question)
        console.print(f"[green]✓ Session {i}/5 created[/green]")

    console.print()

    # Show sessions table
    viewer = PoViewer(po_trace=po.po_trace)
    console.print("[bold]📋 Recent Sessions Table:[/bold]")
    console.print(viewer.render_sessions_table(limit=10))


def demo_json_export():
    """Demo 6: JSON export visualization."""
    print_section_header("Demo 6: JSON Export Visualization")

    console.print("[yellow]Creating session for JSON export...[/yellow]")
    po = PoSelf(philosophers=["wittgenstein"], enable_trace=True)
    response = po.generate("What is the limit of language?")

    session_id = response.log["session_id"]
    viewer = PoViewer(po_trace=po.po_trace)

    console.print("[bold]📄 Session Data as JSON:[/bold]")
    console.print(viewer.render_session_json(session_id))


def demo_full_visualization():
    """Demo 7: Full comprehensive visualization."""
    print_section_header("Demo 7: Full Comprehensive Visualization")

    console.print(
        "[yellow]Creating comprehensive session with multiple philosophers...[/yellow]"
    )
    po = PoSelf(
        philosophers=[
            "aristotle",
            "nietzsche",
            "confucius",
            "sartre",
            "wabi_sabi",
        ],
        enable_trace=True,
    )
    response = po.generate("How should we live in harmony with nature and society?")

    session_id = response.log["session_id"]
    viewer = PoViewer(po_trace=po.po_trace)

    # Show all visualizations
    console.print(viewer.render_session_detail(session_id))
    console.print()

    console.print(viewer.render_metrics_bars(session_id))
    console.print()

    console.print(viewer.render_philosopher_interaction(session_id))
    console.print()

    console.print("[bold]🔄 Event Flow:[/bold]")
    console.print(viewer.render_event_flow(session_id))


def main():
    """Run all Po_viewer demos."""
    console.print(
        Panel.fit(
            "[bold magenta]Po_viewer Demonstration[/bold magenta]\n"
            "[cyan]Visualizing Philosophical Reasoning[/cyan]\n\n"
            "[white]This demo showcases all visualization features of Po_viewer.[/white]",
            border_style="magenta",
        )
    )

    demos = [
        ("Basic Visualization", demo_basic_visualization),
        ("Event Flow", demo_event_flow),
        ("Philosopher Interactions", demo_philosopher_interactions),
        ("Session Comparison", demo_session_comparison),
        ("Sessions Table", demo_sessions_table),
        ("JSON Export", demo_json_export),
        ("Full Visualization", demo_full_visualization),
    ]

    console.print("\n[bold yellow]Available Demos:[/bold yellow]")
    for i, (name, _) in enumerate(demos, 1):
        console.print(f"  {i}. {name}")

    console.print("\n[bold]Select demo number (1-7) or 'all' to run all demos:[/bold]")
    console.print("[dim](Press Enter for 'all')[/dim]")

    try:
        choice = input("> ").strip().lower()

        if choice == "" or choice == "all":
            # Run all demos
            for name, demo_func in demos:
                demo_func()
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # Run specific demo
            demos[int(choice) - 1][1]()
        else:
            console.print("[red]Invalid choice. Please enter 1-7 or 'all'.[/red]")
            return

        # Final summary
        console.print()
        console.print(
            Panel.fit(
                "[bold green]✓ Demonstration Complete![/bold green]\n\n"
                "[white]Po_viewer provides rich visualization for philosophical reasoning.[/white]\n"
                "[cyan]Try the CLI commands:[/cyan]\n"
                "[dim]  python -m po_core.po_viewer sessions\n"
                "  python -m po_core.po_viewer show <session_id>\n"
                "  python -m po_core.po_viewer metrics <session_id>[/dim]",
                border_style="green",
            )
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
