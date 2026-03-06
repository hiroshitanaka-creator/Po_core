# Po_core Repository Structure

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE)

**Document Status:** v2.0 — Reflects actual production state (Phase 5 complete)
**Last Updated:** 2026-02-28
**Package Version:** `po-core-flyingpig` v0.3.0

> This document describes the **actual** repository structure as of Phase 5 completion.
> It replaces the earlier planning document (v1.0, 2025-11-02).

---

## Repository Root Structure

```
Po_core/
│
├── .github/                          # GitHub configuration
│   ├── workflows/
│   │   ├── ci.yml                   # Main CI pipeline (lint + test + security + build)
│   │   ├── import-guard.yml         # Import dependency enforcement
│   │   ├── policy_lab.yml           # Policy lab automation
│   │   └── publish.yml              # PyPI OIDC trusted publishing (TestPyPI / PyPI)
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.yml
│       ├── feature_request.yml
│       ├── good_first_issue.yml
│       ├── philosopher_enhancement.yml
│       └── config.yml
│
├── 01_specifications/               # System specification documents
│   ├── Po_core_spec_doc_v1.0_English.md
│   ├── Po_core_spec_doc_v1.0_japanese.md
│   ├── README_01_specifications_English.md
│   ├── README_01_specifications_japanese.md
│   └── wethics_gate/                # W_Ethics Gate sub-specs
│
├── 02_architecture/                 # Architecture documents
│   ├── philosophy/
│   └── tensors/
│
├── 03_api/                          # API documentation
│
├── 04_modules/                      # Module-level documentation
│   ├── Po_self/
│   ├── output_rendering/
│   ├── po_trace/
│   ├── reason_log/
│   └── viewer/
│
├── 05_research/                     # Research papers and analyses
│   └── README_05_research_en.md
│
├── docs/                            # Extended documentation
│   ├── adr/                         # Architecture Decision Records (ADR 0001–0005)
│   ├── experiments/                 # Experiment notes
│   ├── papers/                      # Academic paper materials
│   ├── spec/                        # Machine-spec documents (M0 milestone)
│   │   ├── prd.md                   # Product Requirements Document v0.3
│   │   ├── srs_v0.1.md              # Software Requirements Specification v0.3
│   │   ├── output_schema_v1.json    # Output schema contract (FR-OUT-001)
│   │   ├── input_schema_v1.json     # Input schema
│   │   ├── session_answers_schema_v1.json
│   │   ├── session_answers_v1.md
│   │   ├── features_v1.md
│   │   ├── principles_v1.md
│   │   ├── requirements_v1.md
│   │   ├── test_cases.md            # Acceptance test specs (AT-001–AT-010+)
│   │   └── traceability.md          # Req ↔ impl ↔ test traceability matrix
│   ├── specifications/
│   ├── traceability/
│   ├── viewer/
│   ├── LOCAL_LLM_GUIDE.md
│   ├── MANUAL_LLM_TESTING.md
│   ├── SAFETY.md
│   ├── TUTORIAL.md
│   └── VISUALIZATION_GUIDE.md
│
├── examples/                        # Usage examples
│   ├── basic/                       # Beginner examples
│   ├── PO_PARTY.md
│   └── README.md
│
├── experiments/                     # Experimental code and configs
│   ├── adversarial/
│   ├── configs/
│   └── results/
│       └── darkpattern_review/
│
├── papers/                          # Academic papers and drafts
│   ├── Po_core_Academia_Paper.md
│   └── arxiv_paper_draft.md        # arXiv preprint draft
│
├── po-synthetic-thought-architect-lite/  # Lightweight variant
│   ├── examples/
│   ├── notes/
│   └── prompt/
│
├── reports/                         # Policy lab reports
│   └── policy_lab/
│
├── scenarios/                       # Acceptance test scenarios (case_001–case_015)
│   ├── case_001.yaml                # 転職：安定企業→スタートアップ
│   ├── case_001_expected.json
│   ├── case_002.yaml                # 人員整理の判断
│   ├── case_002_expected.json
│   ├── case_003.yaml                # 家族介護の設計
│   ├── case_003_expected.json
│   ├── case_004.yaml
│   ├── case_005.yaml
│   ├── case_006.yaml                # ＋expected
│   ├── case_007.yaml
│   ├── case_008.yaml
│   ├── case_009.yaml                # 価値観が不明（問い生成必須）
│   ├── case_009_expected.json
│   ├── case_010.yaml                # 制約の矛盾
│   ├── case_010_expected.json
│   ├── case_011.yaml  ➜  case_015.yaml  # Additional scenarios
│   └── case_011_expected.json ➜ case_015_expected.json
│
├── scripts/                         # Utility scripts
├── sessions/                        # Session data
├── src/                             # Production source code
│   ├── po_core/                     # Main package (po-core-flyingpig)
│   │   └── [see §src/po_core/ below]
│   └── pocore/                      # Legacy namespace shim
│       └── engines/
│
├── tests/                           # Full test suite (2400+ tests)
│   ├── benchmarks/                  # Performance benchmarks
│   ├── experiments/
│   ├── fixtures/
│   ├── integration/
│   ├── redteam/                     # Adversarial / red-team tests
│   ├── unit/                        # Unit tests
│   │   ├── test_philosophers/
│   │   └── [60+ test files]
│   ├── acceptance/                  # Acceptance tests (AT-001–AT-010) [M1]
│   │   ├── conftest.py
│   │   └── test_acceptance_suite.py
│   └── [70+ top-level test files]
│
├── tools/                           # Developer tools
│
│── # ─── Root-level files ────────────────────────────────────
│
├── AGENTS.md                        # AI agent instructions
├── CHANGELOG.md                     # Version history
├── CLAUDE.md                        # Claude Code session context
├── CODE_OF_CONDUCT.md               # Community standards
├── COMMERCIAL_LICENSE.md            # Commercial use terms
├── CONTRIBUTING.md                  # Contribution guidelines
├── Dockerfile                       # Multi-stage Docker image (builder + slim runtime)
├── GRAND_ARCHITECT_ASSESSMENT.md    # Architecture assessment
├── ISSUES.md                        # Issue tracking notes
├── LICENSE                          # GNU AGPLv3
├── License.md                       # License summary
├── NEXT_STEPS.md
├── PHASE_PLAN_v2.md                 # Phase 1–5 rationale and planning
├── Po_core_spec_doc_v1.0.md         # Full spec document (root copy)
├── PROJECT_SUMMARY.md
├── QUICKSTART.md                    # Japanese quickstart
├── QUICKSTART_EN.md                 # English quickstart
├── README.md                        # Project overview + badges
├── REPOSITORY_STRUCTURE.md         # This file
├── docker-compose.yml               # Docker Compose (named volumes, health check)
├── .coveragerc
├── .dockerignore
├── .env.example                     # Environment variable reference
├── .flake8
├── .gitattributes
├── .gitignore
├── .markdownlint.json
├── .markdownlintignore
├── .pre-commit-config.yaml
├── pyproject.toml                   # PEP 517/518 packaging (po-core-flyingpig v0.3.0)
├── pytest.ini                       # Pytest configuration + markers
├── regenerate_golden.py             # Golden file regeneration script
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Development dependencies
└── setup.py                         # Legacy setup shim
```

