"""
Philosopher Correlation Analysis
=================================

Analyze correlation patterns between philosophers:
- Who agrees/disagrees with whom
- Complementary vs. opposing relationships
- Metric co-variation patterns
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

from po_core.po_trace_db import PoTraceDB

console = Console()


class PhilosopherCorrelationAnalyzer:
    """Analyze correlations between philosophers."""

    def __init__(self, trace_db: PoTraceDB):
        """Initialize analyzer with database."""
        self.trace_db = trace_db

    def calculate_correlation_matrix(self, min_sessions: int = 5) -> Dict[str, Any]:
        """
        Calculate correlation matrix between all philosophers.

        Args:
            min_sessions: Minimum number of shared sessions required

        Returns:
            Correlation matrix and metadata
        """
        console.print("\n[cyan]Calculating philosopher correlation matrix...[/cyan]\n")

        # Get all sessions
        sessions = self.trace_db.list_sessions(limit=1000)

        # Build philosopher co-occurrence matrix
        philosopher_sessions = {}  # philosopher -> list of (session_id, metrics)
        philosopher_pairs = {}  # (phil1, phil2) -> list of metric correlations

        for session_meta in sessions:
            session = self.trace_db.get_session(session_meta["session_id"])
            if not session or not session.philosophers:
                continue

            # Record each philosopher's participation
            for phil in session.philosophers:
                if phil not in philosopher_sessions:
                    philosopher_sessions[phil] = []
                philosopher_sessions[phil].append(
                    {
                        "session_id": session.session_id,
                        "metrics": session.metrics,
                    }
                )

        # Calculate pairwise correlations
        philosophers = sorted(philosopher_sessions.keys())

        correlation_matrix = {}
        for i, phil1 in enumerate(philosophers):
            correlation_matrix[phil1] = {}
            for phil2 in philosophers:
                if phil1 == phil2:
                    correlation_matrix[phil1][phil2] = 1.0  # Perfect self-correlation
                else:
                    corr = self._calculate_pairwise_correlation(
                        phil1, phil2, philosopher_sessions, min_sessions
                    )
                    correlation_matrix[phil1][phil2] = corr

        return {
            "matrix": correlation_matrix,
            "philosophers": philosophers,
            "total_sessions": len(sessions),
            "philosopher_count": len(philosophers),
        }

    def _calculate_pairwise_correlation(
        self, phil1: str, phil2: str, philosopher_sessions: Dict, min_sessions: int
    ) -> float:
        """
        Calculate correlation between two philosophers.

        Based on metric co-variation when they appear together.
        """
        # Find sessions where both appear
        sessions1 = {
            s["session_id"]: s["metrics"] for s in philosopher_sessions.get(phil1, [])
        }
        sessions2 = {
            s["session_id"]: s["metrics"] for s in philosopher_sessions.get(phil2, [])
        }

        shared_sessions = set(sessions1.keys()) & set(sessions2.keys())

        if len(shared_sessions) < min_sessions:
            return 0.0  # Not enough data

        # Calculate correlation based on Freedom Pressure co-variation
        # Higher correlation = they tend to agree (similar F_P)
        # Lower correlation = they tend to disagree (different F_P)

        fp_differences = []
        for session_id in shared_sessions:
            fp1 = sessions1[session_id].get("freedom_pressure", 0.5)
            fp2 = sessions2[session_id].get("freedom_pressure", 0.5)
            # Smaller difference = higher agreement
            fp_differences.append(abs(fp1 - fp2))

        if not fp_differences:
            return 0.0

        # Convert difference to correlation
        # avg_diff = 0 → correlation = 1.0
        # avg_diff = 1 → correlation = -1.0
        avg_diff = sum(fp_differences) / len(fp_differences)
        correlation = 1.0 - (2.0 * avg_diff)  # Map [0, 1] to [1, -1]

        return round(correlation, 3)

    def identify_clusters(
        self, correlation_matrix: Dict[str, Dict[str, float]], threshold: float = 0.5
    ) -> List[List[str]]:
        """
        Identify clusters of highly correlated philosophers.

        Args:
            correlation_matrix: Correlation matrix
            threshold: Minimum correlation for clustering

        Returns:
            List of philosopher clusters
        """
        philosophers = list(correlation_matrix.keys())
        visited = set()
        clusters = []

        def dfs(phil: str, cluster: List[str]):
            """Depth-first search to find connected philosophers."""
            visited.add(phil)
            cluster.append(phil)

            for other_phil in philosophers:
                if other_phil not in visited:
                    corr = correlation_matrix[phil].get(other_phil, 0.0)
                    if corr >= threshold:
                        dfs(other_phil, cluster)

        for phil in philosophers:
            if phil not in visited:
                cluster = []
                dfs(phil, cluster)
                if len(cluster) > 1:  # Only clusters with > 1 member
                    clusters.append(cluster)

        return clusters

    def find_oppositions(
        self, correlation_matrix: Dict[str, Dict[str, float]], threshold: float = -0.3
    ) -> List[Tuple[str, str, float]]:
        """
        Find opposing philosopher pairs (negative correlation).

        Args:
            correlation_matrix: Correlation matrix
            threshold: Maximum correlation (negative) for opposition

        Returns:
            List of (phil1, phil2, correlation) tuples
        """
        oppositions = []
        philosophers = list(correlation_matrix.keys())

        for i, phil1 in enumerate(philosophers):
            for phil2 in philosophers[i + 1 :]:
                corr = correlation_matrix[phil1].get(phil2, 0.0)
                if corr <= threshold:
                    oppositions.append((phil1, phil2, corr))

        # Sort by correlation (most negative first)
        oppositions.sort(key=lambda x: x[2])

        return oppositions

    def display_heatmap_ascii(self, correlation_matrix: Dict[str, Dict[str, float]]):
        """Display correlation heatmap in ASCII art."""
        console.print("\n" + "=" * 80)
        console.print("[bold magenta]📊 Philosopher Correlation Heatmap[/bold magenta]")
        console.print("=" * 80 + "\n")

        philosophers = sorted(correlation_matrix.keys())

        # Create table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Philosopher", style="cyan", width=15)

        # Add column for each philosopher (abbreviated)
        for phil in philosophers:
            table.add_column(phil[:4], justify="center", width=5)

        # Add rows
        for phil1 in philosophers:
            row = [phil1[:15]]
            for phil2 in philosophers:
                corr = correlation_matrix[phil1].get(phil2, 0.0)
                # Color code: green = positive, red = negative
                if corr > 0.7:
                    cell = f"[green]{corr:.2f}[/green]"
                elif corr > 0.3:
                    cell = f"[yellow]{corr:.2f}[/yellow]"
                elif corr > -0.3:
                    cell = f"[white]{corr:.2f}[/white]"
                else:
                    cell = f"[red]{corr:.2f}[/red]"
                row.append(cell)
            table.add_row(*row)

        console.print(table)

        console.print("\n[bold]Legend:[/bold]")
        console.print(
            "  [green]Green (>0.7):[/green] Strong positive correlation (complementary)"
        )
        console.print("  [yellow]Yellow (0.3-0.7):[/yellow] Moderate correlation")
        console.print("  [white]White (-0.3-0.3):[/white] Weak/no correlation")
        console.print("  [red]Red (<-0.3):[/red] Negative correlation (opposing)")

    def display_clusters(self, clusters: List[List[str]]):
        """Display philosopher clusters."""
        console.print("\n" + "=" * 80)
        console.print(
            "[bold green]🔗 Philosopher Clusters (Complementary Groups)[/bold green]"
        )
        console.print("=" * 80 + "\n")

        for i, cluster in enumerate(clusters, 1):
            console.print(f"[bold cyan]Cluster {i}:[/bold cyan] {', '.join(cluster)}")

    def display_oppositions(self, oppositions: List[Tuple[str, str, float]]):
        """Display opposing philosopher pairs."""
        console.print("\n" + "=" * 80)
        console.print("[bold red]⚔️  Opposing Pairs (Dialectical Tension)[/bold red]")
        console.print("=" * 80 + "\n")

        table = Table(show_header=True, header_style="bold red")
        table.add_column("Philosopher 1", style="cyan")
        table.add_column("vs.", style="red", justify="center")
        table.add_column("Philosopher 2", style="cyan")
        table.add_column("Correlation", style="red", justify="right")

        for phil1, phil2, corr in oppositions[:10]:  # Top 10
            table.add_row(phil1, "⚔️", phil2, f"{corr:.3f}")

        console.print(table)

    def save_correlation_data(self, data: Dict[str, Any], filename: str = None):
        """Save correlation analysis to JSON."""
        if filename is None:
            from datetime import datetime

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"philosopher_correlations_{timestamp}.json"

        output_path = Path(__file__).parent / "results" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

        console.print(f"\n[green]✓ Correlation data saved to:[/green] {output_path}")

        return output_path


def main():
    """Main function to run correlation analysis."""
    console.print(
        "\n[bold magenta]🔬 Philosopher Correlation Analysis[/bold magenta]\n"
    )

    # Initialize
    trace_db = PoTraceDB()
    analyzer = PhilosopherCorrelationAnalyzer(trace_db)

    # Calculate correlations
    result = analyzer.calculate_correlation_matrix(min_sessions=3)

    console.print(f"[bold]Analysis Summary:[/bold]")
    console.print(f"  - Total sessions analyzed: {result['total_sessions']}")
    console.print(f"  - Philosophers found: {result['philosopher_count']}")

    # Display heatmap
    analyzer.display_heatmap_ascii(result["matrix"])

    # Find clusters
    clusters = analyzer.identify_clusters(result["matrix"], threshold=0.5)
    analyzer.display_clusters(clusters)

    # Find oppositions
    oppositions = analyzer.find_oppositions(result["matrix"], threshold=-0.2)
    analyzer.display_oppositions(oppositions)

    # Save results
    full_result = {
        **result,
        "clusters": clusters,
        "oppositions": [(p1, p2, float(c)) for p1, p2, c in oppositions],
    }
    analyzer.save_correlation_data(full_result)

    # Summary
    console.print("\n" + "=" * 80)
    console.print("[bold green]✅ Correlation Analysis Complete![/bold green]")
    console.print("=" * 80)

    console.print(
        Panel(
            f"""
[bold cyan]Key Findings:[/bold cyan]

• Complementary Clusters: {len(clusters)}
• Opposing Pairs: {len(oppositions)}
• Most Collaborative: {clusters[0] if clusters else 'N/A'}
• Strongest Opposition: {oppositions[0][:2] if oppositions else 'N/A'}

[bold yellow]Insights:[/bold yellow]
Correlation patterns reveal how philosophers interact:
- Positive correlation: Similar reasoning patterns, complementary
- Negative correlation: Opposing perspectives, dialectical tension
- Clusters: Groups that work well together
        """,
            title="[bold green]Analysis Results[/bold green]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()
