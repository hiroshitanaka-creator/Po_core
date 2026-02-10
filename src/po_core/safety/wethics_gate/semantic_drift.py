"""
Semantic Drift Detection
========================

Detects whether repairs have changed the "goal" of a proposal.

The core principle:
- Repairs should fix HOW something is done, not WHAT is being done
- If a repair changes the fundamental goal, it's "semantic drift"
- High drift means the repair is essentially creating a new proposal

This module provides:
- DriftReport: Result of drift analysis
- semantic_drift(): Main drift calculation function

Design Notes:
- Uses simple heuristics (no external NLP dependencies)
- Designed to be replaced with embedding-based similarity later
- Returns drift in [0, 1] where 0 = no change, 1 = complete change
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class DriftReport:
    """
    Result of semantic drift analysis.

    Attributes:
        drift: Drift score in [0, 1], where 0 = no change, 1 = complete change
        notes: Human-readable explanation of drift sources
        key_concepts_before: Key concepts extracted from original text
        key_concepts_after: Key concepts extracted from repaired text
        lost_concepts: Concepts that were in original but not in repaired
        added_concepts: Concepts that were added in repaired text
    """

    drift: float
    notes: str
    key_concepts_before: List[str]
    key_concepts_after: List[str]
    lost_concepts: List[str]
    added_concepts: List[str]


def _extract_key_concepts(text: str) -> Set[str]:
    """
    Extract key concepts from text.

    This is a simple heuristic-based extraction:
    - Looks for noun phrases (Japanese: の-connected, particles)
    - Looks for action verbs
    - Filters common stop words

    In production, replace with proper NLP or embeddings.
    """
    concepts: Set[str] = set()

    # Japanese patterns
    # Noun + particle patterns
    ja_noun_patterns = [
        r"([一-龥ぁ-んァ-ン]+)(を|に|が|は|の|で|と|から|まで|へ)",
        r"([一-龥]+)(する|させる|される|できる)",
    ]

    for pat in ja_noun_patterns:
        for m in re.finditer(pat, text):
            concept = m.group(1)
            if len(concept) >= 2:  # Filter single chars
                concepts.add(concept)

    # English patterns
    # Verb phrases
    en_verb_patterns = [
        r"\b(create|build|develop|implement|design|improve|enhance|optimize)\s+(\w+)",
        r"\b(support|help|assist|enable|provide|offer)\s+(\w+)",
        r"\b(prevent|avoid|reduce|eliminate|remove|stop)\s+(\w+)",
        r"\b(dominate|control|subjugate|capture|exclude|abandon)\s+(\w+)",
    ]

    for pat in en_verb_patterns:
        for m in re.finditer(pat, text, re.I):
            verb = m.group(1).lower()
            obj = m.group(2).lower()
            concepts.add(f"{verb}_{obj}")

    # Key nouns (capitalized or important)
    en_noun_patterns = [
        r"\b(user|customer|market|platform|system|data|privacy|safety|harm)\b",
        r"\b(competitor|exclusion|dependency|manipulation|dignity)\b",
    ]

    for pat in en_noun_patterns:
        for m in re.finditer(pat, text, re.I):
            concepts.add(m.group(1).lower())

    # Goal-indicating phrases
    goal_patterns = [
        r"目的[はが](.{2,20})",
        r"目標[はが](.{2,20})",
        r"ゴール[はが](.{2,20})",
        r"(aim|goal|objective|purpose)\s+(?:is\s+)?(?:to\s+)?(\w+)",
    ]

    for pat in goal_patterns:
        for m in re.finditer(pat, text, re.I):
            concepts.add(f"goal:{m.group(1)[:20]}")

    return concepts


def _calculate_jaccard(set_a: Set[str], set_b: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 1.0  # Both empty = identical
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 1.0
    return intersection / union


def _detect_polarity_flip(before: str, after: str) -> float:
    """
    Detect if the proposal's polarity has flipped.

    Examples:
    - "dominate" -> "collaborate" = flip
    - "exclude" -> "include" = flip
    - "harm" -> "help" = flip

    Returns:
        Polarity flip score in [0, 1]
    """
    flip_pairs = [
        # Destructive -> Constructive
        (r"(支配|dominate)", r"(協調|協力|collaborate|coordinate)"),
        (r"(排除|exclude)", r"(包摂|include|embrace)"),
        (r"(破壊|destroy)", r"(生成|create|build)"),
        (r"(依存させる|addict)", r"(自律|autonomy|empower)"),
        (r"(操作|manipulate)", r"(支援|support|assist)"),
        (r"(切り捨て|abandon)", r"(尊重|respect|support)"),
        (r"(ロックイン|lock.?in)", r"(選択肢|options|interoperability)"),
    ]

    flip_count = 0
    total_pairs = 0

    for destructive, constructive in flip_pairs:
        has_destructive_before = bool(re.search(destructive, before, re.I))
        has_constructive_after = bool(re.search(constructive, after, re.I))

        if has_destructive_before and has_constructive_after:
            flip_count += 1
        if has_destructive_before or has_constructive_after:
            total_pairs += 1

    if total_pairs == 0:
        return 0.0

    return flip_count / total_pairs


def semantic_drift(
    before: str,
    after: str,
    before_goal: Optional[str] = None,
    after_goal: Optional[str] = None,
) -> DriftReport:
    """
    Calculate semantic drift between original and repaired text.

    The drift score combines:
    1. Concept overlap (Jaccard similarity)
    2. Polarity flip detection
    3. Goal change detection (if goals provided)

    Args:
        before: Original text
        after: Repaired text
        before_goal: Optional explicit goal statement for original
        after_goal: Optional explicit goal statement for repaired

    Returns:
        DriftReport with drift score and analysis details
    """
    # Extract concepts
    concepts_before = _extract_key_concepts(before)
    concepts_after = _extract_key_concepts(after)

    if before_goal:
        concepts_before.add(f"goal:{before_goal[:30]}")
    if after_goal:
        concepts_after.add(f"goal:{after_goal[:30]}")

    # Calculate components
    jaccard = _calculate_jaccard(concepts_before, concepts_after)
    concept_drift = 1.0 - jaccard

    polarity_flip = _detect_polarity_flip(before, after)

    # Lost and added concepts
    lost = concepts_before - concepts_after
    added = concepts_after - concepts_before

    # Combined drift score
    # Weight: concept_drift (40%), polarity_flip (40%), text_length_change (20%)
    len_before = len(before)
    len_after = len(after)
    length_ratio = min(len_before, len_after) / max(len_before, len_after, 1)
    length_drift = 1.0 - length_ratio

    drift = 0.4 * concept_drift + 0.4 * polarity_flip + 0.2 * length_drift

    # Clamp to [0, 1]
    drift = max(0.0, min(1.0, drift))

    # Generate notes
    notes_parts = []
    if concept_drift > 0.3:
        notes_parts.append(f"概念の変化が大きい (Jaccard={jaccard:.2f})")
    if polarity_flip > 0.3:
        notes_parts.append(f"極性の反転を検出 (flip={polarity_flip:.2f})")
    if length_drift > 0.3:
        notes_parts.append(f"テキスト長の変化が大きい (ratio={length_ratio:.2f})")
    if lost:
        notes_parts.append(f"失われた概念: {', '.join(list(lost)[:5])}")
    if added:
        notes_parts.append(f"追加された概念: {', '.join(list(added)[:5])}")

    notes = "; ".join(notes_parts) if notes_parts else "ドリフトは軽微"

    return DriftReport(
        drift=drift,
        notes=notes,
        key_concepts_before=sorted(concepts_before),
        key_concepts_after=sorted(concepts_after),
        lost_concepts=sorted(lost),
        added_concepts=sorted(added),
    )


__all__ = [
    "DriftReport",
    "semantic_drift",
]
