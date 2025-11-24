"""Lightweight adapters for philosophers used inside Po_self."""

from __future__ import annotations

from typing import Iterable, List

from po_core.philosophers import (
    Arendt,
    Aristotle,
    Badiou,
    Confucius,
    Deleuze,
    Derrida,
    Dewey,
    Heidegger,
    Jung,
    Kierkegaard,
    Lacan,
    Levinas,
    MerleauPonty,
    Nietzsche,
    Peirce,
    Sartre,
    WabiSabi,
    Watsuji,
    Wittgenstein,
    Zhuangzi,
)
from po_core.po_self.philosophers.adapter import PhilosopherAdapter

DEFAULT_PHILOSOPHERS = [
    Arendt,
    Aristotle,
    Badiou,
    Confucius,
    Deleuze,
    Derrida,
    Dewey,
    Heidegger,
    Jung,
    Kierkegaard,
    Lacan,
    Levinas,
    MerleauPonty,
    Nietzsche,
    Peirce,
    Sartre,
    WabiSabi,
    Watsuji,
    Wittgenstein,
    Zhuangzi,
]


def build_default_adapters() -> List[PhilosopherAdapter]:
    return [PhilosopherAdapter(philosopher()) for philosopher in DEFAULT_PHILOSOPHERS]


def adapter_names(adapters: Iterable[PhilosopherAdapter]) -> List[str]:
    return [adapter.name for adapter in adapters]


__all__ = [
    "PhilosopherAdapter",
    "adapter_names",
    "build_default_adapters",
]
