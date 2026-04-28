from __future__ import annotations

from dataclasses import dataclass

from po_core.domain.proposal import Proposal
from po_core.party_machine import run_philosophers
from po_core.philosophers.identity import resolve_philosopher_id
from po_core.philosophers.manifest import get_enabled_specs
from po_core.philosophers.registry import PhilosopherRegistry


@dataclass
class _TestDouble:
    name: str

    def propose(self, ctx, intent, tensors, memory):
        return [
            Proposal(
                proposal_id=f"{self.name}-p1",
                action_type="answer",
                content="ok",
                confidence=0.7,
                assumption_tags=[],
                risk_tags=[],
                extra={},
            )
        ]


def test_registry_loaded_philosopher_emits_canonical_manifest_id() -> None:
    """Registry-loaded philosophers must emit their canonical manifest philosopher_id."""
    canonical_ids = {s.philosopher_id for s in get_enabled_specs()}

    registry = PhilosopherRegistry(cache_instances=False)
    philosophers, errors = registry.load(["aristotle"])
    assert not errors
    assert philosophers

    _, results = run_philosophers(
        philosophers,
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=5.0,
        execution_mode="thread",
    )

    assert results
    assert all(result.philosopher_id in canonical_ids for result in results)
    assert results[0].philosopher_id == "aristotle"


def test_unregistered_test_double_falls_back_to_name() -> None:
    """Unregistered test doubles must fall back to their .name for philosopher_id."""
    canonical_ids = {s.philosopher_id for s in get_enabled_specs()}

    _, results = run_philosophers(
        [_TestDouble(name="my-test-double")],
        ctx=None,
        intent=None,
        tensors=None,
        memory=None,
        max_workers=1,
        timeout_s=1.0,
        execution_mode="thread",
    )

    assert results
    assert results[0].philosopher_id == "my-test-double"
    assert results[0].philosopher_id not in canonical_ids


def test_resolve_philosopher_id_priority_order() -> None:
    """Unit-test the resolver directly for all three priority tiers."""
    canonical_ids = {s.philosopher_id for s in get_enabled_specs()}

    # Priority 1: explicit philosopher_id attribute wins
    class _WithExplicitId:
        philosopher_id = "kant"
        name = "wrong-name"

    assert resolve_philosopher_id(_WithExplicitId()) == "kant"

    # Priority 2: po_core.philosophers.* module path → canonical ID
    registry = PhilosopherRegistry(cache_instances=False)
    philosophers, _ = registry.load(["aristotle"])
    ph = philosophers[0]
    # Remove the registry-set attribute to test module-path fallback
    del ph.__dict__["philosopher_id"]
    assert resolve_philosopher_id(ph) == "aristotle"
    assert resolve_philosopher_id(ph) in canonical_ids

    # Priority 3: .name for test doubles outside po_core.philosophers.*
    assert resolve_philosopher_id(_TestDouble(name="external-double")) == "external-double"