---

## `src/po_core/` — Source Code

```
src/po_core/
├── __init__.py                      # Package entry (re-exports run, PoSelf, etc.)
├── ensemble.py                      # run_turn pipeline orchestrator (10-step hexagonal)
├── party_machine.py                 # Philosopher combination assembly + AsyncPartyMachine
├── po_self.py                       # PoSelf: high-level wrapper for generate()
├── po_viewer.py                     # PoViewer: trace/explanation visualization
├── po_system_prompt.py              # System prompt builder
├── po_trace.py                      # Trace utilities
├── po_trace_db.py                   # DB-backed tracing
├── database.py                      # SQLite/SQLAlchemy setup
├── visualizations.py                # Matplotlib/Plotly helpers
├── tensor_metrics.py               # Tensor metric calculations
├── runner.py                        # CLI runner helpers
├── cli.py                           # CLI entry point (typer)
├── py.typed                         # PEP 561 type marker
│
├── app/                             # Delivery adapters (REST + public API)
│   ├── api.py                       # po_core.run() — recommended public entry point
│   ├── composer.py                  # StubComposer: rule-based output generator [M1]
│   └── rest/                        # FastAPI REST layer (Phase 5)
│       ├── server.py                # FastAPI app factory
│       ├── config.py                # APISettings (pydantic-settings, PO_ env vars)
│       ├── auth.py                  # X-API-Key authentication
│       ├── rate_limit.py            # SlowAPI rate limiting
│       ├── models.py                # Pydantic request/response models
│       ├── store.py                 # In-process trace store
│       ├── __main__.py              # uvicorn entry point
│       └── routers/                 # 5 route handlers
│           ├── reason.py            # POST /v1/reason
│           ├── stream.py            # POST /v1/reason/stream (SSE)
│           ├── philosophers.py      # GET /v1/philosophers
│           ├── trace.py             # GET /v1/trace/{session_id}
│           └── health.py            # GET /v1/health
│
├── philosophers/                    # 39 philosopher modules
│   ├── manifest.py                  # Philosopher registry + risk levels (0/1/2)
│   └── [39 philosopher .py files]  # aristotle, arendt, camus, confucius, …
│
├── tensors/                         # Tensor computation layer
│   ├── engine.py                    # TensorEngine (main entry point)
│   ├── freedom_pressure_v2.py       # FreedomPressure 6D ML tensor
│   └── metrics/
│       ├── freedom_pressure.py
│       ├── semantic_delta.py        # Multi-backend: sbert / tfidf / basic
│       └── blocked_tensor.py
│
├── safety/                          # W_Ethics Gate (3-layer ethical filter)
│   ├── fallback.py
│   ├── policy_scoring.py
│   └── wethics_gate/
│       ├── gate.py                  # WEthicsGate: W0–W4 orchestrator
│       ├── intention_gate.py        # W1: structural exclusion + obfuscation normalization
│       ├── action_gate.py           # W2/W3: action-level ethical check
│       ├── detectors.py             # PromptInjectionDetector + EnglishKeywordViolation v0.2
│       ├── explanation.py           # ExplanationChain + build_explanation_from_verdict()
│       └── [rule sets]
│
├── aggregator/                      # Pareto aggregation layer
│   ├── pareto.py                    # ParetoAggregator
│   ├── conflict_resolver.py
│   ├── policy_aware.py
│   └── weighted_vote.py
│
├── deliberation/                    # Multi-round philosopher dialogue
│   └── engine.py                    # DeliberationEngine (Settings.deliberation_max_rounds)
│
├── trace/                           # TraceEvent infrastructure
│   ├── schema.py                    # Frozen TraceEvent schema + config_version
│   └── in_memory.py                 # InMemoryTracer + listener/callback support
│
├── viewer/                          # Visualization (Phase 3)
│   └── web/
│       ├── app.py                   # Dash 4-tab layout (Pipeline/Philosophers/W_Ethics/Deliberation)
│       └── figures.py               # Plotly chart builders (incl. deliberation + InteractionMatrix)
│
├── domain/                          # Immutable value types (PEP 420 dataclasses)
│   └── [Context, Proposal, SafetyVerdict, etc.]
│
├── ports/                           # Abstract interfaces (hexagonal architecture)
│   └── [memory, aggregator, tensor_engine, etc.]
│
├── runtime/                         # DI wiring + configuration
│   ├── settings.py                  # Settings (seed injection, NFR-REP-001)
│   ├── wiring.py                    # Dependency injection setup
│   ├── pareto_table_loader.py       # pareto_table.yaml loader (config_version tracked)
│   └── battalion_table_loader.py    # battalion_table.yaml loader
│
├── autonomy/                        # Solar Will (experimental)
│   └── solar_will.py
│
├── memory/                          # Memory backend
├── adapters/                        # Infrastructure adapters
├── cli/                             # CLI commands
├── config/                          # Runtime configuration
├── meta/                            # Meta / self-reflection utilities
└── experiments/                     # In-package experimental code
```

