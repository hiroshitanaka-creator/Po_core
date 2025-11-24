"""
Po_core CLI - Main Command Line Interface

Entry point for the po-core command.
"""

import click
from rich.console import Console
from rich.table import Table

from po_core import __author__, __email__, __version__
from po_core import po_self, po_trace, po_viewer

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="po-core")
def main() -> None:
    """
    Po_core: Philosophy-Driven AI System 🐷🎈

    A system that integrates philosophers as dynamic tensors
    for responsible meaning generation.
    """
    pass


@main.command()
def hello() -> None:
    """Say hello from Po_core"""
    console.print("[bold blue]🐷🎈 Po_core へようこそ![/bold blue]")
    console.print("Philosophy-Driven AI System - Alpha v0.1.0")
    console.print("\n[italic]A frog in a well may not know the ocean, but it can know the sky.[/italic]")


@main.command()
def status() -> None:
    """Show project status"""
    console.print("[bold]📊 Po_core Project Status[/bold]\n")
    console.print("✅ Philosophical Framework: 100%")
    console.print("✅ Documentation: 100%")
    console.print("✅ Architecture Design: 100%")
    console.print("🔄 Implementation: 40%")
    console.print("⏳ Testing: 10%")
    console.print("⏳ Visualization: 10%")


@main.command()
def version() -> None:
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


main.add_command(po_trace.cli, name="trace")
main.add_command(po_self.cli, name="self")
main.add_command(po_viewer.cli, name="view")


if __name__ == "__main__":
    main()
