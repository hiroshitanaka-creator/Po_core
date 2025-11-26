"""
Multi-Agent Reasoning System
==============================

Large-scale prototype: Advanced multi-agent philosophical reasoning
Features:
- Multiple philosopher groups (agents) reasoning in parallel
- Inter-agent communication and knowledge sharing
- Hierarchical reasoning: Group → Meta-Group → Final Consensus
- Conflict resolution and consensus building
- Complex problem decomposition
- Real-time coordination and orchestration
"""
from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

from po_core.po_self import PoSelf
from po_core.po_trace_db import PoTraceDB
from po_core.ensemble import PHILOSOPHER_REGISTRY

console = Console()


# ============================================================================
# Core Data Models
# ============================================================================


class AgentRole(str, Enum):
    """Roles for different agent types."""

    ANALYST = "analyst"  # Analyzes the problem
    EXPLORER = "explorer"  # Explores solution space
    CRITIC = "critic"  # Provides critical evaluation
    SYNTHESIZER = "synthesizer"  # Synthesizes insights
    COORDINATOR = "coordinator"  # Coordinates other agents


@dataclass
class AgentConfig:
    """Configuration for an agent."""

    agent_id: str
    role: AgentRole
    philosophers: List[str]
    priority: int = 1
    max_iterations: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningTask:
    """A reasoning task to be executed."""

    task_id: str
    prompt: str
    parent_task_id: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    assigned_agent: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Dict[str, Any]] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class AgentResult:
    """Result from an agent's reasoning."""

    agent_id: str
    role: AgentRole
    session_id: str
    text: str
    metrics: Dict[str, float]
    confidence: float
    insights: List[str]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================================
# Multi-Agent Reasoning System
# ============================================================================


