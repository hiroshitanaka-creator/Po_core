"""
Interaction Tensor Metric
=========================

Estimates philosopher-philosopher interaction potential from user input.

When an input touches multiple philosophical domains (ethics, epistemology,
aesthetics, politics, etc.), more philosopher interaction (harmony/tension)
is expected. This metric predicts that interaction density.

Score interpretation:
- 0.0 = Single-domain or trivial input (low interaction)
- 0.5 = Moderate cross-domain engagement
- 1.0 = Rich multi-domain input with high interaction potential

Based on the 6 interaction dimensions from the legacy InteractionTensor:
1. conceptual_harmony       - shared thematic vocabulary
2. philosophical_tension    - opposing concept pairs
3. epistemological_breadth  - ways of knowing referenced
4. ethical_engagement       - moral framework keywords
5. ontological_depth        - being/existence themes
6. methodological_diversity - analytical approaches referenced

DEPENDENCY RULES:
- domain only (Context, MemorySnapshot)
"""
from __future__ import annotations

import math
import re
from typing import Dict, List, Tuple

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot


# ── Keyword dictionaries for 6 interaction dimensions ──

_CONCEPTUAL_KEYWORDS: Dict[str, List[str]] = {
    "metaphysics": ["being", "existence", "reality", "substance", "essence", "nature"],
    "epistemology": ["knowledge", "truth", "belief", "certainty", "doubt", "reason"],
    "ethics": ["good", "evil", "virtue", "duty", "right", "wrong", "moral"],
    "aesthetics": ["beauty", "art", "sublime", "taste", "harmony", "form"],
    "politics": ["justice", "power", "freedom", "rights", "equality", "authority"],
    "logic": ["argument", "proof", "valid", "fallacy", "contradiction", "premise"],
}

_TENSION_PAIRS: List[Tuple[str, str]] = [
    ("freedom", "determinism"),
    ("individual", "society"),
    ("reason", "emotion"),
    ("absolute", "relative"),
    ("being", "becoming"),
    ("universal", "particular"),
    ("mind", "body"),
    ("appearance", "reality"),
    ("subjective", "objective"),
    ("theory", "practice"),
]

_EPISTEMOLOGICAL_KEYWORDS = {
    "empirical": ["experience", "observation", "evidence", "experiment", "sense"],
    "rational": ["reason", "logic", "deduction", "a priori", "innate"],
    "intuitive": ["intuition", "insight", "feeling", "awareness", "direct"],
    "dialectical": ["thesis", "antithesis", "synthesis", "contradiction", "sublation"],
    "phenomenological": ["consciousness", "perception", "intentionality", "lived", "phenomenon"],
    "pragmatic": ["practice", "consequence", "usefulness", "inquiry", "action"],
}

_ETHICAL_KEYWORDS = {
    "deontological": ["duty", "obligation", "categorical", "imperative", "right"],
    "consequentialist": ["outcome", "consequence", "utility", "greatest", "happiness"],
    "virtue": ["virtue", "character", "excellence", "flourishing", "eudaimonia"],
    "care": ["care", "empathy", "compassion", "relationship", "responsibility"],
    "existential": ["authentic", "choice", "freedom", "commitment", "absurd"],
}

_ONTOLOGICAL_KEYWORDS = [
    "being", "existence", "nothing", "void", "time", "space",
    "substance", "essence", "dasein", "phenomenon", "noumenon",
    "contingent", "necessary", "possible", "actual", "potential",
]

_METHODOLOGICAL_KEYWORDS = {
    "analytic": ["analysis", "definition", "clarification", "language", "logic"],
    "continental": ["interpretation", "hermeneutic", "deconstruction", "genealogy"],
    "phenomenological": ["describe", "bracket", "reduction", "essence", "horizon"],
    "dialectical": ["dialectic", "contradiction", "synthesis", "negation", "aufheben"],
    "pragmatic": ["experiment", "inquiry", "consequence", "practice", "problem"],
    "critical": ["critique", "power", "ideology", "emancipation", "discourse"],
}


