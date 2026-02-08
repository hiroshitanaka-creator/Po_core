"""
Semantic Delta Metric
=====================

Measures how much the current input diverges from conversation memory.
Higher value = more novel/divergent input relative to history.

0.0 = identical to memory (maximum alignment)
1.0 = completely new topic (maximum divergence)

Uses token overlap analysis between user input and memory items.
"""
from __future__ import annotations

from typing import List, Set, Tuple

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot


def _tokenize(text: str) -> List[str]:
    """Simple whitespace tokenizer with punctuation stripping."""
    tokens = []
    for raw in text.split():
        cleaned = raw.strip(".,!?\"'()[]{}:;`~@#$%^&*+=<>/\\|").lower()
        if cleaned:
            tokens.append(cleaned)
    return tokens


def _token_set(text: str) -> Set[str]:
    """Get unique tokens from text."""
    return set(_tokenize(text))


def metric_semantic_delta(ctx: Context, memory: MemorySnapshot) -> Tuple[str, float]:
    """
    Compute semantic_delta metric.

    Measures token-level divergence between current user input
    and conversation memory. If no memory exists, returns 1.0
    (maximum divergence — completely new context).

    Args:
        ctx: Request context with user_input
        memory: Memory snapshot with conversation history

    Returns:
        ("semantic_delta", value) where value in [0.0, 1.0]
    """
    input_tokens = _token_set(ctx.user_input)

    if not input_tokens:
        return "semantic_delta", 0.5  # Neutral for empty input

    if not memory.items:
        return "semantic_delta", 1.0  # No history = maximum divergence

    # Collect all tokens from memory items
    memory_tokens: Set[str] = set()
    for item in memory.items:
        memory_tokens.update(_tokenize(item.text))

    if not memory_tokens:
        return "semantic_delta", 1.0

    # Compute overlap
    overlap = len(input_tokens & memory_tokens)
    coverage = overlap / len(input_tokens)

    # Delta = 1 - coverage (more coverage = less delta)
    delta = round(1.0 - coverage, 4)
    return "semantic_delta", delta


__all__ = ["metric_semantic_delta"]
