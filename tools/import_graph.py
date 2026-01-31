#!/usr/bin/env python3
"""
Import Graph Analyzer
=====================

Analyzes import dependencies in src/po_core and detects:
1. Circular dependencies
2. Forbidden imports (violating dependency rules)
3. Dependency graph statistics

これが回れば"腸捻転"が数字で見える。

Usage:
    python tools/import_graph.py --check --print

Exit code:
    0: No violations or cycles
    1: Violations or cycles detected
"""

from __future__ import annotations

import argparse
import ast
import os
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple


@dataclass(frozen=True)
class Rule:
    """Forbidden import rule."""
    src_prefix: str
    dst_prefix: str
    message: str


# Dependency rules (INVIOLABLE)
DEFAULT_RULES: List[Rule] = [
    # Core isolation
    Rule("po_core.safety", "po_core.philosophers", "safety/** must not import philosophers/**"),
    Rule("po_core.tensors", "po_core.safety", "tensors/** must not import safety/**"),
    Rule("po_core.viewer", "po_core.philosophers", "viewer/** must not import philosophers/**"),
    Rule("po_core.viewer", "po_core.tensors", "viewer/** must not import tensors/**"),
    Rule("po_core.trace", "po_core.philosophers", "trace/** must not import philosophers/**"),
    Rule("po_core.trace", "po_core.tensors", "trace/** must not import tensors/**"),

    # domain は外に出ない（domain→domain は許可）
    Rule("po_core.domain", "po_core.", "domain/** must not import po_core/**"),

    # ports は domain と ports 以外を見たらアウト
    Rule("po_core.ports", "po_core.tensors", "ports/** must not import tensors/**"),
    Rule("po_core.ports", "po_core.safety", "ports/** must not import safety/**"),
    Rule("po_core.ports", "po_core.philosophers", "ports/** must not import philosophers/**"),
    Rule("po_core.ports", "po_core.autonomy", "ports/** must not import autonomy/**"),
    Rule("po_core.ports", "po_core.runtime", "ports/** must not import runtime/**"),
    Rule("po_core.ports", "po_core.app", "ports/** must not import app/**"),
    Rule("po_core.ports", "po_core.adapters", "ports/** must not import adapters/**"),
    Rule("po_core.ports", "po_core.aggregator", "ports/** must not import aggregator/**"),
    Rule("po_core.ports", "po_core.trace", "ports/** must not import trace/**"),
]


def iter_py_files(root: str) -> Iterable[str]:
    """Iterate over all Python files in a directory."""
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def module_name_from_path(root: str, package: str, path: str) -> str:
    """Convert a file path to a module name."""
    rel = os.path.relpath(path, root)
    rel = rel.replace(os.sep, "/")
    if rel.endswith(".py"):
        rel = rel[:-3]
    if rel.endswith("/__init__"):
        rel = rel[:-9]
    rel = rel.strip("/").replace("/", ".")
    return package if rel == "" else f"{package}.{rel}"


def resolve_import(
    current: str,
    module: Optional[str],
    level: int,
    package: str,
) -> Optional[str]:
    """
    Resolve an import to its full module path.

    Args:
        current: Current module (po_core.a.b.c)
        module: Import target ("x.y" or None)
        level: 0=absolute, 1=from . import..., 2=from .. import...
        package: Base package name (po_core)
    """
    if level == 0:
        if module is None:
            return None
        return module if module.startswith(package + ".") or module == package else None

    # Relative import
    parts = current.split(".")
    # Drop the module leaf (current file module)
    base = parts[:-1]
    # Go up (level-1) packages
    up = max(0, len(base) - (level - 1))
    base = base[:up]
    if not base:
        return package if module is None else (module if module.startswith(package) else None)

    prefix = ".".join(base)
    if module is None:
        return prefix
    return f"{prefix}.{module}"


def extract_deps(py_path: str, current_module: str, package: str) -> Set[str]:
    """Extract po_core dependencies from a Python file."""
    with open(py_path, "r", encoding="utf-8") as f:
        src = f.read()

    try:
        tree = ast.parse(src, filename=py_path)
    except SyntaxError:
        return set()

    deps: Set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if name == package or name.startswith(package + "."):
                    deps.add(name)
        elif isinstance(node, ast.ImportFrom):
            target = resolve_import(current_module, node.module, node.level, package)
            if target and (target == package or target.startswith(package + ".")):
                deps.add(target)

    # Normalize: keep only package-scoped deps
    return {d for d in deps if d == package or d.startswith(package + ".")}


def build_graph(root: str, package: str) -> Dict[str, Set[str]]:
    """Build the full dependency graph."""
    graph: Dict[str, Set[str]] = {}
    for fp in iter_py_files(root):
        mod = module_name_from_path(root, package, fp)
        deps = extract_deps(fp, mod, package)
        graph.setdefault(mod, set()).update(deps)
    return graph


