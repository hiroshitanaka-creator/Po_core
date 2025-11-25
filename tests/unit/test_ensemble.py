from po_core.ensemble import run_ensemble


def test_run_ensemble_returns_expected_shape(sample_prompt, expected_philosophers):
    result = run_ensemble(sample_prompt)

    assert result["prompt"] == sample_prompt
    assert result["philosophers"] == expected_philosophers
    assert len(result["results"]) == len(expected_philosophers)

    for entry in result["results"]:
        assert set(entry) >= {"name", "confidence", "summary", "tags"}
        assert isinstance(entry["confidence"], float)
        assert sample_prompt in entry["summary"]

    log = result["log"]
    assert log["prompt"] == sample_prompt
    assert log["philosophers"] == expected_philosophers
    assert any(event["event"] == "ensemble_started" for event in log["events"])
    assert any(
        event.get("results_recorded") == len(expected_philosophers) for event in log["events"]
    )
