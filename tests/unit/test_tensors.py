"""
Unit tests for Po_core tensor implementations.

Tests cover:
- Base Tensor abstract class behavior
- FreedomPressureTensor computation and analysis
- SemanticProfile evolution tracking
- BlockedTensor entry management and categorization
"""

import numpy as np
import pytest

from po_core.tensors import (
    BlockedTensor,
    FreedomPressureTensor,
    SemanticProfile,
    Tensor,
)
from po_core.tensors.blocked_tensor import BlockedEntry


class ConcreteTensor(Tensor):
    """Concrete implementation of Tensor for testing."""

    def compute(self, value: float = 1.0) -> np.ndarray:
        """Simple compute implementation."""
        self.data = np.full(self.dimensions, value, dtype=np.float64)
        return self.data


class TestTensorBase:
    """Tests for the base Tensor class."""

    def test_tensor_initialization(self):
        """Test basic tensor initialization."""
        tensor = ConcreteTensor("test_tensor", dimensions=5)

        assert tensor.name == "test_tensor"
        assert tensor.dimensions == 5
        assert tensor.data.shape == (5,)
        assert np.allclose(tensor.data, np.zeros(5))

    def test_tensor_with_initial_value_scalar(self):
        """Test tensor initialization with scalar value."""
        tensor = ConcreteTensor("test", dimensions=3, initial_value=0.5)

        assert np.allclose(tensor.data, np.array([0.5, 0.5, 0.5]))

    def test_tensor_with_initial_value_array(self):
        """Test tensor initialization with array."""
        initial = np.array([1.0, 2.0, 3.0])
        tensor = ConcreteTensor("test", dimensions=3, initial_value=initial)

        assert np.allclose(tensor.data, initial)

    def test_tensor_norm(self):
        """Test tensor norm computation."""
        tensor = ConcreteTensor("test", dimensions=3)
        tensor.compute(2.0)  # [2, 2, 2]

        norm = tensor.norm()
        expected = np.sqrt(12)  # sqrt(4 + 4 + 4)
        assert np.isclose(norm, expected)

    def test_tensor_normalize(self):
        """Test tensor normalization."""
        tensor = ConcreteTensor("test", dimensions=3)
        tensor.data = np.array([3.0, 4.0, 0.0])

        normalized = tensor.normalize()
        assert np.isclose(np.linalg.norm(normalized), 1.0)

    def test_tensor_dot_product(self):
        """Test tensor dot product."""
        tensor1 = ConcreteTensor("t1", dimensions=3)
        tensor1.data = np.array([1.0, 2.0, 3.0])

        tensor2 = ConcreteTensor("t2", dimensions=3)
        tensor2.data = np.array([4.0, 5.0, 6.0])

        dot = tensor1.dot(tensor2)
        assert dot == 32.0  # 1*4 + 2*5 + 3*6

    def test_tensor_distance(self):
        """Test tensor distance computation."""
        tensor1 = ConcreteTensor("t1", dimensions=3)
        tensor1.data = np.array([0.0, 0.0, 0.0])

        tensor2 = ConcreteTensor("t2", dimensions=3)
        tensor2.data = np.array([3.0, 4.0, 0.0])

        distance = tensor1.distance(tensor2)
        assert distance == 5.0  # sqrt(9 + 16)

    def test_tensor_to_dict(self):
        """Test tensor serialization to dictionary."""
        tensor = ConcreteTensor("test", dimensions=3, metadata={"key": "value"})
        tensor.compute(1.5)

        tensor_dict = tensor.to_dict()

        assert tensor_dict["name"] == "test"
        assert tensor_dict["dimensions"] == 3
        assert tensor_dict["metadata"]["key"] == "value"
        assert np.allclose(tensor_dict["data"], [1.5, 1.5, 1.5])


