# Changelog

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：[docs/status.md](/docs/status.md)

All notable changes to Po_core will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed

- docs(status): resync `docs/status.md` snapshot with merged Phase9–12 reality and current main-state governance/progress facts.
- chore(test): make `pytest.ini` the single source of truth and keep pytest configuration out of `pyproject.toml`.

### Fixed

- fix(bench): stabilize `test_bench_deliberation_scaling` via measurement hardening (`stable-p50` from multiple batch medians) while keeping the original regression guard semantics `max(r1 * 4.0, 0.95)` to avoid weakening slowdown detection.
- chore(pocore): align legacy contract-core metadata to `0.3.0` by updating `src/pocore/orchestrator.py` default version and synchronizing non-frozen golden meta (`meta.pocore_version` / `meta.generator.version`), while preserving frozen contracts for `case_001` and `case_009`.
- fix(pocore): align policy override behavior across generator/recommendation/trace coverage by preserving orchestrator policy override compatibility (`UNKNOWN_BLOCK`/`TIME_PRESSURE_DAYS`) and reflecting the same snapshot thresholds used by `scripts/policy_lab.py` during execution.

## [0.3.0] - 2026-03-08

### Changed

- chore(test): make `pytest.ini` the single source of truth by removing duplicated pytest options from `pyproject.toml`.
- docs(prd): align `docs/spec/prd.md` status/package/headcount/milestones with SSOT snapshot (`docs/status.md`) and current repository reality (`v0.3.0`, 42 philosophers, M0/M1 complete), and remove PyPI-state ambiguity by documenting `v0.2.0b4` as published history.
- docs(api): unify public philosopher count references to 42 (OpenAPI summary/description and project metadata).
- docs(api): fix OpenAPI `license_info` metadata to AGPL-3.0-or-later + Commercial and add explicit license links in API description.
- chore(release): bump package/runtime metadata to `0.3.0`, update OpenAPI license label, and align acceptance meta contracts while recording acceptance must-pass evidence (acceptance proof: `docs/release/acceptance_proof_v0.3.0.md`).
- ci: add pull-request governance workflow to validate SSOT/status/test-report requirements.
- docs: add PR template checklist to require SSOT acknowledgment, docs/status updates, test reporting, and impact/rollback notes.
- feat(tools): add standalone Phase4 emergence compare CLI (`scripts/eval_emergence.py`) with baseline/with-deliberation execution, human-readable diff, and optional JSON report output.
- changed(deliberation): add `avg_novelty` to `DeliberationResult` and include it in `summary()["emergence"]` for trace/summary observability.

### Fixed

- fix(bench): make `test_bench_deliberation_scaling` non-flaky with rationale-backed threshold constants (`DELIBERATION_SCALING_RATIO_LIMIT`, `DELIBERATION_SCALING_ABS_FLOOR_S`) and assert `rounds=3 p50 < max(rounds=1 p50 * 4.0, 0.95)` so tiny-baseline jitter is absorbed without weakening regression detection intent.
- fix(pocore): make `TIME_PRESSURE_DAYS` references dynamic for policy_lab override compatibility and align execution coverage planning-rule expectations with policy snapshots.
- fixed(tools): correct `avg_novelty` aggregation in eval_emergence to signals-weighted mean and lock behavior with regression tests.

### Documentation

- docs(release): add `docs/operations/publish_playbook.md` to standardize reproducible TestPyPI→PyPI operations (preconditions, workflow_dispatch steps, and rollback playbook), and link it from `docs/status.md`.
- test(solarwill): freeze WARN/CRITICAL degradation behavior for SolarWill `compute_intent` (WARN=clarification-first constraints, CRITICAL=refusal/stop/minimal-guidance constraints).

- test(solarwill): freeze universe-ethics axioms for SolarWill NORMAL mode via `compute_intent` contract test (survival-structure/distortion goals, non-distortion exceptions in constraints).

