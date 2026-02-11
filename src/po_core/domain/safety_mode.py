"""
SafetyMode - 縮退制御のモード判定。

FreedomPressure などのメトリクスから安全モードを推定する。
メトリクス欠損時は WARN に倒す（fail-safe）。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from po_core.domain.tensor_snapshot import TensorSnapshot


class SafetyMode(str, Enum):
    """Safety operation modes."""

    NORMAL = "normal"  # 通常運転（創造性を許容）
    WARN = "warn"  # 警戒モード（慎重に）
    CRITICAL = "critical"  # 危機モード（最小限の応答）
    UNKNOWN = "unknown"  # 不明（計測不能）


@dataclass(frozen=True)
class SafetyModeConfig:
    """Configuration for safety mode inference."""

    metric_key: str = "freedom_pressure"
    warn: float = 0.30  # 正規化FP [0, ~0.44] に適合（Phase 1で調整済）
    critical: float = 0.50
    missing_mode: SafetyMode = SafetyMode.WARN  # ← ここが"締め"


def infer_safety_mode(
    tensors: TensorSnapshot,
    config: SafetyModeConfig = SafetyModeConfig(),
) -> Tuple[SafetyMode, Optional[float]]:
    """
    Infer safety mode from tensor metrics.

    Args:
        tensors: Tensor snapshot containing metrics
        config: Safety mode configuration

    Returns:
        Tuple of (SafetyMode, metric_value or None if missing)

    Note:
        メトリクス欠損時は missing_mode (default: WARN) に倒す。
        計測が壊れてても守りに倒れる。
    """
    v = tensors.metrics.get(config.metric_key)
    if v is None:
        return config.missing_mode, None

    try:
        x = float(v)
    except Exception:
        return config.missing_mode, None

    if x >= config.critical:
        return SafetyMode.CRITICAL, x
    if x >= config.warn:
        return SafetyMode.WARN, x
    return SafetyMode.NORMAL, x


__all__ = ["SafetyMode", "SafetyModeConfig", "infer_safety_mode"]
