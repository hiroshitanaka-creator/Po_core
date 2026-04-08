"""
philosopher_worker.py — DEPRECATED stdin/stdout pickle IPC worker.

This module is NOT used by any production code path.  The active process
execution path is ``po_core.runtime.philosopher_executor._run_one_in_subprocess``
via ``multiprocessing.Queue``.

SECURITY NOTE (B301):
  The pickle.loads() call below is intentionally restricted:
  - It is only reachable when this script is invoked as ``__main__``
  - The stdin pipe is controlled exclusively by a parent Po_core process
  - Input is validated to be SerializedJob before use

MIGRATION STATUS: pending replacement with JSON+dataclass round-trip.
  Blocker: SerializedJob contains philosopher instances (non-JSON-serializable).
  Approach: reconstruct philosopher from philosopher_id + registry in worker.
  Tracked in: docs/tech_debt/P3-2-pickle-ipc.md
"""
from __future__ import annotations

import pickle  # nosec B301 — see module docstring above
import struct
import sys

from po_core.philosopher_process import ExecOutcome, SerializedJob, run_one_philosopher

# Length-prefixed framing: 4-byte big-endian uint32 + payload bytes.
# Prevents partial-read bugs when stdout is flushed in chunks.
_FRAME_HEADER = "!I"


def _write_framed(stream: object, data: bytes) -> None:
    """Write length-prefixed frame to a binary stream."""
    header = struct.pack(_FRAME_HEADER, len(data))
    stream.write(header + data)  # type: ignore[union-attr]
    stream.flush()


def main() -> int:
    payload = sys.stdin.buffer.read()
    try:
        job = pickle.loads(payload)  # nosec B301
    except (pickle.UnpicklingError, TypeError, ValueError) as exc:
        # Pickle deserialization failure: return an error outcome instead of crashing
        error_outcome = ExecOutcome(
            proposals=[],
            n=0,
            timed_out=False,
            error=f"IPC deserialize error: {type(exc).__name__}: {exc}",
            latency_ms=0,
            philosopher_id="<unknown>",
        )
        _write_framed(sys.stdout.buffer, pickle.dumps(error_outcome))  # nosec B301
        return 1

    if not isinstance(job, SerializedJob):
        raise TypeError(f"Expected SerializedJob, got {type(job).__name__}")

    outcome = run_one_philosopher(job)
    _write_framed(
        sys.stdout.buffer,
        pickle.dumps(outcome),  # nosec B301
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