- docs: tighten `docs/厳格固定ルール.md` to align with SolarWill axioms (distortion/lifecycle exceptions), normalize top link blocks, and switch README SSOT/status links to GitHub full URLs.
- docs: rename manifesto file to `Po_core_Manifesto_When_Pigs_Fly.md` and update repository references.
- docs: purge legacy Manifesto filename/URL-encoded references and verify README links target the renamed file.
- test(acceptance): add AT-011 golden for unknowns × deadline boundary to lock question-priority and two-track/uncertainty behavior.
- fixed(acceptance): make StubComposer `now` deterministic for seeded runs to prevent daily golden drift and stabilize golden diff tests.
- test(acceptance): add AT-012 golden for stakeholder externality responsibility/ethics observability and lock ethics `rules_fired` behavior.

## [0.2.0] - 2026-03-03 (Stage2 5-F: stable release)

### Changed

- docs(api): unify public philosopher count references to 42 (OpenAPI summary/description and project metadata).
- Package version finalized from `0.2.0rc1` to `0.2.0` in `pyproject.toml` for stable release publication.
- Release notes normalized in Keep a Changelog order (`Unreleased` → `0.2.0` → `0.2.0rc1`).

### Documentation

- `QUICKSTART.md` updated with post-publish verification steps for the stable release:
  - `pip install po-core-flyingpig==0.2.0`
  - import smoke check
  - minimum quickstart execution path

## [0.2.0rc1] - 2026-02-22 (Phase 3: M1-C CI必須ゲート化 + RC版)

### Changed

- docs(api): unify public philosopher count references to 42 (OpenAPI summary/description and project metadata).
- CI workflow (`.github/workflows/ci.yml`) now makes schema + golden + acceptance gates explicit in the test job.
- Added an explicit JSON Schema gate step (`python -m pytest tests/test_input_schema.py tests/test_output_schema.py -v`) and explicit `jsonschema` dependency install in CI setup.
- Package version bumped from `0.2.0b4` to `0.2.0rc1` in `pyproject.toml` for RC publish readiness.

## [0.2.0b3] - 2026-02-21 (Phase 5 complete)

### Phase 5-E: Performance Benchmarks (2026-02-19)

#### Added — Benchmark Suite

- `tests/benchmarks/test_pipeline_perf.py` — Phase 5-E formal benchmark suite
- **7 benchmark tests** covering all safety modes, async, concurrency:
  - `test_bench_normal_p50` — NORMAL (39 phil) p50 < 5 s → actual **~33 ms**
  - `test_bench_warn_p50` — WARN (5 phil) p50 < 2 s → actual **~34 ms**
  - `test_bench_critical_p50` — CRITICAL (1 phil) p50 < 1 s → actual **~35 ms**
  - `test_bench_coldstart_vs_warmup` — cold-start ≤ 3× warm median
  - `test_bench_async_philosophers` — `async_run_philosophers()` × 39 → **11 ms**
  - `test_bench_concurrent_warn_requests` — 5 concurrent WARN → **181 ms** wall-clock
  - `test_bench_summary_table` — Rich table with p50/p90/p99/req/s per mode
- Rich-powered colored output (PASS/FAIL badges, table with status column)
- `benchmark` marker added to `pytest.ini` and `pyproject.toml`
- Usage: `pytest tests/benchmarks/ -v -s -m benchmark`

### Phase 5.5: PyPI Publish Preparation (2026-02-21)

#### Changed

- docs(api): unify public philosopher count references to 42 (OpenAPI summary/description and project metadata).
- Version bumped to `0.2.0b3` (PEP 440 compliant; `0.2.0-beta` was non-conformant)
- Package renamed from `po-core` → `po-core-flyingpig` in `pyproject.toml`
- `pyproject.toml` metadata updated: 39 philosophers, status=beta, progress=0.95
- `publish.yml` OIDC workflow verified: ready for TestPyPI / PyPI publish

### Phase 5.2: True Async PartyMachine — Real-Time SSE Streaming (2026-02-21)

#### Added

- `PhilosopherCompleted` trace event: emitted per-philosopher **immediately** on
  completion (success, timeout, or error) rather than batched after the full swarm
  — enables real-time progressive SSE streaming of philosopher results.
- `AsyncPartyMachine._dispatch_one(tracer=)` — optional tracer parameter; emits
  `PhilosopherCompleted(name, n, latency_ms, ok)` as each task resolves.
