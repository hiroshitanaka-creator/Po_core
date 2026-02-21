#!/usr/bin/env python3
"""
Po_core Visualization Demo

Demonstrates the advanced visualization capabilities of Po_viewer.

Usage:
    python examples/visualization_demo.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console

from po_core.po_self import PoSelf
from po_core.visualizations import PoVisualizer

console = Console()


def main() -> None:
    """Run visualization demo."""
    console.print("[bold magenta]🎨 Po_core Visualization Demo[/bold magenta]\n")

    # Create output directory
    output_dir = Path("./visualization_outputs")
    output_dir.mkdir(exist_ok=True)
    console.print(f"[cyan]Output directory:[/cyan] {output_dir.absolute()}\n")

    # Initialize Po_self with tracing enabled
    console.print("[yellow]1. Initializing Po_self with tracing...[/yellow]")
    po_self = PoSelf(enable_trace=True)

    # Generate some philosophical responses
    prompts = [
        "What is the meaning of freedom?",
        "How should we balance individual liberty with social responsibility?",
        "What makes a life worth living?",
    ]

    session_ids = []

    for i, prompt in enumerate(prompts, 1):
        console.print(f'\n[yellow]{i+1}. Generating response to:[/yellow] "{prompt}"')
        result = po_self.generate(prompt)
        session_id = result.log["session_id"]
        session_ids.append(session_id)
        console.print(f"   [green]✓[/green] Session ID: {session_id[:12]}...")

    # Initialize visualizer
    console.print("\n[yellow]3. Creating visualizations...[/yellow]\n")
    visualizer = PoVisualizer(po_trace=po_self.po_trace)

    # Use the first session for detailed visualizations
    demo_session = session_ids[0]

    # 1. Tension Map
    console.print("[cyan]   Creating tension map...[/cyan]")
    try:
        tension_path = output_dir / f"tension_map_{demo_session[:8]}.png"
        visualizer.create_tension_map(
            session_id=demo_session, output_path=tension_path, format="png"
        )
        console.print(f"   [green]✓[/green] Saved: {tension_path}")
    except Exception as e:
        console.print(f"   [red]✗[/red] Error: {e}")

    # 2. Philosopher Network
    console.print("[cyan]   Creating philosopher network...[/cyan]")
    try:
        network_path = output_dir / f"network_{demo_session[:8]}.png"
        visualizer.create_philosopher_network(
            session_id=demo_session, output_path=network_path, format="png"
        )
        console.print(f"   [green]✓[/green] Saved: {network_path}")
    except Exception as e:
        console.print(f"   [red]✗[/red] Error: {e}")

    # 3. Interactive Dashboard
    console.print("[cyan]   Creating interactive dashboard...[/cyan]")
    try:
        dashboard_path = output_dir / f"dashboard_{demo_session[:8]}.html"
        visualizer.create_comprehensive_dashboard(
            session_id=demo_session, output_path=dashboard_path, format="html"
        )
        console.print(f"   [green]✓[/green] Saved: {dashboard_path}")
        console.print(f"   [dim]Open in browser to explore interactive features[/dim]")
    except Exception as e:
        console.print(f"   [red]✗[/red] Error: {e}")

    # 4. Metrics Timeline (across all sessions)
    console.print("[cyan]   Creating metrics timeline...[/cyan]")
    try:
        timeline_path = output_dir / "metrics_timeline.html"
        visualizer.create_metrics_timeline(
            session_ids=session_ids,
            output_path=timeline_path,
            format="html",
            title="Philosophical Reasoning Evolution",
        )
        console.print(f"   [green]✓[/green] Saved: {timeline_path}")
        console.print(
            f"   [dim]Shows metrics evolution across {len(session_ids)} sessions[/dim]"
        )
    except Exception as e:
        console.print(f"   [red]✗[/red] Error: {e}")

    # 5. Export all visualizations for one session
    console.print("\n[yellow]4. Exporting all visualizations...[/yellow]")
    try:
        results = visualizer.export_session_visualizations(
            session_id=demo_session,
            output_dir=output_dir / "complete_export",
            formats=["png", "html"],
        )
        console.print(f"   [green]✓[/green] Exported {len(results)} visualizations:")
        for name, path in results.items():
            console.print(f"      • {name}: {path.name}")
    except Exception as e:
        console.print(f"   [red]✗[/red] Error: {e}")

    # Summary
    console.print("\n[bold green]✓ Visualization demo complete![/bold green]")
    console.print(
        f"\n[cyan]All visualizations saved to:[/cyan] {output_dir.absolute()}"
    )
    console.print("\n[bold]What was created:[/bold]")
    console.print(
        "  • [yellow]Tension Map[/yellow] - Heatmap of philosophical tensions"
    )
    console.print(
        "  • [yellow]Network Graph[/yellow] - Philosopher interaction network"
    )
    console.print(
        "  • [yellow]Interactive Dashboard[/yellow] - Comprehensive multi-view analysis"
    )
    console.print("  • [yellow]Metrics Timeline[/yellow] - Evolution across sessions")

    console.print("\n[bold]How to use:[/bold]")
    console.print("  • Open .html files in a web browser for interactive exploration")
    console.print("  • View .png files with any image viewer")
    console.print("  • Use po-viewer CLI commands for custom visualizations")

    console.print("\n[bold]CLI Examples:[/bold]")
    console.print(f"  po-viewer tension-map {demo_session[:12]} -o my_tension.png")
    console.print(f"  po-viewer network {demo_session[:12]} -o my_network.svg")
    console.print(f"  po-viewer viz-dashboard {demo_session[:12]} -o my_dash.html")
    console.print(
        f"  po-viewer export-all {demo_session[:12]} -d ./my_viz -f png -f html"
    )

    console.print("\n[dim]🐷🎈 When pigs fly through philosophical space...[/dim]")


if __name__ == "__main__":
    main()
