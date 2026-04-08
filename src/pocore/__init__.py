"""
pocore — DEPRECATED. Use ``po_core`` instead.

This package (``pocore``) is the M1 scaffold namespace retained for test
backward-compatibility only. It will be removed in a future release.

Migration
---------
  # Old (deprecated)
  from pocore.runner import run_case_file

  # New (canonical)
  from po_core.runner import run_case_file

Public API (deprecated, use po_core equivalents)
-------------------------------------------------
    run_case_file(path, *, seed, now, deterministic) -> dict
    run_session_replay(case_path, answers_path, *, seed, now, deterministic) -> dict
"""

import warnings

warnings.warn(
    "The 'pocore' package is deprecated and will be removed in a future release. "
    "Use 'po_core' instead. "
    "See migration guide in docs/legacy/pocore_migration.md.",
    DeprecationWarning,
    stacklevel=2,
)

from .runner import run_case_file, run_session_replay

__all__ = ["run_case_file", "run_session_replay"]
