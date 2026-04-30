"""
test_sample_trace_contract.py
=============================

Lightweight contract tests for docs/viewer/sample_trace.json.

Purpose: ensure that the sample trace file stays structurally aligned with
the engine trace contract documented in docs/ENGINE_TRACE_CONTRACT.md.

These tests do NOT run the pipeline; they parse the JSON file only.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

_SAMPLE_PATH = (
    Path(__file__).resolve().parents[2] / "docs" / "viewer" / "sample_trace.json"
)

_REQUIRED_EVENT_TYPES = frozenset(
    {
        "TensorComputed",
        "SafetyModeInferred",
        "PhilosophersSelected",
        "ConflictSummaryComputed",
        "ParetoFrontComputed",
        "ParetoWinnerSelected",
        "AggregateCompleted",
        "DecisionEmitted",
    }
)

_TENSOR_REQUIRED_METRICS = frozenset(
    {"freedom_pressure", "semantic_delta", "blocked_tensor", "interaction_tensor"}
)


@pytest.fixture(scope="module")
def sample() -> dict:
    return json.loads(_SAMPLE_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def events_by_type(sample: dict) -> dict:
    result: dict = {}
    for ev in sample["events"]:
        result.setdefault(ev["event_type"], ev)
    return result


class TestSampleTraceContract:
    """TRACE-VIEW-1: sample_trace.json must reflect ENGINE_TRACE_CONTRACT fields."""

    def test_required_event_types_present(self, sample: dict) -> None:
        """All key event types from ENGINE_TRACE_CONTRACT must appear in event_types list."""
        present = set(sample.get("event_types", []))
        missing = _REQUIRED_EVENT_TYPES - present
        assert not missing, (
            f"sample_trace event_types is missing: {missing}. "
            f"Update docs/viewer/sample_trace.json to include these event types."
        )

    def test_tensor_computed_has_metric_status(self, events_by_type: dict) -> None:
        """TensorComputed payload must contain metric_status covering all 4 required metrics."""
        tc = events_by_type.get("TensorComputed")
        assert tc is not None, "TensorComputed event not found in sample_trace.json"

        payload = tc["payload"]
        assert "metric_status" in payload, (
            "TensorComputed payload must have 'metric_status'. "
            "Update docs/viewer/sample_trace.json."
        )
        ms = payload["metric_status"]
        missing = _TENSOR_REQUIRED_METRICS - set(ms)
        assert (
            not missing
        ), f"TensorComputed.metric_status is missing entries for: {missing}"

    def test_tensor_computed_metrics_is_dict(self, events_by_type: dict) -> None:
        """TensorComputed.metrics must be a dict of name→float, not a list."""
        tc = events_by_type["TensorComputed"]
        metrics = tc["payload"]["metrics"]
        assert isinstance(metrics, dict), (
            f"TensorComputed.metrics must be a dict, got {type(metrics).__name__}. "
            "Update docs/viewer/sample_trace.json."
        )
        for name, value in metrics.items():
            assert isinstance(
                value, (int, float)
            ), f"TensorComputed.metrics[{name!r}] must be numeric, got {type(value).__name__}"

    def test_safety_mode_inferred_has_required_fields(
        self, events_by_type: dict
    ) -> None:
        """SafetyModeInferred must have all 7 required fields."""
        smi = events_by_type.get("SafetyModeInferred")
        assert (
            smi is not None
        ), "SafetyModeInferred event not found in sample_trace.json"

        required = {
            "mode",
            "freedom_pressure",
            "warn_threshold",
            "critical_threshold",
            "missing_mode",
            "source_metric",
            "reason",
        }
        missing = required - set(smi["payload"])
        assert not missing, f"SafetyModeInferred payload missing fields: {missing}"

    def test_philosophers_selected_has_selection_rationale(
        self, events_by_type: dict
    ) -> None:
        """PhilosophersSelected must have all selection-rationale fields."""
        ps = events_by_type.get("PhilosophersSelected")
        assert (
            ps is not None
        ), "PhilosophersSelected event not found in sample_trace.json"

        required = {
            "mode",
            "scenario_type",
            "preferred_tags",
            "require_tags",
            "limit_override",
            "limit",
            "max_risk",
            "cost_budget",
            "cost_total",
            "ids",
            "covered_tags",
        }
        missing = required - set(ps["payload"])
        assert not missing, (
            f"PhilosophersSelected payload missing fields: {missing}. "
            "Update docs/viewer/sample_trace.json."
        )

    def test_pareto_winner_selected_has_weighted_score(
        self, events_by_type: dict
    ) -> None:
        """ParetoWinnerSelected.winner must contain weighted_score."""
        pw = events_by_type.get("ParetoWinnerSelected")
        assert (
            pw is not None
        ), "ParetoWinnerSelected event not found in sample_trace.json"

        winner = pw["payload"].get("winner", {})
        assert "weighted_score" in winner, (
            "ParetoWinnerSelected.winner must have 'weighted_score'. "
            "Update docs/viewer/sample_trace.json."
        )
        assert isinstance(winner["weighted_score"], (int, float)), (
            f"ParetoWinnerSelected.winner.weighted_score must be numeric, "
            f"got {type(winner['weighted_score']).__name__}"
        )

    def test_pareto_winner_selected_has_weights(self, events_by_type: dict) -> None:
        """ParetoWinnerSelected payload must have top-level weights dict."""
        pw = events_by_type.get("ParetoWinnerSelected")
        assert (
            pw is not None
        ), "ParetoWinnerSelected event not found in sample_trace.json"

        payload = pw["payload"]
        assert (
            "weights" in payload
        ), "ParetoWinnerSelected payload must have top-level 'weights' key."
        weights = payload["weights"]
        required_objectives = {
            "safety",
            "freedom",
            "explain",
            "brevity",
            "coherence",
            "emergence",
        }
        missing = required_objectives - set(weights)
        assert (
            not missing
        ), f"ParetoWinnerSelected.weights is missing objectives: {missing}"

    def test_decision_emitted_has_final(self, events_by_type: dict) -> None:
        """DecisionEmitted payload must contain 'final' fingerprint."""
        de = events_by_type.get("DecisionEmitted")
        assert de is not None, "DecisionEmitted event not found in sample_trace.json"

        payload = de["payload"]
        assert "final" in payload, (
            "DecisionEmitted payload must have 'final' key. "
            "Update docs/viewer/sample_trace.json."
        )
        final = payload["final"]
        required = {
            "proposal_id",
            "action_type",
            "confidence",
            "content_len",
            "content_hash",
        }
        missing = required - set(final)
        assert not missing, f"DecisionEmitted.final missing fields: {missing}"
