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

Core experiment outputs are versioned under `docs/paper/experiments/` and benchmark summaries under `docs/paper/benchmarks/results/`. The build pipeline appends the latest deterministic snapshot (`scenario_count`, `golden_count`, and scenario digest) into the compiled manuscript to preserve reproducibility.

## Limitations

The current PDF builder intentionally focuses on deterministic single-page rendering to keep infrastructure requirements minimal. Full camera-ready typesetting (multi-page layout, citation styles, figure placement) should be handled in a future release pipeline while preserving deterministic inputs.

## References

1. Po_core repository specs and ADRs (`docs/spec/`, `docs/adr/`).
2. Acceptance and governance tests (`tests/acceptance/`, `tests/test_traceability.py`).
3. Deterministic paper pipeline scripts (`scripts/paper/`).
