"""
Phase 6-C1: Position Clustering Tests
=======================================

Tests for:
  - ClusterResult dataclass
  - PositionClusterer (SpectralClustering + auto-k via silhouette)
  - DeliberationEngine.cluster_result integration
  - ClusteringCompleted TraceEvent schema registration

Markers: phase6c1
"""

from __future__ import annotations

import uuid
from typing import List

import numpy as np
import pytest

from po_core.deliberation.clustering import ClusterResult, PositionClusterer
from po_core.deliberation.engine import DeliberationEngine
from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot

pytestmark = pytest.mark.phase6c1


# ── Helpers ─────────────────────────────────────────────────────────────────


def _ctx(text: str = "What is the nature of reality?") -> Context:
    return Context.now(request_id=str(uuid.uuid4()), user_input=text)


def _intent() -> Intent:
    return Intent.neutral()


def _tensors() -> TensorSnapshot:
    return TensorSnapshot.now({"freedom_pressure": 0.0})


def _memory() -> MemorySnapshot:
    return MemorySnapshot(items=[], summary=None, meta={})


def _proposal(name: str, content: str) -> Proposal:
    return Proposal(
        proposal_id=f"test:{name}:0",
        action_type="answer",
        content=content,
        confidence=0.5,
        extra={"_po_core": {"author": name}, "philosopher": name},
    )


def _two_group_harmony(n_a: int = 3, n_b: int = 3) -> tuple:
    """Build a clear two-cluster harmony matrix.

    Group A has high mutual harmony (0.92) and low harmony (0.05) with group B.
    Returns (harmony_matrix: ndarray, names: list[str]).
    """
    n = n_a + n_b
    names = [f"A{i}" for i in range(n_a)] + [f"B{i}" for i in range(n_b)]
    H = np.full((n, n), 0.05)  # low cross-group harmony
    np.fill_diagonal(H, 1.0)
    # Intra-group A
    for i in range(n_a):
        for j in range(n_a):
            H[i, j] = 0.92
    # Intra-group B
    for i in range(n_a, n):
        for j in range(n_a, n):
            H[i, j] = 0.92
    np.fill_diagonal(H, 1.0)
    return H, names


# ── TestClusterResult ────────────────────────────────────────────────────────


class TestClusterResult:
    def test_default_values(self):
        cr = ClusterResult()
        assert cr.clusters == {}
        assert cr.n_clusters == 1
        assert cr.silhouette == 0.0

    def test_members_returns_correct_list(self):
        cr = ClusterResult(
            clusters={0: ["Hegel", "Kant"], 1: ["Nietzsche"]},
            n_clusters=2,
            silhouette=0.7,
        )
        assert cr.members(0) == ["Hegel", "Kant"]
        assert cr.members(1) == ["Nietzsche"]

    def test_members_returns_empty_for_unknown_cluster(self):
        cr = ClusterResult(clusters={0: ["Hegel"]}, n_clusters=1, silhouette=0.0)
        assert cr.members(99) == []

    def test_cluster_of_returns_correct_id(self):
        cr = ClusterResult(
            clusters={0: ["Hegel", "Kant"], 1: ["Nietzsche", "Sartre"]},
            n_clusters=2,
            silhouette=0.6,
        )
        assert cr.cluster_of("Hegel") == 0
        assert cr.cluster_of("Nietzsche") == 1

    def test_cluster_of_returns_none_for_unknown(self):
        cr = ClusterResult(clusters={0: ["Hegel"]}, n_clusters=1, silhouette=0.0)
        assert cr.cluster_of("Plato") is None

    def test_all_names_returns_all_philosophers(self):
        cr = ClusterResult(
            clusters={0: ["Hegel", "Kant"], 1: ["Nietzsche"]},
            n_clusters=2,
            silhouette=0.5,
        )
        names = cr.all_names()
        assert set(names) == {"Hegel", "Kant", "Nietzsche"}

    def test_to_dict_has_required_keys(self):
        cr = ClusterResult(
            clusters={0: ["A", "B"], 1: ["C"]},
            n_clusters=2,
            silhouette=0.65,
        )
        d = cr.to_dict()
        assert "n_clusters" in d
        assert "cluster_sizes" in d
        assert "silhouette" in d
        assert "clusters" in d

    def test_to_dict_cluster_sizes_match(self):
        cr = ClusterResult(
            clusters={0: ["A", "B"], 1: ["C", "D", "E"]},
            n_clusters=2,
            silhouette=0.7,
        )
        d = cr.to_dict()
        assert d["cluster_sizes"]["0"] == 2
        assert d["cluster_sizes"]["1"] == 3


# ── TestPositionClusterer ────────────────────────────────────────────────────


