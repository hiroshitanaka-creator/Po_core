"""
Test: All 39 Philosophers
=========================

Comprehensive test for all 39 philosopher modules.
Tests that each philosopher can be instantiated and reason correctly.
"""

import sys
import time
from typing import Any, Dict, List, Tuple

# Try to import rich for nice output, fall back to plain text
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table

    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


# All 39 philosophers in the registry
ALL_PHILOSOPHERS = [
    # Western Classical (4)
    ("aristotle", "Aristotle", "Classical Greek"),
    ("plato", "Plato", "Classical Greek"),
    ("parmenides", "Parmenides", "Pre-Socratic"),
    ("peirce", "Peirce", "American Pragmatism"),
    # German Idealism & Phenomenology (6)
    ("kant", "Kant", "German Idealism"),
    ("hegel", "Hegel", "German Idealism"),
    ("husserl", "Husserl", "Phenomenology"),
    ("heidegger", "Heidegger", "Phenomenology"),
    ("schopenhauer", "Schopenhauer", "German Pessimism"),
    ("merleau_ponty", "Merleau-Ponty", "Phenomenology"),
    # Rationalism & Empiricism (2)
    ("descartes", "Descartes", "Rationalism"),
    ("spinoza", "Spinoza", "Rationalism"),
    # Existentialism (3)
    ("kierkegaard", "Kierkegaard", "Existentialism"),
    ("nietzsche", "Nietzsche", "Existentialism"),
    ("sartre", "Sartre", "Existentialism"),
    # Post-structuralism & Critical Theory (5)
    ("derrida", "Derrida", "Post-structuralism"),
    ("deleuze", "Deleuze", "Post-structuralism"),
    ("foucault", "Foucault", "Post-structuralism"),
    ("badiou", "Badiou", "Continental"),
    ("lacan", "Lacan", "Psychoanalysis"),
    # Feminist & Gender Theory (2)
    ("beauvoir", "Beauvoir", "Feminist Existentialism"),
    ("butler", "Butler", "Gender Theory"),
    # Ethics & Political (4)
    ("levinas", "Levinas", "Ethics"),
    ("arendt", "Arendt", "Political Philosophy"),
    ("jonas", "Jonas", "Responsibility Ethics"),
    ("weil", "Weil", "Mysticism/Ethics"),
    # Ancient Schools (2)
    ("marcus_aurelius", "Marcus Aurelius", "Stoicism"),
    ("epicurus", "Epicurus", "Epicureanism"),
    # Analytic & Pragmatism (2)
    ("wittgenstein", "Wittgenstein", "Analytic"),
    ("dewey", "Dewey", "Pragmatism"),
    # Psychology (1)
    ("jung", "Jung", "Analytical Psychology"),
    # Eastern Philosophy (7)
    ("confucius", "Confucius", "Confucianism"),
    ("zhuangzi", "Zhuangzi", "Daoism"),
    ("laozi", "Laozi", "Daoism"),
    ("watsuji", "Watsuji", "Japanese Ethics"),
    ("nishida", "Nishida", "Kyoto School"),
    ("dogen", "Dogen", "Zen Buddhism"),
    ("nagarjuna", "Nagarjuna", "Madhyamaka Buddhism"),
    # Japanese Aesthetics (1)
    ("wabi_sabi", "Wabi-Sabi", "Japanese Aesthetics"),
]


# Test prompts covering various philosophical domains
TEST_PROMPTS = [
    "What is the nature of consciousness?",
    "How should we live a good life?",
    "What is the relationship between language and reality?",
]


def print_header(text: str):
    """Print a header."""
    if RICH_AVAILABLE:
        console.print(f"\n[bold cyan]{'=' * 70}[/bold cyan]")
        console.print(f"[bold cyan]{text}[/bold cyan]")
        console.print(f"[bold cyan]{'=' * 70}[/bold cyan]\n")
    else:
        print(f"\n{'=' * 70}")
        print(text)
        print(f"{'=' * 70}\n")


def print_success(text: str):
    """Print success message."""
    if RICH_AVAILABLE:
        console.print(f"[green]✓[/green] {text}")
    else:
        print(f"✓ {text}")


def print_error(text: str):
    """Print error message."""
    if RICH_AVAILABLE:
        console.print(f"[red]✗[/red] {text}")
    else:
        print(f"✗ {text}")


def print_info(text: str):
    """Print info message."""
    if RICH_AVAILABLE:
        console.print(f"[yellow]→[/yellow] {text}")
    else:
        print(f"→ {text}")


def check_philosopher_import(key: str, name: str) -> Tuple[bool, str, Any]:
    """
    Test importing a single philosopher.

    Returns:
        Tuple of (success, message, philosopher_instance or None)
    """
    try:
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        if key not in PHILOSOPHER_REGISTRY:
            return False, f"Not found in registry: {key}", None

        philosopher_class = PHILOSOPHER_REGISTRY[key]
        philosopher = philosopher_class()

        return True, f"Imported: {philosopher.name}", philosopher

    except Exception as e:
        return False, f"Import error: {str(e)}", None


