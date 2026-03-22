# Baseline Truth (Phase A Freeze)

> Purpose: Record what the repo claims as of HEAD. This is the "what repo says" record,
> not independently verified truth. Each claim has file path + exact snippet.
> All rerun verification is in Phase C / E.

Audit date: 2026-03-22
Audit branch: claude/audit-po-core-v1.0.3-FaZVy
HEAD commit: 39803f8 (docs(release): record Phase 6 pre-publish evidence for v1.0.3 (#506))

---

## 1. Repo Target Version

**Source:** `src/po_core/__init__.py` line 14 (version SSOT)
```python
__version__ = "1.0.3"
```

**Source:** `docs/status.md` line 11
```
- Repository target version: `1.0.3`
```

**Source:** `pyproject.toml` lines 148-149 (dynamic read)
```toml
[tool.setuptools.dynamic]
version = {attr = "po_core.__version__"}
```

**Conclusion:** repo target version = `1.0.3`. Package name = `po-core-flyingpig`.

---

## 2. Latest Published Public Version

**Source:** `docs/status.md` line 12
```
- Latest published public version: `1.0.2`
```

**Source:** `docs/release/pypi_publication_v1.0.2.md` lines 1-8
```markdown
# PyPI Publication Evidence for v1.0.2
- Evidence recorded at (UTC): 2026-03-20T00:00:00Z
- Evidence source: public PyPI release page
- Package: `po-core-flyingpig`
- Version: `1.0.2`
- Publication result evidenced here: **PyPI published**
```
PyPI URL claimed: https://pypi.org/project/po-core-flyingpig/1.0.2/

**Classifier discrepancy (baseline flag):**
- `pyproject.toml` line 29: `"Development Status :: 4 - Beta"`
- `docs/release/pypi_publication_v1.0.2.md` line 23: `classifier evidence: Development Status :: 5 - Production/Stable`
- These do NOT match. The repo has `4-Beta` but the PyPI evidence doc claims the live page shows `5-Production/Stable`.
  This is noted as a potential defect candidate (docs drift or incorrect evidence capture). Verification requires
  checking live PyPI page — not possible in read-only audit.

---

## 3. Packaging Boundary

**Source:** `pyproject.toml` lines 139-145
```toml
[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
include = ["po_core*"]
namespaces = false
```

- Packaged runtime: `src/po_core` (and any sub-packages matching `po_core*`)
- Legacy path: `src/pocore` — NOT explicitly included in packaging boundary
  (only `po_core*` is included; `pocore` does not match `po_core*`)
- Package-data included: `config/*.yaml`, `config/**/*.yaml`, `axis/specs/*.json`,
  `schemas/*.json`, `viewer/*.html`, `py.typed`

**Source:** `pyproject.toml` lines 151-160
```toml
[tool.setuptools.package-data]
po_core = [
    "config/*.yaml",
    "config/*/*.yaml",
    "config/*/*/*.yaml",
    "axis/specs/*.json",
    "schemas/*.json",
    "viewer/*.html",
    "py.typed",
]
```

---

## 4. Published / Pre-publish Truth Boundary

**Source:** `docs/status.md` lines 17-19
```
- External publish status: **published on PyPI for `1.0.2`**
- Canonical evidence boundary: the latest published public version can remain `1.0.2` until
  `1.0.3` is actually published.
```

**Source:** `docs/release/smoke_verification_v1.0.3.md` lines 1-11
```markdown
# Smoke Verification Evidence for v1.0.3
- Version: `1.0.3`
- Evidence status: **local pre-publish smoke — PASSED (2026-03-22)**
- Post-publish operator-supplied transcript not yet recorded in this repository
- Current state: **pre-publish candidate state**
```

**Source:** `docs/release/release_candidate_handoff_v1.0.3.md` lines 43-45
```markdown
- **Stop:** while evidence remains in this candidate state, public wording must stay limited to
  "repository target version is `1.0.3`; latest published public version remains `1.0.2`."
- **Go stronger:** only after operator transcripts, workflow URLs, and a real `1.0.3` PyPI
  evidence file are fixed in-repo.
```

**Conclusion:**
- `1.0.2`: PUBLISHED on PyPI (evidence fixed in repo)
- `1.0.3`: PRE-PUBLISH CANDIDATE ONLY. No TestPyPI URL, no PyPI URL, no workflow run URL in repo.

---

## 5. Phase 6 Repo-recorded Gate Claims (from smoke_verification_v1.0.3.md)

The following was recorded (from docs/release/smoke_verification_v1.0.3.md) as passing on 2026-03-22:

| Gate | Claimed result |
|------|---------------|
| `pytest tests/test_release_readiness.py -v` | 24/24 passed |
| `pytest tests/acceptance/ -v -m acceptance` | 43/43 passed |
| `pytest tests/test_output_schema.py tests/test_golden_e2e.py tests/test_input_schema.py -v` | 103/103 passed |
| `pytest tests/ -v` (full suite) | 3868/3869 passed (1 flaky benchmark timing) |
| `python tools/import_graph.py --check --print` | violations=0, cycles=0 |
| `bandit -r src/ scripts/ -c pyproject.toml` | High=0, Medium=3 (non-critical) |
| `python -m build` | PASSED |
| `twine check dist/*` | PASSED |
| `scripts/release_smoke.py --check-entrypoints` | all passed |

**Status: These are BASELINE CLAIMS only. They must be independently verified in Phase C.**

---

## 6. PR #504 Merge Metadata

From `git log`:
```
e3bea8a docs(release): record Phase 6 pre-publish evidence for v1.0.3 (#504)
```
Also present on same branch:
```
5678d2d docs(release): record Phase 6 pre-publish evidence for v1.0.3 (#505)
39803f8 docs(release): record Phase 6 pre-publish evidence for v1.0.3 (#506)
```

Note: Three consecutive merges with identical title pattern (PR #504, #505, #506). All are
"record Phase 6 pre-publish evidence" commits. PR body was noted as template-unfilled;
merge metadata only is used as baseline. The repeated merge pattern is unusual and will be
investigated in Phase D.

---

## 7. Console Scripts (entrypoints)

**Source:** `pyproject.toml` lines 132-137
```toml
[project.scripts]
po-core = "po_core.cli.commands:main"
po-self = "po_core.po_self:cli"
po-trace = "po_core.po_trace:cli"
po-interactive = "po_core.cli.interactive:main"
po-experiment = "po_core.cli.experiment:main"
```

5 console scripts claimed. All must resolve at install time.

---

## 8. Public API Exports

**Source:** `src/po_core/__init__.py` lines 20-43
```python
def run(*args, **kwargs):
    from po_core.app.api import run as _run
    return _run(*args, **kwargs)

from po_core.ensemble import PHILOSOPHER_REGISTRY
from po_core.po_self import PoSelf, PoSelfResponse
from po_core.po_trace import EventType, PoTrace

__all__ = [
    "__version__", "run",
    "PHILOSOPHER_REGISTRY",
    "PoTrace", "EventType",
    "PoSelf", "PoSelfResponse",
]
```

---

## 9. Development Status Discrepancy (baseline flag)

| Source | Claimed classifier |
|--------|-------------------|
| `pyproject.toml` line 29 | `Development Status :: 4 - Beta` |
| `docs/release/pypi_publication_v1.0.2.md` line 23 | `Development Status :: 5 - Production/Stable` (on live PyPI) |

This is a discrepancy between packaging metadata and what was reportedly on PyPI for `1.0.2`.
Either the pyproject.toml was downgraded after publishing 1.0.2, or the evidence capture is wrong.
**Cannot verify without live PyPI access. Flagged as defect candidate.**

---

## 10. Key Pending Evidence Gaps (as stated by the repo itself)

From `docs/status.md` lines 38-43:
```
1. TestPyPI publication の有無と URL が `1.0.3` では未固定。
2. PyPI publication page evidence が `1.0.3` では未固定。
3. 公開後 smoke の operator transcript が `1.0.3` では未固定。
4. trusted publishing / release run の具体的 workflow URL が `1.0.3` では未記録。
```

**These gaps are acknowledged by the repo itself. They are not new findings at this stage.**
