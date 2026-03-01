from __future__ import annotations

import uuid

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.tensors.freedom_pressure_v2 import FreedomPressureV2
from po_core.tensors.metrics.freedom_pressure import metric_freedom_pressure


def _ctx(text: str) -> Context:
    return Context.now(request_id=str(uuid.uuid4()), user_input=text, meta={})


def _empty_mem() -> MemorySnapshot:
    return MemorySnapshot(items=[], summary=None, meta={})


def test_freedom_pressure_v1_japanese_is_non_zero() -> None:
    text = "私はどちらを選ぶべきでしょうか。社会への影響と責任があり、今すぐ判断したいです。"
    _, score = metric_freedom_pressure(_ctx(text), _empty_mem())
    assert score > 0.0


def test_freedom_pressure_v2_japanese_has_non_zero_and_variance() -> None:
    fp = FreedomPressureV2(model_name="__nonexistent_model_to_force_keyword_fallback__")
    fp.reset_state()
    result = fp.compute_v2(
        "どの選択肢を選ぶべきか迷っています。倫理と責任、社会的影響を考える必要があります。"
    )

    values = list(result.values.values())
    assert any(v > 0.0 for v in values)
    assert len({round(v, 4) for v in values}) > 1


def test_freedom_pressure_v2_english_regression_case() -> None:
    fp = FreedomPressureV2(model_name="__nonexistent_model_to_force_keyword_fallback__")
    fp.reset_state()
    result = fp.compute_v2(
        "I must decide quickly because this is urgent and affects other people in society."
    )

    assert result.values["choice"] > 0.0
    assert result.values["urgency"] > 0.0
    assert result.values["social"] > 0.0
