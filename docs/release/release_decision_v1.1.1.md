# Release Decision Record — v1.1.1 Targeting

Date: 2026-05-20  
Scope: release governance decision for production publish target

## Decision

- `v1.1.0` is classified as **TestPyPI-only historical evidence** and is **superseded**.
- `v1.1.1` is the **production publish target**.

## Confirmed facts (in-repo)

- Package version SSOT is `src/po_core/__init__.py`; `__version__ = "1.1.1"`.
- Latest public PyPI publication evidence remains `1.0.3` (`docs/release/pypi_publication_v1.0.3.md`).
- `v1.1.0` TestPyPI evidence exists (`docs/release/testpypi_publish_log_v1.1.0.md`) and is historical.
- `v1.1.1` publication evidence is pending:
  - TestPyPI publish evidence: pending
  - PyPI production publish evidence: pending
  - Post-publish smoke evidence: pending

## Guardrails

- Do not claim `v1.1.1` as published on PyPI until publication evidence is recorded.
- Do not re-label `v1.1.0` evidence as `v1.1.1` evidence.
- Keep release wording aligned across status/docs/tests with this decision.