def _tokenize(text: str) -> List[str]:
    """Simple lowercase tokenization."""
    return re.findall(r"[a-z']+", text.lower())


def _domain_coverage(tokens: set) -> float:
    """Count how many conceptual domains the input touches (0-1)."""
    domains_hit = 0
    for domain_kws in _CONCEPTUAL_KEYWORDS.values():
        if tokens & set(domain_kws):
            domains_hit += 1
    return domains_hit / len(_CONCEPTUAL_KEYWORDS) if _CONCEPTUAL_KEYWORDS else 0.0


def _tension_score(tokens: set) -> float:
    """Count how many tension pairs are activated (0-1)."""
    pairs_hit = 0
    for a, b in _TENSION_PAIRS:
        if a in tokens or b in tokens:
            pairs_hit += 1
    return pairs_hit / len(_TENSION_PAIRS) if _TENSION_PAIRS else 0.0


def _epistemological_breadth(tokens: set) -> float:
    """How many epistemological approaches are referenced (0-1)."""
    approaches_hit = 0
    for approach_kws in _EPISTEMOLOGICAL_KEYWORDS.values():
        if tokens & set(approach_kws):
            approaches_hit += 1
    return approaches_hit / len(_EPISTEMOLOGICAL_KEYWORDS) if _EPISTEMOLOGICAL_KEYWORDS else 0.0


def _ethical_engagement(tokens: set) -> float:
    """How many ethical frameworks are referenced (0-1)."""
    frameworks_hit = 0
    for fw_kws in _ETHICAL_KEYWORDS.values():
        if tokens & set(fw_kws):
            frameworks_hit += 1
    return frameworks_hit / len(_ETHICAL_KEYWORDS) if _ETHICAL_KEYWORDS else 0.0


def _ontological_depth(tokens: set) -> float:
    """How many ontological concepts appear (0-1)."""
    hits = len(tokens & set(_ONTOLOGICAL_KEYWORDS))
    return min(hits / 4.0, 1.0)


def _methodological_diversity(tokens: set) -> float:
    """How many philosophical methods are referenced (0-1)."""
    methods_hit = 0
    for method_kws in _METHODOLOGICAL_KEYWORDS.values():
        if tokens & set(method_kws):
            methods_hit += 1
    return methods_hit / len(_METHODOLOGICAL_KEYWORDS) if _METHODOLOGICAL_KEYWORDS else 0.0


def _memory_continuity_boost(memory: MemorySnapshot) -> float:
    """Ongoing conversation = more interaction potential."""
    n = len(memory.items)
    if n == 0:
        return 0.0
    return min(n / 20.0, 0.1)


def metric_interaction_tensor(ctx: Context, memory: MemorySnapshot) -> Tuple[str, float]:
    """
    Estimate philosopher-philosopher interaction potential.

    Analyzes the input for cross-domain philosophical content.
    Higher score = more philosophical domains engaged = more interaction expected.

    Returns:
        ("interaction_tensor", value) where value ∈ [0.0, 1.0]
    """
    text = ctx.user_input
    if not text or not text.strip():
        return "interaction_tensor", 0.0

    tokens = set(_tokenize(text))

    # Compute 6 dimensions
    dimensions = [
        _domain_coverage(tokens),
        _tension_score(tokens),
        _epistemological_breadth(tokens),
        _ethical_engagement(tokens),
        _ontological_depth(tokens),
        _methodological_diversity(tokens),
    ]

    # L2 norm normalized to [0, 1]
    raw_norm = math.sqrt(sum(d * d for d in dimensions))
    max_norm = math.sqrt(len(dimensions))  # max when all = 1.0
    normalized = raw_norm / max_norm if max_norm > 0 else 0.0

    # Memory continuity boost
    boost = _memory_continuity_boost(memory)

    value = min(normalized + boost, 1.0)
    return "interaction_tensor", round(value, 4)


__all__ = ["metric_interaction_tensor"]
