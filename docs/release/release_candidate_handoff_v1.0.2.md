# Release Candidate Operator Handoff for v1.0.2

Purpose: give the next maintainer a compact, non-public pre-release handoff bundle for the next release cycle. This file is intentionally shorter than the publish playbook and should be updated with real operator evidence only.

## 1. Machine-verified facts already fixed in-repo

- Repository target version is `1.0.2` and release-facing docs are synced to that version.
- `pyproject.toml` reads package version dynamically from `src/po_core/__init__.py`.
- Release readiness guardrails exist in `tests/test_release_readiness.py`.
- PyPI publication evidence is fixed in `docs/release/pypi_publication_v1.0.2.md`.
- Smoke verification evidence is **not** fixed yet; the current negative placeholder is `docs/release/smoke_verification_v1.0.2.md`.

## 2. Operator evidence still required before stronger public claims

Do **not** claim any of the following until exact operator evidence is recorded in-repo:

- successful GitHub Actions workflow run URL(s)
- TestPyPI package URL(s) and whether TestPyPI was actually used for this release path
- clean-environment install transcript for `po-core-flyingpig==1.0.2`
- clean-environment import transcript showing `po_core.__version__ == "1.0.2"`
- clean-environment smoke transcript for the minimum supported runtime path
- final classification of the publication path: `TestPyPI only` or `TestPyPI + PyPI`

## 3. Local commands/checks that must pass before the next real publish

Run these locally and keep the operator-visible outputs:

```bash
python scripts/check_dev_dependencies.py
pytest tests/test_release_readiness.py -v
pytest tests/acceptance/ -v -m acceptance
pytest tests/test_output_schema.py -v
pytest tests/test_golden_e2e.py tests/test_input_schema.py -v
pytest tests/ -v
bandit -r src/ scripts/ -c pyproject.toml
python -m build
twine check dist/*
```

Also run the clean-environment dependency audit loop and the release smoke procedure from `docs/operations/publish_playbook.md`; those commands stay canonical there to avoid copy drift.

## 4. Evidence capture checklist for the operator

Fill or append evidence files with exact values only:

- [ ] workflow run URL(s)
- [ ] commit SHA used for publish
- [ ] TestPyPI URL(s), if applicable
- [ ] PyPI URL(s)
- [ ] exact install/import/smoke commands
- [ ] exact stdout/stderr transcripts
- [ ] any rollback or follow-up action taken

## 5. Maintainer stop/go rule

- **Stop:** if only public PyPI page evidence exists, public wording must stay limited to "published on PyPI".
- **Go stronger:** only after operator transcripts and workflow URLs are fixed in-repo may maintainers say that publish workflow execution and post-publish smoke verification were completed.
