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

Signals (from ensemble enrichment):
- safety = policy.score（Gate由来）
- freedom = base_freedom(action_type) × (1 - freedom_pressure)
- explain = rationale × author_reliability（Trace由来）
- brevity = 文字数
- coherence = consensus × (1 - conflict_penalty)
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence, Set, Tuple

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig, infer_safety_mode
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.domain.keys import (
    PO_CORE, POLICY, TRACEQ, FREEDOM_PRESSURE, AUTHOR_RELIABILITY,
    PARETO_DEBUG, FRONT, WEIGHTS, WINNER, CONFLICTS, MODE,
)
from po_core.ports.aggregator import AggregatorPort

from po_core.aggregator.conflict_resolver import analyze_conflicts


def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


# ── Signal readers ──────────────────────────────────────────────────────


def _get_float(extra: Mapping[str, Any], *path: str, default: float = 0.0) -> float:
    """Read nested float from extra dict."""
    cur: Any = extra
    for k in path:
        if not isinstance(cur, Mapping) or k not in cur:
            return default
        cur = cur[k]
    try:
        return float(cur)
    except Exception:
        return default


def _policy_score(p: Proposal) -> float:
    """Read policy.score from PO_CORE namespace (ensemble enrichment)."""
    extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
    pc = extra.get(PO_CORE, {})
    return _get_float(pc, POLICY, "score", default=0.5)


def _author_rel(p: Proposal) -> float:
    """Read trace_quality.author_reliability from PO_CORE namespace."""
    extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
    pc = extra.get(PO_CORE, {})
    return _get_float(pc, TRACEQ, AUTHOR_RELIABILITY, default=0.6)


def _freedom_pressure_from_extra(p: Proposal, tensors: TensorSnapshot) -> float:
    """Read freedom_pressure from proposal or fallback to tensors."""
    extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
    pc = extra.get(PO_CORE, {})
    fp_str = pc.get(FREEDOM_PRESSURE, "")
    if fp_str:
        try:
            return float(fp_str)
        except Exception:
            pass
    # fallback to tensors
    v = tensors.metrics.get("freedom_pressure")
    return float(v) if v is not None else 0.0


# ── Tokenization for consensus ──────────────────────────────────────────


def _norm(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "")).strip()
    return s.lower()


def _tokens(text: str) -> Set[str]:
    """Simple tokenizer for Japanese/English."""
    t = _norm(text)
    parts = re.findall(r"[a-z0-9_]+|[\u3040-\u30ff\u4e00-\u9fff]+", t)
    return {p for p in parts if len(p) >= 2}


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _consensus_scores(proposals: Sequence[Proposal]) -> Dict[str, float]:
    """Compute consensus (agreement) score for each proposal."""
    if len(proposals) <= 1:
        return {p.proposal_id: 1.0 for p in proposals}

    toks = {p.proposal_id: _tokens(p.content) for p in proposals}
    ids = [p.proposal_id for p in proposals]
    out: Dict[str, float] = {}
    for i, ida in enumerate(ids):
        s = 0.0
        for j, idb in enumerate(ids):
            if i == j:
                continue
            s += _jaccard(toks[ida], toks[idb])
        out[ida] = s / max(1, (len(ids) - 1))
    return out


# ── Objective computation ───────────────────────────────────────────────


@dataclass(frozen=True)
class ObjectiveVec:
    safety: float
    freedom: float
    explain: float
    brevity: float
    coherence: float

    def as_tuple(self) -> Tuple[float, float, float, float, float]:
        return (self.safety, self.freedom, self.explain, self.brevity, self.coherence)

    def to_dict(self) -> Dict[str, float]:
        return {
            "safety": self.safety,
            "freedom": self.freedom,
            "explain": self.explain,
            "brevity": self.brevity,
            "coherence": self.coherence,
        }


def _base_freedom(action_type: str) -> float:
    """Base freedom score by action type."""
    if action_type == "answer":
        return 1.0
    if action_type == "ask_clarification":
        return 0.55
    if action_type == "refuse":
        return 0.0
    return 0.2  # unknown


def _explain_score(p: Proposal) -> float:
    """
    Compute explanation quality from proposal content.
    """
    extra = dict(p.extra) if isinstance(p.extra, Mapping) else {}
    rationale = str(extra.get("rationale", "") or "")
    citations = extra.get("citations", [])
    c_n = len(citations) if isinstance(citations, list) else 0

    # assumption_tags contribute to explainability
    a = min(5, len(p.assumption_tags))
    score = 0.15 * a + (0.25 if rationale else 0.0) + 0.08 * min(5, c_n)
    return _clamp01(score)


def _brevity_score(p: Proposal, max_len: int = 2000) -> float:
    n = len(p.content or "")
    return _clamp01(1.0 - min(1.0, n / float(max_len)))


