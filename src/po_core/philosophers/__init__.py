"""
Po_core Philosophers Module

This module contains the philosophical reasoning engines.
Each philosopher represents a different perspective and approach to meaning generation.
"""

from po_core.philosophers.aristotle import Aristotle
from po_core.philosophers.base import Philosopher
from po_core.philosophers.deleuze import Deleuze
from po_core.philosophers.derrida import Derrida
from po_core.philosophers.dewey import Dewey
from po_core.philosophers.heidegger import Heidegger
from po_core.philosophers.jung import Jung
from po_core.philosophers.kierkegaard import Kierkegaard
from po_core.philosophers.lacan import Lacan
from po_core.philosophers.levinas import Levinas
from po_core.philosophers.nietzsche import Nietzsche
from po_core.philosophers.sartre import Sartre
from po_core.philosophers.wabi_sabi import WabiSabi
from po_core.philosophers.watsuji import Watsuji
from po_core.philosophers.wittgenstein import Wittgenstein

__all__ = [
    "Philosopher",
    "Aristotle",
    "Deleuze",
    "Dewey",
    "Heidegger",
    "Derrida",
    "Kierkegaard",
    "Lacan",
    "Levinas",
    "Nietzsche",
    "Sartre",
    "Jung",
    "WabiSabi",
    "Watsuji",
    "Wittgenstein",
]
