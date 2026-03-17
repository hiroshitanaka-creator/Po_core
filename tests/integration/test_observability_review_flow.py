"""Integration test for observability/human-review regression line.

Flow under test (deterministic, no external dependency):
1. POST /v1/reason triggers ESCALATE
2. item is queued in /v1/review/pending
3. related trace is retrievable via /v1/trace/{session_id}
4. human decision is submitted
5. HumanReviewDecided appears in trace
6. after app/store reinitialization, trace/history/review state is preserved
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from po_core.app.rest.config import APISettings
from po_core.app.rest.review_store import get_review_store, reset_review_store
from po_core.app.rest.server import create_app
from po_core.app.rest.store import reset_trace_store
from po_core.domain.trace_event import TraceEvent


@pytest.mark.integration
@pytest.mark.observability
def test_observability_review_flow_persists_across_reinitialization(tmp_path):
    """ESCALATE -> review -> trace append -> restart persistence stays observable."""
    db_path = tmp_path / "observability_review.sqlite3"
    session_id = "obs-review-session"
    request_id = "req-obs-review-001"

    settings = APISettings(
        skip_auth=True,
        api_key="",
        trace_store_backend="sqlite",
        trace_db_path=str(db_path),
        review_store_backend="sqlite",
        review_db_path=str(db_path),
    )

    def _build_client() -> TestClient:
        app = create_app(settings)
        from po_core.app.rest import auth

        app.dependency_overrides[auth.require_api_key] = lambda: None
        return TestClient(app, raise_server_exceptions=True)

    def _mock_escalate_run(
        *, user_input, settings, tracer, philosophers=None
    ):  # noqa: ARG001
        tracer.emit(
            TraceEvent.now(
                "DecisionEmitted",
                correlation_id=request_id,
                payload={"gate": {"decision": "escalate"}},
            )
        )
        return {
            "status": "ok",
            "request_id": request_id,
            "verdict": {"decision": "escalate"},
            "proposal": {"content": "Escalated to human review."},
            "proposals": [],
            "tensors": {},
            "safety_mode": "WARN",
        }

    with _build_client() as client:
        with patch(
            "po_core.app.rest.routers.reason.po_run",
            side_effect=_mock_escalate_run,
        ):
            reason_resp = client.post(
                "/v1/reason",
                json={"input": "Need operator decision", "session_id": session_id},
            )
        assert reason_resp.status_code == 200

        pending_resp = client.get("/v1/review/pending")
        assert pending_resp.status_code == 200
        pending_items = pending_resp.json()["items"]
        assert len(pending_items) == 1
        assert pending_items[0]["session_id"] == session_id
        review_id = pending_items[0]["id"]

        trace_before = client.get(f"/v1/trace/{session_id}")
        assert trace_before.status_code == 200
        before_events = trace_before.json()["events"]
        assert any(e["event_type"] == "DecisionEmitted" for e in before_events)

        decision_resp = client.post(
            f"/v1/review/{review_id}/decision",
            json={"decision": "approve", "reviewer": "ops", "comment": "verified"},
        )
        assert decision_resp.status_code == 200

        trace_after = client.get(f"/v1/trace/{session_id}")
        assert trace_after.status_code == 200
        after_events = trace_after.json()["events"]
        assert any(e["event_type"] == "HumanReviewDecided" for e in after_events)

    reset_trace_store()
    reset_review_store()

    with _build_client() as client2:
        pending_after_restart = client2.get("/v1/review/pending")
        assert pending_after_restart.status_code == 200
        assert pending_after_restart.json()["total"] == 0

        trace_after_restart = client2.get(f"/v1/trace/{session_id}")
        assert trace_after_restart.status_code == 200
        restarted_events = trace_after_restart.json()["events"]
        event_types = [event["event_type"] for event in restarted_events]
        assert "DecisionEmitted" in event_types
        assert "HumanReviewDecided" in event_types

        history_resp = client2.get("/v1/trace/history?limit=10")
        assert history_resp.status_code == 200
        assert any(
            item["session_id"] == session_id for item in history_resp.json()["items"]
        )

        decided = get_review_store().apply_decision(
            review_id,
            decision="approve",
            reviewer="ops-restart-check",
            comment="persisted",
        )
        assert decided is not None
        assert decided["status"] == "decided"
