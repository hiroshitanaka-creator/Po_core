# SPDX-License-Identifier: AGPL-3.0-or-later
"""Question layer v1.

FR-Q-001: when unknowns exist, emit structured follow-up questions.
FR-Q-002: when information is sufficient (no unknowns), emit an empty list.
"""

from __future__ import annotations

from typing import Any

_MAX_QUESTIONS = 5


def build_questions(unknowns: list[str]) -> list[dict[str, Any]]:
    """Build deterministic question items from unknowns.

    Args:
        unknowns: List of unresolved items extracted from the input case.

    Returns:
        Schema-compatible question objects. Empty list when unknowns is empty.
    """
    normalized = [str(item).strip() for item in unknowns if str(item).strip()]
    if not normalized:
        return []

    questions: list[dict[str, Any]] = []
    for i, item in enumerate(normalized[:_MAX_QUESTIONS], start=1):
        questions.append(
            {
                "question_id": f"q_{i:03d}",
                "question": f"不明点『{item}』について、判断に使える事実は何ですか？",
                "priority": min(i, 5),
                "why_needed": f"『{item}』が選択肢評価に影響するため",
                "assumption_if_unanswered": "保守的な前提を置いて意思決定します",
                "optional": i > 2,
            }
        )

    return questions