class TestFreedomPressureTensor:
    """Tests for FreedomPressureTensor."""

    def test_freedom_pressure_initialization(self):
        """Test FreedomPressureTensor initialization."""
        fp = FreedomPressureTensor()

        assert fp.name == "Freedom_Pressure"
        assert fp.dimensions == 6
        assert len(fp.dimension_names) == 6
        assert "choice_weight" in fp.dimension_names

    def test_compute_basic_prompt(self):
        """Test computing freedom pressure from basic prompt."""
        fp = FreedomPressureTensor()
        prompt = "What should I do with my life?"

        result = fp.compute(prompt)

        assert result.shape == (6,)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)

    def test_compute_with_ethical_keywords(self):
        """Test freedom pressure with ethical keywords."""
        fp = FreedomPressureTensor()
        prompt = "Is it ethical to lie to protect someone?"

        result = fp.compute(prompt)

        # Should have high ethical stakes
        ethical_idx = fp.dimension_names.index("ethical_stakes")
        assert result[ethical_idx] > 0.5

    def test_compute_with_urgent_keywords(self):
        """Test freedom pressure with temporal urgency."""
        fp = FreedomPressureTensor()
        prompt = "I need to decide immediately what to do!"

        result = fp.compute(prompt)

        # Should have high temporal urgency
        urgency_idx = fp.dimension_names.index("temporal_urgency")
        assert result[urgency_idx] > 0.5

    def test_compute_with_philosopher_perspectives(self):
        """Test computing with philosopher perspectives."""
        fp = FreedomPressureTensor()
        prompt = "What is freedom?"

        perspectives = [
            {
                "philosopher": "sartre",
                "response": "Freedom is radical responsibility for our choices",
                "confidence": 0.9,
                "reasoning": "Existential freedom",
            },
            {
                "philosopher": "nietzsche",
                "response": "Freedom is will to power",
                "confidence": 0.85,
                "reasoning": "Übermensch concept",
            },
        ]

        result = fp.compute(prompt, philosopher_perspectives=perspectives)

        assert result.shape == (6,)
        # With perspectives, should have non-zero values
        assert np.any(result > 0.0)

    def test_get_pressure_summary(self):
        """Test getting pressure summary."""
        fp = FreedomPressureTensor()
        fp.compute("Should I take this job?")

        summary = fp.get_pressure_summary()

        assert "total_pressure" in summary
        assert "max_dimension" in summary
        assert "dimensions" in summary
        assert len(summary["dimensions"]) == 6

    def test_to_dict_includes_dimension_names(self):
        """Test that to_dict includes dimension names."""
        fp = FreedomPressureTensor()
        fp.compute("test prompt")

        tensor_dict = fp.to_dict()

        assert "dimension_names" in tensor_dict
        assert "pressure_summary" in tensor_dict


class TestSemanticProfile:
    """Tests for SemanticProfile."""

    def test_semantic_profile_initialization(self):
        """Test SemanticProfile initialization."""
        sp = SemanticProfile()

        assert sp.name == "Semantic_Profile"
        assert sp.dimensions == 6
        assert len(sp.dimension_names) == 6
        assert "abstract_level" in sp.dimension_names
        assert len(sp.history) == 0

    def test_compute_from_text(self):
        """Test computing semantic profile from text."""
        sp = SemanticProfile()
        text = "Freedom is the fundamental condition of human existence"

        result = sp.compute(text)

        assert result.shape == (6,)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)
        assert len(sp.history) == 1

    def test_evolution_tracking(self):
        """Test semantic evolution tracking."""
        sp = SemanticProfile()

        # First text - abstract
        sp.compute("Being is the fundamental question")

        # Second text - concrete
        sp.compute("I need to buy groceries today")

        assert len(sp.history) == 2
        assert len(sp.evolution_delta) == 1

        # Check that evolution delta was computed
        delta = sp.evolution_delta[0]
        assert delta.shape == (6,)

    def test_get_evolution_trajectory(self):
        """Test getting evolution trajectory."""
        sp = SemanticProfile()

        sp.compute("Abstract philosophical concept")
        sp.compute("Concrete practical example")
        sp.compute("Mixed abstract and concrete")

        trajectory = sp.get_evolution_trajectory()

        assert trajectory.shape == (3, 6)
        assert np.allclose(trajectory[0], sp.history[0])

    def test_get_semantic_delta(self):
        """Test getting semantic delta."""
        sp = SemanticProfile()

        sp.compute("First text")
        sp.compute("Second text")

        delta = sp.get_semantic_delta(0, 1)
        assert delta.shape == (6,)

    def test_get_semantic_delta_invalid_step(self):
        """Test getting semantic delta with invalid step."""
        sp = SemanticProfile()
        sp.compute("First text")

        with pytest.raises(ValueError):
            sp.get_semantic_delta(0, 5)

    def test_get_total_evolution(self):
        """Test getting total evolution."""
        sp = SemanticProfile()

        sp.compute("First")
        sp.compute("Second")
        sp.compute("Third")

        total_evolution = sp.get_total_evolution()
        assert isinstance(total_evolution, float)
        assert total_evolution >= 0.0

    def test_compute_with_perspectives(self):
        """Test computing from philosopher perspectives."""
        sp = SemanticProfile()

        perspectives = [
            {"philosopher": "heidegger", "response": "Dasein is Being-in-the-world"},
            {"philosopher": "sartre", "response": "Existence precedes essence"},
        ]

        result = sp.compute_from_perspectives(perspectives)

        assert result.shape == (6,)
        assert len(sp.history) == 1

    def test_to_dict_includes_evolution(self):
        """Test that to_dict includes evolution data."""
        sp = SemanticProfile()
        sp.compute("First")
        sp.compute("Second")

        sp_dict = sp.to_dict()

        assert "dimension_names" in sp_dict
        assert "history_length" in sp_dict
        assert "total_evolution" in sp_dict


