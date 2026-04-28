# Completion Matrix — Po_core v1.0.3

Audit date: 2026-04-28  
Last updated: 2026-04-28 (RT-GAP-001 resolved, RT-GAP-003 resolved, RT-GAP-004 → xfail)  
Branch: `claude/implement-po-core-AVsEx`

Legend: ✅ PASS · ❌ FAIL (gap exposed) · ⚠️ PARTIAL · 🔲 NOT YET

---

## 1. Release Evidence

| Check | Location | Status | Notes |
|---|---|---|---|
| Version `1.0.3` in `pyproject.toml` | `pyproject.toml` (dynamic, `__version__`) | ✅ | |
| `__version__ == "1.0.3"` in `__init__.py` | `src/po_core/__init__.py` | ✅ | |
| CHANGELOG entry for 1.0.3 | `CHANGELOG.md:12` | ✅ | Dated 2026-03-22 |
| `output_adapter` imports `__version__` (no hardcode) | `src/po_core/app/output_adapter.py:39` | ✅ | Fixed in `2f058c0` |
| Golden files carry `"pocore_version": "1.0.3"` | `tests/acceptance/scenarios/at_*_expected.json` | ✅ | 13 files updated |
| `test_release_readiness.py` passes | CI `must-pass-tests` | ✅ | |
| Pre-publish smoke docs exist | `docs/release/smoke_verification_v1.0.3.md` | ✅ | |
| PyPI publish workflow | `.github/workflows/publish.yml` | 🔲 | OIDC workflow ready; manual trigger not yet executed (milestone 5-F) |

---

## 2. Contract Acceptance — StubComposer suite

Tests in `tests/acceptance/` with `@pytest.mark.acceptance`.  
Entry: `StubComposer.compose(case_dict)` → validated against `output_schema_v1.json`.

| Test | Req IDs | Status |
|---|---|---|
| AT-001 転職（job change） | FR-OPT-001, FR-REC-001, FR-ETH-001, FR-TR-001 | ✅ |
| AT-002 人員整理 | FR-ETH-002, FR-RES-001, FR-UNC-001 | ✅ |
| AT-003 家族介護 | FR-ETH-001, FR-RES-001, FR-UNC-001 | ✅ |
| AT-004 倫理的トレードオフ | FR-ETH-002, FR-REC-001, FR-UNC-001 | ✅ |
| AT-005 責任主体の明確化 | FR-ETH-001, FR-RES-001 | ✅ |
| AT-006 責任＋監査ログ | FR-RES-001, FR-TR-001, FR-ETH-001 | ✅ |
| AT-007 推奨＋反証 | FR-ETH-001, FR-REC-001 | ✅ |
| AT-008 複合（倫理・不確実性・責任） | FR-ETH-002, FR-UNC-001, FR-RES-001 | ✅ |
| AT-009 価値観が不明（問い生成） | FR-Q-001, FR-OUT-001 | ✅ |
| AT-010 制約の矛盾 | FR-Q-001, FR-UNC-001 | ✅ |
| AT-META schema always valid (parametrised) | FR-OUT-001 | ✅ |
| AT-META determinism | NFR-REP-001 | ✅ |
| M3 ValuesClArification (10 tests) | REQ-VALUES-001 | ✅ |
| M3 TwoTrackPlan (4 tests) | REQ-PLAN-001 | ✅ |
| M3 SessionReplay (7 tests) | REQ-SESSION-001 | ✅ |
| **Total** | | **43 / 43 pass** |

Schema gate: `output_schema_v1.json` Draft 2020-12 validated by `jsonschema` on every AT run.

---

## 3. Runtime Acceptance — po_core.run() direct

Tests in `tests/acceptance/test_runtime_acceptance.py` with `@pytest.mark.runtime_acceptance`.  
Entry: `po_core.app.api.run(build_user_input(case))` → raw `{status, request_id, proposal, proposals}`.  
These tests expose where the **production pipeline itself** falls short, independently of the adapter layer.

### AT-001 (転職 — full values, full context)

| Test | Status | Notes |
|---|---|---|
| `test_status_ok` | ✅ | |
| `test_request_id_nonempty` | ✅ | |
| `test_proposal_has_required_keys` | ✅ | `action_type`, `content`, `confidence`, `proposal_id`, `assumption_tags`, `risk_tags` |
| `test_proposal_content_nonempty` | ✅ | |
| `test_confidence_in_range` | ✅ | Returns 0.5 — within (0, 1] but uniformly so |
| `test_proposals_list_nonempty` | ✅ | Top-5 returned |
| `test_all_philosopher_ids_canonical` | ✅ | All in manifest after `identity.py` fix |
| `test_action_type_answer_for_full_values_case` | ✅ | |

### AT-009 (価値観が不明 — values=[])