def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find cycles in the dependency graph using DFS."""
    cycles: List[List[str]] = []
    state: Dict[str, int] = {}  # 0=unseen, 1=visiting, 2=done
    stack: List[str] = []

    def dfs(n: str) -> None:
        state[n] = 1
        stack.append(n)
        for m in graph.get(n, set()):
            if m not in graph:
                continue
            s = state.get(m, 0)
            if s == 0:
                dfs(m)
            elif s == 1:
                # Found cycle
                idx = stack.index(m)
                cyc = stack[idx:] + [m]
                cycles.append(cyc)
        stack.pop()
        state[n] = 2

    for node in graph.keys():
        if state.get(node, 0) == 0:
            dfs(node)

    # Canonicalize cycles to reduce duplicates
    uniq: List[List[str]] = []
    seen: Set[Tuple[str, ...]] = set()
    for c in cycles:
        key = tuple(c)
        if key not in seen:
            seen.add(key)
            uniq.append(c)
    return uniq


def check_rules(graph: Dict[str, Set[str]], rules: List[Rule]) -> List[str]:
    """Check for forbidden imports based on rules."""
    violations: List[str] = []
    for src, dsts in graph.items():
        for dst in dsts:
            for r in rules:
                if not (src.startswith(r.src_prefix) and dst.startswith(r.dst_prefix)):
                    continue

                # allow domain -> domain imports
                if r.src_prefix == "po_core.domain" and dst.startswith("po_core.domain"):
                    continue

                # allow ports -> domain imports
                if r.src_prefix == "po_core.ports" and dst.startswith("po_core.domain"):
                    continue

                # allow ports -> ports imports
                if r.src_prefix == "po_core.ports" and dst.startswith("po_core.ports"):
                    continue

                violations.append(f"{r.message}: {src} -> {dst}")
    return violations


def get_module_category(module: str) -> str:
    """Get the category (top-level package under po_core) for a module."""
    parts = module.split(".")
    if len(parts) >= 2:
        return parts[1]
    return "root"


def analyze_graph(graph: Dict[str, Set[str]]) -> Dict:
    """Analyze the dependency graph and return statistics."""
    from collections import defaultdict

    # Count modules per category
    categories: Dict[str, int] = defaultdict(int)
    for module in graph:
        cat = get_module_category(module)
        categories[cat] += 1

    # Count cross-category dependencies
    cross_deps: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for module, imports in graph.items():
        src_cat = get_module_category(module)
        for imp in imports:
            dst_cat = get_module_category(imp)
            if src_cat != dst_cat:
                cross_deps[src_cat][dst_cat] += 1

    return {
        "total_modules": len(graph),
        "modules_per_category": dict(categories),
        "cross_category_dependencies": {k: dict(v) for k, v in cross_deps.items()},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Import graph analyzer for Po_core")
    ap.add_argument("--root", default="src/po_core", help="Root directory to analyze")
    ap.add_argument("--package", default="po_core", help="Package name")
    ap.add_argument("--check", action="store_true", help="Exit non-zero if violations/cycles exist")
    ap.add_argument("--print", dest="print_output", action="store_true", help="Print summary")
    args = ap.parse_args()

    # Resolve root path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    root = os.path.join(project_root, args.root)

    if not os.path.exists(root):
        print(f"Error: {root} not found", file=sys.stderr)
        return 1

    graph = build_graph(root, args.package)
    cycles = find_cycles(graph)
    violations = check_rules(graph, DEFAULT_RULES)

    if args.print_output or args.check:
        print(f"[import-graph] modules: {len(graph)}")

        if violations:
            print(f"[import-graph] rule violations: {len(violations)}")
            for v in violations[:200]:
                print("  -", v)
            if len(violations) > 200:
                print(f"  ... ({len(violations) - 200} more)")
        else:
            print("[import-graph] rule violations: 0")

        if cycles:
            print(f"[import-graph] cycles detected: {len(cycles)}")
            for c in cycles[:50]:
                print("  - cycle:", " -> ".join(c))
            if len(cycles) > 50:
                print(f"  ... ({len(cycles) - 50} more)")
        else:
            print("[import-graph] cycles detected: 0")

        # Print stats
        stats = analyze_graph(graph)
        print(f"\nModules per category:")
        for cat, count in sorted(stats["modules_per_category"].items()):
            print(f"  {cat}: {count}")

        print(f"\nCross-category dependencies:")
        for src, dsts in sorted(stats["cross_category_dependencies"].items()):
            for dst, count in sorted(dsts.items()):
                print(f"  {src} -> {dst}: {count}")

    if args.check and (violations or cycles):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
