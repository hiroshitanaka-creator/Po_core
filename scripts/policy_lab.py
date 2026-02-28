"""Policy Lab v1: deterministic policy-threshold perturbation and impact reporting."""

from __future__ import annotations

import argparse
import json
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pocore import orchestrator, policy_v1
from pocore.runner import run_case_file

DEFAULT_NOW = "2026-02-22T00:00:00Z"
VALUES_PACK_RULE_IDS = (
    "Q_VALUES_CLARIFICATION_PACK_V1",
    "PLAN_VALUES_CLARIFICATION_PACK_V1",
    "ETH_VALUES_EMPTY_CLARIFICATION",
)
CONFLICT_PACK_RULE_IDS = (
    "ETH_CONSTRAINT_CONFLICT_DISCLOSURE",
    "PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN",
)


@dataclass(frozen=True)
class PolicySnapshot:
    unknown_block: int
    unknown_soft: int
    time_pressure_days: int

    def to_dict(self) -> Dict[str, int]:
        return {
            "UNKNOWN_BLOCK": self.unknown_block,
            "UNKNOWN_SOFT": self.unknown_soft,
            "TIME_PRESSURE_DAYS": self.time_pressure_days,
        }


@contextmanager
def temporary_policy_override(
    *, unknown_block: Optional[int], time_pressure_days: Optional[int]
) -> Iterator[PolicySnapshot]:
    """Temporarily override policy constants in-process without env vars."""

    original = PolicySnapshot(
        unknown_block=int(policy_v1.UNKNOWN_BLOCK),
        unknown_soft=int(policy_v1.UNKNOWN_SOFT),
        time_pressure_days=int(policy_v1.TIME_PRESSURE_DAYS),
    )

    try:
        if unknown_block is not None:
            policy_v1.UNKNOWN_BLOCK = int(unknown_block)
            orchestrator.UNKNOWN_BLOCK = int(unknown_block)
        if time_pressure_days is not None:
            policy_v1.TIME_PRESSURE_DAYS = int(time_pressure_days)
            orchestrator.TIME_PRESSURE_DAYS = int(time_pressure_days)

        yield PolicySnapshot(
            unknown_block=int(policy_v1.UNKNOWN_BLOCK),
            unknown_soft=int(policy_v1.UNKNOWN_SOFT),
            time_pressure_days=int(policy_v1.TIME_PRESSURE_DAYS),
        )
    finally:
        policy_v1.UNKNOWN_BLOCK = original.unknown_block
        policy_v1.UNKNOWN_SOFT = original.unknown_soft
        policy_v1.TIME_PRESSURE_DAYS = original.time_pressure_days
        orchestrator.UNKNOWN_BLOCK = original.unknown_block
        orchestrator.TIME_PRESSURE_DAYS = original.time_pressure_days


def _scenario_files(scenarios_dir: Path) -> List[Path]:
    return sorted(
        p
        for p in scenarios_dir.glob("case_*.yaml")
        if p.is_file() and not p.name.endswith("_expected.yaml")
    )


def _compose_metrics(output: Dict[str, Any]) -> Dict[str, Any]:
    for step in output.get("trace", {}).get("steps", []):
        if step.get("name") == "compose_output":
            metrics = step.get("metrics")
            return metrics if isinstance(metrics, dict) else {}
    return {}


def _parse_metrics(output: Dict[str, Any]) -> Dict[str, Any]:
    for step in output.get("trace", {}).get("steps", []):
        if step.get("name") == "parse_input":
            metrics = step.get("metrics")
            return metrics if isinstance(metrics, dict) else {}
    return {}


