"""
Position Clustering
====================

Phase 6-C1: harmony 行列から哲学者を「立場クラスタ」に自動分類。

設計:
  harmony NxN 行列 (コサイン類似度)
    → Spectral Clustering (sklearn, affinity="precomputed")
    → k は Silhouette スコアで自動決定 (k=2..6 を試す)
    → ClusterResult: {cluster_id → [philosopher_names]}

後退互換:
  enable_clustering=False (デフォルト) では DeliberationResult.cluster_result=None
  enable_clustering=True で有効化
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np


@dataclass
class ClusterResult:
    """
    Result of philosopher position clustering.

    Attributes:
        clusters: Mapping of cluster_id → list of philosopher names
        n_clusters: Number of clusters found
        silhouette: Best silhouette score achieved [-1.0, 1.0]
                    (0.0 when clustering is trivial or not meaningful)
    """

    clusters: Dict[int, List[str]] = field(default_factory=dict)
    n_clusters: int = 1
    silhouette: float = 0.0

    def members(self, cluster_id: int) -> List[str]:
        """Return philosopher names in a given cluster."""
        return self.clusters.get(cluster_id, [])

    def cluster_of(self, name: str) -> Optional[int]:
        """Return the cluster id that a philosopher belongs to, or None."""
        for cid, members in self.clusters.items():
            if name in members:
                return cid
        return None

    def all_names(self) -> List[str]:
        """Return all philosopher names across all clusters."""
        result = []
        for members in self.clusters.values():
            result.extend(members)
        return result

    def to_dict(self) -> Dict:
        """Serializable summary (suitable for TraceEvent payload)."""
        return {
            "n_clusters": self.n_clusters,
            "silhouette": round(self.silhouette, 4),
            "cluster_sizes": {
                str(cid): len(members) for cid, members in self.clusters.items()
            },
            "clusters": {
                str(cid): list(members) for cid, members in self.clusters.items()
            },
        }


class PositionClusterer:
    """
    Cluster philosopher positions using Spectral Clustering on the harmony matrix.

    The harmony matrix (cosine similarity NxN) is used as a precomputed affinity
    matrix. The optimal number of clusters k ∈ [k_min, k_max] is selected by
    maximizing the Silhouette score on the distance matrix (1 - harmony).

    Args:
        k_min: Minimum number of clusters to try (default 2).
        k_max: Maximum number of clusters to try (default 6).
    """

    def __init__(self, k_min: int = 2, k_max: int = 6) -> None:
        self.k_min = max(2, k_min)
        self.k_max = max(self.k_min, k_max)

    def cluster(
        self,
        harmony: np.ndarray,
        names: List[str],
    ) -> ClusterResult:
        """
        Cluster philosophers by position using the harmony (affinity) matrix.

        Args:
            harmony: NxN cosine similarity matrix (values in [0, 1]).
            names:   List of N philosopher names (same order as matrix rows/cols).

        Returns:
            ClusterResult with best clustering found.
        """
        n = len(names)

        # Trivial cases
        if n == 0:
            return ClusterResult(clusters={}, n_clusters=0, silhouette=0.0)
        if n == 1:
            return ClusterResult(
                clusters={0: list(names)}, n_clusters=1, silhouette=0.0
            )

        # Can't have more clusters than data points - 1 (silhouette needs ≥ 2 clusters)
        k_max_eff = min(self.k_max, n - 1)
        k_min_eff = min(self.k_min, k_max_eff)

        if k_min_eff > k_max_eff or k_min_eff < 2:
            # n == 2 means we can try k=2 but can't compute silhouette (need 2+ samples per cluster)
            # Fallback: put everyone in one cluster
            return ClusterResult(
                clusters={0: list(names)}, n_clusters=1, silhouette=0.0
            )

        # Build distance matrix for silhouette scoring (1 - harmony)
        distance = np.clip(1.0 - np.asarray(harmony, dtype=float), 0.0, 1.0)
        np.fill_diagonal(distance, 0.0)

        # Ensure harmony is a valid affinity matrix (non-negative, symmetric, clipped)
        affinity = np.clip(np.asarray(harmony, dtype=float), 0.0, 1.0)

        best_k = k_min_eff
        best_score = -2.0  # below possible silhouette range [-1, 1]
        best_labels: Optional[np.ndarray] = None

        for k in range(k_min_eff, k_max_eff + 1):
            try:
                from sklearn.cluster import SpectralClustering
                from sklearn.metrics import silhouette_score

                sc = SpectralClustering(
                    n_clusters=k,
                    affinity="precomputed",
                    random_state=42,
                    n_init=10,
                )
                labels = sc.fit_predict(affinity)
                n_unique = len(set(labels))
                if n_unique < 2:
                    # All assigned to same cluster → silhouette undefined
                    continue

                score = silhouette_score(distance, labels, metric="precomputed")

                if score > best_score:
                    best_score = score
                    best_k = k
                    best_labels = labels

            except Exception:
                # sklearn not available or clustering failed → skip this k
                continue

        if best_labels is None:
            # No valid clustering found; put everyone in one group
            return ClusterResult(
                clusters={0: list(names)}, n_clusters=1, silhouette=0.0
            )

        # Build cluster_id → philosopher names mapping
        clusters: Dict[int, List[str]] = {}
        for i, label in enumerate(best_labels):
            cid = int(label)
            clusters.setdefault(cid, []).append(names[i])

        return ClusterResult(
            clusters=clusters,
            n_clusters=best_k,
            silhouette=float(best_score),
        )


__all__ = ["ClusterResult", "PositionClusterer"]
