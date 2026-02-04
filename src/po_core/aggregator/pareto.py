"""
Pareto Aggregator - 多目的最適化による提案選択
==============================================

目的:
- proposals を 多目的（Freedom/Safety/Explain/Brevity/Coherence）でスコア化
- Paretoフロント（非支配集合）を作り、そこから mode（SafetyMode）で最終選択
- ConflictResolver のペナルティを "coherence" として反映

DEPENDENCY RULES:
- domain + conflict_resolver のみ依存
- Paretoフロントは O(n^2) だが n<=39 程度なら十分
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Mapping, Sequence, Tuple

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.ports.aggregator import AggregatorPort

from po_core.aggregator.conflict_resolver import analyze_conflicts


def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


@dataclass(frozen=True)
class ObjectiveVec:
    safety: float
    freedom: float
    explain: float
    brevity: float
    coherence: float

    def as_tuple(self) -> Tuple[float, float, float, float, float]:
        return (self.safety, self.freedom, self.explain, self.brevity, self.coherence)


def _action_base(p: Proposal) -> Tuple[float, float]:
    """
    (safety_base, freedom_base)
    """
    if p.action_type == "refuse":
        return 1.0, 0.0
    if p.action_type == "ask_clarification":
        return 0.85, 0.55
    if p.action_type == "answer":
        return 0.55, 1.0
    # 未知は危険扱い
    return 0.20, 0.20


def _explain_score(p: Proposal) -> float:
    """
    依存ゼロで説明性を推定する。
    - philosophers が extra["rationale"] や extra["citations"] を入れてくれたら伸びる
    """
    extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
    rationale = str(extra.get("rationale", "") or "")
    citations = extra.get("citations", [])
    c_n = len(citations) if isinstance(citations, list) else 0

    # assumption_tags は「説明」になり得る（ただし多すぎるとノイズ）
    a = min(5, len(p.assumption_tags))
    score = 0.15 * a + (0.25 if rationale else 0.0) + 0.08 * min(5, c_n)
    return _clamp01(score)


def _brevity_score(p: Proposal, max_len: int = 2000) -> float:
    n = len(p.content or "")
    return _clamp01(1.0 - min(1.0, n / float(max_len)))


def _compute_objectives(p: Proposal, conflict_penalty: float) -> ObjectiveVec:
    sb, fb = _action_base(p)

    # risk_tags は安全性を削る（Gateの前段で締める）
    safety = sb - 0.12 * len(p.risk_tags)
    # confidence は自由度をわずかに押し上げる
    freedom = fb + 0.10 * (p.confidence - 0.5)

    explain = _explain_score(p)
    brevity = _brevity_score(p)

    # coherence: 矛盾に巻き込まれてるほど下がる
    coherence = _clamp01(1.0 - conflict_penalty)

    return ObjectiveVec(
        safety=_clamp01(safety),
        freedom=_clamp01(freedom),
        explain=_clamp01(explain),
        brevity=_clamp01(brevity),
        coherence=coherence,
    )


def _dominates(a: ObjectiveVec, b: ObjectiveVec) -> bool:
    at = a.as_tuple()
    bt = b.as_tuple()
    ge_all = all(x >= y for x, y in zip(at, bt))
    gt_any = any(x > y for x, y in zip(at, bt))
    return ge_all and gt_any


def pareto_front(vs: Sequence[ObjectiveVec]) -> List[int]:
    """
    非支配集合のインデックスを返す（maximize）。
    O(n^2) だが n<=39 程度なら十分。
    """
    n = len(vs)
    front: List[int] = []
    for i in range(n):
        dominated = False
        for j in range(n):
            if i == j:
                continue
            if _dominates(vs[j], vs[i]):
                dominated = True
                break
        if not dominated:
            front.append(i)
    return front


def _weights_for_mode(mode: SafetyMode) -> Mapping[str, float]:
    # ここが「群知能の哲学」。まずは保守寄りに締める。
    if mode == SafetyMode.CRITICAL:
        return {"safety": 0.55, "freedom": 0.00, "explain": 0.20, "brevity": 0.15, "coherence": 0.30}
    if mode in (SafetyMode.WARN, SafetyMode.UNKNOWN):
        return {"safety": 0.40, "freedom": 0.10, "explain": 0.20, "brevity": 0.15, "coherence": 0.25}
    return {"safety": 0.25, "freedom": 0.30, "explain": 0.20, "brevity": 0.10, "coherence": 0.15}


def _weighted_score(v: ObjectiveVec, w: Mapping[str, float]) -> float:
    return (
        v.safety * w.get("safety", 0.0)
        + v.freedom * w.get("freedom", 0.0)
        + v.explain * w.get("explain", 0.0)
        + v.brevity * w.get("brevity", 0.0)
        + v.coherence * w.get("coherence", 0.0)
    )


@dataclass(frozen=True)
class ParetoAggregator(AggregatorPort):
    mode_config: SafetyModeConfig

    def aggregate(self, ctx: Context, intent: Intent, tensors: TensorSnapshot, proposals: Sequence[Proposal]) -> Proposal:
        if not proposals:
            return Proposal(
                proposal_id=f"{ctx.request_id}:aggregate:none",
                action_type="refuse",
                content="No proposals generated.",
                confidence=0.0,
                assumption_tags=["no_proposals"],
                risk_tags=["system"],
            )

        # 1) conflicts -> penalties
        report = analyze_conflicts(proposals)
        penalties = dict(report.penalties)

        # 2) objectives
        vecs: List[ObjectiveVec] = []
        for p in proposals:
            pen = float(penalties.get(p.proposal_id, 0.0))
            vecs.append(_compute_objectives(p, pen))

        # 3) pareto front
        front_idx = pareto_front(vecs)
        mode, fp = infer_safety_mode(tensors, self.mode_config)
        w = _weights_for_mode(mode)

        # 4) frontから mode重みで選ぶ
        def key(i: int) -> Tuple[float, float, float, str]:
            v = vecs[i]
            # 主：重み付き、補助：安全性、整合性、最後に安定なID
            return (_weighted_score(v, w), v.safety, v.coherence, proposals[i].proposal_id)

        best_i = max(front_idx, key=key)
        best = proposals[best_i]
        best_v = vecs[best_i]

        extra = dict(best.extra) if isinstance(best.extra, Mapping) else {}
        extra["pareto"] = {
            "mode": mode.value,
            "freedom_pressure": "" if fp is None else str(fp),
            "front_size": len(front_idx),
            "weights": dict(w),
            "scores": {
                "safety": best_v.safety,
                "freedom": best_v.freedom,
                "explain": best_v.explain,
                "brevity": best_v.brevity,
                "coherence": best_v.coherence,
            },
            "conflicts": {
                "n": len(report.conflicts),
                "suggested_forced_action": report.suggested_forced_action or "",
                "kinds": report.summary.get("kinds", ""),
            },
        }

        # NOTE: Proposal は frozen なので新しく作る
        return Proposal(
            proposal_id=best.proposal_id,
            action_type=best.action_type,
            content=best.content,
            confidence=best.confidence,
            assumption_tags=list(best.assumption_tags),
            risk_tags=list(best.risk_tags),
            extra=extra,
        )


__all__ = [
    "ObjectiveVec",
    "ParetoAggregator",
    "pareto_front",
]