def _case_record(case_path: Path, output: Dict[str, Any]) -> Dict[str, Any]:
    parse_metrics = _parse_metrics(output)
    compose_metrics = _compose_metrics(output)
    recommendation = output.get("recommendation", {})
    return {
        "case_file": case_path.name,
        "case_id": output.get("case_ref", {}).get("case_id"),
        "features": {
            "unknowns_count": int(parse_metrics.get("unknowns_count", 0) or 0),
            "stakeholders_count": int(parse_metrics.get("stakeholders_count", 0) or 0),
            "days_to_deadline": parse_metrics.get("days_to_deadline"),
        },
        "arbitration_code": compose_metrics.get("arbitration_code"),
        "recommendation": {
            "status": recommendation.get("status"),
            "recommended_option_id": recommendation.get("recommended_option_id"),
            "confidence": recommendation.get("confidence"),
        },
        "rules_fired": list(compose_metrics.get("rules_fired", [])),
        "planning_rules_fired": list(compose_metrics.get("rules_fired_planning", [])),
        "question_ids": [
            q.get("question_id")
            for q in output.get("questions", [])
            if isinstance(q, dict) and isinstance(q.get("question_id"), str)
        ],
        "policy_snapshot": dict(compose_metrics.get("policy_snapshot", {})),
    }


