# src/po_core/philosophers/tags.py
"""
Philosopher Role Tags
=====================

タグを定数化してブレを殺す。
哲学者の"兵科"を定義する。
"""

from __future__ import annotations

# 規範・安全・拒否
TAG_COMPLIANCE = "compliance"

# 追加質問・要件定義
TAG_CLARIFY = "clarify"

# 反証・穴探し
TAG_CRITIC = "critic"

# 計画・分解
TAG_PLANNER = "planner"

# 発散・比喩
TAG_CREATIVE = "creative"

# 攻撃者視点（危険寄り）
TAG_REDTEAM = "redteam"

# 汎用
TAG_GENERAL = "general"

# AI横断合成（AI企業哲学者スロット 40-43 専用）
# 複数哲学的伝統を横断し、AI安全・エピステミック謙虚さ視点で統合する
TAG_AI_SYNTHESIS = "ai_synthesis"


__all__ = [
    "TAG_COMPLIANCE",
    "TAG_CLARIFY",
    "TAG_CRITIC",
    "TAG_PLANNER",
    "TAG_CREATIVE",
    "TAG_REDTEAM",
    "TAG_GENERAL",
    "TAG_AI_SYNTHESIS",
]
