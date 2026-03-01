"""
Internal Keys - extra の予約領域
================================

aggregator / ensemble / viewer が同じキーを共有するため、domain に置く。

DEPENDENCY RULES:
- 定数のみ（依存ゼロ）
- ここを import しても循環しない
"""

# top-level namespace (proposal.extra[PO_CORE])
PO_CORE = "_po_core"

# nested keys under PO_CORE
POLICY = "policy"
TRACEQ = "trace_quality"
PARETO_DEBUG = "pareto_debug"
CONFLICTS = "conflicts"
OBJECTIVES = "objectives"
WEIGHTS = "weights"
FRONT = "front"
WINNER = "winner"
MODE = "mode"
FREEDOM_PRESSURE = "freedom_pressure"
AUTHOR = "author"
AUTHOR_RELIABILITY = "author_reliability"
EMERGENCE_NOVELTY = "emergence_novelty"

# Philosopher response provenance (set by base.propose())
RATIONALE = "rationale"  # short justification extracted from reason() output
CITATIONS = "citations"  # list of philosophical references returned by reason()


__all__ = [
    "PO_CORE",
    "POLICY",
    "TRACEQ",
    "PARETO_DEBUG",
    "CONFLICTS",
    "OBJECTIVES",
    "WEIGHTS",
    "FRONT",
    "WINNER",
    "MODE",
    "FREEDOM_PRESSURE",
    "AUTHOR",
    "AUTHOR_RELIABILITY",
    "EMERGENCE_NOVELTY",
    "RATIONALE",
    "CITATIONS",
]
