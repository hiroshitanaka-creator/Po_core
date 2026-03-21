# Release Candidate Operator Handoff for v1.0.3

Purpose: give the maintainer a compact, non-public pre-publish handoff bundle for release candidate `1.0.3` without overstating publication status.

## 1. Machine-verified facts already fixed in-repo

- Repository target version is `1.0.3`.
- Latest public PyPI evidence still points to `1.0.2` via `docs/release/pypi_publication_v1.0.2.md`.
- `pyproject.toml` reads package version dynamically from `src/po_core/__init__.py`.
- Release readiness guardrails exist in `tests/test_release_readiness.py`.
- `docs/status.md` explicitly separates pre-publish candidate truth from post-publish evidence truth.
- `docs/release/smoke_verification_v1.0.3.md` is intentionally a pending placeholder, not publish evidence.

## 2. Operator evidence still required before stronger public claims

Do **not** claim any of the following for `1.0.3` until exact operator evidence is recorded in-repo:

- successful GitHub Actions workflow run URL(s)
- TestPyPI package URL(s) and whether TestPyPI was actually used
- PyPI version page URL for `1.0.3`
- clean-environment install transcript for `po-core-flyingpig==1.0.3`
- clean-environment import transcript showing `po_core.__version__ == "1.0.3"`
- clean-environment smoke transcript for the minimum supported runtime path
- final classification of the publication path: `TestPyPI only` or `TestPyPI + PyPI`

## 3. Local commands/checks that must pass before the real publish

```bash
python scripts/check_dev_dependencies.py
pytest tests/test_release_readiness.py -v
pytest tests/acceptance/ -v -m acceptance
pytest tests/test_output_schema.py -v
pytest tests/test_golden_e2e.py tests/test_input_schema.py -v
pytest tests/ -v
python tools/import_graph.py --check --print
python -m build
twine check dist/*
```

Keep the full dependency-audit and smoke procedure in `docs/operations/publish_playbook.md` as the canonical step-by-step runbook.

## 4. Maintainer stop/go rule

- **Stop:** while evidence remains in this candidate state, public wording must stay limited to “repository target version is `1.0.3`; latest published public version remains `1.0.2`.”
- **Go stronger:** only after operator transcripts, workflow URLs, and a real `1.0.3` PyPI evidence file are fixed in-repo may maintainers say that `1.0.3` was published or smoke-verified.
