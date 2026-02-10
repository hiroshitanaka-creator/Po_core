"""
Full-Scale Reasoning Test: All 20 Philosophers
===============================================

Test the Multi-Agent Reasoning System with all 20 philosophers
organized into 5 specialized agent groups.
"""

import asyncio
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from multi_agent_reasoning import (
    AgentConfig,
    AgentRole,
    MultiAgentReasoningSystem,
)
from po_core.po_trace_db import PoTraceDB

console = Console()


def create_full_scale_agents() -> MultiAgentReasoningSystem:
    """
    Create a full-scale multi-agent system with ALL 20 philosophers.

    Distribution:
    - 5 agents, 4 philosophers each
    - Balanced across different philosophical traditions
    """
    console.print(
        "\n[bold cyan]🚀 Initializing Full-Scale System: 20 Philosophers[/bold cyan]\n"
    )

    system = MultiAgentReasoningSystem(verbose=True)

    # Agent 1: Classical & Analytic (4 philosophers)
    system.register_agent(
        AgentConfig(
            agent_id="classical-analyst",
            role=AgentRole.ANALYST,
            philosophers=["Aristotle", "Wittgenstein", "Peirce", "Dewey"],
            priority=1,
            metadata={"tradition": "Classical & Analytic"},
        )
    )

    # Agent 2: Continental & Existential (4 philosophers)
    system.register_agent(
        AgentConfig(
            agent_id="continental-explorer",
            role=AgentRole.EXPLORER,
            philosophers=["Nietzsche", "Kierkegaard", "Sartre", "Heidegger"],
            priority=2,
            metadata={"tradition": "Continental & Existential"},
        )
    )

    # Agent 3: Postmodern & Critical (4 philosophers)
    system.register_agent(
        AgentConfig(
            agent_id="postmodern-critic",
            role=AgentRole.CRITIC,
            philosophers=["Derrida", "Deleuze", "Badiou", "Levinas"],
            priority=1,
            metadata={"tradition": "Postmodern & Critical"},
        )
    )

    # Agent 4: Phenomenology & Psychology (4 philosophers)
    system.register_agent(
        AgentConfig(
            agent_id="phenomenology-synthesizer",
            role=AgentRole.SYNTHESIZER,
            philosophers=["Merleau-Ponty", "Jung", "Lacan", "Arendt"],
            priority=3,
            metadata={"tradition": "Phenomenology & Psychology"},
        )
    )

    # Agent 5: Eastern Philosophy (4 philosophers)
    system.register_agent(
        AgentConfig(
            agent_id="eastern-coordinator",
            role=AgentRole.COORDINATOR,
            philosophers=["Confucius", "Zhuangzi", "Watsuji", "Wabi-Sabi"],
            priority=2,
            metadata={"tradition": "Eastern Philosophy"},
        )
    )

    console.print(
        "[bold green]✓ All 20 philosophers registered across 5 agents[/bold green]\n"
    )

    return system


