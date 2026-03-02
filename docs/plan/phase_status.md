# Phase 0 Status Report (Roadmap Sync)

## Scope
- Objective: Synchronize roadmap milestones M1–M4 against current repository state and record evidence for achieved/missing items.
- Note: Direct retrieval of the external roadmap URL (`ROADMAP_FINAL_FORM.md` on branch `claude/define-repo-goals-7zqu6`) failed with HTTP 403 from this environment, so this report uses in-repo spec artifacts as authoritative proxies (`docs/spec/traceability.md`, `docs/spec/prd.md`, acceptance/schema tests, and CI workflow).

## M1–M4 Baseline (from in-repo roadmap proxies)

| Milestone | DoD / deliverables (current repo docs) | Requirement IDs / test anchors |
|---|---|---|
| M1: LLMなしE2E | Stub composer + orchestrator path + AT-001〜AT-010 pass | FR-OUT-001, FR-OPT-001, FR-REC-001; `tests/acceptance/test_acceptance_suite.py` |
| M2: 倫理・責任 v1 | ethics_v1 / responsibility_v1 behavior and tests | FR-ETH-001/002, FR-RES-001 |
| M3: 問いの層 v1 | question_layer behavior and tests | FR-Q-001/002 |
| M4: ガバナンス完成 | CI + PR template + ADR運用 + schema governance gates | NFR-GOV-001 |

## Current-state inventory

### 1) Acceptance tests inventory (`tests/acceptance/`)
- Directory exists: `tests/acceptance/`.
- Acceptance suite exists: `tests/acceptance/test_acceptance_suite.py`.
- AT coverage in file: AT-001〜AT-010 plus cross-cutting AT-META tests.
- Required command result:
  - `pytest tests/acceptance/ -v -m acceptance` → **PASS** (17 passed).

### 2) Golden files inventory and format
- Existing golden files under `scenarios/`: 11 files.
  - `case_001,002,003,006,009,010,011,012,013,014,015` (`*_expected.json`).
- Core frozen/critical files referenced by tests are present:
  - `case_001_expected.json`
  - `case_009_expected.json`
  - `case_010_expected.json`
- Format check evidence:
  - golden files are valid JSON and include expected top-level output object keys (e.g., `meta`, `case_ref`, `options`, `recommendation`, `ethics`, `responsibility`, etc.).

### 3) Schema gate / CI validation
- Output schema file exists: `docs/spec/output_schema_v1.json`.
- Input schema file exists: `docs/spec/input_schema_v1.json`.
- CI includes explicit schema validation test step:
  - `.github/workflows/ci.yml` runs `pytest tests/test_golden_e2e.py tests/test_input_schema.py tests/test_output_schema.py -v`.
- Required command result:
  - `pytest tests/test_output_schema.py -v` → **PASS** (41 passed).

## Milestone status matrix (M1–M4)

| Milestone | Status | Evidence | Gap / next delta |
|---|---|---|---|
| M1 | **達成（実装ベースでは実質達成）** | AT-001〜AT-010 acceptance command passed; schema/meta determinism checks in acceptance suite pass. | If external roadmap defines stricter M1 DoD text, reconcile wording once upstream file is accessible. |
| M2 | **部分達成 / 継続中** | FR-ETH / FR-RES assertions already embedded in AT-002/003/004/005/006/008 and pass. | Need explicit roadmap-parity confirmation against external `ROADMAP_FINAL_FORM.md` definitions. |
| M3 | **部分達成 / 継続中** | FR-Q assertions (AT-009/010) present and passing. | Verify FR-Q-002 suppression behavior and roadmap-specific acceptance criteria alignment. |
| M4 | **部分達成 / 継続中** | CI workflow, PR template, ADR docs exist; schema validation included in CI. | Confirm governance completion criteria (process-level items) against external roadmap text. |

## Evidence log (commands run)

```bash
# external roadmap fetch attempt (failed in this environment)
curl -fsSL https://raw.githubusercontent.com/hiroshitanaka-creator/Po_core/claude/define-repo-goals-7zqu6/ROADMAP_FINAL_FORM.md
# -> curl: (22) The requested URL returned error: 403

# required by Phase 0
pytest tests/acceptance/ -v -m acceptance
pytest tests/test_output_schema.py -v

# inventory / validation helpers
python - <<'PY'
from pathlib import Path
import json
exp=sorted(Path('scenarios').glob('case_*_expected.json'))
print('count',len(exp))
for p in exp:
    obj=json.loads(p.read_text())
    print(p.name, list(obj.keys())[:6])
PY
```
