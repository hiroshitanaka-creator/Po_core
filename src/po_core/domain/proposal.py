"""
Proposal - philosopher/aggregatorの成果物。Gateが裁く対象。

This is what philosophers OUTPUT after reasoning.
Proposals can be aggregated, compared, and passed through safety gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping


@dataclass(frozen=True)
class Proposal:
    """
    philosopher/aggregatorの成果物。Gateが裁く対象。

    Attributes:
        proposal_id: Unique identifier for this proposal
        action_type: Type of action (e.g., "answer", "tool_call", "refuse", "ask_clarification")
        content: Execution/output content (final or intermediate)
        confidence: Confidence level in [0, 1]
        assumption_tags: Tags for accountability (assumptions)
        risk_tags: Tags for accountability (risks)
        extra: Additional structured data
    """

    proposal_id: str
    action_type: str  # 例: "answer", "tool_call", "refuse", "ask_clarification" など
    content: str  # 実行/出力内容（最終出力でも中間でもよい）
    confidence: float = 0.5

    # 説明責任のためのタグ（仮定/リスク/観測など）
    assumption_tags: List[str] = field(default_factory=list)
    risk_tags: List[str] = field(default_factory=list)

    # 任意構造（ただしGate/Traceが読むならdomain化を検討）
    extra: Mapping[str, Any] = field(default_factory=dict)

    def compact(self) -> Dict[str, Any]:
        """Return a compact representation for logging/serialization."""
        return {
            "proposal_id": self.proposal_id,
            "action_type": self.action_type,
            "content": self.content,
            "confidence": self.confidence,
            "assumption_tags": list(self.assumption_tags),
            "risk_tags": list(self.risk_tags),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for full serialization."""
        result = self.compact()
        result["extra"] = dict(self.extra)
        return result


__all__ = ["Proposal"]
