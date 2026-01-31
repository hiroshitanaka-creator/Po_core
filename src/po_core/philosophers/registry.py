"""
Philosopher Registry
====================

Builds the list of philosophers for the ensemble.
"""
from __future__ import annotations

from typing import List

from po_core.philosophers.base import PhilosopherProtocol
from po_core.philosophers.dummy import DummyPhilosopher


def build_philosophers() -> List[PhilosopherProtocol]:
    """
    Build the default list of philosophers.

    For the vertical slice, we start with just one philosopher.
    The full 39-philosopher ensemble will be integrated later.
    """
    return [DummyPhilosopher()]


__all__ = ["build_philosophers"]
