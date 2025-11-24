"""
Interactive Reasoning CLI

Interactive command-line interface for philosophical reasoning sessions.
Allows users to:
- Select philosophers for the ensemble
- Enter prompts and receive philosophical reasoning
- View visualizations of tension, pressure, and evolution
- Export reasoning traces
"""

import json
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from po_core.philosophers import (
    Arendt,
    Aristotle,
    Badiou,
    Confucius,
    Deleuze,
    Derrida,
    Dewey,
    Heidegger,
    Jung,
    Kierkegaard,
    Lacan,
    Levinas,
    MerleauPonty,
    Nietzsche,
    Peirce,
    Sartre,
    WabiSabi,
    Watsuji,
    Wittgenstein,
    Zhuangzi,
)
from po_core.po_self import PhilosophicalEnsemble
from po_core.viewer import (
    EvolutionGraphVisualizer,
    PressureDisplayVisualizer,
    TensionMapVisualizer,
)


# Available philosophers
AVAILABLE_PHILOSOPHERS = {
    "sartre": (Sartre, "Jean-Paul Sartre - Existentialism"),
    "nietzsche": (Nietzsche, "Friedrich Nietzsche - Will to Power"),
    "heidegger": (Heidegger, "Martin Heidegger - Being and Time"),
    "derrida": (Derrida, "Jacques Derrida - Deconstruction"),
    "wittgenstein": (Wittgenstein, "Ludwig Wittgenstein - Language Philosophy"),
    "confucius": (Confucius, "Confucius - Virtue Ethics"),
    "zhuangzi": (Zhuangzi, "Zhuangzi - Daoism"),
    "aristotle": (Aristotle, "Aristotle - Virtue and Logic"),
    "kierkegaard": (Kierkegaard, "Søren Kierkegaard - Existentialism"),
    "levinas": (Levinas, "Emmanuel Levinas - Ethics of the Other"),
    "arendt": (Arendt, "Hannah Arendt - Political Philosophy"),
    "deleuze": (Deleuze, "Gilles Deleuze - Difference and Repetition"),
    "badiou": (Badiou, "Alain Badiou - Event Philosophy"),
    "dewey": (Dewey, "John Dewey - Pragmatism"),
    "peirce": (Peirce, "Charles Sanders Peirce - Semiotics"),
    "jung": (Jung, "Carl Jung - Analytical Psychology"),
    "lacan": (Lacan, "Jacques Lacan - Psychoanalysis"),
    "merleau_ponty": (MerleauPonty, "Maurice Merleau-Ponty - Phenomenology"),
    "watsuji": (Watsuji, "Watsuji Tetsurō - Japanese Ethics"),
    "wabi_sabi": (WabiSabi, "Wabi-Sabi - Japanese Aesthetics"),
}


