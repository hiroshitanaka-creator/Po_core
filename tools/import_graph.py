#!/usr/bin/env python3
"""
Import Graph Analyzer
=====================

Analyzes import dependencies in src/po_core and detects:
1. Circular dependencies
2. Forbidden imports (violating dependency rules)
3. Dependency graph statistics

Usage:
    python tools/import_graph.py

Output:
- Dependency graph (JSON)
- Circular dependencies (if any)
- Rule violations
"""

import ast
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# Dependency rules: module -> list of forbidden import patterns
FORBIDDEN_IMPORTS = {
    "po_core.domain": [
        "po_core.philosophers",
        "po_core.tensors",
        "po_core.safety",
        "po_core.trace",
        "po_core.viewer",
        "po_core.ensemble",
        "po_core.autonomy",
    ],
    "po_core.tensors": [
        "po_core.philosophers",
        "po_core.safety",
    ],
    "po_core.safety": [
        "po_core.philosophers",
    ],
    "po_core.trace": [
        "po_core.philosophers",
    ],
    "po_core.viewer": [
        "po_core.philosophers",
        "po_core.tensors",
        "po_core.safety",
    ],
}


def get_module_name(filepath: Path, base_dir: Path) -> str:
    """Convert filepath to module name."""
    rel_path = filepath.relative_to(base_dir)
    parts = list(rel_path.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace(".py", "")
    return ".".join(parts)


def get_imports_from_file(filepath: Path) -> Set[str]:
    """Extract all po_core imports from a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"  Warning: Could not parse {filepath}: {e}", file=sys.stderr)
        return set()

    imports: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("po_core"):
                    imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("po_core"):
                imports.add(node.module)
    return imports


def build_dependency_graph(src_dir: Path) -> Dict[str, Set[str]]:
    """Build the full dependency graph."""
    graph: Dict[str, Set[str]] = defaultdict(set)

    for py_file in src_dir.rglob("*.py"):
        module_name = get_module_name(py_file, src_dir.parent)
        imports = get_imports_from_file(py_file)
        for imp in imports:
            graph[module_name].add(imp)

    return dict(graph)


def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find all cycles in the dependency graph using DFS."""
    cycles: List[List[str]] = []
    visited: Set[str] = set()
    rec_stack: Set[str] = set()
    path: List[str] = []

    def dfs(node: str) -> None:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, set()):
            # Normalize to module level for comparison
            neighbor_base = ".".join(neighbor.split(".")[:3])  # po_core.X.Y

            if neighbor_base in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor_base) if neighbor_base in path else -1
                if cycle_start >= 0:
                    cycle = path[cycle_start:] + [neighbor_base]
                    # Normalize cycle to avoid duplicates
                    min_idx = cycle.index(min(cycle))
                    normalized = cycle[min_idx:] + cycle[:min_idx]
                    if normalized not in cycles:
                        cycles.append(normalized)
            elif neighbor_base not in visited:
                dfs(neighbor_base)

        path.pop()
        rec_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return cycles


def check_forbidden_imports(graph: Dict[str, Set[str]]) -> List[Tuple[str, str, str]]:
    """Check for imports that violate dependency rules."""
    violations: List[Tuple[str, str, str]] = []

    for module, imports in graph.items():
        # Find which rule category this module belongs to
        for rule_prefix, forbidden_list in FORBIDDEN_IMPORTS.items():
            if module.startswith(rule_prefix):
                for imp in imports:
                    for forbidden in forbidden_list:
                        if imp.startswith(forbidden):
                            violations.append((module, imp, f"{rule_prefix} -> {forbidden}"))

    return violations


def get_module_category(module: str) -> str:
    """Get the category (top-level package under po_core) for a module."""
    parts = module.split(".")
    if len(parts) >= 2:
        return parts[1]
    return "root"


def analyze_graph(graph: Dict[str, Set[str]]) -> Dict:
    """Analyze the dependency graph and return statistics."""
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


def main():
    # Find src directory
    script_dir = Path(__file__).parent
    src_dir = script_dir.parent / "src" / "po_core"

    if not src_dir.exists():
        print(f"Error: {src_dir} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing: {src_dir}")
    print("=" * 60)

    # Build graph
    graph = build_dependency_graph(src_dir)

    # Analyze
    stats = analyze_graph(graph)
    print(f"\nTotal modules: {stats['total_modules']}")
    print(f"\nModules per category:")
    for cat, count in sorted(stats['modules_per_category'].items()):
        print(f"  {cat}: {count}")

    print(f"\nCross-category dependencies:")
    for src, dsts in sorted(stats['cross_category_dependencies'].items()):
        for dst, count in sorted(dsts.items()):
            print(f"  {src} -> {dst}: {count}")

    # Check for cycles
    print("\n" + "=" * 60)
    print("Checking for cycles...")
    cycles = find_cycles(graph)
    if cycles:
        print(f"\n⚠️  Found {len(cycles)} cycle(s):")
        for cycle in cycles:
            print(f"  {'  ->  '.join(cycle)}")
    else:
        print("\n✅ No cycles detected!")

    # Check forbidden imports
    print("\n" + "=" * 60)
    print("Checking forbidden imports...")
    violations = check_forbidden_imports(graph)
    if violations:
        print(f"\n⚠️  Found {len(violations)} violation(s):")
        for module, imp, rule in violations:
            print(f"  {module}")
            print(f"    imports: {imp}")
            print(f"    violates: {rule}")
            print()
    else:
        print("\n✅ No forbidden import violations!")

    # Output detailed graph
    print("\n" + "=" * 60)
    print("Dependency details (po_core only):")
    for module in sorted(graph.keys()):
        po_core_imports = [i for i in graph[module] if i.startswith("po_core")]
        if po_core_imports:
            print(f"\n{module}:")
            for imp in sorted(po_core_imports):
                print(f"  -> {imp}")

    return 0 if (not cycles and not violations) else 1


if __name__ == "__main__":
    sys.exit(main())
