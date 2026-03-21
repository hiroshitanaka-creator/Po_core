"""Installed-artifact smoke checks for wheel/sdist validation."""

from __future__ import annotations

import argparse
import importlib.metadata
import inspect
import json
import pathlib
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from contextlib import closing
from importlib import resources
from typing import Sequence

import po_core
import po_core.viewer
from po_core import run
from po_core.cli.commands import main as cli_main
from po_core.runtime.wiring import build_test_system

ENTRYPOINTS = ("po-core", "po-self", "po-trace", "po-interactive", "po-experiment")
ENTRYPOINT_TIMEOUT_SECONDS = 15
_SERVER_START_TIMEOUT_SECONDS = 15


def _find_free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return int(sock.getsockname()[1])


def _run_command(
    command: Sequence[str], *, timeout: int = ENTRYPOINT_TIMEOUT_SECONDS, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    try:
        resolved = subprocess.run(
            list(command),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
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


def _http_request(
    url: str, *, method: str = "GET", payload: dict | None = None, headers: dict[str, str] | None = None
) -> tuple[int, str]:
    body = None
    merged_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        merged_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=merged_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=ENTRYPOINT_TIMEOUT_SECONDS) as resp:
            return resp.getcode(), resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


def _wait_for_http_ready(url: str, *, timeout: int) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            status, _ = _http_request(url)
            if status == 200:
                return
        except Exception as exc:  # pragma: no cover - startup race only
            last_error = exc
        time.sleep(0.2)
    raise SystemExit(f"server did not become ready: {url}; last_error={last_error}")


def _start_rest_server(*, port: int, api_key: str, skip_auth: bool) -> subprocess.Popen[str]:
    env = dict(**__import__('os').environ)
    env.update(
        {
            "PO_HOST": "127.0.0.1",
            "PO_PORT": str(port),
            "PO_SKIP_AUTH": "true" if skip_auth else "false",
            "PO_API_KEY": api_key,
            "PO_TRACE_STORE_BACKEND": "memory",
            "PO_REVIEW_STORE_BACKEND": "memory",
            "PO_PHILOSOPHER_EXECUTION_MODE": "process",
        }
    )
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "po_core.app.rest.server:app", "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )


def _stop_process(process: subprocess.Popen[str]) -> tuple[str, str]:
    try:
        process.terminate()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)
    stdout, stderr = process.communicate()
    return stdout, stderr


def _assert_rest_server_path() -> None:
    bad_port = _find_free_port()
    bad_process = _start_rest_server(port=bad_port, api_key="   ", skip_auth=False)
    try:
        bad_process.wait(timeout=_SERVER_START_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        bad_stdout, bad_stderr = _stop_process(bad_process)
        raise SystemExit(
            "misconfigured auth startup unexpectedly succeeded\n"
            f"STDOUT:\n{bad_stdout}\nSTDERR:\n{bad_stderr}"
        )
    bad_stdout, bad_stderr = _stop_process(bad_process)
    if "Startup aborted" not in f"{bad_stdout}\n{bad_stderr}":
        raise SystemExit(
            "misconfigured auth startup did not fail closed with expected message\n"
            f"STDOUT:\n{bad_stdout}\nSTDERR:\n{bad_stderr}"
        )

    port = _find_free_port()
    process = _start_rest_server(port=port, api_key="smoke-secret", skip_auth=False)
    try:
        _wait_for_http_ready(f"http://127.0.0.1:{port}/v1/health", timeout=_SERVER_START_TIMEOUT_SECONDS)

        unauthorized_status, unauthorized_body = _http_request(
            f"http://127.0.0.1:{port}/v1/reason", method="POST", payload={"input": "smoke"}
        )
        if unauthorized_status != 401:
            raise SystemExit(
                f"expected 401 without API key, got {unauthorized_status}: {unauthorized_body}"
            )

        authorized_status, authorized_body = _http_request(
            f"http://127.0.0.1:{port}/v1/reason",
            method="POST",
            payload={"input": "smoke"},
            headers={"X-API-Key": "smoke-secret"},
        )
        if authorized_status != 200:
            raise SystemExit(f"/v1/reason failed: {authorized_status} {authorized_body}")
        payload = json.loads(authorized_body)
        if payload.get("status") not in {"approved", "blocked", "ok"}:
            raise SystemExit(f"unexpected reason payload: {payload}")

        stream_status, stream_body = _http_request(
            f"http://127.0.0.1:{port}/v1/reason/stream",
            method="POST",
            payload={"input": "smoke"},
            headers={"X-API-Key": "smoke-secret"},
        )
        if stream_status != 200:
            raise SystemExit(f"/v1/reason/stream failed: {stream_status} {stream_body}")
        if "event: done" not in stream_body and '"chunk_type": "done"' not in stream_body:
            raise SystemExit(f"unexpected stream payload: {stream_body}")
    finally:
        stdout, stderr = _stop_process(process)
        print(f"rest_server_stdout:\n{stdout}")
        print(f"rest_server_stderr:\n{stderr}")


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
    _assert_contains(status.stdout, f"Version        : {po_core.__version__}", status_cmd)
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
    if not ("Experiments:" in experiment.stdout or "No experiments found." in experiment.stdout):
        raise SystemExit(
            f"unexpected po-experiment list output:\nSTDOUT:\n{experiment.stdout}\nSTDERR:\n{experiment.stderr}"
        )


def _dist_matches_imported_package(dist_name: str) -> tuple[bool, str]:
    """Return whether installed metadata belongs to the imported checkout."""
    try:
        distribution = importlib.metadata.distribution(dist_name)
    except importlib.metadata.PackageNotFoundError:
        return False, "distribution metadata not installed"

    try:
        imported_init = pathlib.Path(po_core.__file__).resolve()
        dist_init = pathlib.Path(distribution.locate_file("po_core/__init__.py")).resolve()
    except FileNotFoundError:
        return False, "distribution metadata exists but po_core/__init__.py is missing"

    if dist_init == imported_init:
        return True, f"matched import path {dist_init}"

    return (
        False,
        "ignoring unrelated installed distribution metadata at "
        f"{dist_init} (imported checkout uses {imported_init})",
    )


def _resolve_checked_distribution_version(dist_name: str) -> tuple[str | None, str]:
    """Return the installed version only when metadata matches the imported checkout."""
    dist_matches_checkout, dist_note = _dist_matches_imported_package(dist_name)
    if not dist_matches_checkout:
        return None, dist_note
    return importlib.metadata.version(dist_name), dist_note


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-entrypoints", action="store_true")
    args = parser.parse_args()

    pkg_version = po_core.__version__
    print(f"pkg_version={pkg_version}")

    dist_version, dist_note = _resolve_checked_distribution_version("po-core-flyingpig")
    print(f"dist_metadata={dist_note}")
    if dist_version is not None:
        print(f"dist_version={dist_version}")
        if dist_version != pkg_version:
            raise SystemExit(
                f"version mismatch: dist={dist_version} package={pkg_version}"
            )
    else:
        print("dist_version=skipped")

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

    _assert_rest_server_path()

    if args.check_entrypoints:
        _assert_console_scripts()


if __name__ == "__main__":
    main()
