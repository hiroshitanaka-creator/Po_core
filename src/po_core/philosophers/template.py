"""Template philosopher plugin for external contributors.

Copy this file to bootstrap a new philosopher module.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class TemplatePhilosopher(Philosopher):
    """Minimal, deterministic philosopher implementation template."""

    def __init__(self) -> None:
        super().__init__(
            name="Template Philosopher",
            description="Reference implementation for Po_core philosopher plugins.",
        )
        self.tradition = "Template"
        self.key_concepts = ["contract", "determinism", "traceability"]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Return deterministic reasoning with required contract keys."""
        normalized_prompt = " ".join(prompt.strip().split())

        return {
            "reasoning": (
                "Clarify the decision objective, enumerate assumptions, "
                f"and test one reversible action first. Prompt={normalized_prompt}"
            ),
            "perspective": "Plugin template / contract-first reasoning",
            "metadata": {
                "philosopher": self.name,
                "source": "template",
                "uses_context": bool(context),
            },
            "rationale": "Contract-first structure improves auditability.",
            "confidence": 0.6,
            "citations": ["Po_core philosopher plugin spec"],
        }


__all__ = ["TemplatePhilosopher"]
