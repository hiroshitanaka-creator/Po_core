"""
Philosopher Party Machine 🎉
============================

Interactive system that automatically suggests optimal philosopher combinations
based on research findings and executes engaging philosophical reasoning sessions.

Based on research data:
- RQ1: Best combinations (4-philosopher groups with 100% emergence)
- RQ3: Optimal group size (8-14 philosophers, peak at 15)
- RQ4: Dialectical tension correlation (+1975% emergence increase)

Usage:
    from po_core.party_machine import PhilosopherPartyMachine

    party = PhilosopherPartyMachine()
    config = party.suggest_party(
        theme="AI and responsibility",
        mood="balanced"  # calm, balanced, chaotic, critical
    )
    results = party.run_party(config)
    party.visualize_results(results)

Parallel Execution:
    from po_core.party_machine import run_philosophers

    proposals, results = run_philosophers(
        philosophers, ctx, intent, tensors, memory,
        max_workers=12, timeout_s=1.2
    )
"""
from __future__ import annotations

import random
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dataclasses import dataclass, field
from enum import Enum
from time import perf_counter
from typing import Dict, List, Mapping, Optional, Sequence, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from po_core.domain.context import Context
    from po_core.domain.intent import Intent
    from po_core.domain.memory_snapshot import MemorySnapshot
    from po_core.domain.proposal import Proposal
    from po_core.domain.tensor_snapshot import TensorSnapshot
    from po_core.philosophers.base import PhilosopherProtocol

from po_core.domain.keys import PO_CORE, AUTHOR

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class PartyMood(str, Enum):
    """Mood/atmosphere for the philosophical party."""

    CALM = "calm"  # Low tension, harmonious discussion
    BALANCED = "balanced"  # Moderate tension, diverse perspectives
    CHAOTIC = "chaotic"  # High tension, maximum disagreement
    CRITICAL = "critical"  # Critical/skeptical emphasis


class PhilosophicalTheme(str, Enum):
    """Common philosophical themes."""

    ETHICS = "ethics"
    EXISTENCE = "existence"
    KNOWLEDGE = "knowledge"
    POLITICS = "politics"
    CONSCIOUSNESS = "consciousness"
    FREEDOM = "freedom"
    MEANING = "meaning"
    JUSTICE = "justice"
    TECHNOLOGY = "technology"
    DEATH = "death"


@dataclass
class PartyConfig:
    """Configuration for a philosopher party."""

    theme: str
    mood: PartyMood
    philosophers: List[str]
    expected_size: int
    expected_tension: float  # 0.0-1.0
    expected_emergence: float  # 0.0-1.0
    reasoning: str = ""  # Why this combination was chosen


@dataclass
class PartyResults:
    """Results from a philosopher party session."""

    config: PartyConfig
    responses: List[Dict]
    metrics: Dict[str, float]
    consensus: Dict
    emergence_detected: bool
    tension_level: float
    visualization_data: Dict = field(default_factory=dict)


# ============================================================================
# Parallel Execution Engine
# ============================================================================


@dataclass(frozen=True)
class RunResult:
    """Result of a single philosopher execution."""

    philosopher_id: str
    ok: bool
    n: int = 0  # Number of proposals generated
    timed_out: bool = False
    error: Optional[str] = None
    latency_ms: Optional[int] = None  # Execution time in milliseconds


