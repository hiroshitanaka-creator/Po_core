#!/usr/bin/env python3
"""
Po_core Visualization Demo (No API Required)

Demonstrates Po_viewer visualizations using mock data.
Perfect for testing without LLM API costs.

Usage:
    python examples/no_api_visualization_demo.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from po_core.mock_philosophers import MockPoSelf, create_mock_sessions
from po_core.visualizations import PoVisualizer
from rich.console import Console

console = Console()


def main() -> None:
    """Run API-free visualization demo."""
    console.print("[bold magenta]🎨 Po_core Visualization Demo (No API)[/bold magenta]")
    console.print("[dim]Using mock philosophers - no LLM API required![/dim]\n")

    # Create output directory
    output_dir = Path("./visualization_outputs_no_api")
    output_dir.mkdir(exist_ok=True)
    console.print(f"[cyan]Output directory:[/cyan] {output_dir.absolute()}\n")

    # Initialize Mock Po_self
    console.print("[yellow]1. Initializing mock philosophical ensemble...[/yellow]")
    mock_po = MockPoSelf(enable_trace=True)
    console.print(
        "   [green]✓[/green] Mock ensemble ready (20 philosophers available)\n"
    )

    # Generate some philosophical responses
    prompts = [
        "What is the meaning of freedom?",
        "How should we balance individual liberty with social responsibility?",
        "What makes a life worth living?",
    ]

    session_ids = []

    for i, prompt in enumerate(prompts, 1):
        console.print(f'[yellow]{i+1}. Generating response to:[/yellow] "{prompt}"')

        # Generate with random 3-5 philosophers
        result = mock_po.generate(prompt)

        session_id = result["log"]["session_id"]
        session_ids.append(session_id)

        console.print(f"   [green]✓[/green] Session ID: {session_id[:12]}...")
        console.print(
            f"   [dim]Philosophers: {', '.join(result['philosophers_involved'])}[/dim]"
        )
        console.print(
            f"   [dim]Metrics: FP={result['freedom_pressure']:.2f}, "
            f"SD={result['semantic_delta']:.2f}, BT={result['blocked_tensor']:.2f}[/dim]\n"
        )

    # Initialize visualizer
    console.print("[yellow]3. Creating visualizations...[/yellow]\n")
    visualizer = PoVisualizer(po_trace=mock_po.po_trace)

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
            title="Philosophical Reasoning Evolution (Mock Data)",
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

    console.print("\n[bold yellow]🎯 Key Advantages of Mock Testing:[/bold yellow]")
    console.print("  ✓ [green]No API costs[/green] - Completely free to run")
    console.print("  ✓ [green]Deterministic[/green] - Same input = same output")
    console.print("  ✓ [green]Fast[/green] - No network latency")
    console.print("  ✓ [green]Offline[/green] - Works without internet")
    console.print("  ✓ [green]Reproducible[/green] - Perfect for testing & development")

    console.print("\n[bold]Next Steps:[/bold]")
    console.print("  1. Open .html files in a browser for interactive exploration")
    console.print("  2. View .png files with any image viewer")
    console.print("  3. Try with custom prompts by modifying this script")

    console.print("\n[bold]Create Your Own Mock Sessions:[/bold]")
    console.print("  ```python")
    console.print("  from po_core.mock_philosophers import MockPoSelf")
    console.print("  ")
    console.print("  mock_po = MockPoSelf(enable_trace=True)")
    console.print("  result = mock_po.generate('Your question here')")
    console.print("  ```")

    console.print("\n[dim]🐷🎈 Testing pigs can fly without the API bill...[/dim]")


if __name__ == "__main__":
    main()
