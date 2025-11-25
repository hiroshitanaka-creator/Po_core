from po_core.ensemble import DEFAULT_PHILOSOPHERS, run_ensemble


def test_run_ensemble_matches_snapshot(sample_prompt, ensemble_snapshot):
    result = run_ensemble(sample_prompt)

    assert result["prompt"] == ensemble_snapshot["prompt"]
    assert result["philosophers"] == DEFAULT_PHILOSOPHERS
    assert result == ensemble_snapshot


def test_run_ensemble_entries_are_deterministic(sample_prompt):
    first = run_ensemble(sample_prompt)
    second = run_ensemble(sample_prompt)

    assert first == second
    assert all(entry["confidence"] <= 1 for entry in first["results"])
