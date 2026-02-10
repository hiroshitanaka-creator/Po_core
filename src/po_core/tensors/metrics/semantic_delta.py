"""
Semantic Delta Metric
=====================

Measures how much the current input diverges from conversation memory.
Higher value = more novel/divergent input relative to history.

0.0 = identical to memory (maximum alignment)
1.0 = completely new topic (maximum divergence)

Uses TF-IDF cosine similarity between user input and memory items.
This is a significant upgrade from the original token-overlap approach:
TF-IDF weights rare/informative terms more heavily, producing better
semantic distance measurements.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List, Set, Tuple

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot

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
    where N = total docs, df(t) = docs containing term t.
    Uses smoothed variant to ensure non-negative values with small doc sets.
    """
    n_docs = len(documents)
    if n_docs == 0:
        return {}

    # Document frequency: how many documents contain each term
    df: Dict[str, int] = {}
    for doc in documents:
        unique_terms = set(doc)
        for term in unique_terms:
            df[term] = df.get(term, 0) + 1

    # Smoothed IDF: ensures non-negative values even with 2 documents
    return {term: math.log(1 + n_docs / (1 + freq)) for term, freq in df.items()}


def _tfidf_vector(tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    """Compute TF-IDF vector for a token list given IDF values."""
    tf = _compute_tf(tokens)
    return {term: tf_val * idf.get(term, 0.0) for term, tf_val in tf.items()}


def _cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    """
    Compute cosine similarity between two sparse vectors.

    Returns value in [0.0, 1.0].
    """
    if not v1 or not v2:
        return 0.0

    # Dot product
    common_terms = set(v1) & set(v2)
    dot = sum(v1[t] * v2[t] for t in common_terms)

    # Magnitudes
    mag1 = math.sqrt(sum(v * v for v in v1.values()))
    mag2 = math.sqrt(sum(v * v for v in v2.values()))

    if mag1 == 0.0 or mag2 == 0.0:
        return 0.0

    return dot / (mag1 * mag2)


def metric_semantic_delta(ctx: Context, memory: MemorySnapshot) -> Tuple[str, float]:
    """
    Compute semantic_delta metric using TF-IDF cosine similarity.

    Measures semantic divergence between current user input
    and conversation memory. If no memory exists, returns 1.0
    (maximum divergence — completely new context).

    Args:
        ctx: Request context with user_input
        memory: Memory snapshot with conversation history

    Returns:
        ("semantic_delta", value) where value in [0.0, 1.0]
    """
    input_tokens = _tokenize(ctx.user_input)

    if not input_tokens:
        return "semantic_delta", 0.5  # Neutral for empty input

    if not memory.items:
        return "semantic_delta", 1.0  # No history = maximum divergence

    # Tokenize each memory item as a separate document
    memory_docs = [_tokenize(item.text) for item in memory.items]

    # Flatten all memory tokens into one combined document
    all_memory_tokens: List[str] = []
    for doc in memory_docs:
        all_memory_tokens.extend(doc)

    if not all_memory_tokens:
        return "semantic_delta", 1.0

    # Build IDF from all documents (input + each memory item)
    all_docs = [input_tokens] + memory_docs
    idf = _compute_idf(all_docs)

    # Compute TF-IDF vectors
    input_vec = _tfidf_vector(input_tokens, idf)
    memory_vec = _tfidf_vector(all_memory_tokens, idf)

    # Similarity -> delta
    similarity = _cosine_similarity(input_vec, memory_vec)
    delta = round(1.0 - similarity, 4)

    return "semantic_delta", delta


__all__ = ["metric_semantic_delta"]
