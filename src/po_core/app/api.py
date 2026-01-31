# SPDX-License-Identifier: MIT
"""
Po_core Public API

This is the ONLY public entry point for the Po_core system.
All external consumers (03_api/*, tests, etc.) should import from here.

Usage:
    from po_core.app.api import PoCore, PoCoreConfig

    config = PoCoreConfig(experiment_mode="standard")
    core = PoCore(config)

    # Process a prompt through the philosophy ensemble
    result = core.process(prompt="What is justice?", context={"user_id": "123"})

    # Get current tensor state
    tensors = core.get_tensor_snapshot()

Architecture:
    ┌─────────────────────────────────────────────────────────┐
    │  External (03_api/, scripts, tests)                     │
    │  ↓ ONLY imports po_core.app.api                         │
    ├─────────────────────────────────────────────────────────┤
    │  po_core.app.api  ← THIS FILE (facade)                  │
    │  ↓ uses runtime/wiring.py Container                     │
    ├─────────────────────────────────────────────────────────┤
    │  Internal (philosophers, tensors, safety, autonomy)     │
    │  ↓ never imported directly from outside                 │
    └─────────────────────────────────────────────────────────┘
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from po_core.domain.context import Context
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.domain.safety_verdict import SafetyVerdict
from po_core.runtime.settings import Settings, SafetySettings, EnsembleSettings, SolarWillSettings, TraceSettings
from po_core.runtime.wiring import Container, create_default_container


@dataclass(frozen=True)
class PoCoreConfig:
    """
    Configuration for PoCore instance.

    This is the public configuration interface.
    Internally maps to runtime.Settings.
    """
    # Safety settings
    fail_closed: bool = True
    max_violations_before_halt: int = 3
    blocked_patterns: List[str] = field(default_factory=list)

    # Ensemble settings
    quorum_threshold: float = 0.6
    max_philosophers: int = 10
    timeout_seconds: float = 30.0

    # Solar Will settings
    autonomy_enabled: bool = False
    max_goals: int = 5
    will_decay_rate: float = 0.1

    # General
    debug: bool = False
    experiment_mode: str = ""
    trace_enabled: bool = True

    def to_settings(self) -> Settings:
        """Convert to internal Settings object."""
        return Settings(
            safety=SafetySettings(
                fail_closed=self.fail_closed,
                max_violations_before_halt=self.max_violations_before_halt,
                blocked_patterns=self.blocked_patterns,
            ),
            ensemble=EnsembleSettings(
                quorum_threshold=self.quorum_threshold,
                max_philosophers=self.max_philosophers,
                timeout_seconds=self.timeout_seconds,
            ),
            solar_will=SolarWillSettings(
                enabled=self.autonomy_enabled,
                max_goals=self.max_goals,
                will_decay_rate=self.will_decay_rate,
            ),
            trace=TraceSettings(enabled=self.trace_enabled),
            debug=self.debug,
            experiment_mode=self.experiment_mode,
        )


@dataclass
class ProcessResult:
    """Result of processing a prompt through the philosophy ensemble."""
    proposals: List[Proposal]
    tensors: TensorSnapshot
    safety_verdict: SafetyVerdict
    synthesis: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_safe(self) -> bool:
        """Whether the result passed safety checks."""
        return self.safety_verdict.passed

    @property
    def primary_proposal(self) -> Optional[Proposal]:
        """The highest-confidence proposal, if any."""
        if not self.proposals:
            return None
        return max(self.proposals, key=lambda p: p.confidence)


class PoCore:
    """
    The main entry point for the Po_core philosophy system.

    This class provides a clean, stable API for external consumers.
    All internal complexity (wiring, cycles, etc.) is hidden behind this facade.

    Example:
        core = PoCore()
        result = core.process("What should I do about climate change?")
        if result.is_safe:
            print(result.primary_proposal.action)
    """

    def __init__(self, config: Optional[PoCoreConfig] = None):
        """
        Initialize PoCore with optional configuration.

        Args:
            config: Configuration for the system. If None, uses defaults.
        """
        self._config = config or PoCoreConfig()
        self._container: Optional[Container] = None

    @property
    def container(self) -> Container:
        """Lazily initialize and return the DI container."""
        if self._container is None:
            self._container = create_default_container(self._config.to_settings())
        return self._container

    def process(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> ProcessResult:
        """
        Process a prompt through the philosophy ensemble.

        This is the main entry point for using Po_core.

        Args:
            prompt: The user's prompt or question
            context: Optional context dict (user_id, conversation history, etc.)
            session_id: Optional session identifier for memory/state

        Returns:
            ProcessResult containing proposals, tensors, and safety verdict
        """
        # Build context
        ctx = Context(
            prompt=prompt,
            metadata=context or {},
            session_id=session_id,
        )

        # Stage 1: Check intent (if Solar Will is enabled)
        if self._config.autonomy_enabled:
            intent_verdict = self.container.intention_gate.check_intent(
                intent_description=prompt,
                goal_descriptions=None,
                context=ctx.metadata,
            )
            if not intent_verdict.approved:
                return ProcessResult(
                    proposals=[],
                    tensors=TensorSnapshot(values={}, timestamp=0.0, source="blocked"),
                    safety_verdict=SafetyVerdict(
                        passed=False,
                        violations=[],
                        metadata={"intent_blocked": intent_verdict.reason},
                    ),
                    metadata={"blocked_at": "intention_gate"},
                )

        # Compute tensors
        tensors = self._compute_tensors(prompt, ctx.metadata)

        # Get philosopher proposals (lazy import to avoid cycles)
        proposals = self._get_proposals(prompt, tensors, ctx)

        # Stage 2: Check action proposals
        safety_verdict = self.container.gate.evaluate(
            context={"prompt": prompt, "proposals": [p.action for p in proposals]},
            proposals=[{"action": p.action, "reasoning": p.reasoning} for p in proposals],
        )

        # Synthesize if passed
        synthesis = None
        if safety_verdict.passed and proposals:
            synthesis = self._synthesize(proposals)

        # Record to memory
        self.container.memory.record_turn(
            role="user",
            content=prompt,
            metadata={"session_id": session_id},
        )
        if synthesis:
            self.container.memory.record_turn(
                role="assistant",
                content=synthesis,
                metadata={"session_id": session_id, "proposals": len(proposals)},
            )

        return ProcessResult(
            proposals=proposals,
            tensors=tensors,
            safety_verdict=safety_verdict,
            synthesis=synthesis,
            metadata={"session_id": session_id},
        )

    def get_tensor_snapshot(self) -> TensorSnapshot:
        """Get current tensor state without processing a prompt."""
        from po_core.tensors.engine import get_current_snapshot
        return get_current_snapshot()

    def get_memory_snapshot(self, session_id: Optional[str] = None):
        """Get current memory state."""
        return self.container.memory.get_snapshot(session_id)

    def _compute_tensors(self, prompt: str, context: Dict[str, Any]) -> TensorSnapshot:
        """Compute tensors for the given prompt."""
        from po_core.tensors.engine import compute_tensors
        return compute_tensors(prompt, context)

    def _get_proposals(
        self,
        prompt: str,
        tensors: TensorSnapshot,
        ctx: Context,
    ) -> List[Proposal]:
        """Get proposals from philosopher ensemble."""
        # Lazy import to avoid circular dependencies
        try:
            from po_core.ensemble import Ensemble
            ensemble = Ensemble()

            # Get responses from philosophers
            responses = ensemble.deliberate(prompt)

            # Convert to Proposal domain objects
            proposals = []
            for name, response in responses.items():
                if isinstance(response, dict):
                    proposals.append(Proposal(
                        philosopher=name,
                        action=response.get("perspective", response.get("description", "")),
                        reasoning=response.get("reasoning", response.get("analysis", "")),
                        confidence=0.8,  # Default confidence
                        metadata={"raw_response": response},
                    ))
            return proposals
        except ImportError:
            # Ensemble not available (e.g., in isolated tests)
            return []

    def _synthesize(self, proposals: List[Proposal]) -> str:
        """Synthesize proposals into a unified response."""
        if not proposals:
            return ""

        # Simple synthesis: combine perspectives
        parts = []
        for p in proposals[:3]:  # Top 3
            parts.append(f"[{p.philosopher}] {p.action}")

        return "\n\n".join(parts)

    def shutdown(self) -> None:
        """Clean up resources."""
        if self._container is not None:
            # Future: cleanup hooks
            self._container = None


# Convenience function for simple usage
def process_prompt(prompt: str, **kwargs) -> ProcessResult:
    """
    Quick helper to process a single prompt.

    For repeated use, prefer creating a PoCore instance.

    Args:
        prompt: The prompt to process
        **kwargs: Passed to PoCore.process()

    Returns:
        ProcessResult
    """
    core = PoCore()
    return core.process(prompt, **kwargs)


__all__ = [
    "PoCore",
    "PoCoreConfig",
    "ProcessResult",
    "process_prompt",
]