class TestBlockedTensor:
    """Tests for BlockedTensor."""

    def test_blocked_tensor_initialization(self):
        """Test BlockedTensor initialization."""
        bt = BlockedTensor()

        assert bt.name == "Blocked_Tensor"
        assert bt.dimensions == 6
        assert len(bt.dimension_names) == 6
        assert len(bt.blocked_entries) == 0

    def test_add_blocked_entry_with_parameters(self):
        """Test adding blocked entry with parameters."""
        bt = BlockedTensor()

        bt.add_blocked_entry(
            content="Unethical suggestion",
            reason="This is harmful and unethical",
            philosopher="sartre",
            alternative="Ethical alternative",
            intensity=0.9,
        )

        assert len(bt.blocked_entries) == 1
        entry = bt.blocked_entries[0]
        assert entry.content == "Unethical suggestion"
        assert entry.philosopher == "sartre"

    def test_add_blocked_entry_with_entry_object(self):
        """Test adding pre-constructed BlockedEntry."""
        bt = BlockedTensor()

        entry = BlockedEntry(
            content="Test content", reason="Test reason", philosopher="nietzsche"
        )

        bt.add_blocked_entry(entry=entry)

        assert len(bt.blocked_entries) == 1
        assert bt.blocked_entries[0].content == "Test content"

    def test_add_blocked_entry_missing_args(self):
        """Test that adding entry without required args raises error."""
        bt = BlockedTensor()

        with pytest.raises(ValueError):
            bt.add_blocked_entry()

    def test_compute_aggregates_intensities(self):
        """Test that compute aggregates intensities by category."""
        bt = BlockedTensor()

        # Add entries in different categories
        bt.add_blocked_entry(content="A", reason="unethical behavior", intensity=0.8)
        bt.add_blocked_entry(content="B", reason="illogical argument", intensity=0.6)
        bt.add_blocked_entry(
            content="C", reason="another unethical action", intensity=0.4
        )

        result = bt.compute()

        # Should have non-zero values
        assert np.any(result > 0.0)
        # All values should be normalized (between 0 and 1)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)

    def test_classify_blocking_reason(self):
        """Test classification of blocking reasons."""
        bt = BlockedTensor()

        # Ethical filtering
        ethical_idx = bt._classify_blocking_reason("This is unethical and wrong")
        assert ethical_idx == bt.dimension_names.index("ethical_filtering")

        # Logical filtering
        logical_idx = bt._classify_blocking_reason("This is contradictory")
        assert logical_idx == bt.dimension_names.index("logical_filtering")

        # Harmful filtering
        harmful_idx = bt._classify_blocking_reason("This is harmful and dangerous")
        assert harmful_idx == bt.dimension_names.index("harmful_filtering")

    def test_get_blocked_count(self):
        """Test getting blocked entry count."""
        bt = BlockedTensor()

        assert bt.get_blocked_count() == 0

        bt.add_blocked_entry(content="A", reason="test")
        bt.add_blocked_entry(content="B", reason="test")

        assert bt.get_blocked_count() == 2

    def test_get_blocked_by_philosopher(self):
        """Test filtering entries by philosopher."""
        bt = BlockedTensor()

        bt.add_blocked_entry(
            content="A", reason="test", philosopher="sartre", intensity=0.5
        )
        bt.add_blocked_entry(
            content="B", reason="test", philosopher="nietzsche", intensity=0.5
        )
        bt.add_blocked_entry(
            content="C", reason="test", philosopher="sartre", intensity=0.5
        )

        sartre_entries = bt.get_blocked_by_philosopher("sartre")
        assert len(sartre_entries) == 2
        assert all(e.philosopher == "sartre" for e in sartre_entries)

    def test_get_blocked_by_category(self):
        """Test filtering entries by category."""
        bt = BlockedTensor()

        bt.add_blocked_entry(content="A", reason="unethical")
        bt.add_blocked_entry(content="B", reason="illogical")
        bt.add_blocked_entry(content="C", reason="also unethical")

        ethical_entries = bt.get_blocked_by_category("ethical_filtering")
        assert len(ethical_entries) == 2

    def test_get_blocked_by_category_invalid(self):
        """Test that invalid category raises error."""
        bt = BlockedTensor()

        with pytest.raises(ValueError):
            bt.get_blocked_by_category("invalid_category")

    def test_get_blocking_summary(self):
        """Test getting blocking summary statistics."""
        bt = BlockedTensor()

        bt.add_blocked_entry(
            content="A", reason="unethical", philosopher="sartre", intensity=0.8
        )
        bt.add_blocked_entry(
            content="B", reason="illogical", philosopher="nietzsche", intensity=0.6
        )

        summary = bt.get_blocking_summary()

        assert summary["total_blocked"] == 2
        assert "by_category" in summary
        assert "by_philosopher" in summary
        assert "average_intensity" in summary
        assert summary["average_intensity"] == pytest.approx(0.7)

    def test_get_trace_of_absence(self):
        """Test getting Derridean trace of absence."""
        bt = BlockedTensor()

        bt.add_blocked_entry(content="Blocked content", reason="test reason")

        trace = bt.get_trace_of_absence()

        assert len(trace) == 1
        assert isinstance(trace[0], dict)
        assert trace[0]["content"] == "Blocked content"

    def test_to_dict_includes_blocking_data(self):
        """Test that to_dict includes comprehensive blocking data."""
        bt = BlockedTensor()
        bt.add_blocked_entry(content="Test", reason="unethical")

        bt_dict = bt.to_dict()

        assert "dimension_names" in bt_dict
        assert "blocked_count" in bt_dict
        assert "blocking_summary" in bt_dict
        assert "trace_of_absence" in bt_dict
        assert bt_dict["blocked_count"] == 1


