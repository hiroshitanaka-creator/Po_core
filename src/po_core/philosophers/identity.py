"""Philosopher identity resolution.

Provides a single, authoritative function for mapping a philosopher instance to
its stable identity string used in RunResult, ExecOutcome, and trace provenance.

No runtime or API dependencies — safe to import from any layer.
"""

from __future__ import annotations

_CANONICAL_IDS: frozenset[str] | None = None


def _canonical_ids() -> frozenset[str]:
    global _CANONICAL_IDS
    if _CANONICAL_IDS is None:
        from po_core.philosophers.manifest import SPECS  # lazy, avoids import-time cost

        _CANONICAL_IDS = frozenset(s.philosopher_id for s in SPECS if s.enabled)
    return _CANONICAL_IDS


def resolve_philosopher_id(ph: object) -> str:
    """Return the stable identity string for *ph*.

    Resolution order (first non-empty value wins):

    1. ``ph.philosopher_id`` — explicitly set by PhilosopherRegistry.load() for
       manifest philosophers; also usable by custom implementations.
    2. Canonical manifest ID derived from the module path when the philosopher
       lives inside ``po_core.philosophers.*``
       (e.g. ``po_core.philosophers.aristotle`` → ``"aristotle"``).
    3. ``ph.name`` — raw display name used by unregistered test doubles.
    4. Class name — last-resort so the field is never empty.
    """
    # Priority 1: explicit attribute set by registry or custom code
    pid = getattr(ph, "philosopher_id", None)
    if pid and isinstance(pid, str):
        return pid

    # Priority 2: canonical module-path derivation for production philosophers
    module = getattr(type(ph), "__module__", "") or ""
    if module.startswith("po_core.philosophers."):
        candidate = module.rpartition(".")[2]
        if candidate and candidate in _canonical_ids():
            return candidate

    # Priority 3: .name attribute (test doubles, legacy classes)
    name = getattr(ph, "name", None)
    if name and isinstance(name, str):
        return name

    # Priority 4: class name
    return type(ph).__name__