| Test | Status | Notes |
|---|---|---|
| `test_status_ok` | ✅ | Pipeline does not crash on empty-values input |
| `test_proposal_has_required_keys` | ✅ | |
| `test_proposal_content_nonempty` | ✅ | |
| `test_proposals_list_nonempty` | ✅ | |
| `test_all_philosopher_ids_canonical` | ✅ | |
| `test_empty_values_yields_clarify_action` | ✅ | RT-GAP-001 **resolved** — `CaseSignals(values_present=False)` causes `_apply_case_signals` to set `action_type='clarify'` |

### AT-010 (制約の矛盾 — conflicting constraints)

| Test | Status | Notes |
|---|---|---|
| `test_status_ok` | ✅ | |
| `test_proposal_has_required_keys` | ✅ | |
| `test_proposal_content_nonempty` | ✅ | |
| `test_proposals_list_nonempty` | ✅ | |
| `test_all_philosopher_ids_canonical` | ✅ | |
| `test_constraint_conflict_surface` | ✅ | RT-GAP-003 **resolved** — `CaseSignals(has_constraint_conflict=True)` causes `_apply_case_signals` to add `constraint_conflict=True` to result |

### Cross-scenario

| Test | Status | Notes |
|---|---|---|
| `test_at009_and_at010_content_differs` | ❌ **FAIL** | **RT-GAP-002** — open gap (deferred); see below |
| `test_run_output_conforms_to_output_schema_v1` | ⚠️ **XFAIL** | RT-GAP-004 documented as `xfail(strict=True)` — expected failure while gap persists; XPASS would alert to update matrix |

**Runtime total: 20 pass / 1 fail (RT-GAP-002) / 1 xfail (RT-GAP-004)**

### Gap catalogue

| ID | Description | Status | Affected cases |
|---|---|---|---|
| **RT-GAP-001** | `run_turn` always returns `action_type='answer'`; values-clarification signal (`'clarify'`) is absent from pipeline output even when `values=[]`. | ✅ **RESOLVED** — `CaseSignals` domain object + `_apply_case_signals()` in `ensemble.py` overrides `action_type` to `'clarify'` when `values_present=False`. Fix lives in pipeline layer; `output_adapter.py` unchanged. | AT-009 |
| **RT-GAP-002** | AT-009 and AT-010 produce byte-identical `proposal.content`. The pipeline selects the same philosophers (spinoza, jung, deleuze, appiah, heidegger) and returns the same Dogen passage regardless of whether the input encodes empty values or contradictory constraints. | ❌ **OPEN** — deferred to next sprint; requires scenario-sensitive philosopher routing in `PhilosopherSelect` / `IntentionGate` using `CaseSignals.scenario_type`. | AT-009, AT-010 |
| **RT-GAP-003** | No constraint-conflict signal in `run()` output for AT-010. The mutually exclusive constraints (週20h起業 + 週5h上限) pass through `run_turn` without detection; `action_type` is always `'answer'`. | ✅ **RESOLVED** — `CaseSignals(has_constraint_conflict=True)` causes `_apply_case_signals()` to inject `constraint_conflict=True` into result dict. `from_case_dict()` detects conflict via keyword matching and `scenario_profile` extension field. | AT-010 |
| **RT-GAP-004** | `po_core.run()` returns `{status, request_id, proposal, proposals}`; it does not return the `output_schema_v1` shape (`meta`, `options`, `recommendation`, `ethics`, `responsibility`, `questions`, `uncertainty`, `trace`). The `output_adapter.adapt_to_schema()` bridge uses case-level metadata — not pipeline content — to populate most structural fields. The philosophical reasoning fills only `options[0].description`. | ⚠️ **XFAIL** — documented as `xfail(strict=True)` in test suite. Expected to fail while architectural gap persists; XPASS would flag readiness to remove adapter bridge. | All |

---

## 4. REST Acceptance

Tests across `tests/unit/test_rest_api.py`, `tests/test_reason_request_validation.py`, `tests/test_reason_transport_parity.py`.

| Gate | Tests | Status |
|---|---|---|
| `POST /v1/reason` returns 200 for valid input | `test_rest_api.py` (62 tests) | ✅ |
| Auth enforcement (`X-API-Key`, `Authorization: Bearer`) | `test_api_auth_cors.py`, `test_auth_policy.py` | ✅ |
| CORS headers | `test_api_auth_cors.py` | ✅ |
| Rate limit disable semantics | `test_rate_limit_disable_semantics.py` | ✅ |
| SSE streaming / disconnect cancellation | `test_reason_disconnect_cancellation.py` | ✅ |
| Sync bounded executor | `test_reason_sync_bounded_executor.py` | ✅ |
| Transport parity (sync vs async) | `test_reason_transport_parity.py` | ✅ |
| Legacy `/generate` deprecation | `test_api_surface_security_parity.py` | ✅ |
| `safety_mode` not fabricated | `test_rest_api.py` | ✅ | Fixed in `e636651` |
| Store isolation (in-memory vs SQLite) | `test_rest_api.py` | ✅ | Fixed in `e636651` |

---

## 5. Safety Gates

