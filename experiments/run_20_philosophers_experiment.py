"""
Experiment: 20 Philosophers × 10 Sessions
==========================================

Collect statistical data on:
- F_P (Freedom Pressure) variation
- Semantic Delta evolution
- Blocked Tensor patterns
- Fulfillment convergence
- Non-linear jumps (phase transitions)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.panel import Panel

from po_core.po_self import PoSelf
from po_core.po_trace_db import PoTraceDB
from po_core.ensemble import PHILOSOPHER_REGISTRY

console = Console()


# All 20 philosophers
ALL_20_PHILOSOPHERS = list(PHILOSOPHER_REGISTRY.keys())


# Diverse test prompts to explore different reasoning patterns
TEST_PROMPTS = [
    "What is the nature of consciousness?",
    "How should we approach ethical AI development?",
    "What is the meaning of freedom in the digital age?",
    "How can we reconcile individual autonomy with collective responsibility?",
    "What is the relationship between language and reality?",
    "How should we think about death and mortality?",
    "What constitutes a good life?",
    "How do we navigate the tension between tradition and innovation?",
    "What is the role of suffering in human existence?",
    "How can we build meaningful communities in modern society?",
]


class ExperimentRunner:
    """Run controlled experiments with 20 philosophers."""

    def __init__(self, db_url: str = None):
        """Initialize experiment runner."""
        self.trace_db = PoTraceDB(db_url)
        self.results = []
        self.session_data = []

    def run_session(self, session_num: int, prompt: str) -> Dict[str, Any]:
        """
        Run a single session with all 20 philosophers.

        Returns:
            Session data with metrics and metadata
        """
        console.print(f"\n[cyan]Session {session_num + 1}/10:[/cyan] {prompt[:60]}...")

        # Create PoSelf with all 20 philosophers
        po = PoSelf(
            philosophers=ALL_20_PHILOSOPHERS,
            enable_trace=True,
            trace_backend=self.trace_db,
        )

        # Execute reasoning
        result = po.reason(prompt)

        # Extract session data
        session_data = {
            "session_num": session_num,
            "session_id": result.get("session_id"),
            "prompt": prompt,
            "philosophers": result.get("philosophers", []),
            "consensus_leader": result.get("consensus_leader"),
            "metrics": result.get("metrics", {}),
            "timestamp": datetime.utcnow().isoformat(),
            "num_philosophers": len(result.get("philosophers", [])),
        }

        # Display metrics
        metrics = result.get("metrics", {})
        console.print(f"  [green]F_P:[/green] {metrics.get('freedom_pressure', 0):.3f}")
        console.print(
            f"  [yellow]Semantic Δ:[/yellow] {metrics.get('semantic_delta', 0):.3f}"
        )
        console.print(f"  [red]Blocked:[/red] {metrics.get('blocked_tensor', 0):.3f}")
        console.print(
            f"  [magenta]Leader:[/magenta] {result.get('consensus_leader', 'N/A')}"
        )

        return session_data

    def run_experiment(self, num_sessions: int = 10) -> List[Dict[str, Any]]:
        """
        Run the full experiment.

        Args:
            num_sessions: Number of sessions to run

        Returns:
            List of session data dictionaries
        """
        console.print("\n" + "=" * 80)
        console.print(
            "[bold cyan]🔬 Experiment: 20 Philosophers × 10 Sessions[/bold cyan]"
        )
        console.print("=" * 80 + "\n")

        console.print(f"[bold]Configuration:[/bold]")
        console.print(f"  - Philosophers: {len(ALL_20_PHILOSOPHERS)} (all available)")
        console.print(f"  - Sessions: {num_sessions}")
        console.print(f"  - Database: Enabled (PoTraceDB)")
        console.print(f"  - Prompts: Diverse reasoning scenarios\n")

        results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:

            task = progress.add_task("[cyan]Running sessions...", total=num_sessions)

            for i in range(num_sessions):
                prompt = TEST_PROMPTS[i % len(TEST_PROMPTS)]
                session_data = self.run_session(i, prompt)
                results.append(session_data)
                progress.update(task, advance=1)

        self.session_data = results
        return results

    def analyze_results(self) -> Dict[str, Any]:
        """
        Analyze experimental results.

        Returns:
            Analysis dictionary with statistics
        """
        console.print("\n" + "=" * 80)
        console.print("[bold magenta]📊 Analysis Results[/bold magenta]")
        console.print("=" * 80 + "\n")

        if not self.session_data:
            console.print("[red]No data to analyze[/red]")
            return {}

        # Extract metrics time series
        fp_series = [s["metrics"].get("freedom_pressure", 0) for s in self.session_data]
        sd_series = [s["metrics"].get("semantic_delta", 0) for s in self.session_data]
        bt_series = [s["metrics"].get("blocked_tensor", 0) for s in self.session_data]

        # Calculate statistics
        analysis = {
            "total_sessions": len(self.session_data),
            "freedom_pressure": {
                "mean": sum(fp_series) / len(fp_series),
                "min": min(fp_series),
                "max": max(fp_series),
                "range": max(fp_series) - min(fp_series),
                "variance": self._variance(fp_series),
                "series": fp_series,
            },
            "semantic_delta": {
                "mean": sum(sd_series) / len(sd_series),
                "min": min(sd_series),
                "max": max(sd_series),
                "range": max(sd_series) - min(sd_series),
                "variance": self._variance(sd_series),
                "series": sd_series,
            },
            "blocked_tensor": {
                "mean": sum(bt_series) / len(bt_series),
                "min": min(bt_series),
                "max": max(bt_series),
                "range": max(bt_series) - min(bt_series),
                "variance": self._variance(bt_series),
                "series": bt_series,
            },
            "consensus_leaders": self._analyze_leaders(),
            "jumps": self._detect_jumps(fp_series, sd_series),
        }

        self._display_analysis(analysis)

        return analysis

    def _variance(self, series: List[float]) -> float:
        """Calculate variance of a series."""
        if not series:
            return 0.0
        mean = sum(series) / len(series)
        return sum((x - mean) ** 2 for x in series) / len(series)

    def _analyze_leaders(self) -> Dict[str, int]:
        """Analyze consensus leader distribution."""
        leaders = {}
        for session in self.session_data:
            leader = session.get("consensus_leader")
            if leader:
                leaders[leader] = leaders.get(leader, 0) + 1
        return leaders

    def _detect_jumps(
        self, fp_series: List[float], sd_series: List[float]
    ) -> List[Dict]:
        """
        Detect non-linear jumps (potential phase transitions).

        A jump is defined as a change > 2 * standard deviation.
        """
        jumps = []

        # Calculate threshold for F_P
        fp_std = self._variance(fp_series) ** 0.5
        fp_threshold = 2 * fp_std

        # Calculate threshold for Semantic Delta
        sd_std = self._variance(sd_series) ** 0.5
        sd_threshold = 2 * sd_std

        for i in range(1, len(fp_series)):
            fp_change = abs(fp_series[i] - fp_series[i - 1])
            sd_change = abs(sd_series[i] - sd_series[i - 1])

            if fp_change > fp_threshold or sd_change > sd_threshold:
                jumps.append(
                    {
                        "session": i,
                        "fp_change": fp_change,
                        "sd_change": sd_change,
                        "fp_threshold": fp_threshold,
                        "sd_threshold": sd_threshold,
                        "type": "F_P" if fp_change > fp_threshold else "Semantic",
                    }
                )

        return jumps

    def _display_analysis(self, analysis: Dict[str, Any]):
        """Display analysis results."""
        # Metrics table
        metrics_table = Table(
            title="[bold]Metric Statistics[/bold]",
            show_header=True,
            header_style="bold cyan",
        )

        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Mean", justify="right", style="green")
        metrics_table.add_column("Min", justify="right", style="yellow")
        metrics_table.add_column("Max", justify="right", style="yellow")
        metrics_table.add_column("Range", justify="right", style="magenta")
        metrics_table.add_column("Variance", justify="right", style="red")

        for metric_name in ["freedom_pressure", "semantic_delta", "blocked_tensor"]:
            data = analysis[metric_name]
            metrics_table.add_row(
                metric_name.replace("_", " ").title(),
                f"{data['mean']:.4f}",
                f"{data['min']:.4f}",
                f"{data['max']:.4f}",
                f"{data['range']:.4f}",
                f"{data['variance']:.6f}",
            )

        console.print(metrics_table)

        # Consensus leaders
        console.print("\n[bold]Consensus Leaders:[/bold]")
        leaders = analysis["consensus_leaders"]
        for leader, count in sorted(leaders.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]:
            console.print(f"  {leader}: {count} sessions")

        # Jumps
        console.print(
            f"\n[bold]Non-linear Jumps Detected:[/bold] {len(analysis['jumps'])}"
        )
        if analysis["jumps"]:
            console.print("[yellow]Potential phase transitions:[/yellow]")
            for jump in analysis["jumps"]:
                console.print(
                    f"  Session {jump['session']}: "
                    f"{jump['type']} jump (Δ={jump.get('fp_change', jump.get('sd_change')):.4f})"
                )

    def save_results(self, filename: str = None):
        """Save experimental results to JSON file."""
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"experiment_20phil_{timestamp}.json"

        output_path = Path(__file__).parent / "results" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "experiment": "20_philosophers_10_sessions",
            "timestamp": datetime.utcnow().isoformat(),
            "configuration": {
                "num_philosophers": len(ALL_20_PHILOSOPHERS),
                "philosophers": ALL_20_PHILOSOPHERS,
                "num_sessions": len(self.session_data),
            },
            "sessions": self.session_data,
            "analysis": self.analyze_results(),
        }

        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

        console.print(f"\n[green]✓ Results saved to:[/green] {output_path}")

        return output_path


def main():
    """Main function to run the experiment."""
    console.print("\n[bold magenta]🔬 Po_core Research Experiment[/bold magenta]")
    console.print(
        "[bold]Objective:[/bold] Study F_P variation, jumps, and convergence patterns\n"
    )

    # Run experiment
    runner = ExperimentRunner()
    results = runner.run_experiment(num_sessions=10)

    # Analyze
    analysis = runner.analyze_results()

    # Save
    output_file = runner.save_results()

    # Final summary
    console.print("\n" + "=" * 80)
    console.print("[bold green]✅ Experiment Complete![/bold green]")
    console.print("=" * 80)

    console.print(
        Panel(
            f"""
[bold cyan]Experiment Summary:[/bold cyan]

• Total Sessions: {len(results)}
• Philosophers: {len(ALL_20_PHILOSOPHERS)} (all available)
• Database Records: {len(results)} sessions stored
• Non-linear Jumps: {len(analysis.get('jumps', []))} detected
• Data File: {output_file.name}

[bold yellow]Next Steps:[/bold yellow]
1. Visualize F_P evolution over sessions
2. Analyze philosopher correlation patterns
3. Identify phase transition conditions
        """,
            title="[bold green]Experiment Results[/bold green]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()
