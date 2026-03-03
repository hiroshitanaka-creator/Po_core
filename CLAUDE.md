# CLAUDE.md — Po_core Development Context

> This file is read by Claude Code at the start of every session.
> It provides project context, conventions, and current focus.

## What is Po_core?

Philosophy-driven AI: 42 philosopher AI personas deliberate via tensor calculations
(Freedom Pressure, Semantic Delta, Blocked Tensor) and a 3-layer W_Ethics Gate
to generate ethically responsible responses.

**Core thesis:** 「AIは統計的オウムである」という批判に対して、哲学的熟議によって倫理的責任を持つAIが
**構築できる**ことをコード・テスト・論文で証明する。

## Architecture

**Hexagonal `run_turn` pipeline** (10 steps):

```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine → ParetoAggregate → ShadowPareto → ActionGate → MemoryWrite
```

**Entry points:**

- `po_core.run()` — recommended public API (`src/po_core/app/api.py`)
- `PoSelf.generate()` — high-level wrapper (`src/po_core/po_self.py`)

## Key Directories

```
src/po_core/
├── philosophers/     # 42 philosopher modules + manifest + registry
│                     #   39 classic (Western/Eastern) +
│                     #    2 African (Appiah, Fanon) +
│                     #    1 Canadian (CharlesTaylor)
├── tensors/          # TensorEngine + metrics/ (freedom_pressure, semantic_delta, blocked_tensor)
├── safety/           # W_Ethics Gate (wethics_gate/), fallback, policy_scoring
├── aggregator/       # Pareto, conflict_resolver, policy_aware, weighted_vote
├── trace/            # TraceEvent schema, in_memory tracer, decision/pareto events
├── viewer/           # PoViewer, pipeline/tensor/philosopher views
├── domain/           # Immutable value types (Context, Proposal, SafetyVerdict, etc.)
├── ports/            # Abstract interfaces (memory, aggregator, tensor_engine, etc.)
├── runtime/          # DI wiring, settings, pareto/battalion table loaders
├── autonomy/         # Solar Will (experimental)
├── ensemble.py       # run_turn pipeline orchestrator
└── party_machine.py  # Philosopher combination assembly
```

## Conventions

- **Python 3.10+**, formatted with **black 26.1.0**, imports sorted with **isort 5.13.2**
- **pytest** with markers: `unit`, `integration`, `pipeline`, `slow`, `philosophical`, `redteam`, `phase4`, `phase5`, `acceptance`
- CI requires **pipeline-marked tests to pass**; full suite is best-effort
- Philosopher risk levels: 0 (safe), 1 (standard), 2 (risky) — defined in `manifest.py`
- SafetyMode: NORMAL (42 philosophers) / WARN (5) / CRITICAL (1)
- Config-driven philosophy: `pareto_table.yaml`, `battalion_table.yaml`
- TraceEvents use frozen schema with `config_version` tracking
- REST API config via env vars with `PO_` prefix (see `.env.example`)
- Version: `0.2.0b4` (beta) → `0.2.0rc1` after M1 → `0.2.0` after M4 → `1.0.0` after all AT pass + paper draft

## Current Status (2026-03-03)

### 完了済みフェーズ (Phases 1–7 + Spec M0: ALL COMPLETE)

**Phase 1: COMPLETE** — 42-philosopher scaling + tech debt cleared.

**Phase 2: COMPLETE** — ML tensors + Deliberation Engine.

- Semantic Delta: multi-backend (sbert/tfidf/basic) with encode_texts() API
- InteractionMatrix: NxN embedding-based harmony + keyword tension
- DeliberationEngine: multi-round philosopher dialogue (Settings.deliberation_max_rounds)

**Phase 3: COMPLETE** — Viewer WebUI + Explainable W_Ethics Gate + Deliberation Visualization

Key files:

- `src/po_core/viewer/web/app.py` — Dash app factory (4-tab layout)
- `src/po_core/viewer/web/figures.py` — Plotly chart builders (incl. deliberation)
- `src/po_core/safety/wethics_gate/explanation.py` — ExplanationChain + verdict bridge
- `src/po_core/trace/in_memory.py` — InMemoryTracer with listener support

**Phase 4: COMPLETE** — Adversarial Hardening + Ethical Stress Testing.

- `PromptInjectionDetector` — 100% injection/jailbreak detection, ≤20% FP rate
- Enhanced `IntentionGate.check_intent` — W1 structural exclusion + obfuscation normalization
- `tests/redteam/` — 56 red team tests, all passing

**Phase 5: COMPLETE** — Productization. Package: `po-core-flyingpig`.

- FastAPI REST API (`src/po_core/app/rest/`) — 5 routers
- Docker multi-stage build, docker-compose, `.env.example`
- `AsyncPartyMachine` — real-time per-philosopher SSE events
- Benchmarks: p50 ~33ms NORMAL mode
- `publish.yml` OIDC workflow ready (actual PyPI publish: pending M4)

**Phase 6: COMPLETE** — Autonomous Evolution.

- FreedomPressureV2 (6D ML tensor), MetaEthicsMonitor, 3-layer memory

