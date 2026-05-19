"""Packaged JSON Schema resources for :mod:`po_core.runner`."""

from __future__ import annotations

from importlib.resources import files

try:
    from importlib.resources.abc import Traversable  # type: ignore[import-not-found]
except ImportError:  # Python < 3.11
    from importlib.abc import Traversable  # noqa: F811

from typing import Final

PACKAGE_NAME: Final[str] = __name__


def resource_path(name: str) -> Traversable:
    """Return a traversable handle for a packaged schema resource."""
    return files(PACKAGE_NAME).joinpath(name)
