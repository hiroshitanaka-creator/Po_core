"""
Semantic Memory Store  (Phase 6-D)
===================================

意味記憶: 抽象化された哲学的概念知識の蓄積・検索。

人間の哲学者が「正義に関する議論では Aristotle と Rawls がよく対立する」
という知識を持つように、Po_core が繰り返す議論から概念レベルの知識を
抽出して保持する。

Architecture:
  SemanticMemoryEntry — 1つの哲学的概念の知識エントリ
  SemanticMemoryStore — エントリ群の管理・コサイン近傍検索

Usage::

    store = SemanticMemoryStore()
    entry = SemanticMemoryEntry(
        concept="justice",
        associated_philosophers=["Rawls", "Aristotle"],
        typical_tensions=[("Kant", "Nietzsche", 0.82)],
    )
    store.add(entry)
    results = store.search_by_text("What is distributive justice?", top_k=3)
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

import numpy as np

# ── Shared encoder (keyword-bag fallback) ────────────────────────────


def _keyword_embed(texts: List[str]) -> np.ndarray:
    """Lightweight keyword-bag encoder with shared vocabulary."""
    vocab: Dict[str, int] = {}
    token_lists = [re.findall(r"[a-z]+", t.lower()) for t in texts]
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


def _encode(texts: List[str]) -> np.ndarray:
    """Encode texts to embeddings using best available backend."""
    try:
        from po_core.tensors.metrics.semantic_delta import encode_texts

        return encode_texts(texts)
    except Exception:
        return _keyword_embed(texts)


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.clip(np.dot(a, b) / (na * nb), -1.0, 1.0))


# ── SemanticMemoryEntry ───────────────────────────────────────────────


@dataclass
class SemanticMemoryEntry:
    """
    One philosophical concept in semantic memory.

    Attributes:
        concept:                 Central concept / topic keyword.
        entry_id:                Unique identifier (auto-generated).
        associated_philosophers: Philosophers that appear in discussions of this concept.
        typical_tensions:        (philo_a, philo_b, tension_score) triples observed.
        formation_count:         Times this concept was reinforced by new discussions.
        last_activated:          Timestamp of most recent access or update.
        confidence:              0–1 reliability of this knowledge entry.
        _embedding:              Internal vector (set by store; not user-facing).
    """

    concept: str
    entry_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    associated_philosophers: List[str] = field(default_factory=list)
    typical_tensions: List[Tuple[str, str, float]] = field(default_factory=list)
    formation_count: int = 1
    last_activated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: float = 0.5
    _embedding: Optional[np.ndarray] = field(default=None, repr=False, compare=False)

    # ── Mutation helpers ──────────────────────────────────────────────

    def reinforce(
        self, additional_philosophers: List[str] = (), confidence_boost: float = 0.05
    ) -> None:
        """Increment formation_count and merge new philosopher associations."""
        self.formation_count += 1
        self.last_activated = datetime.now(timezone.utc)
        for ph in additional_philosophers:
            if ph and ph not in self.associated_philosophers:
                self.associated_philosophers.append(ph)
        self.confidence = min(1.0, self.confidence + confidence_boost)

    def add_tension(self, philo_a: str, philo_b: str, score: float) -> None:
        """Record or update a tension pair. Latest value wins."""
        self.typical_tensions = [
            t
            for t in self.typical_tensions
            if not (t[0] in (philo_a, philo_b) and t[1] in (philo_a, philo_b))
        ]
        self.typical_tensions.append((philo_a, philo_b, round(score, 4)))

    # ── Serialisation ─────────────────────────────────────────────────

    def to_dict(self) -> Dict:
        return {
            "concept": self.concept,
            "entry_id": self.entry_id,
            "associated_philosophers": list(self.associated_philosophers),
            "typical_tensions": [list(t) for t in self.typical_tensions],
            "formation_count": self.formation_count,
            "last_activated": self.last_activated.isoformat(),
            "confidence": round(self.confidence, 4),
        }


# ── SemanticMemoryStore ───────────────────────────────────────────────


class SemanticMemoryStore:
    """
    In-memory semantic knowledge store with cosine similarity search.

    Entries are indexed by concept name (exact lookup) and by embedding
    (approximate nearest-neighbour via cosine similarity).
    """

    def __init__(self) -> None:
        self._entries: Dict[str, SemanticMemoryEntry] = {}  # concept → entry

    # ── Mutation ──────────────────────────────────────────────────────

    def add(self, entry: SemanticMemoryEntry) -> None:
        """
        Add a new entry or reinforce an existing one with the same concept.

        If concept already exists, existing entry is reinforced with the
        new entry's philosophers and tensions rather than replaced.
        """
        if entry.concept in self._entries:
            existing = self._entries[entry.concept]
            existing.reinforce(entry.associated_philosophers)
            for t in entry.typical_tensions:
                existing.add_tension(t[0], t[1], t[2])
        else:
            self._entries[entry.concept] = entry

    def consolidate(
        self,
        concept: str,
        philosophers: Optional[List[str]] = None,
        tension: Optional[Tuple[str, str, float]] = None,
        confidence_boost: float = 0.05,
    ) -> SemanticMemoryEntry:
        """
        Create or reinforce a concept entry incrementally.

        Returns the updated entry.
        """
        if concept not in self._entries:
            self._entries[concept] = SemanticMemoryEntry(
                concept=concept,
                associated_philosophers=list(philosophers or []),
                confidence=0.3,
            )
        else:
            self._entries[concept].reinforce(philosophers or [], confidence_boost)
        if tension is not None:
            self._entries[concept].add_tension(*tension)
        return self._entries[concept]

    # ── Search ────────────────────────────────────────────────────────

    def get(self, concept: str) -> Optional[SemanticMemoryEntry]:
        """Exact concept lookup."""
        return self._entries.get(concept)

    def search_by_text(
        self, query: str, top_k: int = 5
    ) -> List[Tuple[SemanticMemoryEntry, float]]:
        """
        Return top_k entries most semantically similar to query text.

        Returns:
            List of (entry, similarity_score) sorted by score descending.
        """
        if not self._entries or not query:
            return []
        concepts = list(self._entries.keys())
        all_texts = [query] + concepts
        vecs = _encode(all_texts)
        query_vec = vecs[0]
        concept_vecs = vecs[1:]
        scored = [
            (self._entries[c], _cosine_sim(query_vec, cv))
            for c, cv in zip(concepts, concept_vecs)
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def search_by_embedding(
        self, query_vec: np.ndarray, top_k: int = 5
    ) -> List[Tuple[SemanticMemoryEntry, float]]:
        """
        Search by a pre-computed embedding vector.

        Returns:
            List of (entry, similarity_score) sorted descending.
        """
        if not self._entries:
            return []
        concepts = list(self._entries.keys())
        concept_texts = concepts
        vecs = _encode(concept_texts)
        scored = [
            (self._entries[c], _cosine_sim(query_vec, cv))
            for c, cv in zip(concepts, vecs)
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def high_confidence_entries(
        self, threshold: float = 0.7
    ) -> List[SemanticMemoryEntry]:
        """Return entries with confidence >= threshold."""
        return [e for e in self._entries.values() if e.confidence >= threshold]

    # ── Inspection ────────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._entries)

    def all_entries(self) -> List[SemanticMemoryEntry]:
        return list(self._entries.values())

    def to_dict(self) -> Dict:
        return {c: e.to_dict() for c, e in self._entries.items()}

    def reset(self) -> None:
        self._entries.clear()
