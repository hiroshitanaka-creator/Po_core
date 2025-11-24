import pytest

from po_core.po_self.manager import PoSelfManager


@pytest.mark.integration
@pytest.mark.philosophical
def test_aggregate_is_deterministic_with_seed() -> None:
    manager = PoSelfManager()
    prompt = "deterministic prompt"

    aggregation_first = manager.aggregate(prompt, seed=42)
    aggregation_second = manager.aggregate(prompt, seed=42)

    assert aggregation_first.tensors == aggregation_second.tensors
    assert aggregation_first.contributions == aggregation_second.contributions
    assert aggregation_first.tensors.semantic_profile
