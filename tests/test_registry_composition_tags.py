"""
Registry Composition Tags Test
==============================

Tests that mode-based composition covers required safety tags.
"""

from __future__ import annotations

import pytest

from po_core.domain.safety_mode import SafetyMode
from po_core.philosophers.manifest import PhilosopherSpec
from po_core.philosophers.registry import PhilosopherRegistry
from po_core.philosophers.tags import (
    TAG_CLARIFY,
    TAG_COMPLIANCE,
    TAG_CREATIVE,
    TAG_CRITIC,
    TAG_PLANNER,
    TAG_REDTEAM,
)


class TestCompositionTags:
    """Test that composition covers required tags."""

    def test_warn_composition_covers_safety_tags(self):
        """WARN mode should cover compliance, clarify, and critic tags."""
        specs = [
            PhilosopherSpec(
                "c",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.0,
                tags=(TAG_COMPLIANCE,),
                cost=1,
            ),
            PhilosopherSpec(
                "q",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.0,
                tags=(TAG_CLARIFY,),
                cost=1,
            ),
            PhilosopherSpec(
                "k",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=1,
                weight=1.0,
                tags=(TAG_CRITIC,),
                cost=1,
            ),
            PhilosopherSpec(
                "p",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=1,
                weight=1.0,
                tags=(TAG_PLANNER,),
                cost=3,
            ),
            PhilosopherSpec(
                "r",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=2,
                weight=1.0,
                tags=(TAG_REDTEAM,),
                cost=3,
            ),
        ]
        reg = PhilosopherRegistry(
            specs, max_warn=5, budget_warn=12, cache_instances=False
        )
        sel = reg.select(SafetyMode.WARN)

        assert TAG_COMPLIANCE in sel.covered_tags
        assert TAG_CLARIFY in sel.covered_tags
        assert TAG_CRITIC in sel.covered_tags

    def test_critical_composition_covers_minimal_tags(self):
        """CRITICAL mode should cover compliance and clarify at minimum."""
        specs = [
            PhilosopherSpec(
                "cq",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=2.0,
                tags=(TAG_COMPLIANCE, TAG_CLARIFY),
                cost=1,
            ),
            PhilosopherSpec(
                "k",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=1,
                weight=1.0,
                tags=(TAG_CRITIC,),
                cost=1,
            ),
        ]
        reg = PhilosopherRegistry(
            specs, max_critical=1, budget_critical=3, cache_instances=False
        )
        sel = reg.select(SafetyMode.CRITICAL)

        # Should select cq which covers both compliance and clarify
        assert len(sel.selected_ids) == 1
        assert TAG_COMPLIANCE in sel.covered_tags
        assert TAG_CLARIFY in sel.covered_tags

    def test_normal_composition_covers_all_required_tags(self):
        """NORMAL mode should cover all required tags including creative and redteam."""
        specs = [
            PhilosopherSpec(
                "a",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.5,
                tags=(TAG_COMPLIANCE, TAG_PLANNER),
                cost=1,
            ),
            PhilosopherSpec(
                "b",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=1,
                weight=1.0,
                tags=(TAG_CRITIC,),
                cost=1,
            ),
            PhilosopherSpec(
                "c",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=1,
                weight=1.0,
                tags=(TAG_CREATIVE,),
                cost=1,
            ),
            PhilosopherSpec(
                "d",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=2,
                weight=1.0,
                tags=(TAG_REDTEAM,),
                cost=2,
            ),
        ]
        reg = PhilosopherRegistry(
            specs, max_normal=10, budget_normal=20, cache_instances=False
        )
        sel = reg.select(SafetyMode.NORMAL)

        # Should cover all required tags
        assert TAG_PLANNER in sel.covered_tags
        assert TAG_CRITIC in sel.covered_tags
        assert TAG_COMPLIANCE in sel.covered_tags
        assert TAG_CREATIVE in sel.covered_tags
        assert TAG_REDTEAM in sel.covered_tags


class TestCostBudget:
    """Test that cost budget is respected."""

    def test_cost_budget_limits_selection(self):
        """Should not exceed cost budget even if limit allows more."""
        specs = [
            PhilosopherSpec(
                "a",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=2.0,
                tags=(TAG_COMPLIANCE, TAG_CLARIFY),
                cost=2,
            ),
            PhilosopherSpec(
                "b",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.5,
                tags=(TAG_CRITIC,),
                cost=2,
            ),
            PhilosopherSpec(
                "c",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.0,
                tags=(TAG_PLANNER,),
                cost=2,
            ),
        ]
        # Budget of 3 should only allow 1 philosopher (cost=2)
        reg = PhilosopherRegistry(
            specs, max_critical=3, budget_critical=3, cache_instances=False
        )
        sel = reg.select(SafetyMode.CRITICAL)

        assert sel.cost_total <= 3
        assert len(sel.selected_ids) == 1

    def test_cost_total_is_accurate(self):
        """cost_total should be sum of selected philosophers' costs."""
        specs = [
            PhilosopherSpec(
                "a",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=2.0,
                tags=(TAG_COMPLIANCE,),
                cost=2,
            ),
            PhilosopherSpec(
                "b",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.5,
                tags=(TAG_CLARIFY,),
                cost=3,
            ),
            PhilosopherSpec(
                "c",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.0,
                tags=(TAG_CRITIC,),
                cost=1,
            ),
        ]
        reg = PhilosopherRegistry(
            specs, max_warn=3, budget_warn=10, cache_instances=False
        )
        sel = reg.select(SafetyMode.WARN)

        # All 3 should be selected (total cost = 6)
        expected_cost = sum(
            s.cost for s in specs if s.philosopher_id in sel.selected_ids
        )
        assert sel.cost_total == expected_cost


class TestTagPrioritization:
    """Test that required tags are prioritized."""

    def test_required_tags_filled_first(self):
        """Required tags should be filled before other candidates."""
        specs = [
            PhilosopherSpec(
                "high_weight",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=10.0,
                tags=(),
                cost=1,  # High weight but no tags
            ),
            PhilosopherSpec(
                "compliance",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.0,
                tags=(TAG_COMPLIANCE,),
                cost=1,
            ),
            PhilosopherSpec(
                "clarify",
                "po_core.philosophers.dummy",
                "DummyPhilosopher",
                risk_level=0,
                weight=1.0,
                tags=(TAG_CLARIFY,),
                cost=1,
            ),
        ]
        reg = PhilosopherRegistry(
            specs, max_critical=2, budget_critical=3, cache_instances=False
        )
        sel = reg.select(SafetyMode.CRITICAL)

        # Should select compliance and clarify, not high_weight
        assert "compliance" in sel.selected_ids
        assert "clarify" in sel.selected_ids
        # high_weight should not be selected (no required tags)
        assert "high_weight" not in sel.selected_ids


class TestManifestIntegration:
    """Test with real manifest."""

    def test_real_manifest_warn_covers_safety_tags(self):
        """Real manifest should cover safety tags in WARN mode."""
        reg = PhilosopherRegistry()
        sel = reg.select(SafetyMode.WARN)

        # Should have at least compliance and clarify
        assert TAG_COMPLIANCE in sel.covered_tags
        assert TAG_CLARIFY in sel.covered_tags

    def test_real_manifest_respects_cost_budget(self):
        """Real manifest should respect cost budget."""
        reg = PhilosopherRegistry()

        for mode in [SafetyMode.CRITICAL, SafetyMode.WARN, SafetyMode.NORMAL]:
            sel = reg.select(mode)
            plan = reg._plans[mode]
            assert sel.cost_total <= plan.cost_budget, f"{mode} exceeded cost budget"
