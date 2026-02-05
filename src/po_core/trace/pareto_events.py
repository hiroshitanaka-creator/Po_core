"""
pareto_events.py - Pareto debug を TraceEvent へ確実に吐く helper
==================================================================

目的:
- ParetoAggregator が winner.extra["_po_core"]["pareto_debug"] に入れた payload を
  TraceEventへ確実に吐く
- trace 層に置くことで domain のみ参照（philosophers/tensors 禁止に抵触しない）
- ensemble.py から aggregate 直後に呼ばれる

DEPENDENCY RULES:
- domain のみ依存
- tracer は emit(TraceEvent) を持つ前提（InMemoryTracer など）
"""

from __future__ import annotations

from typing import Any, Mapping, TYPE_CHECKING

from po_core.domain.context import Context
from po_core.domain.proposal import Proposal
from po_core.domain.trace_event import TraceEvent
from po_core.domain.keys import (
    PO_CORE, PARETO_DEBUG, MODE, FREEDOM_PRESSURE, WEIGHTS, FRONT, WINNER, CONFLICTS,
)

if TYPE_CHECKING:
    from po_core.ports.trace import TracePort


def _as_dict(x: Any) -> dict:
    """安全に dict へ変換"""
    return dict(x) if isinstance(x, Mapping) else {}


def emit_pareto_debug_events(tracer: "TracePort", ctx: Context, winner: Proposal) -> None:
    """
    ParetoAggregator が winner.extra["_po_core"]["pareto_debug"] に入れた payload を
    TraceEventへ確実に吐く。

    Args:
        tracer: emit(TraceEvent) を持つ Tracer
        ctx: リクエストコンテキスト
        winner: Aggregator が返した勝者 Proposal

    Emits:
        - ConflictSummaryComputed: コンフリクト情報
        - ParetoFrontComputed: Pareto フロント情報
        - ParetoWinnerSelected: 勝者情報
    """
    extra = _as_dict(winner.extra)
    pc = _as_dict(extra.get(PO_CORE))
    dbg = _as_dict(pc.get(PARETO_DEBUG))
    if not dbg:
        return

    mode = str(dbg.get(MODE, ""))
    fp = str(dbg.get(FREEDOM_PRESSURE, ""))

    conflicts = _as_dict(dbg.get(CONFLICTS))
    front = dbg.get(FRONT, [])
    weights = _as_dict(dbg.get(WEIGHTS))
    winner_payload = _as_dict(dbg.get(WINNER))
    front_size = int(dbg.get("front_size", 0) or 0)

    # 1) ConflictSummaryComputed
    tracer.emit(
        TraceEvent.now(
            "ConflictSummaryComputed",
            ctx.request_id,
            {
                MODE: mode,
                FREEDOM_PRESSURE: fp,
                **conflicts,
            },
        )
    )

    # 2) ParetoFrontComputed
    tracer.emit(
        TraceEvent.now(
            "ParetoFrontComputed",
            ctx.request_id,
            {
                MODE: mode,
                FREEDOM_PRESSURE: fp,
                WEIGHTS: weights,
                "front_size": front_size,
                FRONT: list(front)[:20],  # payload 肥大防止
            },
        )
    )

    # 3) ParetoWinnerSelected
    tracer.emit(
        TraceEvent.now(
            "ParetoWinnerSelected",
            ctx.request_id,
            {
                MODE: mode,
                FREEDOM_PRESSURE: fp,
                WINNER: winner_payload,
            },
        )
    )


__all__ = ["emit_pareto_debug_events"]
