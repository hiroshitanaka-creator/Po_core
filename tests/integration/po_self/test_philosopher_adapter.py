import pytest

from po_core.philosophers import Nietzsche
from po_core.po_self.philosophers import PhilosopherAdapter


@pytest.mark.integration
def test_adapter_outputs_normalized_contribution() -> None:
    adapter = PhilosopherAdapter(Nietzsche())
    contribution = adapter.evaluate("adapter prompt", seed=3)

    assert 0.0 <= contribution.freedom_scalar <= 1.0
    assert 0.0 <= contribution.blocked_scalar <= 1.0
    assert len(contribution.semantic_vector) == 4
    assert all(-1.0 <= value <= 1.0 for value in contribution.semantic_vector)
    assert contribution.summary
