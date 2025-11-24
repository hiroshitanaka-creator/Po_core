"""Deterministic ensemble runner used by CLI smoke tests."""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from po_core.po_trace import trace_recorder

DEFAULT_PHILOSOPHERS: List[str] = ["aristotle", "nietzsche", "wittgenstein"]


def run_ensemble(prompt: str, *, philosophers: Optional[Iterable[str]] = None) -> Dict:
    """Return a deterministic ensemble response for a given prompt.

    This helper keeps outputs stable for tests and documentation by using
    predictable scores and log messages. No external services or randomness are
    involved.
    """

    selected = list(philosophers) if philosophers is not None else DEFAULT_PHILOSOPHERS
    run_id = trace_recorder.start_run(prompt, selected)
    results = []
    base_confidence = 0.88
    for idx, name in enumerate(selected):
        confidence = round(base_confidence - 0.05 * idx, 2)
        summary = f"{name.title()} reflects on '{prompt}'."
        trace_recorder.log_event(
            run_id,
            "philosopher_considered",
            philosopher=name,
            confidence=confidence,
        )
        trace_recorder.log_artifact(
            run_id,
            label="summary",
            content=summary,
            philosopher=name,
        )

        results.append(
            {
                "name": name,
                "confidence": confidence,
                "summary": summary,
                "tags": ["analysis", "deterministic"],
            }
        )

    trace_recorder.complete_run(run_id, status="ok", results_recorded=len(results))
    log = trace_recorder.snapshot(run_id)

    return {
        "prompt": prompt,
        "philosophers": selected,
        "results": results,
        "log": log,
    }
