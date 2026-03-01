"""
Semantic Delta Metric
=====================

Measures how much the current input diverges from conversation memory.
Higher value = more novel/divergent input relative to history.

0.0 = identical to memory (maximum alignment)
1.0 = completely new topic (maximum divergence)

Uses embedding-based cosine similarity between user input and memory items.

**Backends** (selected automatically, first available wins):

1. sentence-transformers  — real semantic embeddings (requires torch)
2. sklearn TfidfVectorizer — TF-IDF sparse vectors (lighter, no GPU)

Both backends produce the same (str, float) return signature.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List, Optional, Set, Tuple

import numpy as np

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.text.embedding_cache import GLOBAL_EMBEDDING_CACHE

# ── Backend Detection ────────────────────────────────────────────────

_BACKEND: Optional[str] = None  # set on first call


def _detect_backend() -> str:
    """Detect best available backend. Result is cached."""
    global _BACKEND
    if _BACKEND is not None:
        return _BACKEND
    try:
        from sentence_transformers import SentenceTransformer  # noqa: F401

        _BACKEND = "sbert"
    except (ImportError, Exception):
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: F401

            _BACKEND = "tfidf"
        except ImportError:
            _BACKEND = "basic"
    return _BACKEND


def _has_sklearn() -> bool:
    """Check if sklearn is available."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: F401

        return True
    except ImportError:
        return False


# ── Shared Encoder API ───────────────────────────────────────────────

_sbert_model = None
_SBERT_MODEL_ID = "sbert:all-MiniLM-L6-v2"


def _get_sbert_model():
    """Lazy-load sentence-transformers model (cached singleton)."""
    global _sbert_model
    if _sbert_model is None:
        from sentence_transformers import SentenceTransformer

        _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _sbert_model


def encode_texts(texts: List[str]) -> np.ndarray:
    """
    Encode a list of texts into dense vectors.

    Returns a 2D array of shape (len(texts), dim).
    This function is reusable by other metrics (InteractionTensor, etc.).

    Automatically falls back if the preferred backend fails at runtime
    (e.g., model download blocked, GPU unavailable).
    """
    global _BACKEND
    backend = _detect_backend()

    if backend == "sbert":
        try:
            return _encode_sbert_cached(texts)
        except Exception:
            # Model download failed or runtime error — fall back
            _BACKEND = "tfidf" if _has_sklearn() else "basic"
            backend = _BACKEND

    if backend == "tfidf":
        return _encode_tfidf(texts)

    # Fallback: basic token overlap vectors
    return _encode_basic(texts)


