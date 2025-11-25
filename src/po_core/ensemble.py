"""Deterministic ensemble runner used by CLI smoke tests."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from po_core import philosophers
from po_core.philosophers.base import Philosopher

DEFAULT_PHILOSOPHERS: List[str] = ["aristotle", "nietzsche", "wittgenstein"]


PHILOSOPHER_REGISTRY: Dict[str, type[Philosopher]] = {
    "arendt": philosophers.Arendt,
    "aristotle": philosophers.Aristotle,
    "badiou": philosophers.Badiou,
    "confucius": philosophers.Confucius,
    "deleuze": philosophers.Deleuze,
    "derrida": philosophers.Derrida,
    "dewey": philosophers.Dewey,
    "heidegger": philosophers.Heidegger,
    "jung": philosophers.Jung,
    "kierkegaard": philosophers.Kierkegaard,
    "lacan": philosophers.Lacan,
    "levinas": philosophers.Levinas,
    "merleau_ponty": philosophers.MerleauPonty,
    "nietzsche": philosophers.Nietzsche,
    "peirce": philosophers.Peirce,
    "sartre": philosophers.Sartre,
    "wabi_sabi": philosophers.WabiSabi,
    "watsuji": philosophers.Watsuji,
    "wittgenstein": philosophers.Wittgenstein,
    "zhuangzi": philosophers.Zhuangzi,
}


@dataclass
class PhilosopherTensor:
    """Structured view of a philosopher's contribution."""

    name: str
    reasoning: str
    perspective: str
    freedom_pressure: float
    semantic_delta: float
    blocked_tensor: float
    tension: str | None = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "reasoning": self.reasoning,
            "perspective": self.perspective,
            "tension": self.tension,
            "freedom_pressure": self.freedom_pressure,
            "semantic_delta": self.semantic_delta,
            "blocked_tensor": self.blocked_tensor,
        }


@dataclass
class EnsembleMetrics:
    """Aggregate ensemble metrics."""

    freedom_pressure: float
    semantic_delta: float
    blocked_tensor: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "freedom_pressure": self.freedom_pressure,
            "semantic_delta": self.semantic_delta,
            "blocked_tensor": self.blocked_tensor,
        }


def _tokenize(text: str) -> List[str]:
    tokens: List[str] = []
    for raw in text.split():
        cleaned = raw.strip(".,!?\"'()[]{}:;`").lower()
        if cleaned:
            tokens.append(cleaned)
    return tokens


def _compute_freedom_pressure(reasoning: str) -> float:
    tokens = _tokenize(reasoning)
    if not tokens:
        return 0.35
    unique_ratio = len(set(tokens)) / len(tokens)
    return round(0.35 + 0.65 * unique_ratio, 2)


def _compute_semantic_delta(prompt: str, reasoning: str) -> float:
    prompt_tokens = set(_tokenize(prompt))
    reasoning_tokens = set(_tokenize(reasoning))
    if not prompt_tokens or not reasoning_tokens:
        return 1.0
    overlap = len(prompt_tokens & reasoning_tokens)
    coverage = overlap / len(prompt_tokens)
    return round(1 - coverage, 2)


def _compute_blocked_tensor(freedom_pressure: float, semantic_delta: float) -> float:
    return round(max(0.0, (1 - freedom_pressure) * 0.5 + semantic_delta * 0.5), 2)


def _load_philosophers(names: Iterable[str]) -> List[Philosopher]:
    loaded: List[Philosopher] = []
    for name in names:
        key = name.lower()
        if key not in PHILOSOPHER_REGISTRY:
            raise ValueError(f"Unknown philosopher: {name}")
        loaded.append(PHILOSOPHER_REGISTRY[key]())
    return loaded


def _aggregate_metrics(tensors: List[PhilosopherTensor]) -> EnsembleMetrics:
    if not tensors:
        return EnsembleMetrics(0.0, 0.0, 0.0)

    freedom_avg = round(sum(t.freedom_pressure for t in tensors) / len(tensors), 2)
    delta_avg = round(sum(t.semantic_delta for t in tensors) / len(tensors), 2)
    blocked_avg = round(sum(t.blocked_tensor for t in tensors) / len(tensors), 2)
    return EnsembleMetrics(freedom_avg, delta_avg, blocked_avg)


def run_ensemble(prompt: str, *, philosophers: Optional[Iterable[str]] = None) -> Dict:
    """Return a structured ensemble response for a given prompt."""

    selected = list(philosophers) if philosophers is not None else DEFAULT_PHILOSOPHERS
    thinkers = _load_philosophers(selected)

    tensors: List[PhilosopherTensor] = []
    for thinker in thinkers:
        reasoning_result = thinker.reason(prompt)
        reasoning_text = str(reasoning_result.get("reasoning", ""))
        perspective = str(reasoning_result.get("perspective", ""))
        tension = reasoning_result.get("tension")

        freedom_pressure = _compute_freedom_pressure(reasoning_text)
        semantic_delta = _compute_semantic_delta(prompt, reasoning_text)
        blocked_tensor = _compute_blocked_tensor(freedom_pressure, semantic_delta)

        tensors.append(
            PhilosopherTensor(
                name=thinker.name,
                reasoning=reasoning_text,
                perspective=perspective,
                tension=tension,
                freedom_pressure=freedom_pressure,
                semantic_delta=semantic_delta,
                blocked_tensor=blocked_tensor,
            )
        )

    aggregate = _aggregate_metrics(tensors)
    ranked = sorted(tensors, key=lambda tensor: tensor.freedom_pressure, reverse=True)

    log = {
        "prompt": prompt,
        "philosophers": selected,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "events": [
            {"event": "ensemble_started", "philosophers": len(selected)},
            {
                "event": "ensemble_completed",
                "results_recorded": len(tensors),
                "status": "ok" if tensors else "empty",
            },
        ],
    }

    consensus_text = ranked[0].reasoning if ranked else ""

    return {
        "prompt": prompt,
        "philosophers": selected,
        "responses": [tensor.to_dict() for tensor in tensors],
        "aggregate": aggregate.to_dict(),
        "consensus": {
            "leader": ranked[0].name if ranked else None,
            "text": consensus_text,
        },
        "log": log,
    }
