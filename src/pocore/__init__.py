"""
pocore — DEPRECATED, TEST-ONLY SHIM.

This package (``pocore``) is the M1 scaffold namespace retained inside the
repository *only* for backward-compatible imports from the existing test
suite.  It is **NOT** packaged into the ``po-core-flyingpig`` wheel (see
``pyproject.toml::tool.setuptools.packages.find.exclude``), so it is never
importable by users of the published distribution.

The package will be deleted once no tests import from ``pocore``.

Migration
---------
  # Old (deprecated, repo-internal only)
  from pocore.runner import run_case_file

  # New (canonical, works for both repo and installed package)
  from po_core.runner import run_case_file

Public API (deprecated, use po_core equivalents)
-------------------------------------------------
    run_case_file(path, *, seed, now, deterministic) -> dict
    run_session_replay(case_path, answers_path, *, seed, now, deterministic) -> dict
"""

import warnings

warnings.warn(
    "The 'pocore' package is a test-only shim that is not shipped with the "
    "po-core-flyingpig wheel; import 'po_core' instead. "
    "See docs/legacy/pocore_migration.md for the migration guide.",
    DeprecationWarning,
    stacklevel=2,
)

from .runner import run_case_file, run_session_replay

__all__ = ["run_case_file", "run_session_replay"]
