"""
Tensor Metrics
==============

Metric functions for TensorEngine.
Each function returns (key, value) tuple.
"""
from po_core.tensors.metrics.freedom_pressure import metric_freedom_pressure

__all__ = ["metric_freedom_pressure"]
