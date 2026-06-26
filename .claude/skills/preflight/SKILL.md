---
name: preflight
description: Run Po_core's formatting, linting, governance, and traceability gates before committing or opening a PR. Use before any commit/push, when preparing a PR, or to reproduce the CI governance checks locally.
---

# Preflight (commit / PR readiness)

Run the same gates CI enforces, in order. Stop and fix at the first failure.

## 1. Format & lint (pre-commit)

Never use `--no-verify`. Run the hooks:

```bash
pre-commit run --all-files
```

Covers black 26.1.0, isort (black profile), flake8 (max-line 88), mypy,
bandit, pydocstyle (google), markdownlint, plus file hygiene hooks. If
pre-commit isn't installed: `pre-commit install`.

## 2. Tests

Use the `run-tests` skill. At minimum reproduce CI:

```bash
pytest tests/ -v -m "not slow"
```

Pipeline-marked tests MUST pass.

## 3. Governance gates (CI parity)

- **Traceability / config_version check**:
  ```bash
  python scripts/update_traceability.py --check
  ```
- **PR governance** (NFR-GOV-001 — substantive PRs must reference requirement
  IDs):
  ```bash
  python scripts/check_pr_governance.py
  ```
- **Release readiness** (only when touching release/version):
  ```bash
  python scripts/check_release_readiness.py
  ```

## 4. Config-change rules (CLAUDE.md "Do NOT")

- Changed `pareto_table.yaml` or `battalion_table.yaml`
  (`src/po_core/config/runtime/`)? You MUST bump the `version` field in the
  same file. Policy-constant changes additionally follow ADR-0012.
- Added a dependency? Update BOTH `pyproject.toml` AND `requirements.txt`.
- Output changed? Regenerate goldens via the `regen-golden` skill.

## 5. Status

Run the `update-status` skill before committing.

## 6. Commit & push

- Develop on the assigned feature branch — never push to `main` without CI
  green.
- Only create a PR if the user explicitly asks.
- `git push -u origin <branch>`; retry on network errors with backoff.
