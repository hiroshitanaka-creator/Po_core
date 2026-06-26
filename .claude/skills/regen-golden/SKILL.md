---
name: regen-golden
description: Regenerate and verify acceptance golden JSON files from scenario YAML deterministically. Use when acceptance tests fail on golden diffs, or after an intentional, spec-backed change to output. Enforces ADR-0002 / ADR-0011 / ADR-0012 (golden updates need a stated spec reason).
---

# Regenerate Golden Files

Golden files are the canonical E2E contract (ADR-0002: full canonical-JSON
match). They may only be regenerated **via the script**, never hand-edited,
and only with a stated specification reason (ADR-0011, ADR-0012).

## Before regenerating — gate yourself

A golden diff is a RED FLAG, not a chore. Confirm first:

1. Is the output change **intended** and backed by spec/ADR/requirement?
   - If NO → this is a regression. Fix the code, do not regenerate.
   - If YES → note which requirement/ADR justifies it (needed for the PR;
     `check-governance` skill enforces requirement-ID references).
2. For `policy_v1` constant changes → ADR-0012 requires `policy_lab`
   evidence + `impacted_requirements` + this regen procedure.

## Regenerate

Use the deterministic regenerator (fixed seed + injected `now`, per ADR-0003):

```bash
# One scenario
python regenerate_golden.py tests/acceptance/scenarios/<case>.yaml

# Multiple
python regenerate_golden.py tests/acceptance/scenarios/*.yaml
```

Defaults: `--seed 0 --now 2026-02-22T00:00:00Z --deterministic`. Keep these
unless a scenario explicitly overrides them — changing seed/now silently
breaks the determinism contract.

Each run writes `<case>_expected.json` next to the scenario.

## Verify

```bash
pytest tests/acceptance/ -v
```

All scenarios must pass. Then:

- Review the golden diff and confirm every change is explained by the
  intended behavior change — no unexpected fields moved.
- Run the `update-status` skill to log the change.