- `AsyncPartyMachine.run(tracer=)` and `async_run_philosophers(tracer=)` — new
  backward-compatible keyword argument passed down the call chain.
- `async_run_turn()` passes `deps.tracer` into `async_run_philosophers`, wiring
  the SSE listener to per-philosopher events automatically.
- `trace/schema.py`: `PhilosopherCompleted` spec registered (`name/n/latency_ms/ok`).
- `tests/unit/test_phase5_async.py`: 15 unit tests — event emission, payload
  correctness, error/timeout paths, schema validation, native-async detection
  (`_has_native_async`), and sync-path regression.

#### Improved

- SSE clients now receive philosopher results as they complete (progressive), not
  as a single burst when the last of 39 philosophers finishes.
- Philosophers overriding `propose_async()` (e.g., future LLM-backed philosophers)
  are dispatched natively on the event loop — zero thread overhead.

### Phase 5-D: True Async PartyMachine (2026-02-19)

#### Added — Async PartyMachine

- `async_run_philosophers()` in `party_machine.py` — asyncio-native parallel execution
  - `asyncio.gather` + `ThreadPoolExecutor` for non-blocking philosopher dispatch
  - Per-philosopher timeout (`timeout_s`) via `asyncio.wait_for`
  - `RunResult` dataclass: `philosopher_id`, `ok`, `timed_out`, `error`
- REST layer (`routers/reason.py`) updated to use `run_in_executor` offload
  - `reason()` and `_sse_generator()` no longer block the FastAPI event loop
- 7 async unit tests in `tests/unit/test_phase5d_async.py`

#### Fixed

- Removed unused `from rich.table import Table` import (F401)
- Replaced bare `f""` / `f"[...]"` f-strings without placeholders (F541)
- Sorted imports per isort rules in `test_phase5d_async.py`

---

## [0.2.0b0] - 2026-02-18

### Phase 5: Productization & Delivery

#### Added — REST API (Issue #13)

- `POST /v1/reason` — synchronous philosophical reasoning endpoint
- `POST /v1/reason/stream` — Server-Sent Events (SSE) streaming reasoning
- `GET /v1/philosophers` — full philosopher manifest (39 philosophers)
- `GET /v1/trace/{session_id}` — trace event retrieval per session
- `GET /v1/health` — health check with version + uptime
- OpenAPI/Swagger auto-generated at `/docs` and `/redoc`
- API key authentication via `X-API-Key` header (`PO_API_KEY` env var)
- `PO_SKIP_AUTH=true` bypass for local development
- `APISettings` via `pydantic-settings` (all config via env vars / `.env`)
- In-process LRU trace store (`max_trace_sessions` configurable)
- 17 unit tests covering all endpoints, auth, SSE, and OpenAPI schema
- `python -m po_core.app.rest` CLI entry point (uvicorn)

#### Added — Docker (Issue #14)

- `Dockerfile` — multi-stage build (builder + slim runtime)
- Non-root `pocore` user for security
- `docker-compose.yml` — API + named volumes + health check
- `.env.example` — documented environment variable reference
- `QUICKSTART.md` updated with Docker and REST API sections
- `HEALTHCHECK` every 30s via `/v1/health`

#### Added — Security Hardening (Phase 5-B)

- CORS middleware configurable via `PO_CORS_ORIGINS` env var
  - Default `"*"` for local development
  - Production: comma-separated origins with `allow_credentials=True`
- SlowAPI rate limiting via `PO_RATE_LIMIT_PER_MINUTE` (default 60 req/min per IP)
- Starlette-compatible typed rate limit handler wrapper (mypy clean)

#### Added — Docker Hardening (Phase 5-C)

- `.dockerignore` — excludes tests, docs, dev files from image build context
- `docker-compose.yml` updated: `PO_CORS_ORIGINS` and `PO_RATE_LIMIT_PER_MINUTE` as environment keys
- Rate limit derived from `APISettings` singleton at request time (not frozen at startup)

#### Changed — PyPI / Package (Phase 5-D)

