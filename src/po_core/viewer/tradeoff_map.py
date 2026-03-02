"""Trade-off map builder from PoSelf response + trace events."""

from __future__ import annotations

from typing import Any, Dict, List, Sequence

from po_core.domain.trace_event import TraceEvent



def _safe_dict(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}



def _safe_list(value: Any) -> List[Any]:
    return list(value) if isinstance(value, list) else []



def _events_from_tracer(tracer: Any) -> List[TraceEvent]:
    if isinstance(tracer, list):
        return [e for e in tracer if isinstance(e, TraceEvent)]

    events = getattr(tracer, "events", None)
    if isinstance(events, list):
        return [e for e in events if isinstance(e, TraceEvent)]

    if isinstance(tracer, Sequence):
        return [e for e in tracer if isinstance(e, TraceEvent)]

    return []



def _find_first_payload(events: Sequence[TraceEvent], event_type: str) -> Dict[str, Any]:
    for event in events:
        if event.event_type == event_type and isinstance(event.payload, dict):
            return dict(event.payload)
    return {}



def build_tradeoff_map(response: Any, tracer: Any) -> Dict[str, Any]:
    """Build trade-off map artifact from PoSelf response and trace events."""
    metadata = _safe_dict(getattr(response, "metadata", {}))
    synthesis_report = _safe_dict(metadata.get("synthesis_report"))

    events = _events_from_tracer(tracer)
    deliberation_payload = _find_first_payload(events, "DeliberationCompleted")
    selected_payload = _find_first_payload(events, "PhilosophersSelected")

    meta: Dict[str, Any] = {
        "request_id": metadata.get("request_id"),
        "status": metadata.get("status"),
        "degraded": metadata.get("degraded"),
        "consensus_leader": getattr(response, "consensus_leader", None),
        "prompt": getattr(response, "prompt", ""),
    }
    if selected_payload:
        for key in ("ids", "mode", "workers"):
            if key in selected_payload:
                meta[key] = selected_payload.get(key)

    axis = {
        "scoreboard": _safe_dict(synthesis_report.get("scoreboard")),
        "disagreements": _safe_list(synthesis_report.get("disagreements")),
        "stance_distribution": _safe_dict(synthesis_report.get("stance_distribution")),
        "axis_vectors": _safe_list(synthesis_report.get("axis_vectors")),
    }

    influence = {
        "influence_graph": _safe_list(deliberation_payload.get("influence_graph")),
        "top_influencers": _safe_list(deliberation_payload.get("top_influencers")),
        "rounds": _safe_list(deliberation_payload.get("rounds")),
        "interaction_summary": _safe_dict(
            deliberation_payload.get("interaction_summary")
        ),
    }

    timeline = [
        {
            "event_type": event.event_type,
            "ts": event.occurred_at.isoformat(),
        }
        for event in events
    ]

    return {
        "meta": meta,
        "axis": axis,
        "influence": influence,
        "timeline": timeline,
    }