class MultiAgentReasoningSystem:
    """
    Advanced multi-agent reasoning system.

    Coordinates multiple philosopher groups to solve complex problems
    through hierarchical reasoning and consensus building.
    """

    def __init__(self, trace_db: Optional[PoTraceDB] = None, verbose: bool = True):
        """
        Initialize multi-agent reasoning system.

        Args:
            trace_db: Database-backed trace system
            verbose: Show detailed progress
        """
        self.trace_db = trace_db or PoTraceDB()
        self.verbose = verbose
        self.agents: Dict[str, AgentConfig] = {}
        self.tasks: Dict[str, ReasoningTask] = {}
        self.results: Dict[str, AgentResult] = {}

    def register_agent(self, config: AgentConfig) -> None:
        """Register a new agent."""
        self.agents[config.agent_id] = config
        if self.verbose:
            console.print(
                f"[green]✓[/green] Registered agent: {config.agent_id} "
                f"({config.role.value}, {len(config.philosophers)} philosophers)"
            )

    def create_task(
        self, prompt: str, parent_task_id: Optional[str] = None
    ) -> ReasoningTask:
        """Create a new reasoning task."""
        task = ReasoningTask(
            task_id=str(uuid.uuid4()),
            prompt=prompt,
            parent_task_id=parent_task_id,
        )
        self.tasks[task.task_id] = task
        return task

    def assign_task(self, task_id: str, agent_id: str) -> None:
        """Assign a task to an agent."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")

        self.tasks[task_id].assigned_agent = agent_id
        self.tasks[task_id].status = "assigned"

    async def execute_task(self, task_id: str) -> AgentResult:
        """Execute a reasoning task with assigned agent."""
        task = self.tasks[task_id]
        if task.assigned_agent is None:
            raise ValueError(f"Task {task_id} has no assigned agent")

        agent_config = self.agents[task.assigned_agent]
        task.status = "in_progress"

        if self.verbose:
            console.print(
                f"[cyan]→[/cyan] Agent {agent_config.agent_id} "
                f"({agent_config.role.value}) executing task..."
            )

        # Create PoSelf instance with agent's philosophers
        po = PoSelf(
            philosophers=agent_config.philosophers,
            enable_trace=True,
            trace_backend=self.trace_db,
        )

        # Execute reasoning
        result = po.reason(task.prompt)

        # Create agent result
        agent_result = AgentResult(
            agent_id=agent_config.agent_id,
            role=agent_config.role,
            session_id=result.get("session_id", ""),
            text=result.get("text", ""),
            metrics=result.get("metrics", {}),
            confidence=self._calculate_confidence(result.get("metrics", {})),
            insights=self._extract_insights(result.get("text", "")),
        )

        task.status = "completed"
        task.result = {
            "text": agent_result.text,
            "metrics": agent_result.metrics,
            "confidence": agent_result.confidence,
        }

        self.results[agent_result.agent_id] = agent_result

        if self.verbose:
            console.print(
                f"[green]✓[/green] Agent {agent_config.agent_id} completed "
                f"(confidence: {agent_result.confidence:.2f})"
            )

        return agent_result

    async def parallel_reasoning(
        self, prompt: str, agent_ids: List[str]
    ) -> List[AgentResult]:
        """Execute reasoning with multiple agents in parallel."""
        if self.verbose:
            console.print(
                f"\n[bold cyan]🚀 Parallel Reasoning:[/bold cyan] "
                f"{len(agent_ids)} agents working simultaneously..."
            )

        # Create tasks for each agent
        tasks = []
        task_ids = []
        for agent_id in agent_ids:
            task = self.create_task(prompt)
            self.assign_task(task.task_id, agent_id)
            tasks.append(self.execute_task(task.task_id))
            task_ids.append(task.task_id)

        # Execute in parallel
        results = await asyncio.gather(*tasks)

        return results

    async def hierarchical_reasoning(self, prompt: str) -> Dict[str, Any]:
        """
        Execute hierarchical reasoning:
        1. Multiple specialized agents analyze the problem
        2. Meta-agent synthesizes insights
        3. Final consensus is reached
        """
        if self.verbose:
            console.print("\n[bold magenta]🏗️  Hierarchical Reasoning[/bold magenta]\n")

        # Phase 1: Specialized Analysis
        console.print("[bold]Phase 1:[/bold] Specialized Analysis")
        analyst_agents = [
            aid for aid, cfg in self.agents.items() if cfg.role == AgentRole.ANALYST
        ]
        phase1_results = await self.parallel_reasoning(prompt, analyst_agents[:3])

        # Phase 2: Critical Evaluation
        console.print("\n[bold]Phase 2:[/bold] Critical Evaluation")
        critic_agents = [
            aid for aid, cfg in self.agents.items() if cfg.role == AgentRole.CRITIC
        ]
        critique_prompt = (
            f"Original question: {prompt}\n\n"
            f"Analyses received:\n"
            + "\n\n".join(
                [
                    f"- {r.role.value}: {r.text[:200]}..."
                    for r in phase1_results
                ]
            )
            + "\n\nProvide critical evaluation."
        )
        phase2_results = await self.parallel_reasoning(critique_prompt, critic_agents[:2])

        # Phase 3: Synthesis
        console.print("\n[bold]Phase 3:[/bold] Synthesis & Consensus")
        synthesizer_agents = [
            aid for aid, cfg in self.agents.items() if cfg.role == AgentRole.SYNTHESIZER
        ]
        synthesis_prompt = (
            f"Original question: {prompt}\n\n"
            f"Synthesize the following perspectives:\n\n"
            + "\n\n".join(
                [
                    f"[{r.role.value}] {r.text[:300]}..."
                    for r in phase1_results + phase2_results
                ]
            )
        )
        phase3_results = await self.parallel_reasoning(
            synthesis_prompt, synthesizer_agents[:1]
        )

        # Build final result
        final_result = {
            "prompt": prompt,
            "phase1_analysis": [
                {
                    "agent": r.agent_id,
                    "role": r.role.value,
                    "confidence": r.confidence,
                    "summary": r.text[:200],
                }
                for r in phase1_results
            ],
            "phase2_critique": [
                {
                    "agent": r.agent_id,
                    "confidence": r.confidence,
                    "summary": r.text[:200],
                }
                for r in phase2_results
            ],
            "phase3_synthesis": {
                "agent": phase3_results[0].agent_id,
                "confidence": phase3_results[0].confidence,
                "text": phase3_results[0].text,
            },
            "final_consensus": phase3_results[0].text,
            "overall_confidence": self._calculate_overall_confidence(
                phase1_results + phase2_results + phase3_results
            ),
        }

        if self.verbose:
            self._display_hierarchical_result(final_result)

        return final_result

    def decompose_problem(self, complex_prompt: str, num_subtasks: int = 3) -> List[str]:
        """
        Decompose a complex problem into subtasks.

        In a real implementation, this would use LLM to intelligently decompose.
        For now, we create simple variations.
        """
        subtasks = [
            f"Aspect {i+1} of the problem: {complex_prompt}" for i in range(num_subtasks)
        ]
        return subtasks

    async def distributed_reasoning(self, complex_prompt: str) -> Dict[str, Any]:
        """
        Solve a complex problem through distributed reasoning:
        1. Decompose problem into subtasks
        2. Distribute subtasks to specialized agents
        3. Aggregate results
        4. Synthesize final answer
        """
        if self.verbose:
            console.print("\n[bold yellow]🌐 Distributed Reasoning[/bold yellow]\n")

        # Decompose problem
        subtasks = self.decompose_problem(complex_prompt, num_subtasks=3)

        # Assign to different agents
        explorer_agents = [
            aid for aid, cfg in self.agents.items() if cfg.role == AgentRole.EXPLORER
        ]

        subtask_results = []
        for i, subtask in enumerate(subtasks):
            agent_id = explorer_agents[i % len(explorer_agents)]
            console.print(f"[cyan]Subtask {i+1}:[/cyan] Assigned to {agent_id}")

            task = self.create_task(subtask)
            self.assign_task(task.task_id, agent_id)
            result = await self.execute_task(task.task_id)
            subtask_results.append(result)

        # Synthesize
        console.print("\n[bold]Aggregating results...[/bold]")
        synthesis = await self._synthesize_distributed_results(
            complex_prompt, subtask_results
        )

        return {
            "prompt": complex_prompt,
            "subtasks": subtasks,
            "subtask_results": [
                {
                    "agent": r.agent_id,
                    "confidence": r.confidence,
                    "summary": r.text[:150],
                }
                for r in subtask_results
            ],
            "final_synthesis": synthesis.text,
            "overall_confidence": synthesis.confidence,
        }

    async def _synthesize_distributed_results(
        self, original_prompt: str, results: List[AgentResult]
    ) -> AgentResult:
        """Synthesize results from distributed reasoning."""
        synthesizer_agents = [
            aid for aid, cfg in self.agents.items() if cfg.role == AgentRole.SYNTHESIZER
        ]

        if not synthesizer_agents:
            # Fallback: return highest confidence result
            return max(results, key=lambda r: r.confidence)

        synthesis_prompt = (
            f"Original question: {original_prompt}\n\n"
            f"Subtask results to synthesize:\n"
            + "\n\n".join([f"- {r.text[:200]}..." for r in results])
        )

        task = self.create_task(synthesis_prompt)
        self.assign_task(task.task_id, synthesizer_agents[0])
        return await self.execute_task(task.task_id)

    def _calculate_confidence(self, metrics: Dict[str, float]) -> float:
        """Calculate confidence score from metrics."""
        if not metrics:
            return 0.5

        # Higher semantic delta and freedom = higher confidence
        # Lower blocked tensor = higher confidence
        semantic = metrics.get("semantic_delta", 0.5)
        freedom = metrics.get("freedom_pressure", 0.5)
        blocked = metrics.get("blocked_tensor", 0.5)

        confidence = (semantic * 0.4 + freedom * 0.4 + (1.0 - blocked) * 0.2)
        return max(0.0, min(1.0, confidence))

    def _calculate_overall_confidence(self, results: List[AgentResult]) -> float:
        """Calculate overall confidence from multiple results."""
        if not results:
            return 0.0
        return sum(r.confidence for r in results) / len(results)

    def _extract_insights(self, text: str) -> List[str]:
        """Extract key insights from reasoning text."""
        # Simplified: split into sentences
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        return sentences[:3]  # Top 3 insights

    def _display_hierarchical_result(self, result: Dict[str, Any]) -> None:
        """Display hierarchical reasoning result in a beautiful format."""
        tree = Tree("[bold magenta]Hierarchical Reasoning Result[/bold magenta]")

        # Phase 1
        phase1 = tree.add("[bold cyan]Phase 1: Analysis[/bold cyan]")
        for analysis in result["phase1_analysis"]:
            phase1.add(
                f"[green]{analysis['role']}[/green] "
                f"(confidence: {analysis['confidence']:.2f})"
            )

        # Phase 2
        phase2 = tree.add("[bold yellow]Phase 2: Critique[/bold yellow]")
        for critique in result["phase2_critique"]:
            phase2.add(f"Agent {critique['agent']} (confidence: {critique['confidence']:.2f})")

        # Phase 3
        phase3 = tree.add("[bold green]Phase 3: Synthesis[/bold green]")
        phase3.add(f"Overall confidence: {result['overall_confidence']:.2f}")

        console.print(tree)
        console.print(
            Panel(
                result["final_consensus"][:500] + "...",
                title="[bold]Final Consensus[/bold]",
                border_style="green",
            )
        )


# ============================================================================
# Demo & Main
# ============================================================================


def create_sample_agents() -> MultiAgentReasoningSystem:
    """Create a sample multi-agent system with diverse philosopher groups."""
    system = MultiAgentReasoningSystem(verbose=True)

    # Analyst agents
    system.register_agent(
        AgentConfig(
            agent_id="analyst-1",
            role=AgentRole.ANALYST,
            philosophers=["Socrates", "Kant", "Wittgenstein"],
            priority=1,
        )
    )
    system.register_agent(
        AgentConfig(
            agent_id="analyst-2",
            role=AgentRole.ANALYST,
            philosophers=["Hegel", "Foucault", "Husserl"],
            priority=1,
        )
    )

    # Explorer agents
    system.register_agent(
        AgentConfig(
            agent_id="explorer-1",
            role=AgentRole.EXPLORER,
            philosophers=["Nietzsche", "Kierkegaard", "Camus"],
            priority=2,
        )
    )

    # Critic agents
    system.register_agent(
        AgentConfig(
            agent_id="critic-1",
            role=AgentRole.CRITIC,
            philosophers=["Popper", "Russell", "Quine"],
            priority=1,
        )
    )

    # Synthesizer agents
    system.register_agent(
        AgentConfig(
            agent_id="synthesizer-1",
            role=AgentRole.SYNTHESIZER,
            philosophers=["Heidegger", "Dewey", "Whitehead"],
            priority=3,
        )
    )

    return system


async def demo_parallel_reasoning():
    """Demo: Parallel reasoning with multiple agents."""
    console.print("\n[bold]Demo 1: Parallel Reasoning[/bold]")
    console.print("=" * 60)

    system = create_sample_agents()
    prompt = "What is the nature of consciousness?"

    agent_ids = ["analyst-1", "analyst-2", "explorer-1"]
    results = await system.parallel_reasoning(prompt, agent_ids)

    console.print("\n[bold green]Results:[/bold green]")
    for result in results:
        console.print(
            Panel(
                f"[cyan]Confidence:[/cyan] {result.confidence:.2f}\n\n"
                f"{result.text[:300]}...",
                title=f"Agent: {result.agent_id} ({result.role.value})",
            )
        )


async def demo_hierarchical_reasoning():
    """Demo: Hierarchical reasoning."""
    console.print("\n[bold]Demo 2: Hierarchical Reasoning[/bold]")
    console.print("=" * 60)

    system = create_sample_agents()
    prompt = "What is the meaning of life?"

    result = await system.hierarchical_reasoning(prompt)


async def demo_distributed_reasoning():
    """Demo: Distributed reasoning for complex problems."""
    console.print("\n[bold]Demo 3: Distributed Reasoning[/bold]")
    console.print("=" * 60)

    system = create_sample_agents()
    prompt = "How can we build ethical AI systems that benefit humanity?"

    result = await system.distributed_reasoning(prompt)

    console.print("\n[bold green]Final Synthesis:[/bold green]")
    console.print(Panel(result["final_synthesis"][:500] + "..."))


async def main():
    """Run all demos."""
    console.print("[bold magenta]Multi-Agent Reasoning System Demo[/bold magenta]\n")

    await demo_parallel_reasoning()
    await demo_hierarchical_reasoning()
    await demo_distributed_reasoning()

    console.print("\n[bold green]✓ All demos completed![/bold green]")


if __name__ == "__main__":
    asyncio.run(main())