class TestBlockedEntry:
    """Tests for BlockedEntry dataclass."""

    def test_blocked_entry_creation(self):
        """Test creating a BlockedEntry."""
        entry = BlockedEntry(
            content="test content",
            reason="test reason",
            philosopher="sartre",
            alternative="alternative",
            intensity=0.75,
        )

        assert entry.content == "test content"
        assert entry.reason == "test reason"
        assert entry.philosopher == "sartre"
        assert entry.alternative == "alternative"
        assert entry.intensity == 0.75
        assert entry.timestamp is not None

    def test_blocked_entry_intensity_clamping(self):
        """Test that intensity is clamped to [0, 1]."""
        entry1 = BlockedEntry(content="A", reason="B", intensity=1.5)
        assert entry1.intensity == 1.0

        entry2 = BlockedEntry(content="A", reason="B", intensity=-0.5)
        assert entry2.intensity == 0.0

    def test_blocked_entry_to_dict(self):
        """Test converting BlockedEntry to dictionary."""
        entry = BlockedEntry(
            content="test", reason="reason", philosopher="nietzsche", intensity=0.5
        )

        entry_dict = entry.to_dict()

        assert entry_dict["content"] == "test"
        assert entry_dict["reason"] == "reason"
        assert entry_dict["philosopher"] == "nietzsche"
        assert entry_dict["intensity"] == 0.5
        assert "timestamp" in entry_dict