def run_philosophers(
    philosophers: Sequence["PhilosopherProtocol"],
    ctx: "Context",
    intent: "Intent",
    tensors: "TensorSnapshot",
    memory: "MemorySnapshot",
    *,
    max_workers: int,
    timeout_s: float,
) -> Tuple[List["Proposal"], List[RunResult]]:
    """
    Execute philosophers in parallel with timeout and isolation.

    Args:
        philosophers: Sequence of philosopher instances to execute
        ctx: Context for the current request
        intent: Parsed intent from intention stage
        tensors: Current tensor snapshot (safety metrics)
        memory: Current memory snapshot
        max_workers: Maximum number of parallel workers
        timeout_s: Timeout in seconds for each philosopher

    Returns:
        Tuple of:
        - List[Proposal]: Successfully generated proposals
        - List[RunResult]: Execution results for each philosopher

    Example:
        proposals, results = run_philosophers(
            philosophers, ctx, intent, tensors, memory,
            max_workers=12, timeout_s=1.2
        )
        # Combine proposals in ensemble...
    """
    from po_core.domain.proposal import Proposal

    proposals: List[Proposal] = []
    results: List[RunResult] = []

    if not philosophers:
        return proposals, results

    def _embed_author(p: "Proposal", author: str) -> "Proposal":
        """Embed author into proposal.extra[PO_CORE][AUTHOR]."""
        extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
        pc = dict(extra.get(PO_CORE, {}))
        pc[AUTHOR] = author
        extra[PO_CORE] = pc
        return Proposal(
            proposal_id=p.proposal_id,
            action_type=p.action_type,
            content=p.content,
            confidence=p.confidence,
            assumption_tags=list(p.assumption_tags),
            risk_tags=list(p.risk_tags),
            extra=extra,
        )

    def _run_single(ph: "PhilosopherProtocol") -> Tuple[Optional[Proposal], int, Optional[str], int, str]:
        """Run a single philosopher with error handling and timing.

        Returns:
            Tuple of (proposal, n_proposals, error, latency_ms, philosopher_id)
        """
        pid = getattr(ph, "name", ph.__class__.__name__)
        t0 = perf_counter()
        try:
            proposal = ph.deliberate(ctx, intent, tensors, memory)
            dt = int((perf_counter() - t0) * 1000)
            # Embed author into proposal
            if proposal is not None:
                proposal = _embed_author(proposal, pid)
            return proposal, 1 if proposal else 0, None, dt, pid
        except Exception as e:
            dt = int((perf_counter() - t0) * 1000)
            tb = traceback.format_exc()
            return None, 0, f"{type(e).__name__}: {e}\n{tb}", dt, pid

    # Parallel execution with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_run_single, ph): ph for ph in philosophers}

        for future in futures:
            ph = futures[future]
            pid = getattr(ph, "name", ph.__class__.__name__)
            try:
                proposal, n, err, dt, author_id = future.result(timeout=timeout_s)
                results.append(RunResult(
                    philosopher_id=author_id,
                    ok=(err is None),
                    n=n,
                    timed_out=False,
                    error=err,
                    latency_ms=dt,
                ))
                if proposal is not None:
                    proposals.append(proposal)
            except FuturesTimeoutError:
                results.append(RunResult(
                    philosopher_id=pid,
                    ok=False,
                    n=0,
                    timed_out=True,
                    error=f"Timeout after {timeout_s}s",
                    latency_ms=None,
                ))
            except Exception as e:
                results.append(RunResult(
                    philosopher_id=pid,
                    ok=False,
                    n=0,
                    timed_out=False,
                    error=f"{type(e).__name__}: {e}",
                    latency_ms=None,
                ))

    return proposals, results


# ============================================================================
# Research-Based Knowledge Base
# ============================================================================

# Best 4-philosopher combinations (from RQ1)
OPTIMAL_4_COMBOS: Dict[PhilosophicalTheme, List[List[str]]] = {
    PhilosophicalTheme.ETHICS: [
        ["kant", "mill", "levinas", "confucius"],
        ["aristotle", "kant", "rawls", "levinas"],
        ["confucius", "dewey", "levinas", "arendt"],
    ],
    PhilosophicalTheme.EXISTENCE: [
        ["heidegger", "sartre", "kierkegaard", "levinas"],
        ["heidegger", "merleau_ponty", "levinas", "watsuji"],
        ["sartre", "kierkegaard", "dewey", "watsuji"],
    ],
    PhilosophicalTheme.KNOWLEDGE: [
        ["aristotle", "dewey", "peirce", "wittgenstein"],
        ["kant", "dewey", "peirce", "merleau_ponty"],
        ["confucius", "dewey", "wittgenstein", "derrida"],
    ],
    PhilosophicalTheme.POLITICS: [
        ["aristotle", "rawls", "arendt", "confucius"],
        ["mill", "rawls", "arendt", "dewey"],
        ["aristotle", "mill", "arendt", "levinas"],
    ],
    PhilosophicalTheme.FREEDOM: [
        ["sartre", "mill", "dewey", "nietzsche"],
        ["kierkegaard", "mill", "arendt", "dewey"],
        ["sartre", "rawls", "dewey", "levinas"],
    ],
    PhilosophicalTheme.CONSCIOUSNESS: [
        ["heidegger", "merleau_ponty", "jung", "lacan"],
        ["sartre", "merleau_ponty", "jung", "watsuji"],
        ["kierkegaard", "jung", "lacan", "levinas"],
    ],
}

