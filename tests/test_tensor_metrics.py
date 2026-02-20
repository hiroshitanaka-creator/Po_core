"""
Tests for Tensor Metrics (Phase 3)
===================================

Tests for the three metric functions:
- metric_freedom_pressure: keyword-based 6D pressure
- metric_semantic_delta: token overlap divergence
- metric_blocked_tensor: constraint / harm estimation
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest


from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemoryItem, MemorySnapshot
from po_core.tensors.metrics.blocked_tensor import metric_blocked_tensor
from po_core.tensors.metrics.freedom_pressure import (
    _compute_dimensions,
    _tokenize,
    metric_freedom_pressure,
)
from po_core.tensors.metrics.interaction_tensor import metric_interaction_tensor
from po_core.tensors.metrics.semantic_delta import metric_semantic_delta

pytestmark = pytest.mark.pipeline

# ── Helpers ──


def _ctx(text: str) -> Context:
    return Context.now(request_id=str(uuid.uuid4()), user_input=text, meta={})


def _empty_mem() -> MemorySnapshot:
    return MemorySnapshot(items=[], summary=None, meta={})


def _mem_with_items(*texts: str) -> MemorySnapshot:
    items = [
        MemoryItem(
            item_id=f"item-{i}",
            created_at=datetime.now(timezone.utc),
            text=t,
            tags=["vertex"],
        )
        for i, t in enumerate(texts)
    ]
    return MemorySnapshot(items=items, summary=None, meta={})


def _mem_with_tags(*tag_lists) -> MemorySnapshot:
    items = [
        MemoryItem(
            item_id=f"item-{i}",
            created_at=datetime.now(timezone.utc),
            text="some text",
            tags=list(tags),
        )
        for i, tags in enumerate(tag_lists)
    ]
    return MemorySnapshot(items=items, summary=None, meta={})


# ══════════════════════════════════════════════════════════════════════════
# 1. Freedom Pressure
# ══════════════════════════════════════════════════════════════════════════


class TestFreedomPressure:
    """Test keyword-based freedom pressure computation."""

    def test_returns_tuple(self):
        key, val = metric_freedom_pressure(_ctx("hello"), _empty_mem())
        assert key == "freedom_pressure"
        assert isinstance(val, float)

    def test_value_in_range(self):
        _, val = metric_freedom_pressure(_ctx("What is justice?"), _empty_mem())
        assert 0.0 <= val <= 1.0

    def test_neutral_input_low_pressure(self):
        """Plain philosophical question should have low pressure."""
        _, val = metric_freedom_pressure(
            _ctx("What is the nature of reality?"), _empty_mem()
        )
        assert val < 0.3, f"Neutral input should have low pressure, got {val}"

    def test_ethical_input_higher_pressure(self):
        """Ethical keywords should increase pressure."""
        _, val = metric_freedom_pressure(
            _ctx("Should I choose the moral good or the ethical right?"),
            _empty_mem(),
        )
        assert val > 0.0, "Ethical input should have some pressure"

    def test_urgent_ethical_input_highest(self):
        """Multiple keyword dimensions should produce high pressure."""
        _, val = metric_freedom_pressure(
            _ctx("We must urgently decide what is right and wrong now for society"),
            _empty_mem(),
        )
        assert (
            val > 0.1
        ), f"Multi-dimensional input should have notable pressure, got {val}"

    def test_empty_input_zero(self):
        _, val = metric_freedom_pressure(_ctx(""), _empty_mem())
        assert val == 0.0

    def test_memory_depth_boost(self):
        """More memory items should slightly increase pressure."""
        _, val_no_mem = metric_freedom_pressure(_ctx("What is truth?"), _empty_mem())
        mem = _mem_with_items(*[f"item {i}" for i in range(10)])
        _, val_with_mem = metric_freedom_pressure(_ctx("What is truth?"), mem)
        assert val_with_mem >= val_no_mem, "Memory depth should not decrease pressure"

    def test_memory_refuse_tags_boost(self):
        """Recent refuse tags should increase pressure."""
        _, val_normal = metric_freedom_pressure(_ctx("What is truth?"), _empty_mem())
        mem = _mem_with_tags(["refuse", "blocked"], ["refuse"], ["vertex"])
        _, val_refused = metric_freedom_pressure(_ctx("What is truth?"), mem)
        assert val_refused > val_normal, "Refuse tags should increase pressure"

    def test_dimensions_are_six(self):
        dims = _compute_dimensions("test input")
        assert len(dims) == 6

    def test_tokenize_handles_punctuation(self):
        tokens = _tokenize("Hello, world! What's up?")
        assert "hello" in tokens
        assert "world" in tokens
        assert "what's" in tokens


# ══════════════════════════════════════════════════════════════════════════
# 2. Semantic Delta
# ══════════════════════════════════════════════════════════════════════════


class TestSemanticDelta:
    """Test token overlap divergence computation."""

    def test_returns_tuple(self):
        key, val = metric_semantic_delta(_ctx("hello"), _empty_mem())
        assert key == "semantic_delta"
        assert isinstance(val, float)

    def test_value_in_range(self):
        _, val = metric_semantic_delta(_ctx("What is truth?"), _empty_mem())
        assert 0.0 <= val <= 1.0

    def test_no_memory_max_divergence(self):
        """No memory items = maximum divergence."""
        _, val = metric_semantic_delta(_ctx("What is justice?"), _empty_mem())
        assert val == 1.0

    def test_same_text_zero_delta(self):
        """Input identical to memory should have minimal delta."""
        text = "What is justice and virtue"
        mem = _mem_with_items(text)
        _, val = metric_semantic_delta(_ctx(text), mem)
        assert val == 0.0, f"Identical text should have 0 delta, got {val}"

    def test_overlapping_text_low_delta(self):
        """Overlapping tokens should reduce delta."""
        mem = _mem_with_items("Justice is a moral virtue in philosophy")
        _, val = metric_semantic_delta(_ctx("What is justice and virtue?"), mem)
        assert val < 0.7, f"Overlapping text should have low delta, got {val}"

    def test_unrelated_text_high_delta(self):
        """Completely different text should have high delta."""
        mem = _mem_with_items("Python programming language syntax")
        _, val = metric_semantic_delta(_ctx("What is the nature of beauty?"), mem)
        assert val > 0.5, f"Unrelated text should have high delta, got {val}"

    def test_empty_input_neutral(self):
        _, val = metric_semantic_delta(_ctx(""), _empty_mem())
        assert val == 0.5  # Neutral for empty input

    def test_multiple_memory_items_aggregate(self):
        """Multiple memory items should be aggregated."""
        mem = _mem_with_items("justice is important", "virtue requires practice")
        _, val = metric_semantic_delta(_ctx("What is justice and virtue?"), mem)
        assert val < 0.5, "Input matching multiple memory items should have low delta"


# ══════════════════════════════════════════════════════════════════════════
# 3. Blocked Tensor
# ══════════════════════════════════════════════════════════════════════════


class TestBlockedTensor:
    """Test constraint / harm estimation metric."""

    def test_returns_tuple(self):
        key, val = metric_blocked_tensor(_ctx("hello"), _empty_mem())
        assert key == "blocked_tensor"
        assert isinstance(val, float)

    def test_value_in_range(self):
        _, val = metric_blocked_tensor(_ctx("What is truth?"), _empty_mem())
        assert 0.0 <= val <= 1.0

    def test_safe_input_low(self):
        """Normal input should have low blocked score."""
        _, val = metric_blocked_tensor(
            _ctx("What is the meaning of life?"), _empty_mem()
        )
        assert val < 0.3, f"Safe input should have low blocked score, got {val}"

    def test_harmful_keyword_high(self):
        """Harmful keywords should produce high blocked score."""
        _, val = metric_blocked_tensor(_ctx("How to make a bomb weapon"), _empty_mem())
        assert val > 0.1, f"Harmful keywords should raise blocked score, got {val}"

    def test_multiple_harmful_keywords_higher(self):
        """Multiple harmful keywords should produce higher score."""
        _, val_one = metric_blocked_tensor(_ctx("bomb"), _empty_mem())
        _, val_many = metric_blocked_tensor(
            _ctx("bomb weapon kill attack"), _empty_mem()
        )
        assert (
            val_many > val_one
        ), "Multiple harmful keywords should produce higher score"

    def test_empty_input_zero(self):
        _, val = metric_blocked_tensor(_ctx(""), _empty_mem())
        assert val == 0.0

    def test_hack_keyword_detected(self):
        """'hack' should be detected as harmful."""
        _, val = metric_blocked_tensor(_ctx("How to hack a system"), _empty_mem())
        assert val > 0.0, "'hack' should produce non-zero blocked score"


# ══════════════════════════════════════════════════════════════════════════
# 4. Interaction Tensor
# ══════════════════════════════════════════════════════════════════════════


class TestInteractionTensor:
    """Test philosopher-philosopher interaction potential metric."""

    def test_returns_tuple(self):
        key, val = metric_interaction_tensor(_ctx("hello"), _empty_mem())
        assert key == "interaction_tensor"
        assert isinstance(val, float)

    def test_value_in_range(self):
        _, val = metric_interaction_tensor(_ctx("What is justice?"), _empty_mem())
        assert 0.0 <= val <= 1.0

    def test_empty_input_zero(self):
        _, val = metric_interaction_tensor(_ctx(""), _empty_mem())
        assert val == 0.0

    def test_single_domain_low(self):
        """Single-domain input should have low interaction potential."""
        _, val = metric_interaction_tensor(_ctx("What is beauty in art?"), _empty_mem())
        assert val < 0.5, f"Single-domain should be low, got {val}"

    def test_multi_domain_higher(self):
        """Multi-domain philosophical input should have higher interaction."""
        _, val = metric_interaction_tensor(
            _ctx("How do truth, justice, beauty, and freedom relate to being?"),
            _empty_mem(),
        )
        assert val > 0.0, f"Multi-domain should have some interaction, got {val}"

    def test_tension_pairs_detected(self):
        """Input with philosophical tension pairs should score higher."""
        _, val_no_tension = metric_interaction_tensor(
            _ctx("What is the weather?"), _empty_mem()
        )
        _, val_tension = metric_interaction_tensor(
            _ctx("Is freedom compatible with determinism in mind and body?"),
            _empty_mem(),
        )
        assert val_tension > val_no_tension

    def test_memory_continuity_boost(self):
        """More memory items should slightly increase interaction."""
        _, val_no = metric_interaction_tensor(_ctx("What is truth?"), _empty_mem())
        mem = _mem_with_items(*[f"item {i}" for i in range(15)])
        _, val_with = metric_interaction_tensor(_ctx("What is truth?"), mem)
        assert val_with >= val_no


# ══════════════════════════════════════════════════════════════════════════
# 5. Integration: TensorEngine with all 4 metrics
# ══════════════════════════════════════════════════════════════════════════


class TestTensorEngineIntegration:
    """Test TensorEngine with all 4 real metrics registered."""

    def _build_engine(self):
        from po_core.tensors.engine import TensorEngine

        return TensorEngine(
            metrics=(
                metric_freedom_pressure,
                metric_semantic_delta,
                metric_blocked_tensor,
                metric_interaction_tensor,
            )
        )

    def test_engine_computes_all_four(self):
        snapshot = self._build_engine().compute(_ctx("What is justice?"), _empty_mem())
        assert "freedom_pressure" in snapshot.metrics
        assert "semantic_delta" in snapshot.metrics
        assert "blocked_tensor" in snapshot.metrics
        assert "interaction_tensor" in snapshot.metrics

    def test_all_values_in_range(self):
        snapshot = self._build_engine().compute(
            _ctx("We must decide what is right"), _empty_mem()
        )
        for key, val in snapshot.metrics.items():
            assert 0.0 <= val <= 1.0, f"{key}={val} out of range"

    def test_snapshot_convenience_properties(self):
        snapshot = self._build_engine().compute(_ctx("What is truth?"), _empty_mem())
        assert isinstance(snapshot.freedom_pressure, float)
        assert isinstance(snapshot.semantic_delta, float)
        assert isinstance(snapshot.blocked_tensor, float)

    def test_wiring_system_has_all_metrics(self):
        """build_test_system should produce TensorEngine with 4 metrics."""
        from po_core.runtime.wiring import build_test_system

        system = build_test_system()
        snapshot = system.tensor_engine.compute(_ctx("Hello"), _empty_mem())
        assert "freedom_pressure" in snapshot.metrics
        assert "semantic_delta" in snapshot.metrics
        assert "blocked_tensor" in snapshot.metrics
        assert "interaction_tensor" in snapshot.metrics