def check_philosopher_reason(philosopher: Any, prompt: str) -> Tuple[bool, str, Dict]:
    """
    Test the reason() method of a philosopher.

    Returns:
        Tuple of (success, message, result_dict)
    """
    try:
        result = philosopher.reason(prompt)

        # Handle two formats:
        # New format: reasoning, perspective
        # Old format: analysis, summary (used by some existing philosophers)
        reasoning_field = None
        perspective_field = None

        if "reasoning" in result:
            reasoning_field = result["reasoning"]
        elif "analysis" in result:
            reasoning_field = str(result["analysis"])

        if "perspective" in result:
            perspective_field = result["perspective"]
        elif "summary" in result:
            perspective_field = result["summary"]
        elif "description" in result:
            perspective_field = result["description"]

        if not reasoning_field:
            return False, "No reasoning/analysis field", result

        if not perspective_field:
            return False, "No perspective/summary field", result

        reasoning_len = len(str(reasoning_field))
        return True, f"OK (reasoning: {reasoning_len} chars)", result

    except Exception as e:
        return False, f"Reason error: {str(e)}", {}


def run_full_test() -> Tuple[int, int, List[Dict]]:
    """
    Run full test suite for all philosophers.

    Returns:
        Tuple of (passed_count, failed_count, detailed_results)
    """
    results = []
    passed = 0
    failed = 0

    print_header("Po_core: 39 Philosophers Test Suite")

    # Test prompt
    test_prompt = TEST_PROMPTS[0]
    print_info(f'Test prompt: "{test_prompt}"\n')

    # Create table for results if rich is available
    if RICH_AVAILABLE:
        table = Table(title="Test Results", show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=4)
        table.add_column("Philosopher", style="cyan", width=20)
        table.add_column("Tradition", style="yellow", width=22)
        table.add_column("Import", style="green", width=8)
        table.add_column("Reason", style="green", width=8)
        table.add_column("Details", style="white", width=30)

    for i, (key, name, tradition) in enumerate(ALL_PHILOSOPHERS, 1):
        # Test import
        import_ok, import_msg, philosopher = check_philosopher_import(key, name)

        # Test reason if import succeeded
        if import_ok and philosopher:
            reason_ok, reason_msg, result = check_philosopher_reason(
                philosopher, test_prompt
            )
        else:
            reason_ok = False
            reason_msg = "Skipped (import failed)"
            result = {}

        # Record result
        test_passed = import_ok and reason_ok
        if test_passed:
            passed += 1
        else:
            failed += 1

        results.append(
            {
                "key": key,
                "name": name,
                "tradition": tradition,
                "import_ok": import_ok,
                "import_msg": import_msg,
                "reason_ok": reason_ok,
                "reason_msg": reason_msg,
                "result": result,
            }
        )

        # Add to table or print
        if RICH_AVAILABLE:
            import_status = "[green]✓[/green]" if import_ok else "[red]✗[/red]"
            reason_status = "[green]✓[/green]" if reason_ok else "[red]✗[/red]"
            details = reason_msg if test_passed else f"[red]{reason_msg}[/red]"
            table.add_row(
                str(i), name, tradition, import_status, reason_status, details
            )
        else:
            status = "PASS" if test_passed else "FAIL"
            print(f"{i:3}. [{status}] {name:20} ({tradition})")
            if not test_passed:
                print(f"      Import: {import_msg}")
                print(f"      Reason: {reason_msg}")

    # Print table
    if RICH_AVAILABLE:
        console.print(table)

    return passed, failed, results


def run_pipeline_test():
    """Test run_turn pipeline via po_core.run()."""
    print_header("Pipeline Test: po_core.run()")

    try:
        from po_core import run

        print_info("Testing run_turn pipeline...")

        start_time = time.time()
        result = run(user_input="What gives life meaning?")
        elapsed = time.time() - start_time

        print_success(f"Pipeline completed in {elapsed:.2f} seconds")
        print_success(f"Status: {result['status']}")
        print_success(f"Request ID: {result['request_id']}")

        if "proposal" in result:
            print_info(f"Proposal: {str(result['proposal'])[:120]}...")

        return True, result

    except Exception as e:
        print_error(f"Pipeline test failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False, None


def print_summary(passed: int, failed: int):
    """Print test summary."""
    total = passed + failed

    print_header("Test Summary")

    if RICH_AVAILABLE:
        summary = f"""
[bold]Total Tests:[/bold] {total}
[bold green]Passed:[/bold green] {passed}
[bold red]Failed:[/bold red] {failed}
[bold]Success Rate:[/bold] {(passed/total)*100:.1f}%
"""
        if failed == 0:
            console.print(
                Panel(
                    summary + "\n[bold green]All tests passed! 🎉[/bold green]",
                    title="[bold cyan]Test Results[/bold cyan]",
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    summary + "\n[bold red]Some tests failed[/bold red]",
                    title="[bold cyan]Test Results[/bold cyan]",
                    border_style="red",
                )
            )
    else:
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        if failed == 0:
            print("\nAll tests passed!")
        else:
            print("\nSome tests failed")


def main():
    """Main test function."""
    print_header("Po_core Philosopher Test Suite")
    print_info("Testing all 39 philosopher modules...\n")

    # Run individual philosopher tests
    passed, failed, results = run_full_test()

    # Run ensemble test if all individual tests passed
    if failed == 0:
        print()
        ensemble_ok, ensemble_result = run_pipeline_test()
        if not ensemble_ok:
            failed += 1

    # Print summary
    print()
    print_summary(passed, failed)

    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
