"""Deterministic ensemble runner used by CLI smoke tests."""
from __future__ import annotations

from typing import Dict, Iterable, Optional

from po_core.po_self import PoSelf, load_default_philosophers

DEFAULT_PHILOSOPHERS = load_default_philosophers()


def run_ensemble(prompt: str, *, philosophers: Optional[Iterable[str]] = None) -> Dict:
    """Return a deterministic ensemble response for a given prompt."""

    engine = PoSelf()
    return engine.run(prompt, philosophers=philosophers)


__all__ = ["run_ensemble", "DEFAULT_PHILOSOPHERS"]
