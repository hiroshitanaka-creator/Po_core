"""
philosopher_worker.py — stdin/stdout JSON IPC worker.

This module is NOT used by any production code path. The active process
execution path is ``po_core.runtime.philosopher_executor._run_one_in_subprocess``
via ``multiprocessing.Queue``.

Security posture:
- No pickle deserialization.
- Input is strict JSON payload with philosopher_id + serializable snapshots.
- Philosopher instance is reconstructed in-worker from registry metadata.
"""
from __future__ import annotations

import json
import struct
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from po_core.philosopher_process import ExecOutcome, SerializedJob, run_one_philosopher
from po_core.philosophers.registry import PhilosopherRegistry

from .domain.context import Context
from .domain.intent import Intent
from .domain.memory_snapshot import MemoryItem, MemorySnapshot
from .domain.tensor_snapshot import TensorSnapshot

# Length-prefixed framing: 4-byte big-endian uint32 + payload bytes.
# Prevents partial-read bugs when stdout is flushed in chunks.
_FRAME_HEADER = "!I"


@dataclass(frozen=True)
class _JsonJob:
    philosopher_id: str
    ctx: Context
    intent: Intent
    tensors: TensorSnapshot
    memory: MemorySnapshot
    limit_per_philosopher: int
    timeout_s: float


def _write_framed(stream: object, data: bytes) -> None:
    """Write length-prefixed frame to a binary stream."""
    header = struct.pack(_FRAME_HEADER, len(data))
    stream.write(header + data)  # type: ignore[union-attr]
    stream.flush()


def _parse_datetime(value: Any) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("datetime field must be a non-empty ISO-8601 string")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _parse_context(payload: Mapping[str, Any]) -> Context:
    request_id = str(payload.get("request_id") or "").strip()
    user_input = str(payload.get("user_input") or "")
    if not request_id:
        raise ValueError("ctx.request_id is required")
    created_at = _parse_datetime(payload.get("created_at"))
    raw_meta = payload.get("meta")
    meta = dict(raw_meta) if isinstance(raw_meta, Mapping) else {}
    return Context(
        request_id=request_id,
        created_at=created_at,
        user_input=user_input,
        meta=meta,
    )


def _parse_intent(payload: Mapping[str, Any]) -> Intent:
    raw_goals = payload.get("goals")
    raw_constraints = payload.get("constraints")
    raw_weights = payload.get("weights")
    goals = [str(x) for x in raw_goals] if isinstance(raw_goals, list) else []
    constraints = (
        [str(x) for x in raw_constraints] if isinstance(raw_constraints, list) else []
    )
    weights = (
        {str(k): float(v) for k, v in dict(raw_weights).items()}
        if isinstance(raw_weights, Mapping)
        else {}
    )
    return Intent(goals=goals, constraints=constraints, weights=weights)


def _parse_tensors(payload: Mapping[str, Any]) -> TensorSnapshot:
    computed_at = _parse_datetime(payload.get("computed_at"))
    raw_metrics = payload.get("metrics")
    metrics = (
        {str(k): float(v) for k, v in dict(raw_metrics).items()}
        if isinstance(raw_metrics, Mapping)
        else {}
    )
    return TensorSnapshot(
        computed_at=computed_at,
        metrics=metrics,
        version=str(payload.get("version") or "v1"),
    )


def _parse_memory(payload: Mapping[str, Any]) -> MemorySnapshot:
    raw_items = payload.get("items")
    items: list[MemoryItem] = []
    if isinstance(raw_items, list):
        for item in raw_items:
            if not isinstance(item, Mapping):
                continue
            item_id = str(item.get("item_id") or "").strip()
            text = str(item.get("text") or "")
            created_at_raw = item.get("created_at")
            if not item_id or created_at_raw is None:
                continue
            tags_raw = item.get("tags")
            tags = [str(x) for x in tags_raw] if isinstance(tags_raw, list) else []
            items.append(
                MemoryItem(
                    item_id=item_id,
                    created_at=_parse_datetime(created_at_raw),
                    text=text,
                    tags=tags,
                )
            )
    raw_meta = payload.get("meta")
    meta = (
        {str(k): str(v) for k, v in dict(raw_meta).items()}
        if isinstance(raw_meta, Mapping)
        else {}
    )
    summary = payload.get("summary")
    return MemorySnapshot(
        items=items,
        summary=str(summary) if isinstance(summary, str) else None,
        meta=meta,
    )


def _decode_json_job(payload: bytes) -> _JsonJob:
    root = json.loads(payload.decode("utf-8"))
    if not isinstance(root, Mapping):
        raise ValueError("IPC payload must be a JSON object")
    philosopher_id = str(root.get("philosopher_id") or "").strip()
    if not philosopher_id:
        raise ValueError("philosopher_id is required")
    ctx_raw = root.get("ctx")
    intent_raw = root.get("intent")
    tensors_raw = root.get("tensors")
    memory_raw = root.get("memory")
    if not isinstance(ctx_raw, Mapping):
        raise ValueError("ctx must be an object")
    if not isinstance(intent_raw, Mapping):
        raise ValueError("intent must be an object")
    if not isinstance(tensors_raw, Mapping):
        raise ValueError("tensors must be an object")
    if not isinstance(memory_raw, Mapping):
        raise ValueError("memory must be an object")

    return _JsonJob(
        philosopher_id=philosopher_id,
        ctx=_parse_context(ctx_raw),
        intent=_parse_intent(intent_raw),
        tensors=_parse_tensors(tensors_raw),
        memory=_parse_memory(memory_raw),
        limit_per_philosopher=int(root.get("limit_per_philosopher", 3)),
        timeout_s=float(root.get("timeout_s", 5.0)),
    )


def _load_philosopher(philosopher_id: str) -> Any:
    registry = PhilosopherRegistry(cache_instances=False)
    philosophers, errors = registry.load([philosopher_id])
    if errors:
        err = errors[0]
        raise ValueError(
            f"Failed to load philosopher {philosopher_id}: {err.error} ({err.module}:{err.symbol})"
        )
    if not philosophers:
        raise ValueError(f"No philosopher loaded for id: {philosopher_id}")
    return philosophers[0]


def _encode_outcome(outcome: ExecOutcome) -> bytes:
    payload = {
        "proposals": [proposal.to_dict() for proposal in outcome.proposals],
        "n": int(outcome.n),
        "timed_out": bool(outcome.timed_out),
        "error": outcome.error,
        "latency_ms": int(outcome.latency_ms),
        "philosopher_id": outcome.philosopher_id,
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")


def main() -> int:
    payload = sys.stdin.buffer.read()
    try:
        json_job = _decode_json_job(payload)
        philosopher = _load_philosopher(json_job.philosopher_id)
        job = SerializedJob(
            philosopher=philosopher,
            ctx=json_job.ctx,
            intent=json_job.intent,
            tensors=json_job.tensors,
            memory=json_job.memory,
            limit_per_philosopher=json_job.limit_per_philosopher,
            timeout_s=json_job.timeout_s,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        error_outcome = ExecOutcome(
            proposals=[],
            n=0,
            timed_out=False,
            error=f"IPC deserialize error: {type(exc).__name__}: {exc}",
            latency_ms=0,
            philosopher_id="<unknown>",
        )
        _write_framed(sys.stdout.buffer, _encode_outcome(error_outcome))
        return 1

    outcome = run_one_philosopher(job)
    _write_framed(sys.stdout.buffer, _encode_outcome(outcome))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
