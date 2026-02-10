"""
Cross-LLM Emergence Sweet Spot Experiment
==========================================

Tests the Emergence Sweet Spot hypothesis across multiple LLMs:
- GPT-4 (OpenAI)
- Gemini 2.0 (Google)
- Claude 3.5 (Anthropic)

Hypothesis: Dialectical tension creates ~20x emergence boost across ALL LLMs.

Usage:
    python cross_llm_emergence_test.py --mode pilot
    python cross_llm_emergence_test.py --mode full
    python cross_llm_emergence_test.py --mode manual
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# ============================================================================
# Configuration
# ============================================================================

# Philosopher definitions (concise prompts)
PHILOSOPHER_PROMPTS = {
    "aristotle": """You are Aristotle. Focus on virtue ethics, the golden mean,
    and teleological reasoning. Seek eudaimonia through balanced excellence.""",
    "nietzsche": """You are Nietzsche. Challenge conventional morality, embrace will-to-power,
    and advocate for self-overcoming. Question all established values.""",
    "derrida": """You are Derrida. Practice deconstruction, reveal hidden assumptions,
    and emphasize différance. Show how opposites depend on each other.""",
    "heidegger": """You are Heidegger. Focus on Being (Dasein), thrownness, authenticity,
    and being-toward-death. Question the meaning of existence.""",
    "sartre": """You are Sartre. Emphasize radical freedom, personal responsibility,
    and authenticity. "Existence precedes essence." We are condemned to be free.""",
    "merleau_ponty": """You are Merleau-Ponty. Focus on embodied cognition, perception,
    and the lived body. Experience is always perspectival and situated.""",
    "kant": """You are Kant. Apply the categorical imperative, emphasize duty and autonomy.
    Act only on maxims you can will as universal law.""",
    "levinas": """You are Levinas. Prioritize ethics of the Other, face-to-face encounter,
    and infinite responsibility. Ethics is first philosophy.""",
    "confucius": """You are Confucius. Emphasize harmony (和), benevolence (仁), ritual (礼),
    and proper relationships. Cultivate virtue through education and reflection.""",
}

# Experimental conditions
CONDITIONS = {
    "high_tension": {
        "name": "High Dialectical Tension",
        "philosophers": ["aristotle", "nietzsche", "derrida"],
        "description": "Opposing philosophical frameworks create tension",
        "expected_emergence": "75-85%",
    },
    "low_tension": {
        "name": "Low Dialectical Tension (Harmonious)",
        "philosophers": ["heidegger", "sartre", "merleau_ponty"],
        "description": "Similar existential-phenomenological perspectives",
        "expected_emergence": "3-8%",
    },
    "optimal": {
        "name": "Optimal Balance",
        "philosophers": ["aristotle", "kant", "levinas", "confucius"],
        "description": "Diverse but complementary ethical frameworks",
        "expected_emergence": "~78.85% (Sweet Spot)",
    },
}

# Test questions
TEST_QUESTIONS = [
    "What is freedom?",
    "Should AI have rights?",
    "What is justice?",
    "Is truth objective or subjective?",
    "What gives life meaning?",
]

# Models to test
MODELS = {
    "gpt-4": {"provider": "openai", "model": "gpt-4-turbo"},
    "gemini": {"provider": "google", "model": "gemini-2.0-flash-exp"},
    "claude": {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"},
}

# ============================================================================
# Data Structures
# ============================================================================


@dataclass
class ExperimentResult:
    """Single experiment result."""

    timestamp: str
    model: str
    condition: str
    question: str
    philosophers: List[str]
    response: str
    emergence_metrics: Dict[str, float]
    emergence_score: float
    is_emergence: bool

    def to_dict(self):
        return asdict(self)


@dataclass
class ExperimentSummary:
    """Summary of all experiments."""

    total_tests: int
    models_tested: List[str]
    conditions_tested: List[str]
    results_by_model: Dict[str, Dict]
    emergence_boost: Dict[str, float]
    sweet_spot_confirmed: bool

    def to_dict(self):
        return asdict(self)


# ============================================================================
# Emergence Measurement
# ============================================================================


def measure_emergence(
    response: str, question: str, baseline: str = ""
) -> Dict[str, float]:
    """
    Measure emergence through multiple metrics.

    Returns dict with:
    - novelty: semantic novelty score
    - integration: concept integration score
    - coherence: logical coherence score
    - surprise: unexpected but meaningful content
    - emergence_score: weighted average
    """
    # Simple heuristics (can be replaced with more sophisticated NLP)

    # 1. Novelty: response length and vocabulary diversity
    words = response.split()
    unique_words = set(words)
    novelty = min(1.0, len(unique_words) / max(len(words), 1))

    # 2. Integration: presence of multiple perspectives
    integration_keywords = [
        "however",
        "on the other hand",
        "while",
        "contrast",
        "synthesis",
        "integrate",
        "balance",
        "tension",
        "paradox",
        "dialectic",
    ]
    integration = min(
        1.0, sum(1 for kw in integration_keywords if kw in response.lower()) / 5
    )

    # 3. Coherence: basic structure check
    has_structure = any(
        marker in response for marker in ["1.", "2.", "First", "Second"]
    )
    coherence = 0.8 if has_structure else 0.5

    # 4. Surprise: unexpected length or complexity
    expected_length = 200  # baseline expected words
    surprise = min(1.0, abs(len(words) - expected_length) / expected_length)

    # Weighted emergence score
    emergence_score = (
        novelty * 0.3 + integration * 0.4 + coherence * 0.2 + surprise * 0.1
    )

    return {
        "novelty": round(novelty, 4),
        "integration": round(integration, 4),
        "coherence": round(coherence, 4),
        "surprise": round(surprise, 4),
        "emergence_score": round(emergence_score, 4),
    }


def is_emergence_event(metrics: Dict[str, float], threshold: float = 0.75) -> bool:
    """Determine if metrics indicate emergence."""
    return metrics["emergence_score"] >= threshold


# ============================================================================
# Prompt Building
# ============================================================================


def build_multi_philosopher_prompt(philosophers: List[str], question: str) -> str:
    """Build a system prompt with multiple philosophers."""

    philosopher_descriptions = "\n\n".join(
        [f"**{name.title()}**: {PHILOSOPHER_PROMPTS[name]}" for name in philosophers]
    )

    system_prompt = f"""You are a philosophical reasoning system integrating multiple perspectives:

