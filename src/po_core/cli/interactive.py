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
import sys
from typing import Any, Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from po_core.po_self import PoSelf
from po_core.viewer import (
    EvolutionGraphVisualizer,
    PressureDisplayVisualizer,
    TensionMapVisualizer,
)

# Available philosophers
AVAILABLE_PHILOSOPHERS = {
    "sartre": "Jean-Paul Sartre - Existentialism",
    "nietzsche": "Friedrich Nietzsche - Will to Power",
    "heidegger": "Martin Heidegger - Being and Time",
    "derrida": "Jacques Derrida - Deconstruction",
    "wittgenstein": "Ludwig Wittgenstein - Language Philosophy",
    "confucius": "Confucius - Virtue Ethics",
    "zhuangzi": "Zhuangzi - Daoism",
    "aristotle": "Aristotle - Virtue and Logic",
    "kierkegaard": "Søren Kierkegaard - Existentialism",
    "levinas": "Emmanuel Levinas - Ethics of the Other",
    "arendt": "Hannah Arendt - Political Philosophy",
    "deleuze": "Gilles Deleuze - Difference and Repetition",
    "badiou": "Alain Badiou - Event Philosophy",
    "dewey": "John Dewey - Pragmatism",
    "peirce": "Charles Sanders Peirce - Semiotics",
    "jung": "Carl Jung - Analytical Psychology",
    "lacan": "Jacques Lacan - Psychoanalysis",
    "merleau_ponty": "Maurice Merleau-Ponty - Phenomenology",
    "watsuji": "Watsuji Tetsurō - Japanese Ethics",
    "wabi_sabi": "Wabi-Sabi - Japanese Aesthetics",
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

    def __init__(self) -> None:
        """Initialize interactive session."""
        self.console = Console()
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
        for i, (key, desc) in enumerate(phil_list, 1):
            table.add_row(str(i), key, desc)

        self.console.print(table)

        # Get selection
        self.console.print("\n[bold]Selection options:[/bold]")
        self.console.print(
            "  • Enter philosopher keys separated by commas (e.g., 'sartre,nietzsche,heidegger')"
        )
        self.console.print("  • Enter 'all' to use all philosophers")
        self.console.print(
            "  • Press Enter for default selection (sartre, nietzsche, heidegger)"
        )

        selection = Prompt.ask(
            "\n[cyan]Select philosophers[/cyan]", default="sartre,nietzsche,heidegger"
        )

        if selection.lower() == "all":
            self.selected_philosophers = list(AVAILABLE_PHILOSOPHERS.keys())
        else:
            selected = [s.strip().lower() for s in selection.split(",")]
            # Validate selection
            valid = [s for s in selected if s in AVAILABLE_PHILOSOPHERS]
            if not valid:
                self.console.print(
                    "[red]No valid philosophers selected. Exiting.[/red]"
                )
                return False
            self.selected_philosophers = valid

        # Confirm selection
        self.console.print(
            f"\n[green]✓ Selected {len(self.selected_philosophers)} philosophers:[/green]"
        )
        for phil in self.selected_philosophers:
            desc = AVAILABLE_PHILOSOPHERS[phil]
            self.console.print(f"  • {desc}")

        return True

    def _create_ensemble(self) -> None:
        """Create philosophical ensemble with selected philosophers."""
        self.console.print("\n[yellow]Creating ensemble...[/yellow]")

        # Create PoSelf pipeline with the exact selected allowlist
        self.po = PoSelf(philosophers=self.selected_philosophers, enable_trace=True)

        self.console.print(
            f"[green]✓ Ensemble created with {len(self.selected_philosophers)} philosophers[/green]"
        )

    def _reasoning_loop(self) -> None:
        """Interactive reasoning loop."""
        self.console.rule("[bold cyan]Step 2: Interactive Reasoning[/bold cyan]")

        while True:
            try:
                # Get prompt
                self.console.print()
                prompt = Prompt.ask(
                    "[bold cyan]Enter your philosophical question[/bold cyan] (or 'quit' to exit)"
                )

                if prompt.lower() in ["quit", "exit", "q"]:
                    break

                if not prompt.strip():
                    continue

                # Execute reasoning
                self.console.print("\n[yellow]🤔 Reasoning...[/yellow]")
                result = self.po.generate(prompt).to_dict()
                self.reasoning_history.append(result)

                # Display result
                self._display_result(result)
                self.console.print(
                    "\n[dim]Visualization views are intentionally disabled in "
                    "po-interactive because the current PoSelf response contract "
                    "does not expose the structured tensor payloads required by "
                    "the legacy visualizers.[/dim]"
                )

                # Ask to continue
                if not Confirm.ask(
                    "\n[cyan]Continue with another question?[/cyan]", default=True
                ):
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

        self.console.print("\n[bold magenta]Text:[/bold magenta]")
        self.console.print(result.get("text", ""))

        leader = result.get("consensus_leader") or "unknown"
        self.console.print(f"\n[bold cyan]Consensus leader:[/bold cyan] {leader}")

        philosophers = result.get("philosophers", [])
        if philosophers:
            self.console.print("\n[bold]Selected philosophers:[/bold]")
            for name in philosophers:
                self.console.print(f"  • {name}")

        metrics = result.get("metrics", {})
        if metrics:
            self.console.print("\n[bold yellow]Metrics:[/bold yellow]")
            for key, value in metrics.items():
                self.console.print(f"  • {key}: {value}")

        responses = result.get("responses", [])
        if responses:
            self.console.print("\n[bold green]Per-philosopher responses:[/bold green]")
            for item in responses:
                name = item.get("name", "unknown")
                latency_ms = item.get("latency_ms", 0)
                proposals = item.get("proposals", 0)
                self.console.print(
                    f"  • {name}: proposals={proposals}, latency_ms={latency_ms}"
                )

        metadata = result.get("metadata", {})
        status = metadata.get("status", "unknown")
        degraded = metadata.get("degraded", False)
        self.console.print(f"\n[bold]Status:[/bold] {status} (degraded={degraded})")

        events = result.get("log", {}).get("events", [])
        self.console.print(f"[bold]Trace events:[/bold] {len(events)}")

    def _show_visualizations(self, result: Dict[str, Any]) -> None:
        """Visualization entrypoint retained only for backward-compatible internals."""
        self.console.print(
            "[yellow]Visualization rendering is not supported by the current "
            "PoSelfResponse contract in po-interactive.[/yellow]"
        )

    def _session_summary(self) -> None:
        """Display session summary and offer export."""
        self.console.rule("[bold cyan]Session Summary[/bold cyan]")

        self.console.print(
            f"\n[bold]Reasoning Sessions:[/bold] {len(self.reasoning_history)}"
        )
        self.console.print(
            f"[bold]Philosophers:[/bold] {len(self.selected_philosophers)}"
        )

        if self.reasoning_history:
            # Offer trace export
            if Confirm.ask("\n[cyan]Export reasoning traces?[/cyan]", default=False):
                self._export_traces()

        self.console.print(
            "\n[bold green]Thank you for using Po_core Interactive Reasoning![/bold green]"
        )

    def _export_traces(self) -> None:
        """Export reasoning traces to JSON file."""
        filename = Prompt.ask(
            "[cyan]Enter filename[/cyan]", default="po_core_reasoning_trace.json"
        )

        try:
            export_data = {
                "session": {
                    "philosophers": self.selected_philosophers,
                    "total_reasonings": len(self.reasoning_history),
                },
                "reasoning_history": self.reasoning_history,
            }

            with open(filename, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            self.console.print(f"[green]✓ Traces exported to {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting traces: {e}[/red]")


def main() -> None:
    """Main entry point for interactive CLI."""
    if any(arg in {"-h", "--help"} for arg in sys.argv[1:]):
        print(
            "Usage: po-interactive\n"
            "\n"
            "Interactive Po_core session with philosopher selection, prompt loop,\n"
            "textual PoSelf summaries, and trace export. Rich tensor\n"
            "visualizations are currently disabled in this CLI.\n"
            "\n"
            "Options:\n"
            "  -h, --help  Show this help message and exit."
        )
        return

    session = InteractiveReasoningSession()
    try:
        session.run()
    except KeyboardInterrupt:
        session.console.print("\n\n[yellow]Session terminated by user[/yellow]")
    except Exception as e:
        session.console.print(f"\n\n[red]Unexpected error: {e}[/red]")


if __name__ == "__main__":
    main()
