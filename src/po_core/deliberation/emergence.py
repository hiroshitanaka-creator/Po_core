"""
Emergence Detector
==================

Detects genuine philosophical emergence during deliberation rounds.

"Emergence" occurs when a proposal in round N is semantically distant from
ALL baseline (round 1) proposals — i.e., the philosophers collectively created
something genuinely new that no single voice proposed initially.

Novelty score = max cosine distance between current proposal and all baselines.
  0.0 → identical to a baseline proposal (no emergence)
  1.0 → completely orthogonal (maximum emergence)

Threshold (default 0.65) is calibrated so that paraphrase-level rewording
stays below it while truly novel synthesis crosses it.

Usage::

    from po_core.deliberation.emergence import EmergenceDetector, EmergenceSignal
    from po_core.tensors.metrics.semantic_delta import encode_texts

    detector = EmergenceDetector()
    signals = detector.detect(baseline_proposals, current_proposals, round_num=2)
    for sig in signals:
        print(sig.novelty_score, sig.source_philosopher)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

import numpy as np

from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.domain.proposal import Proposal

# ── Cosine helpers ────────────────────────────────────────────────────


def _cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    """1 − cosine_similarity, clamped to [0, 1]."""
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a < 1e-10 or norm_b < 1e-10:
        return 1.0
    sim = float(np.dot(a, b) / (norm_a * norm_b))
    return float(np.clip(1.0 - sim, 0.0, 1.0))


def _keyword_embed(texts: List[str]) -> np.ndarray:
    """
    Lightweight keyword-bag embedding when sentence-transformers is absent.

    Builds a vocabulary from all texts and returns normalised TF vectors.
    Sufficient for unit tests; sbert backend is preferred in production.
    """
    import re

    def tokenise(t: str) -> List[str]:
        return re.findall(r"[a-z]+", t.lower())

    vocab: dict[str, int] = {}
    token_lists = [tokenise(t) for t in texts]
    for toks in token_lists:
        for tok in toks:
            if tok not in vocab:
                vocab[tok] = len(vocab)

    dim = max(len(vocab), 1)
    vecs = np.zeros((len(texts), dim), dtype=float)
    for i, toks in enumerate(token_lists):
        for tok in toks:
            vecs[i, vocab[tok]] += 1.0
        # L2-normalise
        n = np.linalg.norm(vecs[i])
        if n > 1e-10:
            vecs[i] /= n
    return vecs


def _encode(texts: List[str]) -> np.ndarray:
    """Encode texts to embeddings using best available backend."""
    try:
        from po_core.tensors.metrics.semantic_delta import encode_texts

        return encode_texts(texts)
    except Exception:
        return _keyword_embed(texts)


# ── Data classes ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class EmergenceSignal:
    """
    A detected emergence event for a single proposal.

    Attributes:
        novelty_score:       Cosine distance from nearest baseline proposal [0, 1].
        source_philosopher:  Author of the emergent proposal.
        catalyst_pair:       Two philosophers whose interaction most likely triggered
                             emergence (highest pairwise novelty contribution).
                             Empty strings if only one philosopher was involved.
        round_detected:      Deliberation round in which emergence was detected.
    """

    novelty_score: float
    source_philosopher: str
    catalyst_pair: Tuple[str, str]
    round_detected: int

    def is_strong(self, strong_threshold: float = 0.85) -> bool:
        """Return True if novelty_score exceeds the strong-emergence threshold."""
        return self.novelty_score >= strong_threshold


# ── EmergenceDetector ─────────────────────────────────────────────────


class EmergenceDetector:
    """
    Detects genuine philosophical emergence across deliberation rounds.

    Args:
        threshold:   Minimum novelty_score to report as emergence (default 0.65).
        strong_threshold: Score above which emergence is "strong" / pipeline-halting
                         (default 0.85). Passed through to EmergenceSignal.is_strong().
    """

    def __init__(
        self,
        threshold: float = 0.65,
        strong_threshold: float = 0.85,
    ) -> None:
        self.threshold = threshold
        self.strong_threshold = strong_threshold

    # ── Public API ────────────────────────────────────────────────────

    def detect(
        self,
        baseline_proposals: Sequence[Proposal],
        current_proposals: Sequence[Proposal],
        round_num: int,
    ) -> List[EmergenceSignal]:
        """
        Compare *current_proposals* to *baseline_proposals* and return
        EmergenceSignals for any proposal whose novelty exceeds threshold.

        Args:
            baseline_proposals: Proposals from round 1 (reference set).
            current_proposals:  Proposals from the current round.
            round_num:          Round number (for the signal record).

        Returns:
            List of EmergenceSignal, sorted by novelty_score descending.
        """
        if not baseline_proposals or not current_proposals:
            return []

        baseline_texts = [p.content for p in baseline_proposals]
        current_texts = [p.content for p in current_proposals]

        # Encode both sets in one call (batch efficiency)
        all_texts = baseline_texts + current_texts
        all_vecs = _encode(all_texts)

        base_vecs = all_vecs[: len(baseline_texts)]
        curr_vecs = all_vecs[len(baseline_texts) :]

        baseline_authors = [_get_author(p) for p in baseline_proposals]

        signals: List[EmergenceSignal] = []
        for i, (proposal, vec) in enumerate(zip(current_proposals, curr_vecs)):
            # Novelty = distance to NEAREST baseline proposal.
            # A proposal is emergent only when it is far from ALL baselines.
            # min(distances) = distance to the best-matching baseline.
            distances = [_cosine_distance(vec, bv) for bv in base_vecs]
            min_dist = float(min(distances)) if distances else 0.0

            if min_dist < self.threshold:
                continue

            # Catalyst = the baseline proposal MOST different from the new one;
            # the "challenging" counterpart that sparked the novel synthesis.
            farthest_idx = int(np.argmax(distances))
            catalyst_author = baseline_authors[farthest_idx] if baseline_authors else ""
            source = _get_author(proposal)

            signals.append(
                EmergenceSignal(
                    novelty_score=round(min_dist, 4),
                    source_philosopher=source,
                    catalyst_pair=(source, catalyst_author),
                    round_detected=round_num,
                )
            )

        signals.sort(key=lambda s: s.novelty_score, reverse=True)
        return signals

    def has_strong_emergence(self, signals: List[EmergenceSignal]) -> bool:
        """Return True if any signal is above strong_threshold."""
        return any(s.is_strong(self.strong_threshold) for s in signals)


# ── Helpers ───────────────────────────────────────────────────────────


def _get_author(proposal: Proposal) -> str:
    """Extract philosopher name from proposal.extra."""
    extra = proposal.extra if isinstance(proposal.extra, dict) else {}
    pc = extra.get(PO_CORE, {})
    return pc.get(AUTHOR, "") or extra.get("philosopher", "")
