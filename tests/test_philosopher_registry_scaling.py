"""
Philosopher Registry Scaling Test
==================================

Tests the 1→5→39 philosopher scaling based on SafetyMode.
"""
from __future__ import annotations

import pytest

from po_core.domain.safety_mode import SafetyMode
from po_core.philosophers.registry import PhilosopherRegistry, Selection
from po_core.philosophers.manifest import SPECS, PhilosopherSpec


class TestPhilosopherRegistrySelection:
    """Test SafetyMode-based selection logic."""

    def test_critical_mode_selects_one(self):
        """CRITICAL mode should select only 1 philosopher (safest)."""
        registry = PhilosopherRegistry()
        selection = registry.select(SafetyMode.CRITICAL)

        assert selection.mode == SafetyMode.CRITICAL
        assert len(selection.selected_ids) == 1
        # Should be a risk_level=0 philosopher
        spec = next(s for s in SPECS if s.philosopher_id == selection.selected_ids[0])
        assert spec.risk_level == 0

    def test_warn_mode_selects_five(self):
        """WARN mode should select 5 philosophers."""
        registry = PhilosopherRegistry()
        selection = registry.select(SafetyMode.WARN)

        assert selection.mode == SafetyMode.WARN
        assert len(selection.selected_ids) == 5
        # All should be risk_level <= 1
        for pid in selection.selected_ids:
            spec = next(s for s in SPECS if s.philosopher_id == pid)
            assert spec.risk_level <= 1

    def test_normal_mode_selects_all(self):
        """NORMAL mode should select up to 39 philosophers."""
        registry = PhilosopherRegistry(max_normal=39)
        selection = registry.select(SafetyMode.NORMAL)

        assert selection.mode == SafetyMode.NORMAL
        # Should select many philosophers (up to available)
        assert len(selection.selected_ids) > 5

    def test_unknown_mode_treated_as_warn(self):
        """UNKNOWN mode should be treated as WARN (fail-safe)."""
        registry = PhilosopherRegistry()
        selection = registry.select(SafetyMode.UNKNOWN)

        assert selection.mode == SafetyMode.UNKNOWN
        assert len(selection.selected_ids) == 5
        # All should be risk_level <= 1
        for pid in selection.selected_ids:
            spec = next(s for s in SPECS if s.philosopher_id == pid)
            assert spec.risk_level <= 1

    def test_selection_order_is_stable(self):
        """Same mode should always select same philosophers in same order."""
        registry = PhilosopherRegistry()

        sel1 = registry.select(SafetyMode.WARN)
        sel2 = registry.select(SafetyMode.WARN)

        assert sel1.selected_ids == sel2.selected_ids

    def test_selection_prioritizes_weight(self):
        """Higher weight philosophers should be selected first within risk tier."""
        registry = PhilosopherRegistry()
        selection = registry.select(SafetyMode.CRITICAL)

        # Find the selected philosopher's weight
        selected_spec = next(s for s in SPECS if s.philosopher_id == selection.selected_ids[0])

        # Should have high weight among risk_level=0
        risk0_specs = [s for s in SPECS if s.risk_level == 0 and s.enabled]
        max_weight = max(s.weight for s in risk0_specs)
        assert selected_spec.weight == max_weight


class TestPhilosopherRegistryLoading:
    """Test philosopher loading from selection."""

    def test_load_returns_instances(self):
        """load() should return philosopher instances and errors."""
        registry = PhilosopherRegistry()
        selection = registry.select(SafetyMode.CRITICAL)

        philosophers, errors = registry.load(selection.selected_ids)

        assert len(philosophers) >= 1
        # Should be a valid philosopher instance
        ph = philosophers[0]
        assert hasattr(ph, "deliberate") or hasattr(ph, "propose")

    def test_select_and_load_convenience(self):
        """select_and_load() should combine both operations."""
        registry = PhilosopherRegistry()

        philosophers = registry.select_and_load(SafetyMode.WARN)

        # At least 1 philosopher should be loaded (cost budget limits selection)
        assert len(philosophers) >= 1

    def test_caching_returns_same_instance(self):
        """Cached instances should be reused."""
        registry = PhilosopherRegistry(cache_instances=True)

        phs1 = registry.select_and_load(SafetyMode.CRITICAL)
        phs2 = registry.select_and_load(SafetyMode.CRITICAL)

        assert phs1[0] is phs2[0]

    def test_no_caching_returns_different_instances(self):
        """Without caching, new instances should be created."""
        registry = PhilosopherRegistry(cache_instances=False)

        phs1 = registry.select_and_load(SafetyMode.CRITICAL)
        phs2 = registry.select_and_load(SafetyMode.CRITICAL)

        assert phs1[0] is not phs2[0]


