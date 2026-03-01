from __future__ import annotations

import argparse
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, Mapping, Optional

from po_core.po_self import PoSelf
from po_core.trace.event_log import JsonlEventLogger


def _extract_replay_inputs(events: list[Mapping[str, Any]]) -> Dict[str, Any]:
    for ev in events:
        if ev.get("stage") != "propose":
            continue
        payload = ev.get("payload", {})
        if not isinstance(payload, Mapping):
            continue
        return {
            "prompt": str(payload.get("prompt", "")),
            "philosophers": payload.get("philosophers"),
            "context": (
                payload.get("context")
                if isinstance(payload.get("context"), Mapping)
                else {}
            ),
        }
    raise ValueError("No propose event found; cannot replay run")


@contextmanager
def _temporary_env(name: str, value: str) -> Iterator[None]:
    old = os.environ.get(name)
    os.environ[name] = value
    try:
        yield
    finally:
        if old is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = old


def replay_run(run_id: str, log_dir: str | Path | None = None) -> Dict[str, Any]:
    """Replay a run from its event log and regenerate synthesis report structure."""
    logger = JsonlEventLogger(base_dir=log_dir)
    events = [e.to_dict() for e in logger.load(run_id)]
    if not events:
        raise FileNotFoundError(f"No event log found for run_id={run_id}")

    replay_inputs = _extract_replay_inputs(events)
    philosophers = replay_inputs.get("philosophers")
    if not isinstance(philosophers, list) or not philosophers:
        philosophers = None

    with _temporary_env("PO_STRUCTURED_OUTPUT", "1"):
        response = PoSelf().generate(
            replay_inputs["prompt"],
            philosophers=philosophers,
            context=dict(replay_inputs.get("context") or {}),
        )

    report = (response.metadata or {}).get("synthesis_report")
    return {
        "run_id": run_id,
        "prompt": replay_inputs["prompt"],
        "report": report,
        "result": response.to_dict(),
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay Po_core run from JSONL event log"
    )
    parser.add_argument("run_id", help="Run ID to replay")
    parser.add_argument(
        "--log-dir",
        default=".po_core_runs",
        help="Directory containing <run_id>.jsonl (default: .po_core_runs)",
    )
    args = parser.parse_args(argv)

    replayed = replay_run(args.run_id, log_dir=args.log_dir)
    # keep stdlib-only output format for python -m invocation
    import json

    print(json.dumps(replayed, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
