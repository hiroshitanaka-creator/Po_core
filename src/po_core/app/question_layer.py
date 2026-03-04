# SPDX-License-Identifier: AGPL-3.0-or-later
"""Question layer v1.

FR-Q-001: when unknowns exist, emit structured follow-up questions.
FR-Q-002: when information is sufficient (no unknowns), emit an empty list.

REQ-QST-001: questions は features（unknowns_count / unknowns_items /
    days_to_deadline / stakeholders_count）を用いた決定論ルールで優先順位付けし、
    最大5件を返すこと。deadline が近い場合は「期限の柔軟性」「暫定対応の許容範囲」
    を上位に出すこと。
"""

from __future__ import annotations

import datetime
from typing import Any

_MAX_QUESTIONS = 5
_DEADLINE_URGENT_DAYS = 14  # <= 14 days is considered urgent


def _days_to_deadline(deadline_raw: Any, now: str | None = None) -> int | None:
    """Return integer days to deadline, or None if unparseable."""
    if not deadline_raw:
        return None
    deadline_str = str(deadline_raw).strip()
    if not deadline_str:
        return None
    try:
        # Support YYYY-MM-DD and ISO 8601 with trailing Z
        deadline_str_clean = deadline_str.replace("Z", "+00:00")
        if "T" in deadline_str_clean:
            deadline_date = datetime.datetime.fromisoformat(deadline_str_clean).date()
        else:
            deadline_date = datetime.date.fromisoformat(deadline_str_clean[:10])
    except ValueError:
        return None

    if now:
        try:
            now_clean = now.replace("Z", "+00:00")
            if "T" in now_clean:
                now_date = datetime.datetime.fromisoformat(now_clean).date()
            else:
                now_date = datetime.date.fromisoformat(now_clean[:10])
        except ValueError:
            now_date = datetime.date.today()
    else:
        now_date = datetime.date.today()

    return (deadline_date - now_date).days


def _is_deadline_urgent(case: dict[str, Any], now: str | None = None) -> bool:
    """Return True when deadline is within _DEADLINE_URGENT_DAYS days."""
    days = _days_to_deadline(case.get("deadline"), now)
    if days is None:
        return False
    return days <= _DEADLINE_URGENT_DAYS


def build_questions(
    unknowns: list[str],
    case: dict[str, Any] | None = None,
    now: str | None = None,
) -> list[dict[str, Any]]:
    """Build deterministic question items from unknowns with deadline priority.

    REQ-QST-001: When deadline is urgent (≤14 days), prepend questions about
    deadline flexibility and interim actions at priority 1 and 2.

    Args:
        unknowns: List of unresolved items extracted from the input case.
        case:     Full case dict (used for deadline detection).
        now:      ISO-8601 UTC string for relative deadline calculation.

    Returns:
        Schema-compatible question objects (max 5). Empty list when unknowns empty
        and no deadline urgency.
    """
    case = case or {}
    normalized = [str(item).strip() for item in unknowns if str(item).strip()]
    urgent = _is_deadline_urgent(case, now)
    deadline_raw = case.get("deadline")

    questions: list[dict[str, Any]] = []

    # REQ-QST-001: Deadline urgency → prepend deadline-specific questions
    if urgent and deadline_raw:
        # Use absolute deadline date for determinism (not wall-clock-relative "X日以内")
        deadline_label = str(deadline_raw).strip()[:10]
        questions.append(
            {
                "question_id": "q_d01",
                "question": (
                    f"期限（{deadline_label}）の柔軟性はありますか？"
                    "期限を延長・分割できる余地があれば、リスクを大幅に低減できます。"
                ),
                "priority": 1,
                "why_needed": "期限の硬直性が判断の幅を大きく左右するため",
                "assumption_if_unanswered": "期限は固定と仮定して保守的に対応します",
                "optional": False,
            }
        )
        questions.append(
            {
                "question_id": "q_d02",
                "question": (
                    "期限までに暫定対応（部分的・リスクを限定した行動）は許容されますか？"
                    "完全な解決を待つより、段階的実施で対応できる可能性があります。"
                ),
                "priority": 2,
                "why_needed": "暫定対応の余地があるかで選択肢の質が変わるため",
                "assumption_if_unanswered": "暫定対応は許容されないと仮定します",
                "optional": False,
            }
        )

    # Unknown-based questions
    if not normalized:
        return questions[:_MAX_QUESTIONS]

    remaining_slots = _MAX_QUESTIONS - len(questions)
    for i, item in enumerate(normalized[:remaining_slots], start=1):
        # Shift priority when deadline questions already occupy slots 1-2
        base_priority = min(i + len(questions), 5)
        questions.append(
            {
                "question_id": f"q_{i:03d}",
                "question": f"不明点『{item}』について、判断に使える事実は何ですか？",
                "priority": base_priority,
                "why_needed": f"『{item}』が選択肢評価に影響するため",
                "assumption_if_unanswered": "保守的な前提を置いて意思決定します",
                "optional": base_priority > 2,
            }
        )

    return questions[:_MAX_QUESTIONS]