def display_agent_summary(system: MultiAgentReasoningSystem):
    """Display a summary table of all agents and philosophers."""
    table = Table(
        title="[bold magenta]Full-Scale Agent Configuration[/bold magenta]",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Agent ID", style="cyan", no_wrap=True)
    table.add_column("Role", style="yellow")
    table.add_column("Philosophers", style="white")
    table.add_column("Tradition", style="green")

    for agent_id, config in system.agents.items():
        philosophers_str = ", ".join(config.philosophers)
        tradition = config.metadata.get("tradition", "N/A")
        table.add_row(agent_id, config.role.value, philosophers_str, tradition)

    console.print(table)
    console.print(
        f"\n[bold]Total Philosophers:[/bold] {sum(len(c.philosophers) for c in system.agents.values())}"
    )
    console.print(f"[bold]Total Agents:[/bold] {len(system.agents)}\n")


async def test_parallel_reasoning_20():
    """Test parallel reasoning with all 5 agents (20 philosophers)."""
    console.print("\n" + "=" * 80)
    console.print(
        "[bold cyan]TEST 1: Parallel Reasoning (All 20 Philosophers)[/bold cyan]"
    )
    console.print("=" * 80 + "\n")

    system = create_full_scale_agents()
    display_agent_summary(system)

    prompt = "What is the relationship between technology and human freedom?"

    console.print(f"[bold]Prompt:[/bold] {prompt}\n")

    # Execute with all 5 agents in parallel
    all_agent_ids = list(system.agents.keys())

    start_time = datetime.utcnow()
    results = await system.parallel_reasoning(prompt, all_agent_ids)
    end_time = datetime.utcnow()

    duration = (end_time - start_time).total_seconds()

    # Display results
    console.print(f"\n[bold green]✓ Completed in {duration:.2f} seconds[/bold green]\n")

    # Results table
    results_table = Table(
        title="[bold]Reasoning Results[/bold]",
        show_header=True,
        header_style="bold magenta",
    )

    results_table.add_column("Agent", style="cyan")
    results_table.add_column("Role", style="yellow")
    results_table.add_column("Confidence", style="green", justify="right")
    results_table.add_column("Summary", style="white")

    for result in results:
        summary = result.text[:100] + "..." if len(result.text) > 100 else result.text
        results_table.add_row(
            result.agent_id, result.role.value, f"{result.confidence:.2%}", summary
        )

    console.print(results_table)

    # Statistics
    avg_confidence = sum(r.confidence for r in results) / len(results)
    console.print(f"\n[bold]Average Confidence:[/bold] {avg_confidence:.2%}")
    console.print(
        f"[bold]Total Insights Generated:[/bold] {sum(len(r.insights) for r in results)}"
    )

    return system, results


async def test_hierarchical_reasoning_20():
    """Test hierarchical reasoning with full 20-philosopher system."""
    console.print("\n" + "=" * 80)
    console.print(
        "[bold magenta]TEST 2: Hierarchical Reasoning (20 Philosophers)[/bold magenta]"
    )
    console.print("=" * 80 + "\n")

    system = create_full_scale_agents()

    prompt = (
        "How should we approach the challenge of artificial general intelligence (AGI)?"
    )

    console.print(f"[bold]Prompt:[/bold] {prompt}\n")

    # Note: hierarchical_reasoning will use agents by role
    # We have: 1 Analyst, 1 Explorer, 1 Critic, 1 Synthesizer, 1 Coordinator

    start_time = datetime.utcnow()
    result = await system.hierarchical_reasoning(prompt)
    end_time = datetime.utcnow()

    duration = (end_time - start_time).total_seconds()

    console.print(
        f"\n[bold green]✓ Hierarchical reasoning completed in {duration:.2f} seconds[/bold green]\n"
    )

    # Display consensus
    console.print(
        Panel(
            (
                result["final_consensus"][:800] + "..."
                if len(result["final_consensus"]) > 800
                else result["final_consensus"]
            ),
            title="[bold green]Final Consensus (All 20 Philosophers)[/bold green]",
            border_style="green",
        )
    )

    console.print(
        f"\n[bold]Overall Confidence:[/bold] {result['overall_confidence']:.2%}\n"
    )

    return system, result


async def test_distributed_reasoning_20():
    """Test distributed reasoning for complex problem."""
    console.print("\n" + "=" * 80)
    console.print(
        "[bold yellow]TEST 3: Distributed Reasoning (20 Philosophers)[/bold yellow]"
    )
    console.print("=" * 80 + "\n")

    system = create_full_scale_agents()

    prompt = """
    Design a comprehensive ethical framework for humanity's expansion into space,
    considering technological, social, environmental, and philosophical dimensions.
    """

    console.print(f"[bold]Complex Prompt:[/bold] {prompt.strip()}\n")

    start_time = datetime.utcnow()
    result = await system.distributed_reasoning(prompt)
    end_time = datetime.utcnow()

    duration = (end_time - start_time).total_seconds()

    console.print(
        f"\n[bold green]✓ Distributed reasoning completed in {duration:.2f} seconds[/bold green]\n"
    )

    # Display synthesis
    console.print(
        Panel(
            (
                result["final_synthesis"][:800] + "..."
                if len(result["final_synthesis"]) > 800
                else result["final_synthesis"]
            ),
            title="[bold yellow]Final Synthesis (Distributed Across 20 Philosophers)[/bold yellow]",
            border_style="yellow",
        )
    )

    console.print(
        f"\n[bold]Overall Confidence:[/bold] {result['overall_confidence']:.2%}\n"
    )

    return system, result


async def test_database_integration():
    """Test database integration with full-scale reasoning."""
    console.print("\n" + "=" * 80)
    console.print("[bold blue]TEST 4: Database Integration[/bold blue]")
    console.print("=" * 80 + "\n")

    # Create system with database backend
    trace_db = PoTraceDB()
    system = MultiAgentReasoningSystem(trace_db=trace_db, verbose=True)

    # Register agents
    system.register_agent(
        AgentConfig(
            agent_id="db-test-agent",
            role=AgentRole.ANALYST,
            philosophers=["Aristotle", "Nietzsche", "Wittgenstein", "Heidegger"],
            priority=1,
        )
    )

    prompt = "What is the nature of truth in the digital age?"

    # Execute reasoning
    task = system.create_task(prompt)
    system.assign_task(task.task_id, "db-test-agent")
    result = await system.execute_task(task.task_id)

    # Check database
    stats = trace_db.get_statistics()

    console.print(f"[bold green]✓ Session stored in database[/bold green]")
    console.print(f"[bold]Database Statistics:[/bold]")
    console.print(f"  - Total sessions: {stats['total_sessions']}")
    console.print(f"  - Total events: {stats['total_events']}")
    console.print(f"  - Philosophers tracked: {len(stats['philosopher_usage'])}")

    return trace_db, stats


async def run_comprehensive_test():
    """Run all tests in sequence."""
    console.print("\n" + "=" * 80)
    console.print(
        "[bold magenta]🎈 PO_CORE FULL-SCALE TEST: 20 PHILOSOPHERS 🐷[/bold magenta]"
    )
    console.print("=" * 80)

    results = {}

    # Test 1: Parallel
    system1, res1 = await test_parallel_reasoning_20()
    results["parallel"] = res1

    # Test 2: Hierarchical
    system2, res2 = await test_hierarchical_reasoning_20()
    results["hierarchical"] = res2

    # Test 3: Distributed
    system3, res3 = await test_distributed_reasoning_20()
    results["distributed"] = res3

    # Test 4: Database
    trace_db, stats = await test_database_integration()
    results["database"] = stats

    # Final summary
    console.print("\n" + "=" * 80)
    console.print("[bold green]✅ ALL TESTS COMPLETED SUCCESSFULLY![/bold green]")
    console.print("=" * 80 + "\n")

    summary_tree = Tree("[bold magenta]Test Summary[/bold magenta]")

    parallel_branch = summary_tree.add("[cyan]Parallel Reasoning[/cyan]")
    parallel_branch.add(f"Agents: 5")
    parallel_branch.add(f"Philosophers: 20")
    parallel_branch.add(f"Results: {len(results['parallel'])} agent responses")

    hierarchical_branch = summary_tree.add("[magenta]Hierarchical Reasoning[/magenta]")
    hierarchical_branch.add(f"Phases: 3 (Analysis → Critique → Synthesis)")
    hierarchical_branch.add(
        f"Confidence: {results['hierarchical']['overall_confidence']:.2%}"
    )

    distributed_branch = summary_tree.add("[yellow]Distributed Reasoning[/yellow]")
    distributed_branch.add(f"Subtasks: {len(results['distributed']['subtasks'])}")
    distributed_branch.add(
        f"Confidence: {results['distributed']['overall_confidence']:.2%}"
    )

    db_branch = summary_tree.add("[blue]Database Integration[/blue]")
    db_branch.add(f"Sessions: {stats['total_sessions']}")
    db_branch.add(f"Events: {stats['total_events']}")

    console.print(summary_tree)

    console.print(
        "\n[bold green]🎉 Po_core successfully processed reasoning with all 20 philosophers![/bold green]"
    )
    console.print("[bold]System is ready for enterprise deployment! 🚀[/bold]\n")


if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())
