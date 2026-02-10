"""
Tensor Metrics Module

Advanced tensor-based metrics for Po_core philosophical reasoning analysis.
Implements Freedom Pressure Tensor (F_P), Semantic Profile, and Blocked Tensor.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Lazy load the sentence transformer model
_SENTENCE_MODEL: Optional[SentenceTransformer] = None


def _get_sentence_model() -> SentenceTransformer:
    """Get or initialize the sentence transformer model."""
    global _SENTENCE_MODEL
    if _SENTENCE_MODEL is None:
        _SENTENCE_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _SENTENCE_MODEL


@dataclass
class FreedomPressureTensor:
    """
    Multi-dimensional Freedom Pressure Tensor.

    Represents the "freedom" or "constraint" experienced by a philosopher
    during reasoning, measured across multiple dimensions.
    """

    # Lexical freedom: Vocabulary diversity and richness
    lexical_freedom: float

    # Semantic freedom: Divergence from prompt constraints
    semantic_freedom: float

    # Structural freedom: Reasoning pattern complexity
    structural_freedom: float

    # Overall freedom pressure (0-1, higher = more freedom)
    overall: float

    # Raw tensor representation
    tensor: torch.Tensor

    @classmethod
    def compute(
        cls, prompt: str, reasoning: str, philosopher_name: str = "unknown"
    ) -> "FreedomPressureTensor":
        """
        Compute Freedom Pressure Tensor from prompt and reasoning.

        Args:
            prompt: The input prompt
            reasoning: The philosopher's reasoning text
            philosopher_name: Name of the philosopher (for logging)

        Returns:
            FreedomPressureTensor instance
        """
        # 1. Lexical Freedom: Token diversity
        tokens = reasoning.split()
        if not tokens:
            lexical_freedom = 0.0
        else:
            unique_ratio = len(set(tokens)) / len(tokens)
            # Scaled to 0-1, with 0.5 as average
            lexical_freedom = min(1.0, unique_ratio * 1.5)

        # 2. Semantic Freedom: Embedding-based divergence
        semantic_freedom = _compute_semantic_freedom(prompt, reasoning)

        # 3. Structural Freedom: Sentence complexity
        structural_freedom = _compute_structural_freedom(reasoning)

        # 4. Overall freedom (weighted average)
        overall = (
            lexical_freedom * 0.3 + semantic_freedom * 0.5 + structural_freedom * 0.2
        )

        # 5. Create tensor representation
        tensor = torch.tensor(
            [lexical_freedom, semantic_freedom, structural_freedom, overall],
            dtype=torch.float32,
        )

        return cls(
            lexical_freedom=round(lexical_freedom, 3),
            semantic_freedom=round(semantic_freedom, 3),
            structural_freedom=round(structural_freedom, 3),
            overall=round(overall, 3),
            tensor=tensor,
        )

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format."""
        return {
            "lexical_freedom": self.lexical_freedom,
            "semantic_freedom": self.semantic_freedom,
            "structural_freedom": self.structural_freedom,
            "overall": self.overall,
        }


@dataclass
class SemanticProfile:
    """
    Semantic profile representing meaning space of reasoning.

    Uses sentence embeddings to capture semantic relationships.
    """

    # Embedding vector
    embedding: torch.Tensor

    # Similarity to prompt (0-1)
    prompt_similarity: float

    # Semantic coherence score (0-1)
    coherence: float

    @classmethod
    def compute(cls, prompt: str, reasoning: str) -> "SemanticProfile":
        """
        Compute semantic profile from prompt and reasoning.

        Args:
            prompt: The input prompt
            reasoning: The philosopher's reasoning text

        Returns:
            SemanticProfile instance
        """
        model = _get_sentence_model()

        # Get embeddings
        prompt_embedding = model.encode(prompt, convert_to_tensor=True)
        reasoning_embedding = model.encode(reasoning, convert_to_tensor=True)

        # Compute cosine similarity
        similarity = torch.nn.functional.cosine_similarity(
            prompt_embedding.unsqueeze(0), reasoning_embedding.unsqueeze(0)
        ).item()

        # Normalize to 0-1 range (cosine similarity is -1 to 1)
        prompt_similarity = (similarity + 1) / 2

        # Compute coherence (self-similarity of reasoning sentences)
        coherence = _compute_coherence(reasoning, model)

        return cls(
            embedding=reasoning_embedding,
            prompt_similarity=round(prompt_similarity, 3),
            coherence=round(coherence, 3),
        )

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format."""
        return {
            "prompt_similarity": self.prompt_similarity,
            "coherence": self.coherence,
        }


@dataclass
class BlockedTensor:
    """
    Blocked Tensor: Combined metric of freedom and semantic constraint.

    Represents the overall "blocking" or constraint on philosophical reasoning.
    Higher values indicate more constraint/blocking.
    """

    # Freedom pressure component (inverted: higher F_P = lower blocking)
    freedom_component: float

    # Semantic delta component (higher delta = more blocking)
    semantic_component: float

    # Overall blocking score (0-1, higher = more blocked)
    overall: float

    # Tensor representation
    tensor: torch.Tensor

    @classmethod
    def compute(
        cls, freedom_pressure: FreedomPressureTensor, semantic_profile: SemanticProfile
    ) -> "BlockedTensor":
        """
        Compute Blocked Tensor from freedom pressure and semantic profile.

        Args:
            freedom_pressure: FreedomPressureTensor instance
            semantic_profile: SemanticProfile instance

        Returns:
            BlockedTensor instance
        """
        # Freedom component: Inverse of freedom (high freedom = low blocking)
        freedom_component = 1.0 - freedom_pressure.overall

        # Semantic component: Inverse of similarity (low similarity = high blocking)
        semantic_component = 1.0 - semantic_profile.prompt_similarity

        # Overall blocking with non-linear combination
        # Using geometric mean for more sensitivity
        overall = np.sqrt(freedom_component * semantic_component)

        # Create tensor
        tensor = torch.tensor(
            [freedom_component, semantic_component, overall], dtype=torch.float32
        )

        return cls(
            freedom_component=round(freedom_component, 3),
            semantic_component=round(semantic_component, 3),
            overall=round(overall, 3),
            tensor=tensor,
        )

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format."""
        return {
            "freedom_component": self.freedom_component,
            "semantic_component": self.semantic_component,
            "overall": self.overall,
        }


