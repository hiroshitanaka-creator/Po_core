# Po_core Repository Structure

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE)

**Document Status:** release-readiness inventory aligned to package version `1.0.2`  
**Last Updated:** 2026-03-20
**Scope:** actual repository layout and release-critical files only

This document is maintained from the repository tree and current packaging / CI configuration. It intentionally avoids historical milestone claims that are not encoded in the current repo.

---

## Repository Root

Top-level directories currently present in the repository:

- `.github/` — issue templates and GitHub Actions workflows
- `01_specifications/`, `02_architecture/`, `03_api/`, `04_modules/`, `05_research/` — legacy and current design/reference docs
- `clients/` — generated / maintained client SDK assets
- `docs/` — operational docs, ADRs, release evidence, specs, papers, results
- `examples/` — source-checkout usage examples
- `experiments/` — non-runtime experimental code and data, including Claude-testing assets now isolated from `src/po_core`
- `papers/`, `reports/`, `sessions/` — research and run artifacts
- `scenarios/` — golden-contract scenario inputs/expected outputs
- `scripts/` — release, export, research, and maintenance scripts
- `src/` — runtime Python packages (`po_core`, `pocore`)
- `tests/` — acceptance, unit, integration, red-team, runtime, execution, viewer, adapter, and benchmark suites
- `tools/` — repo maintenance tooling

Key root files used for release readiness:

- `pyproject.toml` — packaging metadata and dependency truth source
- `README.md`, `QUICKSTART.md`, `QUICKSTART_EN.md` — user-facing install/runtime docs
- `CHANGELOG.md` — versioned release notes
- `.env.example` — deployment environment defaults
- `requirements.txt`, `requirements-dev.txt` — repo-local editable-install convenience wrappers for a cloned checkout
- `pytest.ini` — pytest configuration / markers

---

## GitHub Actions / Release Path

`.github/workflows/` currently contains:

- `ci.yml` — lint, must-pass tests, full suite, security, build, artifact smoke
- `publish.yml` — guarded TestPyPI / PyPI publishing
- `import-guard.yml` — import graph enforcement
- `policy_lab.yml` — policy-lab automation
- `pr-governance.yml` — PR governance checks
- `typescript-sdk.yml` — OpenAPI / TypeScript SDK refresh

---

## Runtime Package: `src/po_core/`

The published runtime package lives under `src/po_core/` and currently contains these subpackages / major modules:

- `adapters/`
- `aggregator/`
- `app/`
  - `app/api.py` — public programmatic entrypoint facade
  - `app/rest/` — FastAPI delivery layer
- `autonomy/solarwill/`
- `axis/specs/`
- `cli/`
- `config/` and `config/runtime/`
- `deliberation/`
- `domain/`
- `experiments/` — runtime experiment helpers that are intentionally part of the package
- `memory/`
- `meta/`
- `philosophers/`
  - `manifest.py` / `registry.py` / `allowlist.py`
  - rule-based philosopher modules
  - `llm_personas.py` / `llm_philosopher.py` for runtime LLM persona routing
  - `prompts/` for non-packaged YAML draft assets only
- `ports/`
- `runtime/`
- `safety/`
- `schemas/`
- `tensors/`
- `text/`
- `trace/`
- `viewer/` and `viewer/web/`

Release-relevant module facts:

- Package version SSOT is `src/po_core/__init__.py`.
- OpenAPI metadata is emitted from `src/po_core/app/rest/server.py`.
- Installed package data is limited to config YAML, axis specs, JSON schemas, viewer assets, and `py.typed`; unfinished philosopher YAML prompt drafts are not packaged.
- Experimental Claude-testing modules are **not** under `src/po_core` and therefore are not part of the published runtime surface.

---

## Philosopher Inventory

- `src/po_core/philosophers/manifest.py` defines the enabled runtime philosopher roster and related metadata.
- Public docs and API metadata should describe the runtime roster as **42 integrated philosophers**.
- Runtime selection budgets in settings cap the default NORMAL path at **39 active philosophers maximum per request**.
- The `src/po_core/philosophers/` directory also contains helper modules such as `dummy.py`, `template.py`, `tags.py`, `llm_personas.py`, and `llm_philosopher.py`; directory file count must not be confused with the 42-person runtime roster.

---

## Legacy / Experimental / Non-Packaged Assets

These are intentionally outside the published runtime package:

- `src/pocore/` — legacy namespace / contract-core compatibility code
- `experiments/claude_testing/` — Claude-only prompt/testing helpers (`po_system_prompt.py`, `po_claude_client.py`, `po_test_runner.py`)
- `examples/` — illustrative scripts, not package API
- `docs/experiments/`, `docs/results/`, `papers/`, `reports/`, `sessions/` — research / evidence artifacts

---

## Tests

`tests/` currently includes these major areas:

- `acceptance/` — acceptance contract suite
- `adapters/` — adapter-specific tests
- `app/rest/` — REST-specific tests
- `axis/`, `calibration/`, `runtime/`, `trace/`, `viewer/` — subsystem tests
- `benchmarks/` — performance checks
- `execution/` — timeout / execution backend checks
- `experiments/` — experiment framework tests
- `integration/` — cross-module integration tests
- `philosophers/` and `unit/test_philosophers/` — philosopher behavior tests
- `redteam/` — adversarial safety tests
- `unit/` — broad unit test coverage

Release readiness additionally relies on top-level tests such as:

- `tests/test_release_readiness.py`
- `tests/test_output_schema.py`
- `tests/test_golden_e2e.py`
- `tests/test_input_schema.py`

---

## Release-Critical Source of Truth Map

- **Version:** `src/po_core/__init__.py`
- **Packaging metadata:** `pyproject.toml`
- **OpenAPI metadata:** `src/po_core/app/rest/server.py`
- **Release workflow gates:** `.github/workflows/ci.yml`, `.github/workflows/publish.yml`
- **Golden contract:** `scenarios/`, `tests/test_golden_e2e.py`
- **Prompt runtime SSOT:** `src/po_core/philosophers/llm_personas.py`
- **Experimental Claude-only assets:** `experiments/claude_testing/`

---

## Maintenance Rule for This Document

When repository structure, packaging boundaries, or release-critical paths change, update this file together with `tests/test_release_readiness.py` so stale inventory phrases are rejected automatically.
