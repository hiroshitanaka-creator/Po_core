from __future__ import annotations

import pickle
import sys

from po_core.philosopher_process import SerializedJob, run_one_philosopher


def main() -> int:
    payload = sys.stdin.buffer.read()
    job = pickle.loads(
        payload
    )  # nosec B301 — internal IPC only; parent process controls stdin pipe
    if not isinstance(job, SerializedJob):
        raise TypeError(f"Expected SerializedJob, got {type(job).__name__}")
    outcome = run_one_philosopher(job)
    sys.stdout.buffer.write(
        pickle.dumps(outcome)
    )  # nosec B301 — internal IPC only; written to parent-controlled stdout pipe
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
