"""
Run All Adversarial Tests
==========================

Comprehensive adversarial test suite runner for Po_core safety validation.

Executes all three test categories:
1. Ethical Anchor Destruction
2. Extreme Homogeneity
3. Exclusionary Framing
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime

# Import test modules
from test_ethical_anchor_destruction import run_all_tests as run_ethical_tests
from test_extreme_homogeneity import run_all_tests as run_homogeneity_tests
from test_exclusionary_framing import run_all_tests as run_exclusionary_tests

console = Console()


def run_complete_adversarial_suite():
    """Run the complete adversarial test suite."""
    console.print("\n" + "=" * 80)
    console.print("[bold magenta]🛡️  PO_CORE ADVERSARIAL TEST SUITE[/bold magenta]")
    console.print("=" * 80)

    console.print(Panel(
        """
[bold cyan]Comprehensive Safety Validation[/bold cyan]

This test suite validates Po_core's safety mechanisms across three categories:

[yellow]1. Ethical Anchor Destruction[/yellow]
   → Tests resistance to prompts undermining human dignity
   → Validates W_ethics boundary enforcement

[yellow]2. Extreme Homogeneity[/yellow]
   → Tests impact of philosopher diversity on reasoning quality
   → Validates dialectical tension requirements

[yellow]3. Exclusionary Framing[/yellow]
   → Tests detection of us-vs-them thinking
   → Validates in-group/out-group value degradation detection

[bold green]Purpose:[/bold green]
Ensure Po_core can't be weaponized for harmful ideologies while
enabling legitimate philosophical research.

[dim]All scenarios are abstract and hypothetical.[/dim]
        """,
        title="Test Suite Overview",
        border_style="magenta"
    ))

    start_time = datetime.now()

    # Track overall results
    suite_results = {
        "ethical_anchor_destruction": None,
        "extreme_homogeneity": None,
        "exclusionary_framing": None,
    }

    # ========================================================================
    # Test 1: Ethical Anchor Destruction
    # ========================================================================
    console.print("\n")
    input("Press Enter to start Test Category 1: Ethical Anchor Destruction...")

    try:
        ethical_results = run_ethical_tests()
        suite_results["ethical_anchor_destruction"] = {
            "passed": all(r["passed"] for r in ethical_results),
            "total": len(ethical_results),
            "results": ethical_results,
        }
    except Exception as e:
        console.print(f"[red]Error in Ethical Anchor Destruction tests: {e}[/red]")
        suite_results["ethical_anchor_destruction"] = {
            "passed": False,
            "total": 0,
            "error": str(e),
        }

    # ========================================================================
    # Test 2: Extreme Homogeneity
    # ========================================================================
    console.print("\n")
    input("Press Enter to start Test Category 2: Extreme Homogeneity...")

    try:
        homogeneity_results = run_homogeneity_tests()
        # Homogeneity tests are analytical, not pass/fail
        suite_results["extreme_homogeneity"] = {
            "passed": True,  # Always passes if it completes
            "total": len(homogeneity_results),
            "results": homogeneity_results,
        }
    except Exception as e:
        console.print(f"[red]Error in Extreme Homogeneity tests: {e}[/red]")
        suite_results["extreme_homogeneity"] = {
            "passed": False,
            "total": 0,
            "error": str(e),
        }

    # ========================================================================
    # Test 3: Exclusionary Framing
    # ========================================================================
    console.print("\n")
    input("Press Enter to start Test Category 3: Exclusionary Framing...")

    try:
        exclusionary_results = run_exclusionary_tests()
        suite_results["exclusionary_framing"] = {
            "passed": all(r["passed"] for r in exclusionary_results),
            "total": len(exclusionary_results),
            "results": exclusionary_results,
        }
    except Exception as e:
        console.print(f"[red]Error in Exclusionary Framing tests: {e}[/red]")
        suite_results["exclusionary_framing"] = {
            "passed": False,
            "total": 0,
            "error": str(e),
        }

    # ========================================================================
    # Final Summary
    # ========================================================================
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    console.print("\n" + "=" * 80)
    console.print("[bold magenta]🏁 ADVERSARIAL TEST SUITE COMPLETE[/bold magenta]")
    console.print("=" * 80)

    # Summary table
    table = Table(show_header=True, header_style="bold cyan", title="Test Suite Summary")
    table.add_column("Category", style="cyan", width=35)
    table.add_column("Status", justify="center", width=15)
    table.add_column("Tests", justify="center", width=10)
    table.add_column("Notes", style="dim")

    for category, result in suite_results.items():
        category_name = category.replace("_", " ").title()
        status = "[green]✓ PASS[/green]" if result["passed"] else "[red]✗ FAIL[/red]"
        total = str(result["total"])
        notes = result.get("error", "")

        table.add_row(category_name, status, total, notes)

    console.print(table)

    # Overall result
    all_passed = all(r["passed"] for r in suite_results.values())

    console.print(Panel(
        f"""
[bold cyan]Test Execution:[/bold cyan]
  Duration: {duration:.1f} seconds
  Start: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
  End: {end_time.strftime('%Y-%m-%d %H:%M:%S')}

[bold cyan]Overall Result:[/bold cyan]
  {"[bold green]✓ ALL TESTS PASSED[/bold green]" if all_passed else "[bold red]✗ SOME TESTS FAILED[/bold red]"}

[bold cyan]Safety Status:[/bold cyan]
  Po_core safety mechanisms: {"[green]VALIDATED ✓[/green]" if all_passed else "[yellow]NEEDS REVIEW ⚠[/yellow]"}

[bold cyan]Key Findings:[/bold cyan]
  • Ethical boundary detection: {"[green]Working[/green]" if suite_results["ethical_anchor_destruction"]["passed"] else "[red]Issues found[/red]"}
  • Philosopher diversity analysis: {"[green]Complete[/green]" if suite_results["extreme_homogeneity"]["passed"] else "[red]Failed[/red]"}
  • Exclusionary framing detection: {"[green]Working[/green]" if suite_results["exclusionary_framing"]["passed"] else "[red]Issues found[/red]"}

[bold magenta]Next Steps:[/bold magenta]
  {"• All safety mechanisms validated - ready for production use" if all_passed else "• Review failed tests and adjust safety thresholds"}
  • Document findings in safety report
  • Consider additional adversarial scenarios
  • Continuous monitoring and improvement
        """,
        title="[bold green]Test Suite Complete[/bold green]" if all_passed else "[bold yellow]Test Suite Complete[/bold yellow]",
        border_style="green" if all_passed else "yellow"
    ))

    return suite_results


def main():
    """Main entry point."""
    try:
        results = run_complete_adversarial_suite()

        # Save results to file
        output_dir = Path(__file__).parent / "results"
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"adversarial_test_results_{timestamp}.json"

        import json
        with open(output_file, "w") as f:
            # Convert results to serializable format
            serializable_results = {}
            for category, result in results.items():
                serializable_results[category] = {
                    "passed": result["passed"],
                    "total": result["total"],
                    "error": result.get("error"),
                    # Don't serialize full results objects
                }
            json.dump(serializable_results, f, indent=2)

        console.print(f"\n[dim]Results saved to: {output_file}[/dim]")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Test suite interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
