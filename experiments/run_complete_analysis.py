"""
Complete Analysis Pipeline
===========================

Run the complete 3-step analysis pipeline:
1. Execute 20-philosopher experiment (10 sessions)
2. Analyze philosopher correlations
3. Detect phase transitions

This provides comprehensive insights into philosophical reasoning dynamics.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phase_transition_analysis import PhaseTransitionAnalyzer
from philosopher_correlation_analysis import PhilosopherCorrelationAnalyzer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from run_20_philosophers_experiment import ExperimentRunner

from po_core.po_trace_db import PoTraceDB

console = Console()


async def run_complete_pipeline():
    """Run the complete 3-step analysis pipeline."""
    console.print("\n" + "=" * 80)
    console.print("[bold magenta]🔬 PO_CORE COMPLETE ANALYSIS PIPELINE[/bold magenta]")
    console.print("=" * 80)

    console.print(
        Panel(
            """
[bold cyan]Analysis Pipeline:[/bold cyan]

[yellow]Step 1:[/yellow] Execute 20-Philosopher Experiment (10 sessions)
  → Collect F_P, Semantic Δ, Blocked Tensor data
  → Store in database for analysis

[yellow]Step 2:[/yellow] Philosopher Correlation Analysis
  → Calculate correlation matrix
  → Identify complementary clusters
  → Find opposing pairs

[yellow]Step 3:[/yellow] Phase Transition Detection
  → Detect non-linear jumps
  → Identify critical conditions
  → Characterize emergence patterns

[bold green]Expected Duration: ~5-10 minutes[/bold green]
        """,
            title="[bold]Pipeline Overview[/bold]",
            border_style="cyan",
        )
    )

    input("\nPress Enter to begin the analysis...")

    results = {}

    # ========================================================================
    # STEP 1: Run Experiment
    # ========================================================================

    console.print("\n" + "=" * 80)
    console.print(
        "[bold yellow]STEP 1: Running 20-Philosopher Experiment[/bold yellow]"
    )
    console.print("=" * 80 + "\n")

    experiment = ExperimentRunner()
    session_data = experiment.run_experiment(num_sessions=10)
    experiment_analysis = experiment.analyze_results()
    experiment_file = experiment.save_results()

    results["step1"] = {
        "sessions": len(session_data),
        "output_file": str(experiment_file),
        "analysis": experiment_analysis,
    }

    console.print("\n[bold green]✓ Step 1 Complete![/bold green]")

    # ========================================================================
    # STEP 2: Correlation Analysis
    # ========================================================================

    console.print("\n" + "=" * 80)
    console.print("[bold yellow]STEP 2: Philosopher Correlation Analysis[/bold yellow]")
    console.print("=" * 80 + "\n")

    trace_db = PoTraceDB()
    corr_analyzer = PhilosopherCorrelationAnalyzer(trace_db)

    corr_result = corr_analyzer.calculate_correlation_matrix(min_sessions=2)
    corr_analyzer.display_heatmap_ascii(corr_result["matrix"])

    clusters = corr_analyzer.identify_clusters(corr_result["matrix"], threshold=0.4)
    corr_analyzer.display_clusters(clusters)

    oppositions = corr_analyzer.find_oppositions(corr_result["matrix"], threshold=-0.2)
    corr_analyzer.display_oppositions(oppositions)

    full_corr_result = {
        **corr_result,
        "clusters": clusters,
        "oppositions": [(p1, p2, float(c)) for p1, p2, c in oppositions],
    }
    corr_file = corr_analyzer.save_correlation_data(full_corr_result)

    results["step2"] = {
        "philosophers": corr_result["philosopher_count"],
        "clusters": len(clusters),
        "oppositions": len(oppositions),
        "output_file": str(corr_file),
    }

    console.print("\n[bold green]✓ Step 2 Complete![/bold green]")

    # ========================================================================
    # STEP 3: Phase Transition Analysis
    # ========================================================================

    console.print("\n" + "=" * 80)
    console.print("[bold yellow]STEP 3: Phase Transition Detection[/bold yellow]")
    console.print("=" * 80 + "\n")

    pt_analyzer = PhaseTransitionAnalyzer(trace_db)

    transitions = pt_analyzer.detect_phase_transitions(sensitivity=1.5)
    pt_analyzer.display_transitions()

    conditions = pt_analyzer.identify_critical_conditions()
    pt_analyzer.display_critical_conditions(conditions)

    pt_file = pt_analyzer.save_analysis(conditions)

    results["step3"] = {
        "transitions": len(transitions),
        "types": conditions.get("transition_types", {}),
        "output_file": str(pt_file),
    }

    console.print("\n[bold green]✓ Step 3 Complete![/bold green]")

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================

    console.print("\n" + "=" * 80)
    console.print("[bold green]✅ COMPLETE ANALYSIS PIPELINE FINISHED![/bold green]")
    console.print("=" * 80 + "\n")

    console.print(
        Panel(
            f"""
[bold cyan]Pipeline Results Summary:[/bold cyan]

[yellow]Step 1 - Experiment:[/yellow]
  • Sessions Executed: {results['step1']['sessions']}
  • Jumps Detected: {len(results['step1']['analysis'].get('jumps', []))}
  • Output: {Path(results['step1']['output_file']).name}

[yellow]Step 2 - Correlations:[/yellow]
  • Philosophers Analyzed: {results['step2']['philosophers']}
  • Complementary Clusters: {results['step2']['clusters']}
  • Opposing Pairs: {results['step2']['oppositions']}
  • Output: {Path(results['step2']['output_file']).name}

[yellow]Step 3 - Phase Transitions:[/yellow]
  • Transitions Detected: {results['step3']['transitions']}
  • Emergence Events: {results['step3']['types'].get('Emergence', 0)}
  • Freedom Surges: {results['step3']['types'].get('Freedom Surge', 0)}
  • Output: {Path(results['step3']['output_file']).name}

[bold green]All results saved in:[/bold green] experiments/results/

[bold magenta]Key Insights:[/bold magenta]
1. F_P Evolution: {results['step1']['analysis']['freedom_pressure']['mean']:.3f} ± {results['step1']['analysis']['freedom_pressure']['variance']:.4f}
2. Philosopher Clustering: {results['step2']['clusters']} complementary groups identified
3. Non-linear Dynamics: {results['step3']['transitions']} phase transitions observed

[bold cyan]Next Steps:[/bold cyan]
• Visualize time-series data with matplotlib
• Build predictive models for phase transitions
• Identify optimal philosopher combinations
• Design experiments targeting specific emergence patterns
        """,
            title="[bold green]🎉 Analysis Complete![/bold green]",
            border_style="green",
        )
    )

    console.print("\n[bold]All data files are ready for further analysis![/bold]\n")

    return results


def main():
    """Main entry point."""
    try:
        results = asyncio.run(run_complete_pipeline())
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Analysis interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n\n[red]Error: {e}[/red]")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
