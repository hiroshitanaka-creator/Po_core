"""
Base Visualizer Class

Abstract base for all Po_core visualizers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class PhilosophicalVisualizer(ABC):
    """
    Abstract base class for philosophical visualizations.

    All visualizers should inherit from this class and implement
    the render() method.
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize visualizer.

        Args:
            console: Rich console for output (creates new if not provided)
        """
        self.console = console or Console()

    @abstractmethod
    def render(self, data: Dict[str, Any]) -> None:
        """
        Render visualization.

        Args:
            data: Data to visualize
        """
        pass

    def create_titled_panel(self, content: Any, title: str,
                           subtitle: Optional[str] = None) -> Panel:
        """
        Create a titled panel for display.

        Args:
            content: Panel content
            title: Panel title
            subtitle: Optional subtitle

        Returns:
            Rich Panel object
        """
        return Panel(
            content,
            title=f"[bold cyan]{title}[/bold cyan]",
            subtitle=subtitle,
            border_style="cyan",
            padding=(1, 2)
        )

    def create_data_table(self, title: str, columns: list) -> Table:
        """
        Create a styled data table.

        Args:
            title: Table title
            columns: List of column names

        Returns:
            Rich Table object
        """
        table = Table(title=title, show_header=True, header_style="bold magenta")

        for column in columns:
            table.add_column(column)

        return table

    def print_header(self, title: str) -> None:
        """
        Print a formatted header.

        Args:
            title: Header title
        """
        self.console.rule(f"[bold magenta]{title}[/bold magenta]")

    def print_section(self, title: str, content: str) -> None:
        """
        Print a formatted section.

        Args:
            title: Section title
            content: Section content
        """
        self.console.print(f"\n[bold cyan]{title}:[/bold cyan]")
        self.console.print(content)
