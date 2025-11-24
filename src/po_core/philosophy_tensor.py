"""Stub generator for philosophy tensor outputs."""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from typing import Sequence


STATEMENTS: Sequence[str] = (
    "The examined life is one long chain of careful questions.",
    "Doubt is the engine; wonder is the fuel.",
    "To choose is to declare what we are willing to become accountable for.",
    "Every model is a mirror; we must decide what we are ready to see.",
    "Harmony arrives when competing truths learn to keep tempo together.",
)


@dataclass
class PhilosophyResponse:
    prompt: str
    response: str
    confidence: float


def synthesize(prompt: str, seed: int) -> PhilosophyResponse:
    """Generate a deterministic philosophical response."""
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    seeded_value = seed + int(digest[:8], 16)
    random.seed(seeded_value)
    response = random.choice(STATEMENTS)
    confidence = round(0.5 + (random.random() * 0.5), 2)
    return PhilosophyResponse(prompt=prompt, response=response, confidence=confidence)
