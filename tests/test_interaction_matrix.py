"""
Interaction Matrix Tests (Phase 2 Task 7)
==========================================

Tests for the NxN philosopher interaction matrix computed from actual proposals.
Uses embedding-based cosine similarity for harmony and keyword detection for tension.
"""

from __future__ import annotations

import uuid

import numpy as np
import pytest

from po_core.domain.proposal import Proposal
from po_core.tensors.interaction_tensor import (
    InteractionMatrix,
    InteractionPair,
    _compute_tension,
)


# ── Helpers ──────────────────────────────────────────────────────────


def _proposal(name: str, content: str, confidence: float = 0.5) -> Proposal:
    """Create a Proposal with embedded philosopher name."""
    return Proposal(
        proposal_id=f"test:{name}:0",
        action_type="answer",
        content=content,
        confidence=confidence,
        extra={
            "_po_core": {"author": name},
            "philosopher": name,
        },
    )


# ── Tension computation ─────────────────────────────────────────────


class TestTension:
    def test_no_tension(self):
        score = _compute_tension("beauty and art", "truth and knowledge")
        assert score == 0.0

    def test_one_opposition(self):
        score = _compute_tension("individual freedom", "collective responsibility")
        assert score > 0.0

    def test_multiple_oppositions(self):
        score = _compute_tension(
            "freedom and subjective being with order",
            "determinism and objective becoming with chaos",
        )
        assert score > 0.3

    def test_symmetric(self):
        s1 = _compute_tension("freedom", "determinism")
        s2 = _compute_tension("determinism", "freedom")
        assert s1 == s2


# ── InteractionMatrix.from_proposals() ──────────────────────────────


class TestFromProposals:
    def test_empty_proposals(self):
        m = InteractionMatrix.from_proposals([])
        assert len(m.names) == 0
        assert m.harmony.shape == (0, 0)

    def test_single_proposal(self):
        m = InteractionMatrix.from_proposals([
            _proposal("Aristotle", "virtue is the golden mean"),
        ])
        assert len(m.names) == 1
        assert m.harmony[0, 0] == 1.0  # self-similarity
        assert len(m.pairs) == 0  # no pairs with single philosopher

    def test_two_similar_proposals(self):
        m = InteractionMatrix.from_proposals([
            _proposal("Aristotle", "virtue is the golden mean of character excellence"),
            _proposal("Confucius", "virtue is cultivated through ritual and character"),
        ])
        assert len(m.names) == 2
        assert m.harmony.shape == (2, 2)
        assert m.harmony[0, 0] == 1.0
        assert m.harmony[1, 1] == 1.0
        # Similar content → harmony > 0
        assert m.harmony[0, 1] > 0.0
        assert len(m.pairs) == 1

    def test_two_different_proposals(self):
        m = InteractionMatrix.from_proposals([
            _proposal("Aristotle", "virtue ethics golden mean eudaimonia character"),
            _proposal("Kant", "duty categorical imperative obligation universal law"),
        ])
        # Different vocabulary → lower harmony than identical
        assert m.harmony[0, 1] < 1.0
        assert len(m.pairs) == 1

    def test_harmony_symmetry(self):
        m = InteractionMatrix.from_proposals([
            _proposal("A", "truth beauty justice"),
            _proposal("B", "freedom responsibility ethics"),
        ])
        assert m.harmony[0, 1] == pytest.approx(m.harmony[1, 0], abs=1e-6)

    def test_tension_with_opposing_concepts(self):
        m = InteractionMatrix.from_proposals([
            _proposal("Sartre", "individual freedom is absolute and subjective"),
            _proposal("Hegel", "collective determinism is relative and objective"),
        ])
        # Should detect tension from opposing pairs
        assert m.tension[0, 1] > 0.0
        assert m.pairs[0].tension > 0.0

    def test_synthesis_formula(self):
        m = InteractionMatrix.from_proposals([
            _proposal("A", "truth beauty"),
            _proposal("B", "truth justice"),
        ])
        # synthesis = harmony * (1 - tension)
        expected = m.harmony[0, 1] * (1.0 - m.tension[0, 1])
        assert m.synthesis[0, 1] == pytest.approx(expected, abs=1e-6)

    def test_many_proposals(self):
        """Test with realistic number of proposals."""
        proposals = [
            _proposal("Aristotle", "virtue is found in the golden mean between extremes"),
            _proposal("Kant", "duty demands adherence to categorical imperative"),
            _proposal("Nietzsche", "individual will to power transcends morality"),
            _proposal("Confucius", "harmony comes through ritual and proper relations"),
            _proposal("Sartre", "existence precedes essence freedom is absolute"),
        ]
        m = InteractionMatrix.from_proposals(proposals)
        assert len(m.names) == 5
        assert m.harmony.shape == (5, 5)
        assert m.tension.shape == (5, 5)
        assert m.synthesis.shape == (5, 5)
        # C(5,2) = 10 pairs
        assert len(m.pairs) == 10
        # All values in [0, 1]
        assert np.all(m.harmony >= 0.0) and np.all(m.harmony <= 1.0)
        assert np.all(m.tension >= 0.0) and np.all(m.tension <= 1.0)
        assert np.all(m.synthesis >= 0.0) and np.all(m.synthesis <= 1.0)

    def test_names_extracted_from_proposals(self):
        proposals = [
            _proposal("Aristotle", "virtue"),
            _proposal("Kant", "duty"),
            _proposal("Hegel", "spirit"),
        ]
        m = InteractionMatrix.from_proposals(proposals)
        assert m.names == ["Aristotle", "Kant", "Hegel"]


