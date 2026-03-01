from __future__ import annotations

import json
import os
from pathlib import Path

from po_core.po_self import PoSelf
from po_core.trace.event_log import JsonlEventLogger, mask_sensitive_payload
from po_core.trace.replay import replay_run


def test_mask_sensitive_payload_masks_pii() -> None:
    payload = {
        "email": "user@example.com",
        "phone": "+81 090-1234-5678",
        "address": "1 Chiyoda city",
    }
    masked = mask_sensitive_payload(payload)
    assert "example.com" not in json.dumps(masked, ensure_ascii=False)
    assert "1234" not in json.dumps(masked, ensure_ascii=False)


def test_event_log_and_replay(tmp_path: Path) -> None:
    old = os.environ.get("PO_STRUCTURED_OUTPUT")
    os.environ["PO_STRUCTURED_OUTPUT"] = "1"
    try:
        response = PoSelf(enable_trace=True, trace_dir=str(tmp_path)).generate(
            "Contact me at test@example.com or 090-1111-2222",
            context={"address": "1 Main Street"},
        )
    finally:
        if old is None:
            os.environ.pop("PO_STRUCTURED_OUTPUT", None)
        else:
            os.environ["PO_STRUCTURED_OUTPUT"] = old

    run_id = response.metadata["request_id"]
    log_file = tmp_path / f"{run_id}.jsonl"
    assert log_file.exists()

    logger = JsonlEventLogger(base_dir=tmp_path)
    events = logger.load(run_id)
    stages = [e.stage for e in events]
    assert stages == ["propose", "critique", "synthesize"]

    log_text = log_file.read_text(encoding="utf-8")
    assert "test@example.com" not in log_text
    assert "090-1111-2222" not in log_text

    replayed = replay_run(run_id, log_dir=tmp_path)
    report = replayed.get("report")
    assert isinstance(report, dict)
    assert "axis_scoreboard" in report
    assert "open_questions" in report
