"""Shared philosopher allowlist wrapper for SafetyMode-based selection."""

from __future__ import annotations

from typing import Any

from po_core.philosophers.manifest import SPECS


class AllowlistRegistry:
    """Filter selected philosopher IDs by a caller-provided allowlist.

    The wrapper is applied *after* the underlying registry performs normal
    SafetyMode/risk/cost selection. This preserves safety guarantees while
    allowing explicit caller control over subset selection.
    """

    def __init__(self, wrapped: Any, allowlist: list[str]) -> None:
        self._wrapped = wrapped
        self._allowlist: set[str] = set(allowlist)

    def select(self, mode: Any, **kwargs: Any) -> Any:
        from po_core.philosophers.registry import Selection

        sel = self._wrapped.select(mode, **kwargs)
        filtered_ids = [pid for pid in sel.selected_ids if pid in self._allowlist]
        if not filtered_ids:
            raise ValueError(
                f"philosophers allowlist {sorted(self._allowlist)!r} has no overlap "
                f"with SafetyMode-{mode.value!r} selection "
                f"{sel.selected_ids!r}. "
                "Expand the allowlist or remove the philosophers argument."
            )
        cost = sum(s.cost for s in SPECS if s.philosopher_id in set(filtered_ids))
        return Selection(
            mode=mode,
            selected_ids=filtered_ids,
            cost_total=cost,
            covered_tags=sel.covered_tags,
        )

    def load(self, selected_ids: Any) -> Any:
        return self._wrapped.load(selected_ids)

    def select_and_load(self, mode: Any) -> Any:
        sel = self.select(mode)
        phs, _ = self.load(sel.selected_ids)
        return phs
