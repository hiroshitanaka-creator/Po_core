"""
Semantic Delta Metric Tests
============================

Tests for the embedding-based semantic delta metric.
Tests are backend-agnostic: they work with sentence-transformers,
sklearn TF-IDF, or the basic fallback.
"""

from __future__ import annotations

import numpy as np
import pytest

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemoryItem, MemorySnapshot
from po_core.tensors.metrics.semantic_delta import (
    _compute_idf,
    _compute_tf,
    _cosine_similarity,
    _tfidf_vector,
    _tokenize,
    cosine_sim,
    encode_texts,
    get_backend,
    metric_semantic_delta,
)

# ── Helper factories ─────────────────────────────────────────────────


def _ctx(text: str) -> Context:
    from datetime import datetime, timezone

    return Context(
        request_id="test-001",
        user_input=text,
        created_at=datetime.now(timezone.utc),
    )


def _memory(*texts: str) -> MemorySnapshot:
    from datetime import datetime, timezone

    items = [
        MemoryItem(item_id=f"mem-{i}", created_at=datetime.now(timezone.utc), text=t)
        for i, t in enumerate(texts)
    ]
    return MemorySnapshot(items=items)


def _empty_memory() -> MemorySnapshot:
    return MemorySnapshot(items=[])


# ── Backend detection ────────────────────────────────────────────────


class TestBackend:
    def test_backend_detected(self):
        backend = get_backend()
        assert backend in ("sbert", "tfidf", "basic")

    def test_encode_texts_returns_2d_array(self):
        result = encode_texts(["hello world", "foo bar"])
        assert isinstance(result, np.ndarray)
        assert result.ndim == 2
        assert result.shape[0] == 2

    def test_encode_texts_consistent_dim(self):
        r1 = encode_texts(["hello", "world", "test"])
        assert r1.shape[0] == 3
        # All vectors same dimension
        assert r1.shape[1] > 0

    def test_cosine_sim_identical(self):
        v = np.array([1.0, 2.0, 3.0])
        assert cosine_sim(v, v) == pytest.approx(1.0)

    def test_cosine_sim_orthogonal(self):
        v1 = np.array([1.0, 0.0])
        v2 = np.array([0.0, 1.0])
        assert cosine_sim(v1, v2) == pytest.approx(0.0)

    def test_cosine_sim_zero_vector(self):
        v1 = np.array([0.0, 0.0])
        v2 = np.array([1.0, 2.0])
        assert cosine_sim(v1, v2) == 0.0


# ── Tokenizer tests (basic backend internals) ───────────────────────


class TestTokenizer:
    def test_basic_tokenization(self):
        tokens = _tokenize("Hello world! How are you?")
        assert "hello" in tokens
        assert "world" in tokens
        # Stopwords removed
        assert "how" not in tokens
        assert "are" not in tokens
        assert "you" not in tokens

    def test_punctuation_stripping(self):
        tokens = _tokenize("truth, beauty... and justice!")
        assert "truth" in tokens
        assert "beauty" in tokens
        assert "justice" in tokens

    def test_single_char_filtered(self):
        tokens = _tokenize("I a x truth")
        assert "truth" in tokens
        # Single chars removed
        assert "x" not in tokens

    def test_empty_text(self):
        assert _tokenize("") == []
        assert _tokenize("   ") == []

    def test_stopwords_removed(self):
        tokens = _tokenize("the quick brown fox is in the house")
        assert "quick" in tokens
        assert "brown" in tokens
        assert "fox" in tokens
        assert "house" in tokens
        assert "the" not in tokens
        assert "is" not in tokens
        assert "in" not in tokens


# ── TF/IDF computation tests ────────────────────────────────────────


class TestTFIDF:
    def test_compute_tf(self):
        tf = _compute_tf(["truth", "beauty", "truth"])
        assert tf["truth"] == pytest.approx(2 / 3)
        assert tf["beauty"] == pytest.approx(1 / 3)

    def test_compute_tf_empty(self):
        tf = _compute_tf([])
        assert tf == {}

    def test_compute_idf(self):
        docs = [["truth", "beauty"], ["truth", "justice"], ["beauty", "justice"]]
        idf = _compute_idf(docs)
        # All appear in same number of docs
        assert idf["truth"] == idf["beauty"] == idf["justice"]

    def test_idf_rare_term_higher(self):
        docs = [["common", "rare"], ["common", "other"], ["common", "yet"]]
        idf = _compute_idf(docs)
        assert idf["rare"] > idf["common"]

    def test_idf_empty_docs(self):
        assert _compute_idf([]) == {}

    def test_tfidf_vector(self):
        idf = {"truth": 1.0, "beauty": 0.5}
        vec = _tfidf_vector(["truth", "beauty", "truth"], idf)
        assert vec["truth"] == pytest.approx(2 / 3 * 1.0)
        assert vec["beauty"] == pytest.approx(1 / 3 * 0.5)


# ── Cosine similarity (dict) tests ──────────────────────────────────


class TestCosineSimilarity:
    def test_identical_vectors(self):
        v = {"truth": 1.0, "beauty": 0.5}
        assert _cosine_similarity(v, v) == pytest.approx(1.0)

    def test_orthogonal_vectors(self):
        v1 = {"truth": 1.0}
        v2 = {"beauty": 1.0}
        assert _cosine_similarity(v1, v2) == pytest.approx(0.0)

    def test_partial_overlap(self):
        v1 = {"truth": 1.0, "beauty": 1.0}
        v2 = {"truth": 1.0, "justice": 1.0}
        sim = _cosine_similarity(v1, v2)
        assert 0.0 < sim < 1.0

    def test_empty_vectors(self):
        assert _cosine_similarity({}, {"truth": 1.0}) == 0.0
        assert _cosine_similarity({"truth": 1.0}, {}) == 0.0
        assert _cosine_similarity({}, {}) == 0.0


