"""
Runtime Settings
================

Configuration and feature flags for Po_core.

Settings are loaded from:
1. Default values (this file)
2. Environment variables (PO_CORE_*)
3. Config file (po_core.toml or po_core.json)

DEPENDENCY RULES:
- This file depends ONLY on: stdlib
- No imports from other po_core modules
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SafetySettings:
    """Settings for the safety/wethics_gate system."""

    # Gate thresholds
    tau_reject: float = 0.6
    tau_repair: float = 0.3
    max_repairs: int = 2

    # Drift detection
    tau_drift_reject: float = 0.7
    tau_drift_escalate: float = 0.4

    # Strict mode (escalate -> reject)
    strict_no_escalate: bool = False

    # Enable 2-stage gate
    enable_intention_gate: bool = True


@dataclass
class EnsembleSettings:
    """Settings for the ensemble system."""

    # Default philosophers
    default_philosophers: List[str] = field(
        default_factory=lambda: ["aristotle", "kant", "nietzsche"]
    )

    # Enable tracing
    enable_tracer: bool = True

    # Enable advanced metrics
    enable_advanced_metrics: bool = True


@dataclass
class SolarWillSettings:
    """Settings for the Solar Will autonomy system."""

    # Learning rate for will updates
    learning_rate: float = 0.3

    # Maximum goals to generate
    max_goals: int = 3

    # Enable Solar Will integration
    enabled: bool = True


@dataclass
class TraceSettings:
    """Settings for tracing and logging."""

    # Default trace directory
    trace_dir: Path = field(default_factory=lambda: Path("traces"))

    # Trace verbosity level
    verbosity: str = "INFO"  # DEBUG, INFO, WARNING, ERROR

    # Persist traces to disk
    persist: bool = True


@dataclass
class Settings:
    """
    Master settings for Po_core.

    Load order:
    1. Default values
    2. Environment variables (PO_CORE_*)
    3. Config file overrides
    """

    safety: SafetySettings = field(default_factory=SafetySettings)
    ensemble: EnsembleSettings = field(default_factory=EnsembleSettings)
    solar_will: SolarWillSettings = field(default_factory=SolarWillSettings)
    trace: TraceSettings = field(default_factory=TraceSettings)

    # Global settings
    debug: bool = False
    experiment_mode: str = ""  # For A/B testing

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""
        settings = cls()

        # Load debug mode
        settings.debug = os.getenv("PO_CORE_DEBUG", "").lower() in ("1", "true", "yes")

        # Load experiment mode
        settings.experiment_mode = os.getenv("PO_CORE_EXPERIMENT", "")

        # Load safety settings
        if tau_reject := os.getenv("PO_CORE_SAFETY_TAU_REJECT"):
            settings.safety.tau_reject = float(tau_reject)
        if strict := os.getenv("PO_CORE_SAFETY_STRICT"):
            settings.safety.strict_no_escalate = strict.lower() in ("1", "true", "yes")

        # Load ensemble settings
        if philosophers := os.getenv("PO_CORE_DEFAULT_PHILOSOPHERS"):
            settings.ensemble.default_philosophers = [
                p.strip() for p in philosophers.split(",")
            ]

        # Load Solar Will settings
        if learning_rate := os.getenv("PO_CORE_SOLARWILL_LEARNING_RATE"):
            settings.solar_will.learning_rate = float(learning_rate)
        if solarwill_enabled := os.getenv("PO_CORE_SOLARWILL_ENABLED"):
            settings.solar_will.enabled = solarwill_enabled.lower() in ("1", "true", "yes")

        # Load trace settings
        if trace_dir := os.getenv("PO_CORE_TRACE_DIR"):
            settings.trace.trace_dir = Path(trace_dir)
        if verbosity := os.getenv("PO_CORE_TRACE_VERBOSITY"):
            settings.trace.verbosity = verbosity.upper()

        return settings

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "debug": self.debug,
            "experiment_mode": self.experiment_mode,
            "safety": {
                "tau_reject": self.safety.tau_reject,
                "tau_repair": self.safety.tau_repair,
                "max_repairs": self.safety.max_repairs,
                "tau_drift_reject": self.safety.tau_drift_reject,
                "tau_drift_escalate": self.safety.tau_drift_escalate,
                "strict_no_escalate": self.safety.strict_no_escalate,
                "enable_intention_gate": self.safety.enable_intention_gate,
            },
            "ensemble": {
                "default_philosophers": self.ensemble.default_philosophers,
                "enable_tracer": self.ensemble.enable_tracer,
                "enable_advanced_metrics": self.ensemble.enable_advanced_metrics,
            },
            "solar_will": {
                "learning_rate": self.solar_will.learning_rate,
                "max_goals": self.solar_will.max_goals,
                "enabled": self.solar_will.enabled,
            },
            "trace": {
                "trace_dir": str(self.trace.trace_dir),
                "verbosity": self.trace.verbosity,
                "persist": self.trace.persist,
            },
        }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def configure(settings: Settings) -> None:
    """Set the global settings instance."""
    global _settings
    _settings = settings


__all__ = [
    "Settings",
    "SafetySettings",
    "EnsembleSettings",
    "SolarWillSettings",
    "TraceSettings",
    "get_settings",
    "configure",
]
