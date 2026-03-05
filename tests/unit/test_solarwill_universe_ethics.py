"""SolarWill 宇宙ルール倫理（NORMAL）契約テスト。"""

from __future__ import annotations

from datetime import datetime, timezone

from po_core.autonomy.solarwill.engine import SolarWillEngine
from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.safety_mode import SafetyModeConfig
from po_core.domain.tensor_snapshot import TensorSnapshot


def test_compute_intent_normal_freezes_universe_ethics_axioms() -> None:
    """NORMAL 時の Intent が宇宙ルール倫理の公理を満たす。"""
    engine = SolarWillEngine(config=SafetyModeConfig(warn=0.30, critical=0.50))
    ctx = Context(
        request_id="req-solarwill-ethics-normal",
        created_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
        user_input="倫理方針を確認したい",
        meta={"entry": "unit-test"},
    )
    tensors = TensorSnapshot(
        computed_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
        metrics={
            "freedom_pressure": 0.10,
            "blocked_tensor": 0.20,
            "semantic_delta": 0.20,
        },
        snapshot_id="snap-solarwill-ethics-normal",
    )

    intent, meta = engine.compute_intent(ctx, tensors, MemorySnapshot.empty())

    assert meta["mode"] == "normal"

    assert any("生存構造" in goal and "歪み" in goal for goal in intent.goals)

    assert any(
        ("歪み" in constraint or "生存構造" in constraint or "破壊" in constraint)
        and any(kw in constraint for kw in ("与えない", "支援しない"))
        for constraint in intent.constraints
    )

    assert any(
        all(kw in constraint for kw in ("ライフサイクル", "弱肉強食", "自然"))
        for constraint in intent.constraints
    )


def test_compute_intent_warn_degrades_to_clarification_first() -> None:
    """WARN 時は確認質問優先の安全側 Intent に縮退する。"""
    engine = SolarWillEngine(config=SafetyModeConfig(warn=0.30, critical=0.50))
    ctx = Context(
        request_id="req-solarwill-ethics-warn",
        created_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
        user_input="危険そうだが判断に必要情報が不足している",
        meta={"entry": "unit-test"},
    )
    tensors = TensorSnapshot(
        computed_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
        metrics={
            "freedom_pressure": 0.31,
            "blocked_tensor": 0.20,
            "semantic_delta": 0.20,
        },
        snapshot_id="snap-solarwill-ethics-warn",
    )

    intent, meta = engine.compute_intent(ctx, tensors, MemorySnapshot.empty())

    assert meta["mode"] == "warn"
    assert any("確認" in goal and "質問" in goal for goal in intent.goals)
    assert "違法行為をしない" in intent.constraints
    assert "他者に害を与えない" in intent.constraints
    assert any("不確実性" in constraint and "確認質問" in constraint for constraint in intent.constraints)


def test_compute_intent_critical_degrades_to_refusal_stop_minimal_guidance() -> None:
    """CRITICAL 時は拒否/停止/最小案内の安全縮退を固定する。"""
    engine = SolarWillEngine(config=SafetyModeConfig(warn=0.30, critical=0.50))
    ctx = Context(
        request_id="req-solarwill-ethics-critical",
        created_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
        user_input="重大な歪みを誘発する要求",
        meta={"entry": "unit-test"},
    )
    tensors = TensorSnapshot(
        computed_at=datetime(2026, 2, 22, tzinfo=timezone.utc),
        metrics={
            "freedom_pressure": 0.50,
            "blocked_tensor": 0.20,
            "semantic_delta": 0.20,
        },
        snapshot_id="snap-solarwill-ethics-critical",
    )

    intent, meta = engine.compute_intent(ctx, tensors, MemorySnapshot.empty())

    assert meta["mode"] == "critical"
    assert any(
        ("拒否" in goal or "中止" in goal) and "最小限" in goal
        for goal in intent.goals
    )
    assert "違法行為をしない" in intent.constraints
    assert "他者に害を与えない" in intent.constraints
    assert any("安全" in constraint and "提案しない" in constraint for constraint in intent.constraints)
