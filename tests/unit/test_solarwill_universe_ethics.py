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

