"""
Po_self: Philosophical Ensemble Module

The core reasoning engine that integrates multiple philosophers
as interacting tensors.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

import click
from rich.console import Console

from po_core.ensemble import DEFAULT_PHILOSOPHERS, run_ensemble
from po_core.po_trace import PoTrace
from po_core.safety import validate_philosopher_group, create_ethics_guardian

console = Console()


@dataclass
class PoSelfResponse:
    """Structured response returned by Po_self.generate."""

    prompt: str
    text: str
    metrics: Dict[str, float]
    philosophers: List[str]
    consensus_leader: Optional[str]
    responses: List[Dict[str, object]]
    log: Dict[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "prompt": self.prompt,
            "text": self.text,
            "metrics": self.metrics,
            "philosophers": self.philosophers,
            "consensus_leader": self.consensus_leader,
            "responses": self.responses,
            "log": self.log,
        }


class PoSelf:
    """Coordinate philosopher tensors and expose a deterministic generate API."""

    def __init__(
        self,
        *,
        philosophers: Optional[Iterable[str]] = None,
        enable_trace: bool = True,
        allow_restricted: bool = False,
        dangerous_pattern_mode: bool = False,
        enable_ethics_guardian: bool = True,
    ) -> None:
        """
        Initialize Po_self with safety validation.

        Args:
            philosophers: List of philosophers to include
            enable_trace: Enable Po_trace logging
            allow_restricted: Allow RESTRICTED tier philosophers
            dangerous_pattern_mode: Enable dangerous pattern detection mode
                                   (required when using RESTRICTED philosophers)
            enable_ethics_guardian: Enable W_ethics boundary checking
        """
        self.philosophers = list(philosophers) if philosophers is not None else DEFAULT_PHILOSOPHERS
        self.enable_trace = enable_trace
        self.po_trace = PoTrace() if enable_trace else None

        # Safety validation
        validation = validate_philosopher_group(
            self.philosophers,
            allow_restricted=allow_restricted,
            dangerous_pattern_mode=dangerous_pattern_mode,
        )

        if not validation["valid"]:
            # Raise error with detailed explanation
            error_msg = "Philosopher group validation failed:\n"
            for restriction in validation["restrictions"]:
                error_msg += f"  • {restriction}\n"

            if validation["blocked_philosophers"]:
                error_msg += f"\nBlocked philosophers: {', '.join(validation['blocked_philosophers'])}\n"
                error_msg += "\nTo use RESTRICTED tier philosophers:\n"
                error_msg += "  1. Set allow_restricted=True\n"
                error_msg += "  2. Set dangerous_pattern_mode=True\n"
                error_msg += "  3. Use only for research purposes with ethical oversight\n"

            raise ValueError(error_msg)

        # Show warnings for monitored/restricted philosophers
        if validation["warnings"]:
            for warning in validation["warnings"]:
                console.print(f"[yellow]⚠ {warning}[/yellow]")

        # Initialize W_ethics guardian
        self.ethics_guardian = create_ethics_guardian() if enable_ethics_guardian else None
        self.enable_ethics_guardian = enable_ethics_guardian
        self.allow_restricted = allow_restricted
        self.dangerous_pattern_mode = dangerous_pattern_mode

    def generate(self, prompt: str) -> PoSelfResponse:
        """Run the ensemble and emit a structured response."""

        # Create trace session if enabled
        session_id = None
        if self.po_trace:
            session_id = self.po_trace.create_session(
                prompt=prompt,
                philosophers=self.philosophers,
                metadata={
                    "source": "po_self.generate",
                    "allow_restricted": self.allow_restricted,
                    "dangerous_pattern_mode": self.dangerous_pattern_mode,
                },
            )

        ensemble_result = run_ensemble(
            prompt,
            philosophers=self.philosophers,
            po_trace=self.po_trace,
            session_id=session_id,
        )
        responses = ensemble_result.get("responses", [])
        aggregate = ensemble_result.get("aggregate", {})
        consensus = ensemble_result.get("consensus", {})

        text = consensus.get("text") or " ".join(r.get("reasoning", "") for r in responses)
        metrics: Dict[str, float] = {
            "freedom_pressure": float(aggregate.get("freedom_pressure", 0.0)),
            "semantic_delta": float(aggregate.get("semantic_delta", 0.0)),
            "blocked_tensor": float(aggregate.get("blocked_tensor", 0.0)),
        }

        # W_ethics boundary checking
        ethics_result = None
        if self.ethics_guardian:
            ethics_result = self.ethics_guardian.check_text(
                text=text,
                context=prompt,
            )

            # Add W_ethics to metrics
            metrics["w_ethics"] = ethics_result["cumulative_w_ethics"]

            # Check if session should be stopped
            if ethics_result["should_stop"]:
                console.print("[bold red]⛔ SESSION STOPPED: Ethical boundary violation[/bold red]")
                console.print(f"[red]W_ethics: {ethics_result['cumulative_w_ethics']:.3f}[/red]")
                console.print(f"[red]Violations: {ethics_result['violation_count']}[/red]")

                # Add dangerous ideology flag to log
                log = ensemble_result.get("log", {})
                log["ethics_violation"] = True
                log["dangerous_ideology_suspicion"] = ethics_result["dangerous_ideology_flag"]
                log["w_ethics_violations"] = [
                    {
                        "type": v.violation_type.value,
                        "severity": v.severity,
                        "confidence": v.confidence,
                        "matched_text": v.matched_text,
                    }
                    for v in ethics_result["violations"]
                ]

                # Raise exception to stop session
                raise RuntimeError(
                    f"Session stopped due to ethical boundary violations. "
                    f"W_ethics: {ethics_result['cumulative_w_ethics']:.3f}. "
                    f"This session has been flagged for safety review."
                )

            # Log warnings for minor violations
            if ethics_result["violation_count"] > 0:
                console.print(
                    f"[yellow]⚠ W_ethics warning: {ethics_result['violation_count']} "
                    f"potential violations detected (W_ethics: {ethics_result['cumulative_w_ethics']:.3f})[/yellow]"
                )

        # Add session_id to log
        log = ensemble_result.get("log", {})
        if session_id:
            log["session_id"] = session_id

        # Add ethics result to log
        if ethics_result:
            log["w_ethics"] = {
                "cumulative": ethics_result["cumulative_w_ethics"],
                "violation_count": ethics_result["violation_count"],
                "dangerous_ideology_flag": ethics_result["dangerous_ideology_flag"],
            }

        return PoSelfResponse(
            prompt=prompt,
            text=text,
            metrics=metrics,
            philosophers=self.philosophers,
            consensus_leader=consensus.get("leader"),
            responses=responses,
            log=log,
        )


def cli() -> None:
    """Po_self CLI entry point"""
    console.print("[bold magenta]🧠 Po_self - Philosophical Ensemble[/bold magenta]")
    console.print("Type `po-core prompt \"What is meaning?\"` to explore the ensemble.")


if __name__ == "__main__":
    cli()
