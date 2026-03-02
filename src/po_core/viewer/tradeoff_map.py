"""Trade-off map builder from PoSelf response + trace events."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Sequence

from po_core.domain.trace_event import TraceEvent



def _safe_dict(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}



def _safe_list(value: Any) -> List[Any]:
    return list(value) if isinstance(value, list) else []


def _safe_dict_or_list(value: Any) -> Dict[str, Any] | List[Any]:
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, list):
        return list(value)
    return {}


def _safe_float(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _flatten_influence_graph(influence_graph: Any) -> List[Dict[str, Any]]:
    if not isinstance(influence_graph, dict):
        return []

    edges: List[Dict[str, Any]] = []
    for sender, node in influence_graph.items():
        if not isinstance(node, dict):
            continue
        influenced = node.get("influenced")
        if not isinstance(influenced, dict):
            continue

        for recipient, delta in influenced.items():
            weight = _safe_float(delta)
            if not sender or not recipient or weight is None:
                continue
            edges.append({"from": str(sender), "to": str(recipient), "weight": weight})

    return edges



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


def _meta_axis_fields(metadata: Dict[str, Any], synthesis_report: Dict[str, Any]) -> Dict[str, Any]:
    axis_name = synthesis_report.get("axis_name")
    axis_spec_version = synthesis_report.get("axis_spec_version")

    proposal = _safe_dict(metadata.get("proposal"))
    proposal_po_core = _safe_dict(_safe_dict(proposal.get("extra")).get("po_core"))

    if axis_name is None:
        axis_name = proposal_po_core.get("axis_name")
    if axis_spec_version is None:
        axis_spec_version = proposal_po_core.get("axis_spec_version")

    fields: Dict[str, Any] = {
        "axis_scoring_calibration_enabled": bool(
            os.getenv("PO_AXIS_SCORING_CALIBRATION_PARAMS")
        )
    }
    if axis_name is not None:
        fields["axis_name"] = axis_name
    if axis_spec_version is not None:
        fields["axis_spec_version"] = axis_spec_version
    return fields


def validate_tradeoff_map_v1(obj: dict) -> None:
    """Validate minimal tradeoff_map v1 contract."""
    if not isinstance(obj, dict):
        raise ValueError("tradeoff_map must be a dict")

    required_types = {
        "schema_version": str,
        "meta": dict,
        "axis": dict,
        "influence": dict,
        "timeline": list,
    }
    for key, expected_type in required_types.items():
        if key not in obj:
            raise ValueError(f"tradeoff_map missing required key: {key}")
        if not isinstance(obj[key], expected_type):
            type_name = type(obj[key]).__name__
            raise ValueError(
                f"tradeoff_map key '{key}' must be {expected_type.__name__}, got {type_name}"
            )

    if obj["schema_version"] != "tradeoff_map_v1":
        raise ValueError(
            "tradeoff_map schema_version must be 'tradeoff_map_v1', "
            f"got {obj['schema_version']!r}"
        )



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
    meta.update(_meta_axis_fields(metadata, synthesis_report))
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
        "influence_graph": _safe_dict_or_list(deliberation_payload.get("influence_graph")),
        "influence_edges": _flatten_influence_graph(
            deliberation_payload.get("influence_graph")
        ),
        "top_influencers": _safe_list(deliberation_payload.get("top_influencers")),
        "interference_pairs_top": _safe_list(
            deliberation_payload.get("interference_pairs_top")
        ),
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
        "schema_version": "tradeoff_map_v1",
        "meta": meta,
        "axis": axis,
        "influence": influence,
        "timeline": timeline,
    }