class InteractiveReasoningSession:
    """
    Interactive reasoning session manager.

    Manages:
    - Philosopher selection
    - Prompt input
    - Reasoning execution
    - Visualization display
    - Trace export
    """

    def __init__(self):
        """Initialize interactive session."""
        self.console = Console()
        self.ensemble: Optional[PhilosophicalEnsemble] = None
        self.selected_philosophers: List[str] = []
        self.reasoning_history: List[Dict[str, Any]] = []

        # Visualizers
        self.tension_visualizer = TensionMapVisualizer(console=self.console)
        self.pressure_visualizer = PressureDisplayVisualizer(console=self.console)
        self.evolution_visualizer = EvolutionGraphVisualizer(console=self.console)

    def run(self) -> None:
        """Run the interactive session."""
        self._print_welcome()

        # Step 1: Select philosophers
        if not self._select_philosophers():
            return

        # Step 2: Create ensemble
        self._create_ensemble()

        # Step 3: Interactive reasoning loop
        self._reasoning_loop()

        # Step 4: Session summary and export
        self._session_summary()

    def _print_welcome(self) -> None:
        """Print welcome message."""
        welcome_text = """
[bold magenta]🧠 Po_core Interactive Reasoning Session[/bold magenta]

Welcome to the philosophical reasoning interface!
You will:
  1. Select philosophers for your ensemble
  2. Enter prompts for philosophical analysis
  3. View multi-dimensional insights and visualizations
  4. Export reasoning traces for further study

[dim]Press Ctrl+C at any time to exit[/dim]
        """
        self.console.print(Panel(welcome_text, border_style="magenta"))

    def _select_philosophers(self) -> bool:
        """
        Select philosophers for the ensemble.

        Returns:
            True if philosophers were selected, False otherwise
        """
        self.console.rule("[bold cyan]Step 1: Select Philosophers[/bold cyan]")

        # Display available philosophers
        self.console.print("\n[bold]Available Philosophers:[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", justify="right", style="cyan")
        table.add_column("Key", style="yellow")
        table.add_column("Philosopher", style="green")

        phil_list = sorted(AVAILABLE_PHILOSOPHERS.items())
        for i, (key, (_, desc)) in enumerate(phil_list, 1):
            table.add_column(f"{i}", style="dim")
            table.add_row(str(i), key, desc)

        self.console.print(table)

        # Get selection
        self.console.print("\n[bold]Selection options:[/bold]")
        self.console.print("  • Enter philosopher keys separated by commas (e.g., 'sartre,nietzsche,heidegger')")
        self.console.print("  • Enter 'all' to use all philosophers")
        self.console.print("  • Press Enter for default selection (sartre, nietzsche, heidegger)")

        selection = Prompt.ask("\n[cyan]Select philosophers[/cyan]", default="sartre,nietzsche,heidegger")

        if selection.lower() == "all":
            self.selected_philosophers = list(AVAILABLE_PHILOSOPHERS.keys())
        else:
            selected = [s.strip().lower() for s in selection.split(",")]
            # Validate selection
            valid = [s for s in selected if s in AVAILABLE_PHILOSOPHERS]
            if not valid:
                self.console.print("[red]No valid philosophers selected. Exiting.[/red]")
                return False
            self.selected_philosophers = valid

        # Confirm selection
        self.console.print(f"\n[green]✓ Selected {len(self.selected_philosophers)} philosophers:[/green]")
        for phil in self.selected_philosophers:
            desc = AVAILABLE_PHILOSOPHERS[phil][1]
            self.console.print(f"  • {desc}")

        return True

    def _create_ensemble(self) -> None:
        """Create philosophical ensemble with selected philosophers."""
        self.console.print("\n[yellow]Creating ensemble...[/yellow]")

        # Instantiate philosophers
        philosophers = []
        for phil_key in self.selected_philosophers:
            PhilClass, _ = AVAILABLE_PHILOSOPHERS[phil_key]
            philosophers.append(PhilClass())

        # Create ensemble
        self.ensemble = PhilosophicalEnsemble(
            philosophers=philosophers,
            enable_tracing=True
        )

        self.console.print(f"[green]✓ Ensemble created with {len(philosophers)} philosophers[/green]")

    def _reasoning_loop(self) -> None:
        """Interactive reasoning loop."""
        self.console.rule("[bold cyan]Step 2: Interactive Reasoning[/bold cyan]")

        while True:
            try:
                # Get prompt
                self.console.print()
                prompt = Prompt.ask("[bold cyan]Enter your philosophical question[/bold cyan] (or 'quit' to exit)")

                if prompt.lower() in ["quit", "exit", "q"]:
                    break

                if not prompt.strip():
                    continue

                # Execute reasoning
                self.console.print("\n[yellow]🤔 Reasoning...[/yellow]")
                result = self.ensemble.reason(prompt)
                self.reasoning_history.append(result)

                # Display result
                self._display_result(result)

                # Ask for visualizations
                if Confirm.ask("\n[cyan]View visualizations?[/cyan]", default=True):
                    self._show_visualizations(result)

                # Ask to continue
                if not Confirm.ask("\n[cyan]Continue with another question?[/cyan]", default=True):
                    break

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Session interrupted[/yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[red]Error: {e}[/red]")
                if not Confirm.ask("[cyan]Continue?[/cyan]", default=True):
                    break

    def _display_result(self, result: Dict[str, Any]) -> None:
        """
        Display reasoning result.

        Args:
            result: Reasoning result from ensemble
        """
        self.console.rule("[bold green]Reasoning Result[/bold green]")

        # Display synthesis
        synthesis = result.get("synthesis", {})
        self.console.print("\n[bold magenta]Synthesis:[/bold magenta]")

        insights = synthesis.get("insights", [])
        for insight in insights:
            phil = insight.get("philosopher", "Unknown")
            insight_text = insight.get("insight", "")
            self.console.print(f"\n[bold cyan]{phil}:[/bold cyan]")
            self.console.print(f"  {insight_text}")

        # Display tensions
        tensions = synthesis.get("tensions", [])
        if tensions:
            self.console.print("\n[bold red]Philosophical Tensions:[/bold red]")
            for tension in tensions:
                desc = tension.get("description", "")
                self.console.print(f"  • {desc}")

        # Display annotations
        annotations = result.get("annotations", [])
        if annotations:
            self.console.print("\n[bold yellow]Key Philosophical Concepts:[/bold yellow]")
            # Show top 5 concepts
            for ann in annotations[:5]:
                concept = ann.get("concept", "")
                definition = ann.get("definition", "")
                self.console.print(f"  • [cyan]{concept}[/cyan]: {definition[:80]}...")

    def _show_visualizations(self, result: Dict[str, Any]) -> None:
        """
        Show visualizations menu.

        Args:
            result: Reasoning result
        """
        while True:
            self.console.print("\n[bold]Available Visualizations:[/bold]")
            self.console.print("  1. Tension Map - Philosopher interactions")
            self.console.print("  2. Pressure Display - Freedom and ethical dimensions")
            self.console.print("  3. Evolution Graph - Semantic transformation")
            self.console.print("  4. All visualizations")
            self.console.print("  5. Back to reasoning")

            choice = Prompt.ask("[cyan]Select visualization[/cyan]", choices=["1", "2", "3", "4", "5"], default="5")

            if choice == "1":
                self.tension_visualizer.render(result)
            elif choice == "2":
                self.pressure_visualizer.render(result)
            elif choice == "3":
                self.evolution_visualizer.render(result)
            elif choice == "4":
                self.tension_visualizer.render(result)
                self.pressure_visualizer.render(result)
                self.evolution_visualizer.render(result)
            elif choice == "5":
                break

            if choice != "5" and not Confirm.ask("\n[cyan]View another visualization?[/cyan]", default=False):
                break

    def _session_summary(self) -> None:
        """Display session summary and offer export."""
        self.console.rule("[bold cyan]Session Summary[/bold cyan]")

        self.console.print(f"\n[bold]Reasoning Sessions:[/bold] {len(self.reasoning_history)}")
        self.console.print(f"[bold]Philosophers:[/bold] {len(self.selected_philosophers)}")

        if self.reasoning_history:
            # Offer trace export
            if Confirm.ask("\n[cyan]Export reasoning traces?[/cyan]", default=False):
                self._export_traces()

        self.console.print("\n[bold green]Thank you for using Po_core Interactive Reasoning![/bold green]")

    def _export_traces(self) -> None:
        """Export reasoning traces to JSON file."""
        filename = Prompt.ask("[cyan]Enter filename[/cyan]", default="po_core_reasoning_trace.json")

        try:
            export_data = {
                "session": {
                    "philosophers": self.selected_philosophers,
                    "total_reasonings": len(self.reasoning_history)
                },
                "reasoning_history": self.reasoning_history
            }

            with open(filename, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            self.console.print(f"[green]✓ Traces exported to {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting traces: {e}[/red]")


def main() -> None:
    """Main entry point for interactive CLI."""
    session = InteractiveReasoningSession()
    try:
        session.run()
    except KeyboardInterrupt:
        session.console.print("\n\n[yellow]Session terminated by user[/yellow]")
    except Exception as e:
        session.console.print(f"\n\n[red]Unexpected error: {e}[/red]")


if __name__ == "__main__":
    main()
