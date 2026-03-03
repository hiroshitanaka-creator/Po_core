#!/usr/bin/env python3
"""Compatibility entrypoint for the v1.0.0 release readiness check."""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1] / "check_release_readiness.py"
    runpy.run_path(str(target), run_name="__main__")
