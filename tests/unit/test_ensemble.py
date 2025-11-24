from datetime import datetime

import pytest

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


@pytest.mark.unit
def test_run_ensemble_is_deterministic_and_ordered(sample_prompt):
    result = run_ensemble(sample_prompt)

    names = [entry["name"] for entry in result["results"]]
    assert names == DEFAULT_PHILOSOPHERS

    expected_confidences = [0.88, 0.83, 0.78]
    confidences = [entry["confidence"] for entry in result["results"]]
    assert confidences == expected_confidences


@pytest.mark.unit
def test_run_ensemble_respects_custom_philosopher_order(sample_prompt):
    custom = ["a", "b", "c", "d"]

    result = run_ensemble(sample_prompt, philosophers=custom)

    assert [entry["name"] for entry in result["results"]] == custom
    assert result["philosophers"] == custom
    assert result["log"]["philosophers"] == custom


@pytest.mark.unit
def test_run_ensemble_log_schema(sample_prompt):
    result = run_ensemble(sample_prompt)

    log = result["log"]
    assert set(log) == {"prompt", "philosophers", "created_at", "events"}
    assert log["philosophers"] == DEFAULT_PHILOSOPHERS

    assert log["created_at"].endswith("Z")
    # Confirm timestamp is ISO-8601 compatible (strip the trailing Z for parsing)
    datetime.fromisoformat(log["created_at"].rstrip("Z"))

    assert len(log["events"]) == 2
    start_event, completed_event = log["events"]
    assert start_event == {
        "event": "ensemble_started",
        "philosophers": len(DEFAULT_PHILOSOPHERS),
    }
    assert completed_event == {
        "event": "ensemble_completed",
        "results_recorded": len(DEFAULT_PHILOSOPHERS),
        "status": "ok",
    }