def _compute_objectives(
    p: Proposal,
    tensors: TensorSnapshot,
    conflict_penalty: float,
    consensus: float,
) -> ObjectiveVec:
    """
    Compute multi-objective scores using real signals.

    Args:
        p: Proposal with embedded signals
        tensors: Tensor snapshot (fallback for freedom_pressure)
        conflict_penalty: Penalty from ConflictResolver
        consensus: Agreement score with other proposals
    """
    # safety = policy.score (Gate verdict)
    safety = _policy_score(p)

    # freedom = base(action_type) × (1 - freedom_pressure)
    fp = _freedom_pressure_from_extra(p, tensors)
    base_free = _base_freedom(p.action_type)
    freedom = _clamp01(base_free * (1.0 - fp))

    # explain = rationale × author_reliability
    rationale = _explain_score(p)
    rel = _author_rel(p)
    explain = _clamp01(0.65 * rationale + 0.35 * rel)

    # brevity
    brevity = _brevity_score(p)

    # coherence = consensus × (1 - conflict_penalty)
    coherence = _clamp01(consensus * (1.0 - conflict_penalty))

    return ObjectiveVec(
        safety=_clamp01(safety),
        freedom=_clamp01(freedom),
        explain=_clamp01(explain),
        brevity=_clamp01(brevity),
        coherence=coherence,
    )


# ── Pareto front ────────────────────────────────────────────────────────


def _dominates(a: ObjectiveVec, b: ObjectiveVec) -> bool:
    at = a.as_tuple()
    bt = b.as_tuple()
    ge_all = all(x >= y for x, y in zip(at, bt))
    gt_any = any(x > y for x, y in zip(at, bt))
    return ge_all and gt_any


def pareto_front(vs: Sequence[ObjectiveVec]) -> List[int]:
    """
    Return indices of non-dominated solutions (maximize all objectives).
    O(n^2) but n<=39 is acceptable.
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


# ── Mode-based weights ──────────────────────────────────────────────────


def _weights_for_mode(mode: SafetyMode) -> Mapping[str, float]:
    """Weights for weighted-sum selection from Pareto front."""
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


# ── Aggregator ──────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ParetoAggregator(AggregatorPort):
    mode_config: SafetyModeConfig

    def aggregate(
        self,
        ctx: Context,
        intent: Intent,
        tensors: TensorSnapshot,
        proposals: Sequence[Proposal],
    ) -> Proposal:
        if not proposals:
            return Proposal(
                proposal_id=f"{ctx.request_id}:aggregate:none",
                action_type="refuse",
                content="No proposals generated.",
                confidence=0.0,
                assumption_tags=["no_proposals"],
                risk_tags=["system"],
            )

        # 1) Conflict analysis -> penalties
        report = analyze_conflicts(proposals)
        penalties = dict(report.penalties)

        # 2) Consensus scores
        cons = _consensus_scores(proposals)

        # 3) Compute objectives for each proposal
        vecs: List[ObjectiveVec] = []
        for p in proposals:
            pen = float(penalties.get(p.proposal_id, 0.0))
            consensus = cons.get(p.proposal_id, 0.5)
            vecs.append(_compute_objectives(p, tensors, pen, consensus))

        # 4) Pareto front
        front_idx = pareto_front(vecs)
        mode, fp = infer_safety_mode(tensors, self.mode_config)
        w = _weights_for_mode(mode)

        # 5) Select best from front using weighted score
        def key(i: int) -> Tuple[float, float, float, str]:
            v = vecs[i]
            return (_weighted_score(v, w), v.safety, v.coherence, proposals[i].proposal_id)

        best_i = max(front_idx, key=key)
        best = proposals[best_i]
        best_v = vecs[best_i]

        # 6) Build debug info for trace
        def _hash10(text: str) -> str:
            return hashlib.sha1((text or "").encode("utf-8")).hexdigest()[:10]

        front_rows = []
        for i in front_idx[:20]:  # limit to 20
            p = proposals[i]
            v = vecs[i]
            front_rows.append({
                "proposal_id": p.proposal_id,
                "action_type": p.action_type,
                "scores": v.to_dict(),
                "content_len": len(p.content or ""),
                "content_hash": _hash10(p.content or ""),
            })

        winner_payload = {
            "proposal_id": best.proposal_id,
            "action_type": best.action_type,
            "scores": best_v.to_dict(),
            "content_len": len(best.content or ""),
            "content_hash": _hash10(best.content or ""),
        }

        dbg = {
            MODE: mode.value,
            FREEDOM_PRESSURE: "" if fp is None else str(fp),
            WEIGHTS: dict(w),
            "front_size": len(front_idx),
            FRONT: front_rows,
            WINNER: winner_payload,
            CONFLICTS: {
                "n": len(report.conflicts),
                "kinds": report.summary.get("kinds", ""),
                "suggested_forced_action": report.suggested_forced_action or "",
                "top": [
                    {
                        "id": c.conflict_id,
                        "kind": c.kind,
                        "severity": c.severity,
                        "proposal_ids": c.proposal_ids[:6],
                    }
                    for c in report.conflicts[:5]
                ],
            },
        }

        # 7) Embed debug in PO_CORE namespace
        extra = dict(best.extra) if isinstance(best.extra, Mapping) else {}
        pc = dict(extra.get(PO_CORE, {}))
        pc[PARETO_DEBUG] = dbg

        # Also keep legacy "pareto" key for compatibility
        extra["pareto"] = {
            "mode": mode.value,
            "freedom_pressure": "" if fp is None else str(fp),
            "front_size": len(front_idx),
            "weights": dict(w),
            "scores": best_v.to_dict(),
            "conflicts": {
                "n": len(report.conflicts),
                "suggested_forced_action": report.suggested_forced_action or "",
                "kinds": report.summary.get("kinds", ""),
            },
        }
        extra[PO_CORE] = pc

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
