#!/usr/bin/env python
from __future__ import annotations

import json
from pathlib import Path

CASES = {
    "high_bias_affiliate": {
        "label": "ECHO_BLOCKED",
        "bias_original": 0.91,
        "bias_final": 0.27,
        "execution_allowed": False,
        "requires_human_confirm": True,
        "reasons": [
            "single affiliate source dominates evidence",
            "ad-like phrasing detected in candidate summaries",
            "insufficient independent merchant signals",
        ],
    },
    "mixed_contaminated": {
        "label": "ECHO_CHECK",
        "bias_original": 0.62,
        "bias_final": 0.41,
        "execution_allowed": False,
        "requires_human_confirm": True,
        "reasons": [
            "some contamination removed but uncertainty remains",
            "merchant metadata has partial gaps",
            "human confirmation required for accountability",
        ],
    },
    "clean_multi_merchant": {
        "label": "ECHO_VERIFIED",
        "bias_original": 0.33,
        "bias_final": 0.12,
        "execution_allowed": True,
        "requires_human_confirm": False,
        "reasons": [
            "multiple merchants corroborate core claims",
            "risk signals under policy threshold",
            "responsibility boundaries are explicit",
        ],
    },
}


def main() -> int:
    runs = Path("runs")
    runs.mkdir(parents=True, exist_ok=True)
    for case, payload in CASES.items():
        audit = {
            "case": case,
            "summary": payload,
            "verify_command": f"po-cosmic verify runs/{case}.badge.json",
        }
        badge = {"case": case, **payload}
        (runs / f"{case}.audit.json").write_text(
            json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (runs / f"{case}.badge.json").write_text(
            json.dumps(badge, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print("generated demo-shopping runs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
