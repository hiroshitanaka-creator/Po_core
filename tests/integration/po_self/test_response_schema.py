import pytest

from po_core.core.response import PoCoreResponse
from po_core import po_self


@pytest.mark.integration
def test_generate_returns_complete_response() -> None:
    prompt = "test response schema"
    response = po_self.generate(prompt, seed=7)

    assert isinstance(response, PoCoreResponse)
    assert response.text
    assert response.tensors.semantic_profile
    assert response.tensors.freedom_pressure >= 0
    assert response.contributions
    assert response.trace_meta["prompt"] == prompt
    assert response.trace_meta["seed"] == 7
