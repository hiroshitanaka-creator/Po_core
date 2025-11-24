"""Philosophical ensemble and design signals for Po_self."""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Optional

from po_core.philosophers import (
    Heidegger,
    Levinas,
    Nietzsche,
    Philosopher,
    PhilosopherSignal,
    Sartre,
    Watsuji,
)


@dataclass
class DesignSignals:
    """Lightweight container for README-driven design cues."""

    freedom_pressure: float
    ethical_resonance: float
    responsibility_pressure: float
    meaning_profile: Dict[str, float] = field(default_factory=dict)


@dataclass
class EnsembleResult:
    """Aggregated result of Po_self ensemble reasoning."""

    prompt: str
    response: str
    weights: Dict[str, float]
    philosopher_signals: List[PhilosopherSignal]
    design_signals: DesignSignals


def compute_meaning_profile(prompt: str) -> Dict[str, float]:
    """Derive a minimal meaning profile inspired by README signals."""

    tokens = [token.strip(".,!?") for token in prompt.lower().split() if token]
    length = max(len(tokens), 1)

    poetic = sum(1 for token in tokens if len(token) >= 7) / length
    action = sum(1 for token in tokens if token.endswith("ing")) / length
    relation = sum(1 for token in tokens if token in {"with", "together", "between", "relation"}) / length

    return {
        "poetic_granularity": round(poetic, 3),
        "action_intent": round(action, 3),
        "relational_density": round(relation, 3),
    }


def compute_freedom_pressure_tensor(prompt: str, observation_pressure: float = 0.5) -> float:
    """Approximate the freedom pressure tensor from prompt features."""

    prompt_energy = min(len(prompt) / 280, 1.0)
    creativity_bias = 0.35 if any(symbol in prompt for symbol in {"?", "!"}) else 0.15
    freedom_pressure = prompt_energy * (1 - observation_pressure) + creativity_bias

    return round(min(max(freedom_pressure, 0.0), 1.0), 3)


def compute_ethical_resonance(prompt: str) -> float:
    """Estimate ethical resonance by detecting normative vocabulary."""

    ethical_tokens = {"should", "must", "responsibility", "ethic", "care", "justice", "duty"}
    tokens = prompt.lower().split()
    if not tokens:
        return 0.0

    matches = sum(1 for token in tokens if any(key in token for key in ethical_tokens))
    return round(min(matches / len(tokens) + 0.1, 1.0), 3)


def compute_design_signals(prompt: str, observation_pressure: float = 0.5) -> DesignSignals:
    """Bundle core design signals (freedom, ethics, responsibility)."""

    freedom_pressure = compute_freedom_pressure_tensor(prompt, observation_pressure)
    ethical_resonance = compute_ethical_resonance(prompt)
    meaning_profile = compute_meaning_profile(prompt)

    responsibility_pressure = round(
        (freedom_pressure + ethical_resonance) / 2 + meaning_profile["relational_density"] * 0.2,
        3,
    )

    return DesignSignals(
        freedom_pressure=freedom_pressure,
        ethical_resonance=ethical_resonance,
        responsibility_pressure=min(responsibility_pressure, 1.0),
        meaning_profile=meaning_profile,
    )


def _normalize_weights(philosophers: Iterable[Philosopher], weights: Optional[Mapping[str, float]]) -> Dict[str, float]:
    provided = weights or {}
    normalized: Dict[str, float] = {}

    for philosopher in philosophers:
        normalized[philosopher.name] = float(provided.get(philosopher.name, 1.0))

    total = sum(normalized.values()) or 1.0
    return {name: value / total for name, value in normalized.items()}


def load_default_philosophers() -> List[Philosopher]:
    """Load a compact yet diverse ensemble of philosophers."""

    return [Nietzsche(), Sartre(), Heidegger(), Levinas(), Watsuji()]


def run_ensemble(
    prompt: str,
    *,
    observation_pressure: float = 0.5,
    weights: Optional[Mapping[str, float]] = None,
    philosophers: Optional[List[Philosopher]] = None,
) -> EnsembleResult:
    """Execute Po_self ensemble reasoning with simple weighted aggregation."""

    if not prompt.strip():
        raise ValueError("Prompt must not be empty")

    philosopher_instances = philosophers or load_default_philosophers()
    weight_map = _normalize_weights(philosopher_instances, weights)

    signals = [philosopher.analyze(prompt) for philosopher in philosopher_instances]
    design_signals = compute_design_signals(prompt, observation_pressure)

    weighted_fragments = [
        f"{signal.name}: {signal.reasoning}" for signal in signals if signal.reasoning
    ]
    response = " \n".join(weighted_fragments[:3]) or "No reasoning available."

    return EnsembleResult(
        prompt=prompt,
        response=response,
        weights=weight_map,
        philosopher_signals=signals,
        design_signals=design_signals,
    )