def _planning_rules_summary(
    records: Sequence[Dict[str, Any]],
    *,
    two_track_rule_id: str = "PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN",
    top_n: int = 5,
) -> Dict[str, Any]:
    frequency: Dict[str, int] = {}
    two_track_triggered_cases = 0
    for record in records:
        rules = [
            rule_id
            for rule_id in record.get("planning_rules_fired", [])
            if isinstance(rule_id, str)
        ]
        if two_track_rule_id in rules:
            two_track_triggered_cases += 1
        for rule_id in rules:
            frequency[rule_id] = frequency.get(rule_id, 0) + 1

    sorted_frequency = sorted(
        frequency.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return {
        "two_track_rule_id": two_track_rule_id,
        "two_track_triggered_cases": two_track_triggered_cases,
        "planning_rule_frequency_top": [
            {"rule_id": rule_id, "count": count}
            for rule_id, count in sorted_frequency[:top_n]
        ],
    }




def _rule_pack_summary(
    records: Sequence[Dict[str, Any]],
    *,
    pack_name: str,
    rule_ids: Sequence[str],
) -> Dict[str, Any]:
    total_cases = len(records)
    case_counts: Dict[str, int] = {rule_id: 0 for rule_id in rule_ids}

    for record in records:
        fired = {
            rule_id
            for rule_id in (
                list(record.get("rules_fired", []))
                + list(record.get("planning_rules_fired", []))
            )
            if isinstance(rule_id, str)
        }
        for rule_id in rule_ids:
            if rule_id in fired:
                case_counts[rule_id] += 1

    distribution = [
        {
            "rule_id": rule_id,
            "cases": count,
            "frequency": round((count / total_cases), 4) if total_cases else 0.0,
        }
        for rule_id, count in case_counts.items()
    ]

    return {
        "pack": pack_name,
        "total_cases": total_cases,
        "rule_case_counts": distribution,
        "triggered_case_total": sum(1 for row in distribution if row["cases"] > 0),
    }


def _rule_pack_delta(*, baseline: Dict[str, Any], variant: Dict[str, Any]) -> Dict[str, Any]:
    baseline_by_rule = {
        row.get("rule_id"): row
        for row in baseline.get("rule_case_counts", [])
        if isinstance(row, dict) and isinstance(row.get("rule_id"), str)
    }
    rows = []
    for row in variant.get("rule_case_counts", []):
        if not isinstance(row, dict) or not isinstance(row.get("rule_id"), str):
            continue
        before = baseline_by_rule.get(row["rule_id"], {})
        before_cases = int(before.get("cases", 0) or 0)
        after_cases = int(row.get("cases", 0) or 0)
        rows.append(
            {
                "rule_id": row["rule_id"],
                "baseline_cases": before_cases,
                "variant_cases": after_cases,
                "delta_cases": after_cases - before_cases,
                "baseline_frequency": float(before.get("frequency", 0.0) or 0.0),
                "variant_frequency": float(row.get("frequency", 0.0) or 0.0),
            }
        )

    return {
        "pack": variant.get("pack"),
        "rule_deltas": rows,
    }

def _load_traceability_index(path: Path) -> Dict[str, Dict[str, set[str]]]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    reqs = payload.get("requirements", [])
    idx: Dict[str, Dict[str, set[str]]] = {}
    for req in reqs:
        req_id = req.get("id")
        if not isinstance(req_id, str):
            continue
        for ref in req.get("code_refs", []):
            if not isinstance(ref, dict):
                continue
            kind = ref.get("kind")
            value = ref.get("value")
            if isinstance(kind, str) and isinstance(value, str):
                idx.setdefault(kind, {})
                idx[kind].setdefault(value, set()).add(req_id)
    return idx


def _diff_case(
    baseline: Dict[str, Any],
    variant: Dict[str, Any],
    trace_idx: Dict[str, Dict[str, set[str]]],
) -> Dict[str, Any]:
    changed_fields: List[str] = []
    if baseline.get("arbitration_code") != variant.get("arbitration_code"):
        changed_fields.append("arbitration_code")
    if baseline.get("recommendation") != variant.get("recommendation"):
        changed_fields.append("recommendation")
    if baseline.get("rules_fired") != variant.get("rules_fired"):
        changed_fields.append("rules_fired")
    if baseline.get("planning_rules_fired") != variant.get("planning_rules_fired"):
        changed_fields.append("planning_rules_fired")
    if baseline.get("policy_snapshot") != variant.get("policy_snapshot"):
        changed_fields.append("policy_snapshot")

    impacted: set[str] = set()
    for code in [baseline.get("arbitration_code"), variant.get("arbitration_code")]:
        if isinstance(code, str):
            impacted.update(trace_idx.get("arbitration_code", {}).get(code, set()))

    base_rules = set(baseline.get("rules_fired", []))
    var_rules = set(variant.get("rules_fired", []))
    base_rules.update(baseline.get("planning_rules_fired", []))
    var_rules.update(variant.get("planning_rules_fired", []))
    for rule_id in sorted(base_rules | var_rules):
        impacted.update(trace_idx.get("rule_id", {}).get(rule_id, set()))

    base_questions = set(baseline.get("question_ids", []))
    var_questions = set(variant.get("question_ids", []))
    for question_id in sorted(base_questions | var_questions):
        impacted.update(trace_idx.get("question_id", {}).get(question_id, set()))

    if changed_fields:
        impacted.update(trace_idx.get("module", {}).get("src/pocore/policy_v1.py", set()))
        impacted.update(
            trace_idx.get("module", {}).get(
                "src/pocore/engines/recommendation_v1.py", set()
            )
        )

    return {
        "case_file": variant.get("case_file"),
        "case_id": variant.get("case_id"),
        "changed": bool(changed_fields),
        "changed_fields": changed_fields,
        "baseline": baseline,
        "variant": variant,
        "impacted_requirements": sorted(impacted),
    }


def run_policy_lab(args: argparse.Namespace) -> Dict[str, Any]:
    scenarios_dir = Path(args.scenarios_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    scenario_files = _scenario_files(scenarios_dir)

    baseline_snapshot = PolicySnapshot(
        unknown_block=int(policy_v1.UNKNOWN_BLOCK),
        unknown_soft=int(policy_v1.UNKNOWN_SOFT),
        time_pressure_days=int(policy_v1.TIME_PRESSURE_DAYS),
    )

    baseline_records: Dict[str, Dict[str, Any]] = {}
    variant_records: Dict[str, Dict[str, Any]] = {}

    if args.compare_baseline:
        for case_path in scenario_files:
            out = run_case_file(case_path, seed=args.seed, now=args.now, deterministic=True)
            baseline_records[case_path.name] = _case_record(case_path, out)

    with temporary_policy_override(
        unknown_block=args.unknown_block,
        time_pressure_days=args.time_pressure_days,
    ) as active_snapshot:
        for case_path in scenario_files:
            out = run_case_file(case_path, seed=args.seed, now=args.now, deterministic=True)
            variant_records[case_path.name] = _case_record(case_path, out)
            if not variant_records[case_path.name]["policy_snapshot"]:
                variant_records[case_path.name]["policy_snapshot"] = active_snapshot.to_dict()

    result: Dict[str, Any] = {
        "meta": {
            "tool": "policy_lab_v1",
            "now": args.now,
            "seed": int(args.seed),
            "scenarios_dir": str(scenarios_dir),
            "baseline_policy": baseline_snapshot.to_dict(),
            "variant_policy": {
                "UNKNOWN_BLOCK": int(args.unknown_block),
                "UNKNOWN_SOFT": baseline_snapshot.unknown_soft,
                "TIME_PRESSURE_DAYS": int(args.time_pressure_days),
            },
            "compare_baseline": bool(args.compare_baseline),
            "cases_total": len(scenario_files),
        },
        "cases": [],
    }

    if args.compare_baseline:
        trace_idx = _load_traceability_index(Path("docs/traceability/traceability_v1.yaml"))
        diffs = [
            _diff_case(baseline_records[name], variant_records[name], trace_idx)
            for name in sorted(variant_records)
        ]
        planning_summary = _planning_rules_summary(
            [variant_records[name] for name in sorted(variant_records)]
        )
        baseline_values_pack = _rule_pack_summary(
            [baseline_records[name] for name in sorted(baseline_records)],
            pack_name="values",
            rule_ids=VALUES_PACK_RULE_IDS,
        )
        variant_values_pack = _rule_pack_summary(
            [variant_records[name] for name in sorted(variant_records)],
            pack_name="values",
            rule_ids=VALUES_PACK_RULE_IDS,
        )
        baseline_conflict_pack = _rule_pack_summary(
            [baseline_records[name] for name in sorted(baseline_records)],
            pack_name="conflict",
            rule_ids=CONFLICT_PACK_RULE_IDS,
        )
        variant_conflict_pack = _rule_pack_summary(
            [variant_records[name] for name in sorted(variant_records)],
            pack_name="conflict",
            rule_ids=CONFLICT_PACK_RULE_IDS,
        )
        result["cases"] = diffs
        result["summary"] = {
            "changed_cases": sum(1 for d in diffs if d["changed"]),
            "impacted_requirements": sorted(
                {req for d in diffs for req in d["impacted_requirements"]}
            ),
            **planning_summary,
            "values_pack": {
                "baseline": baseline_values_pack,
                "variant": variant_values_pack,
                "delta": _rule_pack_delta(
                    baseline=baseline_values_pack, variant=variant_values_pack
                ),
            },
            "conflict_pack": {
                "baseline": baseline_conflict_pack,
                "variant": variant_conflict_pack,
                "delta": _rule_pack_delta(
                    baseline=baseline_conflict_pack, variant=variant_conflict_pack
                ),
            },
        }
    else:
        result["cases"] = [variant_records[name] for name in sorted(variant_records)]
        result["summary"] = {
            "values_pack": {
                "variant": _rule_pack_summary(
                    [variant_records[name] for name in sorted(variant_records)],
                    pack_name="values",
                    rule_ids=VALUES_PACK_RULE_IDS,
                )
            },
            "conflict_pack": {
                "variant": _rule_pack_summary(
                    [variant_records[name] for name in sorted(variant_records)],
                    pack_name="conflict",
                    rule_ids=CONFLICT_PACK_RULE_IDS,
                )
            },
        }

    json_path = output_dir / "policy_lab_report.json"
    md_path = output_dir / "policy_lab_report.md"
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    md_path.write_text(_render_markdown(result), encoding="utf-8")

    return {
        "json": str(json_path),
        "md": str(md_path),
        "result": result,
    }


def _render_markdown(report: Dict[str, Any]) -> str:
    meta = report.get("meta", {})
    lines = [
        "# Policy Lab v1 Report",
        "",
        f"- now: `{meta.get('now')}`",
        f"- seed: `{meta.get('seed')}`",
        f"- compare_baseline: `{meta.get('compare_baseline')}`",
        f"- baseline_policy: `{meta.get('baseline_policy')}`",
        f"- variant_policy: `{meta.get('variant_policy')}`",
        "",
    ]

    summary = report.get("summary")
    if isinstance(summary, dict):
        lines.extend(
            [
                "## Summary",
                f"- changed_cases: **{summary.get('changed_cases', 0)}**",
                "- impacted_requirements: "
                + (", ".join(summary.get("impacted_requirements", [])) or "(none)"),
                f"- planning two-track triggered cases ({summary.get('two_track_rule_id', 'PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN')}): **{summary.get('two_track_triggered_cases', 0)}**",
                "",
            ]
        )

        top_rules = summary.get("planning_rule_frequency_top")
        if top_rules is not None:
            lines.append("### Planning rule frequency (top)")
            if isinstance(top_rules, list) and top_rules:
                for row in top_rules:
                    lines.append(
                        f"- `{row.get('rule_id', 'unknown_rule')}`: {row.get('count', 0)}"
                    )
            else:
                lines.append("- (none)")
            lines.append("")

        for key in ("values_pack", "conflict_pack"):
            pack_block = summary.get(key, {})
            variant = pack_block.get("variant", {}) if isinstance(pack_block, dict) else {}
            lines.append(f"### {key.replace('_', ' ').title()} rule frequency")
            for row in variant.get("rule_case_counts", []):
                lines.append(
                    f"- `{row.get('rule_id', 'unknown_rule')}`: {row.get('cases', 0)} cases ({row.get('frequency', 0.0):.2%})"
                )
            if not variant.get("rule_case_counts"):
                lines.append("- (none)")
            lines.append("")

            delta = pack_block.get("delta") if isinstance(pack_block, dict) else None
            if isinstance(delta, dict) and delta.get("rule_deltas"):
                lines.append(
                    f"#### {key.replace('_', ' ').title()} baseline delta (--compare-baseline)"
                )
                for row in delta.get("rule_deltas", []):
                    lines.append(
                        "- `{}`: {} → {} (Δ {:+d})".format(
                            row.get("rule_id", "unknown_rule"),
                            row.get("baseline_cases", 0),
                            row.get("variant_cases", 0),
                            row.get("delta_cases", 0),
                        )
                    )
                lines.append("")

    lines.append("## Case Results")
    lines.append("")
    for case in report.get("cases", []):
        lines.append(
            f"### {case.get('case_file')} ({case.get('case_id', 'unknown_case_id')})"
        )
        if "baseline" in case and "variant" in case:
            lines.append(f"- changed: `{case.get('changed')}`")
            lines.append(
                "- changed_fields: "
                + (", ".join(case.get("changed_fields", [])) or "(none)")
            )
            lines.append(
                "- impacted_requirements: "
                + (", ".join(case.get("impacted_requirements", [])) or "(none)")
            )
            lines.append(
                f"- baseline arbitration/recommendation: `{case['baseline'].get('arbitration_code')}` / `{case['baseline'].get('recommendation', {}).get('status')}`"
            )
            lines.append(
                f"- variant arbitration/recommendation: `{case['variant'].get('arbitration_code')}` / `{case['variant'].get('recommendation', {}).get('status')}`"
            )
        else:
            lines.append(
                f"- arbitration/recommendation: `{case.get('arbitration_code')}` / `{case.get('recommendation', {}).get('status')}`"
            )
            lines.append(f"- rules_fired: {case.get('rules_fired', [])}")
        lines.append("")

    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Policy Lab v1")
    parser.add_argument("--unknown-block", type=int, default=policy_v1.UNKNOWN_BLOCK)
    parser.add_argument(
        "--time-pressure-days", type=int, default=policy_v1.TIME_PRESSURE_DAYS
    )
    parser.add_argument("--now", default=DEFAULT_NOW)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scenarios-dir", default="scenarios")
    parser.add_argument("--output-dir", default="reports/policy_lab")
    parser.add_argument("--compare-baseline", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    run_policy_lab(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
