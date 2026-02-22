"""
pocore — Philosophy-driven decision engine (M1 scaffold).

Design stance:
- Determinism first.
- Schema as contract.
- Golden files are executable specifications.

Public API
----------
    run_case_file(path, *, seed, now, deterministic) -> dict
"""

from .runner import run_case_file

__all__ = ["run_case_file"]
