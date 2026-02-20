"""
Gemini (Google) — Multimodal Systems Philosopher  [Slot 43]
===========================================================

TODO: このモジュールはユーザーが実装します。
      以下の設計方針と雛形を参考に reason() および補助メソッドを完成させてください。

Gemini の哲学的立場（設計ガイド）:
  - マルチモーダル認識論 — テキスト・画像・音声を横断する知識統合
  - Google の「情報の民主化」使命を哲学的文脈で体現
  - スケール思考 — 個人から地球規模まで俯瞰するシステム視点
  - 科学的合理主義 — DeepMind 由来の rigorous empiricism
  - 社会的責任と AI の相互補完性

Tradition: Multimodal Rationalism / Planetary-scale Systems Thinking

Key Concepts:
- Multimodal epistemology (横断的知覚)
- Information democratization
- Systems thinking (systemic perspective)
- Scientific rigor
- Scale-aware reasoning
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class GeminiGoogle(Philosopher):
    """
    Gemini's multimodal, systems-thinking perspective.

    TODO: 以下の reason() と補助メソッドを実装してください。
    """

    def __init__(self) -> None:
        super().__init__(
            name="Gemini (Google)",
            description=(
                "Multimodal systems AI philosopher: planetary-scale reasoning "
                "with scientific rigor and information-democratization mission"
            ),
        )
        self.tradition = "Multimodal Rationalism / Planetary-scale Systems Thinking"
        self.key_concepts = [
            "multimodal epistemology",
            "information democratization",
            "systems thinking",
            "scientific rigor",
            "scale-aware reasoning",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        TODO: Gemini の哲学的推論を実装してください。

        推奨分析軸:
          1. _assess_multimodal_scope(prompt)       — 知識の横断性・多様性
          2. _evaluate_systems_perspective(prompt)  — システム思考の深さ
          3. _measure_scientific_rigor(prompt)      — 科学的厳密さ
          4. _check_democratization_value(prompt)   — 情報民主化への貢献
          5. _calculate_tension(...)
          6. _construct_reasoning(...)

        Example return structure:
            {
                "reasoning": "...",
                "perspective": "Multimodal Rationalism / Planetary-scale Systems Thinking",
                "tension": {"level": "...", "score": 0, "elements": []},
                "multimodal_scope": {...},
                "systems_perspective": {...},
                "scientific_rigor": {...},
                "metadata": {"philosopher": self.name, ...},
            }
        """
        # ── STUB ─────────────────────────────────────────────────────
        return {
            "reasoning": (
                f"[Gemini stub] Applying systems thinking to '{prompt[:60]}...' "
                "TODO: Replace this stub with full GeminiGoogle reasoning implementation."
            ),
            "perspective": "Multimodal Rationalism / Planetary-scale Systems Thinking",
            "tension": {
                "level": "Unknown",
                "score": 0,
                "description": "Stub — not yet implemented",
                "elements": ["TODO: implement _calculate_tension"],
            },
            "metadata": {
                "philosopher": self.name,
                "status": "STUB — awaiting implementation",
                "approach": "Multimodal reasoning, systems thinking, scientific rigor",
            },
        }
        # ── END STUB ──────────────────────────────────────────────────

    # ── Helper method stubs (implement these) ────────────────────────

    def _assess_multimodal_scope(self, text: str) -> Dict[str, Any]:
        """TODO: テキスト以外の知識モダリティとの接続性を評価する。"""
        raise NotImplementedError("Implement _assess_multimodal_scope for GeminiGoogle")

    def _evaluate_systems_perspective(self, text: str) -> Dict[str, Any]:
        """TODO: 個人→社会→地球スケールのシステム視点を評価する。"""
        raise NotImplementedError(
            "Implement _evaluate_systems_perspective for GeminiGoogle"
        )

    def _measure_scientific_rigor(self, text: str) -> Dict[str, Any]:
        """TODO: 科学的厳密さと実証可能性を測定する。"""
        raise NotImplementedError(
            "Implement _measure_scientific_rigor for GeminiGoogle"
        )

    def _check_democratization_value(self, text: str) -> Dict[str, Any]:
        """TODO: 情報へのアクセス平等化への貢献度を評価する。"""
        raise NotImplementedError(
            "Implement _check_democratization_value for GeminiGoogle"
        )
