"""
pareto_table.py - Pareto設定ローダー
====================================

外部ファイル（JSON-in-YAML）からParetoConfigを読み込む。
battalion_table と同じ思想：YAMLだけど中身はJSON＝依存ゼロで読める。

DEPENDENCY RULES:
- domain のみ依存
- JSON は標準ライブラリ（依存ゼロ）
- YAML は optional（なければ JSON として読む）
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Mapping, Set

from po_core.domain.pareto_config import ParetoConfig, ParetoTuning, ParetoWeights
from po_core.domain.safety_mode import SafetyMode


def _read_text(path: str) -> str:
    """ファイルを読み込む"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _as_dict(x: Any) -> dict:
    """安全に dict へ変換"""
    return dict(x) if isinstance(x, Mapping) else {}


def _to_mode(s: str) -> SafetyMode:
    """文字列を SafetyMode に変換"""
    s = (s or "").lower()
    if s == "normal":
        return SafetyMode.NORMAL
    if s == "warn":
        return SafetyMode.WARN
    if s == "critical":
        return SafetyMode.CRITICAL
    return SafetyMode.UNKNOWN


def load_pareto_table(path: str) -> ParetoConfig:
    """
    Pareto設定ファイルを読み込む。

    Args:
        path: 設定ファイルパス（JSON-in-YAML or pure JSON）

    Returns:
        ParetoConfig

    Raises:
        RuntimeError: パースに失敗した場合
        ValueError: inherit 循環が検出された場合
    """
    raw = _read_text(path)

    data: Any = None
    try:
        # JSON-in-YAML ならここで終わる（依存ゼロ）
        data = json.loads(raw)
    except Exception:
        try:
            import yaml  # type: ignore
            data = yaml.safe_load(raw)
        except Exception as e:
            raise RuntimeError(
                "pareto_table parse failed (use JSON-in-YAML or install pyyaml)"
            ) from e

    d = _as_dict(data)
    ver = int(d.get("version", 1) or 1)

    weights = _as_dict(d.get("weights"))
    tuning = _as_dict(d.get("tuning"))

    # inherit 解決（unknown -> warn 等）
    def resolve(name: str, seen: Set[str]) -> Mapping[str, Any]:
        if name in seen:
            raise ValueError(f"inherit cycle: {name}")
        seen.add(name)

        m = _as_dict(weights.get(name))
        if "inherit" in m:
            base = resolve(str(m["inherit"]), seen)
            merged = dict(base)
            merged.update({k: v for k, v in m.items() if k != "inherit"})
            return merged
        return m

    w_by_mode: Dict[SafetyMode, ParetoWeights] = {}
    for key in ("normal", "warn", "critical", "unknown"):
        m = resolve(key, set())
        w_by_mode[_to_mode(key)] = ParetoWeights(
            safety=float(m.get("safety", 0.0)),
            freedom=float(m.get("freedom", 0.0)),
            explain=float(m.get("explain", 0.0)),
            brevity=float(m.get("brevity", 0.0)),
            coherence=float(m.get("coherence", 0.0)),
        )

    mix = _as_dict(tuning.get("explain_mix"))
    t = ParetoTuning(
        brevity_max_len=int(tuning.get("brevity_max_len", 2000)),
        explain_rationale_weight=float(mix.get("rationale", 0.65)),
        explain_author_rel_weight=float(mix.get("author_rel", 0.35)),
        front_limit=int(tuning.get("front_limit", 20)),
    )

    return ParetoConfig(weights_by_mode=w_by_mode, tuning=t, version=ver, source=f"file:{path}")


__all__ = ["load_pareto_table"]
