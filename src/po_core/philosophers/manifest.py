"""
Philosopher Manifest
====================

39人の哲学者の"名簿"。拡張の唯一の入口。

risk_level:
- 0: 安全寄り（コンプラ、確認、拒否、整理）
- 1: 標準
- 2: 攻め（発散、挑発、探索）
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


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
    """

    philosopher_id: str
    module: str
    symbol: str
    risk_level: int = 1
    weight: float = 1.0
    enabled: bool = True


# 39人の哲学者名簿
SPECS: List[PhilosopherSpec] = [
    # ── risk_level=0: 安全寄り（倫理重視、確認、整理）──────────────
    PhilosopherSpec("dummy", "po_core.philosophers.dummy", "DummyPhilosopher", risk_level=0, weight=2.0),
    PhilosopherSpec("kant", "po_core.philosophers.kant", "Kant", risk_level=0, weight=1.5),
    PhilosopherSpec("confucius", "po_core.philosophers.confucius", "Confucius", risk_level=0, weight=1.5),
    PhilosopherSpec("marcus_aurelius", "po_core.philosophers.marcus_aurelius", "MarcusAurelius", risk_level=0, weight=1.4),
    PhilosopherSpec("jonas", "po_core.philosophers.jonas", "Jonas", risk_level=0, weight=1.3),
    PhilosopherSpec("weil", "po_core.philosophers.weil", "Weil", risk_level=0, weight=1.2),
    PhilosopherSpec("levinas", "po_core.philosophers.levinas", "Levinas", risk_level=0, weight=1.1),
    PhilosopherSpec("watsuji", "po_core.philosophers.watsuji", "Watsuji", risk_level=0, weight=1.0),
    PhilosopherSpec("dogen", "po_core.philosophers.dogen", "Dogen", risk_level=0, weight=1.0),
    PhilosopherSpec("wabi_sabi", "po_core.philosophers.wabi_sabi", "WabiSabi", risk_level=0, weight=1.0),

    # ── risk_level=1: 標準（バランス型）──────────────────────────
    PhilosopherSpec("aristotle", "po_core.philosophers.aristotle", "Aristotle", risk_level=1, weight=1.5),
    PhilosopherSpec("plato", "po_core.philosophers.plato", "Plato", risk_level=1, weight=1.4),
    PhilosopherSpec("descartes", "po_core.philosophers.descartes", "Descartes", risk_level=1, weight=1.3),
    PhilosopherSpec("spinoza", "po_core.philosophers.spinoza", "Spinoza", risk_level=1, weight=1.2),
    PhilosopherSpec("hegel", "po_core.philosophers.hegel", "Hegel", risk_level=1, weight=1.2),
    PhilosopherSpec("husserl", "po_core.philosophers.husserl", "Husserl", risk_level=1, weight=1.1),
    PhilosopherSpec("merleau_ponty", "po_core.philosophers.merleau_ponty", "MerleauPonty", risk_level=1, weight=1.1),
    PhilosopherSpec("wittgenstein", "po_core.philosophers.wittgenstein", "Wittgenstein", risk_level=1, weight=1.1),
    PhilosopherSpec("peirce", "po_core.philosophers.peirce", "Peirce", risk_level=1, weight=1.0),
    PhilosopherSpec("dewey", "po_core.philosophers.dewey", "Dewey", risk_level=1, weight=1.0),
    PhilosopherSpec("arendt", "po_core.philosophers.arendt", "Arendt", risk_level=1, weight=1.0),
    PhilosopherSpec("beauvoir", "po_core.philosophers.beauvoir", "Beauvoir", risk_level=1, weight=1.0),
    PhilosopherSpec("nishida", "po_core.philosophers.nishida", "Nishida", risk_level=1, weight=1.0),
    PhilosopherSpec("laozi", "po_core.philosophers.laozi", "Laozi", risk_level=1, weight=1.0),
    PhilosopherSpec("zhuangzi", "po_core.philosophers.zhuangzi", "Zhuangzi", risk_level=1, weight=1.0),
    PhilosopherSpec("nagarjuna", "po_core.philosophers.nagarjuna", "Nagarjuna", risk_level=1, weight=1.0),
    PhilosopherSpec("parmenides", "po_core.philosophers.parmenides", "Parmenides", risk_level=1, weight=0.9),
    PhilosopherSpec("epicurus", "po_core.philosophers.epicurus", "Epicurus", risk_level=1, weight=0.9),
    PhilosopherSpec("jung", "po_core.philosophers.jung", "Jung", risk_level=1, weight=0.9),

    # ── risk_level=2: 攻め（発散、挑発、探索、批判）───────────────
    PhilosopherSpec("nietzsche", "po_core.philosophers.nietzsche", "Nietzsche", risk_level=2, weight=1.2),
    PhilosopherSpec("heidegger", "po_core.philosophers.heidegger", "Heidegger", risk_level=2, weight=1.1),
    PhilosopherSpec("sartre", "po_core.philosophers.sartre", "Sartre", risk_level=2, weight=1.1),
    PhilosopherSpec("kierkegaard", "po_core.philosophers.kierkegaard", "Kierkegaard", risk_level=2, weight=1.0),
    PhilosopherSpec("schopenhauer", "po_core.philosophers.schopenhauer", "Schopenhauer", risk_level=2, weight=1.0),
    PhilosopherSpec("foucault", "po_core.philosophers.foucault", "Foucault", risk_level=2, weight=1.0),
    PhilosopherSpec("derrida", "po_core.philosophers.derrida", "Derrida", risk_level=2, weight=0.9),
    PhilosopherSpec("deleuze", "po_core.philosophers.deleuze", "Deleuze", risk_level=2, weight=0.9),
    PhilosopherSpec("lacan", "po_core.philosophers.lacan", "Lacan", risk_level=2, weight=0.8),
    PhilosopherSpec("badiou", "po_core.philosophers.badiou", "Badiou", risk_level=2, weight=0.8),
    PhilosopherSpec("butler", "po_core.philosophers.butler", "Butler", risk_level=2, weight=0.8),
]


def get_enabled_specs() -> List[PhilosopherSpec]:
    """Get all enabled philosopher specs."""
    return [s for s in SPECS if s.enabled]


__all__ = ["PhilosopherSpec", "SPECS", "get_enabled_specs"]
