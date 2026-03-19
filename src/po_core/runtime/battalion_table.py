"""
battalion_table.py - 編成表ローダー
===================================

外部ファイル（JSON-in-YAML）から SafetyModeごとの編成ポリシーを読み込む。

目的:
- 「思想＝設計方針」を 02_architecture に固定
- ただしコードはその内容に依存しない（差し替え可能）

DEPENDENCY RULES:
- domain には依存しない（SafetyMode enumのみ）
- JSON は標準ライブラリのみで読む（依存ゼロ）
- YAML は optional（jsonとして読めなければ pyyaml を試す）
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Any, Dict, Mapping, Set, Tuple

from po_core.domain.safety_mode import SafetyMode

_DEFAULT_RESOURCE = "runtime/battalion_table.yaml"


@dataclass(frozen=True)
class BattalionModePlan:
    """
    SafetyModeごとの編成方針。

    Attributes:
        limit: 採用する哲学者数の上限
        max_risk: 許容する最大 risk_tier
        cost_budget: 合計コスト上限
        require_tags: 可能なら含めたいタグ（不足時はベストエフォート）
    """

    limit: int
    max_risk: int
    cost_budget: int
    require_tags: Tuple[str, ...]


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_packaged_default_text() -> str:
    """Read packaged default battalion table text from installed artifact."""

    return (
        resources.files("po_core.config")
        .joinpath(_DEFAULT_RESOURCE)
        .read_text(encoding="utf-8")
    )


def load_battalion_table(path: str) -> Dict[SafetyMode, BattalionModePlan]:
    """
    編成表YAMLをロードする。

    Args:
        path: YAMLファイルパス

    Returns:
        SafetyMode -> BattalionModePlan の辞書

    Note:
        JSON形式なら依存ゼロ。YAML形式の場合は PyYAML が必要。
    """
    raw = _read_text(path)
    return _parse_battalion_table(raw)


def load_packaged_battalion_table() -> Dict[SafetyMode, BattalionModePlan]:
    """Load default battalion table from packaged resources."""

    return _parse_battalion_table(read_packaged_default_text())


def _parse_battalion_table(raw: str) -> Dict[SafetyMode, BattalionModePlan]:
    data: Any = None
    try:
        data = json.loads(raw)  # JSON形式なら依存ゼロ
    except Exception:
        # YAMLを使いたい場合だけPyYAMLを許可
        try:
            import yaml

            data = yaml.safe_load(raw)
        except Exception as e:
            raise RuntimeError(
                "battalion_table parse failed (use JSON-in-YAML or install pyyaml)"
            ) from e

    if not isinstance(data, dict) or "modes" not in data:
        raise ValueError("invalid battalion_table schema")

    modes = data["modes"]
    if not isinstance(modes, dict):
        raise ValueError("invalid modes")

    # inherit解決
    def resolve(name: str, seen: Set[str]) -> Mapping[str, Any]:
        if name in seen:
            raise ValueError(f"inherit cycle: {name}")
        seen.add(name)

        m = modes.get(name)
        if not isinstance(m, dict):
            raise ValueError(f"mode not found: {name}")

        if "inherit" in m:
            base = resolve(str(m["inherit"]), seen)
            merged = dict(base)
            merged.update({k: v for k, v in m.items() if k != "inherit"})
            return merged
        return m

    out: Dict[SafetyMode, BattalionModePlan] = {}
    for key in ("normal", "warn", "critical", "unknown"):
        m = resolve(key, set())
        require_tags = tuple(m.get("require_tags", []) or [])
        out[_to_mode(key)] = BattalionModePlan(
            limit=int(m.get("limit", 0)),
            max_risk=int(m.get("max_risk", 1)),
            cost_budget=int(m.get("cost_budget", 0)),
            require_tags=require_tags,
        )

    return out


def _to_mode(s: str) -> SafetyMode:
    s = (s or "").lower()
    if s == "normal":
        return SafetyMode.NORMAL
    if s == "warn":
        return SafetyMode.WARN
    if s == "critical":
        return SafetyMode.CRITICAL
    return SafetyMode.UNKNOWN


__all__ = [
    "BattalionModePlan",
    "load_battalion_table",
    "load_packaged_battalion_table",
    "read_packaged_default_text",
]