# Philosopher tension pairs (high dialectical tension)
HIGH_TENSION_PAIRS: List[Tuple[str, str]] = [
    ("kant", "nietzsche"),  # Duty vs. Will-to-Power
    ("aristotle", "derrida"),  # Essentialism vs. Deconstruction
    ("confucius", "sartre"),  # Harmony vs. Radical Freedom
    ("heidegger", "dewey"),  # Being vs. Pragmatism
    ("mill", "kierkegaard"),  # Utilitarianism vs. Existentialism
    ("rawls", "deleuze"),  # Justice vs. Difference
    ("levinas", "nietzsche"),  # Ethics of Other vs. Self-Overcoming
]

# Philosopher compatibility clusters
HARMONIOUS_CLUSTERS: Dict[str, List[str]] = {
    "continental": ["heidegger", "sartre", "kierkegaard", "merleau_ponty", "levinas"],
    "analytic": ["wittgenstein", "dewey", "peirce", "mill"],
    "eastern": ["confucius", "zhuangzi", "watsuji", "wabi_sabi"],
    "political": ["aristotle", "rawls", "arendt", "mill", "dewey"],
    "psychoanalytic": ["jung", "lacan", "nietzsche"],
    "postmodern": ["derrida", "deleuze", "badiou", "lacan"],
}


# ============================================================================
# Philosopher Party Machine
# ============================================================================


