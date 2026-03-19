"""Packaged JSON Schema resources for :mod:`po_core.runner`."""

from __future__ import annotations

from importlib.abc import Traversable
from importlib.resources import files
from typing import Final

PACKAGE_NAME: Final[str] = __name__


def resource_path(name: str) -> Traversable:
    """Return a traversable handle for a packaged schema resource."""
    return files(PACKAGE_NAME).joinpath(name)