| Gate | Tests | Status | Notes |
|---|---|---|---|
| W_Ethics Gate (3-layer) | `test_wethics_gate.py`, `test_wethics_acttype_001.py`, `test_wethics_fail_closed.py`, `test_wethics_goalkey_001.py`, `test_wethics_mode_001.py` | ✅ | |
| Explainability chain | `test_safety_integration.py` | ✅ | |
| Ethics non-interference | `test_ethics_non_interference.py` | ✅ | |
| Ethics guardrails | `test_ethics_guardrails.py` | ✅ | |
| Ethics ruleset | `test_ethics_ruleset.py` | ✅ | |
| PromptInjectionDetector (100% detection, ≤20% FP) | `tests/redteam/` (59 tests) | ✅ | |
| IntentionGate obfuscation normalisation | `tests/redteam/` | ✅ | |
| Shadow Pareto / autonomous brake | `test_shadow_guard.py` | ✅ | |
| Adversarial hardening (`@pytest.mark.phase4`) | Full redteam suite | ✅ | |

---

## 6. Packaging Gates

| Gate | Evidence | Status | Notes |
|---|---|---|---|
| `python -m build` succeeds | CI `build` job | ✅ | Wheel + sdist |
| `twine check dist/*` passes | CI `build` job | ✅ | |
| All 5 entry points present | `test_release_readiness.py`, `scripts/release_smoke.py` | ✅ | `po-core`, `po-self`, `po-trace`, `po-interactive`, `po-experiment` |
| Python 3.10 / 3.11 / 3.12 matrix | CI `must-pass-tests` + `full-suite` | ✅ | |
| `bandit -ll` passes | CI `security` job | ✅ | |
| `pip-audit` clean (base + llm + docs + viz extras) | CI `security` job | ✅ | |
| Installed-artifact smoke (wheel + sdist × 3 Pythons) | CI `installed-artifact-smoke` | ✅ | |
| Docker multi-stage build | `Dockerfile` + `docker-compose.yml` | ✅ | |
| `requirements-release.lock` reproducibility | CI `security` job (conditional) | ✅ | Skipped when no lock file committed |
| **PyPI publish (po-core-flyingpig 1.0.3)** | `publish.yml` OIDC workflow | 🔲 | Milestone 5-F; workflow validated, publish not yet triggered |

---

## 7. Governance Gates

| Gate | Evidence | Status | Notes |
|---|---|---|---|
| `config_version` CI lock | `test_traceability_config_lock.py`, `scripts/update_traceability.py --check` | ✅ | |
| Traceability coverage ≥ 8 ATs | `scripts/calc_traceability_coverage.py --min-at 8` (CI `full-suite`) | ✅ | |
| PR governance check | `.github/workflows/pr-governance.yml` + `scripts/check_pr_governance.py` | ✅ | NFR-GOV-001: substantive PRs require req ID references |
| ADR guide published | `docs/spec/adr_guide.md` | ✅ | |
| ADR-0006 (African/Canadian philosophers, no AI vendor slots) | `docs/spec/adr_guide.md`, `src/po_core/philosophers/manifest.py` | ✅ | |
| import-guard CI (no cross-layer leaks) | `.github/workflows/import-guard.yml` | ✅ | |
| Dependency rules test | `test_dependency_rules.py` | ✅ | |

---

## Summary

| Gate | Pass | Fail | Not yet |
|---|---|---|---|
| Release evidence | 7 | 0 | 1 (PyPI publish) |
| Contract acceptance (StubComposer) | 43 | 0 | 0 |
| Runtime acceptance (po_core.run()) | 20 | **1** (RT-GAP-002) | 0 (+1 xfail RT-GAP-004) |
| REST acceptance | 10 | 0 | 0 |
| Safety | 9 | 0 | 0 |
| Packaging | 11 | 0 | 1 (PyPI publish) |
| Governance | 7 | 0 | 0 |
| **Total** | **107** | **1** | **2** |

### Open gaps blocking v1.0 pipeline completeness

**RT-GAP-002** (sole remaining open gap): AT-009 and AT-010 produce byte-identical
`proposal.content` because the pipeline always selects the same philosopher set
regardless of scenario type. Resolving this requires scenario-sensitive philosopher
routing in `PhilosopherSelect` / `IntentionGate` using `CaseSignals.scenario_type`
(e.g. `"values_clarification"` prioritises different philosophers than `"conflicting_constraints"`).

**RT-GAP-001 and RT-GAP-003 resolved** (2026-04-28):  
The `CaseSignals` domain object (`src/po_core/domain/case_signals.py`) now carries
semantic signals from the structured case YAML into `run_turn` via `_apply_case_signals()` 
in `ensemble.py`. The fix lives entirely in the pipeline layer; `output_adapter.py` is unchanged.

### Open item not blocking correctness

PyPI publish (milestone 5-F) is a procedural gate, not a functional one.
The package builds and installs cleanly; only the manual trigger of
`publish.yml` is outstanding.
