"""
Po_core Philosophers Module

This module contains the philosophical reasoning engines.
Each philosopher represents a different perspective and approach to meaning generation.
"""

from po_core.philosophers.base import Philosopher
from po_core.philosophers.derrida import Derrida
from po_core.philosophers.heidegger import Heidegger
from po_core.philosophers.sartre import Sartre

__all__ = [
    "Philosopher",
    "Heidegger",
    "Derrida",
    "Sartre",
]
