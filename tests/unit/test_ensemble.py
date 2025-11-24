from po_core.ensemble import DEFAULT_PHILOSOPHERS, run_ensemble


def test_run_ensemble_returns_expected_shape(sample_prompt):
    result = run_ensemble(sample_prompt)

    assert result["prompt"] == sample_prompt
    assert result["philosophers"] == DEFAULT_PHILOSOPHERS
    assert len(result["results"]) == len(DEFAULT_PHILOSOPHERS)

    for entry in result["results"]:
        assert set(entry) >= {"name", "confidence", "summary", "tags"}
        assert isinstance(entry["confidence"], float)
        assert sample_prompt in entry["summary"]

    log = result["log"]
    assert log["prompt"] == sample_prompt
    assert log["philosophers"] == DEFAULT_PHILOSOPHERS
    assert any(event["event"] == "ensemble_started" for event in log["events"])
    assert any(event.get("results_recorded") == len(DEFAULT_PHILOSOPHERS) for event in log["events"])
