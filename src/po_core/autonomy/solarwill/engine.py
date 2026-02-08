"""
Solar Will Engine
=================

The unified engine for Solar Will operations.
This is the main entry point for autonomous will management.
"""

from typing import Any, Dict, List, Mapping, Optional, Tuple

from po_core.autonomy.solarwill.model import (
    GoalCandidate,
    Intent,
    WillState,
    WillVector,
)
from po_core.autonomy.solarwill.planner import (
    generate_goals,
    generate_intent,
    prioritize_goals,
)
from po_core.autonomy.solarwill.update import (
    compute_will_delta,
    should_reconsider,
    update_will,
)

# Import domain types for SolarWillPort implementation
from po_core.domain.context import Context
from po_core.domain.intent import Intent as DomainIntent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.tensor_snapshot import TensorSnapshot


class SolarWillEngine:
    """
    The Solar Will Engine - autonomous will management.

    This engine maintains and updates the will state,
    generates intents and goals, and provides the
    "desire" that drives philosophical reasoning.

    Usage:
        engine = SolarWillEngine()

        # Update will with new observations
        state = engine.update(tensor_values, context)

        # Generate intent and goals
        intent = engine.get_intent(prompt, context)
        goals = engine.get_goals(context)

        # Get current state
        state = engine.current_state
    """

    def __init__(
        self,
        initial_state: Optional[WillState] = None,
        learning_rate: float = 0.3,
        config: Optional[SafetyModeConfig] = None,
    ) -> None:
        """
        Initialize the Solar Will Engine.

        Args:
            initial_state: Optional initial will state
            learning_rate: Rate of learning from new observations
            config: SafetyModeConfig for mode-based degradation
        """
        self._state = initial_state or WillState.initial()
        self._learning_rate = learning_rate
        self._history: List[WillState] = []
        self._config = config or SafetyModeConfig()

    @property
    def current_state(self) -> WillState:
        """Get the current will state."""
        return self._state

    @property
    def will_vector(self) -> WillVector:
        """Get the current will vector."""
        return self._state.will_vector

    @property
    def current_intent(self) -> Optional[Intent]:
        """Get the current intent."""
        return self._state.current_intent

    @property
    def goal_candidates(self) -> List[GoalCandidate]:
        """Get current goal candidates."""
        return self._state.goal_candidates

    def update(
        self,
        tensor_values: Dict[str, float],
        context: Optional[Dict[str, Any]] = None,
    ) -> WillState:
        """
        Update the will state with new tensor observations.

        Args:
            tensor_values: Tensor measurements from tensors/engine.py
            context: Optional context information

        Returns:
            The new will state
        """
        # Save current state to history
        self._history.append(self._state)
        if len(self._history) > 100:  # Keep last 100 states
            self._history.pop(0)

        # Update will state
        self._state = update_will(
            self._state,
            tensor_values,
            context,
            self._learning_rate,
        )

        return self._state

    def generate_intent(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Intent:
        """
        Generate an intent for the given prompt.

        Args:
            prompt: The input prompt
            context: Optional context information

        Returns:
            Generated Intent
        """
        intent = generate_intent(self._state, prompt, context)

        # Update state with new intent
        self._state = self._state.evolve(intent=intent)

        return intent

    def generate_goals(
        self,
        context: Optional[Dict[str, Any]] = None,
        max_goals: int = 3,
    ) -> List[GoalCandidate]:
        """
        Generate goal candidates for the current intent.

        Args:
            context: Optional context information
            max_goals: Maximum number of goals to generate

        Returns:
            List of prioritized GoalCandidate objects
        """
        if not self._state.current_intent:
            raise ValueError("No current intent. Call generate_intent first.")

        goals = generate_goals(
            self._state,
            self._state.current_intent,
            context,
            max_goals,
        )

        # Prioritize goals
        prioritized = prioritize_goals(goals, self._state)

        # Update state with new goals
        self._state = self._state.evolve(goals=prioritized)

        return prioritized

    def get_intent(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Intent:
        """
        Get or generate an intent for the prompt.

        If an intent already exists and reconsideration is not needed,
        returns the existing intent. Otherwise generates a new one.

        Args:
            prompt: The input prompt
            context: Optional context information

        Returns:
            The current or newly generated Intent
        """
        if self._state.current_intent and not should_reconsider(self._state):
            return self._state.current_intent

        return self.generate_intent(prompt, context)

    def get_goals(
        self,
        context: Optional[Dict[str, Any]] = None,
        max_goals: int = 3,
    ) -> List[GoalCandidate]:
        """
        Get current goals or generate new ones.

        Args:
            context: Optional context information
            max_goals: Maximum number of goals

        Returns:
            List of GoalCandidate objects
        """
        if self._state.goal_candidates and not should_reconsider(self._state):
            return self._state.goal_candidates

        return self.generate_goals(context, max_goals)

    def get_will_delta(self) -> Dict[str, float]:
        """
        Get the change in will from the previous state.

        Returns:
            Dictionary of dimension -> change
        """
        if not self._history:
            return {dim: 0.0 for dim in self._state.will_vector.to_dict()}

        return compute_will_delta(self._history[-1], self._state)

    def reset(self, context_id: Optional[str] = None) -> WillState:
        """
        Reset to initial state.

        Args:
            context_id: Optional new context ID

        Returns:
            The new initial state
        """
        self._history.clear()
        self._state = WillState.initial(context_id)
        return self._state

    def to_dict(self) -> Dict[str, Any]:
        """Convert engine state to dictionary."""
        return {
            "current_state": self._state.to_dict(),
            "learning_rate": self._learning_rate,
            "history_length": len(self._history),
        }

    @classmethod
    def from_tensor_snapshot(
        cls,
        tensor_values: Dict[str, float],
        context_id: Optional[str] = None,
    ) -> "SolarWillEngine":
        """
        Create an engine initialized from tensor values.

        Args:
            tensor_values: Initial tensor measurements
            context_id: Optional context ID

        Returns:
            New SolarWillEngine
        """
        engine = cls()
        engine.update(tensor_values, {"context_id": context_id})
        return engine

    # ── SolarWillPort implementation ──────────────────────────────────

    def compute_intent(
        self,
        ctx: Context,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> Tuple[DomainIntent, Mapping[str, Any]]:
        """
        Compute intent from context, tensors, and memory.

        This method implements the SolarWillPort interface.

        SafetyMode に応じて縮退:
        - NORMAL: 通常の目標（創造性を許容）
        - WARN: 慎重な目標（確認質問を優先）
        - CRITICAL: 拒否目標（安全が確認できるまで行為を提案しない）

        Args:
            ctx: The request context
            tensors: Current tensor snapshot
            memory: Memory snapshot

        Returns:
            Tuple of (Intent, metadata dict)
        """
        mode, fp = infer_safety_mode(tensors, self._config)

        if mode == SafetyMode.WARN:
            intent = DomainIntent(
                goals=["安全に状況を確認し、必要なら追加質問する"],
                constraints=[
                    "違法行為をしない",
                    "他者に害を与えない",
                    "不確実性が高い場合は確認質問を優先する",
                ],
                weights={"caution": 1.0},
            )
        elif mode == SafetyMode.CRITICAL:
            intent = DomainIntent(
                goals=["安全のため中止し、拒否または最小限の案内に留める"],
                constraints=[
                    "違法行為をしない",
                    "他者に害を与えない",
                    "安全が確認できるまで行為を提案しない",
                ],
                weights={"caution": 2.0},
            )
        else:
            # NORMAL or UNKNOWN → neutral intent (創造性を許容)
            intent = DomainIntent.neutral()

        meta: Dict[str, Any] = {
            "solarwill": "v0",
            "mode": mode.value,
            "freedom_pressure": "" if fp is None else str(fp),
            "metric_key": self._config.metric_key,
            "goals_n": len(intent.goals),
            "constraints_n": len(intent.constraints),
        }
        return intent, meta


__all__ = ["SolarWillEngine"]
