"""
Influence Weight Tracker
========================

Tracks how much each philosopher's proposals change other philosophers'
subsequent re-proposals during deliberation.

"Influence" is measured as the cosine distance between a philosopher's
original proposal and the revised proposal of each philosopher who received
it as a counterargument. A high influence score means the philosopher's
ideas forced others to move significantly.

Usage::

    from po_core.deliberation.influence import InfluenceTracker

    tracker = InfluenceTracker()
    # After round 1 (original proposals):
    tracker.set_baseline(round1_proposals)
    # After round 2 (revised proposals):
    tracker.update(round2_proposals, counterargument_map)

    weights = tracker.weights()          # dict[philosopher_id → InfluenceWeight]
    top = tracker.top_influencers(n=3)   # sorted list of (name, total_influence)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple

import numpy as np

from po_core.domain.keys import AUTHOR
from po_core.domain.proposal import Proposal

# ── Reuse the same encoder as EmergenceDetector ───────────────────────

try:
    from po_core.deliberation.emergence import _encode, _get_author
except ImportError:
    # Fallback (shouldn't happen in production)
    def _get_author(proposal: "Proposal") -> str:  # type: ignore[misc]
        extra = proposal.extra if isinstance(proposal.extra, dict) else {}
        return extra.get(AUTHOR, "") or extra.get("philosopher", "")

    def _encode(texts: List[str]) -> np.ndarray:  # type: ignore[misc]
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
            n = np.linalg.norm(vecs[i])
            if n > 1e-10:
                vecs[i] /= n
        return vecs


def _cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na < 1e-10 or nb < 1e-10:
        return 1.0
    return float(np.clip(1.0 - np.dot(a, b) / (na * nb), 0.0, 1.0))


# ── Data classes ──────────────────────────────────────────────────────


@dataclass
class InfluenceWeight:
    """
    Influence record for a single philosopher.

    Attributes:
        philosopher_id: Name of the influencing philosopher.
        influenced:     Map from influenced-philosopher-id → delta_score.
                        delta_score = cosine distance the target's proposal moved
                        after receiving this philosopher's counterargument.
    """

    philosopher_id: str
    influenced: Dict[str, float] = field(default_factory=dict)

    def total_influence(self) -> float:
        """Sum of all delta scores (overall influence strength)."""
        return sum(self.influenced.values())

    def to_dict(self) -> Dict:
        return {
            "philosopher_id": self.philosopher_id,
            "influenced": dict(self.influenced),
            "total_influence": round(self.total_influence(), 4),
        }


# ── InfluenceTracker ──────────────────────────────────────────────────


class InfluenceTracker:
    """
    Tracks philosopher influence across deliberation rounds.

    Workflow:
    1. Call ``set_baseline(round1_proposals)`` before deliberation starts.
    2. After each round, call ``update(revised_proposals, counterarg_map)``
       where counterarg_map is ``{recipient_name: sender_name}``.
    3. Call ``weights()`` or ``top_influencers()`` for results.
    """

    def __init__(self) -> None:
        # Store (name, text) pairs so baseline and revised can be encoded
        # in the same call → shared vocabulary for keyword backend.
        self._baseline_texts: Dict[str, str] = {}  # name → original content
        self._baseline: Dict[str, np.ndarray] = {}  # name → embedding (sbert cache)
        self._weights: Dict[str, InfluenceWeight] = {}

    # ── Setup ─────────────────────────────────────────────────────────

    def set_baseline(self, proposals: Sequence[Proposal]) -> None:
        """
        Store baseline texts for round 1 proposals.

        Embeddings are computed lazily in update() together with revised texts
        so that keyword-bag vectors share a unified vocabulary.

        Must be called before the first update().
        """
        for p in proposals:
            name = _get_author(p)
            if name:
                self._baseline_texts[name] = p.content

    # ── Update ────────────────────────────────────────────────────────

    def update(
        self,
        revised_proposals: Sequence[Proposal],
        counterarg_map: Dict[str, str],
    ) -> None:
        """
        Measure how much each revised proposal moved from its baseline.

        Baseline and revised texts are encoded together in one batch so that
        keyword-bag vectors live in the same vector space.

        Args:
            revised_proposals: Proposals produced in the current round.
            counterarg_map:    ``{recipient_name: sender_name}`` — maps each
                               philosopher who revised their proposal to the
                               philosopher whose argument triggered the revision.
        """
        if not revised_proposals or not self._baseline_texts:
            return

        revised_names = [_get_author(p) for p in revised_proposals]
        revised_texts = [p.content for p in revised_proposals]

        # Only process philosophers who are in the counterarg_map and baseline
        relevant = [
            (name, text)
            for name, text in zip(revised_names, revised_texts)
            if name and name in self._baseline_texts and name in counterarg_map
        ]
        if not relevant:
            return

        # Encode baseline + revised texts in ONE call → shared vocabulary
        rel_names = [n for n, _ in relevant]
        rel_texts = [t for _, t in relevant]
        baseline_texts_for_relevant = [self._baseline_texts[n] for n in rel_names]

        all_texts = baseline_texts_for_relevant + rel_texts
        all_vecs = _encode(all_texts)
        base_vecs = all_vecs[: len(rel_names)]
        curr_vecs = all_vecs[len(rel_names) :]

        for name, base_vec, curr_vec in zip(rel_names, base_vecs, curr_vecs):
            delta = _cosine_distance(curr_vec, base_vec)
            sender = counterarg_map[name]

            # Record influence: sender influenced name by delta
            if sender not in self._weights:
                self._weights[sender] = InfluenceWeight(philosopher_id=sender)
            self._weights[sender].influenced[name] = round(delta, 4)

    # ── Results ───────────────────────────────────────────────────────

    def weights(self) -> Dict[str, InfluenceWeight]:
        """Return all influence weights, keyed by philosopher name."""
        return dict(self._weights)

    def top_influencers(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        Return top-N philosophers by total influence, sorted descending.

        Returns:
            List of (philosopher_name, total_influence_score).
        """
        ranked = [(name, w.total_influence()) for name, w in self._weights.items()]
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked[:n]

    def reset(self) -> None:
        """Clear all state (baseline + weights)."""
        self._baseline_texts.clear()
        self._baseline.clear()
        self._weights.clear()

    def to_dict(self) -> Dict:
        """Serialise all influence weights to a plain dict."""
        return {name: w.to_dict() for name, w in self._weights.items()}
