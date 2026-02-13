"""
Tests for Phase 3 Plotly figures: tension heatmap and evolution timeline.
"""

import pytest

from po_core.viewer.web.figures import build_evolution_timeline, build_tension_heatmap

pytestmark = [pytest.mark.unit, pytest.mark.observability]


class TestTensionHeatmap:
    """build_tension_heatmap produces valid Plotly figures."""

    def test_with_data(self):
        philosophers = ["Aristotle", "Kant", "Nietzsche"]
        tension = [[0, 0.3, 0.8], [0.3, 0, 0.5], [0.8, 0.5, 0]]

        fig = build_tension_heatmap(philosophers, tension)
        assert fig is not None
        assert len(fig.data) >= 1
        assert fig.data[0].type == "heatmap"

    def test_with_harmony(self):
        philosophers = ["A", "B"]
        tension = [[0, 0.5], [0.5, 0]]
        harmony = [[0, 0.9], [0.9, 0]]

        fig = build_tension_heatmap(philosophers, tension, harmony_matrix=harmony)
        assert fig is not None
        assert len(fig.data) == 2  # two heatmaps (subplots)

    def test_empty_data(self):
        fig = build_tension_heatmap([], [])
        assert fig is not None
        # Should show annotation "No tension data"
        assert len(fig.layout.annotations) > 0

    def test_no_philosophers(self):
        fig = build_tension_heatmap([], [[0.5]])
        assert fig is not None


class TestEvolutionTimeline:
    """build_evolution_timeline produces valid Plotly polar chart."""

    def test_with_data(self):
        dims = ["abstract_level", "emotional_valence", "novelty", "depth"]
        vals = [0.7, 0.5, 0.8, 0.3]

        fig = build_evolution_timeline(dims, vals, total_evolution=0.35, history_length=5)
        assert fig is not None
        assert len(fig.data) >= 1
        assert fig.data[0].type == "scatterpolar"
        # Values should close the polygon (len + 1)
        assert len(fig.data[0].r) == len(dims) + 1

    def test_empty_data(self):
        fig = build_evolution_timeline([], [])
        assert fig is not None
        assert len(fig.layout.annotations) > 0

    def test_single_dimension(self):
        fig = build_evolution_timeline(["depth"], [0.6])
        assert fig is not None

    def test_title_includes_stats(self):
        fig = build_evolution_timeline(
            ["a", "b"], [0.5, 0.5], total_evolution=0.2, history_length=3
        )
        assert "3 steps" in fig.layout.title.text
        assert "0.200" in fig.layout.title.text