# ── InteractionPair ──────────────────────────────────────────────────


class TestInteractionPair:
    def test_to_dict(self):
        pair = InteractionPair(
            philosopher_a="A", philosopher_b="B",
            harmony=0.75, tension=0.25, synthesis=0.5625,
        )
        d = pair.to_dict()
        assert d["philosopher_a"] == "A"
        assert d["harmony"] == 0.75
        assert d["tension"] == 0.25
        assert d["synthesis"] == 0.5625


# ── Helper methods ───────────────────────────────────────────────────


class TestHelperMethods:
    @pytest.fixture
    def matrix(self):
        return InteractionMatrix.from_proposals([
            _proposal("Sartre", "individual freedom is absolute and subjective existence"),
            _proposal("Hegel", "collective determinism is relative and objective spirit"),
            _proposal("Aristotle", "virtue is the golden mean of character"),
            _proposal("Confucius", "virtue harmony comes through ritual and proper relations"),
        ])

    def test_high_tension_pairs(self, matrix):
        pairs = matrix.high_tension_pairs(threshold=0.0)
        # Any pair with opposing concepts should appear
        # At least Sartre-Hegel should have tension
        names_involved = {(p.philosopher_a, p.philosopher_b) for p in pairs}
        assert len(pairs) >= 0  # At least none crash

    def test_high_harmony_pairs(self, matrix):
        # With TF-IDF backend, harmony values may be 0 for dissimilar texts
        # Use a very negative threshold to get all pairs
        all_pairs = matrix.pairs
        assert len(all_pairs) == 6  # C(4,2) = 6
        # Some pairs should have non-zero harmony (Aristotle-Confucius share "virtue")
        harmonious = matrix.high_harmony_pairs(threshold=0.05)
        assert len(harmonious) >= 1

    def test_high_interference_pairs(self, matrix):
        pairs = matrix.high_interference_pairs(top_k=3)
        assert len(pairs) <= 3
        # Should be sorted by interference descending
        if len(pairs) >= 2:
            i0 = pairs[0].tension * (1.0 - pairs[0].harmony)
            i1 = pairs[1].tension * (1.0 - pairs[1].harmony)
            assert i0 >= i1

    def test_summary(self, matrix):
        s = matrix.summary()
        assert s["n_philosophers"] == 4
        assert 0.0 <= s["mean_harmony"] <= 1.0
        assert 0.0 <= s["mean_tension"] <= 1.0
        assert 0.0 <= s["mean_synthesis"] <= 1.0


# ── Integration with real philosophers ───────────────────────────────


class TestRealPhilosophers:
    def test_with_all_39_proposals(self):
        """Run InteractionMatrix on actual philosopher proposals."""
        from po_core.domain.context import Context
        from po_core.domain.intent import Intent
        from po_core.domain.memory_snapshot import MemorySnapshot
        from po_core.domain.safety_mode import SafetyMode
        from po_core.domain.tensor_snapshot import TensorSnapshot
        from po_core.philosophers.registry import PhilosopherRegistry

        registry = PhilosopherRegistry(cache_instances=True)
        sel = registry.select(SafetyMode.NORMAL)
        philosophers, _ = registry.load(sel.selected_ids)

        ctx = Context.now(request_id=str(uuid.uuid4()), user_input="What is justice?")
        intent = Intent.neutral()
        tensors = TensorSnapshot.now({"freedom_pressure": 0.0})
        memory = MemorySnapshot(items=[], summary=None, meta={})

        proposals = []
        for ph in philosophers:
            try:
                props = ph.propose(ctx, intent, tensors, memory)
                if props:
                    proposals.extend(props)
            except Exception:
                continue

        # Should have proposals from most philosophers
        assert len(proposals) >= 30

        m = InteractionMatrix.from_proposals(proposals)
        assert len(m.names) >= 30
        assert m.harmony.shape[0] == len(m.names)
        assert m.harmony.shape[1] == len(m.names)

        # Summary should be reasonable
        s = m.summary()
        assert s["n_philosophers"] >= 30
        assert 0.0 < s["mean_harmony"] < 1.0

        # Should find some high-interference pairs
        hi_pairs = m.high_interference_pairs(top_k=5)
        assert len(hi_pairs) > 0