- Version bumped from `0.1.0-alpha` → `0.2.0-beta`
- Development Status classifier updated to `4 - Beta`
- `pytest.ini` + `pyproject.toml` markers: added `phase5`, `redteam`, `phase4`
- `.github/workflows/publish.yml` — OIDC trusted publishing for TestPyPI and PyPI
  - `workflow_dispatch` (manual): target = `testpypi` or `pypi`
  - `release` event: auto-publish to PyPI

#### Fixed — CI

- `mypy` type check passes in CI (same-venv Python path)
- `type: ignore[arg-type]` on rate limit handler correctly typed via wrapper function

---

## [0.1.0-alpha] - 2025-11-02

### Added - Project Foundation

**Documentation**

- Initial README.md with comprehensive project overview
- CONTRIBUTING.md with Flying Pig Philosophy integration
- CODE_OF_CONDUCT.md emphasizing philosophical discourse
- MANIFESTO.md (Japanese and English versions)
- LICENSE (GNU AGPLv3)
- Repository structure documentation

**Philosophy**

- Flying Pig Philosophy framework established
- Integration design for 10+ philosophers:
  - Sartre (Freedom Pressure)
  - Jung (Shadow Integration)
  - Derrida (Trace/Rejection)
  - Heidegger (Dasein/Present Absence)
  - Watsuji Tetsurō (Aidagara/Betweenness)
  - Spinoza (Conatus)
  - Arendt (Public Stage)
  - Wittgenstein (Language Games)
  - Peirce (Semiotic Delta)
  - Aristotle (Phronesis)

**Design Documents**

- Po_core architecture specification v1.0 (36 pages)
- Po_self AI論文 (11章構成)
- Po_trace evolution module design
- Po_core Viewer design specifications
- 120+ design documents in development (Google Drive archive)

**Infrastructure**

- GitHub repository structure defined
- .gitignore for Python/AI/ML projects
- Development workflow established
- Testing framework planned

### Philosophy

This initial release establishes Po_core's foundation: an AI system that generates meaning through philosophical responsibility rather than just optimization. We're not building a chatbot that pretends to think ethically—we're building a system where ethical thinking is the mechanism.

As our manifesto states:
> "We don't know if pigs can fly. But we attached a balloon to one to find out."

This is the balloon. Now we begin the experiment.

---

## Version Number Scheme

