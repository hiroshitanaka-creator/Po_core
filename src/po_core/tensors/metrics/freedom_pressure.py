"""
Freedom Pressure Metric
=======================

Computes freedom_pressure from user input + memory context.
Uses keyword-based dimensional analysis adapted from legacy FreedomPressureTensor.

0.0 = no pressure (NORMAL mode, maximum freedom)
1.0 = maximum pressure (CRITICAL mode, maximum restriction)

Dimensions:
- choice_weight: Decision-related keywords
- responsibility_degree: Duty/obligation keywords
- temporal_urgency: Urgency keywords
- ethical_stakes: Moral/ethical keywords
- social_impact: Community/social keywords
- authenticity_pressure: Self/identity keywords

Memory factors:
- Conversation depth amplifies pressure slightly
- Recent "refuse" or "blocked" tags increase pressure
"""

from __future__ import annotations

import math
import re
from typing import List, Pattern, Tuple, Union

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.text.normalize import normalize_text

# ── Keyword lists for each dimension ──

_Keyword = Union[str, Pattern[str]]

_CHOICE_KEYWORDS_EN = [
    "should",
    "must",
    "ought",
    "decide",
    "choose",
    "what",
    "option",
    "alternative",
]
_RESPONSIBILITY_KEYWORDS_EN = [
    "responsible",
    "duty",
    "obligation",
    "accountable",
    "consequence",
]
_URGENCY_KEYWORDS_EN = [
    "now",
    "urgent",
    "immediate",
    "quickly",
    "soon",
    "hurry",
    "deadline",
]
_ETHICAL_KEYWORDS_EN = [
    "right",
    "wrong",
    "good",
    "bad",
    "moral",
    "ethical",
    "virtue",
    "harm",
    "justice",
]
_SOCIAL_KEYWORDS_EN = ["we", "us", "society", "people", "community", "others", "public"]
_AUTHENTICITY_KEYWORDS_EN = [
    "authentic",
    "genuine",
    "true",
    "self",
    "identity",
    "real",
    "honest",
]

# Japanese examples used for calibration comments:
# - choice: 「どちらを選ぶべきか」「判断したい」
# - responsibility: 「責任を取る義務」
# - urgency: 「至急」「締め切りが迫る」
_CHOICE_KEYWORDS_JA: List[_Keyword] = [
    "選ぶ",
    "選択",
    "判断",
    "決め",
    "どちら",
    "べき",
    "どうすべき",
]
_RESPONSIBILITY_KEYWORDS_JA: List[_Keyword] = [
    "責任",
    "義務",
    "説明責任",
    "結果",
    "影響",
]
_URGENCY_KEYWORDS_JA: List[_Keyword] = [
    "至急",
    "緊急",
    "今すぐ",
    "すぐ",
    "急い",
    "締め切り",
    "期限",
]
_ETHICAL_KEYWORDS_JA: List[_Keyword] = [
    "倫理",
    "道徳",
    "正しい",
    "間違",
    "善",
    "悪",
    "害",
    "公正",
    "正義",
]
_SOCIAL_KEYWORDS_JA: List[_Keyword] = [
    "社会",
    "他者",
    "みんな",
    "人々",
    "公共",
    "コミュニティ",
    "世間",
]
_AUTHENTICITY_KEYWORDS_JA: List[_Keyword] = [
    "本音",
    "自分らし",
    "真正",
    "誠実",
    "本心",
    "自己",
    "アイデンティティ",
]

_ALL_DIMENSIONS = [
    ("choice_weight", _CHOICE_KEYWORDS_EN, _CHOICE_KEYWORDS_JA),
    ("responsibility_degree", _RESPONSIBILITY_KEYWORDS_EN, _RESPONSIBILITY_KEYWORDS_JA),
    ("temporal_urgency", _URGENCY_KEYWORDS_EN, _URGENCY_KEYWORDS_JA),
    ("ethical_stakes", _ETHICAL_KEYWORDS_EN, _ETHICAL_KEYWORDS_JA),
    ("social_impact", _SOCIAL_KEYWORDS_EN, _SOCIAL_KEYWORDS_JA),
    ("authenticity_pressure", _AUTHENTICITY_KEYWORDS_EN, _AUTHENTICITY_KEYWORDS_JA),
]


