# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""Two-Track Plan builder v1.

REQ-PLAN-001: unknowns があり期限圧力が閾値以上のとき、
    action_plan に Track A（可逆・低リスク）と Track B（unknowns解消）を
    決定論順序で出力する。

推奨裁定（status / recommended_option_id / arbitration_code）には介入しない。
"""

from __future__ import annotations

import datetime
from typing import Any

_TIME_PRESSURE_DAYS = 30  # <= 30 days = time pressure threshold


def _days_to_deadline(deadline_raw: Any, now: str | None = None) -> int | None:
    """Return integer days to deadline, or None if unparseable."""
    if not deadline_raw:
        return None
    deadline_str = str(deadline_raw).strip()
    if not deadline_str:
        return None
    try:
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


def needs_two_track_plan(case: dict[str, Any], now: str | None = None) -> bool:
    """Return True when Two-Track Plan should be generated (REQ-PLAN-001).

    Condition: unknowns exist AND deadline pressure is high (≤30 days).
    """
    unknowns = case.get("unknowns", [])
    if not unknowns:
        return False
    days = _days_to_deadline(case.get("deadline"), now)
    if days is None:
        return False
    return days <= _TIME_PRESSURE_DAYS


def build_two_track_plan(
    case: dict[str, Any],
    now: str | None = None,
) -> list[dict[str, Any]]:
    """Build a deterministic Two-Track action plan (REQ-PLAN-001).

    Track A: Reversible, low-risk actions executable now regardless of unknowns.
    Track B: Steps to resolve critical unknowns before committing further.

    Args:
        case: Validated case dict.
        now:  ISO-8601 UTC string for relative deadline calculation.

    Returns:
        List of action plan steps (max 5), interleaving Track A and B.
    """
    unknowns: list[str] = list(case.get("unknowns", []) or [])
    constraints: list[str] = list(case.get("constraints", []) or [])
    deadline = case.get("deadline")
    # Use absolute deadline date for determinism (not wall-clock-relative "X日以内")
    days_str = f"期限（{str(deadline).strip()[:10]}）" if deadline else "期限内"

    # Track A: reversible/low-risk immediate actions
    track_a_steps: list[dict[str, Any]] = []

    constraint_hint = constraints[0] if constraints else "現状の制約"
    track_a_steps.append(
        {
            "step": (
                f"【Track A-1】現状の記録と影響範囲の可視化（{days_str}で実施）"
                f" — {constraint_hint}の範囲内でできる可逆的な準備を開始する"
            ),
            "rationale": "不確実性が高い状況でも今すぐ取れる低リスク行動から着手する",
        }
    )
    track_a_steps.append(
        {
            "step": (
                "【Track A-2】関係者への状況共有と暫定合意の取得"
                " — 最終判断を保留しながら関係者の理解を得る"
            ),
            "rationale": "後戻りできる段階で関係者を巻き込み、合意形成コストを下げる",
        }
    )

    # Track B: unknown resolution steps
    track_b_steps: list[dict[str, Any]] = []
    for i, unknown in enumerate(unknowns[:2], start=1):
        track_b_steps.append(
            {
                "step": (
                    f"【Track B-{i}】不明点『{unknown}』の解消"
                    f" — 情報収集・専門家確認・テスト等で判断可能な状態にする"
                ),
                "rationale": f"『{unknown}』が未解決なまま全面実施するとリスクが高まるため",
            }
        )

    # Merge: A1, B1, A2, B2, ... (max 5 total)
    plan: list[dict[str, Any]] = []
    a_iter = iter(track_a_steps)
    b_iter = iter(track_b_steps)
    for _ in range(5):
        step = next(a_iter, None) or next(b_iter, None)
        if step is None:
            break
        plan.append(step)
        step = next(b_iter, None) or next(a_iter, None)
        if step is None:
            break
        plan.append(step)
        if len(plan) >= 5:
            break

    return plan[:5]
