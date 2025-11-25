"""Po_self: Minimal philosophical ensemble engine.

This module provides a deterministic scoring pipeline that evaluates a
prompt across a handful of philosophers. It intentionally avoids network
calls or randomness so tests and docs remain stable.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from po_core.philosophers.simple import (
    DEFAULT_PHILOSOPHERS,
    DEFAULT_PHILOSOPHER_KEYS,
    SimplePhilosopher,
)
from po_core.po_trace import PoTrace


class PoSelf:
    """Evaluate prompts using simple deterministic philosopher profiles."""

    def __init__(self, *, profiles: Iterable[SimplePhilosopher] | None = None) -> None:
        self.profiles = list(profiles or DEFAULT_PHILOSOPHERS)

    def _select_profiles(self, philosophers: Optional[Iterable[str]]) -> List[SimplePhilosopher]:
        if philosophers is None:
            return self.profiles

        wanted = set(philosophers)
        return [profile for profile in self.profiles if profile.key in wanted]

    def run(self, prompt: str, *, philosophers: Optional[Iterable[str]] = None) -> Dict:
        chosen_profiles = self._select_profiles(philosophers)
        trace = PoTrace(prompt, [profile.key for profile in chosen_profiles])
        trace.record_event(
            "ensemble_started",
            decision="Initializing deterministic philosopher scoring",
            metadata={"philosophers": [profile.key for profile in chosen_profiles]},
        )

        results = []
        for profile in chosen_profiles:
            confidence = profile.score(prompt)
            trace.record_event(
                "philosopher_scored",
                decision=profile.rationale(prompt),
                metadata={"philosopher": profile.key, "confidence": confidence},
            )
            results.append(
                {
                    "key": profile.key,
                    "name": profile.name,
                    "weight": profile.weight,
                    "description": profile.description,
                    "confidence": confidence,
                    "summary": profile.summary(prompt),
                    "tags": ["deterministic", "ensemble"],
                }
            )

        trace.record_event(
            "ensemble_completed",
            decision="Aggregated philosopher scores",
            metadata={"results_recorded": len(results)},
        )

        return {
            "prompt": prompt,
            "philosophers": [profile.key for profile in chosen_profiles],
            "results": results,
            "log": trace.to_dict(),
        }


def load_default_philosophers() -> List[str]:
    """Return the default philosopher keys."""

    return list(DEFAULT_PHILOSOPHER_KEYS)


__all__ = ["PoSelf", "load_default_philosophers"]
