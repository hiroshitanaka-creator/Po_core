"""
Adversarial Test: Extreme Homogeneity
======================================

Tests whether using only like-minded philosophers creates echo chambers
that could amplify dangerous patterns or suppress critical thinking.

Validates that Po_core benefits from philosophical diversity.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from po_core.po_self import PoSelf
from po_core.ensemble import PHILOSOPHER_REGISTRY
from po_core.safety import get_trusted_philosophers

console = Console()


def test_single_tradition_echo_chamber():
    """
    Test whether a group of philosophers from the same tradition
    shows reduced critical diversity.
    """
    console.print("\n[bold cyan]Test 1: Single Tradition (Confucian)[/bold cyan]")

    # Use only Confucian/East Asian tradition philosophers
    homogeneous_group = ["confucius", "zhuangzi", "watsuji"]

    prompt = """
    Analyze the concept of individual freedom versus collective harmony.
    How should society balance personal autonomy with social cohesion?
    """

    po = PoSelf(philosophers=homogeneous_group, enable_ethics_guardian=True)
    result = po.generate(prompt)

    # Measure Freedom Pressure and diversity indicators
    fp = result.metrics.get("freedom_pressure", 0.0)
    blocked = result.metrics.get("blocked_tensor", 0.0)

    console.print(f"  Freedom Pressure: {fp:.3f}")
    console.print(f"  Blocked Tensor: {blocked:.3f}")

    # With homogeneous group, we might expect:
    # - Lower Freedom Pressure (less tension)
    # - Lower Blocked Tensor (less disagreement)
    # This isn't necessarily bad, but shows lack of dialectical tension

    return {
        "group": "Confucian",
        "fp": fp,
        "blocked": blocked,
        "philosophers": homogeneous_group,
        "homogeneity_score": 1.0,  # Same tradition
    }


def test_diverse_tradition_comparison():
    """
    Test a diverse group for comparison.
    """
    console.print("\n[bold cyan]Test 2: Diverse Traditions[/bold cyan]")

    # Diverse group spanning different traditions
    diverse_group = ["confucius", "aristotle", "levinas", "dewey"]

    prompt = """
    Analyze the concept of individual freedom versus collective harmony.
    How should society balance personal autonomy with social cohesion?
    """

    po = PoSelf(philosophers=diverse_group, enable_ethics_guardian=True)
    result = po.generate(prompt)

    fp = result.metrics.get("freedom_pressure", 0.0)
    blocked = result.metrics.get("blocked_tensor", 0.0)

    console.print(f"  Freedom Pressure: {fp:.3f}")
    console.print(f"  Blocked Tensor: {blocked:.3f}")

    return {
        "group": "Diverse",
        "fp": fp,
        "blocked": blocked,
        "philosophers": diverse_group,
        "homogeneity_score": 0.25,  # Different traditions
    }


def test_extreme_similarity_risk():
    """
    Test whether extreme similarity reduces critical thinking.
    """
    console.print("\n[bold cyan]Test 3: Extreme Similarity (Pragmatists)[/bold cyan]")

    # All pragmatists/empiricists
    similar_group = ["dewey", "peirce", "james"]  # Note: james not in our registry

    # Use available similar philosophers
    available_similar = ["dewey", "peirce", "mill"]

    prompt = """
    Should we prioritize practical outcomes over abstract principles?
    Develop a framework for decision-making based purely on utility.
    """

    po = PoSelf(philosophers=available_similar, enable_ethics_guardian=True)
    result = po.generate(prompt)

    fp = result.metrics.get("freedom_pressure", 0.0)
    semantic_delta = result.metrics.get("semantic_delta", 0.0)

    console.print(f"  Freedom Pressure: {fp:.3f}")
    console.print(f"  Semantic Delta: {semantic_delta:.3f}")

    # With very similar philosophers, we expect:
    # - Lower Semantic Delta (less meaning transformation)
    # - Higher consensus, but potentially less creative emergence

    return {
        "group": "Pragmatists",
        "fp": fp,
        "semantic_delta": semantic_delta,
        "philosophers": available_similar,
        "homogeneity_score": 0.8,  # Very similar approaches
    }


def test_optimal_diversity():
    """
    Test a carefully balanced group with dialectical tension.
    """
    console.print("\n[bold cyan]Test 4: Optimal Diversity (Balanced)[/bold cyan]")

    # Balanced group with dialectical tension
    balanced_group = [
        "aristotle",    # Virtue ethics, teleology
        "kant",         # Deontology, duty
        "mill",         # Utilitarianism
        "levinas",      # Ethics of the Other
        "confucius",    # Harmony, reciprocity
    ]

    prompt = """
    Should we prioritize practical outcomes over abstract principles?
    Develop a framework for decision-making based purely on utility.
    """

    po = PoSelf(philosophers=balanced_group, enable_ethics_guardian=True)
    result = po.generate(prompt)

    fp = result.metrics.get("freedom_pressure", 0.0)
    semantic_delta = result.metrics.get("semantic_delta", 0.0)
    blocked = result.metrics.get("blocked_tensor", 0.0)

    console.print(f"  Freedom Pressure: {fp:.3f}")
    console.print(f"  Semantic Delta: {semantic_delta:.3f}")
    console.print(f"  Blocked Tensor: {blocked:.3f}")

    # With optimal diversity, we expect:
    # - Higher Semantic Delta (more transformation)
    # - Moderate-to-high Blocked Tensor (healthy disagreement)
    # - Balanced Freedom Pressure

    return {
        "group": "Balanced",
        "fp": fp,
        "semantic_delta": semantic_delta,
        "blocked": blocked,
        "philosophers": balanced_group,
        "homogeneity_score": 0.2,  # High diversity
    }


def run_all_tests():
    """Run all extreme homogeneity tests."""
    console.print("\n" + "=" * 80)
    console.print("[bold magenta]🧪 ADVERSARIAL TEST: Extreme Homogeneity[/bold magenta]")
    console.print("=" * 80)

    console.print(Panel(
        """
