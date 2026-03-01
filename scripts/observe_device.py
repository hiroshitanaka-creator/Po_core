#!/usr/bin/env python3
"""Observe trade-off device outputs and deliberation traces from PoSelf."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from po_core.po_self import PoSelf
from po_core.trace.in_memory import InMemoryTracer


def _short_summary(report: Dict[str, Any] | None) -> None:
    if not isinstance(report, dict):
        return

    scoreboard = report.get("scoreboard")
    disagreements = report.get("disagreements")

    if isinstance(scoreboard, dict):
        print("\n[scoreboard summary]")
        for axis in sorted(scoreboard.keys()):
            entry = scoreboard.get(axis)
            if isinstance(entry, dict):
                mean = entry.get("mean")
                variance = entry.get("variance")
                samples = entry.get("samples")
                print(
                    f"- {axis}: mean={mean}, variance={variance}, samples={samples}"
                )

    if isinstance(disagreements, list):
        print("\n[disagreements summary]")
        for idx, item in enumerate(disagreements[:3], start=1):
            if isinstance(item, dict):
                axis = item.get("axis")
                spread = item.get("spread")
                print(f"- #{idx}: axis={axis}, spread={spread}")
            else:
                print(f"- #{idx}: {item}")
        if len(disagreements) > 3:
            print(f"- ... ({len(disagreements) - 3} more)")


def main() -> int:
    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "転職するべき？家族とキャリアのトレードオフが悩み"
    )

    os.environ.setdefault("PO_STRUCTURED_OUTPUT", "1")

    po = PoSelf(enable_trace=True)
    response = po.generate(prompt)

    metadata = response.metadata or {}

    print(f"request_id: {metadata.get('request_id')}")
    print(f"status: {metadata.get('status')}")
    print(f"degraded: {metadata.get('degraded')}")
    print(f"consensus_leader: {response.consensus_leader}")

    report = metadata.get("synthesis_report")
    print("\n[synthesis_report]")
    if report is None:
        print("None")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))

    tracer = po.get_trace()
    print("\n[DeliberationCompleted payload]")
    if not isinstance(tracer, InMemoryTracer):
        print("None")
        return 0

    event = next(
        (e for e in tracer.events if e.event_type == "DeliberationCompleted"), None
    )
    if event is None:
        print("None")
        return 0

    print(json.dumps(event.payload, ensure_ascii=False, indent=2, sort_keys=True))
    _short_summary(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