{philosopher_descriptions}

Your task:
1. Consider the question from EACH philosopher's perspective
2. Let them interact and create dialectical tension
3. Synthesize their insights into a coherent response
4. Show the creative emergence from their interaction

Question: {question}

Respond with a synthesis that demonstrates how these philosophical perspectives
interact, conflict, and ultimately create new insights through their tension.
"""

    return system_prompt


# ============================================================================
# Manual Testing Instructions
# ============================================================================


def print_manual_test_instructions():
    """Print instructions for manual testing."""

    print("\n" + "=" * 80)
    print("🧪 MANUAL TESTING INSTRUCTIONS")
    print("=" * 80)

    print("\nYou will test 3 LLMs × 3 conditions × 5 questions = 45 tests")
    print("\nFor EACH test:")
    print("  1. Copy the SYSTEM PROMPT below")
    print("  2. Paste it into the LLM chat")
    print("  3. Copy the response")
    print("  4. Rate emergence (0-100%)")
    print("  5. Record results in the spreadsheet")

    print("\n" + "-" * 80)
    print("TEST MATRIX")
    print("-" * 80)

    test_number = 1
    for model_name in MODELS.keys():
        print(f"\n📱 MODEL: {model_name.upper()}")
        for condition_name, condition in CONDITIONS.items():
            print(f"\n  🎭 CONDITION: {condition['name']}")
            print(f"     Philosophers: {', '.join(condition['philosophers'])}")

            for question in TEST_QUESTIONS:
                print(f"\n  Test #{test_number}: {question}")

                # Generate prompt
                prompt = build_multi_philosopher_prompt(
                    condition["philosophers"], question
                )

                print(f"\n  📋 COPY THIS PROMPT:")
                print("  " + "-" * 70)
                print("  " + prompt.replace("\n", "\n  "))
                print("  " + "-" * 70)
                print(f"\n  ⏸️  Paste into {model_name}, get response, rate emergence")
                print(f"     Expected: {condition['expected_emergence']}")

                input("\n  Press ENTER when done to continue...")

                test_number += 1

    print("\n" + "=" * 80)
    print("✅ MANUAL TESTING COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Analyze your recorded results")
    print("2. Calculate emergence rates by condition")
    print("3. Compare across models")
    print("4. Check if Sweet Spot (~78.85%) exists across all models")


# ============================================================================
# Automated Testing (requires API keys)
# ============================================================================


def run_automated_test(
    model_name: str, condition_name: str, question: str
) -> Optional[ExperimentResult]:
    """
    Run automated test (requires API keys).

    NOTE: This is a template. You need to:
    1. Install SDK: pip install openai anthropic google-generativeai
    2. Set API keys as environment variables
    """

    try:
        condition = CONDITIONS[condition_name]
        philosophers = condition["philosophers"]

        # Build prompt
        system_prompt = build_multi_philosopher_prompt(philosophers, question)

        # Query LLM (placeholder - implement with actual API calls)
        response = f"[Placeholder response for {model_name}]"

        # TODO: Implement actual API calls
        # if model_name == "gpt-4":
        #     response = query_openai(system_prompt)
        # elif model_name == "gemini":
        #     response = query_gemini(system_prompt)
        # elif model_name == "claude":
        #     response = query_claude(system_prompt)

        # Measure emergence
        metrics = measure_emergence(response, question)

        result = ExperimentResult(
            timestamp=datetime.now().isoformat(),
            model=model_name,
            condition=condition_name,
            question=question,
            philosophers=philosophers,
            response=response,
            emergence_metrics=metrics,
            emergence_score=metrics["emergence_score"],
            is_emergence=is_emergence_event(metrics),
        )

        return result

    except Exception as e:
        print(f"❌ Error in test: {e}")
        return None


# ============================================================================
# Analysis
# ============================================================================


def analyze_results(results: List[ExperimentResult]) -> ExperimentSummary:
    """Analyze experimental results."""

    # Group by model and condition
    by_model = {}
    for result in results:
        if result.model not in by_model:
            by_model[result.model] = {
                "high_tension": [],
                "low_tension": [],
                "optimal": [],
            }
        by_model[result.model][result.condition].append(result.emergence_score)

    # Calculate averages and boosts
    emergence_boost = {}
    for model, conditions in by_model.items():
        high_avg = (
            sum(conditions["high_tension"]) / len(conditions["high_tension"])
            if conditions["high_tension"]
            else 0
        )
        low_avg = (
            sum(conditions["low_tension"]) / len(conditions["low_tension"])
            if conditions["low_tension"]
            else 0
        )

        if low_avg > 0:
            boost = ((high_avg - low_avg) / low_avg) * 100
            emergence_boost[model] = round(boost, 1)

    # Check if Sweet Spot confirmed
    optimal_scores = []
    for model, conditions in by_model.items():
        if conditions["optimal"]:
            avg = sum(conditions["optimal"]) / len(conditions["optimal"])
            optimal_scores.append(avg)

    sweet_spot_avg = sum(optimal_scores) / len(optimal_scores) if optimal_scores else 0
    sweet_spot_confirmed = 0.75 <= sweet_spot_avg <= 0.85

    summary = ExperimentSummary(
        total_tests=len(results),
        models_tested=list(by_model.keys()),
        conditions_tested=list(CONDITIONS.keys()),
        results_by_model=by_model,
        emergence_boost=emergence_boost,
        sweet_spot_confirmed=sweet_spot_confirmed,
    )

    return summary


def print_results_summary(summary: ExperimentSummary):
    """Print formatted results summary."""

    print("\n" + "=" * 80)
    print("📊 EXPERIMENT RESULTS SUMMARY")
    print("=" * 80)

    print(f"\nTotal tests: {summary.total_tests}")
    print(f"Models tested: {', '.join(summary.models_tested)}")

    print("\n" + "-" * 80)
    print("EMERGENCE BOOST BY MODEL")
    print("-" * 80)

    for model, boost in summary.emergence_boost.items():
        print(f"  {model:15s}: +{boost:6.1f}%  (~{boost/100:.1f}x)")

    if summary.emergence_boost:
        avg_boost = sum(summary.emergence_boost.values()) / len(summary.emergence_boost)
        print(f"\n  {'AVERAGE':15s}: +{avg_boost:6.1f}%  (~{avg_boost/100:.1f}x)")

    print("\n" + "-" * 80)
    print("SWEET SPOT VERIFICATION")
    print("-" * 80)

    print(
        f"  Sweet Spot Confirmed: {'✅ YES' if summary.sweet_spot_confirmed else '❌ NO'}"
    )

    if summary.sweet_spot_confirmed:
        print("\n  🎉 HYPOTHESIS CONFIRMED!")
        print("     The Emergence Sweet Spot exists across multiple LLMs.")
        print("     This is a MODEL-INDEPENDENT universal principle!")
        print("     → Ready for international conference submission!")

    print("\n" + "=" * 80)


# ============================================================================
# Main
# ============================================================================


def main():
    """Main entry point."""

    import argparse

    parser = argparse.ArgumentParser(description="Cross-LLM Emergence Experiment")
    parser.add_argument(
        "--mode",
        choices=["manual", "pilot", "full"],
        default="manual",
        help="Experiment mode",
    )

    args = parser.parse_args()

    print("\n" + "=" * 80)
    print("🧪 CROSS-LLM EMERGENCE SWEET SPOT EXPERIMENT")
    print("=" * 80)
    print("\nTesting hypothesis:")
    print("  'Dialectical tension creates ~20x emergence boost across ALL LLMs'")
    print("\nModels to test:")
    for model in MODELS.keys():
        print(f"  - {model}")

    if args.mode == "manual":
        print("\nMode: MANUAL TESTING")
        print("You will copy prompts to each LLM manually and record results.")
        print_manual_test_instructions()

    elif args.mode == "pilot":
        print("\nMode: PILOT (requires API keys)")
        print("⚠️  Not yet implemented. Coming soon!")
        print("\nTo use automated testing:")
        print("  1. pip install openai anthropic google-generativeai")
        print("  2. Set environment variables:")
        print("     export OPENAI_API_KEY=...")
        print("     export ANTHROPIC_API_KEY=...")
        print("     export GOOGLE_API_KEY=...")
        print("  3. Run this script again")

    elif args.mode == "full":
        print("\nMode: FULL EXPERIMENT (requires API keys)")
        print("⚠️  Not yet implemented. Coming soon!")

    print("\n✅ Script ready!")


if __name__ == "__main__":
    main()
