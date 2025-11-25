import pytest

from po_core.ensemble import DEFAULT_PHILOSOPHERS, run_ensemble


def test_run_ensemble_returns_expected_shape(sample_prompt):
    result = run_ensemble(sample_prompt)

    assert result["prompt"] == sample_prompt
    assert result["philosophers"] == DEFAULT_PHILOSOPHERS
    assert len(result["responses"]) == len(DEFAULT_PHILOSOPHERS)

    for entry in result["responses"]:
        assert set(entry) >= {"name", "reasoning", "freedom_pressure", "semantic_delta", "blocked_tensor"}
        assert isinstance(entry["freedom_pressure"], float)
        assert isinstance(entry["semantic_delta"], float)
        assert isinstance(entry["blocked_tensor"], float)

    log = result["log"]
    assert log["prompt"] == sample_prompt
    assert log["philosophers"] == DEFAULT_PHILOSOPHERS
    assert any(event["event"] == "ensemble_started" for event in log["events"])
    assert any(event.get("results_recorded") == len(DEFAULT_PHILOSOPHERS) for event in log["events"])


def test_run_ensemble_orders_and_aggregates(sample_prompt):
    result = run_ensemble(sample_prompt)

    names = [entry["name"] for entry in result["responses"]]
    assert names == [
        "Aristotle (Ἀριστοτέλης)",
        "Friedrich Nietzsche",
        "Ludwig Wittgenstein",
    ]

    aggregate = result["aggregate"]
    computed_freedom = round(sum(entry["freedom_pressure"] for entry in result["responses"]) / len(result["responses"]), 2)
    computed_delta = round(sum(entry["semantic_delta"] for entry in result["responses"]) / len(result["responses"]), 2)
    computed_blocked = round(sum(entry["blocked_tensor"] for entry in result["responses"]) / len(result["responses"]), 2)

    assert aggregate["freedom_pressure"] == computed_freedom == pytest.approx(0.82)
    assert aggregate["semantic_delta"] == computed_delta == pytest.approx(0.76)
    assert aggregate["blocked_tensor"] == computed_blocked == pytest.approx(0.47)
    assert result["consensus"]["leader"] == names[0]