class TestPhilosopherRegistryCustomization:
    """Test registry customization."""

    def test_custom_limits(self):
        """Custom limits should override defaults."""
        registry = PhilosopherRegistry(
            max_critical=2,
            max_warn=3,
            max_normal=10,
        )

        assert len(registry.select(SafetyMode.CRITICAL).selected_ids) == 2
        assert len(registry.select(SafetyMode.WARN).selected_ids) == 3
        assert len(registry.select(SafetyMode.NORMAL).selected_ids) == 10

    def test_custom_specs(self):
        """Custom specs should be used instead of defaults."""
        custom_specs = [
            PhilosopherSpec("test1", "po_core.philosophers.dummy", "DummyPhilosopher", risk_level=0),
            PhilosopherSpec("test2", "po_core.philosophers.dummy", "DummyPhilosopher", risk_level=0),
        ]
        registry = PhilosopherRegistry(specs=custom_specs, max_critical=1)

        selection = registry.select(SafetyMode.CRITICAL)
        assert selection.selected_ids == ["test1"]


class TestScalingRatios:
    """Test the 1→5→39 scaling pattern."""

    def test_scaling_ratio(self):
        """Verify the 1:5:39 scaling ratio."""
        registry = PhilosopherRegistry(
            max_critical=1,
            max_warn=5,
            max_normal=39,
        )

        critical = registry.select(SafetyMode.CRITICAL)
        warn = registry.select(SafetyMode.WARN)
        normal = registry.select(SafetyMode.NORMAL)

        # Exact counts may vary based on available philosophers
        assert len(critical.selected_ids) == 1
        assert len(warn.selected_ids) == 5
        # Normal gets all enabled philosophers up to limit
        assert len(normal.selected_ids) <= 39

    def test_risk_level_filtering(self):
        """Verify risk level filtering per mode."""
        registry = PhilosopherRegistry()

        critical_ids = set(registry.select(SafetyMode.CRITICAL).selected_ids)
        warn_ids = set(registry.select(SafetyMode.WARN).selected_ids)
        normal_ids = set(registry.select(SafetyMode.NORMAL).selected_ids)

        # CRITICAL is subset of WARN which is subset of NORMAL (in terms of risk)
        for pid in critical_ids:
            spec = next(s for s in SPECS if s.philosopher_id == pid)
            assert spec.risk_level == 0, "CRITICAL should only have risk_level=0"

        for pid in warn_ids:
            spec = next(s for s in SPECS if s.philosopher_id == pid)
            assert spec.risk_level <= 1, "WARN should only have risk_level<=1"


class TestManifestIntegrity:
    """Test manifest data integrity."""

    def test_specs_count(self):
        """Should have expected number of philosopher specs."""
        # Including dummy, we have 40 specs total
        assert len(SPECS) >= 39, "Should have at least 39 philosophers"

    def test_specs_have_required_fields(self):
        """All specs should have required fields."""
        for spec in SPECS:
            assert spec.philosopher_id
            assert spec.module
            assert spec.symbol
            assert spec.risk_level in (0, 1, 2)
            assert spec.weight > 0

    def test_unique_ids(self):
        """All philosopher IDs should be unique."""
        ids = [s.philosopher_id for s in SPECS]
        assert len(ids) == len(set(ids)), "Duplicate philosopher IDs found"

    def test_risk_level_distribution(self):
        """Should have philosophers across all risk levels."""
        by_risk = {0: [], 1: [], 2: []}
        for spec in SPECS:
            by_risk[spec.risk_level].append(spec.philosopher_id)

        assert len(by_risk[0]) >= 1, "Need at least 1 risk_level=0 philosopher"
        assert len(by_risk[1]) >= 1, "Need at least 1 risk_level=1 philosopher"
        # risk_level=2 is optional but good to have
