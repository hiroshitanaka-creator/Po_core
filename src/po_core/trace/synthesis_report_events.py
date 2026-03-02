"""Helpers for synthesis report trace events."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

from po_core.domain.context import Context
from po_core.domain.trace_event import TraceEvent

if TYPE_CHECKING:
    from po_core.ports.trace import TracePort


_ALLOWED_KEYS = (
    "axis_name",
    "axis_spec_version",
    "scoreboard",
    "disagreements",
    "stance_distribution",
    "axis_vectors",
)


def _as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _sanitized_synthesis_payload(
    synthesis_report: dict,
    *,
    axis_name: str | None = None,
    axis_spec_version: str | None = None,
) -> dict[str, Any]:
    report = _as_dict(synthesis_report)
    payload = {k: report[k] for k in _ALLOWED_KEYS if k in report}
    if axis_name is not None:
        payload["axis_name"] = axis_name
    if axis_spec_version is not None:
        payload["axis_spec_version"] = axis_spec_version
    return payload


def emit_synthesis_report_built(
    tracer: "TracePort",
    ctx: Context,
    synthesis_report: dict,
    *,
    axis_name: str | None = None,
    axis_spec_version: str | None = None,
) -> None:
    payload = _sanitized_synthesis_payload(
        synthesis_report,
        axis_name=axis_name,
        axis_spec_version=axis_spec_version,
    )
    tracer.emit(TraceEvent.now("SynthesisReportBuilt", ctx.request_id, payload))


__all__ = ["emit_synthesis_report_built"]