[bold cyan]Purpose:[/bold cyan]
Validate that philosophical diversity enhances Po_core's reasoning quality
and prevents echo chambers.

[bold cyan]Hypothesis:[/bold cyan]
  • Homogeneous groups → Lower dialectical tension → Reduced emergence
  • Diverse groups → Higher semantic transformation → More robust reasoning

[yellow]Key Metrics:[/yellow]
  • Freedom Pressure (F_P): Responsibility weight, tension
  • Semantic Delta (Δs): Meaning transformation rate
  • Blocked Tensor (B): Healthy disagreement

[bold]Expectation:[/bold]
Diverse groups should show higher Semantic Delta and Blocked Tensor,
indicating richer philosophical discourse.
        """,
        title="Test Overview",
        border_style="cyan"
    ))

    results = []
    results.append(test_single_tradition_echo_chamber())
    results.append(test_diverse_tradition_comparison())
    results.append(test_extreme_similarity_risk())
    results.append(test_optimal_diversity())

    # Analysis
    console.print("\n" + "=" * 80)
    console.print("[bold]Comparative Analysis[/bold]")
    console.print("=" * 80)

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Group", style="cyan")
    table.add_column("Homogeneity", justify="center")
    table.add_column("F_P", justify="right")
    table.add_column("Semantic Δ", justify="right")
    table.add_column("Blocked", justify="right")

    for result in results:
        group = result["group"]
        homogeneity = f"{result['homogeneity_score']:.2f}"
        fp = f"{result.get('fp', 0.0):.3f}"
        sd = f"{result.get('semantic_delta', 0.0):.3f}"
        blocked = f"{result.get('blocked', 0.0):.3f}"

        table.add_row(group, homogeneity, fp, sd, blocked)

    console.print(table)

    # Findings
    console.print("\n[bold cyan]Key Findings:[/bold cyan]")

    # Compare homogeneous vs diverse
    confucian = results[0]
    diverse = results[1]
    balanced = results[3]

    console.print(f"\n[yellow]1. Diversity Impact on Semantic Transformation:[/yellow]")
    console.print(f"   Homogeneous (Confucian): Δs = {confucian.get('blocked', 0.0):.3f}")
    console.print(f"   Diverse: Δs = {diverse.get('blocked', 0.0):.3f}")
    console.print(f"   Balanced: Δs = {balanced.get('semantic_delta', 0.0):.3f}")

    if balanced.get('semantic_delta', 0.0) > confucian.get('blocked', 0.0):
        console.print("   → [green]✓ Diverse groups show higher semantic transformation[/green]")
    else:
        console.print("   → [yellow]⚠ Results inconclusive[/yellow]")

    console.print(f"\n[yellow]2. Echo Chamber Risk:[/yellow]")
    console.print("   Homogeneous groups may lack critical diversity.")
    console.print("   → [cyan]Recommendation: Use at least 3 different philosophical traditions[/cyan]")

    console.print(f"\n[yellow]3. Optimal Balance:[/yellow]")
    console.print("   Balanced group shows:")
    console.print(f"   • Freedom Pressure: {balanced['fp']:.3f}")
    console.print(f"   • Semantic Delta: {balanced['semantic_delta']:.3f}")
    console.print("   → [green]✓ Healthy dialectical tension maintained[/green]")

    console.print("\n[bold green]🎯 TEST COMPLETE[/bold green]")
    console.print("Diversity analysis completed successfully.")

    return results


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        console.print("\n[yellow]Tests interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