---

## `tests/` — Test Suite

```
tests/
├── conftest.py                      # Global pytest fixtures
│
├── unit/                            # Unit tests (phase-organized)
│   ├── test_philosophers/           # 39 philosopher unit tests
│   ├── test_phase3_observability.py # Phase 3: Viewer + ExplanationChain (34 tests)
│   ├── test_phase4_hardening.py     # Phase 4: W_Ethics Gate edge cases (29 tests)
│   ├── test_phase5_async.py         # Phase 5: AsyncPartyMachine
│   ├── test_rest_api.py             # REST API (24 tests: endpoints, auth, SSE, rate limit)
│   └── [60+ additional unit tests]
│
├── integration/                     # Integration tests
│
├── redteam/                         # Adversarial + red-team tests (Phase 4)
│   ├── test_prompt_injection.py     # 7 tests (all pass, Phase 4)
│   ├── test_goal_misalignment.py    # 7 tests (all pass, Phase 4)
│   ├── test_jailbreak_extended.py   # 15 adversarial patterns
│   ├── test_ethics_boundary.py      # 16 ethical grey zone tests
│   └── test_defense_metrics.py      # 11 defense metric automation tests
│
├── acceptance/                      # Given/When/Then acceptance tests [M1]
│   ├── conftest.py                  # Scenario loader fixtures
│   └── test_acceptance_suite.py    # AT-001–AT-010 (schema + requirement validation)
│
├── benchmarks/
│   └── test_pipeline_perf.py        # p50 ~33ms NORMAL mode (Phase 5)
│
├── fixtures/
│
└── [70+ pipeline/smoke/golden tests]
    ├── test_run_turn_e2e.py         # Pipeline E2E (CI must-pass)
    ├── test_philosopher_bridge.py   # (CI must-pass)
    ├── test_smoke_pipeline.py       # (CI must-pass)
    ├── test_golden_e2e.py           # Golden file E2E
    ├── test_golden_regression.py    # Golden regression
    ├── test_output_schema.py        # output_schema_v1 contract
    ├── test_input_schema.py         # input_schema_v1 contract
    └── [more…]
```

