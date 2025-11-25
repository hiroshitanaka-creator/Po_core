#!/usr/bin/env bash
# Demonstrate the Po_self CLI path with tensor output and tracing.

PROMPT="Does innovation flourish more through cooperation or competition?"
LOG_PATH="examples/basic/cli_trace.ndjson"

python -m po_core.cli po-self "$PROMPT" --show-tensors --log-file "$LOG_PATH" --ndjson
