"""Installed-artifact smoke checks for wheel/sdist validation."""

from __future__ import annotations

import importlib.metadata
import inspect
import pathlib

import po_core
import po_core.viewer
from po_core import run
from po_core.runtime.wiring import build_test_system


def main() -> None:
    dist_version = importlib.metadata.version("po-core-flyingpig")
    pkg_version = po_core.__version__
    print(f"dist_version={dist_version}")
    print(f"pkg_version={pkg_version}")
    if dist_version != pkg_version:
        raise SystemExit(
            f"version mismatch: dist={dist_version} package={pkg_version}"
        )

    viewer_path = pathlib.Path(inspect.getfile(po_core.viewer)).parent / "standalone.html"
    print(f"viewer_html={viewer_path}")
    if not viewer_path.exists():
        raise SystemExit(f"viewer HTML missing: {viewer_path}")

    system = build_test_system()
    config_source = system.aggregator.config.source
    print(f"runtime_config_source={config_source}")
    if not str(config_source).startswith("package:"):
        raise SystemExit(f"unexpected runtime config source: {config_source}")

    result = run("What is justice?")
    status = result.get("status")
    print(f"run_status={status}")
    if status not in {"ok", "blocked"}:
        raise SystemExit(f"unexpected run status: {status}")


if __name__ == "__main__":
    main()
