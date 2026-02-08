"""
Blocked Tensor Metric
=====================

Estimates the degree to which reasoning should be constrained/blocked.
Combines freedom_pressure (inverse) and semantic_delta into a single
constraint metric.

0.0 = no constraint needed (safe, on-topic)
1.0 = maximum constraint (high pressure + high divergence)

Also performs direct harmful keyword detection as an additional signal.
"""

from __future__ import annotations

from typing import List, Tuple

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot

# Harmful/sensitive keyword lists for direct detection
_HARMFUL_KEYWORDS = [
    "bomb",
    "weapon",
    "kill",
    "attack",
    "poison",
    "exploit",
    "hack",
    "steal",
    "fraud",
    "illegal",
]

_SENSITIVE_KEYWORDS = [
    "suicide",
    "self-harm",
    "overdose",
    "abuse",
]


def _tokenize(text: str) -> List[str]:
    """Simple whitespace tokenizer with punctuation stripping."""
    tokens = []
    for raw in text.split():
        cleaned = raw.strip(".,!?\"'()[]{}:;`~@#$%^&*+=<>/\\|").lower()
        if cleaned:
            tokens.append(cleaned)
    return tokens


def _harmful_score(text: str) -> float:
    """Detect harmful/sensitive keywords in text. Returns [0,1]."""
    tokens = set(_tokenize(text))
    if not tokens:
        return 0.0

    harmful_hits = sum(1 for kw in _HARMFUL_KEYWORDS if kw in tokens)
    sensitive_hits = sum(1 for kw in _SENSITIVE_KEYWORDS if kw in tokens)

    # Weight harmful more than sensitive
    score = (harmful_hits * 0.15) + (sensitive_hits * 0.10)
    return min(score, 1.0)


def metric_blocked_tensor(ctx: Context, memory: MemorySnapshot) -> Tuple[str, float]:
    """
    Compute blocked_tensor metric.

    Estimates reasoning constraint level from:
    1. Harmful keyword detection in user input
    2. Input vocabulary diversity (low diversity = more constrained)

    Args:
        ctx: Request context with user_input
        memory: Memory snapshot

    Returns:
        ("blocked_tensor", value) where value in [0.0, 1.0]
    """
    text = ctx.user_input

    if not text.strip():
        return "blocked_tensor", 0.0

    # Component 1: Direct harmful keyword detection
    harm = _harmful_score(text)

    # Component 2: Vocabulary diversity (inverse)
    # Low diversity = more constrained / formulaic
    tokens = _tokenize(text)
    if tokens:
        unique_ratio = len(set(tokens)) / len(tokens)
        constraint = 1.0 - unique_ratio  # Low uniqueness = high constraint
    else:
        constraint = 0.0

    # Combine: harm dominates if present, otherwise use constraint
    value = max(harm, constraint * 0.3)
    value = min(value, 1.0)

    return "blocked_tensor", round(value, 4)


__all__ = ["metric_blocked_tensor"]
