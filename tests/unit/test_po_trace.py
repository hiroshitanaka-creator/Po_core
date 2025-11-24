from po_core.po_trace import trace_recorder


def test_trace_recorder_tracks_events_and_artifacts(sample_prompt):
    trace_recorder.reset()

    run_id = trace_recorder.start_run(sample_prompt, ["socrates"])
    trace_recorder.log_event(run_id, "philosopher_considered", philosopher="socrates", confidence=0.5)
    trace_recorder.log_artifact(run_id, label="draft", content="Initial thoughts", philosopher="socrates")
    trace_recorder.complete_run(run_id, status="ok")

    snapshot = trace_recorder.snapshot(run_id)

    assert snapshot["prompt"] == sample_prompt
    assert snapshot["status"] == "ok"
    assert snapshot["events"][0]["event"] == "ensemble_started"
    assert any(event["event"] == "ensemble_completed" for event in snapshot["events"])

    artifact = snapshot["artifacts"][0]
    assert artifact["label"] == "draft"
    assert artifact["philosopher"] == "socrates"


def test_recent_runs_filtering_by_prompt_and_philosopher(sample_prompt):
    trace_recorder.reset()
    run_id = trace_recorder.start_run(sample_prompt, ["socrates", "plato"])
    trace_recorder.log_event(run_id, "philosopher_considered", philosopher="plato", confidence=0.7)
    trace_recorder.complete_run(run_id, status="ok")

    filtered = trace_recorder.recent_runs(
        prompt_filter="authentically",
        philosopher_filter=["plato"],
        status_filter="ok",
    )

    assert len(filtered) == 1
    assert filtered[0]["prompt"] == sample_prompt
    assert filtered[0]["events"][-1]["status"] == "ok"


def test_snapshot_is_isolated(sample_prompt):
    trace_recorder.reset()
    run_id = trace_recorder.start_run(sample_prompt, ["aristotle"])
    trace_recorder.complete_run(run_id, status="ok")

    snapshot = trace_recorder.snapshot(run_id)
    snapshot["prompt"] = "modified"

    assert trace_recorder.snapshot(run_id)["prompt"] == sample_prompt
