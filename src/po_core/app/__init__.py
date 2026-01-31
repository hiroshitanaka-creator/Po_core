"""
Po_core Application Layer
=========================

This module provides the single public entry point for external consumers.
All external code (e.g., 03_api/*, examples/*) should import ONLY from po_core.app.api.

Usage:
    from po_core.app import run

    result = run(user_input="What is justice?")
"""

from po_core.app.api import run

__all__ = ["run"]