# Helper functions


def _compute_semantic_freedom(prompt: str, reasoning: str) -> float:
    """
    Compute semantic freedom using sentence embeddings.

    Higher divergence from prompt = higher freedom.
    """
    try:
        model = _get_sentence_model()

        prompt_emb = model.encode(prompt, convert_to_tensor=True)
        reasoning_emb = model.encode(reasoning, convert_to_tensor=True)

        # Cosine similarity
        similarity = torch.nn.functional.cosine_similarity(
            prompt_emb.unsqueeze(0), reasoning_emb.unsqueeze(0)
        ).item()

        # Convert to freedom (inverse of similarity)
        # Normalize from [-1, 1] to [0, 1]
        freedom = (1 - similarity) / 2

        return max(0.0, min(1.0, freedom))
    except Exception:
        # Fallback to simple token-based metric
        prompt_tokens = set(prompt.lower().split())
        reasoning_tokens = set(reasoning.lower().split())
        if not prompt_tokens or not reasoning_tokens:
            return 0.5

        overlap = len(prompt_tokens & reasoning_tokens)
        coverage = overlap / len(prompt_tokens)
        return 1.0 - coverage


def _compute_structural_freedom(reasoning: str) -> float:
    """
    Compute structural freedom based on sentence complexity.

    Measures variability in sentence length and structure.
    """
    sentences = [s.strip() for s in reasoning.split(".") if s.strip()]
    if len(sentences) < 2:
        return 0.5

    # Sentence length variance (normalized)
    lengths = [len(s.split()) for s in sentences]
    mean_length = np.mean(lengths)
    std_length = np.std(lengths)

    if mean_length == 0:
        return 0.5

    # Coefficient of variation (normalized to 0-1)
    cv = std_length / mean_length
    freedom = min(1.0, cv)

    return freedom


def _compute_coherence(text: str, model: SentenceTransformer) -> float:
    """
    Compute internal coherence of text.

    Measures how semantically related different parts of the text are.
    """
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    if len(sentences) < 2:
        return 1.0

    # Get embeddings for all sentences
    embeddings = model.encode(sentences, convert_to_tensor=True)

    # Compute pairwise similarities
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = torch.nn.functional.cosine_similarity(
            embeddings[i].unsqueeze(0), embeddings[i + 1].unsqueeze(0)
        ).item()
        similarities.append(sim)

    # Average similarity (normalized to 0-1)
    avg_similarity = np.mean(similarities)
    coherence = (avg_similarity + 1) / 2

    return max(0.0, min(1.0, coherence))


def compute_all_metrics(
    prompt: str, reasoning: str, philosopher_name: str = "unknown"
) -> Dict[str, any]:
    """
    Compute all tensor metrics for a philosopher's reasoning.

    Args:
        prompt: The input prompt
        reasoning: The philosopher's reasoning text
        philosopher_name: Name of the philosopher

    Returns:
        Dictionary with all metrics
    """
    # Compute individual metrics
    fp_tensor = FreedomPressureTensor.compute(prompt, reasoning, philosopher_name)
    semantic_profile = SemanticProfile.compute(prompt, reasoning)
    blocked_tensor = BlockedTensor.compute(fp_tensor, semantic_profile)

    return {
        "freedom_pressure": fp_tensor.to_dict(),
        "semantic_profile": semantic_profile.to_dict(),
        "blocked_tensor": blocked_tensor.to_dict(),
        # Legacy compatibility
        "freedom_pressure_value": fp_tensor.overall,
        "semantic_delta": 1.0 - semantic_profile.prompt_similarity,
        "blocked_tensor_value": blocked_tensor.overall,
    }
