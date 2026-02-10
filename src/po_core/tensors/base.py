"""
Base Tensor Class

Abstract base class for all philosophical tensors in Po_core.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import numpy as np


class Tensor(ABC):
    """
    Abstract base class for philosophical tensors.

    A tensor in Po_core represents a philosophical concept in a
    computable mathematical structure.

    Attributes:
        name: Name of the tensor
        dimensions: Number of dimensions
        shape: Shape of the tensor array
        data: Underlying numpy array
        metadata: Additional metadata about the tensor
        created_at: Timestamp of creation
    """

    def __init__(
        self,
        name: str,
        dimensions: int,
        initial_value: Optional[Union[np.ndarray, float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize a tensor.

        Args:
            name: Name of the tensor
            dimensions: Number of dimensions
            initial_value: Initial value (scalar or array)
            metadata: Optional metadata dictionary
        """
        self.name = name
        self.dimensions = dimensions
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow().isoformat() + "Z"

        # Initialize data
        if isinstance(initial_value, np.ndarray):
            self.data = initial_value
            self.shape = initial_value.shape
        elif isinstance(initial_value, (int, float)):
            self.data = np.full(dimensions, initial_value, dtype=np.float64)
            self.shape = (dimensions,)
        else:
            self.data = np.zeros(dimensions, dtype=np.float64)
            self.shape = (dimensions,)

    @abstractmethod
    def compute(self, *args: Any, **kwargs: Any) -> np.ndarray:
        """
        Compute the tensor value based on inputs.

        This method should be implemented by subclasses to define
        the specific computation logic for each tensor type.

        Returns:
            Computed tensor as numpy array
        """
        pass

    def norm(self) -> float:
        """
        Calculate the norm (magnitude) of the tensor.

        Returns:
            L2 norm of the tensor
        """
        return float(np.linalg.norm(self.data))

    def normalize(self) -> "Tensor":
        """
        Normalize the tensor to unit length.

        Returns:
            Self for method chaining
        """
        norm_value = self.norm()
        if norm_value > 0:
            self.data = self.data / norm_value
        return self

    def dot(self, other: "Tensor") -> float:
        """
        Calculate dot product with another tensor.

        Args:
            other: Another tensor

        Returns:
            Dot product value
        """
        if self.data.shape != other.data.shape:
            raise ValueError(f"Shape mismatch: {self.data.shape} vs {other.data.shape}")
        return float(np.dot(self.data.flatten(), other.data.flatten()))

    def distance(self, other: "Tensor") -> float:
        """
        Calculate Euclidean distance to another tensor.

        Args:
            other: Another tensor

        Returns:
            Euclidean distance
        """
        if self.data.shape != other.data.shape:
            raise ValueError(f"Shape mismatch: {self.data.shape} vs {other.data.shape}")
        return float(np.linalg.norm(self.data - other.data))

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert tensor to dictionary format.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "dimensions": self.dimensions,
            "shape": list(self.shape),
            "data": self.data.tolist(),
            "norm": self.norm(),
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        """String representation of the tensor."""
        return (
            f"{self.__class__.__name__}(name='{self.name}', "
            f"shape={self.shape}, norm={self.norm():.3f})"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"⚡ {self.name} [shape={self.shape}, norm={self.norm():.3f}]"
