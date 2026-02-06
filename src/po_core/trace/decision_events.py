"""
decision_events.py - 最終決定の監査イベント helper
===================================================

目的:
- 「候補（Pareto/哲学者）→ 最終（Gate後）」の変遷を監査ログに残す
- DecisionEmitted: 最終的に外へ出した決定
- SafetyOverrideApplied: Gate により上書きされた事実

SECURITY NOTE:
- Gate前の提案は危険な内容を含み得るので、生contentは載せない
- hash/len/action_type のみ（漏洩耐性）

DEPENDENCY RULES:
- domain のみ依存
- tracer は emit(TraceEvent) を持つ前提
"""

from __future__ import annotations

import hashlib
from typing import Any, Mapping, Optional, TYPE_CHECKING

from po_core.domain.context import Context
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import SafetyVerdict
from po_core.domain.trace_event import TraceEvent
from po_core.domain.keys import (
    PO_CORE,
    POLICY,
    TRACEQ,
    PARETO_DEBUG,
    FREEDOM_PRESSURE,
    AUTHOR,
    AUTHOR_RELIABILITY,
)

if TYPE_CHECKING:
    from po_core.ports.trace import TracePort


def _as_dict(x: Any) -> dict:
    """安全に dict へ変換"""
    return dict(x) if isinstance(x, Mapping) else {}


def _hash10(text: str) -> str:
    """content の指紋（sha1[:10]）"""
    return hashlib.sha1((text or "").encode("utf-8")).hexdigest()[:10]


def _pareto_cfg_from(p: Optional[Proposal]) -> tuple[str, str]:
    """Proposalから pareto config_version/source を抽出（なければ空文字列）"""
    if p is None:
        return "", ""
    extra = _as_dict(p.extra)
    pc = _as_dict(extra.get(PO_CORE))
    dbg = _as_dict(pc.get(PARETO_DEBUG))
    return str(dbg.get("config_version", "")), str(dbg.get("config_source", ""))


def proposal_fingerprint(p: Proposal) -> dict:
    """
    監査用の最小指紋。

    WARNING:
        Gate前の提案は危険な内容を含み得るので、生contentは載せない（hash/lenのみ）。
        これで「説明力」と「漏洩耐性」を両立する。
    """
    extra = _as_dict(p.extra)
    pc = _as_dict(extra.get(PO_CORE))
    pol = _as_dict(pc.get(POLICY))
    tq = _as_dict(pc.get(TRACEQ))
    dbg = _as_dict(pc.get(PARETO_DEBUG))

    return {
        "proposal_id": p.proposal_id,
        "action_type": p.action_type,
        "confidence": float(p.confidence),
        "content_len": len(p.content or ""),
        "content_hash": _hash10(p.content or ""),
        # optional signals (enriched by ensemble)
        "author": str(pc.get(AUTHOR, "")),
        "freedom_pressure": str(pc.get(FREEDOM_PRESSURE, "")),
        "policy_decision": str(pol.get("decision", "")),
        "policy_score": str(pol.get("score", "")),
        "author_reliability": str(tq.get(AUTHOR_RELIABILITY, "")),
        # pareto config meta (A/B comparison用)
        "pareto_config_version": str(dbg.get("config_version", "")),
        "pareto_config_source": str(dbg.get("config_source", "")),
    }


def verdict_summary(v: SafetyVerdict) -> dict:
    """SafetyVerdict の監査用サマリ"""
    return {
        "decision": v.decision.value,
        "rule_ids": list(v.rule_ids)[:12],
        "required_changes_n": len(v.required_changes),
        "reasons_n": len(v.reasons),
        "meta": dict(v.meta),
    }


def emit_safety_override_applied(
    tracer: "TracePort",
    ctx: Context,
    *,
    variant: str = "main",
    stage: str,
    reason: str,
    from_proposal: Proposal,
    to_proposal: Proposal,
    verdict: SafetyVerdict,
) -> None:
    """
    「候補（Pareto/哲学者/集約）→ 最終（縮退/置換）」の上書きを監査ログに残す。

    Args:
        tracer: emit(TraceEvent) を持つ Tracer
        ctx: リクエストコンテキスト
        variant: "main" or "shadow" (A/B評価用)
        stage: "intent" or "action"
        reason: 上書き理由（例: "gate_revise", "gate_reject"）
        from_proposal: 上書き前の候補
        to_proposal: 上書き後の提案（fallback）
        verdict: Gate の判定結果

    Emits:
        SafetyOverrideApplied: 安全上書きの事実
    """
    tracer.emit(
        TraceEvent.now(
            "SafetyOverrideApplied",
            ctx.request_id,
            {
                "variant": variant,
                "stage": stage,
                "reason": reason,
                "from": proposal_fingerprint(from_proposal),
                "to": proposal_fingerprint(to_proposal),
                "gate": verdict_summary(verdict),
            },
        )
    )


def emit_decision_emitted(
    tracer: "TracePort",
    ctx: Context,
    *,
    variant: str = "main",
    stage: str,
    origin: str,
    final: Proposal,
    candidate: Optional[Proposal] = None,
    gate_verdict: Optional[SafetyVerdict] = None,
    degraded: bool = False,
) -> None:
    """
    最終的に外へ出した決定（= "プロダクションの事実"）を必ず残す。

    Args:
        tracer: emit(TraceEvent) を持つ Tracer
        ctx: リクエストコンテキスト
        variant: "main" or "shadow" (A/B評価用)
        stage: "intent" or "action"
        origin: 決定の出所（"pareto", "safety_fallback", "intent_gate_fallback" 等）
        final: 最終的に出力される提案
        candidate: 元の候補（あれば）
        gate_verdict: Gate の判定結果（あれば）
        degraded: 縮退したかどうか

    Emits:
        DecisionEmitted: 最終決定の事実
    """
    cfg_ver, cfg_src = _pareto_cfg_from(candidate)  # candidate優先（finalがfallbackでも追える）

    payload: dict = {
        "variant": variant,
        "stage": stage,
        "origin": origin,
        "degraded": bool(degraded),
        "pareto_config_version": cfg_ver,
        "pareto_config_source": cfg_src,
        "final": proposal_fingerprint(final),
        "candidate": proposal_fingerprint(candidate) if candidate is not None else None,
    }
    if gate_verdict is not None:
        payload["gate"] = verdict_summary(gate_verdict)

    tracer.emit(TraceEvent.now("DecisionEmitted", ctx.request_id, payload))


__all__ = [
    "proposal_fingerprint",
    "verdict_summary",
    "emit_safety_override_applied",
    "emit_decision_emitted",
]
