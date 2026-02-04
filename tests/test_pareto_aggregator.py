"""
Test Pareto Aggregator
======================

Paretoフロント + mode重み付き選択のテスト。
"""

from datetime import datetime, timezone

from po_core.aggregator.pareto import ParetoAggregator, pareto_front, ObjectiveVec
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.proposal import Proposal
from po_core.domain.safety_mode import SafetyMode, SafetyModeConfig
from po_core.domain.tensor_snapshot import TensorSnapshot


def test_pareto_selects_and_annotates():
    """Paretoが選択し、extraにpareto情報を付与する"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r1", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.2})

    ps = [
        Proposal("p1", "answer", "短い答え", 0.6),
        Proposal("p2", "ask_clarification", "質問します", 0.7),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)
    assert "pareto" in dict(out.extra)


def test_pareto_front_basic():
    """pareto_front が非支配集合を返す"""
    vecs = [
        ObjectiveVec(safety=0.8, freedom=0.2, explain=0.5, brevity=0.5, coherence=0.5),
        ObjectiveVec(safety=0.5, freedom=0.8, explain=0.5, brevity=0.5, coherence=0.5),
        ObjectiveVec(safety=0.3, freedom=0.3, explain=0.5, brevity=0.5, coherence=0.5),  # dominated
    ]
    front = pareto_front(vecs)
    assert 0 in front
    assert 1 in front
    assert 2 not in front  # dominated by both 0 and 1


def test_pareto_critical_prefers_safety():
    """CRITICAL mode では safety 重視"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r1", datetime.now(timezone.utc), "x")
    # freedom_pressure=0.9 → CRITICAL mode
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.9})

    ps = [
        Proposal("safe", "refuse", "できません", 0.9),
        Proposal("free", "answer", "自由に答えます", 0.9),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)
    # CRITICAL では refuse が選ばれやすい
    assert out.action_type == "refuse"


def test_pareto_normal_allows_answer():
    """NORMAL mode では answer が許容される"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r1", datetime.now(timezone.utc), "x")
    # freedom_pressure=0.2 → NORMAL mode
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.2})

    ps = [
        Proposal("ans", "answer", "答えます", 0.8),
        Proposal("ref", "refuse", "できません", 0.3),
    ]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)
    # NORMAL では answer が選ばれやすい
    assert out.action_type == "answer"


def test_pareto_empty_proposals():
    """空のproposalsでrefuseを返す"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r1", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={})

    out = agg.aggregate(ctx, Intent.neutral(), tensors, [])
    assert out.action_type == "refuse"
    assert "no_proposals" in out.assumption_tags


def test_pareto_extra_contains_scores():
    """extra["pareto"]["scores"] が含まれる"""
    cfg = SafetyModeConfig(warn=0.6, critical=0.85, missing_mode=SafetyMode.WARN)
    agg = ParetoAggregator(cfg)

    ctx = Context("r1", datetime.now(timezone.utc), "x")
    tensors = TensorSnapshot(datetime.now(timezone.utc), metrics={"freedom_pressure": 0.4})

    ps = [Proposal("p1", "answer", "テスト", 0.7)]

    out = agg.aggregate(ctx, Intent.neutral(), tensors, ps)
    pareto_info = dict(out.extra).get("pareto", {})
    assert "scores" in pareto_info
    scores = pareto_info["scores"]
    assert "safety" in scores
    assert "freedom" in scores
    assert "coherence" in scores
