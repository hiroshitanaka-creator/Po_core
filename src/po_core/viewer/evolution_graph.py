"""
Evolution Graph Visualizer

Visualizes semantic evolution over time as a graph showing
how meaning transforms through philosophical reasoning.
"""

from typing import Any, Dict, List

import numpy as np
from rich.table import Table

from po_core.viewer.visualizer import PhilosophicalVisualizer


class EvolutionGraphVisualizer(PhilosophicalVisualizer):
    """
    Visualizer for semantic evolution graphs.

    Displays:
    - Semantic profile evolution over time
    - Dimensional changes
    - Evolution trajectory
    - Key transformation points
    """

    def render(self, data: Dict[str, Any]) -> None:
        """
        Render evolution graph visualization.

        Args:
            data: Data from PhilosophicalEnsemble with semantic_profile
        """
        self.print_header("📈 Semantic Evolution Graph")

        # Extract semantic profile data
        sp_data = data.get("semantic_profile", {})
        if not sp_data:
            self.console.print("[yellow]No semantic profile data available[/yellow]")
            return

        # Display evolution summary
        self._render_evolution_summary(sp_data)

        # Display evolution trajectory
        self._render_evolution_trajectory(sp_data)

        # Display dimensional evolution
        self._render_dimensional_evolution(sp_data)

        # Display key transformations
        self._render_transformations(sp_data)

    def _render_evolution_summary(self, sp_data: Dict[str, Any]) -> None:
        """
        Render evolution summary.

        Args:
            sp_data: Semantic profile data
        """
        self.console.print("\n[bold magenta]Evolution Summary:[/bold magenta]")

        history_length = sp_data.get("history_length", 0)
        total_evolution = sp_data.get("total_evolution", 0.0)

        table = Table(show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")

        table.add_row("Reasoning Steps", str(history_length))
        table.add_row("Total Evolution", f"{total_evolution:.4f}")

        if history_length > 1:
            avg_evolution = total_evolution / (history_length - 1)
            table.add_row("Average Step Evolution", f"{avg_evolution:.4f}")

        self.console.print(table)

        # Evolution intensity
        if total_evolution > 0.5:
            self.console.print(
                "\n[bold red]High semantic transformation[/bold red] - meaning evolved significantly"
            )
        elif total_evolution > 0.2:
            self.console.print(
                "\n[bold yellow]Moderate transformation[/bold yellow] - meaning shifted moderately"
            )
        else:
            self.console.print(
                "\n[dim]Low transformation[/dim] - meaning remained relatively stable"
            )

    def _render_evolution_trajectory(self, sp_data: Dict[str, Any]) -> None:
        """
        Render evolution trajectory as ASCII graph.

        Args:
            sp_data: Semantic profile data
        """
        self.console.print("\n[bold cyan]Evolution Trajectory:[/bold cyan]")

        # Get current semantic profile
        current_data = sp_data.get("data", [])
        dimension_names = sp_data.get("dimension_names", [])

        if not current_data or not dimension_names:
            self.console.print("[dim]No trajectory data[/dim]")
            return

        # Display current semantic position
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Dimension", style="cyan")
        table.add_column("Value", justify="right")
        table.add_column("Visualization", justify="left")

        for i, name in enumerate(dimension_names):
            value = current_data[i] if i < len(current_data) else 0.0

            # Format name
            display_name = name.replace("_", " ").title()

            # Create visualization
            left_label, right_label = self._get_dimension_labels(name)
            bar_pos = int(value * 20)
            bar = " " * bar_pos + "●" + " " * (20 - bar_pos)
            vis = f"{left_label[:8]:8s} |{bar}| {right_label[:8]:8s}"

            table.add_row(display_name, f"{value:.3f}", vis)

        self.console.print(table)

    def _get_dimension_labels(self, dimension_name: str) -> tuple:
        """
        Get left and right labels for a dimension.

        Args:
            dimension_name: Name of the dimension

        Returns:
            Tuple of (left_label, right_label)
        """
        labels = {
            "abstract_level": ("Concrete", "Abstract"),
            "concrete_level": ("Simple", "Complex"),
            "emotional_valence": ("Negative", "Positive"),
            "logical_coherence": ("Incoherent", "Coherent"),
            "novelty": ("Familiar", "Novel"),
            "depth": ("Shallow", "Deep"),
        }

        return labels.get(dimension_name, ("Low", "High"))

    def _render_dimensional_evolution(self, sp_data: Dict[str, Any]) -> None:
        """
        Render dimensional evolution over time.

        Args:
            sp_data: Semantic profile data
        """
        self.console.print("\n[bold yellow]Dimensional Evolution:[/bold yellow]")

        dimension_names = sp_data.get("dimension_names", [])
        history_length = sp_data.get("history_length", 0)

        if history_length < 2:
            self.console.print("[dim]Not enough history for evolution display[/dim]")
            return

        # Note: In a full implementation, we would get the actual history
        # For now, we show the current state and total evolution
        total_evolution = sp_data.get("total_evolution", 0.0)

        self.console.print(
            f"\nAcross {history_length} reasoning steps, "
            f"meaning evolved by [bold]{total_evolution:.4f}[/bold] units"
        )

        # Estimate which dimensions changed most (simplified)
        current_data = sp_data.get("data", [])

        if current_data:
            self.console.print("\n[bold]Current Semantic Characteristics:[/bold]")

            # Find prominent dimensions
            sorted_dims = sorted(
                enumerate(current_data), key=lambda x: abs(x[1] - 0.5), reverse=True
            )

            for idx, value in sorted_dims[:3]:
                if idx < len(dimension_names):
                    name = dimension_names[idx].replace("_", " ").title()
                    if value > 0.6:
                        self.console.print(f"  • High {name}: {value:.3f}")
                    elif value < 0.4:
                        self.console.print(f"  • Low {name}: {value:.3f}")

    def _render_transformations(self, sp_data: Dict[str, Any]) -> None:
        """
        Render key transformation points.

        Args:
            sp_data: Semantic profile data
        """
        self.console.print("\n[bold magenta]Key Transformations:[/bold magenta]")

        total_evolution = sp_data.get("total_evolution", 0.0)
        history_length = sp_data.get("history_length", 0)

        if history_length < 2:
            self.console.print("[dim]No transformations yet[/dim]")
            return

        # Identify transformation pattern
        if total_evolution > 0.5:
            self.console.print(
                "• [bold red]Major semantic shift[/bold red] detected\n"
                "  Meaning underwent significant transformation through reasoning"
            )
        elif total_evolution > 0.2:
            self.console.print(
                "• [bold yellow]Moderate semantic evolution[/bold yellow] observed\n"
                "  Meaning refined and developed through philosophical analysis"
            )
        else:
            self.console.print(
                "• [dim]Stable semantic pattern[/dim]\n"
                "  Meaning remained consistent across reasoning steps"
            )

        # Current semantic characteristics
        current_data = sp_data.get("data", [])
        dimension_names = sp_data.get("dimension_names", [])

        if current_data and dimension_names:
            # Identify dominant characteristic
            max_idx = int(np.argmax([abs(v - 0.5) for v in current_data]))
            max_dim = (
                dimension_names[max_idx]
                if max_idx < len(dimension_names)
                else "unknown"
            )
            max_value = current_data[max_idx] if max_idx < len(current_data) else 0.5

            direction = "high" if max_value > 0.5 else "low"
            self.console.print(
                f"\n• [bold]Dominant characteristic:[/bold] "
                f"{max_dim.replace('_', ' ')} ({direction}, {max_value:.3f})"
            )

    def render_ascii_timeline(
        self, values: List[float], width: int = 50, height: int = 10
    ) -> None:
        """
        Render an ASCII timeline graph.

        Args:
            values: List of values to plot
            width: Width of the graph
            height: Height of the graph
        """
        if not values:
            return

        # Normalize values to height
        min_val = min(values)
        max_val = max(values)
        value_range = max_val - min_val if max_val > min_val else 1.0

        # Create graph grid
        graph = [[" " for _ in range(width)] for _ in range(height)]

        # Plot values
        for i, value in enumerate(values):
            if i >= width:
                break

            normalized = (value - min_val) / value_range
            y = int((1 - normalized) * (height - 1))
            y = max(0, min(height - 1, y))

            graph[y][i] = "●"

            # Draw connecting line
            if i > 0:
                prev_value = values[i - 1]
                prev_normalized = (prev_value - min_val) / value_range
                prev_y = int((1 - prev_normalized) * (height - 1))
                prev_y = max(0, min(height - 1, prev_y))

                # Draw vertical line between points
                if abs(y - prev_y) > 1:
                    start = min(y, prev_y)
                    end = max(y, prev_y)
                    for dy in range(start + 1, end):
                        if graph[dy][i] == " ":
                            graph[dy][i] = "│"

        # Print graph
        self.console.print("\n[dim]Timeline:[/dim]")
        for row in graph:
            self.console.print("".join(row))

        # Print axis
        self.console.print("─" * width)
        self.console.print(f"Min: {min_val:.2f}  Max: {max_val:.2f}")
