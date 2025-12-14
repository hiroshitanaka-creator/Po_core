"""
Tension Map Visualizer

Visualizes philosophical tensions and harmonies between philosophers
as a matrix/heatmap with ASCII art representation.
"""

from typing import Any, Dict, List

import numpy as np
from rich.table import Table
from rich.text import Text

from po_core.viewer.visualizer import PhilosophicalVisualizer


class TensionMapVisualizer(PhilosophicalVisualizer):
    """
    Visualizer for philosophical tension maps.

    Displays:
    - Tension matrix between philosophers
    - Harmony matrix
    - Synthesis potential
    - Key tensions and harmonies
    """

    def render(self, data: Dict[str, Any]) -> None:
        """
        Render tension map visualization.

        Args:
            data: Interaction data from PhilosophicalEnsemble
        """
        self.print_header("🔥 Philosophical Tension Map")

        # Extract data
        interactions = data.get("interactions", {})
        if not interactions:
            self.console.print("[yellow]No interaction data available[/yellow]")
            return

        philosophers = interactions.get("philosophers", [])
        tension_matrix = np.array(interactions.get("tension_matrix", []))
        harmony_matrix = np.array(interactions.get("harmony_matrix", []))
        synthesis_potential = np.array(interactions.get("synthesis_potential_matrix", []))

        # Display tension matrix
        self._render_tension_matrix(philosophers, tension_matrix)

        # Display harmony matrix
        self._render_harmony_matrix(philosophers, harmony_matrix)

        # Display synthesis potential
        self._render_synthesis_potential(philosophers, synthesis_potential)

        # Display statistics
        self._render_statistics(interactions)

        # Display key tensions and harmonies
        self._render_key_interactions(interactions)

    def _render_tension_matrix(self, philosophers: List[str],
                               tensor_matrix: np.ndarray) -> None:
        """
        Render tension matrix as ASCII heatmap.

        Args:
            philosophers: List of philosopher names
            tensor_matrix: Tension values matrix
        """
        self.console.print("\n[bold red]Tension Matrix:[/bold red]")

        # Create table
        table = Table(show_header=True, header_style="bold red")
        table.add_column("", style="cyan")

        for phil in philosophers:
            table.add_column(phil[:8], justify="center")

        # Add rows
        for i, phil in enumerate(philosophers):
            row = [phil[:8]]
            for j in range(len(philosophers)):
                if i == j:
                    row.append("—")
                else:
                    value = tensor_matrix[i, j]
                    # Color code by intensity
                    if value > 0.7:
                        row.append(f"[bold red]{value:.2f}[/bold red]")
                    elif value > 0.4:
                        row.append(f"[yellow]{value:.2f}[/yellow]")
                    else:
                        row.append(f"[dim]{value:.2f}[/dim]")
            table.add_row(*row)

        self.console.print(table)

        # ASCII heatmap
        self.console.print("\n[dim]ASCII Heatmap (█ = high tension):[/dim]")
        self._render_ascii_heatmap(tensor_matrix, max_value=1.0)

    def _render_harmony_matrix(self, philosophers: List[str],
                               harmony_matrix: np.ndarray) -> None:
        """
        Render harmony matrix.

        Args:
            philosophers: List of philosopher names
            harmony_matrix: Harmony values matrix
        """
        self.console.print("\n[bold green]Harmony Matrix:[/bold green]")

        table = Table(show_header=True, header_style="bold green")
        table.add_column("", style="cyan")

        for phil in philosophers:
            table.add_column(phil[:8], justify="center")

        for i, phil in enumerate(philosophers):
            row = [phil[:8]]
            for j in range(len(philosophers)):
                if i == j:
                    row.append("—")
                else:
                    value = harmony_matrix[i, j]
                    # Color code by intensity
                    if value > 0.7:
                        row.append(f"[bold green]{value:.2f}[/bold green]")
                    elif value > 0.4:
                        row.append(f"[green]{value:.2f}[/green]")
                    else:
                        row.append(f"[dim]{value:.2f}[/dim]")
            table.add_row(*row)

        self.console.print(table)

        # ASCII heatmap
        self.console.print("\n[dim]ASCII Heatmap (█ = high harmony):[/dim]")
        self._render_ascii_heatmap(harmony_matrix, max_value=1.0)

    def _render_synthesis_potential(self, philosophers: List[str],
                                    synthesis_matrix: np.ndarray) -> None:
        """
        Render synthesis potential matrix.

        Args:
            philosophers: List of philosopher names
            synthesis_matrix: Synthesis potential matrix
        """
        self.console.print("\n[bold blue]Synthesis Potential:[/bold blue]")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("", style="cyan")

        for phil in philosophers:
            table.add_column(phil[:8], justify="center")

        for i, phil in enumerate(philosophers):
            row = [phil[:8]]
            for j in range(len(philosophers)):
                if i == j:
                    row.append("—")
                else:
                    value = synthesis_matrix[i, j]
                    # Color code by potential
                    if value > 0.7:
                        row.append(f"[bold blue]{value:.2f}[/bold blue]")
                    elif value > 0.4:
                        row.append(f"[blue]{value:.2f}[/blue]")
                    else:
                        row.append(f"[dim]{value:.2f}[/dim]")
            table.add_row(*row)

        self.console.print(table)

    def _render_ascii_heatmap(self, matrix: np.ndarray, max_value: float = 1.0) -> None:
        """
        Render ASCII heatmap.

        Args:
            matrix: Value matrix
            max_value: Maximum value for normalization
        """
        # Heatmap characters (low to high)
        chars = [" ", "░", "▒", "▓", "█"]

        for row in matrix:
            line = ""
            for value in row:
                # Normalize and map to character
                normalized = value / max_value
                char_idx = min(int(normalized * len(chars)), len(chars) - 1)
                line += chars[char_idx] * 2
            self.console.print(line)

    def _render_statistics(self, interactions: Dict[str, Any]) -> None:
        """
        Render statistical summary.

        Args:
            interactions: Interaction data
        """
        self.console.print("\n[bold magenta]Statistical Summary:[/bold magenta]")

        avg_harmony = interactions.get("average_harmony", 0.0)
        avg_tension = interactions.get("average_tension", 0.0)

        table = Table(show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")

        table.add_row("Average Harmony", f"{avg_harmony:.3f}")
        table.add_row("Average Tension", f"{avg_tension:.3f}")
        table.add_row("Harmony/Tension Ratio", f"{avg_harmony / max(avg_tension, 0.001):.3f}")

        self.console.print(table)

    def _render_key_interactions(self, interactions: Dict[str, Any]) -> None:
        """
        Render key interactions (highest tension and harmony).

        Args:
            interactions: Interaction data
        """
        pairwise = interactions.get("pairwise_interactions", [])
        if not pairwise:
            return

        self.console.print("\n[bold yellow]Key Interactions:[/bold yellow]")

        # Find highest tension
        highest_tension = max(pairwise, key=lambda x: x.get("tension", 0))
        self.console.print(
            f"\n[bold red]Highest Tension:[/bold red] "
            f"{highest_tension.get('philosopher_a')} ↔ {highest_tension.get('philosopher_b')}"
        )
        self.console.print(f"  Tension: {highest_tension.get('tension', 0):.3f}")
        self.console.print(f"  Harmony: {highest_tension.get('harmony', 0):.3f}")

        # Find highest harmony
        highest_harmony = max(pairwise, key=lambda x: x.get("harmony", 0))
        self.console.print(
            f"\n[bold green]Highest Harmony:[/bold green] "
            f"{highest_harmony.get('philosopher_a')} ↔ {highest_harmony.get('philosopher_b')}"
        )
        self.console.print(f"  Harmony: {highest_harmony.get('harmony', 0):.3f}")
        self.console.print(f"  Tension: {highest_harmony.get('tension', 0):.3f}")

        # Find best synthesis potential
        best_synthesis = max(pairwise, key=lambda x: x.get("synthesis_potential", 0))
        self.console.print(
            f"\n[bold blue]Best Synthesis Potential:[/bold blue] "
            f"{best_synthesis.get('philosopher_a')} ↔ {best_synthesis.get('philosopher_b')}"
        )
        self.console.print(f"  Potential: {best_synthesis.get('synthesis_potential', 0):.3f}")