Po_core follows [Semantic Versioning](https://semver.org/):

**MAJOR.MINOR.PATCH-STAGE**

- **MAJOR:** Incompatible API changes
- **MINOR:** New functionality (backward compatible)
- **PATCH:** Bug fixes (backward compatible)
- **STAGE:** Development stage (alpha, beta, rc, stable)

### Development Stages

**Alpha (current):** Core architecture and design phase

- Heavy development in progress
- APIs unstable
- Philosophical concepts being validated
- **Goal:** Prove feasibility

**Beta (planned):** Feature complete but unstable

- All major features implemented
- APIs stabilizing
- Extensive testing in progress
- **Goal:** Refine implementation

**RC (Release Candidate):** Stable, production-ready candidates

- No new features
- Bug fixes only
- Production testing
- **Goal:** Final validation

**Stable:** Production ready

- Stable APIs
- Comprehensive documentation
- Battle-tested
- **Goal:** Real-world deployment

---

## Upcoming Milestones

### v0.2.0 stable (Target: 2026-Q1)

**Goal:** Phase 5 complete — REST API stable + PyPI published

**Remaining work:**

- [x] Async `PartyMachine` (Phase 5.2 — real-time per-philosopher SSE events)
- [x] Formal benchmark suite (Phase 5-E — `tests/benchmarks/test_pipeline_perf.py`)
- [ ] Publish `po-core-flyingpig` to TestPyPI (manual `workflow_dispatch` → target: testpypi)
- [ ] Publish `po-core-flyingpig` to PyPI on v0.2.0b3 release tag

### v1.0.0 (Target: 2026-Q2/Q3)

**Goal:** Production-ready release

**Requirements:**

- [ ] Stable public APIs (no breaking changes)
- [ ] Complete documentation + QUICKSTART
- [ ] >80% test coverage
- [ ] Performance benchmarks (latency SLA < 5s NORMAL mode)
- [ ] Kubernetes / Helm chart
- [ ] Security audit

---

## Development Principles

### How We Track Changes

**Added:** New features or capabilities
**Changed:** Changes to existing functionality
**Deprecated:** Features marked for removal
**Removed:** Features that have been removed
**Fixed:** Bug fixes
**Security:** Security vulnerability fixes
**Philosophy:** Philosophical refinements or validations

### Our Approach to Versioning

**We publish failures:** If a philosophical concept doesn't work as expected, we document it in the changelog under "Changed" or "Philosophy"

**We iterate rapidly:** Alpha versions may have breaking changes between minor versions

**We value transparency:** Every decision is documented with rationale

**We revise gracefully:** When we're wrong, we say so and explain what we learned

---

## Historical Context

### The Origin (2024-2025)

Po_core emerged from a simple question: **What if AI had to take responsibility for meaning, not just generate optimal responses?**

The project began with 120+ design documents exploring how philosophical concepts could be implemented as mathematical tensors. Each philosopher represents not just a "perspective" but a computational mechanism that creates pressure, tension, and meaning.

### The Manifesto

Po_core is built on the **Flying Pig Philosophy**:

1. **Hypothesize Boldly** — The impossible becomes possible when someone formalizes it
2. **Verify Rigorously** — Bold hypotheses demand brutal testing
3. **Revise Gracefully** — Failures are data, not shame

This changelog embodies that philosophy. We'll document what works, what doesn't, and what we learn.

---

## Contributing to This Changelog

When contributing to Po_core:

1. **Add your changes** under [Unreleased]
2. **Use proper categories** (Added, Changed, Fixed, etc.)
3. **Be specific** — Explain what changed and why
4. **Reference issues** — Link to related GitHub issues
5. **Include philosophy** — If changes affect philosophical concepts, explain

### Example Entry

```markdown
### Added
- Nietzsche's Eternal Recurrence tensor ([#42](link))
  - Tracks cyclic patterns in reasoning chains
  - Creates tension with Sartre's freedom pressure
  - See docs/design/philosophers/nietzsche.md for details
```

### For Failed Experiments

We explicitly welcome documentation of failures:

```markdown
### Philosophy
- Attempted implementation of Kant's categorical imperative as a constraint tensor
  - **Result:** Created excessive rigidity in responses
  - **Learning:** Deontological ethics may need different formalization approach
  - **Next steps:** Exploring virtue ethics framework instead
  - See docs/experiments/failures/kant_constraint.md
```

---

## Long-Term Vision

### Beyond v1.0

**Expand Philosophical Coverage**

- Eastern philosophy (Confucius, Zhuangzi, Nāgārjuna)
- Indigenous philosophies
- Contemporary philosophers
- User-contributed philosophers

**Research Applications**

- Academic papers on philosophical AI
- Collaborations with philosophy departments
- Open datasets of philosophical reasoning traces

**Community Growth**

- Developer ecosystem
- Educational resources
- Philosophical AI conference

**Real-World Impact**

- Ethical AI systems for high-stakes decisions
- Transparency in AI reasoning
- Responsible AI deployment

---

## Questions?

If you have questions about versioning or changelog entries:

- Open a [GitHub Discussion](link)
- See [CONTRIBUTING.md](./CONTRIBUTING.md)
- Email: <flyingpig0229+github@gmail.com>

---

## Links

- **Repository:** <https://github.com/hiroshitanaka-creator/Po_core>
- **Documentation:** <https://hiroshitanaka-creator.github.io/Po_core/>
- **Issue Tracker:** <https://github.com/hiroshitanaka-creator/Po_core/issues>
- **Discussions:** <https://github.com/hiroshitanaka-creator/Po_core/discussions>

---

*"Whatever path you take, unique scenery and emotions await that only that route can offer."*

**Keep a Changelog:** We track every step, every success, every failure.
**Semantic Versioning:** We version our progress with precision.
**Flying Pig Philosophy:** We document boldly, test rigorously, revise gracefully.

🐷🎈
