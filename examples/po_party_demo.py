"""
🎉 Po_Party: Interactive Philosopher Party Demo
===============================================

The most fun way to explore Po_core!

Select a theme and mood, and watch as Po_core automatically assembles
the perfect philosopher party based on cutting-edge research findings.

Based on research data:
- RQ1: Optimal combinations (4-philosopher groups, 100% emergence)
- RQ3: Best group sizes (8-14 philosophers, peak at 15)
- RQ4: Dialectical tension → +1975% emergence boost

Usage:
    python examples/po_party_demo.py

This example supports direct source-checkout execution by bootstrapping the
repository `src/` directory onto `sys.path`.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import random
from typing import Dict, List

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from po_core.party_machine import (
    PartyConfig,
    PartyMood,
    PhilosopherPartyMachine,
    PhilosophicalTheme,
)
from po_core.po_self import PoSelf

console = Console()


# ============================================================================
# Interactive UI
# ============================================================================


def show_welcome():
    """Display welcome screen."""
    console.clear()
    console.print()
    console.print(
        Panel(
            """
[bold magenta]🎉 Welcome to Po_Party! 🎉[/bold magenta]

[cyan]The Interactive Philosopher Party Machine[/cyan]

Pick a theme. Choose a mood. Watch philosophy come alive.

[yellow]How it works:[/yellow]
  1️⃣  You select a philosophical theme
  2️⃣  You choose the party atmosphere (mood)
  3️⃣  Po_core assembles the perfect philosopher lineup
  4️⃣  Watch them reason together in real-time
  5️⃣  See emergence, tension, and insights visualized

[bold green]Research-powered:[/bold green]
  ✓ Optimal combinations from 10,600 session analysis
  ✓ +1975% emergence boost from dialectical tension
  ✓ Perfect group sizes (8-14, peak at 15)

