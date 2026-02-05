"""
test_pareto_debug_payload.py
============================

ParetoAggregator が winner.extra["_po_core"]["pareto_debug"] に
debug payload を必ず埋め込むことを検証する。
"""

from datetime import datetime, timezone

from po_core.aggregator.pareto import ParetoAggregator
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.keys import PO_CORE, PARETO_DEBUG, FRONT, WINNER, CONFLICTS, WEIGHTS, MODE, FREEDOM_PRESSURE
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
from po_core.domain.tensor_snapshot import TensorSnapshot


def test_pareto_aggregator_attaches_pareto_debug_payload():
    """ParetoAggregator が pareto_debug を winner に埋め込む"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r1", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.2})

    ps = [
        Proposal("p1", "answer", "短い答え", confidence=0.6),
        Proposal("p2", "ask_clarification", "確認質問", confidence=0.7),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)

    extra = dict(out.extra)
    pc = dict(extra.get(PO_CORE, {}))
    dbg = pc.get(PARETO_DEBUG)

    assert isinstance(dbg, dict)
    assert FRONT in dbg
    assert WINNER in dbg
    assert CONFLICTS in dbg
    assert dbg[WINNER]["proposal_id"] == out.proposal_id


def test_pareto_debug_has_mode_and_freedom_pressure():
    """pareto_debug に mode と freedom_pressure が含まれる"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r2", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.75})

    ps = [
        Proposal("p1", "answer", "答え", confidence=0.8),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)

    pc = dict(out.extra.get(PO_CORE, {}))
    dbg = pc.get(PARETO_DEBUG, {})

    assert MODE in dbg
    assert FREEDOM_PRESSURE in dbg
    assert dbg[MODE] in ("normal", "warn", "critical", "unknown")
    assert dbg[FREEDOM_PRESSURE] != ""


def test_pareto_debug_front_has_content_hash():
    """front の各エントリに content_hash が含まれる"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r3", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.3})

    ps = [
        Proposal("p1", "answer", "テスト回答A", confidence=0.6),
        Proposal("p2", "answer", "テスト回答B", confidence=0.7),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)

    pc = dict(out.extra.get(PO_CORE, {}))
    dbg = pc.get(PARETO_DEBUG, {})
    front = dbg.get(FRONT, [])

    assert len(front) >= 1
    for row in front:
        assert "content_hash" in row
        assert isinstance(row["content_hash"], str)
        assert len(row["content_hash"]) == 10  # sha1[:10]


def test_pareto_debug_winner_has_scores():
    """winner payload に scores が含まれる"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r4", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.1})

    ps = [
        Proposal("p1", "answer", "勝者の回答", confidence=0.9),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)

    pc = dict(out.extra.get(PO_CORE, {}))
    dbg = pc.get(PARETO_DEBUG, {})
    winner = dbg.get(WINNER, {})

    assert "scores" in winner
    scores = winner["scores"]
    assert "safety" in scores
    assert "freedom" in scores
    assert "explain" in scores
    assert "brevity" in scores
    assert "coherence" in scores


def test_pareto_debug_conflicts_has_top():
    """conflicts に top リストが含まれる"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r5", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.2})

    ps = [
        Proposal("p1", "answer", "はい、可能です", confidence=0.8),
        Proposal("p2", "refuse", "いいえ、拒否します", confidence=0.7),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)

    pc = dict(out.extra.get(PO_CORE, {}))
    dbg = pc.get(PARETO_DEBUG, {})
    conflicts = dbg.get(CONFLICTS, {})

    assert "n" in conflicts
    assert "top" in conflicts
    assert isinstance(conflicts["top"], list)


def test_pareto_debug_weights_present():
    """pareto_debug に weights が含まれる"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r6", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.9})

    ps = [
        Proposal("p1", "answer", "回答", confidence=0.7),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)

    pc = dict(out.extra.get(PO_CORE, {}))
    dbg = pc.get(PARETO_DEBUG, {})

    assert WEIGHTS in dbg
    weights = dbg[WEIGHTS]
    assert "safety" in weights
    assert "freedom" in weights
