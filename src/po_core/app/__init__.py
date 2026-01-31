# SPDX-License-Identifier: MIT
"""
Po_core Application Layer

This module provides the single public entry point for external consumers.
All external code (e.g., 03_api/*) should import ONLY from po_core.app.api.
"""

from po_core.app.api import PoCore, PoCoreConfig

__all__ = ["PoCore", "PoCoreConfig"]
