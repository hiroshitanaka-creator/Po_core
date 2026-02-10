"""
Simple Test: 20 Philosophers Configuration
===========================================

Demonstrates the full-scale 20-philosopher configuration
without requiring full installation.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree

console = Console()


# All 20 available philosophers from PHILOSOPHER_REGISTRY
ALL_PHILOSOPHERS = [
    "Arendt",
    "Aristotle",
    "Badiou",
    "Confucius",
    "Deleuze",
    "Derrida",
    "Dewey",
    "Heidegger",
    "Jung",
    "Kierkegaard",
    "Lacan",
    "Levinas",
    "Merleau-Ponty",
    "Nietzsche",
    "Peirce",
    "Sartre",
    "Wabi-Sabi",
    "Watsuji",
    "Wittgenstein",
    "Zhuangzi",
]


class AgentConfiguration:
    """Represents an agent configuration."""

    def __init__(self, agent_id, role, philosophers, tradition):
        self.agent_id = agent_id
        self.role = role
        self.philosophers = philosophers
        self.tradition = tradition


def create_full_scale_configuration():
    """
    Create the full-scale 20-philosopher configuration.

    Returns:
        List of 5 agents, each with 4 philosophers
    """
    agents = [
        AgentConfiguration(
            agent_id="classical-analyst",
            role="Analyst",
            philosophers=["Aristotle", "Wittgenstein", "Peirce", "Dewey"],
            tradition="Classical & Analytic Philosophy",
        ),
        AgentConfiguration(
            agent_id="continental-explorer",
            role="Explorer",
            philosophers=["Nietzsche", "Kierkegaard", "Sartre", "Heidegger"],
            tradition="Continental & Existential",
        ),
        AgentConfiguration(
            agent_id="postmodern-critic",
            role="Critic",
            philosophers=["Derrida", "Deleuze", "Badiou", "Levinas"],
            tradition="Postmodern & Critical Theory",
        ),
        AgentConfiguration(
            agent_id="phenomenology-synthesizer",
            role="Synthesizer",
            philosophers=["Merleau-Ponty", "Jung", "Lacan", "Arendt"],
            tradition="Phenomenology & Psychology",
        ),
        AgentConfiguration(
            agent_id="eastern-coordinator",
            role="Coordinator",
            philosophers=["Confucius", "Zhuangzi", "Watsuji", "Wabi-Sabi"],
            tradition="Eastern Philosophy",
        ),
    ]

    return agents


def display_configuration():
    """Display the full-scale configuration."""
    console.print("\n" + "=" * 80)
    console.print(
        "[bold cyan]🎈 Po_core: Full-Scale 20-Philosopher Configuration 🐷[/bold cyan]"
    )
    console.print("=" * 80 + "\n")

    agents = create_full_scale_configuration()

    # Create summary table
    table = Table(
        title="[bold magenta]Agent Configuration Matrix[/bold magenta]",
        show_header=True,
        header_style="bold cyan",
        show_lines=True,
    )

    table.add_column("Agent ID", style="cyan", no_wrap=True, width=25)
    table.add_column("Role", style="yellow", width=12)
    table.add_column("Philosophers (4)", style="white", width=35)
    table.add_column("Tradition", style="green", width=30)

    for agent in agents:
        philosophers_str = "\n".join(agent.philosophers)
        table.add_row(agent.agent_id, agent.role, philosophers_str, agent.tradition)

    console.print(table)

    # Statistics
    total_philosophers = sum(len(agent.philosophers) for agent in agents)
    console.print(
        f"\n[bold green]✓ Total Philosophers:[/bold green] {total_philosophers}"
    )
    console.print(f"[bold green]✓ Total Agents:[/bold green] {len(agents)}")
    console.print(
        f"[bold green]✓ Average per Agent:[/bold green] {total_philosophers / len(agents):.1f}\n"
    )

    # Verify all philosophers are covered
    used_philosophers = []
    for agent in agents:
        used_philosophers.extend(agent.philosophers)

    console.print(f"[bold]Philosophers Used:[/bold] {sorted(used_philosophers)}\n")

    return agents


def display_reasoning_scenarios(agents):
    """Display example reasoning scenarios."""
    console.print("=" * 80)
    console.print("[bold magenta]Reasoning Scenarios[/bold magenta]")
    console.print("=" * 80 + "\n")

    scenarios = [
        {
            "name": "Parallel Reasoning",
            "description": "All 5 agents reason simultaneously on the same question",
            "active_agents": 5,
            "active_philosophers": 20,
            "example": "What is the relationship between technology and human freedom?",
        },
        {
            "name": "Hierarchical Reasoning",
            "description": "Sequential reasoning through multiple phases",
            "active_agents": 5,
            "active_philosophers": 20,
            "example": "Phase 1: Analysts analyze\nPhase 2: Critics evaluate\nPhase 3: Synthesizers integrate",
        },
        {
            "name": "Distributed Reasoning",
            "description": "Complex problem decomposed across agents",
            "active_agents": 5,
            "active_philosophers": 20,
            "example": "Ethical framework for space expansion\n→ Each agent handles one dimension",
        },
        {
            "name": "Focused Reasoning",
            "description": "Single agent with 4 philosophers",
            "active_agents": 1,
            "active_philosophers": 4,
            "example": "Quick analysis requiring specific expertise",
        },
    ]

    for scenario in scenarios:
        tree = Tree(f"[bold cyan]{scenario['name']}[/bold cyan]")
        tree.add(f"[yellow]Description:[/yellow] {scenario['description']}")
        tree.add(f"[green]Active Agents:[/green] {scenario['active_agents']}")
        tree.add(
            f"[green]Active Philosophers:[/green] {scenario['active_philosophers']}"
        )
        tree.add(f"[white]Example:[/white]\n{scenario['example']}")
        console.print(tree)
        console.print()


def display_philosopher_details():
    """Display detailed information about each philosopher."""
    console.print("=" * 80)
    console.print("[bold magenta]Philosopher Details (All 20)[/bold magenta]")
    console.print("=" * 80 + "\n")

    agents = create_full_scale_configuration()

    for agent in agents:
        panel_content = f"[bold cyan]Role:[/bold cyan] {agent.role}\n"
        panel_content += f"[bold yellow]Tradition:[/bold yellow] {agent.tradition}\n\n"
        panel_content += "[bold green]Philosophers:[/bold green]\n"

        for i, phil in enumerate(agent.philosophers, 1):
            panel_content += f"  {i}. {phil}\n"

        console.print(
            Panel(
                panel_content,
                title=f"[bold]{agent.agent_id}[/bold]",
                border_style="cyan",
            )
        )
        console.print()


def display_performance_metrics():
    """Display expected performance characteristics."""
    console.print("=" * 80)
    console.print("[bold magenta]Performance Characteristics[/bold magenta]")
    console.print("=" * 80 + "\n")

    metrics_table = Table(show_header=True, header_style="bold cyan")
    metrics_table.add_column("Scenario", style="cyan", width=25)
    metrics_table.add_column("Agents", justify="right", style="yellow", width=8)
    metrics_table.add_column("Philosophers", justify="right", style="green", width=15)
    metrics_table.add_column("Execution", style="white", width=20)
    metrics_table.add_column("Use Case", style="magenta", width=25)

    metrics_table.add_row(
        "Parallel (All)", "5", "20", "Concurrent", "Multi-perspective analysis"
    )
    metrics_table.add_row(
        "Hierarchical", "5", "20", "Sequential (3 phases)", "Deep deliberation"
    )
    metrics_table.add_row(
        "Distributed", "3-5", "12-20", "Subtask allocation", "Complex problem solving"
    )
    metrics_table.add_row(
        "Focused", "1", "4", "Single-thread", "Quick specialized query"
    )

    console.print(metrics_table)
    console.print()


def main():
    """Main function to display all information."""
    # Display configuration
    agents = display_configuration()

    # Display reasoning scenarios
    display_reasoning_scenarios(agents)

    # Display philosopher details
    display_philosopher_details()

    # Display performance metrics
    display_performance_metrics()

    # Final summary
    console.print("=" * 80)
    console.print(
        "[bold green]✅ Full-Scale 20-Philosopher Configuration Complete![/bold green]"
    )
    console.print("=" * 80 + "\n")

    console.print(
        Panel(
            """
[bold cyan]This configuration enables:[/bold cyan]

• [green]Multi-perspective reasoning[/green] across 5 philosophical traditions
• [green]Parallel processing[/green] with all 20 philosophers simultaneously
• [green]Hierarchical deliberation[/green] through analysis, critique, and synthesis
• [green]Distributed problem-solving[/green] for complex, multifaceted questions
• [green]Cultural diversity[/green] with Western and Eastern philosophical wisdom

[bold yellow]Ready for enterprise deployment! 🚀[/bold yellow]
        """,
            title="[bold magenta]Po_core: When Pigs Fly 🐷🎈[/bold magenta]",
            border_style="magenta",
        )
    )


if __name__ == "__main__":
    main()
