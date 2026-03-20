"""Installed-artifact smoke checks for wheel/sdist validation."""

from __future__ import annotations

import argparse
import importlib.metadata
import inspect
import pathlib
import subprocess
import sys
from importlib import resources

import po_core
import po_core.viewer
from po_core import run
from po_core.cli.commands import main as cli_main
from po_core.runtime.wiring import build_test_system

ENTRYPOINTS = ("po-core", "po-self", "po-trace", "po-interactive", "po-experiment")


def _assert_console_scripts() -> None:
    for entrypoint in ENTRYPOINTS:
        resolved = subprocess.run(
            [entrypoint, "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        print(f"entrypoint={entrypoint} rc={resolved.returncode}")
        if resolved.returncode != 0:
            raise SystemExit(
                f"console script failed: {entrypoint}\nSTDOUT:\n{resolved.stdout}\nSTDERR:\n{resolved.stderr}"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-entrypoints", action="store_true")
    args = parser.parse_args()

    dist_version = importlib.metadata.version("po-core-flyingpig")
    pkg_version = po_core.__version__
    print(f"dist_version={dist_version}")
    print(f"pkg_version={pkg_version}")
    if dist_version != pkg_version:
        raise SystemExit(f"version mismatch: dist={dist_version} package={pkg_version}")

    config_root = resources.files("po_core.config")
    battalion_resource = config_root.joinpath("runtime/battalion_table.yaml")
    pareto_resource = config_root.joinpath("runtime/pareto_table.yaml")
    print(f"battalion_resource={battalion_resource}")
    print(f"pareto_resource={pareto_resource}")
    if not battalion_resource.is_file():
        raise SystemExit(f"missing battalion resource: {battalion_resource}")
    if not pareto_resource.is_file():
        raise SystemExit(f"missing pareto resource: {pareto_resource}")

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

    cli_name = getattr(cli_main, "name", None)
    print(f"cli_name={cli_name}")
    if cli_name != "main":
        raise SystemExit(f"unexpected cli main name: {cli_name}")

    if args.check_entrypoints:
        _assert_console_scripts()


if __name__ == "__main__":
    main()
