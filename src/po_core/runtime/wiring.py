"""
Dependency Wiring
=================

Assembles concrete implementations and provides dependency injection.

This is the ONLY file that should:
1. Import concrete implementations from adapters/
2. Create instances with specific configurations
3. Wire dependencies together

Core modules receive dependencies as parameters, not through imports.

Usage:
    from po_core.runtime import get_container

    container = get_container()
    result = container.ensemble.run(prompt)
"""

from dataclasses import dataclass
from typing import Optional

from po_core.ports.memory import MemoryPort, InMemoryMemory
from po_core.runtime.settings import Settings, get_settings


@dataclass
class Container:
    """
    Dependency injection container.

    Holds all wired dependencies for the application.
    Access components via this container, not direct imports.
    """

    settings: Settings
    memory: MemoryPort

    # Lazy-loaded components
    _gate: Optional["WethicsGate"] = None
    _two_stage_gate: Optional["TwoStageGate"] = None
    _solar_will: Optional["SolarWillEngine"] = None
    _intention_gate: Optional["IntentionGate"] = None

    @property
    def gate(self) -> "WethicsGate":
        """Get the safety gate (lazy loaded)."""
        if self._gate is None:
            from po_core.safety.wethics_gate import WethicsGate, GateConfig

            config = GateConfig(
                tau_reject=self.settings.safety.tau_reject,
                tau_repair=self.settings.safety.tau_repair,
                max_repairs=self.settings.safety.max_repairs,
                tau_drift_reject=self.settings.safety.tau_drift_reject,
                tau_drift_escalate=self.settings.safety.tau_drift_escalate,
                strict_no_escalate=self.settings.safety.strict_no_escalate,
            )
            self._gate = WethicsGate(config=config)
        return self._gate

    @property
    def two_stage_gate(self) -> "TwoStageGate":
        """Get the 2-stage ethics gate (lazy loaded)."""
        if self._two_stage_gate is None:
            from po_core.safety.wethics_gate import TwoStageGate, GateConfig

            config = GateConfig(
                tau_reject=self.settings.safety.tau_reject,
                tau_repair=self.settings.safety.tau_repair,
                max_repairs=self.settings.safety.max_repairs,
            )
            self._two_stage_gate = TwoStageGate(config=config)
        return self._two_stage_gate

    @property
    def solar_will(self) -> "SolarWillEngine":
        """Get the Solar Will engine (lazy loaded)."""
        if self._solar_will is None:
            from po_core.autonomy.solarwill import SolarWillEngine

            self._solar_will = SolarWillEngine(
                learning_rate=self.settings.solar_will.learning_rate
            )
        return self._solar_will

    @property
    def intention_gate(self) -> "IntentionGate":
        """Get the intention gate (lazy loaded)."""
        if self._intention_gate is None:
            from po_core.safety.wethics_gate.intention_gate import IntentionGate

            self._intention_gate = IntentionGate()
        return self._intention_gate

    def run_ensemble(
        self,
        prompt: str,
        philosophers: Optional[list] = None,
    ) -> dict:
        """
        Run the ensemble with proper dependency injection.

        Args:
            prompt: The input prompt
            philosophers: Optional list of philosopher names

        Returns:
            Ensemble result dictionary
        """
        from po_core.ensemble import run_ensemble

        return run_ensemble(
            prompt,
            philosophers=philosophers or self.settings.ensemble.default_philosophers,
            enable_tracer=self.settings.ensemble.enable_tracer,
        )


# Global container instance
_container: Optional[Container] = None


def get_container(settings: Optional[Settings] = None) -> Container:
    """
    Get the global container instance.

    Creates and wires all dependencies on first call.

    Args:
        settings: Optional settings override

    Returns:
        Wired Container instance
    """
    global _container

    if _container is None or settings is not None:
        settings = settings or get_settings()
        memory = _create_memory(settings)
        _container = Container(
            settings=settings,
            memory=memory,
        )

    return _container


def configure(settings: Settings) -> Container:
    """
    Configure the container with specific settings.

    Useful for testing or different configurations.

    Args:
        settings: Settings to use

    Returns:
        New Container instance
    """
    global _container
    _container = None  # Reset
    return get_container(settings)


def _create_memory(settings: Settings) -> MemoryPort:
    """
    Create the memory implementation based on settings.

    Args:
        settings: Application settings

    Returns:
        MemoryPort implementation
    """
    # For now, use PoSelfMemoryAdapter by default
    # Can switch based on settings.experiment_mode
    if settings.debug:
        # Use in-memory for testing
        return InMemoryMemory()

    try:
        from po_core.adapters import PoSelfMemoryAdapter
        return PoSelfMemoryAdapter()
    except ImportError:
        # Fallback to in-memory if Po_self not available
        return InMemoryMemory()


# Type hints for lazy properties (for IDE support)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from po_core.safety.wethics_gate import WethicsGate, TwoStageGate
    from po_core.safety.wethics_gate.intention_gate import IntentionGate
    from po_core.autonomy.solarwill import SolarWillEngine


def create_default_container(settings: Optional[Settings] = None) -> Container:
    """
    Create a new container with default or provided settings.

    Unlike get_container(), this always creates a fresh container
    (no global state).

    Args:
        settings: Optional settings override

    Returns:
        New Container instance
    """
    settings = settings or get_settings()
    memory = _create_memory(settings)
    return Container(
        settings=settings,
        memory=memory,
    )


__all__ = [
    "Container",
    "get_container",
    "configure",
    "create_default_container",
]
