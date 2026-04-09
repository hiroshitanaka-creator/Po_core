from __future__ import annotations

from po_core.app.rest.routers.reason import _persist_and_finalize_result
from po_core.trace.in_memory import InMemoryTracer


def test_reason_payload_does_not_fabricate_default_safety_mode() -> None:
    payload = _persist_and_finalize_result(
        session_id="s-1",
        result={
            "request_id": "r-1",
            "status": "ok",
            "proposal": {"content": "answer"},
            "proposals": [],
            "tensors": {},
        },
        tracer=InMemoryTracer(),
        elapsed_ms=1.2,
        source="/v1/reason",
    )

    assert payload.get("safety_mode") is None
