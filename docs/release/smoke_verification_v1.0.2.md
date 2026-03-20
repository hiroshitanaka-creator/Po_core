# Smoke Verification Evidence for v1.0.2

- Evidence status: **operator-supplied transcript not yet recorded in this repository**
- Why this file exists: `1.0.2` is evidenced as published on PyPI, but that fact does not cross the full release evidence boundary by itself. The repository still needs the human operator's clean install/import/smoke transcript before claiming post-publish smoke verification.

## Required operator values (not supplied in this task)

- workflow run URL(s)
- package URL(s) used during verification
- exact install command(s)
- exact import command(s)
- exact smoke command(s)
- exact stdout/stderr output
- exact publication result: `TestPyPI only` or `TestPyPI + PyPI`

## Current verified state

- Verified from public evidence: PyPI version page exists for `po-core-flyingpig 1.0.2`.
- Not yet fixed as truth in this file: clean-environment install/import/smoke success.
- Boundary note: this file stays intentionally negative until the operator transcript exists; for the canonical wording used in public docs, see `docs/status.md`.

## Promotion rule

Do not update public docs to say that post-publish smoke verification passed until the operator transcript is pasted here verbatim (or into a sibling evidence file) with real URLs and real command output.