# ── Main metric function tests ──────────────────────────────────────


class TestMetricSemanticDelta:
    def test_empty_input(self):
        name, val = metric_semantic_delta(_ctx(""), _empty_memory())
        assert name == "semantic_delta"
        assert val == 0.5

    def test_no_memory(self):
        name, val = metric_semantic_delta(_ctx("What is truth?"), _empty_memory())
        assert name == "semantic_delta"
        assert val == 1.0

    def test_identical_content(self):
        """Same text in input and memory should give low delta."""
        name, val = metric_semantic_delta(
            _ctx("What is philosophical truth and wisdom?"),
            _memory("What is philosophical truth and wisdom?"),
        )
        assert name == "semantic_delta"
        assert val < 0.3  # Very similar

    def test_completely_different(self):
        """Completely different topics should give high delta."""
        name, val = metric_semantic_delta(
            _ctx("quantum physics entanglement particles"),
            _memory("cooking pasta recipe ingredients tomato"),
        )
        assert name == "semantic_delta"
        assert val > 0.5  # Very different

    def test_partial_overlap(self):
        """Partially overlapping content should give moderate delta."""
        name, val = metric_semantic_delta(
            _ctx("What is philosophical truth?"),
            _memory("Philosophical analysis of beauty and truth"),
        )
        assert name == "semantic_delta"
        assert 0.01 < val < 0.95  # Moderate

    def test_multiple_memory_items(self):
        """Memory with multiple items — closer to one should reduce delta."""
        name, val = metric_semantic_delta(
            _ctx("freedom and responsibility in ethics"),
            _memory(
                "freedom is essential in philosophy",
                "cooking recipes for dinner",
                "mathematical equations in physics",
            ),
        )
        assert name == "semantic_delta"
        assert val < 1.0

    def test_value_range(self):
        """Delta should always be in [0.0, 1.0]."""
        test_cases = [
            (_ctx("truth"), _empty_memory()),
            (_ctx("truth"), _memory("truth")),
            (_ctx("truth"), _memory("beauty")),
            (_ctx("hello world truth beauty"), _memory("hello world truth beauty")),
        ]
        for ctx, mem in test_cases:
            name, val = metric_semantic_delta(ctx, mem)
            assert 0.0 <= val <= 1.0, f"Delta {val} out of range for {ctx.user_input}"

    def test_similar_content_lower_delta(self):
        """Sharing vocabulary should give lower delta than completely different."""
        name1, val1 = metric_semantic_delta(
            _ctx("existentialism phenomenology hermeneutics"),
            _memory("existentialism phenomenology hermeneutics epistemology"),
        )
        name2, val2 = metric_semantic_delta(
            _ctx("existentialism phenomenology hermeneutics"),
            _memory("weather sports traffic news"),
        )
        assert val1 < val2

    def test_stopword_invariance(self):
        """Adding stopwords shouldn't significantly change the delta."""
        name1, val1 = metric_semantic_delta(
            _ctx("truth beauty justice"),
            _memory("truth beauty justice"),
        )
        name2, val2 = metric_semantic_delta(
            _ctx("the truth and the beauty of justice"),
            _memory("truth beauty justice"),
        )
        # Should be similar since both backends handle stopwords
        assert abs(val1 - val2) < 0.3


# ── Embedding API tests ──────────────────────────────────────────────


class TestEncodeTexts:
    def test_similar_texts_closer(self):
        """Semantically similar texts should have higher cosine similarity."""
        embs = encode_texts(
            [
                "philosophy of mind consciousness",
                "philosophy of mind awareness",
                "cooking pasta recipe tomato sauce",
            ]
        )
        sim_close = cosine_sim(embs[0], embs[1])
        sim_far = cosine_sim(embs[0], embs[2])
        assert sim_close > sim_far

    def test_paraphrase_detection(self):
        """Paraphrases should have reasonable similarity."""
        embs = encode_texts(
            [
                "freedom is essential for human dignity",
                "liberty is fundamental to human worth",
            ]
        )
        sim = cosine_sim(embs[0], embs[1])
        # Even TF-IDF should find some similarity (shared words: human)
        assert sim > 0.0

    def test_empty_text_handled(self):
        """Empty texts should not crash."""
        embs = encode_texts(["", "hello world"])
        assert embs.shape[0] == 2


# ── Integration with pipeline ───────────────────────────────────────


class TestSemanticDeltaIntegration:
    def test_metric_signature(self):
        """Metric returns correct signature for TensorEngine."""
        name, val = metric_semantic_delta(_ctx("test"), _empty_memory())
        assert isinstance(name, str)
        assert isinstance(val, float)
        assert name == "semantic_delta"

    def test_used_in_tensor_engine(self):
        """Verify metric works when injected into TensorEngine."""
        from po_core.tensors.engine import TensorEngine

        engine = TensorEngine(metrics=[metric_semantic_delta])
        result = engine.compute(_ctx("What is truth?"), _empty_memory())
        assert "semantic_delta" in result.metrics
        assert result.metrics["semantic_delta"] == 1.0  # no memory = max divergence


__all__: list = []