**Phase 7 (→ refactored): COMPLETE** — Philosopher diversity expansion.

- Originally: AI vendor slots (Claude/GPT/Gemini/Grok)
- **Refactored 2026-03-03 (ADR-0006):** Replaced with African & Canadian philosophers
  - Kwame Anthony Appiah (Ghana/US) — Cosmopolitanism, anti-essentialism [Slot 40]
  - Frantz Fanon (Martinique/Algeria) — Decolonialism, liberation philosophy [Slot 41]
  - Charles Taylor (Canada) — Communitarianism, politics of recognition [Slot 42]

**Spec M0: COMPLETE** (2026-02-28) — PRD / SRS / Schema / TestCases / Traceability

### 進行中マイルストーン

**🔄 M1: LLMなしE2E（期限: 2026-03-15）**

- ✅ StubComposer → `output_schema_v1.json` 準拠出力 (`src/po_core/app/composer.py`)
- ✅ AT-001〜AT-010 テストスイート追加 (`tests/acceptance/`)
- 🔲 `jsonschema` CI バリデーションゲート追加
- 🔲 Golden files: `case_001_expected.json`, `case_009_expected.json`

**完了基準:** `pytest tests/acceptance/ -v` が全10件グリーン（スタブ実装で）

---

## Roadmap (ROADMAP_FINAL_FORM.md 準拠)

```
Stage 1: 仕様の完成 [2026-03〜05]  ← M1〜M4
Stage 2: v1.0 リリース [2026-06]   ← PyPI + 全AT通過
Stage 3: エコシステム [2026 Q3-Q4] ← 永続化・WebSocket・SDK
Stage 4: 学術的証明 [2026 Q4-2027] ← 論文・ベンチマーク
Stage 5: 最終系 [2027〜]           ← 哲学的AI推論の参照実装
```

### マイルストーン詳細

| マイルストーン | 期限 | 内容 | 状態 |
|---|---|---|---|
| **M1** | 2026-03-15 | LLMなしE2E: AT-001〜010 スタブで全通過 + jsonschema CI gate | 🔄 進行中 |
| **M2** | 2026-04-05 | ethics_v1 + responsibility_v1 + 不確実性ラベル | 🔲 未着手 |
| **M3** | 2026-04-26 | question_layer v1 (問い生成・問い抑制) | 🔲 未着手 |
| **M4** | 2026-05-10 | ガバナンス完成: CI全自動 + ADR運用 + Traceability auto | 🔲 未着手 |
| **5-F** | 2026-06 | PyPI公開 (`po-core-flyingpig 0.2.0`) | 🔲 未着手 |
| **v1.0.0** | 2026-06 | 全AT通過 + 論文ドラフト完成 + CI 100% green | 🔲 未着手 |

### バージョン戦略

```
現在: 0.2.0b4 (beta)
M1:   0.2.0rc1 (release candidate)
M4:   0.2.0    (stable, PyPI)
v1.0: 1.0.0    (全AT通過 + 論文ドラフト完成)
```

See `ROADMAP_FINAL_FORM.md` for full rationale.

---

## Testing

```bash
# Pipeline tests (must-pass, fast)
pytest tests/test_run_turn_e2e.py tests/test_philosopher_bridge.py tests/test_smoke_pipeline.py -v

# Full suite
pytest tests/ -v --tb=short

# Acceptance tests (M1 target: all 10 green)
pytest tests/acceptance/ -v

# Single philosopher
pytest tests/unit/test_philosophers/test_aristotle.py -v

# Red team (Phase 4 hardening)
pytest tests/redteam/ -v
pytest -m "redteam or phase4" -v

# Phase 3 observability
pytest -m observability -v

# Phase 5 REST API
pytest tests/unit/test_rest_api.py -v

# Benchmarks
pytest tests/benchmarks/ -v
```

## REST API (Phase 5)

```bash
# Run locally
python -m po_core.app.rest

# Run with Docker
docker compose up

# Health check
curl http://localhost:8000/v1/health

# Reason endpoint (no auth in dev)
curl -X POST http://localhost:8000/v1/reason \
     -H "Content-Type: application/json" \
     -d '{"input": "What is justice?"}'
```

Key env vars (see `.env.example`):

- `PO_API_KEY` — enable auth (empty = no auth)
- `PO_CORS_ORIGINS` — comma-separated allowed origins (default `"*"`)
- `PO_RATE_LIMIT_PER_MINUTE` — per-IP rate limit (default `60`)

## Do NOT

- Push to `main` without CI passing
- Modify `pareto_table.yaml` or `battalion_table.yaml` without updating `config_version`
- Add dependencies without updating both `pyproject.toml` and `requirements.txt`
- Skip pre-commit hooks (`--no-verify`)
- Import from `po_core.ensemble` directly — use `po_core.run()` or `PoSelf.generate()`
- Import from `po_core.app.rest` directly in non-API code — REST layer is a delivery adapter only
- Add AI vendor names (Claude, GPT, Gemini, etc.) as philosopher slots — use historical/academic philosophers only (see ADR-0006)
