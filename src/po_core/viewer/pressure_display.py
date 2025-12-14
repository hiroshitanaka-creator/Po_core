"""
Pressure Display Visualizer

Visualizes Freedom Pressure Tensor and ethical stakes
as bar charts and dimensional breakdowns.
"""

from typing import Any, Dict

import numpy as np
from rich.bar import Bar
from rich.table import Table

from po_core.viewer.visualizer import PhilosophicalVisualizer


class PressureDisplayVisualizer(PhilosophicalVisualizer):
    """
    Visualizer for Freedom Pressure and ethical dimensions.

    Displays:
    - Freedom Pressure by dimension
    - Ethical stakes visualization
    - Responsibility metrics
    - Temporal urgency indicators
    """

    def render(self, data: Dict[str, Any]) -> None:
        """
        Render pressure display visualization.

        Args:
            data: Data from PhilosophicalEnsemble with freedom_pressure
        """
        self.print_header("⚖️ Freedom Pressure & Ethical Dimensions")

        # Extract freedom pressure data
        fp_data = data.get("freedom_pressure", {})
        if not fp_data:
            self.console.print("[yellow]No freedom pressure data available[/yellow]")
            return

        # Display overall pressure
        self._render_overall_pressure(fp_data)

        # Display dimensional breakdown
        self._render_dimensional_breakdown(fp_data)

        # Display pressure bars
        self._render_pressure_bars(fp_data)

        # Display key insights
        self._render_insights(fp_data)

    def _render_overall_pressure(self, fp_data: Dict[str, Any]) -> None:
        """
        Render overall pressure summary.

        Args:
            fp_data: Freedom pressure data
        """
        summary = fp_data.get("pressure_summary", {})
        total_pressure = summary.get("total_pressure", 0.0)
        max_dimension = summary.get("max_dimension", {})

        self.console.print("\n[bold magenta]Overall Assessment:[/bold magenta]")

        # Pressure level indicator
        if total_pressure > 0.7:
            level = "[bold red]CRITICAL[/bold red]"
            indicator = "🔴"
        elif total_pressure > 0.5:
            level = "[bold yellow]HIGH[/bold yellow]"
            indicator = "🟡"
        elif total_pressure > 0.3:
            level = "[bold blue]MODERATE[/bold blue]"
            indicator = "🔵"
        else:
            level = "[dim]LOW[/dim]"
            indicator = "🟢"

        self.console.print(f"{indicator} Pressure Level: {level}")
        self.console.print(f"Total Pressure: {total_pressure:.3f}")

        if max_dimension:
            max_dim_name = max_dimension.get("name", "Unknown")
            max_dim_value = max_dimension.get("value", 0.0)
            self.console.print(
                f"Primary Pressure: [cyan]{max_dim_name}[/cyan] ({max_dim_value:.3f})"
            )

    def _render_dimensional_breakdown(self, fp_data: Dict[str, Any]) -> None:
        """
        Render dimensional breakdown table.

        Args:
            fp_data: Freedom pressure data
        """
        self.console.print("\n[bold cyan]Dimensional Breakdown:[/bold cyan]")

        dimensions = fp_data.get("pressure_summary", {}).get("dimensions", [])
        if not dimensions:
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Dimension", style="cyan")
        table.add_column("Value", justify="right")
        table.add_column("Level", justify="center")
        table.add_column("Bar", justify="left")

        for dim in dimensions:
            name = dim.get("name", "").replace("_", " ").title()
            value = dim.get("value", 0.0)

            # Determine level
            if value > 0.7:
                level = "[red]High[/red]"
            elif value > 0.4:
                level = "[yellow]Medium[/yellow]"
            else:
                level = "[dim]Low[/dim]"

            # Create simple ASCII bar
            bar_length = int(value * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)

            table.add_row(name, f"{value:.3f}", level, bar)

        self.console.print(table)

    def _render_pressure_bars(self, fp_data: Dict[str, Any]) -> None:
        """
        Render pressure as horizontal bars.

        Args:
            fp_data: Freedom pressure data
        """
        self.console.print("\n[bold yellow]Pressure Visualization:[/bold yellow]")

        dimension_names = fp_data.get("dimension_names", [])
        data_array = fp_data.get("data", [])

        if not dimension_names or not data_array:
            return

        for i, name in enumerate(dimension_names):
            value = data_array[i] if i < len(data_array) else 0.0

            # Format name
            display_name = name.replace("_", " ").title()[:20]

            # Color by value
            if value > 0.7:
                color = "red"
            elif value > 0.4:
                color = "yellow"
            else:
                color = "green"

            # Create bar
            bar_width = int(value * 50)
            bar = f"[{color}]{'█' * bar_width}[/{color}]"

            self.console.print(f"{display_name:20s} {value:5.2f} {bar}")

    def _render_insights(self, fp_data: Dict[str, Any]) -> None:
        """
        Render key insights about pressure.

        Args:
            fp_data: Freedom pressure data
        """
        self.console.print("\n[bold magenta]Key Insights:[/bold magenta]")

        dimensions = fp_data.get("pressure_summary", {}).get("dimensions", [])
        if not dimensions:
            return

        # Find highest and lowest pressure dimensions
        sorted_dims = sorted(dimensions, key=lambda d: d.get("value", 0), reverse=True)

        highest = sorted_dims[0] if sorted_dims else None
        lowest = sorted_dims[-1] if sorted_dims else None

        if highest:
            name = highest.get("name", "").replace("_", " ")
            value = highest.get("value", 0)
            self.console.print(
                f"• [red]Highest pressure:[/red] {name} ({value:.3f})"
            )

            # Interpretation
            if "ethical" in name.lower():
                self.console.print("  → Strong ethical considerations present")
            elif "responsibility" in name.lower():
                self.console.print("  → High sense of responsibility and accountability")
            elif "temporal" in name.lower():
                self.console.print("  → Time-sensitive decision with urgency")
            elif "choice" in name.lower():
                self.console.print("  → Significant choice weight and agency")
            elif "social" in name.lower():
                self.console.print("  → Strong social impact concerns")
            elif "authenticity" in name.lower():
                self.console.print("  → Authenticity and genuine expression emphasized")

        if lowest:
            name = lowest.get("name", "").replace("_", " ")
            value = lowest.get("value", 0)
            self.console.print(
                f"\n• [dim]Lowest pressure:[/dim] {name} ({value:.3f})"
            )

        # Overall interpretation
        total = fp_data.get("pressure_summary", {}).get("total_pressure", 0)
        self.console.print(f"\n[bold]Overall Interpretation:[/bold]")

        if total > 0.7:
            self.console.print(
                "This situation carries [bold red]critical existential weight[/bold red]. "
                "Freedom and responsibility are highly engaged. Authentic choice is crucial."
            )
        elif total > 0.5:
            self.console.print(
                "This situation involves [bold yellow]significant freedom pressure[/bold yellow]. "
                "Multiple dimensions of responsibility are active. Careful consideration warranted."
            )
        elif total > 0.3:
            self.console.print(
                "This situation has [bold blue]moderate pressure[/bold blue]. "
                "Some freedom and responsibility present, but not overwhelming."
            )
        else:
            self.console.print(
                "This situation has [dim]low freedom pressure[/dim]. "
                "Less urgent or less tied to existential responsibility."
            )
