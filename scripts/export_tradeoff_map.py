#!/usr/bin/env python3
"""Export trade-off map artifacts (JSON + Markdown) from PoSelf trace."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from po_core.po_self import PoSelf
from po_core.viewer.tradeoff_map import build_tradeoff_map


def _render_axis_table(scoreboard: Dict[str, Any]) -> str:
    if not scoreboard:
        return "No axis scoreboard available."

    lines: List[str] = [
        "| axis | mean | variance | samples |",
        "|---|---:|---:|---:|",
    ]
    for axis in sorted(scoreboard.keys()):
        entry = scoreboard.get(axis)
        if not isinstance(entry, dict):
            continue
        lines.append(
            "| {axis} | {mean} | {variance} | {samples} |".format(
                axis=axis,
                mean=entry.get("mean", ""),
                variance=entry.get("variance", ""),
                samples=entry.get("samples", ""),
            )
        )
    return "\n".join(lines) if len(lines) > 2 else "No axis scoreboard available."




def _render_axis_vectors_table(axis_vectors: List[Any]) -> str:
    if not axis_vectors:
        return "No axis vectors available."

    lines: List[str] = [
        "| author | safety | benefit | feasibility | confidence | policy |",
        "|---|---:|---:|---:|---:|---|",
    ]

    rows: List[Dict[str, Any]] = []
    for item in axis_vectors:
        if isinstance(item, dict):
            rows.append(item)

    for item in sorted(rows, key=lambda row: str(row.get("author") or "")):
        scores = item.get("axis_scores", {})
        scores = scores if isinstance(scores, dict) else {}
        lines.append(
            "| {author} | {safety} | {benefit} | {feasibility} | {confidence} | {policy} |".format(
                author=item.get("author", ""),
                safety=scores.get("safety", ""),
                benefit=scores.get("benefit", ""),
                feasibility=scores.get("feasibility", ""),
                confidence=item.get("confidence", ""),
                policy=item.get("policy", ""),
            )
        )

    return "\n".join(lines) if len(lines) > 2 else "No axis vectors available."

def _render_disagreements(disagreements: List[Any]) -> str:
    if not disagreements:
        return "No disagreements captured."

    lines: List[str] = []
    for item in disagreements:
        if not isinstance(item, dict):
            lines.append(f"- {item}")
            continue

        dtype = item.get("type")
        if dtype == "stance_split":
            lines.append(
                "- type=stance_split, n_stances={n_stances}, largest_group={largest_group}".format(
                    n_stances=item.get("n_stances", ""),
                    largest_group=item.get("largest_group", ""),
                )
            )
            continue

        if dtype == "axis_variance":
            lines.append(
                "- type=axis_variance, axis={axis}, variance={variance}, samples={samples}".format(
                    axis=item.get("axis", "unknown"),
                    variance=item.get("variance", ""),
                    samples=item.get("samples", ""),
                )
            )
            continue

        axis = item.get("axis", "unknown")
        spread = item.get("spread", "")
        kind = item.get("kind", "")
        n_stances = item.get("n_stances", "")
        lines.append(
            f"- axis={axis}, spread={spread}, kind={kind}, n_stances={n_stances}"
        )
    return "\n".join(lines)


def _node_id(label: Any) -> str:
    text = str(label or "unknown")
    safe = re.sub(r"[^A-Za-z0-9_]", "_", text)
    return safe or "unknown"


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


def _render_mermaid(influence_edges: List[Any], influence_graph: Any) -> str:
    lines: List[str] = ["```mermaid", "graph LR"]

    candidates = influence_edges if isinstance(influence_edges, list) else []
    if not candidates:
        candidates = _flatten_influence_graph(influence_graph)

    added = False
    for edge in candidates:
        if not isinstance(edge, dict):
            continue
        src = edge.get("from") or edge.get("source") or edge.get("philosopher_a")
        dst = edge.get("to") or edge.get("target") or edge.get("philosopher_b")
        weight = edge.get("weight")
        if weight is None:
            weight = edge.get("influence")
        if src and dst:
            src_text = str(src)
            dst_text = str(dst)
            src_id = _node_id(src_text)
            dst_id = _node_id(dst_text)
            label = "" if weight is None else f"|{weight}|"
            lines.append(f"  {src_id}[\"{src_text}\"] -->{label} {dst_id}[\"{dst_text}\"]")
            added = True

    if not added:
        lines.append("  Empty[No influence edges found]")

    lines.append("```")
    return "\n".join(lines)


def _render_markdown(tradeoff_map: Dict[str, Any]) -> str:
    meta = tradeoff_map.get("meta", {})
    axis = tradeoff_map.get("axis", {})
    influence = tradeoff_map.get("influence", {})

    scoreboard = axis.get("scoreboard", {})
    disagreements = axis.get("disagreements", [])
    axis_vectors = axis.get("axis_vectors", [])
    influence_graph = influence.get("influence_graph", [])
    influence_edges = influence.get("influence_edges", [])

    lines = [
        "# Trade-off Map Report",
        "",
        "## Meta",
        f"- request_id: `{meta.get('request_id', '')}`",
        f"- status: `{meta.get('status', '')}`",
        f"- degraded: `{meta.get('degraded', '')}`",
        f"- consensus_leader: `{meta.get('consensus_leader', '')}`",
        f"- mode: `{meta.get('mode', '')}`",
        f"- prompt: {meta.get('prompt', '')}",
        "",
        "## Axis Scoreboard",
        _render_axis_table(scoreboard if isinstance(scoreboard, dict) else {}),
        "",
        "## Disagreements",
        _render_disagreements(disagreements if isinstance(disagreements, list) else []),
        "",
        "## Axis Vectors",
        _render_axis_vectors_table(axis_vectors if isinstance(axis_vectors, list) else []),
        "",
        "## Influence Graph",
        _render_mermaid(
            influence_edges if isinstance(influence_edges, list) else [],
            influence_graph,
        ),
        "",
        "## Influence Disclaimer",
        "Influence scores are a proxy derived from cosine-distance movement across revisions, not causal proof.",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True, help="Prompt for PoSelf")
    parser.add_argument(
        "--out-json", default="tradeoff_map.json", help="Output JSON path"
    )
    parser.add_argument(
        "--out-md", default="tradeoff_map.md", help="Output Markdown path"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    os.environ.setdefault("PO_STRUCTURED_OUTPUT", "1")

    po = PoSelf(enable_trace=True)
    response = po.generate(args.prompt)
    tracer = po.get_trace()

    tradeoff_map = build_tradeoff_map(response=response, tracer=tracer)

    out_json = Path(args.out_json)
    out_json.write_text(
        json.dumps(tradeoff_map, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    out_md = Path(args.out_md)
    out_md.write_text(_render_markdown(tradeoff_map), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
