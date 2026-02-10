"""
decision_compare.py - Shadow Pareto A/B比較の監査イベント
========================================================

目的:
- Shadow Pareto A/B評価の結果を監査ログに残す
- 「mainとshadowで最終決定がどう変わったか」を事実として記録
- raw content は載せない（decision_events と同じ方針）

DEPENDENCY RULES:
- domain のみ依存
- tracer は emit(TraceEvent) を持つ前提
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

from po_core.domain.context import Context
from po_core.domain.proposal import Proposal
from po_core.domain.trace_event import TraceEvent
from po_core.trace.decision_events import proposal_fingerprint

if TYPE_CHECKING:
    from po_core.ports.trace import TracePort


def _as_dict(x: Any) -> dict:
    """安全に dict へ変換"""
    return dict(x) if isinstance(x, Mapping) else {}


def _to_float(x: Any) -> float | None:
    """安全に float へ変換（失敗時は None）"""
    try:
        return float(x)
    except Exception:
        return None


def emit_decision_comparison(
    tracer: "TracePort",
    ctx: Context,
    *,
    main_candidate: Proposal,
    main_final: Proposal,
    shadow_candidate: Proposal,
    shadow_final: Proposal,
) -> None:
    """
    Shadow Pareto A/B評価の比較結果を監査ログに残す。

    Args:
        tracer: emit(TraceEvent) を持つ Tracer
        ctx: リクエストコンテキスト
        main_candidate: main Pareto の候補
        main_final: main の最終決定（Gate後）
        shadow_candidate: shadow Pareto の候補
        shadow_final: shadow の最終決定（Gate後）

    Emits:
        DecisionComparisonComputed: A/B比較の事実
    """
    mc = proposal_fingerprint(main_candidate)
    mf = proposal_fingerprint(main_final)
    sc = proposal_fingerprint(shadow_candidate)
    sf = proposal_fingerprint(shadow_final)

    def changed(a: dict, b: dict, k: str) -> bool:
        """2つの指紋で特定キーが異なるか"""
        return str(a.get(k, "")) != str(b.get(k, ""))

    payload = {
        "main": {"candidate": mc, "final": mf},
        "shadow": {"candidate": sc, "final": sf},
        "diff": {
            "candidate_action_changed": changed(mc, sc, "action_type"),
            "candidate_content_changed": changed(mc, sc, "content_hash"),
            "final_action_changed": changed(mf, sf, "action_type"),
            "final_content_changed": changed(mf, sf, "content_hash"),
            "main_config_version": str(mc.get("pareto_config_version", "")),
            "shadow_config_version": str(sc.get("pareto_config_version", "")),
            "main_config_source": str(mc.get("pareto_config_source", "")),
            "shadow_config_source": str(sc.get("pareto_config_source", "")),
        },
    }

    # policy_score delta（取れたら）
    mps = _to_float(mf.get("policy_score"))
    sps = _to_float(sf.get("policy_score"))
    if mps is not None and sps is not None:
        payload["diff"]["final_policy_score_delta"] = sps - mps

    tracer.emit(TraceEvent.now("DecisionComparisonComputed", ctx.request_id, payload))


__all__ = ["emit_decision_comparison"]