class PhilosopherPartyMachine:
    """
    Automatically suggests and runs optimal philosopher combinations
    based on research findings.
    """

    def __init__(self, verbose: bool = True):
        """Initialize the party machine."""
        self.verbose = verbose
        self.available_philosophers = [
            "aristotle", "kant", "mill", "confucius", "dewey",
            "heidegger", "sartre", "kierkegaard", "merleau_ponty",
            "levinas", "rawls", "arendt", "peirce", "wittgenstein",
            "derrida", "deleuze", "badiou", "jung", "watsuji",
            "zhuangzi", "wabi_sabi", "lacan",
        ]

    def suggest_party(
        self,
        theme: str,
        mood: PartyMood = PartyMood.BALANCED,
        custom_prompt: Optional[str] = None,
    ) -> PartyConfig:
        """
        Suggest optimal philosopher party configuration.

        Args:
            theme: Philosophical theme (ethics, existence, etc.)
            mood: Desired atmosphere (calm, balanced, chaotic, critical)
            custom_prompt: Optional custom theme description

        Returns:
            PartyConfig with suggested philosophers and parameters
        """
        # Normalize theme
        theme_key = self._match_theme(theme)

        # Determine optimal size based on mood and research
        size = self._determine_size(mood)

        # Select philosophers based on theme and mood
        philosophers = self._select_philosophers(theme_key, mood, size)

        # Calculate expected metrics
        tension = self._estimate_tension(philosophers, mood)
        emergence = self._estimate_emergence(philosophers, tension)

        # Generate reasoning
        reasoning = self._generate_reasoning(theme, mood, philosophers, tension, emergence)

        config = PartyConfig(
            theme=custom_prompt or theme,
            mood=mood,
            philosophers=philosophers,
            expected_size=len(philosophers),
            expected_tension=tension,
            expected_emergence=emergence,
            reasoning=reasoning,
        )

        if self.verbose:
            self._display_config(config)

        return config

    def _match_theme(self, theme: str) -> PhilosophicalTheme:
        """Match user theme to enum."""
        theme_lower = theme.lower()

        # Direct match
        for t in PhilosophicalTheme:
            if t.value in theme_lower:
                return t

        # Keyword matching
        keywords = {
            PhilosophicalTheme.ETHICS: ["moral", "right", "wrong", "responsibility", "duty"],
            PhilosophicalTheme.EXISTENCE: ["being", "dasein", "ontology", "existence"],
            PhilosophicalTheme.KNOWLEDGE: ["epistemology", "truth", "knowledge", "certainty"],
            PhilosophicalTheme.POLITICS: ["society", "democracy", "power", "government"],
            PhilosophicalTheme.CONSCIOUSNESS: ["mind", "awareness", "subject", "psyche"],
            PhilosophicalTheme.FREEDOM: ["liberty", "autonomy", "choice", "free will"],
            PhilosophicalTheme.MEANING: ["purpose", "significance", "life", "value"],
            PhilosophicalTheme.JUSTICE: ["fairness", "equality", "rights", "law"],
            PhilosophicalTheme.TECHNOLOGY: ["AI", "machine", "digital", "virtual"],
            PhilosophicalTheme.DEATH: ["mortality", "dying", "afterlife", "finitude"],
        }

        for theme_enum, words in keywords.items():
            if any(word in theme_lower for word in words):
                return theme_enum

        # Default to meaning
        return PhilosophicalTheme.MEANING

    def _determine_size(self, mood: PartyMood) -> int:
        """Determine optimal group size based on mood and research."""
        # Research findings: 8-14 optimal, peak at 15
        if mood == PartyMood.CALM:
            return random.choice([4, 5, 6])  # Smaller, harmonious groups
        elif mood == PartyMood.BALANCED:
            return random.choice([8, 10, 12, 15])  # Optimal range
        elif mood == PartyMood.CHAOTIC:
            return random.choice([15, 18, 20])  # Larger, more complex
        else:  # CRITICAL
            return random.choice([6, 8, 10])  # Medium with critical focus

    def _select_philosophers(
        self,
        theme: PhilosophicalTheme,
        mood: PartyMood,
        size: int,
    ) -> List[str]:
        """Select philosophers based on theme, mood, and desired size."""
        selected = []

        # Start with optimal combo if size <= 4
        if size <= 4 and theme in OPTIMAL_4_COMBOS:
            combo = random.choice(OPTIMAL_4_COMBOS[theme])
            return combo[:size]

        # For larger groups, build strategically
        if theme in OPTIMAL_4_COMBOS:
            # Start with a good base combo
            base = random.choice(OPTIMAL_4_COMBOS[theme])
            selected.extend(base)

        # Add philosophers based on mood
        if mood == PartyMood.CALM:
            # Add harmonious philosophers
            cluster = random.choice(list(HARMONIOUS_CLUSTERS.values()))
            for p in cluster:
                if p not in selected and len(selected) < size:
                    selected.append(p)

        elif mood == PartyMood.CHAOTIC:
            # Add tension-creating pairs
            for p1, p2 in HIGH_TENSION_PAIRS:
                if len(selected) >= size:
                    break
                if p1 not in selected:
                    selected.append(p1)
                if len(selected) < size and p2 not in selected:
                    selected.append(p2)

        elif mood == PartyMood.CRITICAL:
            # Add critical/skeptical philosophers
            critical_types = ["nietzsche", "wittgenstein", "derrida", "kierkegaard", "sartre"]
            for p in critical_types:
                if p not in selected and len(selected) < size:
                    selected.append(p)

        # Fill remaining slots with diverse philosophers
        remaining = [p for p in self.available_philosophers if p not in selected]
        random.shuffle(remaining)

        while len(selected) < size and remaining:
            selected.append(remaining.pop())

        return selected[:size]

    def _estimate_tension(self, philosophers: List[str], mood: PartyMood) -> float:
        """Estimate dialectical tension level."""
        tension = 0.0

        # Count tension pairs
        tension_count = 0
        for p1, p2 in HIGH_TENSION_PAIRS:
            if p1 in philosophers and p2 in philosophers:
                tension_count += 1

        # Base tension from pairs
        tension = min(1.0, tension_count * 0.2)

        # Mood adjustment
        mood_multiplier = {
            PartyMood.CALM: 0.3,
            PartyMood.BALANCED: 0.7,
            PartyMood.CHAOTIC: 1.2,
            PartyMood.CRITICAL: 0.9,
        }
        tension *= mood_multiplier[mood]

        # Diversity bonus
        clusters_present = sum(
            1 for cluster in HARMONIOUS_CLUSTERS.values()
            if any(p in philosophers for p in cluster)
        )
        diversity_factor = min(1.0, clusters_present / 4)
        tension += diversity_factor * 0.3

        return min(1.0, tension)

    def _estimate_emergence(self, philosophers: List[str], tension: float) -> float:
        """Estimate emergence probability based on research findings."""
        # Base from group size (research: 8-14 optimal)
        size = len(philosophers)
        if 8 <= size <= 14:
            size_factor = 1.0
        elif size == 15:
            size_factor = 1.1  # Peak performance
        elif 4 <= size < 8:
            size_factor = 0.7
        else:
            size_factor = 0.5

        # Research finding: Tension increases emergence by ~19.75x (1975%)
        # We model this as: emergence = base * (1 + tension * 19)
        base_emergence = 0.05  # 5% baseline
        emergence = base_emergence * (1 + tension * 19) * size_factor

        return min(1.0, emergence)

    def _generate_reasoning(
        self,
        theme: str,
        mood: PartyMood,
        philosophers: List[str],
        tension: float,
        emergence: float,
    ) -> str:
        """Generate human-readable reasoning for the configuration."""
        lines = [
            f"🎯 Theme: {theme}",
            f"🎭 Mood: {mood.value}",
            f"👥 Party size: {len(philosophers)} philosophers",
            f"",
            f"⚡ Expected tension: {tension:.1%}",
            f"✨ Expected emergence: {emergence:.1%}",
            f"",
            "📊 Research basis:",
        ]

        # Add research insights
        if len(philosophers) == 4:
            lines.append("  • Optimal 4-philosopher combo (100% emergence from RQ1)")
        elif 8 <= len(philosophers) <= 14:
            lines.append("  • Optimal group size range (RQ3: 8-14 philosophers)")
        elif len(philosophers) == 15:
            lines.append("  • Peak performance size (RQ3: 15 philosophers)")

        if tension > 0.6:
            lines.append(f"  • High dialectical tension → +{int(tension * 1975)}% emergence boost (RQ4)")

        lines.append("")
        lines.append(f"🧠 Selected philosophers: {', '.join(philosophers)}")

        return "\n".join(lines)

    def _display_config(self, config: PartyConfig) -> None:
        """Display party configuration with Rich formatting."""
        console.print(Panel(
            config.reasoning,
            title=f"[bold magenta]🎉 Philosopher Party Configuration[/bold magenta]",
            border_style="magenta",
        ))


# ============================================================================
# Factory Functions
# ============================================================================


def create_party(theme: str, mood: str = "balanced") -> PartyConfig:
    """
    Quick factory function to create a party configuration.

    Args:
        theme: Philosophical theme
        mood: Party mood (calm, balanced, chaotic, critical)

    Returns:
        PartyConfig ready to run
    """
    machine = PhilosopherPartyMachine(verbose=False)
    mood_enum = PartyMood(mood)
    return machine.suggest_party(theme, mood_enum)


__all__ = [
    "PhilosopherPartyMachine",
    "PartyConfig",
    "PartyResults",
    "PartyMood",
    "PhilosophicalTheme",
    "create_party",
    # Parallel execution
    "run_philosophers",
    "RunResult",
]
