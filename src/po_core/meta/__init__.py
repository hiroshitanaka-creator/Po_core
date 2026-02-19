"""
Po_core Meta-Ethics Module
===========================

倫理的自己反省 (Ethical Self-Reflection) コンポーネント群。

Phase 6-C 実装:
  EthicalQualityScore     — 1推論サイクルの倫理品質スコア (4指標 + 総合)
  MetaEthicsMonitor       — CUSUM ドリフト監視 + SafetyMode 自動引き上げ
  DriftState              — CUSUM 状態スナップショット
  PhilosopherQualityLedger — 哲学者別品質履歴
  PhilosopherRecord       — 哲学者個別レコード

Usage::

    from po_core.meta import (
        EthicalQualityScore,
        MetaEthicsMonitor,
        PhilosopherQualityLedger,
    )

    ledger  = PhilosopherQualityLedger()
    monitor = MetaEthicsMonitor(ledger, drift_threshold=0.15)

    score = EthicalQualityScore.compute(
        request_id=ctx.request_id,
        proposals=proposals,
        winner=winner,
        verdict=verdict,
        tensors=tensors,
    )
    escalation = monitor.record(score, tracer)
"""

from po_core.meta.ethics_monitor import (
    DriftState,
    EthicalQualityScore,
    MetaEthicsMonitor,
)
from po_core.meta.philosopher_ledger import PhilosopherQualityLedger, PhilosopherRecord

__all__ = [
    "DriftState",
    "EthicalQualityScore",
    "MetaEthicsMonitor",
    "PhilosopherQualityLedger",
    "PhilosopherRecord",
]
