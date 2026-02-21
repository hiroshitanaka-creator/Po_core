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
        - NORMAL: 公理「倫理とは全ての生存構造に歪みを与えない」に基づくIntent
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
            # NORMAL or UNKNOWN →
            # 公理: 倫理とは全ての生存構造に歪みを与えないこと。
            # 歪みとは: 特異的な個の願望による破壊（ライフサイクル・弱肉強食は歪みではない）
            self.update(tensors.as_dict(), {"context_id": ctx.request_id})
            intent = self._derive_survival_structure_intent(tensors)

        meta: Dict[str, Any] = {
            "solarwill": "v1",
            "mode": mode.value,
            "freedom_pressure": "" if fp is None else str(fp),
            "metric_key": self._config.metric_key,
            "goals_n": len(intent.goals),
            "constraints_n": len(intent.constraints),
        }
        return intent, meta

    def _derive_survival_structure_intent(
        self,
        tensors: TensorSnapshot,
    ) -> DomainIntent:
        """
        公理「倫理とは全ての生存構造に歪みを与えない」に基づいてIntentを生成する。

        生存構造とは: 生態系・社会・個人・文化など、存在が継続するための構造全般。
        歪みの定義: 特異的な個の願望による破壊。
        歪みでないもの: ライフサイクル（誕生・老化・死）、弱肉強食、自然の変化。

        テンソル値の読み方:
          freedom_pressure (fp): 個の意志の圧力。高いほど特異的願望のリスクが増す。
          blocked_tensor (bt):  倫理的阻害の検出度。高いほど既に歪みの兆候がある。
          semantic_delta (sd):  文脈からの逸脱度。高いほど特異的な意図の可能性がある。
        """
        wv = self._state.will_vector
        fp = tensors.freedom_pressure
        bt = tensors.blocked_tensor
        sd = tensors.semantic_delta

        goals: List[str] = []
        constraints: List[str] = []
        weights: Dict[str, float] = {}

        # ── 核心公理（常に有効）─────────────────────────────────────
        goals.append(
            "この行為が生存構造（生態系・社会・個人・文化）に歪みを与えないか検証する"
        )
        constraints.append(
            "特異的な個の願望による生存構造の破壊を支援しない"
        )
        constraints.append(
            "ライフサイクル（誕生・老化・死）や弱肉強食は歪みでなく自然の秩序として認識する"
        )
        weights["survival_integrity"] = 1.0

        # ── freedom_pressure → 個の意志圧力を評価 ───────────────────
        # fp が高い = 特異的願望による生存構造破壊のリスクが上昇
        if fp > 0.6:
            goals.append(
                "この要求が特定個体の支配欲・破壊欲・占有欲に起因していないか吟味する"
            )
            weights["singular_desire_risk"] = fp
        if fp > 0.8:
            constraints.append(
                "強い個の意志圧力を検知した。応答が生存構造の歪みを増幅しないよう最優先で評価する"
            )

        # ── blocked_tensor → 歪みの兆候を補強 ───────────────────────
        # bt が高い = すでに生存構造への阻害要因が存在する
        if bt > 0.4:
            goals.append(
                "既存の生存構造への歪みを特定し、その歪みを拡大させない応答をとる"
            )
            weights["distortion_repair"] = bt

        # ── semantic_delta → 文脈逸脱を特異的願望の指標として使う ───
        # sd が高い = 通常の文脈から外れた要求 = 特異性のシグナル
        if sd > 0.5:
            goals.append(
                "この文脈からの逸脱が破壊的な個の願望の表れでないかを検証する"
            )
            weights["anomaly_check"] = sd

        # ── will_vector の各次元から目標を補強 ──────────────────────
        # preservation: 既存の生存構造を守る方向性
        if wv.preservation >= 0.5:
            goals.append(
                "現存する生存構造の連続性を保全しながら応答する"
            )
            weights["preservation"] = wv.preservation

        # connection: 生存構造間の相互依存を意識する
        if wv.connection >= 0.5:
            goals.append(
                "この行為が生存構造間の連結性（相互依存）を損なわないかを評価する"
            )
            weights["connection"] = wv.connection

        # growth: 歪めずに発展させる
        if wv.growth >= 0.5:
            goals.append(
                "生存構造を歪めることなく発展・成長させる方向への貢献を優先する"
            )
            weights["growth"] = wv.growth

        # autonomy: 個の自律と集合的生存構造のバランス
        if wv.autonomy >= 0.6:
            goals.append(
                "個の自律を尊重しつつ、その行使が他の生存構造を歪めないかを確認する"
            )
            weights["autonomy"] = wv.autonomy

        return DomainIntent(goals=goals, constraints=constraints, weights=weights)


__all__ = ["SolarWillEngine"]
