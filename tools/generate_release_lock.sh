#!/usr/bin/env bash
# ======================================================================
# tools/generate_release_lock.sh
# ----------------------------------------------------------------------
# Regenerate `requirements-release.lock` with hash-pinned dependencies so
# that release Docker builds can be reproduced bit-for-bit from a single
# git commit.
#
# Usage:
#   bash tools/generate_release_lock.sh
#
# Output:
#   requirements-release.lock  — hash-pinned, ready for
#                                `pip install --require-hashes -r ...`
#
# Notes:
#   * Uses `pip-compile` from pip-tools (install via `pip install pip-tools`).
#   * The file is intentionally committed to the repository so that the
#     Docker build in `Dockerfile` can resolve the exact same artifacts
#     at any point in the future.  `pip-audit` runs against this file in
#     CI to track vulnerability drift without losing reproducibility.
# ======================================================================
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v pip-compile >/dev/null 2>&1; then
    echo "error: pip-compile not found.  Run 'pip install pip-tools' first." >&2
    exit 2
fi

pip-compile \
    --generate-hashes \
    --output-file=requirements-release.lock \
    --resolver=backtracking \
    --strip-extras \
    requirements.txt

echo "Wrote requirements-release.lock ($(wc -l <requirements-release.lock) lines)"
