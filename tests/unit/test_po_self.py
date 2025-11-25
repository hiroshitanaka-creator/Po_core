from po_core.po_self import PoSelf


def test_po_self_generate_returns_structured_response(sample_prompt):
    response = PoSelf().generate(sample_prompt)

    assert response.prompt == sample_prompt
    assert response.consensus_leader == "Aristotle (Ἀριστοτέλης)"
    assert response.metrics["freedom_pressure"] == 0.82
    assert response.metrics["semantic_delta"] == 0.76
    assert response.metrics["blocked_tensor"] == 0.47
    assert response.responses
    assert response.log["prompt"] == sample_prompt


def test_po_self_respects_custom_philosophers(sample_prompt):
    response = PoSelf(philosophers=["wittgenstein"]).generate(sample_prompt)

    assert response.philosophers == ["wittgenstein"]
    assert response.consensus_leader == "Ludwig Wittgenstein"
    assert len(response.responses) == 1
