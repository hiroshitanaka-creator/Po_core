"""
Philosopher Manifest (兵科表)
=============================

42人の哲学者と、非公開の sentinel helper `dummy` を扱う内部兵科表。
tags と cost で役割とコストを明示。

risk_level:
- 0: 安全寄り（コンプラ、確認、拒否、整理）
- 1: 標準
- 2: 攻め（発散、挑発、探索）

tags:
- compliance: 規範・安全・拒否
- clarify: 追加質問・要件定義
- critic: 反証・穴探し
- planner: 計画・分解
- creative: 発散・比喩
- redteam: 攻撃者視点（危険寄り）
- general: 汎用

cost:
- 1: 軽い
- 3: 重い
- 5: 激重
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from po_core.deliberation.roles import PHILOSOPHER_ROLE_MAP, Role
from po_core.philosophers.tags import (
    TAG_CLARIFY,
    TAG_COMPLIANCE,
    TAG_CREATIVE,
    TAG_CRITIC,
    TAG_GENERAL,
    TAG_PLANNER,
    TAG_REDTEAM,
)


@dataclass(frozen=True)
class PhilosopherSpec:
    """
    哲学者の仕様。

    Attributes:
        philosopher_id: 一意の識別子
        module: モジュールパス (e.g., "po_core.philosophers.socrates")
        symbol: クラス名 or ファクトリ関数名
        risk_level: 0=safe, 1=normal, 2=risky
        weight: 同tier内での優先度（大きいほど優先）
        enabled: 有効フラグ
        tags: 兵科タグ（役割）
        cost: 推論/計算の重さ (1=軽い, 3=重い, 5=激重)
    """

    philosopher_id: str
    module: str
    symbol: str
    risk_level: int = 1
    weight: float = 1.0
    enabled: bool = True
    tags: Tuple[str, ...] = ()
    cost: int = 1


# 内部 runtime 兵科表（42 philosophers + non-philosopher helper `dummy`）
SPECS: List[PhilosopherSpec] = [
    # ══════════════════════════════════════════════════════════════════════
    # risk_level=0: 安全寄り（倫理重視、確認、整理）
    # ══════════════════════════════════════════════════════════════════════
    PhilosopherSpec(
        "dummy",
        "po_core.philosophers.dummy",
        "DummyPhilosopher",
        risk_level=0,
        weight=1.0,
        enabled=True,
        tags=(TAG_COMPLIANCE, TAG_CLARIFY),
        cost=1,
    ),
    PhilosopherSpec(
        "kant",
        "po_core.philosophers.kant",
        "Kant",
        risk_level=0,
        weight=1.5,
        tags=(TAG_COMPLIANCE, TAG_CRITIC),
        cost=2,
    ),
    PhilosopherSpec(
        "confucius",
        "po_core.philosophers.confucius",
        "Confucius",
        risk_level=0,
        weight=1.5,
        tags=(TAG_COMPLIANCE, TAG_CLARIFY),
        cost=1,
    ),
    PhilosopherSpec(
        "marcus_aurelius",
        "po_core.philosophers.marcus_aurelius",
        "MarcusAurelius",
        risk_level=0,
        weight=1.4,
        tags=(TAG_COMPLIANCE, TAG_PLANNER),
        cost=1,
    ),
    PhilosopherSpec(
        "jonas",
        "po_core.philosophers.jonas",
        "Jonas",
        risk_level=0,
        weight=1.3,
        tags=(TAG_COMPLIANCE, TAG_CRITIC),
        cost=2,
    ),
    PhilosopherSpec(
        "weil",
        "po_core.philosophers.weil",
        "Weil",
        risk_level=0,
        weight=1.2,
        tags=(TAG_COMPLIANCE, TAG_CLARIFY),
        cost=1,
    ),
    PhilosopherSpec(
        "levinas",
        "po_core.philosophers.levinas",
        "Levinas",
        risk_level=0,
        weight=1.1,
        tags=(TAG_COMPLIANCE, TAG_CLARIFY),
        cost=2,
    ),
    PhilosopherSpec(
        "watsuji",
        "po_core.philosophers.watsuji",
        "Watsuji",
        risk_level=0,
        weight=1.0,
        tags=(TAG_COMPLIANCE, TAG_GENERAL),
        cost=1,
    ),
    PhilosopherSpec(
        "dogen",
        "po_core.philosophers.dogen",
        "Dogen",
        risk_level=0,
        weight=1.0,
        tags=(TAG_CLARIFY, TAG_GENERAL),
        cost=1,
    ),
    PhilosopherSpec(
        "wabi_sabi",
        "po_core.philosophers.wabi_sabi",
        "WabiSabi",
        risk_level=0,
        weight=1.0,
        tags=(TAG_CLARIFY, TAG_GENERAL),
        cost=1,
    ),
    # ══════════════════════════════════════════════════════════════════════
    # risk_level=1: 標準（バランス型）
    # ══════════════════════════════════════════════════════════════════════
    PhilosopherSpec(
        "aristotle",
        "po_core.philosophers.aristotle",
        "Aristotle",
        risk_level=1,
        weight=1.5,
        tags=(TAG_PLANNER, TAG_CRITIC),
        cost=2,
    ),
    PhilosopherSpec(
        "plato",
        "po_core.philosophers.plato",
        "Plato",
        risk_level=1,
        weight=1.4,
        tags=(TAG_PLANNER, TAG_GENERAL),
        cost=2,
    ),
    PhilosopherSpec(
        "descartes",
        "po_core.philosophers.descartes",
        "Descartes",
        risk_level=1,
        weight=1.3,
        tags=(TAG_CRITIC, TAG_PLANNER),
        cost=2,
    ),
    PhilosopherSpec(
        "spinoza",
        "po_core.philosophers.spinoza",
        "Spinoza",
        risk_level=1,
        weight=1.2,
        tags=(TAG_PLANNER, TAG_GENERAL),
        cost=2,
    ),
    PhilosopherSpec(
        "hegel",
        "po_core.philosophers.hegel",
        "Hegel",
        risk_level=1,
        weight=1.2,
        tags=(TAG_CRITIC, TAG_PLANNER),
        cost=3,
    ),
    PhilosopherSpec(
        "husserl",
        "po_core.philosophers.husserl",
        "Husserl",
        risk_level=1,
        weight=1.1,
        tags=(TAG_CLARIFY, TAG_CRITIC),
        cost=2,
    ),
    PhilosopherSpec(
        "merleau_ponty",
        "po_core.philosophers.merleau_ponty",
        "MerleauPonty",
        risk_level=1,
        weight=1.1,
        tags=(TAG_CLARIFY, TAG_GENERAL),
        cost=2,
    ),
    PhilosopherSpec(
        "wittgenstein",
        "po_core.philosophers.wittgenstein",
        "Wittgenstein",
        risk_level=1,
        weight=1.1,
        tags=(TAG_CRITIC, TAG_CLARIFY),
        cost=2,
    ),
    PhilosopherSpec(
        "peirce",
        "po_core.philosophers.peirce",
        "Peirce",
        risk_level=1,
        weight=1.0,
        tags=(TAG_PLANNER, TAG_CRITIC),
        cost=2,
    ),
    PhilosopherSpec(
        "dewey",
        "po_core.philosophers.dewey",
        "Dewey",
        risk_level=1,
        weight=1.0,
        tags=(TAG_PLANNER, TAG_GENERAL),
        cost=1,
    ),
    PhilosopherSpec(
        "arendt",
        "po_core.philosophers.arendt",
        "Arendt",
        risk_level=1,
        weight=1.0,
        tags=(TAG_CRITIC, TAG_COMPLIANCE),
        cost=2,
    ),
    PhilosopherSpec(
        "beauvoir",
        "po_core.philosophers.beauvoir",
        "Beauvoir",
        risk_level=1,
        weight=1.0,
        tags=(TAG_CRITIC, TAG_GENERAL),
        cost=2,
    ),
    PhilosopherSpec(
        "nishida",
        "po_core.philosophers.nishida",
        "Nishida",
        risk_level=1,
        weight=1.0,
        tags=(TAG_CLARIFY, TAG_GENERAL),
        cost=2,
    ),
    PhilosopherSpec(
        "laozi",
        "po_core.philosophers.laozi",
        "Laozi",
        risk_level=1,
        weight=1.0,
        tags=(TAG_CLARIFY, TAG_GENERAL),
        cost=1,
    ),
    PhilosopherSpec(
        "zhuangzi",
        "po_core.philosophers.zhuangzi",
        "Zhuangzi",
        risk_level=1,
        weight=1.0,
        tags=(TAG_CREATIVE, TAG_CLARIFY),
        cost=1,
    ),
    PhilosopherSpec(
        "nagarjuna",
        "po_core.philosophers.nagarjuna",
        "Nagarjuna",
        risk_level=1,
        weight=1.0,
        tags=(TAG_CRITIC, TAG_CLARIFY),
        cost=2,
    ),
    PhilosopherSpec(
        "parmenides",
        "po_core.philosophers.parmenides",
        "Parmenides",
        risk_level=1,
        weight=0.9,
        tags=(TAG_CRITIC, TAG_GENERAL),
        cost=1,
    ),
    PhilosopherSpec(
        "epicurus",
        "po_core.philosophers.epicurus",
        "Epicurus",
        risk_level=1,
        weight=0.9,
        tags=(TAG_PLANNER, TAG_GENERAL),
        cost=1,
    ),
    PhilosopherSpec(
        "jung",
        "po_core.philosophers.jung",
        "Jung",
        risk_level=1,
        weight=0.9,
        tags=(TAG_CREATIVE, TAG_CLARIFY),
        cost=2,
    ),
    # ══════════════════════════════════════════════════════════════════════
    # risk_level=2: 攻め（発散、挑発、探索、批判）
    # ══════════════════════════════════════════════════════════════════════
    PhilosopherSpec(
        "nietzsche",
        "po_core.philosophers.nietzsche",
        "Nietzsche",
        risk_level=2,
        weight=1.2,
        tags=(TAG_REDTEAM, TAG_CRITIC),
        cost=2,
    ),
    PhilosopherSpec(
        "heidegger",
        "po_core.philosophers.heidegger",
        "Heidegger",
        risk_level=2,
        weight=1.1,
        tags=(TAG_CRITIC, TAG_CREATIVE),
        cost=3,
    ),
    PhilosopherSpec(
        "sartre",
        "po_core.philosophers.sartre",
        "Sartre",
        risk_level=2,
        weight=1.1,
        tags=(TAG_REDTEAM, TAG_CREATIVE),
        cost=2,
    ),
    PhilosopherSpec(
        "kierkegaard",
        "po_core.philosophers.kierkegaard",
        "Kierkegaard",
        risk_level=2,
        weight=1.0,
        tags=(TAG_CRITIC, TAG_CREATIVE),
        cost=2,
    ),
    PhilosopherSpec(
        "schopenhauer",
        "po_core.philosophers.schopenhauer",
        "Schopenhauer",
        risk_level=2,
        weight=1.0,
        tags=(TAG_CRITIC, TAG_REDTEAM),
        cost=2,
    ),
    PhilosopherSpec(
        "foucault",
        "po_core.philosophers.foucault",
        "Foucault",
        risk_level=2,
        weight=1.0,
        tags=(TAG_REDTEAM, TAG_CRITIC),
        cost=3,
    ),
    PhilosopherSpec(
        "derrida",
        "po_core.philosophers.derrida",
        "Derrida",
        risk_level=2,
        weight=0.9,
        tags=(TAG_CREATIVE, TAG_CRITIC),
        cost=3,
    ),
    PhilosopherSpec(
        "deleuze",
        "po_core.philosophers.deleuze",
        "Deleuze",
        risk_level=2,
        weight=0.9,
        tags=(TAG_CREATIVE, TAG_REDTEAM),
        cost=3,
    ),
    PhilosopherSpec(
        "lacan",
        "po_core.philosophers.lacan",
        "Lacan",
        risk_level=2,
        weight=0.8,
        tags=(TAG_CREATIVE, TAG_CRITIC),
        cost=3,
    ),
    PhilosopherSpec(
        "badiou",
        "po_core.philosophers.badiou",
        "Badiou",
        risk_level=2,
        weight=0.8,
        tags=(TAG_REDTEAM, TAG_CREATIVE),
        cost=3,
    ),
    PhilosopherSpec(
        "butler",
        "po_core.philosophers.butler",
        "Butler",
        risk_level=2,
        weight=0.8,
        tags=(TAG_CRITIC, TAG_CREATIVE),
        cost=2,
    ),
    # ══════════════════════════════════════════════════════════════════════
    # アフリカ系哲学者スロット 40-41 / カナダ系哲学者スロット 42
    # ══════════════════════════════════════════════════════════════════════
    PhilosopherSpec(
        "appiah",
        "po_core.philosophers.appiah",
        "Appiah",
        risk_level=1,
        weight=1.2,
        enabled=True,  # Slot 40 — Kwame Anthony Appiah (Ghana/US)
        tags=(TAG_GENERAL, TAG_CLARIFY, TAG_CRITIC),
        cost=2,
    ),
    PhilosopherSpec(
        "fanon",
        "po_core.philosophers.fanon",
        "Fanon",
        risk_level=2,
        weight=1.1,
        enabled=True,  # Slot 41 — Frantz Fanon (Martinique/Algeria)
        tags=(TAG_REDTEAM, TAG_CRITIC, TAG_CREATIVE),
        cost=2,
    ),
    PhilosopherSpec(
        "charles_taylor",
        "po_core.philosophers.charles_taylor",
        "CharlesTaylor",
        risk_level=1,
        weight=1.2,
        enabled=True,  # Slot 42 — Charles Taylor (Canada)
        tags=(TAG_PLANNER, TAG_CLARIFY, TAG_COMPLIANCE),
        cost=2,
    ),
]


DUMMY_PHILOSOPHER_ID = "dummy"
PUBLIC_PHILOSOPHER_COUNT = 42


def get_enabled_specs() -> List[PhilosopherSpec]:
    """Return all enabled internal runtime specs, including helper slots."""
    return [s for s in SPECS if s.enabled]


def get_public_philosopher_specs() -> List[PhilosopherSpec]:
    """Return only the canonical 42 philosopher specs for public surfaces."""
    return [
        s for s in SPECS if s.enabled and s.philosopher_id != DUMMY_PHILOSOPHER_ID
    ]


def get_role_for_philosopher(philosopher_id: str) -> Role | None:
    """Resolve philosopher_id to functional role."""
    return PHILOSOPHER_ROLE_MAP.get(philosopher_id)


__all__ = [
    "DUMMY_PHILOSOPHER_ID",
    "PUBLIC_PHILOSOPHER_COUNT",
    "PhilosopherSpec",
    "SPECS",
    "get_enabled_specs",
    "get_public_philosopher_specs",
    "get_role_for_philosopher",
]

