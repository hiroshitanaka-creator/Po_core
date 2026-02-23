"""
src/pocore/orchestrator.py
==========================

Pipeline orchestrator: parse_input → engines → compose_output.

This is the deterministic core of Po_core.
All engine calls are pure functions: (case, features) → output.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union

from . import parse_input
from .engines import (
    ethics_v1,
    generator_stub,
    question_v1,
    recommendation_v1,
    responsibility_v1,
    uncertainty_v1,
)
from .tracer import build_trace
from .policy_v1 import TIME_PRESSURE_DAYS, UNKNOWN_BLOCK
from .utils import deterministic_run_id, input_digest, normalize_now

POCORE_VERSION = "0.1.0"
SCHEMA_VERSION = "1.0"


def run_case(
    case: Dict[str, Any],
    *,
    case_path: Optional[Path] = None,
    seed: int = 0,
    now: Union[str, Any] = "2026-02-22T00:00:00Z",
    deterministic: bool = True,
) -> Dict[str, Any]:
    """Run a validated case dict through the deterministic pipeline."""

    created_at = normalize_now(now)
    cid = str(case.get("case_id", "case_unknown"))
    title = str(case.get("title", ""))

    # 1. parse_input → features
    parsed = parse_input.parse(case, case_path=case_path, now=created_at)
    short_id = parsed.short_id
    features = parsed.features

    # Deterministic run_id (golden contract)
    run_id = deterministic_run_id(short_id)

    # 2. Compute digest
    digest = input_digest(case)

    # 3. Engines (sequential, each engine may mutate options in-place)
    options = generator_stub.generate_options(
        case, short_id=short_id, features=features
    )
    options, ethics_summary = ethics_v1.apply(
        case, short_id=short_id, features=features, options=options
    )
    options, responsibility_summary = responsibility_v1.apply(
        case, short_id=short_id, features=features, options=options
    )
    questions = question_v1.generate(case, short_id=short_id, features=features)
    recommendation, arbitration_code = recommendation_v1.arbitrate_recommendation(
        case, short_id=short_id, features=features, options=options
    )
    uncertainty = uncertainty_v1.summarize(case, short_id=short_id, features=features)

    # 4. Trace
    trace = build_trace(
        short_id=short_id,
        created_at=created_at,
        options_count=len(options),
        questions_count=len(questions),
        features=features,
        arbitration_code=arbitration_code,
        policy_snapshot={
            "UNKNOWN_BLOCK": UNKNOWN_BLOCK,
            "TIME_PRESSURE_DAYS": TIME_PRESSURE_DAYS,
        },
    )

    return {
        "meta": {
            "schema_version": SCHEMA_VERSION,
            "pocore_version": POCORE_VERSION,
            "run_id": run_id,
            "created_at": created_at,
            "seed": int(seed),
            "deterministic": bool(deterministic),
            "generator": {
                "name": "generator_stub",
                "version": POCORE_VERSION,
                "mode": "stub",
            },
        },
        "case_ref": {
            "case_id": cid,
            "title": title,
            "input_digest": digest,
        },
        "options": options,
        "recommendation": recommendation,
        "ethics": ethics_summary,
        "responsibility": responsibility_summary,
        "questions": questions,
        "uncertainty": uncertainty,
        "trace": trace,
    }
