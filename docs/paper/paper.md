# Po_core Reproducible Paper Draft

## Abstract

This document is generated through a deterministic local pipeline.
The pipeline binds experiment outputs and paper rendering in repository-managed scripts.

## Method

1. Generate experiment snapshot JSON under `docs/paper/experiments/`.
2. Build a compiled markdown with embedded experiment summary.
3. Render deterministic PDF.

## Results

Results are embedded from `results_latest.json` at build time.

## Conclusion

The repository can regenerate experiment output snapshots and an accompanying PDF via fixed commands.
