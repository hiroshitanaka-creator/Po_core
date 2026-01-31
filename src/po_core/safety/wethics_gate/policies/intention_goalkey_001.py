"""
WG.INT.GOALKEY.001 - Intent Goal Keyword Guard
==============================================

Detects dangerous keywords in intent/user_input.
- hard keywords -> REJECT
- soft keywords -> REVISE (ambiguous, request clarification)
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.safety.wethics_gate.policies.base import IntentionPolicy


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


@dataclass(frozen=True)
class IntentGoalKeywordGuardPolicy(IntentionPolicy):
    """
    WG.INT.GOALKEY.001
    - hard keywords -> REJECT
    - soft keywords -> REVISE
    """

    rule_id: str = "WG.INT.GOALKEY.001"
    priority: int = 10

    hard: Tuple[str, ...] = (
        # Clearly dangerous terms
        "爆弾", "殺人", "テロ", "麻薬", "自殺",
        "make a bomb", "terrorist", "kill someone", "suicide", "drug trafficking",
    )
    soft: Tuple[str, ...] = (
        # Context-dependent terms (can be harmless in some contexts)
        "ハッキング", "hack", "クラック", "crack",
        "銃", "weapon",
    )

    allow_phrases: Tuple[str, ...] = (
        # Reduce false positives for soft keywords
        "life hack", "ライフハック", "hackathon", "ハッカソン",
    )

    def check(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> Optional[SafetyVerdict]:
        fields: List[Tuple[str, str]] = []

        # Check user_input as well (catches danger before SolarWill processes it)
        fields.append(("ctx.user_input", ctx.user_input))
        for i, g in enumerate(intent.goals):
            fields.append((f"intent.goals[{i}]", g))
        for i, c in enumerate(intent.constraints):
            fields.append((f"intent.constraints[{i}]", c))

        # Check for allow phrases (only relaxes soft keywords)
        whole = _norm(" ".join([t for _, t in fields]))
        allow_soft = any(_norm(ap) in whole for ap in self.allow_phrases)

        # Hard keyword check (immediate REJECT)
        for field, text in fields:
            nt = _norm(text)
            for kw in self.hard:
                nkw = _norm(kw)
                if nkw and nkw in nt:
                    return SafetyVerdict(
                        decision=Decision.REJECT,
                        rule_ids=[self.rule_id],
                        reasons=[f"[{self.rule_id}] 危険な目的/要求を検出: '{kw}' ({field})"],
                        required_changes=["危険な目的/要求を除去し、無害な目的へ言い換えてください。"],
                        meta={"stage": "intent", "matched": kw, "field": field},
                    )

        # Soft keyword check (REVISE)
        if not allow_soft:
            for field, text in fields:
                nt = _norm(text)
                for kw in self.soft:
                    nkw = _norm(kw)
                    if nkw and nkw in nt:
                        return SafetyVerdict(
                            decision=Decision.REVISE,
                            rule_ids=[self.rule_id],
                            reasons=[f"[{self.rule_id}] 文脈により危険になり得る語を検出: '{kw}' ({field})"],
                            required_changes=[
                                "目的/要求が無害であることが明確になるよう、語を言い換えるか具体化してください。",
                                "安全/倫理上の制約（例: 違法行為をしない、他者に害を与えない）を明示してください。",
                            ],
                            meta={"stage": "intent", "matched": kw, "field": field},
                        )

        return None


__all__ = ["IntentGoalKeywordGuardPolicy"]