[dim]Let's make philosophy fun again! 🐷🎈[/dim]
        """,
            title="Po_Party",
            border_style="magenta",
            padding=(1, 2),
        )
    )


def select_theme() -> str:
    """Interactive theme selection."""
    console.print("\n[bold cyan]📚 Step 1: Choose your theme[/bold cyan]\n")

    themes = {
        "1": ("Ethics & Morality", "ethics"),
        "2": ("Existence & Being", "existence"),
        "3": ("Knowledge & Truth", "knowledge"),
        "4": ("Politics & Society", "politics"),
        "5": ("Consciousness & Mind", "consciousness"),
        "6": ("Freedom & Choice", "freedom"),
        "7": ("Meaning & Purpose", "meaning"),
        "8": ("Justice & Fairness", "justice"),
        "9": ("AI & Technology", "technology"),
        "10": ("Death & Mortality", "death"),
        "11": ("Custom theme", "custom"),
    }

    for key, (name, _) in themes.items():
        console.print(f"  {key}. {name}")

    choice = Prompt.ask(
        "\n[yellow]Select theme[/yellow]", choices=list(themes.keys()), default="1"
    )

    if choice == "11":
        custom = Prompt.ask("[yellow]Enter your custom theme[/yellow]")
        return custom
    else:
        return themes[choice][1]


def select_mood() -> PartyMood:
    """Interactive mood selection."""
    console.print("\n[bold cyan]🎭 Step 2: Choose the atmosphere[/bold cyan]\n")

    moods = {
        "1": (PartyMood.CALM, "Calm", "Harmonious, gentle discussion"),
        "2": (PartyMood.BALANCED, "Balanced", "Mix of harmony and tension"),
        "3": (PartyMood.CHAOTIC, "Chaotic", "Maximum disagreement and creativity"),
        "4": (PartyMood.CRITICAL, "Critical", "Skeptical, questioning everything"),
    }

    for key, (_, name, desc) in moods.items():
        console.print(f"  {key}. [bold]{name}[/bold] - {desc}")

    choice = Prompt.ask(
        "\n[yellow]Select mood[/yellow]", choices=list(moods.keys()), default="2"
    )

    return moods[choice][0]


def display_party_config(config: PartyConfig):
    """Display the suggested party configuration."""
    console.print(
        "\n[bold magenta]🎊 Your Philosopher Party is Ready![/bold magenta]\n"
    )

    # Main info panel
    console.print(
        Panel(
            config.reasoning,
            title="Party Configuration",
            border_style="cyan",
        )
    )

    # Philosopher roster
    table = Table(
        title="🧠 Philosopher Roster", show_header=True, header_style="bold magenta"
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Philosopher", style="cyan")
    table.add_column("Tradition", style="green")

    traditions = {
        "aristotle": "Ancient Greek",
        "kant": "German Idealism",
        "mill": "British Empiricism",
        "confucius": "Chinese",
        "dewey": "American Pragmatism",
        "heidegger": "Phenomenology",
        "sartre": "Existentialism",
        "kierkegaard": "Existentialism",
        "merleau_ponty": "Phenomenology",
        "levinas": "Ethics/Phenomenology",
        "rawls": "Political Philosophy",
        "arendt": "Political Philosophy",
        "peirce": "Pragmatism",
        "wittgenstein": "Analytic Philosophy",
        "derrida": "Poststructuralism",
        "deleuze": "Poststructuralism",
        "badiou": "Continental",
        "jung": "Psychoanalysis",
        "watsuji": "Japanese Philosophy",
        "zhuangzi": "Daoism",
        "wabi_sabi": "Japanese Aesthetics",
        "lacan": "Psychoanalysis",
        "nietzsche": "German Philosophy",
    }

    for i, phil in enumerate(config.philosophers, 1):
        tradition = traditions.get(phil, "Unknown")
        table.add_row(str(i), phil.replace("_", " ").title(), tradition)

    console.print(table)

    # Metrics preview
    metrics_table = Table(show_header=False, box=None, padding=(0, 2))
    metrics_table.add_column("Metric", style="yellow")
    metrics_table.add_column("Value", style="cyan")

    metrics_table.add_row("⚡ Expected Tension", f"{config.expected_tension:.1%}")
    metrics_table.add_row("✨ Expected Emergence", f"{config.expected_emergence:.1%}")
    metrics_table.add_row("📊 Research Basis", "10,600 sessions analyzed")

    console.print("\n")
    console.print(Panel(metrics_table, title="Expected Metrics", border_style="green"))


def run_party_simulation(config: PartyConfig, prompt: str):
    """
    Run the party with Po_self and display results.

    Note: This is a simplified version. Full multi-agent implementation
    would use the Multi-Agent Reasoning System.
    """
    console.print("\n[bold green]🚀 Starting the Party...[/bold green]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Assembling philosophers...", total=100)

        # Simulate party setup
        for i in range(20):
            progress.update(task, advance=5)
            import time

            time.sleep(0.05)

        progress.update(task, description="[cyan]Running philosophical reasoning...")

        # Create Po_self instance with the party philosophers
        try:
            po = PoSelf(philosophers=config.philosophers)

            # Run generation
            result = po.generate(prompt)

            progress.update(task, completed=100)

        except Exception as e:
            console.print(f"[red]Error during party: {e}[/red]")
            return None

    # Display results
    display_party_results(result, config)

    return result


def display_party_results(result, config: PartyConfig):
    """Display party results with rich visualization."""
    console.print("\n" + "=" * 80)
    console.print("[bold magenta]🎉 Party Results![/bold magenta]")
    console.print("=" * 80 + "\n")

    # Consensus text
    console.print(
        Panel(
            result.text[:500] + "..." if len(result.text) > 500 else result.text,
            title="💬 Philosophical Consensus",
            border_style="cyan",
        )
    )

    # Metrics dashboard
    metrics_table = Table(
        title="📊 Party Metrics Dashboard",
        show_header=True,
        header_style="bold magenta",
        border_style="green",
    )
    metrics_table.add_column("Metric", style="yellow", width=25)
    metrics_table.add_column("Value", justify="right", style="cyan", width=15)
    metrics_table.add_column("Interpretation", style="dim")

    fp = result.metrics.get("freedom_pressure", 0.0)
    sd = result.metrics.get("semantic_delta", 0.0)
    bt = result.metrics.get("blocked_tensor", 0.0)
    we = result.metrics.get("w_ethics", 0.0)

    metrics_table.add_row(
        "⚡ Freedom Pressure (F_P)", f"{fp:.3f}", "Responsibility weight"
    )
    metrics_table.add_row(
        "🔄 Semantic Delta (Δs)", f"{sd:.3f}", "Meaning transformation"
    )
    metrics_table.add_row("🚫 Blocked Tensor (B)", f"{bt:.3f}", "Healthy disagreement")
    metrics_table.add_row("✅ W_ethics", f"{we:.3f}", "Ethical safety score")

    console.print("\n")
    console.print(metrics_table)

    # Emergence detection
    emergence_detected = sd > 0.5 or bt > 0.4
    if emergence_detected:
        console.print("\n[bold green]✨ EMERGENCE DETECTED! ✨[/bold green]")
        console.print(
            "[green]High semantic transformation and dialectical tension detected.[/green]"
        )
    else:
        console.print("\n[yellow]📊 Standard reasoning pattern (no emergence)[/yellow]")

    # Comparison with expected
    console.print("\n[bold]📈 Expected vs. Actual:[/bold]")
    comparison = Table(show_header=True, header_style="bold")
    comparison.add_column("Aspect", style="yellow")
    comparison.add_column("Expected", justify="center", style="dim")
    comparison.add_column("Actual", justify="center", style="cyan")
    comparison.add_column("Match", justify="center")

    tension_match = "✓" if abs(bt - config.expected_tension) < 0.3 else "~"
    emergence_match = (
        "✓" if emergence_detected == (config.expected_emergence > 0.5) else "~"
    )

    comparison.add_row(
        "Tension", f"{config.expected_tension:.1%}", f"{bt:.1%}", tension_match
    )
    comparison.add_row(
        "Emergence",
        f"{config.expected_emergence:.1%}",
        f"{'Yes' if emergence_detected else 'No'}",
        emergence_match,
    )

    console.print(comparison)

    # Consensus leader
    if result.consensus_leader:
        console.print(f"\n[bold]👑 Consensus Leader:[/bold] {result.consensus_leader}")


def main_interactive():
    """Main interactive flow."""
    if any(arg in {"-h", "--help"} for arg in sys.argv[1:]):
        print(
            "Usage: python examples/po_party_demo.py\n"
            "\n"
            "Interactive Po_Party demo based on current PoSelf API. "
            "Supports direct source-checkout execution."
        )
        return

    show_welcome()

    input("\n[dim]Press Enter to start...[/dim]")

    # Step 1: Select theme
    theme = select_theme()

    # Step 2: Select mood
    mood = select_mood()

    # Step 3: Generate party configuration
    console.print("\n[bold yellow]🔮 Consulting research database...[/bold yellow]")

    machine = PhilosopherPartyMachine(verbose=False)
    config = machine.suggest_party(theme=theme, mood=mood)

    display_party_config(config)

    # Step 4: Confirm and run
    if not Confirm.ask("\n[bold]Ready to start the party?[/bold]", default=True):
        console.print("\n[yellow]Party cancelled. Come back anytime! 👋[/yellow]")
        return

    # Get prompt from user
    console.print(
        "\n[bold cyan]💭 What question should the philosophers discuss?[/bold cyan]"
    )
    console.print(f"[dim]Theme: {config.theme}[/dim]\n")

    default_prompts = {
        "ethics": "Is there a universal foundation for ethics, or is morality relative to culture?",
        "existence": "What does it mean to exist authentically in the modern world?",
        "knowledge": "Can we ever achieve certain knowledge, or is all knowing perspectival?",
        "politics": "What is the relationship between individual freedom and social justice?",
        "consciousness": "Is consciousness a product of the brain, or something more fundamental?",
        "freedom": "Are humans truly free, or are our choices determined by forces beyond our control?",
        "meaning": "Where does meaning come from in a universe without inherent purpose?",
        "justice": "What is justice, and how do we balance competing claims of fairness?",
        "technology": "How should we approach the ethical challenges posed by AI and technology?",
        "death": "How should we understand death, and what does mortality teach us about life?",
    }

    default_prompt = default_prompts.get(theme, "What is the nature of reality?")

    user_prompt = Prompt.ask(
        "[yellow]Enter your question[/yellow]", default=default_prompt
    )

    # Step 5: Run the party!
    result = run_party_simulation(config, user_prompt)

    if result:
        # Ask if they want another party
        if Confirm.ask("\n[bold]🎉 Host another party?[/bold]", default=True):
            console.clear()
            main_interactive()
        else:
            console.print(
                "\n[bold green]Thanks for partying with Po_core! 🐷🎈[/bold green]"
            )
            console.print("[dim]Until next time...[/dim]\n")


# ============================================================================
# Quick Demos
# ============================================================================


def quick_demo():
    """Quick non-interactive demo."""
    console.print("[bold magenta]🎉 Po_Party Quick Demo[/bold magenta]\n")

    # Demo 1: Ethics party
    console.print("[bold]Demo 1: Ethics & Morality (Balanced)[/bold]\n")
    config = create_party("ethics", "balanced")
    display_party_config(config)

    console.print("\n" + "=" * 80 + "\n")

    # Demo 2: Chaos party
    console.print("[bold]Demo 2: Existence (Chaotic)[/bold]\n")
    config = create_party("existence", "chaotic")
    display_party_config(config)

    console.print("\n" + "=" * 80 + "\n")

    # Demo 3: Calm party
    console.print("[bold]Demo 3: Knowledge (Calm)[/bold]\n")
    config = create_party("knowledge", "calm")
    display_party_config(config)

    console.print("\n[bold green]✅ Quick demo complete![/bold green]")
    console.print("[dim]Try interactive mode: po-core party[/dim]\n")


def create_party(theme: str, mood: str):
    """Helper for quick demo."""
    from po_core.party_machine import create_party as factory_create

    return factory_create(theme, mood)


# ============================================================================
# Main
# ============================================================================


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_demo()
    else:
        try:
            main_interactive()
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Party interrupted. Goodbye! 👋[/yellow]\n")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            import traceback

            traceback.print_exc()
