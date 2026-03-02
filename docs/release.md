# Release Guide

## v1.0.0 readiness check

Use the automated checker before creating a release tag.

```bash
python scripts/check_release_readiness.py --ci-status-file .tmp/ci_status.json
```

The script verifies:

- AT-001〜AT-010 acceptance suite passes
- Required CI jobs (`lint`, `test`, `security`, `build`) are `success`
- `CHANGELOG.md` has an `[Unreleased]` entry
- `docs/spec/output_schema_v1.json` indicates v1.0 (`title` + `meta.schema_version.const=1.0`)

### CI status file format

Either format below is accepted.

```json
{
  "required_jobs": {
    "lint": "success",
    "test": "success",
    "security": "success",
    "build": "success"
  }
}
```

```json
{
  "check_runs": [
    {"name": "lint", "conclusion": "success"},
    {"name": "test", "conclusion": "success"},
    {"name": "security", "conclusion": "success"},
    {"name": "build", "conclusion": "success"}
  ]
}
```
