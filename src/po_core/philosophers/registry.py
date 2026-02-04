"""
Philosopher Registry
====================

SafetyModeに応じて哲学者を選抜・ロードする。
1→5→39の段階解放を実現。

DEPENDENCY RULES:
- import は domain + importlib だけ
- philosophers自身は safety/runtime を見ない
- registry は "選抜とロード" のみ（判断はしない）
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Dict, List, Sequence

from po_core.domain.safety_mode import SafetyMode
from po_core.philosophers.base import PhilosopherProtocol
from po_core.philosophers.manifest import PhilosopherSpec, SPECS


@dataclass(frozen=True)
class Selection:
    """選抜結果。"""

    mode: SafetyMode
    selected_ids: List[str]


class PhilosopherRegistry:
    """
    哲学者レジストリ。

    SafetyModeに応じて哲学者を選抜し、動的にロードする。
    - CRITICAL: 1人（最も安全な哲学者のみ）
    - WARN: 5人（安全〜標準の哲学者）
    - NORMAL: 39人（全員）
    """

    def __init__(
        self,
        specs: Sequence[PhilosopherSpec] = SPECS,
        *,
        max_normal: int = 39,
        max_warn: int = 5,
        max_critical: int = 1,
        cache_instances: bool = True,
    ):
        self._specs = list(specs)
        self._max = {
            SafetyMode.NORMAL: max_normal,
            SafetyMode.WARN: max_warn,
            SafetyMode.CRITICAL: max_critical,
            SafetyMode.UNKNOWN: max_warn,  # UNKNOWNはWARN扱い（締める）
        }
        self._cache = cache_instances
        self._instances: Dict[str, PhilosopherProtocol] = {}

    def select(self, mode: SafetyMode) -> Selection:
        """
        SafetyModeに応じて哲学者を選抜。

        Args:
            mode: SafetyMode

        Returns:
            Selection with selected_ids
        """
        limit = self._max.get(mode, self._max[SafetyMode.WARN])

        # modeごとのrisk上限
        if mode == SafetyMode.CRITICAL:
            max_risk = 0
        elif mode in (SafetyMode.WARN, SafetyMode.UNKNOWN):
            max_risk = 1
        else:
            max_risk = 2

        candidates = [
            s for s in self._specs
            if s.enabled and s.risk_level <= max_risk
        ]

        # 安全側→重み→id の順で安定選抜
        candidates.sort(key=lambda s: (s.risk_level, -s.weight, s.philosopher_id))

        selected = candidates[: max(0, limit)]
        return Selection(mode=mode, selected_ids=[s.philosopher_id for s in selected])

    def load(self, selected_ids: Sequence[str]) -> List[PhilosopherProtocol]:
        """
        選抜された哲学者をロード。

        Args:
            selected_ids: 選抜されたphilosopher_idのリスト

        Returns:
            ロードされた哲学者インスタンスのリスト
        """
        by_id = {s.philosopher_id: s for s in self._specs}
        out: List[PhilosopherProtocol] = []

        for pid in selected_ids:
            spec = by_id.get(pid)
            if spec is None:
                continue

            if self._cache and pid in self._instances:
                out.append(self._instances[pid])
                continue

            mod = importlib.import_module(spec.module)
            obj = getattr(mod, spec.symbol)

            # objがクラスでも関数でも callable なら呼べる
            ph = obj() if callable(obj) else obj  # type: ignore[misc]
            out.append(ph)

            if self._cache:
                self._instances[pid] = ph

        return out

    def select_and_load(self, mode: SafetyMode) -> List[PhilosopherProtocol]:
        """選抜とロードを一度に行う。"""
        sel = self.select(mode)
        return self.load(sel.selected_ids)


# Backward compat: 固定リストを返す（wiring.pyが依存）
def build_philosophers() -> List[PhilosopherProtocol]:
    """
    Build the default list of philosophers.

    For backward compatibility, returns the NORMAL mode selection.
    New code should use PhilosopherRegistry directly.
    """
    registry = PhilosopherRegistry(cache_instances=False)
    return registry.select_and_load(SafetyMode.NORMAL)


__all__ = [
    "PhilosopherRegistry",
    "Selection",
    "build_philosophers",
]
