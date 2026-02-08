"""
Freedom Pressure Tensor (F_P)

Based on Sartre's theory of freedom and responsibility.

The Freedom Pressure Tensor quantifies the existential weight
of choices and the pressure field of responsibility.
"""

from typing import Any, Dict, List, Optional

import numpy as np

from po_core.tensors.base import Tensor


class FreedomPressureTensor(Tensor):
    """
    Freedom Pressure Tensor (F_P).

    Represents the existential pressure arising from freedom and responsibility.
    Based on Sartre's concept that "existence precedes essence" and that
    humans are "condemned to be free."

    Dimensions:
        - Choice weight: Weight of decision
        - Responsibility degree: Level of accountability
        - Temporal urgency: Time pressure
        - Ethical stakes: Moral significance
        - Social impact: Effect on others
        - Authenticity pressure: Demand for authentic choice

    The norm of F_P represents the overall responsibility weight.
    """

    DEFAULT_DIMENSIONS = 6

    def __init__(
        self,
        name: str = "Freedom_Pressure",
        dimensions: int = DEFAULT_DIMENSIONS,
        initial_value: Optional[np.ndarray] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize Freedom Pressure Tensor.

        Args:
            name: Name of the tensor
            dimensions: Number of dimensions (default: 6)
            initial_value: Initial tensor values
            metadata: Additional metadata
        """
        super().__init__(name, dimensions, initial_value, metadata)

        # Initialize dimension names
        self.dimension_names = [
            "choice_weight",
            "responsibility_degree",
            "temporal_urgency",
            "ethical_stakes",
            "social_impact",
            "authenticity_pressure",
        ]

    def compute(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        philosopher_perspectives: Optional[List[Dict[str, Any]]] = None,
    ) -> np.ndarray:
        """
        Compute Freedom Pressure based on philosophical analysis.

        Args:
            prompt: Input prompt to analyze
            context: Optional context information
            philosopher_perspectives: List of philosopher analyses

        Returns:
            Computed F_P tensor
        """
        context = context or {}
        philosopher_perspectives = philosopher_perspectives or []

        # Base pressure from prompt analysis
        pressure = self._analyze_prompt_pressure(prompt)

        # Aggregate philosopher perspectives
        if philosopher_perspectives:
            perspective_pressure = self._aggregate_perspectives(
                philosopher_perspectives
            )
            pressure = 0.7 * pressure + 0.3 * perspective_pressure

        # Apply context modifiers
        if context:
            pressure = self._apply_context(pressure, context)

        self.data = pressure
        return self.data

    def _analyze_prompt_pressure(self, prompt: str) -> np.ndarray:
        """
        Analyze prompt to determine base pressure values.

        Args:
            prompt: Input prompt

        Returns:
            Base pressure array
        """
        prompt_lower = prompt.lower()

        # Choice weight: Presence of decision-related keywords
        choice_indicators = ["should", "must", "ought", "decide", "choose", "what"]
        choice_weight = sum(1 for word in choice_indicators if word in prompt_lower)
        choice_weight = min(choice_weight / len(choice_indicators), 1.0)

        # Responsibility degree: Ethical/moral keywords
        responsibility_indicators = [
            "responsible",
            "duty",
            "obligation",
            "accountable",
        ]
        responsibility = sum(
            1 for word in responsibility_indicators if word in prompt_lower
        )
        responsibility = min(responsibility / len(responsibility_indicators), 1.0)

        # Temporal urgency: Time-related keywords
        urgency_indicators = ["now", "urgent", "immediate", "quickly", "soon"]
        urgency = sum(1 for word in urgency_indicators if word in prompt_lower)
        urgency = min(urgency / len(urgency_indicators), 1.0)

        # Ethical stakes: Moral/ethical keywords
        ethical_indicators = [
            "right",
            "wrong",
            "good",
            "bad",
            "moral",
            "ethical",
            "virtue",
        ]
        ethical = sum(1 for word in ethical_indicators if word in prompt_lower)
        ethical = min(ethical / len(ethical_indicators), 1.0)

        # Social impact: Social keywords
        social_indicators = ["we", "us", "society", "people", "community", "others"]
        social = sum(1 for word in social_indicators if word in prompt_lower)
        social = min(social / len(social_indicators), 1.0)

        # Authenticity pressure: Self-related keywords
        authenticity_indicators = ["authentic", "genuine", "true", "self", "I"]
        authenticity = sum(
            1 for word in authenticity_indicators if word in prompt_lower
        )
        authenticity = min(authenticity / len(authenticity_indicators), 1.0)

        return np.array(
            [
                choice_weight,
                responsibility,
                urgency,
                ethical,
                social,
                authenticity,
            ],
            dtype=np.float64,
        )

    def _aggregate_perspectives(self, perspectives: List[Dict[str, Any]]) -> np.ndarray:
        """
        Aggregate freedom pressure from multiple philosopher perspectives.

        Args:
            perspectives: List of philosopher perspective dictionaries

        Returns:
            Aggregated pressure array
        """
        if not perspectives:
            return np.zeros(self.dimensions, dtype=np.float64)

        # Extract pressure indicators from each perspective
        pressures = []
        for perspective in perspectives:
            # Base pressure on perspective content
            p = self._extract_pressure_from_perspective(perspective)
            pressures.append(p)

        # Average the pressures
        return np.mean(pressures, axis=0)

    def _extract_pressure_from_perspective(
        self, perspective: Dict[str, Any]
    ) -> np.ndarray:
        """
        Extract pressure indicators from a single perspective.

        Args:
            perspective: Philosopher perspective dictionary

        Returns:
            Pressure array
        """
        # Use default medium pressure if no specific indicators
        base_pressure = 0.5

        # Adjust based on perspective metadata
        if "metadata" in perspective:
            metadata = perspective["metadata"]
            if "approach" in metadata:
                # Existentialists may increase freedom pressure
                if "existential" in metadata["approach"].lower():
                    base_pressure = 0.7

        return np.full(self.dimensions, base_pressure, dtype=np.float64)

    def _apply_context(
        self, pressure: np.ndarray, context: Dict[str, Any]
    ) -> np.ndarray:
        """
        Apply context modifiers to pressure.

        Args:
            pressure: Base pressure array
            context: Context dictionary

        Returns:
            Modified pressure array
        """
        modified = pressure.copy()

        # Increase urgency if context indicates time pressure
        if context.get("urgent"):
            modified[2] = min(modified[2] * 1.5, 1.0)

        # Increase social impact if in social context
        if context.get("social_context"):
            modified[4] = min(modified[4] * 1.3, 1.0)

        return modified

    def get_dimension_value(self, dimension_name: str) -> float:
        """
        Get value for a specific dimension.

        Args:
            dimension_name: Name of the dimension

        Returns:
            Dimension value

        Raises:
            ValueError: If dimension name is invalid
        """
        try:
            idx = self.dimension_names.index(dimension_name)
            return float(self.data[idx])
        except ValueError:
            raise ValueError(
                f"Invalid dimension name: {dimension_name}. "
                f"Valid names: {self.dimension_names}"
            )

    def get_pressure_summary(self) -> Dict[str, float]:
        """
        Get summary of pressure values by dimension.

        Returns:
            Dictionary mapping dimension names to values
        """
        return {
            name: float(self.data[i]) for i, name in enumerate(self.dimension_names)
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary with dimension details.

        Returns:
            Enhanced dictionary representation
        """
        base_dict = super().to_dict()
        base_dict["dimension_names"] = self.dimension_names
        base_dict["pressure_summary"] = self.get_pressure_summary()
        base_dict["overall_pressure"] = self.norm()
        return base_dict
