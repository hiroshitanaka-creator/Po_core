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

from . import parse_input, policy_v1
from .engines import (
    ethics_v1,
    generator_stub,
    question_v1,
    recommendation_v1,
    responsibility_v1,
    uncertainty_v1,
)
from .tracer import build_trace
from .utils import deterministic_run_id, input_digest, normalize_now

# Backward-compatible module attributes for policy override tests/tools.
UNKNOWN_BLOCK = policy_v1.UNKNOWN_BLOCK
TIME_PRESSURE_DAYS = policy_v1.TIME_PRESSURE_DAYS

POCORE_VERSION = "0.3.0"
FROZEN_PROFILE_POCORE_VERSION = "0.1.0"
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
    profile = str(features.get("scenario_profile", "")) if isinstance(features, dict) else ""

    # Frozen golden contracts keep legacy metadata as-is.
    # See AGENTS.md freeze rule for case_001/case_009.
    pocore_version = (
        FROZEN_PROFILE_POCORE_VERSION
        if profile in {"job_change_transition_v1", "values_clarification_v1"}
        else POCORE_VERSION
    )

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
    ethics_rules_fired = ethics_v1.rules_fired_for(short_id=short_id, features=features)
    planning_rules_fired = generator_stub.rules_fired_for(features=features)
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
        rules_fired=ethics_rules_fired,
        planning_rules_fired=planning_rules_fired,
        arbitration_code=arbitration_code,
        policy_snapshot={
            "UNKNOWN_BLOCK": UNKNOWN_BLOCK,
            "TIME_PRESSURE_DAYS": TIME_PRESSURE_DAYS,
        },
    )

    return {
        "meta": {
            "schema_version": SCHEMA_VERSION,
            "pocore_version": pocore_version,
            "run_id": run_id,
            "created_at": created_at,
            "seed": int(seed),
            "deterministic": bool(deterministic),
            "generator": {
                "name": "generator_stub",
                "version": pocore_version,
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
