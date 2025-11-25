"""Core Po_self tensor ensemble featuring philosophical contributors."""
from .ensemble import PoSelfEnsemble, TensorEnsembleResult
from .philosophers import DerridaPhilosopher, JungPhilosopher, SartrePhilosopher
from .tensor import TensorState

__all__ = [
    "PoSelfEnsemble",
    "TensorEnsembleResult",
    "TensorState",
    "DerridaPhilosopher",
    "JungPhilosopher",
    "SartrePhilosopher",
]
