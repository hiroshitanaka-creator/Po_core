"""
Po_core Philosophers Module

This module contains the philosophical reasoning engines.
Each philosopher represents a different perspective and approach to meaning generation.
"""

from po_core.philosophers.aristotle import Aristotle
from po_core.philosophers.base import Philosopher
from po_core.philosophers.derrida import Derrida
from po_core.philosophers.heidegger import Heidegger
from po_core.philosophers.jung import Jung
from po_core.philosophers.sartre import Sartre
from po_core.philosophers.watsuji import Watsuji

__all__ = [
    "Philosopher",
    "Aristotle",
    "Heidegger",
    "Derrida",
    "Sartre",
    "Jung",
    "Watsuji",
]
