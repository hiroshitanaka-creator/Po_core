"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers
as interacting tensors.

This module orchestrates:
- Philosopher ensemble integration
- Multi-philosopher interaction mechanisms
- Freedom Pressure Tensor computation
- Semantic profile tracking
- Blocked content logging
"""

from typing import Any, Dict, List, Optional
import numpy as np

from po_core.philosophers.base import Philosopher
from po_core.tensors.freedom_pressure import FreedomPressureTensor
from po_core.tensors.semantic_profile import SemanticProfile
from po_core.tensors.blocked_tensor import BlockedTensor, BlockedEntry
from po_core.tensors.concept_quantifier import ConceptQuantifier
from po_core.tensors.interaction_tensor import InteractionTensor
from po_core.trace.tracer import ReasoningTracer, TraceLevel
from po_core.trace.annotator import PhilosophicalAnnotator


class PhilosophicalEnsemble:
    """
    Philosophical Ensemble Manager.

    Integrates multiple philosophers and manages their interactions
    through tensor-based mechanisms.

    Attributes:
        philosophers: List of philosopher instances
        tracer: Reasoning tracer for logging
        annotator: Philosophical annotator
        freedom_pressure: Freedom Pressure Tensor
        semantic_profile: Semantic Profile Tensor
        blocked_tensor: Blocked Tensor
    """

    def __init__(
        self,
        philosophers: List[Philosopher],
        enable_tracing: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize philosophical ensemble.

        Args:
            philosophers: List of philosopher instances
            enable_tracing: Whether to enable reasoning tracing
            metadata: Additional metadata
        """
        self.philosophers = philosophers
        self.metadata = metadata or {}
        self.enable_tracing = enable_tracing

        # Initialize components
        self.tracer: Optional[ReasoningTracer] = None
        self.annotator = PhilosophicalAnnotator()

        # Initialize tensors
        self.freedom_pressure = FreedomPressureTensor()
        self.semantic_profile = SemanticProfile()
        self.blocked_tensor = BlockedTensor()
        self.concept_quantifier = ConceptQuantifier()
        self.interaction_tensor = InteractionTensor(num_philosophers=len(philosophers))

        # Interaction history
        self.interaction_history: List[Dict[str, Any]] = []

    def reason(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        philosophers_subset: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate philosophical reasoning through ensemble.

        Args:
            prompt: Input prompt
            context: Optional context information
            philosophers_subset: Optional subset of philosophers to use

        Returns:
            Ensemble reasoning result
        """
        context = context or {}

        # Initialize tracer
        if self.enable_tracing:
            self.tracer = ReasoningTracer(
                prompt=prompt, metadata={"context": context, "ensemble_size": len(self.philosophers)}
            )
            self.tracer.log_event(
                level=TraceLevel.INFO,
                event="ensemble_reasoning_started",
                message=f"Starting ensemble reasoning with {len(self.philosophers)} philosophers",
            )

        # Filter philosophers if subset specified
        active_philosophers = self._get_active_philosophers(philosophers_subset)

        # Stage 1: Collect individual philosopher perspectives
        perspectives = self._collect_perspectives(prompt, context, active_philosophers)

        # Stage 2: Compute Freedom Pressure
        freedom_pressure_data = self._compute_freedom_pressure(
            prompt, context, perspectives
        )

        # Stage 3: Analyze semantic evolution
        semantic_data = self._track_semantic_evolution(prompt, perspectives)

        # Stage 4: Detect and log blocked content
        blocked_data = self._identify_blocked_content(perspectives)

        # Stage 5: Synthesize ensemble response
        synthesis = self._synthesize_response(
            prompt, perspectives, freedom_pressure_data, semantic_data
        )

        # Stage 6: Add philosophical annotations
        annotations = self._annotate_reasoning(synthesis, perspectives)

        # Stage 7: Calculate philosopher interactions
        interaction_data = self._calculate_interactions(perspectives)

        # Stage 8: Quantify key philosophical concepts
        concept_data = self._quantify_concepts(prompt, perspectives, annotations)

        # Complete tracing
        result = {
            "prompt": prompt,
            "philosophers": [p.name for p in active_philosophers],
            "perspectives": perspectives,
            "synthesis": synthesis,
            "freedom_pressure": freedom_pressure_data,
            "semantic_profile": semantic_data,
            "blocked_content": blocked_data,
            "annotations": annotations,
            "interactions": interaction_data,
            "concepts": concept_data,
            "metadata": self.metadata,
        }

        if self.tracer:
            self.tracer.complete(result=result)
            result["trace"] = self.tracer.to_dict()

        return result

    def _get_active_philosophers(
        self, subset: Optional[List[str]]
    ) -> List[Philosopher]:
        """Get active philosophers for this reasoning session."""
        if subset is None:
            return self.philosophers

        return [p for p in self.philosophers if p.name in subset]

    def _collect_perspectives(
        self,
        prompt: str,
        context: Dict[str, Any],
        philosophers: List[Philosopher],
    ) -> List[Dict[str, Any]]:
        """
        Collect reasoning from each philosopher.

        Args:
            prompt: Input prompt
            context: Context dictionary
            philosophers: Active philosophers

        Returns:
            List of perspective dictionaries
        """
        perspectives = []

        for philosopher in philosophers:
            # Get philosopher's reasoning
            reasoning = philosopher.reason(prompt, context)

            perspective = {
                "philosopher": philosopher.name,
                "reasoning": reasoning,
            }

            perspectives.append(perspective)

            # Log to tracer
            if self.tracer:
                self.tracer.log_philosopher_reasoning(
                    philosopher=philosopher.name,
                    reasoning=reasoning,
                )

        return perspectives

    def _compute_freedom_pressure(
        self,
        prompt: str,
        context: Dict[str, Any],
        perspectives: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Compute Freedom Pressure Tensor.

        Args:
            prompt: Input prompt
            context: Context dictionary
            perspectives: Philosopher perspectives

        Returns:
            Freedom pressure data
        """
        self.freedom_pressure.compute(
            prompt=prompt,
            context=context,
            philosopher_perspectives=perspectives,
        )

        pressure_data = self.freedom_pressure.to_dict()

        # Log to tracer
        if self.tracer:
            self.tracer.log_tensor_computation(
                tensor_name="Freedom_Pressure",
                tensor_data=pressure_data,
            )

        return pressure_data

    def _track_semantic_evolution(
        self, prompt: str, perspectives: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Track semantic evolution through perspectives.

        Args:
            prompt: Input prompt
            perspectives: Philosopher perspectives

        Returns:
            Semantic profile data
        """
        # Start with prompt
        previous_state = self.semantic_profile.compute(prompt)

        # Track evolution through each perspective
        for perspective in perspectives:
            reasoning_text = str(perspective.get("reasoning", ""))
            self.semantic_profile.compute(
                text=reasoning_text,
                previous_state=previous_state.copy(),
            )
            previous_state = self.semantic_profile.data.copy()

        semantic_data = self.semantic_profile.to_dict()

        # Log to tracer
        if self.tracer:
            self.tracer.log_tensor_computation(
                tensor_name="Semantic_Profile",
                tensor_data=semantic_data,
            )

        return semantic_data

    def _identify_blocked_content(
        self, perspectives: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Identify and log blocked/rejected content.

        Args:
            perspectives: Philosopher perspectives

        Returns:
            Blocked content data
        """
        # This is a simplified implementation
        # In a real system, this would analyze perspective conflicts
        # and identify what was rejected

        # Example: Check for contradictions or filtered content
        for perspective in perspectives:
            philosopher = perspective["philosopher"]
            reasoning = perspective.get("reasoning", {})

            # Check if reasoning includes rejection indicators
            reasoning_text = str(reasoning)
            if any(word in reasoning_text.lower() for word in ["reject", "filter", "avoid"]):
                # Log as blocked content
                self.blocked_tensor.add_blocked_entry(
                    content="[Detected filtered content]",
                    reason="Philosopher applied filtering",
                    philosopher=philosopher,
                )

                if self.tracer:
                    self.tracer.log_blocked_content(
                        content="[Filtered by philosopher]",
                        reason="Applied philosophical filtering",
                        philosopher=philosopher,
                    )

        blocked_data = self.blocked_tensor.to_dict()

        # Log to tracer
        if self.tracer:
            self.tracer.log_tensor_computation(
                tensor_name="Blocked_Tensor",
                tensor_data=blocked_data,
            )

        return blocked_data

    def _synthesize_response(
        self,
        prompt: str,
        perspectives: List[Dict[str, Any]],
        freedom_pressure: Dict[str, Any],
        semantic_profile: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Synthesize ensemble response from perspectives.

        Args:
            prompt: Input prompt
            perspectives: Philosopher perspectives
            freedom_pressure: Freedom pressure data
            semantic_profile: Semantic profile data

        Returns:
            Synthesized response
        """
        # Extract key insights from each perspective
        insights = []
        tensions = []

        for perspective in perspectives:
            philosopher = perspective["philosopher"]
            reasoning = perspective.get("reasoning", {})

            # Extract reasoning text
            if isinstance(reasoning, dict):
                reasoning_text = reasoning.get("reasoning", "")
            else:
                reasoning_text = str(reasoning)

            insights.append({
                "philosopher": philosopher,
                "insight": reasoning_text[:200] + "..." if len(reasoning_text) > 200 else reasoning_text,
            })

        # Identify philosophical tensions
        # (Simplified - in reality would do deeper analysis)
        if len(perspectives) > 1:
            tensions.append({
                "description": "Multiple philosophical perspectives present",
                "philosophers": [p["philosopher"] for p in perspectives],
            })

        # Overall synthesis
        synthesis = {
            "insights": insights,
            "tensions": tensions,
            "overall_pressure": freedom_pressure.get("overall_pressure", 0.0),
            "semantic_evolution": semantic_profile.get("total_evolution", 0.0),
        }

        # Log decision
        if self.tracer:
            self.tracer.log_decision(
                decision="Ensemble synthesis completed",
                reasoning=f"Integrated {len(perspectives)} perspectives",
                alternatives=[p["philosopher"] for p in perspectives],
            )

        return synthesis

    def _annotate_reasoning(
        self,
        synthesis: Dict[str, Any],
        perspectives: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Add philosophical annotations.

        Args:
            synthesis: Synthesized response
            perspectives: Philosopher perspectives

        Returns:
            List of annotations
        """
        all_annotations = []

        # Annotate each perspective
        for perspective in perspectives:
            annotations = self.annotator.annotate_reasoning(
                reasoning=perspective.get("reasoning", {}),
                philosopher=perspective.get("philosopher"),
            )

            for annotation in annotations:
                all_annotations.append(annotation.to_dict())

        return all_annotations

    def _calculate_interactions(
        self, perspectives: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate philosopher interactions.

        Args:
            perspectives: Philosopher perspectives

        Returns:
            Interaction data including harmony, tension, and influence
        """
        # Compute interaction tensor
        self.interaction_tensor.compute(perspectives)

        # Extract interaction matrices
        harmony_matrix = self.interaction_tensor.get_harmony_matrix()
        tension_matrix = self.interaction_tensor.get_tension_matrix()
        synthesis_potential = self.interaction_tensor.get_synthesis_potential_matrix()

        # Get philosopher names
        philosopher_names = [p.get("philosopher", "") for p in perspectives]

        # Log to tracer
        if self.tracer:
            self.tracer.log_tensor_computation(
                tensor_name="Interaction_Tensor",
                tensor_data=self.interaction_tensor.data.tolist(),
                metadata={
                    "philosophers": philosopher_names,
                    "average_harmony": float(np.mean(harmony_matrix)),
                    "average_tension": float(np.mean(tension_matrix)),
                }
            )

        # Store interaction history
        self.interaction_history.append({
            "philosophers": philosopher_names,
            "harmony_matrix": harmony_matrix.tolist(),
            "tension_matrix": tension_matrix.tolist(),
            "synthesis_potential": synthesis_potential.tolist(),
        })

        return {
            "philosophers": philosopher_names,
            "harmony_matrix": harmony_matrix.tolist(),
            "tension_matrix": tension_matrix.tolist(),
            "synthesis_potential_matrix": synthesis_potential.tolist(),
            "average_harmony": float(np.mean(harmony_matrix)),
            "average_tension": float(np.mean(tension_matrix)),
            "pairwise_interactions": [
                interaction.to_dict()
                for interaction in self.interaction_tensor.interactions.values()
            ],
        }

    def _quantify_concepts(
        self,
        prompt: str,
        perspectives: List[Dict[str, Any]],
        annotations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Quantify philosophical concepts.

        Args:
            prompt: Input prompt
            perspectives: Philosopher perspectives
            annotations: Philosophical annotations

        Returns:
            Quantified concept data
        """
        quantified_concepts = []

        # Extract concepts from annotations
        concept_names = set()
        for annotation in annotations:
            concept_name = annotation.get("concept", "")
            if concept_name:
                concept_names.add(concept_name)

        # Quantify each concept for each philosopher
        for perspective in perspectives:
            philosopher = perspective.get("philosopher", "")
            reasoning = perspective.get("reasoning", {})

            # Extract text from reasoning
            if isinstance(reasoning, dict):
                text = reasoning.get("reasoning", "")
            else:
                text = str(reasoning)

            # Quantify concepts mentioned by this philosopher
            for concept_name in concept_names:
                if concept_name.lower() in text.lower():
                    # Compute quantification
                    self.concept_quantifier.compute(
                        concept_name=concept_name,
                        philosopher=philosopher,
                        text=text
                    )

                    # Get quantified concept
                    concept = self.concept_quantifier.get_concept(concept_name, philosopher)
                    if concept:
                        quantified_concepts.append(concept.to_dict())
                    else:
                        # Create from current data
                        quantified_concepts.append({
                            "name": concept_name,
                            "philosopher": philosopher,
                            "vector": self.concept_quantifier.data.tolist(),
                            "confidence": 0.7,
                        })

        # Log to tracer
        if self.tracer:
            self.tracer.log_event(
                level=TraceLevel.INFO,
                event="concept_quantification",
                message=f"Quantified {len(quantified_concepts)} philosophical concepts",
                data={"concepts": [c.get("name") for c in quantified_concepts]}
            )

        return {
            "quantified_concepts": quantified_concepts,
            "concept_space_dimensions": self.concept_quantifier.dimension_names,
            "total_concepts": len(quantified_concepts),
        }

    def get_interaction_history(self) -> List[Dict[str, Any]]:
        """Get history of philosopher interactions."""
        return self.interaction_history

    def reset(self) -> None:
        """Reset ensemble state."""
        self.freedom_pressure = FreedomPressureTensor()
        self.semantic_profile = SemanticProfile()
        self.blocked_tensor = BlockedTensor()
        self.concept_quantifier = ConceptQuantifier()
        self.interaction_tensor = InteractionTensor(num_philosophers=len(self.philosophers))
        self.interaction_history = []
        self.tracer = None


# Convenience function for CLI compatibility
def cli() -> None:
    """Po_self CLI entry point."""
    from rich.console import Console

    console = Console()
    console.print("[bold magenta]🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    console.print("Full ensemble implementation is now active!")
    console.print("\nFeatures:")
    console.print("  ✓ Philosopher ensemble integration")
    console.print("  ✓ Freedom Pressure Tensor computation")
    console.print("  ✓ Semantic profile tracking")
    console.print("  ✓ Blocked content logging")
    console.print("  ✓ Philosophical annotations")


if __name__ == "__main__":
    cli()
