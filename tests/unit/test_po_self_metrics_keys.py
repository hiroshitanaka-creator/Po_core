"""
PR-2: Unit tests for PoSelfResponse.metrics honesty and responses key fix.

Verifies:
- metrics values are None (not 0.0) when TensorComputed emits only keys
- metrics values are real floats when TensorComputed emits a dict
- responses[n]["proposals"] is read from trace key "n", not "n_proposals"
- existing callers that check key presence (key in metrics) still pass
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from unittest.mock import MagicMock

import pytest

from po_core.domain.trace_event import TraceEvent
from po_core.po_self import PoSelf, PoSelfResponse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TS = datetime.now(timezone.utc)


def _event(event_type: str, payload: dict) -> TraceEvent:
    return TraceEvent(
        event_type=event_type,
        occurred_at=_TS,
        correlation_id="test-req",
        payload=payload,
    )


def _make_tracer(events: list[TraceEvent]) -> MagicMock:
    tracer = MagicMock()
    tracer.events = events
    return tracer


def _make_result(status: str = "ok") -> dict[str, Any]:
    return {
        "request_id": "test-req",
        "status": status,
        "proposal": {
            "proposal_id": "pareto:confucius:1",
            "action_type": "answer",
            "content": "Test answer",
            "confidence": 0.7,
            "assumption_tags": [],
            "risk_tags": [],
        },
    }


def _build_response(events: list[TraceEvent], result: dict | None = None) -> PoSelfResponse:
    """Call PoSelf._build_response() with synthetic events."""
    po = PoSelf()
    ctx = MagicMock()
    ctx.request_id = "test-req"
    tracer = _make_tracer(events)
    return po._build_response("test prompt", result or _make_result(), tracer, ctx)


# ---------------------------------------------------------------------------
# Metrics — keys present, values are None (not 0.0)
# ---------------------------------------------------------------------------


class TestMetricsKeyList:
    """TensorComputed emits a list of keys; values must be None, not 0.0."""

    def test_metric_keys_present_in_response(self):
        """Keys from TensorComputed are present in response.metrics."""
        events = [
            _event("TensorComputed", {"metrics": ["freedom_pressure", "semantic_delta"], "version": 1}),
        ]
        resp = _build_response(events)
        assert "freedom_pressure" in resp.metrics
        assert "semantic_delta" in resp.metrics

    def test_metric_values_are_none_not_zero(self):
        """Values must be None when only keys are emitted, not a 0.0 stub."""
        events = [
            _event("TensorComputed", {"metrics": ["freedom_pressure", "blocked_tensor"], "version": 1}),
        ]
        resp = _build_response(events)
        assert resp.metrics["freedom_pressure"] is None, (
            "Expected None, not a stub 0.0. "
            f"Got: {resp.metrics['freedom_pressure']!r}"
        )
        assert resp.metrics["blocked_tensor"] is None

    def test_no_tensor_event_gives_empty_metrics(self):
        """When no TensorComputed event exists, metrics is empty dict."""
        resp = _build_response([])
        assert resp.metrics == {}

    def test_all_known_metrics_are_none(self):
        """All four standard metric keys map to None."""
        keys = ["freedom_pressure", "semantic_delta", "blocked_tensor", "interaction_tensor"]
        events = [
            _event("TensorComputed", {"metrics": keys, "version": 1}),
        ]
        resp = _build_response(events)
        for k in keys:
            assert k in resp.metrics
            assert resp.metrics[k] is None, f"{k} should be None, got {resp.metrics[k]!r}"

    def test_key_in_check_still_works(self):
        """Existing code that checks 'freedom_pressure' in metrics still passes."""
        events = [
            _event("TensorComputed", {"metrics": ["freedom_pressure"], "version": 1}),
        ]
        resp = _build_response(events)
        # This is the pattern used in existing test_po_self.py:
        assert "freedom_pressure" in resp.metrics


# ---------------------------------------------------------------------------
# Metrics — dict payload path (real values)
# ---------------------------------------------------------------------------


class TestMetricsDictPayload:
    """When TensorComputed emits a dict, real float values should be used."""

    def test_dict_payload_produces_real_floats(self):
        """Dict payload in TensorComputed leads to real float values."""
        events = [
            _event("TensorComputed", {
                "metrics": {"freedom_pressure": 0.42, "semantic_delta": 0.17},
                "version": 1,
            }),
        ]
        resp = _build_response(events)
        assert resp.metrics["freedom_pressure"] == pytest.approx(0.42)
        assert resp.metrics["semantic_delta"] == pytest.approx(0.17)

    def test_dict_payload_no_none_values(self):
        """Dict payload must not produce None values."""
        events = [
            _event("TensorComputed", {"metrics": {"freedom_pressure": 0.5}, "version": 1}),
        ]
        resp = _build_response(events)
        assert resp.metrics["freedom_pressure"] is not None


# ---------------------------------------------------------------------------
# responses — "proposals" key reads from trace "n", not "n_proposals"
# ---------------------------------------------------------------------------


class TestResponsesNKey:
    """PhilosopherResult events emit key 'n'; responses must read that key."""

    def test_proposals_count_comes_from_n_key(self):
        """responses[i]['proposals'] should equal the 'n' value in the trace."""
        events = [
            _event("PhilosopherResult", {
                "name": "aristotle",
                "n": 3,
                "timed_out": False,
                "error": "",
                "latency_ms": 42,
            }),
        ]
        resp = _build_response(events)
        assert len(resp.responses) == 1
        assert resp.responses[0]["proposals"] == 3, (
            "Expected proposals=3 from trace key 'n', "
            f"got {resp.responses[0]['proposals']!r}"
        )

    def test_proposals_count_not_from_n_proposals_key(self):
        """A stale 'n_proposals' key in the payload must NOT be used.

        This is the regression: old code read 'n_proposals' which doesn't
        exist in ensemble.py trace emissions, so the count was always 0.
        The new code reads 'n', so even if 'n_proposals' is absent, we get
        the real count.
        """
        # Simulate a payload that ONLY has 'n' (as ensemble.py emits):
        events = [
            _event("PhilosopherResult", {
                "name": "kant",
                "n": 2,
                # deliberately NO 'n_proposals' key
                "timed_out": False,
                "error": "",
                "latency_ms": 10,
            }),
        ]
        resp = _build_response(events)
        assert resp.responses[0]["proposals"] == 2

    def test_multiple_philosophers_proposals_counts(self):
        """Each philosopher's count is read independently."""
        events = [
            _event("PhilosopherResult", {"name": "plato", "n": 1, "timed_out": False, "error": "", "latency_ms": 5}),
            _event("PhilosopherResult", {"name": "hegel", "n": 4, "timed_out": False, "error": "", "latency_ms": 8}),
        ]
        resp = _build_response(events)
        assert len(resp.responses) == 2
        counts = {r["name"]: r["proposals"] for r in resp.responses}
        assert counts["plato"] == 1
        assert counts["hegel"] == 4

    def test_n_defaults_to_zero_on_timeout(self):
        """When 'n' key is absent (e.g. timeout path), defaults to 0."""
        events = [
            _event("PhilosopherResult", {
                "name": "nietzsche",
                "timed_out": True,
                "error": "timeout",
                "latency_ms": -1,
                # 'n' absent because philosopher never returned
            }),
        ]
        resp = _build_response(events)
        assert resp.responses[0]["proposals"] == 0
