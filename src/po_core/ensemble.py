"""Deterministic ensemble runner used by CLI smoke tests."""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from po_core.po_trace import PoTrace, TraceLevel

DEFAULT_PHILOSOPHERS: List[str] = ["aristotle", "nietzsche", "wittgenstein"]


def run_ensemble(
    prompt: str,
    *,
    philosophers: Optional[Iterable[str]] = None,
    trace_level: str = TraceLevel.CONCISE.value,
    trace_output: Optional[str] = None,
) -> Dict:
    """Return a deterministic ensemble response for a given prompt.

    This helper keeps outputs stable for tests and documentation by using
    predictable scores and log messages. No external services or randomness are
    involved.
    """

    selected = list(philosophers) if philosophers is not None else DEFAULT_PHILOSOPHERS
    tracer = PoTrace(prompt=prompt)
    tracer.record_event("ensemble_started", philosophers=len(selected))

    results = []
    base_confidence = 0.88
    trace_level_enum = TraceLevel(trace_level)

    for idx, name in enumerate(selected):
        confidence = round(base_confidence - 0.05 * idx, 2)
        summary = f"{name.title()} reflects on '{prompt}'."
        results.append(
            {
                "name": name,
                "confidence": confidence,
                "summary": summary,
                "tags": ["analysis", "deterministic"],
            }
        )

        tracer.record_emission(name, summary)
        tracer.log_reason(
            name,
            reason=f"Weighted perspective {idx + 1} with confidence {confidence}.",
        )
        tracer.log_rejection(
            name,
            content=f"{name.title()} withheld speculation about '{prompt}'.",
            rationale="Speculative content intentionally suppressed to keep reasoning auditable.",
        )
        tracer.attribute(
            name,
            weight=round(confidence / base_confidence, 2),
            note="Deterministic weighting for demo run.",
        )

    tracer.record_event("ensemble_completed", results_recorded=len(results), status="ok")

    trace_data = tracer.to_dict(level=trace_level_enum)
    tracer.export(trace_output, level=trace_level_enum)

    return {
        "prompt": prompt,
        "philosophers": selected,
        "results": results,
        "trace": trace_data,
        "log": trace_data,
    }