class TestPositionClusterer:
    def test_empty_names_returns_empty_clusters(self):
        clusterer = PositionClusterer()
        H = np.zeros((0, 0))
        result = clusterer.cluster(H, [])
        assert result.n_clusters == 0
        assert result.clusters == {}

    def test_single_philosopher_returns_one_cluster(self):
        clusterer = PositionClusterer()
        H = np.array([[1.0]])
        result = clusterer.cluster(H, ["Hegel"])
        assert result.n_clusters == 1
        assert "Hegel" in result.members(0)

    def test_two_group_structure_produces_two_clusters(self):
        """Clear 2-group harmony → exactly 2 clusters should be detected."""
        H, names = _two_group_harmony(n_a=3, n_b=3)
        clusterer = PositionClusterer(k_min=2, k_max=4)
        result = clusterer.cluster(H, names)
        assert result.n_clusters == 2

    def test_all_philosophers_are_assigned(self):
        """Every philosopher name appears in exactly one cluster."""
        H, names = _two_group_harmony(n_a=3, n_b=3)
        clusterer = PositionClusterer(k_min=2, k_max=4)
        result = clusterer.cluster(H, names)
        all_assigned = result.all_names()
        assert set(all_assigned) == set(names)

    def test_cluster_count_within_bounds(self):
        """Cluster count must be within [k_min, k_max] or fallback to 1."""
        H, names = _two_group_harmony(n_a=4, n_b=4)
        clusterer = PositionClusterer(k_min=2, k_max=3)
        result = clusterer.cluster(H, names)
        assert result.n_clusters in (1, 2, 3)

    def test_two_philosophers_handled_gracefully(self):
        """n=2 is a degenerate case; should not raise."""
        H = np.array([[1.0, 0.1], [0.1, 1.0]])
        clusterer = PositionClusterer()
        result = clusterer.cluster(H, ["A", "B"])
        # Either 1 or 2 clusters — just no crash
        assert result.n_clusters in (1, 2)

    def test_silhouette_is_float(self):
        H, names = _two_group_harmony(n_a=3, n_b=3)
        clusterer = PositionClusterer()
        result = clusterer.cluster(H, names)
        assert isinstance(result.silhouette, float)


# ── TestDeliberationResultClustering ─────────────────────────────────────────


class TestDeliberationResultClustering:
    def test_cluster_result_is_none_by_default(self):
        """Without enable_clustering, cluster_result should be None."""
        proposals = [
            _proposal("Alpha", "Free will exists."),
            _proposal("Beta", "Determinism is true."),
        ]
        engine = DeliberationEngine(
            max_rounds=1, detect_emergence=False, track_influence=False
        )
        result = engine.deliberate(
            [], _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        assert result.cluster_result is None

    def test_cluster_result_is_set_when_enabled(self):
        """With enable_clustering=True, cluster_result should be a ClusterResult."""
        proposals = [
            _proposal("Alpha", "Free will exists."),
            _proposal("Beta", "Determinism is true."),
        ]
        engine = DeliberationEngine(
            max_rounds=1,
            detect_emergence=False,
            track_influence=False,
            enable_clustering=True,
        )
        result = engine.deliberate(
            [], _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        assert result.cluster_result is not None
        assert isinstance(result.cluster_result, ClusterResult)

    def test_cluster_result_covers_all_proposals(self):
        """All philosophers from round-1 proposals appear in cluster_result."""
        proposals = [
            _proposal("Alpha", "Virtue is the highest good."),
            _proposal("Beta", "Power is the highest good."),
            _proposal("Gamma", "Happiness is the highest good."),
        ]
        engine = DeliberationEngine(
            max_rounds=1,
            detect_emergence=False,
            track_influence=False,
            enable_clustering=True,
        )
        result = engine.deliberate(
            [], _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        assert result.cluster_result is not None
        assigned = set(result.cluster_result.all_names())
        assert assigned == {"Alpha", "Beta", "Gamma"}

    def test_summary_includes_clustering_key(self):
        """summary() must include a 'clustering' key when cluster_result is set."""
        proposals = [
            _proposal("Alpha", "Being is primary."),
            _proposal("Beta", "Becoming is primary."),
        ]
        engine = DeliberationEngine(
            max_rounds=1,
            detect_emergence=False,
            track_influence=False,
            enable_clustering=True,
        )
        result = engine.deliberate(
            [], _ctx(), _intent(), _tensors(), _memory(), proposals
        )
        s = result.summary()
        assert "clustering" in s
        assert s["clustering"] is not None


# ── TestClusteringCompletedSchema ─────────────────────────────────────────────


class TestClusteringCompletedSchema:
    def test_clustering_completed_event_spec_registered(self):
        """ClusteringCompleted must be registered in trace schema SPECS."""
        from po_core.trace.schema import SPECS

        event_types = {s.event_type for s in SPECS}
        assert "ClusteringCompleted" in event_types

    def test_cluster_result_to_dict_satisfies_schema_keys(self):
        """ClusterResult.to_dict() must contain all keys required by ClusteringCompleted spec."""
        from po_core.trace.schema import _get_spec

        spec = _get_spec("ClusteringCompleted")
        assert spec is not None

        cr = ClusterResult(
            clusters={0: ["Hegel"], 1: ["Nietzsche"]},
            n_clusters=2,
            silhouette=0.75,
        )
        payload = cr.to_dict()
        for key in spec.required_keys:
            assert key in payload, f"Missing required key: {key}"
