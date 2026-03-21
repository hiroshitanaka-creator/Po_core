# Smoke Verification Evidence for v1.0.3

- Version: `1.0.3`
- Evidence status: **operator-supplied transcript not yet recorded in this repository**
- Current state: **pre-publish candidate state**
- Why this file exists: `1.0.3` is the repository target version, but no publication or post-publish smoke evidence has been fixed in-repo yet.

## Required operator values (not supplied in this task)

- workflow run URL(s)
- package URL(s) used during verification
- exact install command(s)
- exact import command(s)
- exact smoke command(s)
- exact stdout/stderr output
- exact publication result: `TestPyPI only` or `TestPyPI + PyPI`

## Current verified state

- Verified from repository truth: `src/po_core/__init__.py` targets `1.0.3`.
- Verified from repository truth: release-facing docs describe `1.0.3` as a pre-publish candidate, not as a published release.
- Not yet fixed as truth in this file: TestPyPI publication, PyPI publication, clean-environment install/import/smoke success.

## Promotion rule

Do not update public docs to say that `1.0.3` was published or post-publish smoke verification passed until the operator transcript and exact evidence URLs are pasted here verbatim (or into sibling evidence files) with real values.