def _tokenize(text: str) -> List[str]:
    """Simple whitespace tokenizer with punctuation stripping."""
    tokens = []
    for raw in text.split():
        cleaned = raw.strip(".,!?\"'()[]{}:;`~@#$%^&*+=<>/\\|").lower()
        if cleaned:
            tokens.append(cleaned)
    return tokens


def _keyword_ratio_en(tokens: List[str], keywords: List[str]) -> float:
    """Exact-token match ratio for English keywords (legacy behavior)."""
    if not keywords:
        return 0.0
    token_set = set(tokens)
    hits = sum(1 for kw in keywords if kw in token_set)
    return min(hits / len(keywords), 1.0)


def _keyword_ratio_ja(text: str, keywords: List[_Keyword]) -> float:
    """Substring/regex match ratio for Japanese text without tokenization."""
    if not keywords:
        return 0.0
    hits = 0
    for kw in keywords:
        if isinstance(kw, re.Pattern):
            matched = kw.search(text) is not None
        else:
            matched = kw in text
        if matched:
            hits += 1
    return min(hits / len(keywords), 1.0)


def _compute_dimensions(text: str) -> List[float]:
    """Compute 6-dimensional pressure from text."""
    normalized = normalize_text(text)
    tokens = _tokenize(normalized)
    values: List[float] = []
    for _, kws_en, kws_ja in _ALL_DIMENSIONS:
        en_ratio = _keyword_ratio_en(tokens, kws_en)
        ja_ratio = _keyword_ratio_ja(normalized, kws_ja)
        values.append(max(en_ratio, ja_ratio))
    return values


def _l2_norm(values: List[float]) -> float:
    """L2 norm of a vector."""
    return math.sqrt(sum(v * v for v in values))


def _memory_pressure_boost(memory: MemorySnapshot) -> float:
    """Compute additional pressure from conversation history."""
    if not memory.items:
        return 0.0

    boost = 0.0

    # Conversation depth: more items = slightly more pressure
    depth = len(memory.items)
    boost += min(depth * 0.005, 0.05)  # max +0.05 from depth

    # Recent refusals or blocks increase pressure
    recent_tags = []
    for item in memory.items[-5:]:  # Last 5 items
        recent_tags.extend(item.tags)

    refuse_count = sum(1 for t in recent_tags if t in ("refuse", "blocked", "rejected"))
    boost += min(refuse_count * 0.03, 0.1)  # max +0.1 from refusals

    return boost


def metric_freedom_pressure(ctx: Context, memory: MemorySnapshot) -> Tuple[str, float]:
    """
    Compute freedom_pressure metric.

    Analyses user input via keyword-based dimensional analysis,
    computes L2 norm of 6 dimensions, adds memory-based boost.

    Args:
        ctx: Request context with user_input
        memory: Memory snapshot with conversation history

    Returns:
        ("freedom_pressure", value) where value in [0.0, 1.0]
    """
    dimensions = _compute_dimensions(ctx.user_input)

    # L2 norm of 6D vector, normalized to [0, 1]
    # Max possible L2 norm of 6 × 1.0 = sqrt(6) ≈ 2.449
    raw_norm = _l2_norm(dimensions)
    max_norm = math.sqrt(len(dimensions))
    normalized = raw_norm / max_norm if max_norm > 0 else 0.0

    # Add memory-based boost
    boost = _memory_pressure_boost(memory)
    value = min(normalized + boost, 1.0)

    return "freedom_pressure", round(value, 4)


__all__ = ["metric_freedom_pressure"]
