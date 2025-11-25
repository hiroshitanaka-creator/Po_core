"""Three-philosopher Po_self ensemble implementation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from .philosophers import DerridaPhilosopher, JungPhilosopher, Philosopher, SartrePhilosopher
from .tensor import TensorState


@dataclass
class TensorEnsembleResult:
    """Container for tensor outputs and metadata."""

    prompt: str
    base_tensor: TensorState
    philosopher_tensors: List[TensorState] = field(default_factory=list)
    composite_tensor: Optional[TensorState] = None

    def to_dict(self) -> Dict:
        return {
            "prompt": self.prompt,
            "base_tensor": self.base_tensor.to_dict(),
            "philosopher_tensors": [tensor.to_dict() for tensor in self.philosopher_tensors],
            "composite_tensor": self.composite_tensor.to_dict() if self.composite_tensor else None,
        }


class PoSelfEnsemble:
    """Minimal deterministic ensemble across Sartre, Jung, and Derrida."""

    def __init__(self, philosophers: Optional[Iterable[Philosopher]] = None) -> None:
        self.philosophers: List[Philosopher] = list(philosophers) if philosophers else [
            SartrePhilosopher(),
            JungPhilosopher(),
            DerridaPhilosopher(),
        ]

    def infer(self, prompt: str) -> TensorEnsembleResult:
        """Run the ensemble and return tensor outputs."""

        word_count = len(prompt.split())
        base_tensor = TensorState(
            name="prompt",
            value=prompt,
            description="Normalized prompt tensor",
            metadata={"word_count": word_count},
        )

        philosopher_tensors: List[TensorState] = []
        weighted_sum = 0.0
        total_weight = 0.0

        for philosopher in self.philosophers:
            tensor = philosopher.evaluate(prompt, base_tensor)
            philosopher_tensors.append(tensor)
            weight = tensor.metadata.get("weight", 0.0)
            weighted_sum += tensor.value * weight
            total_weight += weight

        composite_value = round(weighted_sum / total_weight, 3) if total_weight else 0.0
        composite_tensor = TensorState(
            name="ensemble",
            value=composite_value,
            description="Weighted philosophical agreement score",
            metadata={
                "weights": {tensor.name: tensor.metadata.get("weight", 0.0) for tensor in philosopher_tensors},
                "contributors": [tensor.name for tensor in philosopher_tensors],
            },
        )

        return TensorEnsembleResult(
            prompt=prompt,
            base_tensor=base_tensor,
            philosopher_tensors=philosopher_tensors,
            composite_tensor=composite_tensor,
        )
