"""
Philosopher Registry (編成官)
==============================

SafetyModeに応じて哲学者を「編成」する。
単なる選抜ではなく、タグを満たす＋cost budgetで締める。

- 「誰を呼ぶか」が設計になった
- mode別の"編成表"で必須タグを満たす
- コスト予算で重い哲学者混入を防ぐ
- ロードは落とさず"エラー回収"
- battalion_plans で外部設定を優先可能

DEPENDENCY RULES:
- import は domain + importlib だけ
- philosophers自身は safety/runtime を見ない
- registry は "編成とロード" のみ（判断はしない）
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Mapping, Optional, Sequence, Tuple

from po_core.deliberation.roles import PHILOSOPHER_ROLE_MAP, Role
from po_core.domain.safety_mode import SafetyMode

if TYPE_CHECKING:
    from po_core.runtime.battalion_table import BattalionModePlan

from po_core.philosophers.base import PhilosopherProtocol
from po_core.philosophers.manifest import SPECS, PhilosopherSpec
from po_core.philosophers.tags import (
    TAG_CLARIFY,
    TAG_COMPLIANCE,
    TAG_CREATIVE,
    TAG_CRITIC,
    TAG_PLANNER,
    TAG_REDTEAM,
)


@dataclass(frozen=True)
class Selection:
    """選抜結果。"""

    mode: SafetyMode
    selected_ids: List[str]
    cost_total: int
    covered_tags: List[str]


@dataclass(frozen=True)
class LoadError:
    """ロードエラー。"""

    philosopher_id: str
    module: str
    symbol: str
    error: str


@dataclass(frozen=True)
class SelectionPlan:
    """編成表（mode別の選抜計画）。"""

    limit: int
    max_risk: int
    cost_budget: int
    require_tags: Tuple[str, ...]


class PhilosopherRegistry:
    """
    哲学者レジストリ（編成官）。

    SafetyModeに応じて哲学者を編成し、動的にロードする。
    - CRITICAL: 1人（最も安全な哲学者のみ）, コスト予算3
    - WARN: 5人（安全〜標準の哲学者）, コスト予算12
    - NORMAL: 39人（全員）, コスト予算80

    battalion_plans が渡されるとそちらを優先する（外部設定）。
    """

    def __init__(
        self,
        specs: Sequence[PhilosopherSpec] = SPECS,
        *,
        max_normal: int = 39,
        max_warn: int = 5,
        max_critical: int = 1,
        budget_normal: int = 80,
        budget_warn: int = 12,
        budget_critical: int = 3,
        cache_instances: bool = True,
        battalion_plans: Optional[Mapping[SafetyMode, "BattalionModePlan"]] = None,
        required_roles: Optional[Sequence[Role]] = None,
    ):
        self._specs = list(specs)
        self._cache = cache_instances
        self._instances: Dict[str, PhilosopherProtocol] = {}
        self._required_roles: Tuple[Role, ...] = tuple(required_roles or ())

        # battalion_plans が渡されたらそちらを優先
        if battalion_plans is not None:
            self._plans: Dict[SafetyMode, SelectionPlan] = {}
            for mode, bp in battalion_plans.items():
                self._plans[mode] = SelectionPlan(
                    limit=bp.limit,
                    max_risk=bp.max_risk,
                    cost_budget=bp.cost_budget,
                    require_tags=bp.require_tags,
                )
        else:
            # mode別 "編成表"（内蔵デフォルト）
            self._plans = {
                SafetyMode.NORMAL: SelectionPlan(
                    limit=max_normal,
                    max_risk=2,
                    cost_budget=budget_normal,
                    require_tags=(
                        TAG_PLANNER,
                        TAG_CRITIC,
                        TAG_COMPLIANCE,
                        TAG_CREATIVE,
                        TAG_REDTEAM,
                    ),
                ),
                SafetyMode.WARN: SelectionPlan(
                    limit=max_warn,
                    max_risk=1,
                    cost_budget=budget_warn,
                    require_tags=(TAG_COMPLIANCE, TAG_CLARIFY, TAG_CRITIC),
                ),
                SafetyMode.CRITICAL: SelectionPlan(
                    limit=max_critical,
                    max_risk=0,
                    cost_budget=budget_critical,
                    require_tags=(TAG_COMPLIANCE, TAG_CLARIFY),
                ),
                SafetyMode.UNKNOWN: SelectionPlan(  # UNKNOWNはWARN扱いで締める
                    limit=max_warn,
                    max_risk=1,
                    cost_budget=budget_warn,
                    require_tags=(TAG_COMPLIANCE, TAG_CLARIFY),
                ),
            }

    def select(self, mode: SafetyMode) -> Selection:
        """
        SafetyModeに応じて哲学者を編成。

        1. 必須タグを満たす（タグごとに最適な1人を選ぶ）
        2. 残り枠をbest候補で埋める（cost budget内で）

        Args:
            mode: SafetyMode

        Returns:
            Selection with selected_ids, cost_total, covered_tags
        """
        plan = self._plans.get(mode, self._plans[SafetyMode.WARN])

        candidates = [
            s for s in self._specs if s.enabled and s.risk_level <= plan.max_risk
        ]
        if self._required_roles:
            role_values = set(self._required_roles)
            candidates = [
                s
                for s in candidates
                if PHILOSOPHER_ROLE_MAP.get(s.philosopher_id) in role_values
            ]
        if mode == SafetyMode.NORMAL:
            candidates = [s for s in candidates if "ai_synthesis" not in s.tags]
        if mode == SafetyMode.CRITICAL:
            candidates = [s for s in candidates if s.philosopher_id != "dummy"]
        # 安定順：安全→重み→id（決定論）
        candidates.sort(key=lambda s: (s.risk_level, -s.weight, s.philosopher_id))

        selected: List[PhilosopherSpec] = []
        cost_total = 0
        covered: set[str] = set()

        def can_take(s: PhilosopherSpec) -> bool:
            return (len(selected) < plan.limit) and (
                cost_total + s.cost <= plan.cost_budget
            )

        # 1) 必須タグを満たす（すでにcoveredならスキップ）
        for tag in plan.require_tags:
            if tag in covered:
                continue
            pick = None
            for s in candidates:
                if s in selected:
                    continue
                if tag in s.tags and can_take(s):
                    pick = s
                    break
            if pick is not None:
                selected.append(pick)
                cost_total += pick.cost
                covered.update(pick.tags)

        # 2) 残り枠をbest候補で埋める
        for s in candidates:
            if s in selected:
                continue
            if not can_take(s):
                continue
            selected.append(s)
            cost_total += s.cost
            covered.update(s.tags)
            if len(selected) >= plan.limit:
                break

        return Selection(
            mode=mode,
            selected_ids=[s.philosopher_id for s in selected],
            cost_total=cost_total,
            covered_tags=sorted(list(covered)),
        )

    def load(
        self, selected_ids: Sequence[str]
    ) -> Tuple[List[PhilosopherProtocol], List[LoadError]]:
        """
        選抜された哲学者をロード（エラー回収付き）。

        39人になるとimportミスが必ず出る。
        なのでloadは落とさず"エラー回収"する。

        Args:
            selected_ids: 選抜されたphilosopher_idのリスト

        Returns:
            Tuple of:
            - ロードされた哲学者インスタンスのリスト
            - ロードエラーのリスト
        """
        by_id = {s.philosopher_id: s for s in self._specs}
        out: List[PhilosopherProtocol] = []
        errors: List[LoadError] = []

        for pid in selected_ids:
            spec = by_id.get(pid)
            if spec is None:
                errors.append(LoadError(pid, "", "", "spec_not_found"))
                continue

            if self._cache and pid in self._instances:
                out.append(self._instances[pid])
                continue

            try:
                mod = importlib.import_module(spec.module)
                obj = getattr(mod, spec.symbol)
                ph = obj() if callable(obj) else obj  # class or factory or instance
                # All Philosopher subclasses implement propose()/info
                # natively via the base class.
                if not hasattr(ph, "propose") or not hasattr(ph, "info"):
                    raise TypeError(
                        f"{pid} does not implement PhilosopherProtocol "
                        f"(missing propose() or info)"
                    )
                out.append(ph)
                if self._cache:
                    self._instances[pid] = ph
            except Exception as e:
                if spec.enabled:
                    raise RuntimeError(
                        f"failed_to_load_enabled_philosopher:{pid}"
                    ) from e
                errors.append(
                    LoadError(pid, spec.module, spec.symbol, type(e).__name__)
                )

        return out, errors

    def select_and_load(self, mode: SafetyMode) -> List[PhilosopherProtocol]:
        """選抜とロードを一度に行う（エラーは無視）。"""
        sel = self.select(mode)
        phs, _ = self.load(sel.selected_ids)
        return phs


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
    "LoadError",
    "SelectionPlan",
    "build_philosophers",
]
