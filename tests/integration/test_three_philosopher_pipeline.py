import json
from typing import List

import pytest

pytest.importorskip("rich")

from po_core.ensemble import DEFAULT_PHILOSOPHERS
from po_core.cli import main


@pytest.mark.integration
@pytest.mark.usefixtures("fixed_timestamp")
def test_three_philosopher_pipeline_outputs_are_deterministic(sample_prompt, ensemble_run):
    results = ensemble_run["results"]
    confidences: List[float] = [entry["confidence"] for entry in results]

    assert ensemble_run["prompt"] == sample_prompt
    assert ensemble_run["philosophers"] == DEFAULT_PHILOSOPHERS
    assert confidences == [0.88, 0.83, 0.78]
    assert [entry["name"] for entry in results] == DEFAULT_PHILOSOPHERS
    assert all(sample_prompt in entry["summary"] for entry in results)

    log = ensemble_run["log"]
    assert log["prompt"] == sample_prompt
    assert log["philosophers"] == DEFAULT_PHILOSOPHERS
    assert log["created_at"].endswith("Z")
    assert log["events"] == [
        {"event": "ensemble_started", "philosophers": 3},
        {"event": "ensemble_completed", "results_recorded": 3, "status": "ok"},
    ]


@pytest.mark.integration
@pytest.mark.usefixtures("fixed_timestamp")
def test_three_philosopher_trace_matches_cli_output(sample_prompt, cli_runner):
    result = cli_runner.invoke(main, ["log", sample_prompt])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["philosophers"] == DEFAULT_PHILOSOPHERS
    assert payload["prompt"] == sample_prompt
    assert payload["events"][0]["event"] == "ensemble_started"
    assert payload["events"][1]["status"] == "ok"
    assert payload["created_at"].endswith("Z")