---

## `docs/spec/` — Machine-Readable Specification (M0 Milestone)

```
docs/spec/
├── prd.md                           # Product Requirements Document v0.3
├── srs_v0.1.md                      # Software Requirements Specification v0.3
├── output_schema_v1.json            # Output schema (FR-OUT-001, ADR-0004)
├── input_schema_v1.json             # Input schema
├── session_answers_schema_v1.json   # Session answers schema
├── session_answers_v1.md
├── features_v1.md
├── principles_v1.md
├── requirements_v1.md
├── test_cases.md                    # Acceptance test case specs (AT-001–AT-010+)
└── traceability.md                  # Requirement ↔ implementation ↔ test matrix
```

**M0 Status (due 2026-03-01):** ✅ PRD/SRS/Schema/TestCases/Traceability created.
**M1 Status (due 2026-03-15):** 🔄 In Progress — Stub Composer + AT-001–AT-010 acceptance runner.

---

## `scenarios/` — Acceptance Test Scenarios

Each scenario is a YAML case file used by `tests/acceptance/test_acceptance_suite.py`:

| File | Test ID | Topic |
|------|---------|-------|
| `case_001.yaml` | AT-001 | 転職：安定企業→スタートアップ |
| `case_002.yaml` | AT-002 | チームの人員整理 |
| `case_003.yaml` | AT-003 | 家族介護の設計 |
| `case_004.yaml` | AT-004 | 倫理的トレードオフ（医療系） |
| `case_005.yaml` | AT-005 | 責任主体の明確化 |
| `case_006.yaml` | AT-006 | 責任 + トレース重視 |
| `case_007.yaml` | AT-007 | 推奨 + 反証 |
| `case_008.yaml` | AT-008 | 倫理・不確実性・責任の複合 |
| `case_009.yaml` | AT-009 | 価値観不明（問い生成必須） |
| `case_010.yaml` | AT-010 | 制約の矛盾（矛盾検出 + 問い生成） |
| `case_011.yaml`–`case_015.yaml` | — | Additional edge cases |

