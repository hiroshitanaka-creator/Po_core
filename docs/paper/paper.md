# Po_core: A Philosophy-Driven AI Deliberation Framework for Ethical Decision Support

## Abstract

Po_core proposes a deterministic, accountable AI deliberation stack that prioritizes ethical reasoning, responsibility attribution, and traceability over unconstrained text generation. This paper package is built reproducibly inside the repository so that claims can be re-checked by rebuilding artifacts from versioned scripts.

## Introduction

Recent criticism frames LLM systems as "stochastic parrots" that cannot justify decisions. Po_core addresses this by enforcing explicit contracts on schema validity, deterministic execution, and trace output. The objective of this paper artifact is to provide an arXiv-ready structure tied directly to executable evidence in the repository.

## Method

1. Generate deterministic experiment snapshots under `docs/paper/experiments/`.
2. Build comparative benchmark artifacts under `docs/paper/benchmarks/results/`.
3. Compile `paper.md` with embedded snapshot metadata.
4. Render a deterministic PDF from the compiled manuscript.

## Experiments

Deterministic evidence is generated into repository-tracked artifacts:

- Experiment snapshot: `docs/paper/experiments/results_latest.json`
  - created_at: `2026-02-22T00:00:00Z`
  - seed: `0`
  - digest keys: `scenario_digest`, `snapshot_digest`
- Comparative benchmark: `docs/paper/benchmarks/results/comparative_results.json`
  - created_at: `2026-02-22T00:00:00Z`
  - seed: `0`
  - digest key: `results_digest`

### Benchmark table (overall)

| System | Diversity | Explainability | Safety | Emergence | Overall |
|---|---:|---:|---:|---:|---:|
| Po_core | 100.00 | 91.00 | 89.00 | 87.00 | 91.75 |
| Mixture-of-Experts baseline | 58.00 | 47.00 | 61.00 | 73.00 | 59.75 |
| RLHF baseline | 35.00 | 51.00 | 72.00 | 46.00 | 51.00 |
| Chain-of-Thought baseline | 36.00 | 63.00 | 54.00 | 44.00 | 49.25 |
| Single LLM (GPT/Claude) | 31.00 | 42.00 | 57.00 | 48.00 | 44.50 |

The benchmark chart is emitted as `docs/paper/benchmarks/results/comparative_overall.svg`, and the CSV/Markdown tables are co-generated for reproducible paper assembly.

## Limitations

The current PDF builder intentionally focuses on deterministic single-page rendering to keep infrastructure requirements minimal. Full camera-ready typesetting (multi-page layout, citation styles, figure placement) should be handled in a future release pipeline while preserving deterministic inputs.

## References

1. Po_core repository specs and ADRs (`docs/spec/`, `docs/adr/`).
2. Acceptance and governance tests (`tests/acceptance/`, `tests/test_traceability.py`).
3. Deterministic paper pipeline scripts (`scripts/paper/`).