def _encode_sbert_cached(texts: List[str]) -> np.ndarray:
    model = _get_sbert_model()
    encoded: list[np.ndarray] = []
    missing_texts: list[str] = []
    missing_indices: list[int] = []

    for i, text in enumerate(texts):
        cached = GLOBAL_EMBEDDING_CACHE.get(text, _SBERT_MODEL_ID)
        if cached is None:
            missing_texts.append(text)
            missing_indices.append(i)
            encoded.append(np.array([], dtype=np.float64))
            continue
        encoded.append(cached)

    if missing_texts:
        fresh = model.encode(
            missing_texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        for idx, text, emb in zip(missing_indices, missing_texts, fresh):
            arr = np.array(emb, dtype=np.float64)
            GLOBAL_EMBEDDING_CACHE.put(text, _SBERT_MODEL_ID, arr)
            encoded[idx] = arr

    return np.vstack(encoded) if encoded else np.zeros((0, 1), dtype=np.float64)


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """
    Cosine similarity between two 1D vectors.

    Returns value in [-1.0, 1.0], clamped to [0.0, 1.0] for delta use.
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def get_backend() -> str:
    """Return the active backend name. Useful for tests and diagnostics."""
    return _detect_backend()


def preload_models() -> Dict[str, str]:
    """Optional startup preloading for semantic_delta dependencies."""
    backend = _detect_backend()
    status: Dict[str, str] = {"backend": backend}
    if backend == "sbert":
        try:
            _get_sbert_model()
            status["sbert"] = "ready"
        except Exception as exc:
            status["sbert"] = f"failed: {exc}"
    return status


def configure_embedding_cache(*, max_size: int) -> None:
    GLOBAL_EMBEDDING_CACHE.set_max_size(max_size)


def clear_embedding_cache() -> None:
    GLOBAL_EMBEDDING_CACHE.clear()


# ── TF-IDF Backend ───────────────────────────────────────────────────


def _encode_tfidf(texts: List[str]) -> np.ndarray:
    """Encode texts using sklearn TfidfVectorizer → dense numpy array."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    if not texts or all(not t.strip() for t in texts):
        return np.zeros((len(texts), 1))

    vectorizer = TfidfVectorizer(
        stop_words="english",
        min_df=1,
        max_df=1.0,
        sublinear_tf=True,
    )
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
        return tfidf_matrix.toarray()
    except ValueError:
        # All texts are stop-words or empty after preprocessing
        return np.zeros((len(texts), 1))


# ── Basic (legacy) Backend ───────────────────────────────────────────

# Common English stopwords (low semantic value)
_STOPWORDS: Set[str] = {
    "a",
    "an",
    "the",
    "is",
    "it",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "and",
    "or",
    "but",
    "not",
    "with",
    "as",
    "by",
    "was",
    "are",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "can",
    "this",
    "that",
    "these",
    "those",
    "i",
    "you",
    "he",
    "she",
    "we",
    "they",
    "me",
    "him",
    "her",
    "us",
    "them",
    "my",
    "your",
    "his",
    "its",
    "our",
    "their",
    "what",
    "which",
    "who",
    "whom",
    "how",
    "when",
    "where",
    "why",
    "if",
    "then",
    "so",
    "no",
    "yes",
    "all",
    "each",
    "every",
    "both",
    "few",
    "more",
    "most",
    "some",
    "any",
    "from",
    "about",
    "into",
    "over",
    "after",
    "before",
    "between",
    "through",
    "during",
    "above",
    "below",
    "up",
    "down",
    "out",
    "off",
    "just",
    "only",
    "very",
    "also",
    "too",
    "than",
    "here",
    "there",
}


def _tokenize(text: str) -> List[str]:
    """Tokenize text: lowercase, strip punctuation, remove stopwords."""
    tokens = []
    for raw in text.split():
        cleaned = raw.strip(".,!?\"'()[]{}:;`~@#$%^&*+=<>/\\|").lower()
        if cleaned and cleaned not in _STOPWORDS and len(cleaned) > 1:
            tokens.append(cleaned)
    return tokens


def _compute_tf(tokens: List[str]) -> Dict[str, float]:
    """Compute term frequency (TF) for a token list."""
    counts = Counter(tokens)
    n = len(tokens) if tokens else 1
    return {term: count / n for term, count in counts.items()}


def _compute_idf(documents: List[List[str]]) -> Dict[str, float]:
    """
    Compute inverse document frequency (IDF) across documents.

    IDF(t) = log(1 + N / (1 + df(t)))
    """
    n_docs = len(documents)
    if n_docs == 0:
        return {}
    df: Dict[str, int] = {}
    for doc in documents:
        for term in set(doc):
            df[term] = df.get(term, 0) + 1
    return {term: math.log(1 + n_docs / (1 + freq)) for term, freq in df.items()}


def _tfidf_vector(tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    """Compute TF-IDF vector for a token list given IDF values."""
    tf = _compute_tf(tokens)
    return {term: tf_val * idf.get(term, 0.0) for term, tf_val in tf.items()}


def _cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    """Cosine similarity between two sparse dict vectors. Returns [0.0, 1.0]."""
    if not v1 or not v2:
        return 0.0
    common = set(v1) & set(v2)
    dot = sum(v1[t] * v2[t] for t in common)
    mag1 = math.sqrt(sum(v * v for v in v1.values()))
    mag2 = math.sqrt(sum(v * v for v in v2.values()))
    if mag1 == 0.0 or mag2 == 0.0:
        return 0.0
    return dot / (mag1 * mag2)


def _encode_basic(texts: List[str]) -> np.ndarray:
    """Fallback: encode using hand-rolled TF-IDF into dense numpy arrays."""
    if not texts:
        return np.zeros((0, 1))

    all_tokens = [_tokenize(t) for t in texts]
    idf = _compute_idf(all_tokens)

    if not idf:
        return np.zeros((len(texts), 1))

    vocab = sorted(idf.keys())
    vocab_idx = {term: i for i, term in enumerate(vocab)}
    dim = len(vocab)
    result = np.zeros((len(texts), dim))
    for i, tokens in enumerate(all_tokens):
        vec = _tfidf_vector(tokens, idf)
        for term, val in vec.items():
            if term in vocab_idx:
                result[i, vocab_idx[term]] = val
    return result


# ── Main Metric Function ─────────────────────────────────────────────


def metric_semantic_delta(ctx: Context, memory: MemorySnapshot) -> Tuple[str, float]:
    """
    Compute semantic_delta metric using embedding cosine similarity.

    Measures semantic divergence between current user input and conversation
    memory. Automatically selects the best available backend:
    sentence-transformers (dense embeddings) or TF-IDF (sparse vectors).

    Args:
        ctx: Request context with user_input
        memory: Memory snapshot with conversation history

    Returns:
        ("semantic_delta", value) where value in [0.0, 1.0]
    """
    user_input = ctx.user_input.strip()

    if not user_input:
        return "semantic_delta", 0.5  # Neutral for empty input

    if not memory.items:
        return "semantic_delta", 1.0  # No history = maximum divergence

    memory_texts = [item.text for item in memory.items if item.text.strip()]
    if not memory_texts:
        return "semantic_delta", 1.0

    # Combine all memory into one aggregate document
    combined_memory = " ".join(memory_texts)

    # Encode input + memory together for consistent vectorization
    embeddings = encode_texts([user_input, combined_memory])

    similarity = cosine_sim(embeddings[0], embeddings[1])
    # Clamp to [0, 1] then invert
    similarity = max(0.0, min(1.0, similarity))
    delta = round(1.0 - similarity, 4)

    return "semantic_delta", delta


__all__ = [
    "metric_semantic_delta",
    "encode_texts",
    "cosine_sim",
    "get_backend",
    "preload_models",
    "configure_embedding_cache",
    "clear_embedding_cache",
]
