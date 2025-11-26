#!/usr/bin/env python3
"""
Interactive Po_viewer - Interactive Session Browser

Interactive tool for browsing and visualizing philosophical reasoning sessions.
Provides a menu-driven interface for exploring Po_trace sessions.
"""
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

from po_core.po_viewer import PoViewer
from po_core.po_self import PoSelf

console = Console()


class InteractiveViewer:
    """Interactive session browser."""

    def __init__(self):
        """Initialize interactive viewer."""
        self.viewer = PoViewer()
        self.current_session_id: Optional[str] = None
        self.running = True

    def show_header(self):
        """Show application header."""
        console.clear()
        console.print(
            Panel.fit(
                "[bold magenta]Po_viewer Interactive Browser[/bold magenta]\n"
                "[cyan]Explore Philosophical Reasoning Sessions[/cyan]",
                border_style="magenta",
            )
        )
        console.print()

    def show_main_menu(self):
        """Show main menu."""
        menu = Table(
            show_header=False,
            box=box.SIMPLE,
            border_style="cyan",
        )
        menu.add_column("Option", style="cyan bold")
        menu.add_column("Description", style="white")

        menu.add_row("1", "📋 List recent sessions")
        menu.add_row("2", "🔍 View session details")
        menu.add_row("3", "📊 Show session metrics")
        menu.add_row("4", "🔄 Show event flow")
        menu.add_row("5", "👥 Show philosopher interactions")
        menu.add_row("6", "⚖️  Compare two sessions")
        menu.add_row("7", "📊 Show analytics dashboard")
        menu.add_row("8", "🆕 Create new session")
        menu.add_row("9", "📄 Export session JSON")
        menu.add_row("0", "❌ Exit")

        console.print(menu)
        console.print()

    def list_sessions(self):
        """List recent sessions."""
        limit = Prompt.ask(
            "[cyan]How many sessions to show?[/cyan]",
            default="10",
        )

        try:
            limit = int(limit)
        except ValueError:
            console.print("[red]Invalid number. Using 10.[/red]")
            limit = 10

        table = self.viewer.render_sessions_table(limit=limit)
        console.print(table)
        console.print()

        if Confirm.ask("Select a session to view?", default=False):
            session_id = Prompt.ask("[cyan]Enter session ID (first 8 chars are enough)[/cyan]")
            self.current_session_id = self._find_session_id(session_id)
            if self.current_session_id:
                self.view_session_details()

    def view_session_details(self):
        """View session details."""
        session_id = self._get_session_id()
        if not session_id:
            return

        console.print(self.viewer.render_session_detail(session_id))
        console.print()

        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def show_metrics(self):
        """Show session metrics."""
        session_id = self._get_session_id()
        if not session_id:
            return

        console.print(self.viewer.render_metrics_bars(session_id))
        console.print()

        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def show_event_flow(self):
        """Show event flow."""
        session_id = self._get_session_id()
        if not session_id:
            return

        console.print(self.viewer.render_event_flow(session_id))
        console.print()

        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def show_interactions(self):
        """Show philosopher interactions."""
        session_id = self._get_session_id()
        if not session_id:
            return

        console.print(self.viewer.render_philosopher_interaction(session_id))
        console.print()

        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def compare_sessions(self):
        """Compare two sessions."""
        console.print("[yellow]Comparing two sessions[/yellow]")
        console.print()

        session_id1 = Prompt.ask("[cyan]Enter first session ID[/cyan]")
        session_id1 = self._find_session_id(session_id1)
        if not session_id1:
            console.print("[red]First session not found[/red]")
            return

        session_id2 = Prompt.ask("[cyan]Enter second session ID[/cyan]")
        session_id2 = self._find_session_id(session_id2)
        if not session_id2:
            console.print("[red]Second session not found[/red]")
            return

        console.print(self.viewer.compare_sessions(session_id1, session_id2))
        console.print()

        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def show_dashboard(self):
        """Show analytics dashboard."""
        limit = Prompt.ask(
            "[cyan]How many sessions to analyze?[/cyan]",
            default="20",
        )

        try:
            limit = int(limit)
        except ValueError:
            console.print("[red]Invalid number. Using 20.[/red]")
            limit = 20

        console.print(self.viewer.render_dashboard(limit=limit))
        console.print()

        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def create_new_session(self):
        """Create a new philosophical reasoning session."""
        console.print("[yellow]Creating a new philosophical reasoning session[/yellow]")
        console.print()

        prompt = Prompt.ask("[cyan]Enter your philosophical question[/cyan]")
        if not prompt.strip():
            console.print("[red]Prompt cannot be empty[/red]")
            return

        use_custom = Confirm.ask(
            "Do you want to select specific philosophers?",
            default=False,
        )

        philosophers = None
        if use_custom:
            console.print(
                "[dim]Available: aristotle, nietzsche, sartre, heidegger, "
                "confucius, wabi_sabi, wittgenstein, etc.[/dim]"
            )
            phil_input = Prompt.ask(
                "[cyan]Enter philosopher names (comma-separated)[/cyan]"
            )
            philosophers = [p.strip() for p in phil_input.split(",") if p.strip()]

        # Create session
        console.print("\n[yellow]Generating philosophical reasoning...[/yellow]")
        try:
            po = PoSelf(philosophers=philosophers, enable_trace=True)
            response = po.generate(prompt)

            self.current_session_id = response.log["session_id"]
            self.viewer = PoViewer(po_trace=po.po_trace)

            console.print("[green]✓ Session created successfully![/green]")
            console.print(f"[cyan]Session ID: {self.current_session_id}[/cyan]")
            console.print()

            # Show summary
            console.print(f"[bold]Consensus Leader:[/bold] {response.consensus_leader}")
            console.print(f"[bold]Philosophers:[/bold] {', '.join(response.philosophers)}")
            console.print()
            console.print(f"[bold]Response:[/bold]")
            console.print(Panel(response.text, border_style="green"))
            console.print()

            if Confirm.ask("View full visualization?", default=True):
                console.print(self.viewer.render_metrics_bars(self.current_session_id))
                console.print()
                console.print(
                    self.viewer.render_philosopher_interaction(self.current_session_id)
                )
                console.print()

        except Exception as e:
            console.print(f"[red]Error creating session: {e}[/red]")

        console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def export_session_json(self):
        """Export session as JSON."""
        session_id = self._get_session_id()
        if not session_id:
            return

        console.print(self.viewer.render_session_json(session_id))
        console.print()

        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def _get_session_id(self) -> Optional[str]:
        """Get session ID (use current or ask user)."""
        if self.current_session_id:
            use_current = Confirm.ask(
                f"Use current session ({self.current_session_id[:8]}...)?",
                default=True,
            )
            if use_current:
                return self.current_session_id

        session_id = Prompt.ask("[cyan]Enter session ID[/cyan]")
        return self._find_session_id(session_id)

    def _find_session_id(self, partial_id: str) -> Optional[str]:
        """Find full session ID from partial ID."""
        sessions = self.viewer.po_trace.list_sessions(limit=100)
        for session in sessions:
            if session["session_id"].startswith(partial_id):
                return session["session_id"]

        console.print(f"[red]Session {partial_id} not found[/red]")
        return None

    def run(self):
        """Run interactive viewer."""
        try:
            while self.running:
                self.show_header()

                if self.current_session_id:
                    console.print(
                        f"[dim]Current session: {self.current_session_id[:16]}...[/dim]"
                    )
                    console.print()

                self.show_main_menu()

                choice = Prompt.ask(
                    "[bold cyan]Select an option[/bold cyan]",
                    choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                )

                console.clear()

                if choice == "0":
                    console.print(
                        "[yellow]Thank you for using Po_viewer![/yellow]"
                    )
                    self.running = False
                elif choice == "1":
                    self.list_sessions()
                elif choice == "2":
                    self.view_session_details()
                elif choice == "3":
                    self.show_metrics()
                elif choice == "4":
                    self.show_event_flow()
                elif choice == "5":
                    self.show_interactions()
                elif choice == "6":
                    self.compare_sessions()
                elif choice == "7":
                    self.show_dashboard()
                elif choice == "8":
                    self.create_new_session()
                elif choice == "9":
                    self.export_session_json()

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")


def main():
    """Main entry point."""
    viewer = InteractiveViewer()
    viewer.run()


if __name__ == "__main__":
    main()
