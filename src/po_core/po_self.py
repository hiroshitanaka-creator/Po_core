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
    ) -> None:
        self.philosophers = list(philosophers) if philosophers is not None else DEFAULT_PHILOSOPHERS
        self.enable_trace = enable_trace
        self.po_trace = PoTrace() if enable_trace else None

    def generate(self, prompt: str) -> PoSelfResponse:
        """Run the ensemble and emit a structured response."""

        # Create trace session if enabled
        session_id = None
        if self.po_trace:
            session_id = self.po_trace.create_session(
                prompt=prompt,
                philosophers=self.philosophers,
                metadata={"source": "po_self.generate"},
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

        # Add session_id to log
        log = ensemble_result.get("log", {})
        if session_id:
            log["session_id"] = session_id

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
