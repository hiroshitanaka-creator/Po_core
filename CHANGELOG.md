# Changelog

All notable changes to Po_core will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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
- LICENSE (MIT License)
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
