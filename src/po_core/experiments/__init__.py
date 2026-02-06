"""Experiment management framework for Po_core.

This package provides tools for running A/B experiments on different
Pareto philosophy configurations, analyzing results statistically,
and automatically promoting winning variants.

Key components:
- storage: Persist experiment definitions, samples, and analyses
- runner: Execute experiments by running multiple variants
- analyzer: Statistical analysis (t-tests, significance testing)
- promoter: Automatic promotion of winning configurations
"""

from po_core.experiments.analyzer import ExperimentAnalyzer
from po_core.experiments.promoter import ExperimentPromoter
from po_core.experiments.runner import ExperimentRunner
from po_core.experiments.storage import ExperimentStorage

__all__ = [
    "ExperimentStorage",
    "ExperimentRunner",
    "ExperimentAnalyzer",
    "ExperimentPromoter",
]