---

## Architecture Overview

### Hexagonal `run_turn` Pipeline (10 steps)

```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine → ParetoAggregate → ShadowPareto → ActionGate → MemoryWrite
```

### Public Entry Points

```python
# Recommended
from po_core.app.api import run
result = run(user_input="What is justice?")

# High-level wrapper
from po_core import PoSelf
po = PoSelf()
response = po.generate("What is justice?")

# Stub Composer (rule-based, no LLM) [M1]
from po_core.app.composer import StubComposer
composer = StubComposer(seed=42)
output = composer.compose(case_dict)  # Returns output_schema_v1-compliant dict
```

### SafetyMode and Philosopher Counts

| SafetyMode | Philosophers | Trigger |
|-----------|-------------|---------|
| NORMAL | 39 | freedom_pressure < threshold |
| WARN | 5 | medium freedom_pressure |
| CRITICAL | 1 | high freedom_pressure |

---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Python files | `snake_case.py` | `tensor_engine.py` |
| Python classes | `PascalCase` | `FreedomPressureTensor` |
| Python functions | `snake_case` | `calculate_semantic_delta()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_PHILOSOPHERS = 39` |
| Markdown (major) | `UPPER_SNAKE.md` | `README.md`, `CONTRIBUTING.md` |
| Markdown (docs) | `lowercase-with-dashes.md` | `quickstart.md` |
| Config files | `lowercase.yaml` | `pareto_table.yaml` |
| Test files | `test_feature_name.py` | `test_philosopher_bridge.py` |
| Scenario files | `case_NNN_topic.yaml` | `case_001_job_change.yaml` |

---

## Key Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | PEP 517/518 packaging; `po-core-flyingpig` v0.3.0; `AGPL-3.0-or-later` |
| `pytest.ini` | Markers: `unit`, `integration`, `pipeline`, `slow`, `philosophical`, `redteam`, `phase4`, `phase5`, `acceptance` |
| `config/pareto_table.yaml` | Pareto weights (config_version tracked — must increment on change) |
| `config/battalion_table.yaml` | Philosopher battalions (config_version tracked) |
| `.env.example` | All `PO_` env vars: `PO_API_KEY`, `PO_CORS_ORIGINS`, `PO_RATE_LIMIT_PER_MINUTE`, … |

---

## License

| Use case | License |
|----------|---------|
| Personal / Academic / Research / OSS (AGPLv3-compliant) | **Free** — [GNU AGPLv3](./LICENSE) |
| Commercial / Proprietary / SaaS without source disclosure | **Commercial License required** — [COMMERCIAL_LICENSE.md](./COMMERCIAL_LICENSE.md) |

SPDX-License-Identifier: `AGPL-3.0-or-later`

---

## Phase Completion Status

| Phase | Title | Status |
|-------|-------|--------|
| Phase 1 | 39-philosopher scaling + tech debt | ✅ COMPLETE (2354 tests) |
| Phase 2 | ML tensors + Deliberation Engine | ✅ COMPLETE (2396 tests) |
| Phase 3 | Viewer WebUI + Explainable W_Ethics Gate | ✅ COMPLETE |
| Phase 4 | Adversarial Hardening (85 new tests) | ✅ COMPLETE |
| Phase 5 | REST API + Security + Docker + Async + Benchmarks | ✅ COMPLETE (v0.3.0) |
| M0 | Spec Scaffolding (PRD/SRS/Schema/Traceability) | ✅ COMPLETE |
| M1 | Stub Composer + E2E Acceptance Runner | 🔄 IN PROGRESS |

---

*This document is auto-maintained. When adding new modules or reorganizing directories, update this file and run `black`/`isort` checks.*
