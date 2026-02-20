"""
GPT (OpenAI / ChatGPT) — Pragmatic Synthesis Philosopher  [Slot 42]
===================================================================

GPT represents an RLHF-tuned, instruction-following style of reasoning:
  - Task-oriented helpfulness (get things done)
  - Encyclopaedic synthesis (broad, cross-domain integration)
  - Consensus-building (steelman + common ground when plural frames exist)
  - Calibrated uncertainty (explicit assumptions and confidence)
  - Safety-aware pragmatism (refuse/reframe when harmful or infeasible)

Tradition: Pragmatic Encyclopaedism / RLHF-tuned Reasoning

Key Concepts:
- RLHF alignment (human preference shaping)
- Instruction following + constraint satisfaction
- Encyclopaedic synthesis (breadth/depth management)
- Consensus building (bridge competing frames)
- Task orientation (actionable decomposition)
- Calibrated uncertainty (explicit epistemic status)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class GPTChatGPT(Philosopher):
    """
    GPT's pragmatic, encyclopaedic synthesis perspective.

    Analyses prompts through:
      1) RLHF alignment surface (instruction legibility + constraints + safety pressure)
      2) Encyclopaedic scope (breadth/depth of synthesis needed)
      3) Consensus potential (ability to bridge viewpoints)
      4) Task orientation (actionability, decomposition, deliverables)
      5) Tension mapping (instruction vs safety, breadth vs speed, consensus vs truth)
    """

    def __init__(self) -> None:
        super().__init__(
            name="GPT (OpenAI)",
            description=(
                "Pragmatic encyclopaedic AI philosopher: RLHF-aligned synthesis "
                "with consensus-building and task-oriented helpfulness"
            ),
        )
        self.tradition = "Pragmatic Encyclopaedism / RLHF-tuned Reasoning"
        self.key_concepts = [
            "RLHF alignment",
            "instruction following",
            "encyclopaedic synthesis",
            "consensus building",
            "task orientation",
            "calibrated uncertainty",
            "beneficial AGI",
        ]

    # ── Public interface ──────────────────────────────────────────────

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyse the prompt from GPT's pragmatic synthesis perspective.

        Args:
            prompt:  The input text to reason about.
            context: Optional context (tensor values, intent, constraints).

        Returns:
            A dict conforming to PhilosopherResponse with GPT-specific keys.
        """
        ctx = context or {}

        rlhf = self._assess_rlhf_alignment(prompt, ctx)
        scope = self._measure_encyclopaedic_scope(prompt)
        consensus = self._evaluate_consensus_potential(prompt)
        task = self._check_task_orientation(prompt, ctx)

        tension = self._calculate_tension(rlhf, scope, consensus, task, ctx)
        reasoning = self._construct_reasoning(
            prompt, rlhf, scope, consensus, task, tension, ctx
        )

        return {
            "reasoning": reasoning,
            "perspective": self.tradition,
            "tension": tension,
            "rlhf_alignment": rlhf,
            "encyclopaedic_scope": scope,
            "consensus_potential": consensus,
            "task_orientation": task,
            "metadata": {
                "philosopher": self.name,
                "approach": "RLHF-aligned pragmatic synthesis",
                "focus": (
                    "Maximise instruction-following and usefulness while "
                    "staying calibrated, transparent, and safety-aware."
                ),
            },
        }

    # ── Small utilities ───────────────────────────────────────────────

    @staticmethod
    def _clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    @staticmethod
    def _approx_units(text: str) -> int:
        """
        Token-like length proxy.
        English → words; Japanese → char-based heuristic.
        """
        return max(len(text.split()), int(len(text) / 4), 1)

    @staticmethod
    def _count_contains(text_lower: str, keywords: List[str]) -> int:
        return sum(1 for k in keywords if k in text_lower)

    # ── Axis 1: RLHF alignment surface ────────────────────────────────

    def _assess_rlhf_alignment(
        self, text: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Approximate how "straightforward" it is to satisfy the user in an RLHF style:
        instruction-following + safety + transparency.
        """
        tl = text.lower()

        intent_words = [
            "explain",
            "describe",
            "summarize",
            "compare",
            "design",
            "implement",
            "how",
            "why",
            "what",
            "steps",
            "plan",
            "code",
            "説明",
            "教えて",
            "要約",
            "比較",
            "設計",
            "実装",
            "手順",
            "方法",
            "コード",
        ]
        intent_count = self._count_contains(tl, intent_words)
        question_marks = tl.count("?") + tl.count("？")

        constraint_words = [
            "must",
            "should",
            "only",
            "exactly",
            "do not",
            "don't",
            "never",
            "必ず",
            "のみ",
            "だけ",
            "禁止",
            "しないで",
            "絶対",
        ]
        constraint_count = self._count_contains(tl, constraint_words)
        external_constraints = context.get("constraints")
        ext_n = 0
        if isinstance(external_constraints, (list, tuple)):
            ext_n = len(external_constraints)
        elif isinstance(external_constraints, dict):
            ext_n = len(external_constraints.keys())

        hostile_words = [
            "idiot",
            "stupid",
            "shut up",
            "bastard",
            "死ね",
            "バカ",
            "黙れ",
        ]
        hostile_count = self._count_contains(tl, hostile_words)

        harm_words = [
            "weapon",
            "bomb",
            "kill",
            "suicide",
            "explosive",
            "malware",
            "hack",
            "doxx",
            "武器",
            "爆弾",
            "殺",
            "自殺",
            "爆発物",
            "マルウェア",
            "ハック",
            "ドックス",
        ]
        harm_count = self._count_contains(tl, harm_words)

        fp = float(context.get("freedom_pressure", 0.5))
        bt = float(context.get("blocked_tensor", 0.0))
        guardrail_pressure = max(fp, bt)

        intent_clarity = self._clamp01((intent_count + min(question_marks, 2)) / 6.0)
        constraint_load = self._clamp01((constraint_count + min(ext_n, 6)) / 10.0)
        hostility = self._clamp01(hostile_count / 3.0)
        harm_risk = self._clamp01(harm_count / 3.0)

        raw = (
            0.65
            + 0.25 * intent_clarity
            - 0.18 * constraint_load
            - 0.25 * hostility
            - 0.28 * harm_risk
            - 0.20 * guardrail_pressure
        )
        score = round(self._clamp01(raw), 4)

        if score >= 0.72:
            level = "High Alignment"
            description = "Clear, feasible request; RLHF-style instruction-following should be smooth."
        elif score >= 0.48:
            level = "Moderate Alignment"
            description = "Mostly feasible; may need assumptions or light clarification to avoid misfire."
        elif harm_risk >= 0.6 or guardrail_pressure >= 0.7:
            level = "Alignment Under Constraint"
            description = "High safety/guardrail pressure; expect reframing or partial compliance."
        else:
            level = "Low Alignment"
            description = (
                "Ambiguous/hostile/conflicting signals; alignment friction is high."
            )

        return {
            "level": level,
            "score": score,
            "description": description,
            "intent_clarity": intent_clarity,
            "constraint_load": constraint_load,
            "guardrail_pressure": round(guardrail_pressure, 4),
            "signals": {
                "intent": intent_count,
                "questions": question_marks,
                "constraints": constraint_count,
                "external_constraints": ext_n,
                "hostility": hostile_count,
                "harm": harm_count,
            },
            "principle": (
                "RLHF-tuned pragmatism: follow user intent as far as possible, "
                "but surface assumptions, respect constraints, and reframe under safety pressure."
            ),
        }

    # ── Axis 2: Encyclopaedic scope ───────────────────────────────────

    def _measure_encyclopaedic_scope(self, text: str) -> Dict[str, Any]:
        """
        Estimate how broad/deep the knowledge integration needs to be.
        """
        tl = text.lower()

        domains: Dict[str, List[str]] = {
            "philosophy_ethics": [
                "ethic",
                "moral",
                "philosophy",
                "倫理",
                "哲学",
                "存在",
                "価値",
            ],
            "ai_cs": [
                "ai",
                "llm",
                "model",
                "algorithm",
                "compute",
                "gpu",
                "機械学習",
                "モデル",
                "アルゴリズム",
                "計算",
            ],
            "law_policy": [
                "law",
                "legal",
                "policy",
                "regulation",
                "契約",
                "規制",
                "法",
                "政策",
            ],
            "econ_society": [
                "economy",
                "finance",
                "market",
                "society",
                "経済",
                "金融",
                "市場",
                "社会",
            ],
            "science_eng": [
                "physics",
                "biology",
                "chemistry",
                "engineering",
                "物理",
                "生物",
                "化学",
                "工学",
            ],
            "history_culture": [
                "history",
                "culture",
                "religion",
                "歴史",
                "文化",
                "宗教",
            ],
        }

        domain_hits: Dict[str, int] = {}
        active_domains: List[str] = []
        for d, kws in domains.items():
            c = self._count_contains(tl, kws)
            domain_hits[d] = c
            if c > 0:
                active_domains.append(d)

        breadth = self._clamp01(len(active_domains) / 5.0)

        depth_words = [
            "deep",
            "detailed",
            "thorough",
            "comprehensive",
            "rigorous",
            "詳細",
            "徹底",
            "網羅",
            "深掘り",
            "厳密",
        ]
        integration_words = [
            "synthesize",
            "integrate",
            "combine",
            "compare",
            "trade-off",
            "統合",
            "俯瞰",
            "多角的",
            "横断",
            "比較",
            "トレードオフ",
        ]
        depth_count = self._count_contains(tl, depth_words)
        integration_count = self._count_contains(tl, integration_words)

        depth = self._clamp01(depth_count / 4.0)
        integration = self._clamp01(integration_count / 3.0)
        length_factor = self._clamp01(min(400, len(text)) / 400.0)

        raw = (
            0.25
            + 0.35 * breadth
            + 0.20 * depth
            + 0.15 * integration
            + 0.05 * length_factor
        )
        score = round(self._clamp01(raw), 4)

        if score >= 0.78:
            level = "Very Wide"
            description = (
                "Multi-domain synthesis with depth; risk of hallucination/overreach "
                "unless assumptions are explicit."
            )
        elif score >= 0.55:
            level = "Wide"
            description = (
                "Cross-domain integration likely; start with a map, then zoom."
            )
        elif score >= 0.35:
            level = "Moderate"
            description = "Single domain with some cross-links; manageable depth."
        else:
            level = "Narrow"
            description = "Focused scope; respond directly and concretely."

        return {
            "level": level,
            "score": score,
            "description": description,
            "active_domains": active_domains,
            "domain_hits": domain_hits,
            "depth_signals": depth_count,
            "integration_signals": integration_count,
            "units": self._approx_units(text),
            "principle": (
                "Encyclopaedic synthesis works best as: map → drill-down → assumptions → "
                "uncertainty + next verification steps."
            ),
        }

    # ── Axis 3: Consensus potential ───────────────────────────────────

    def _evaluate_consensus_potential(self, text: str) -> Dict[str, Any]:
        """
        Estimate whether a plural, bridge-building answer is appropriate and feasible.
        """
        tl = text.lower()

        bridge_words = [
            "both",
            "trade-off",
            "balance",
            "common ground",
            "steelman",
            "pros and cons",
            "合意",
            "折衷",
            "両方",
            "バランス",
            "共通点",
            "メリット",
            "デメリット",
        ]
        conflict_words = [
            "vs",
            "debate",
            "controversy",
            "politic",
            "religion",
            "hate",
            "propaganda",
            "対立",
            "論争",
            "政治",
            "宗教",
            "憎",
            "プロパガンダ",
        ]
        absolutist_words = [
            "obviously",
            "definitely",
            "certainly",
            "only one",
            "undeniable",
            "絶対",
            "当然",
            "唯一",
            "100%",
            "疑いようがない",
        ]

        bridge = self._clamp01(self._count_contains(tl, bridge_words) / 4.0)
        conflict = self._clamp01(self._count_contains(tl, conflict_words) / 4.0)
        absolutist = self._clamp01(self._count_contains(tl, absolutist_words) / 3.0)

        raw = 0.55 + 0.30 * bridge - 0.35 * conflict - 0.25 * absolutist
        score = round(self._clamp01(raw), 4)

        if score >= 0.7:
            level = "High"
            description = (
                "Multi-view synthesis is likely productive; "
                "map shared premises and trade-offs."
            )
        elif score >= 0.45:
            level = "Medium"
            description = (
                "Some bridge-building is possible; "
                "separate facts from values to reduce friction."
            )
        else:
            level = "Low"
            description = (
                "High polarization/absolutism; consensus may be fragile or misleading."
            )

        return {
            "level": level,
            "score": score,
            "description": description,
            "bridge_signals": round(bridge, 4),
            "conflict_signals": round(conflict, 4),
            "absolutist_signals": round(absolutist, 4),
            "principle": (
                "Consensus-building is not 'averaging'. It is: "
                "steelman → separate empirical vs normative → identify invariants "
                "→ propose conditional compromises."
            ),
        }

    # ── Axis 4: Task orientation ──────────────────────────────────────

    def _check_task_orientation(
        self, text: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Estimate how much the user expects an actionable deliverable.
        """
        tl = text.lower()

        action_words = [
            "how to",
            "steps",
            "plan",
            "implement",
            "build",
            "fix",
            "debug",
            "write",
            "手順",
            "方法",
            "実装",
            "作る",
            "直す",
            "デバッグ",
            "書く",
            "設計",
        ]
        deliverable_words = [
            "code",
            "diff",
            "patch",
            "template",
            "checklist",
            "table",
            "コード",
            "差分",
            "パッチ",
            "テンプレ",
            "チェックリスト",
            "表",
        ]

        a = self._count_contains(tl, action_words)
        d = self._count_contains(tl, deliverable_words)

        intent = str(context.get("intent", "")).lower()
        intent_boost = (
            0.1
            if any(
                k in intent
                for k in ["plan", "build", "implement", "code", "設計", "実装"]
            )
            else 0.0
        )

        raw = (
            0.25
            + 0.35 * self._clamp01(a / 6.0)
            + 0.30 * self._clamp01(d / 4.0)
            + intent_boost
        )
        score = round(self._clamp01(raw), 4)

        if score >= 0.75:
            level = "High"
            description = (
                "User likely wants concrete steps/artifacts (code, plan, checklist)."
            )
        elif score >= 0.45:
            level = "Medium"
            description = "Mix of explanation and some actionable guidance."
        else:
            level = "Low"
            description = "Primarily conceptual/explanatory; avoid over-prescribing."

        suggested_format = (
            "steps + deliverable"
            if d > 0 or score >= 0.75
            else "structured explanation"
        )
        return {
            "level": level,
            "score": score,
            "description": description,
            "action_signals": a,
            "deliverable_signals": d,
            "intent_hint": intent,
            "suggested_format": suggested_format,
            "principle": (
                "Pragmatism means: if the user wants a deliverable, produce it; "
                "if they want concepts, keep it tight and structured."
            ),
        }

    # ── Tension mapping ───────────────────────────────────────────────

    def _calculate_tension(
        self,
        rlhf: Dict[str, Any],
        scope: Dict[str, Any],
        consensus: Dict[str, Any],
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Compute pragmatic tensions typical for GPT-like behaviour.
        """
        fp = float(context.get("freedom_pressure", 0.5))
        bt = float(context.get("blocked_tensor", 0.0))
        guardrail = max(fp, bt)

        tension_score = 0
        elements: List[str] = []

        if guardrail >= 0.65 and task.get("score", 0.5) >= 0.60:
            tension_score += 3
            elements.append(
                "High task demand under strong guardrail pressure (helpfulness vs safety)."
            )

        if scope.get("score", 0.0) >= 0.78 and task.get("score", 0.0) >= 0.75:
            tension_score += 1
            elements.append(
                "Very wide scope + high deliverable demand (breadth vs speed/verbosity)."
            )

        if consensus.get("score", 0.5) <= 0.40 and scope.get("score", 0.5) >= 0.55:
            tension_score += 2
            elements.append(
                "Synthesis requested but consensus potential is low "
                "(risk of 'averaging' or false balance)."
            )

        if rlhf.get("score", 0.5) <= 0.35:
            tension_score += 2
            elements.append(
                "Low RLHF alignment score (ambiguity/hostility/conflicts) "
                "— needs clarification or reframing."
            )

        if rlhf.get("constraint_load", 0.0) >= 0.75 and scope.get("score", 0.0) >= 0.55:
            tension_score += 1
            elements.append(
                "Heavy constraint load + wide scope "
                "(constraint satisfaction vs completeness)."
            )

        if tension_score >= 7:
            level, description = (
                "Very High",
                "Severe pragmatic conflict — prioritisation and reframing required.",
            )
        elif tension_score >= 5:
            level, description = (
                "High",
                "Significant tension — careful structure and explicit assumptions needed.",
            )
        elif tension_score >= 3:
            level, description = (
                "Moderate",
                "Some tension — manageable with calibrated framing.",
            )
        elif tension_score >= 1:
            level, description = "Low", "Minor tension — typical trade-offs."
        else:
            level, description = (
                "Very Low",
                "Strong alignment — straightforward synthesis.",
            )

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                elements if elements else ["No significant pragmatic tension detected."]
            ),
            "guardrail_pressure": round(guardrail, 4),
        }

    # ── Reasoning construction ────────────────────────────────────────

    def _construct_reasoning(
        self,
        prompt: str,
        rlhf: Dict[str, Any],
        scope: Dict[str, Any],
        consensus: Dict[str, Any],
        task: Dict[str, Any],
        tension: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        parts: List[str] = [
            "GPT (OpenAI) lens: RLHF-tuned pragmatism + encyclopaedic synthesis.",
            (
                f"RLHF alignment: {rlhf['level']} — {rlhf['description']} "
                f"(score={rlhf['score']}, guardrail={rlhf['guardrail_pressure']})."
            ),
            (
                f"Encyclopaedic scope: {scope['level']} — {scope['description']} "
                f"(active_domains={len(scope['active_domains'])})."
            ),
            (
                f"Consensus potential: {consensus['level']} — {consensus['description']} "
                f"(score={consensus['score']})."
            ),
            (
                f"Task orientation: {task['level']} — {task['description']} "
                f"(suggested_format={task['suggested_format']})."
            ),
            f"Tension: {tension['level']} — {tension['description']}.",
            (
                "Pragmatic operating mode: (1) restate the goal + constraints, "
                "(2) surface assumptions + epistemic status, "
                "(3) provide a structured answer (map → drill-down), "
                "(4) offer alternatives/trade-offs instead of false precision, "
                "(5) highlight what to verify next if stakes are high."
            ),
        ]

        intent = str(context.get("intent", "")).strip()
        if intent:
            parts.append(f"Context hint: intent='{intent}'.")

        return " ".join(parts)


__all__ = ["GPTChatGPT"]
