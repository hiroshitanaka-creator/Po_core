"""Deterministic LRU cache for text embeddings."""

from __future__ import annotations

import os
from collections import OrderedDict
from dataclasses import dataclass

import numpy as np

from po_core.text.normalize import normalize_text


def _read_cache_size() -> int:
    raw = os.getenv("PO_EMBEDDING_CACHE_SIZE", "256").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 256


@dataclass
class EmbeddingCacheStats:
    hits: int = 0
    misses: int = 0


class EmbeddingLRUCache:
    """Small deterministic LRU cache keyed by normalized text + model_id."""

    def __init__(self, max_size: int | None = None) -> None:
        self._max_size = _read_cache_size() if max_size is None else max(0, max_size)
        self._cache: OrderedDict[str, np.ndarray] = OrderedDict()
        self._stats = EmbeddingCacheStats()

    @property
    def max_size(self) -> int:
        return self._max_size

    def set_max_size(self, value: int) -> None:
        self._max_size = max(0, value)
        self._trim()

    def make_key(self, text: str, model_id: str) -> str:
        return f"{model_id}::{normalize_text(text)}"

    def get(self, text: str, model_id: str) -> np.ndarray | None:
        key = self.make_key(text, model_id)
        if key not in self._cache:
            self._stats.misses += 1
            return None
        self._cache.move_to_end(key)
        self._stats.hits += 1
        return np.array(self._cache[key], copy=True)

    def put(self, text: str, model_id: str, value: np.ndarray) -> None:
        if self._max_size <= 0:
            return
        key = self.make_key(text, model_id)
        self._cache[key] = np.array(value, copy=True)
        self._cache.move_to_end(key)
        self._trim()

    def clear(self) -> None:
        self._cache.clear()
        self._stats = EmbeddingCacheStats()

    def stats(self) -> EmbeddingCacheStats:
        return EmbeddingCacheStats(hits=self._stats.hits, misses=self._stats.misses)

    def _trim(self) -> None:
        while len(self._cache) > self._max_size:
            self._cache.popitem(last=False)


GLOBAL_EMBEDDING_CACHE = EmbeddingLRUCache()


__all__ = ["EmbeddingLRUCache", "EmbeddingCacheStats", "GLOBAL_EMBEDDING_CACHE"]
