"""
Phase Transition Analysis
==========================

Identify critical points where meaning generation undergoes
non-linear jumps (phase transitions) in philosophical reasoning.

Analyzes:
- F_P (Freedom Pressure) discontinuities
- Semantic Delta sudden shifts
- Critical thresholds and conditions
- Emergence patterns
"""

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from po_core.po_trace_db import PoTraceDB

console = Console()


class PhaseTransitionAnalyzer:
    """Analyze phase transitions in philosophical reasoning."""

    def __init__(self, trace_db: PoTraceDB):
        """Initialize analyzer."""
        self.trace_db = trace_db
        self.transitions = []

    def detect_phase_transitions(
        self, session_ids: List[str] = None, sensitivity: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Detect phase transitions in reasoning sessions.

        A phase transition is characterized by:
        1. Sudden jump in F_P or Semantic Delta (> sensitivity * σ)
        2. Change in reasoning pattern
        3. Emergence of new meaning

        Args:
            session_ids: List of session IDs to analyze (None = all recent)
            sensitivity: Threshold multiplier (higher = fewer detections)

        Returns:
            List of detected transitions
        """
        console.print("\n[cyan]🔍 Detecting Phase Transitions...[/cyan]\n")

        # Get sessions
        if session_ids is None:
            sessions_meta = self.trace_db.list_sessions(limit=100)
            session_ids = [s["session_id"] for s in sessions_meta]

        # Load session data
        sessions = []
        for sid in session_ids:
            session = self.trace_db.get_session(sid)
            if session:
                sessions.append(session)

        if len(sessions) < 2:
            console.print("[yellow]Not enough sessions for analysis[/yellow]")
            return []

        # Extract time series
        fp_series = [s.metrics.get("freedom_pressure", 0.5) for s in sessions]
        sd_series = [s.metrics.get("semantic_delta", 0.5) for s in sessions]
        bt_series = [s.metrics.get("blocked_tensor", 0.3) for s in sessions]

        # Calculate statistics
        fp_mean, fp_std = self._mean_std(fp_series)
        sd_mean, sd_std = self._mean_std(sd_series)

        # Detect transitions
        transitions = []

        for i in range(1, len(sessions)):
            session_curr = sessions[i]
            session_prev = sessions[i - 1]

            fp_curr = fp_series[i]
            fp_prev = fp_series[i - 1]
            sd_curr = sd_series[i]
            sd_prev = sd_series[i - 1]
            bt_curr = bt_series[i]
            bt_prev = bt_series[i - 1]

            # Calculate changes
            fp_change = abs(fp_curr - fp_prev)
            sd_change = abs(sd_curr - sd_prev)
            bt_change = abs(bt_curr - bt_prev)

            # Check if change exceeds threshold
            fp_threshold = sensitivity * fp_std
            sd_threshold = sensitivity * sd_std

            is_fp_jump = fp_change > fp_threshold
            is_sd_jump = sd_change > sd_threshold

            if is_fp_jump or is_sd_jump:
                # Characterize the transition
                transition_type = self._characterize_transition(
                    fp_change, sd_change, bt_change, fp_threshold, sd_threshold
                )

                transition = {
                    "session_index": i,
                    "session_id": session_curr.session_id,
                    "previous_session_id": session_prev.session_id,
                    "prompt": session_curr.prompt[:100],
                    "type": transition_type,
                    "fp_change": round(fp_change, 4),
                    "sd_change": round(sd_change, 4),
                    "bt_change": round(bt_change, 4),
                    "fp_threshold": round(fp_threshold, 4),
                    "sd_threshold": round(sd_threshold, 4),
                    "significance": self._calculate_significance(
                        fp_change, sd_change, fp_threshold, sd_threshold
                    ),
                    "metrics_before": {
                        "freedom_pressure": round(fp_prev, 4),
                        "semantic_delta": round(sd_prev, 4),
                        "blocked_tensor": round(bt_prev, 4),
                    },
                    "metrics_after": {
                        "freedom_pressure": round(fp_curr, 4),
                        "semantic_delta": round(sd_curr, 4),
                        "blocked_tensor": round(bt_curr, 4),
                    },
                }

                transitions.append(transition)

        self.transitions = transitions

        console.print(f"[green]✓ Found {len(transitions)} phase transitions[/green]\n")

        return transitions

    def _mean_std(self, series: List[float]) -> Tuple[float, float]:
        """Calculate mean and standard deviation."""
        if not series:
            return 0.0, 0.0

        mean = sum(series) / len(series)
        variance = sum((x - mean) ** 2 for x in series) / len(series)
        std = math.sqrt(variance)

        return mean, std

    def _characterize_transition(
        self,
        fp_change: float,
        sd_change: float,
        bt_change: float,
        fp_threshold: float,
        sd_threshold: float,
    ) -> str:
        """
        Characterize the type of phase transition.

        Types:
        - "Freedom Surge": Large F_P increase
        - "Semantic Shift": Large Semantic Delta change
        - "Dialectical Jump": Both F_P and SD jump
        - "Emergence": F_P + SD increase, BT decrease
        - "Constraint": F_P decrease, BT increase
        """
        fp_jump = fp_change > fp_threshold
        sd_jump = sd_change > sd_threshold

        if fp_jump and sd_jump:
            if bt_change > 0.1:
                return "Dialectical Jump"
            else:
                return "Emergence"
        elif fp_jump:
            return "Freedom Surge"
        elif sd_jump:
            return "Semantic Shift"
        else:
            return "Minor Transition"

    def _calculate_significance(
        self,
        fp_change: float,
        sd_change: float,
        fp_threshold: float,
        sd_threshold: float,
    ) -> float:
        """
        Calculate significance score of transition.

        Higher score = more significant transition.
        """
        fp_sig = fp_change / fp_threshold if fp_threshold > 0 else 0
        sd_sig = sd_change / sd_threshold if sd_threshold > 0 else 0

        return round(max(fp_sig, sd_sig), 2)

    def identify_critical_conditions(self) -> Dict[str, Any]:
        """
        Identify critical conditions that lead to phase transitions.

        Returns:
            Dictionary of critical thresholds and patterns
        """
        console.print("\n[cyan]🎯 Identifying Critical Conditions...[/cyan]\n")

        if not self.transitions:
            console.print("[yellow]No transitions to analyze[/yellow]")
            return {}

        # Analyze conditions before transitions
        pre_fp = [t["metrics_before"]["freedom_pressure"] for t in self.transitions]
        pre_sd = [t["metrics_before"]["semantic_delta"] for t in self.transitions]
        pre_bt = [t["metrics_before"]["blocked_tensor"] for t in self.transitions]

        # Calculate critical thresholds
        critical_conditions = {
            "total_transitions": len(self.transitions),
            "transition_types": self._count_transition_types(),
            "critical_thresholds": {
                "freedom_pressure": {
                    "mean": round(sum(pre_fp) / len(pre_fp), 4),
                    "min": round(min(pre_fp), 4),
                    "max": round(max(pre_fp), 4),
                },
                "semantic_delta": {
                    "mean": round(sum(pre_sd) / len(pre_sd), 4),
                    "min": round(min(pre_sd), 4),
                    "max": round(max(pre_sd), 4),
                },
                "blocked_tensor": {
                    "mean": round(sum(pre_bt) / len(pre_bt), 4),
                    "min": round(min(pre_bt), 4),
                    "max": round(max(pre_bt), 4),
                },
            },
            "most_significant": self._find_most_significant(),
        }

        return critical_conditions

    def _count_transition_types(self) -> Dict[str, int]:
        """Count occurrences of each transition type."""
        types = {}
        for t in self.transitions:
            t_type = t["type"]
            types[t_type] = types.get(t_type, 0) + 1
        return types

    def _find_most_significant(self) -> Dict[str, Any]:
        """Find the most significant transition."""
        if not self.transitions:
            return {}

        most_sig = max(self.transitions, key=lambda t: t["significance"])

        return {
            "session_id": most_sig["session_id"],
            "type": most_sig["type"],
            "significance": most_sig["significance"],
            "prompt": most_sig["prompt"],
        }

    def display_transitions(self):
        """Display detected transitions."""
        console.print("\n" + "=" * 80)
        console.print("[bold magenta]⚡ Phase Transitions Detected[/bold magenta]")
        console.print("=" * 80 + "\n")

        if not self.transitions:
            console.print("[yellow]No transitions detected[/yellow]")
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", justify="right", style="cyan", width=3)
        table.add_column("Type", style="yellow", width=18)
        table.add_column("Significance", justify="right", style="green", width=12)
        table.add_column("ΔF_P", justify="right", style="magenta", width=8)
        table.add_column("ΔSD", justify="right", style="blue", width=8)
        table.add_column("Prompt", style="white", width=40)

        for i, t in enumerate(self.transitions, 1):
            table.add_row(
                str(i),
                t["type"],
                f"{t['significance']:.2f}x",
                f"{t['fp_change']:.3f}",
                f"{t['sd_change']:.3f}",
                t["prompt"][:37] + "..." if len(t["prompt"]) > 37 else t["prompt"],
            )

        console.print(table)

    def display_critical_conditions(self, conditions: Dict[str, Any]):
        """Display critical conditions analysis."""
        console.print("\n" + "=" * 80)
        console.print("[bold green]🎯 Critical Conditions[/bold green]")
        console.print("=" * 80 + "\n")

        tree = Tree("[bold]Phase Transition Analysis[/bold]")

        # Overall stats
        stats_branch = tree.add(
            f"[cyan]Total Transitions:[/cyan] {conditions['total_transitions']}"
        )

        # Transition types
        types_branch = tree.add("[yellow]Transition Types:[/yellow]")
        for t_type, count in conditions["transition_types"].items():
            types_branch.add(f"{t_type}: {count}")

        # Critical thresholds
        thresholds_branch = tree.add(
            "[green]Critical Thresholds (Pre-Transition):[/green]"
        )
        for metric, values in conditions["critical_thresholds"].items():
            metric_branch = thresholds_branch.add(f"{metric}:")
            metric_branch.add(f"Mean: {values['mean']:.4f}")
            metric_branch.add(f"Range: [{values['min']:.4f}, {values['max']:.4f}]")

        # Most significant
        most_sig = conditions["most_significant"]
        if most_sig:
            sig_branch = tree.add(f"[magenta]Most Significant Transition:[/magenta]")
            sig_branch.add(f"Type: {most_sig['type']}")
            sig_branch.add(f"Significance: {most_sig['significance']:.2f}x threshold")
            sig_branch.add(f"Prompt: {most_sig['prompt']}")

        console.print(tree)

    def save_analysis(self, conditions: Dict[str, Any], filename: str = None):
        """Save phase transition analysis."""
        if filename is None:
            from datetime import datetime

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"phase_transitions_{timestamp}.json"

        output_path = Path(__file__).parent / "results" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "analysis_type": "phase_transitions",
            "transitions": self.transitions,
            "critical_conditions": conditions,
        }

        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

        console.print(f"\n[green]✓ Analysis saved to:[/green] {output_path}")

        return output_path


def main():
    """Main function to run phase transition analysis."""
    console.print("\n[bold magenta]🔬 Phase Transition Analysis[/bold magenta]")
    console.print("[bold]Detecting Non-linear Jumps in Meaning Generation[/bold]\n")

    # Initialize
    trace_db = PoTraceDB()
    analyzer = PhaseTransitionAnalyzer(trace_db)

    # Detect transitions
    transitions = analyzer.detect_phase_transitions(sensitivity=1.5)

    # Display results
    analyzer.display_transitions()

    # Identify critical conditions
    conditions = analyzer.identify_critical_conditions()
    analyzer.display_critical_conditions(conditions)

    # Save results
    analyzer.save_analysis(conditions)

    # Summary
    console.print("\n" + "=" * 80)
    console.print("[bold green]✅ Phase Transition Analysis Complete![/bold green]")
    console.print("=" * 80)

    if transitions:
        console.print(
            Panel(
                f"""
[bold cyan]Key Findings:[/bold cyan]

• Phase Transitions Detected: {len(transitions)}
• Emergence Events: {conditions['transition_types'].get('Emergence', 0)}
• Freedom Surges: {conditions['transition_types'].get('Freedom Surge', 0)}
• Semantic Shifts: {conditions['transition_types'].get('Semantic Shift', 0)}

[bold yellow]Critical Threshold (F_P):[/bold yellow]
  Mean: {conditions['critical_thresholds']['freedom_pressure']['mean']:.4f}
  Range: [{conditions['critical_thresholds']['freedom_pressure']['min']:.4f},
          {conditions['critical_thresholds']['freedom_pressure']['max']:.4f}]

[bold magenta]Insight:[/bold magenta]
Non-linear jumps indicate moments where the philosophical system
generates genuinely new meaning through collective reasoning.
            """,
                title="[bold green]Analysis Results[/bold green]",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                "[yellow]No phase transitions detected. Try:\n"
                "1. Run more diverse reasoning sessions\n"
                "2. Decrease sensitivity threshold\n"
                "3. Use different philosophical combinations[/yellow]",
                title="[bold yellow]Recommendations[/bold yellow]",
                border_style="yellow",
            )
        )


if __name__ == "__main__":
    main()
