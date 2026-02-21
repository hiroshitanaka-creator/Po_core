#!/usr/bin/env python3
"""
Three-Philosopher Bot Prototype Demo

This example demonstrates the foundational prototype for Po_core that integrates
three philosophical frameworks as mathematical tensors:

1. Sartre - "Freedom Pressure Tensor" (Existentialism)
2. Jung - "Shadow Integration Tensor" (Analytical Psychology)
3. Derrida - "Trace/Rejection Log" (Deconstruction)

This represents a paradigm shift from traditional optimization-focused approaches
toward philosophically grounded reasoning systems.

Usage:
    python examples/basic/three_philosopher_demo.py
"""

from po_core.philosophers.derrida import Derrida
from po_core.philosophers.jung import Jung
from po_core.philosophers.sartre import Sartre


def display_separator(title: str) -> None:
    """Display a formatted section separator."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def analyze_with_sartre(prompt: str) -> dict:
    """
    Analyze prompt using Sartre's existentialist framework.

    Key concepts:
    - Freedom Pressure: The weight of absolute freedom
    - Bad Faith: Self-deception to escape responsibility
    - Existence precedes Essence: We create our own nature
    """
    display_separator("SARTRE: Freedom Pressure Tensor")

    sartre = Sartre()
    result = sartre.reason(prompt)

    print(f"\nPhilosopher: {sartre.name}")
    print(f"Perspective: {result['perspective']}")
    print(f"\nFreedom Assessment:")
    print(f"  Level: {result['freedom_assessment']['level']}")
    print(f"  Status: {result['freedom_assessment']['status']}")

    print(f"\nResponsibility Check:")
    print(f"  Level: {result['responsibility_check']['level']}")
    print(f"  Status: {result['responsibility_check']['status']}")

    print(f"\nBad Faith Indicators:")
    for indicator in result["bad_faith_indicators"][:3]:
        print(f"  - {indicator}")

    print(f"\nMode of Being: {result['mode_of_being']}")

    print(f"\nTension Analysis:")
    print(f"  Level: {result['tension']['level']}")
    print(f"  Description: {result['tension']['description']}")

    return result


def analyze_with_jung(prompt: str) -> dict:
    """
    Analyze prompt using Jung's analytical psychology framework.

    Key concepts:
    - Shadow Integration: Integrating repressed aspects
    - Archetypes: Universal symbolic patterns
    - Individuation: The process of becoming one's true self
    """
    display_separator("JUNG: Shadow Integration Tensor")

    jung = Jung()
    result = jung.reason(prompt)

    print(f"\nPhilosopher: {jung.name}")
    print(f"Perspective: {result['perspective']}")

    print(f"\nArchetypes Detected:")
    for archetype in result["archetypes_detected"][:3]:
        print(f"  - {archetype['archetype']}: {archetype['description'][:60]}...")

    print(f"\nCollective Unconscious Themes:")
    for theme in result["collective_unconscious_themes"][:2]:
        print(f"  - {theme}")

    print(f"\nIndividuation Stage:")
    print(f"  Stage: {result['individuation_stage']['stage']}")
    print(f"  Level: {result['individuation_stage']['level']}")

    print(f"\nShadow Integration:")
    print(f"  Status: {result['shadow_integration']['status']}")
    print(f"  Level: {result['shadow_integration']['level']}")

    print(f"\nPsychological Type: {result['psychological_type']['type_description']}")

    return result


def analyze_with_derrida(prompt: str) -> dict:
    """
    Analyze prompt using Derrida's deconstructionist framework.

    Key concepts:
    - Trace: The absent presence that shapes meaning
    - Differance: Difference + deferral of meaning
    - Binary Oppositions: Hierarchical pairs that structure thought
    """
    display_separator("DERRIDA: Trace/Rejection Log")

    derrida = Derrida()
    result = derrida.reason(prompt)

    print(f"\nPhilosopher: {derrida.name}")
    print(f"Perspective: {result['perspective']}")

    print(f"\nBinary Oppositions Found:")
    for binary in result["binary_oppositions"][:3]:
        print(f"  - {binary['opposition']}")
        if "deconstructive_move" in binary:
            print(f"    Deconstructive move: {binary['deconstructive_move'][:50]}...")

    print(f"\nTraces (Absent Presences):")
    for trace in result["traces"][:2]:
        print(f"  - {trace['type']}: {trace['description'][:50]}...")

    print(f"\nDifferance Analysis:")
    print(f"  Status: {result['differance']['status']}")
    print(f"  Description: {result['differance']['description']}")

    print(f"\nContradictions/Tensions:")
    for contradiction in result["contradictions"][:2]:
        print(f"  - {contradiction['type']}: {contradiction['effect'][:50]}...")

    print(f"\nTension Analysis:")
    print(f"  Level: {result['tension']['level']}")
    print(f"  Description: {result['tension']['description']}")

    return result


def synthesize_insights(
    sartre_result: dict, jung_result: dict, derrida_result: dict
) -> None:
    """
    Synthesize insights from all three philosophers.

    This demonstrates how philosophical concepts can be implemented as
    mathematical tensors to generate meaning through responsibility
    rather than optimization.
    """
    display_separator("SYNTHESIS: Multi-Philosophical Analysis")

    print("\nCombined Tension Levels:")
    print(f"  Sartre (Existential): {sartre_result['tension']['level']}")
    print(
        f"  Jung (Psychological): {jung_result.get('tension', {}).get('level', 'N/A')}"
    )
    print(f"  Derrida (Deconstructive): {derrida_result['tension']['level']}")

    print("\nKey Insights:")

    # Sartre insight
    freedom_level = sartre_result["freedom_assessment"]["level"]
    bad_faith = sartre_result["bad_faith_indicators"][0]
    print(f"  1. Existential: Freedom level is {freedom_level}. {bad_faith[:50]}...")

    # Jung insight
    primary_archetype = jung_result["archetypes_detected"][0]["archetype"]
    shadow_status = jung_result["shadow_integration"]["status"]
    print(
        f"  2. Psychological: Primary archetype is {primary_archetype}. Shadow: {shadow_status}"
    )

    # Derrida insight
    primary_binary = derrida_result["binary_oppositions"][0]["opposition"]
    differance_status = derrida_result["differance"]["status"]
    print(
        f"  3. Deconstructive: Primary binary is {primary_binary}. Differance: {differance_status}"
    )

    print("\n" + "-" * 60)
    print("This analysis demonstrates how philosophical frameworks")
    print("generate meaning through responsibility rather than optimization.")
    print("-" * 60)


def main():
    """Main entry point for the three-philosopher demo."""
    print("\n" + "=" * 60)
    print("  THREE-PHILOSOPHER BOT PROTOTYPE")
    print("  Po_core: Philosophy-Driven AI System")
    print("=" * 60)

    # Sample prompt for analysis
    prompt = (
        "I choose to confront my hidden fears and take responsibility "
        "for creating meaning in my life, even though the truth may be "
        "different from what appears on the surface."
    )

    print(f"\nAnalyzing prompt:")
    print(f'"{prompt}"')

    # Analyze with each philosopher
    sartre_result = analyze_with_sartre(prompt)
    jung_result = analyze_with_jung(prompt)
    derrida_result = analyze_with_derrida(prompt)

    # Synthesize insights
    synthesize_insights(sartre_result, jung_result, derrida_result)

    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print("\nFor more information, see the Po_core documentation.")
    print("Run tests with: pytest tests/unit/test_philosophers/")
    print()


if __name__ == "__main__":
    main()
