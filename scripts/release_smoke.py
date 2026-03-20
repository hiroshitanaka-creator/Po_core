"""Installed-artifact smoke checks for wheel/sdist validation."""

from __future__ import annotations

import argparse
import importlib.metadata
import inspect
import json
import pathlib
import subprocess
from importlib import resources
from typing import Sequence

import po_core
import po_core.viewer
from po_core import run
from po_core.cli.commands import main as cli_main
from po_core.runtime.wiring import build_test_system

ENTRYPOINTS = ("po-core", "po-self", "po-trace", "po-interactive", "po-experiment")
ENTRYPOINT_TIMEOUT_SECONDS = 15


def _run_command(
    command: Sequence[str], *, timeout: int = ENTRYPOINT_TIMEOUT_SECONDS
) -> subprocess.CompletedProcess[str]:
    try:
        resolved = subprocess.run(
            list(command),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise SystemExit(
            f"command timed out after {timeout}s: {' '.join(command)}\n"
            f"STDOUT:\n{exc.stdout or ''}\nSTDERR:\n{exc.stderr or ''}"
        ) from exc

    print(f"command={' '.join(command)} rc={resolved.returncode}")
    if resolved.stdout:
        print(f"stdout:\n{resolved.stdout}")
    if resolved.stderr:
        print(f"stderr:\n{resolved.stderr}")
    if resolved.returncode != 0:
        raise SystemExit(
            f"command failed: {' '.join(command)}\nSTDOUT:\n{resolved.stdout}\nSTDERR:\n{resolved.stderr}"
        )
    return resolved


def _assert_contains(output: str, expected: str, command: Sequence[str]) -> None:
    if expected not in output:
        raise SystemExit(
            f"expected {expected!r} in output of {' '.join(command)}\nActual output:\n{output}"
        )


def _assert_console_scripts() -> None:
    for entrypoint in ENTRYPOINTS:
        _run_command([entrypoint, "--help"])

    version_cmd = ["po-core", "version"]
    version = _run_command(version_cmd)
    if version.stdout.strip() != po_core.__version__:
        raise SystemExit(
            f"unexpected po-core version output: {version.stdout.strip()!r} != {po_core.__version__!r}"
        )

    status_cmd = ["po-core", "status"]
    status = _run_command(status_cmd)
    _assert_contains(status.stdout, "Project Status", status_cmd)
    _assert_contains(
        status.stdout, f"Version        : {po_core.__version__}", status_cmd
    )
    _assert_contains(status.stdout, "Philosophers   : 42", status_cmd)

    prompt_cmd = ["po-core", "prompt", "smoke", "--format", "json"]
    prompt = _run_command(prompt_cmd)
    try:
        prompt_payload = json.loads(prompt.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"po-core prompt did not emit valid JSON. Output:\n{prompt.stdout}"
        ) from exc
    if prompt_payload.get("prompt") != "smoke":
        raise SystemExit(f"unexpected prompt echo: {prompt_payload}")
    if not isinstance(prompt_payload.get("responses"), list):
        raise SystemExit(f"prompt responses must be a list: {prompt_payload}")
    if not isinstance(prompt_payload.get("metrics"), dict):
        raise SystemExit(f"prompt metrics must be a dict: {prompt_payload}")

    self_cmd = ["po-self"]
    self_output = _run_command(self_cmd)
    _assert_contains(self_output.stdout, "Po_self - Philosophical Ensemble", self_cmd)

    experiment_cmd = ["po-experiment", "list"]
    experiment = _run_command(experiment_cmd)
    if not (
        "Experiments:" in experiment.stdout
        or "No experiments found." in experiment.stdout
    ):
        raise SystemExit(
            f"unexpected po-experiment list output:\nSTDOUT:\n{experiment.stdout}\nSTDERR:\n{experiment.stderr}"
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

    viewer_path = (
        pathlib.Path(inspect.getfile(po_core.viewer)).parent / "standalone.html"
    )
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
