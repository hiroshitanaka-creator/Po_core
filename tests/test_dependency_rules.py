"""
Dependency Rules Enforcement Tests
==================================

These tests enforce the architectural dependency rules.
If a module imports something it shouldn't, these tests fail.

INVIOLABLE RULES:
1. domain/ imports NOTHING from po_core (only stdlib)
2. tensors/ does NOT import from philosophers/ or safety/
3. safety/ does NOT import from philosophers/
4. philosophers/ does NOT import from safety/ or tensors/ (directly)

The dependency graph should be:
    domain/ <- tensors/ <- ensemble.py
    domain/ <- philosophers/ <- ensemble.py
    domain/ <- safety/ <- ensemble.py
    domain/ <- trace/ <- ensemble.py

NOT:
    tensors/ -> philosophers/
    tensors/ -> safety/
    safety/ -> philosophers/
    domain/ -> anything in po_core
"""
import ast
import os
from pathlib import Path
from typing import List, Set, Tuple


def get_imports_from_file(filepath: Path) -> Set[str]:
    """Extract all imports from a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
    except (SyntaxError, UnicodeDecodeError):
        return set()

    imports: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
                # Also track sub-imports
                for alias in node.names:
                    if alias.name != "*":
                        imports.add(f"{node.module}.{alias.name}")
    return imports


def get_all_imports_in_directory(directory: Path) -> List[Tuple[Path, Set[str]]]:
    """Get all imports from all Python files in a directory."""
    results = []
    for py_file in directory.rglob("*.py"):
        imports = get_imports_from_file(py_file)
        results.append((py_file, imports))
    return results


def imports_match_pattern(imports: Set[str], pattern: str) -> Set[str]:
    """Find imports that match a pattern (e.g., 'po_core.philosophers')."""
    return {imp for imp in imports if pattern in imp}


class TestDependencyRules:
    """Tests to enforce import rules."""

    def setup_method(self):
        """Set up paths for testing."""
        # Find the src directory
        self.src_dir = Path(__file__).parent.parent / "src" / "po_core"
        assert self.src_dir.exists(), f"src directory not found at {self.src_dir}"

    def test_domain_has_no_po_core_imports(self):
        """domain/ must not import anything from po_core."""
        domain_dir = self.src_dir / "domain"
        if not domain_dir.exists():
            return  # Domain not yet created

        violations = []
        for py_file, imports in get_all_imports_in_directory(domain_dir):
            po_core_imports = imports_match_pattern(imports, "po_core")
            # domain.* imports are OK (internal), but not other po_core.*
            external_po_core = {
                imp for imp in po_core_imports
                if not imp.startswith("po_core.domain")
            }
            if external_po_core:
                violations.append((py_file, external_po_core))

        assert not violations, (
            f"domain/ must not import from po_core (except domain/): "
            f"{[(str(f), list(v)) for f, v in violations]}"
        )

    def test_tensors_does_not_import_philosophers(self):
        """tensors/ must not import from philosophers/."""
        tensors_dir = self.src_dir / "tensors"
        if not tensors_dir.exists():
            return

        violations = []
        for py_file, imports in get_all_imports_in_directory(tensors_dir):
            philosopher_imports = imports_match_pattern(imports, "po_core.philosophers")
            if philosopher_imports:
                violations.append((py_file, philosopher_imports))

        assert not violations, (
            f"tensors/ must not import from philosophers/: "
            f"{[(str(f), list(v)) for f, v in violations]}"
        )

    def test_tensors_does_not_import_safety(self):
        """tensors/ must not import from safety/."""
        tensors_dir = self.src_dir / "tensors"
        if not tensors_dir.exists():
            return

        violations = []
        for py_file, imports in get_all_imports_in_directory(tensors_dir):
            safety_imports = imports_match_pattern(imports, "po_core.safety")
            if safety_imports:
                violations.append((py_file, safety_imports))

        assert not violations, (
            f"tensors/ must not import from safety/: "
            f"{[(str(f), list(v)) for f, v in violations]}"
        )

    def test_safety_does_not_import_philosophers(self):
        """safety/ must not import from philosophers/."""
        safety_dir = self.src_dir / "safety"
        if not safety_dir.exists():
            return

        violations = []
        for py_file, imports in get_all_imports_in_directory(safety_dir):
            philosopher_imports = imports_match_pattern(imports, "po_core.philosophers")
            if philosopher_imports:
                violations.append((py_file, philosopher_imports))

        assert not violations, (
            f"safety/ must not import from philosophers/: "
            f"{[(str(f), list(v)) for f, v in violations]}"
        )

    def test_trace_does_not_import_philosophers_directly(self):
        """trace/ should not import philosophers/ directly (only via domain types)."""
        trace_dir = self.src_dir / "trace"
        if not trace_dir.exists():
            return

        violations = []
        for py_file, imports in get_all_imports_in_directory(trace_dir):
            philosopher_imports = imports_match_pattern(imports, "po_core.philosophers")
            if philosopher_imports:
                violations.append((py_file, philosopher_imports))

        assert not violations, (
            f"trace/ should not import from philosophers/ directly: "
            f"{[(str(f), list(v)) for f, v in violations]}"
        )


class TestArchitecturalLayers:
    """Tests to verify architectural layering."""

    def setup_method(self):
        """Set up paths for testing."""
        self.src_dir = Path(__file__).parent.parent / "src" / "po_core"

    def test_domain_layer_exists(self):
        """domain/ directory should exist."""
        domain_dir = self.src_dir / "domain"
        assert domain_dir.exists(), "domain/ directory not found"

    def test_domain_exports_core_types(self):
        """domain/__init__.py should export core types."""
        from po_core.domain import (
            Context,
            Proposal,
            TensorSnapshot,
            SafetyVerdict,
            TraceEvent,
        )
        assert Context is not None
        assert Proposal is not None
        assert TensorSnapshot is not None
        assert SafetyVerdict is not None
        assert TraceEvent is not None

    def test_tensors_engine_exists(self):
        """tensors/engine.py should exist."""
        engine_file = self.src_dir / "tensors" / "engine.py"
        assert engine_file.exists(), "tensors/engine.py not found"

    def test_tensors_engine_returns_domain_types(self):
        """tensors engine should return domain types."""
        from po_core.tensors import compute_tensors
        from po_core.domain import TensorSnapshot

        result = compute_tensors("test prompt")
        assert isinstance(result, TensorSnapshot)

    def test_philosophers_base_has_contract(self):
        """philosophers/base.py should define the contract types."""
        from po_core.philosophers.base import (
            Philosopher,
            PhilosopherResponse,
            Context,
            normalize_response,
        )
        assert Philosopher is not None
        assert PhilosopherResponse is not None
        assert Context is not None
        assert normalize_response is not None


class TestNoCircularImports:
    """Tests to detect circular import issues."""

    def test_can_import_all_core_modules(self):
        """All core modules should be importable without circular import errors."""
        # These imports should not raise ImportError
        import po_core.domain
        import po_core.tensors
        import po_core.philosophers
        import po_core.safety
        import po_core.ensemble

    def test_domain_imports_cleanly(self):
        """domain/ should import without dependencies."""
        # This should work even if other modules have issues
        from po_core.domain import (
            Context,
            Proposal,
            TensorSnapshot,
            SafetyVerdict,
            TraceEvent,
        )
