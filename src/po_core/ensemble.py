"""Deterministic ensemble runner used by CLI smoke tests."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List, Optional

from po_core.po_trace import PoTrace

DEFAULT_PHILOSOPHERS: List[str] = ["aristotle", "nietzsche", "wittgenstein"]


def run_ensemble(
    prompt: str, *, philosophers: Optional[Iterable[str]] = None, trace_sink: Optional[str] = None
) -> Dict:
    """Return a deterministic ensemble response for a given prompt.

    This helper keeps outputs stable for tests and documentation by using
    predictable scores and log messages. No external services or randomness are
    involved.
    """

    selected = list(philosophers) if philosophers is not None else DEFAULT_PHILOSOPHERS
    trace = PoTrace(prompt, sink_path=trace_sink)
    trace.record_input({"philosophers": selected})

    results = []
    base_confidence = 0.88
    for idx, name in enumerate(selected):
        contribution = {
            "name": name,
            "confidence": round(base_confidence - 0.05 * idx, 2),
            "summary": f"{name.title()} reflects on '{prompt}'.",
            "tags": ["analysis", "deterministic"],
        }
        results.append(contribution)

        blocked = []
        if contribution["confidence"] < 0.8:
            blocked.append(f"{name}_tensor")

        trace.add_philosopher_step(name, contribution, freedom_pressure=1 - contribution["confidence"], blocked_tensors=blocked)

    log = {
        "prompt": prompt,
        "philosophers": selected,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "events": [
            {"event": "ensemble_started", "philosophers": len(selected)},
            {
                "event": "ensemble_completed",
                "results_recorded": len(results),
                "status": "ok",
            },
        ],
    }

    trace.set_outputs({"results": results, "log": log})
    trace_payload = trace.persist()

    return {
        "prompt": prompt,
        "philosophers": selected,
        "results": results,
        "log": log,
        "trace": trace_payload,
    }
