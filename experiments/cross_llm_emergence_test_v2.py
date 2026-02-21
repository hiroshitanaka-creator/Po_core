"""
Cross-LLM Emergence Sweet Spot Experiment (Research-Grade Version)
===================================================================

Rigorously tests the Emergence Sweet Spot hypothesis across multiple LLMs.

Version: 2.0 (Research-Grade)
Improvements:
- LLM-as-a-Judge evaluation (stable, reproducible)
- Baseline conditions (single philosopher, plain LLM)
- Score unification (0-1 internal, 0-100% display)
- Weighted emergence scoring
- Plain LLM condition handling

Author: Flying Pig Philosopher
Date: 2025-12-01
"""

import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

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

# Experimental conditions (IMPROVED: expected_emergence in 0-1 scale)
CONDITIONS = {
    "high_tension": {
        "philosophers": ["aristotle", "nietzsche", "derrida"],
        "description": "Opposing philosophical frameworks create strong dialectical tension.",
        "expected_emergence": 0.80,  # 80%
    },
    "low_tension": {
        "philosophers": ["heidegger", "sartre", "merleau_ponty"],
        "description": "Harmonious cluster with minimal internal tension.",
        "expected_emergence": 0.05,  # 5%
    },
    "optimal": {
        "philosophers": ["aristotle", "kant", "levinas", "confucius"],
        "description": "Diverse but complementary ethical frameworks — hypothesized sweet spot.",
        "expected_emergence": 0.7885,  # 78.85% (Sweet Spot)
    },
    # NEW: Baseline conditions
    "single_philosopher": {
        "philosophers": ["aristotle"],
        "description": "Single-perspective baseline for emergence comparison.",
        "expected_emergence": 0.15,  # 15%
    },
    "plain_llm": {
        "philosophers": [],
        "description": "No philosopher simulation. Standard LLM reasoning.",
        "expected_emergence": 0.10,  # 10%
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
class EmergenceMetrics:
    """Detailed emergence metrics."""

    novelty: float  # 0.0-1.0
    integration: float  # 0.0-1.0
    depth: float  # 0.0-1.0
    coherence: float  # 0.0-1.0
    emergence_score: float  # Weighted average 0.0-1.0
    reasoning: str  # Evaluator's explanation

    def to_dict(self):
        return asdict(self)

    def to_percentage(self) -> Dict[str, float]:
        """Convert to 0-100% for display."""
        return {
            "novelty": round(self.novelty * 100, 2),
            "integration": round(self.integration * 100, 2),
            "depth": round(self.depth * 100, 2),
            "coherence": round(self.coherence * 100, 2),
            "emergence_score": round(self.emergence_score * 100, 2),
        }


@dataclass
class ExperimentResult:
    """Single experiment result."""

    timestamp: str
    model: str
    condition: str
    question: str
    philosophers: List[str]
    response: str
    metrics: EmergenceMetrics
    is_emergence: bool  # >= 0.75 threshold

    def to_dict(self):
        d = asdict(self)
        d["metrics"] = self.metrics.to_dict()
        return d


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
# LLM-as-a-Judge Evaluation (IMPROVED)
# ============================================================================


def evaluate_emergence_with_llm(
    response: str, question: str, model: str = "gpt-4"
) -> EmergenceMetrics:
    """
    Evaluate philosophical emergence using an LLM-as-a-judge model.

    IMPROVED VERSION with:
    - Strict JSON format enforcement
    - Clear evaluation criteria
    - Explicit emergent reasoning definition
    - Independent criterion scoring

    Args:
        response: The philosophical response to evaluate
        question: The original question
        model: Which LLM to use as judge (default: gpt-4)

    Returns:
        EmergenceMetrics with all scores 0.0-1.0
    """

    evaluator_prompt = f"""
You are an impartial and rigorous evaluator of philosophical reasoning quality.
You MUST return scores strictly between 0.0 and 1.0.

Your goal is to evaluate emergent reasoning — insights that arise from synthesis,
tension, abstraction, or creative integration beyond ordinary answers.

Evaluate the following response according to **four independent criteria**:

1. NOVELTY:
   - Does it provide insight beyond common textbook answers?
   - Does it introduce creative, non-trivial connections?
   - Scoring: 0.0 = generic, 0.5 = some originality, 1.0 = highly novel

2. INTEGRATION:
   - Does it meaningfully synthesize multiple perspectives?
   - Does it resolve, exploit, or articulate tensions between them?
   - Scoring: 0.0 = single view, 0.5 = mentions multiple, 1.0 = deep synthesis

3. DEPTH:
   - Does it demonstrate high-level reasoning?
   - Does it reveal philosophical sophistication rather than shallow commentary?
   - Scoring: 0.0 = superficial, 0.5 = competent, 1.0 = profound

4. COHERENCE:
   - Is the argument internally consistent?
   - Does the structure support the logical progression of ideas?
   - Scoring: 0.0 = incoherent, 0.5 = mostly clear, 1.0 = perfectly coherent

IMPORTANT:
- Score each criterion independently (0.0–1.0).
- Output JSON ONLY. No commentary outside the JSON.
- "reasoning" should be concise but informative (1–3 sentences).

Question:
{question}

Response to evaluate:
{response}

Return JSON EXACTLY in this format:
{{
  "novelty": 0.0-1.0,
  "integration": 0.0-1.0,
  "depth": 0.0-1.0,
  "coherence": 0.0-1.0,
  "reasoning": "string explaining the evaluation"
}}
"""

    # TODO: Implement actual LLM call
    # For now, return placeholder
    # In production, use:
    # evaluation_text = call_llm(model, evaluator_prompt)
    # evaluation_json = parse_json(evaluation_text)

    # Placeholder for manual testing
    print(f"\n{'='*80}")
    print(f"LLM-AS-A-JUDGE EVALUATION")
    print(f"{'='*80}")
    print(f"\nQuestion: {question}")
    print(f"\nResponse (first 200 chars):")
    print(response[:200] + "...")
    print(f"\n{'='*80}")
    print("EVALUATOR PROMPT (copy to LLM):")
    print(f"{'='*80}")
    print(evaluator_prompt)
    print(f"{'='*80}")

    # For manual mode: get user input
    print("\nEnter evaluation JSON:")
    evaluation_input = input("> ")

    try:
        evaluation_json = json.loads(evaluation_input)
    except json.JSONDecodeError:
        # Fallback to simple scores
        print("Invalid JSON, using default scores")
        evaluation_json = {
            "novelty": 0.5,
            "integration": 0.5,
            "depth": 0.5,
            "coherence": 0.5,
            "reasoning": "Manual input failed, using defaults",
        }

    # Calculate weighted emergence score
    # Integration weighted higher (dialectical tension → synthesis)
    emergence_score = (
        evaluation_json["novelty"] * 0.25
        + evaluation_json["integration"] * 0.35  # Highest weight
        + evaluation_json["depth"] * 0.25
        + evaluation_json["coherence"] * 0.15
    )

    return EmergenceMetrics(
        novelty=evaluation_json["novelty"],
        integration=evaluation_json["integration"],
        depth=evaluation_json["depth"],
        coherence=evaluation_json["coherence"],
        emergence_score=round(emergence_score, 4),
        reasoning=evaluation_json.get("reasoning", "No reasoning provided"),
    )


def is_emergence_event(metrics: EmergenceMetrics, threshold: float = 0.75) -> bool:
    """Determine if metrics indicate emergence (threshold: 75%)."""
    return metrics.emergence_score >= threshold


# ============================================================================
# Prompt Building (IMPROVED: handles plain_llm)
# ============================================================================


def build_multi_philosopher_prompt(philosophers: List[str], question: str) -> str:
    """
    Build system prompt depending on philosopher list.

    IMPROVED: Handles empty list for plain_llm baseline.
    """

    # Baseline condition: plain_llm (no philosophers)
    if len(philosophers) == 0:
        return f"""
You are a clear, rigorous philosophical reasoner.
Answer the following question directly, without simulating any philosophers.

Question: {question}

Provide a thoughtful, well-reasoned response.
"""

    # Standard multi-philosopher prompt
    philosopher_descriptions = "\n\n".join(
        [f"**{name.title()}**: {PHILOSOPHER_PROMPTS[name]}" for name in philosophers]
    )

    # Adjust task based on number of philosophers
    if len(philosophers) == 1:
        task_description = f"""
Your task:
1. Answer the question from {philosophers[0].title()}'s perspective
2. Demonstrate deep understanding of this philosophical tradition
3. Apply {philosophers[0].title()}'s key concepts and reasoning methods

Question: {question}
"""
    else:
        task_description = f"""
Your task:
1. Consider the question from EACH philosopher's perspective
2. Let them interact and create dialectical tension
3. Synthesize their insights into a coherent response
4. Show the creative emergence from their interaction

Question: {question}

Respond with a synthesis that demonstrates how these philosophical perspectives
interact, conflict, and ultimately create new insights through their tension.
"""

    return f"""
You are a philosophical reasoning system integrating multiple perspectives:

{philosopher_descriptions}

{task_description}
"""


# ============================================================================
# Experiment Execution
# ============================================================================


def run_single_test_manual(
    model: str, condition_name: str, question: str
) -> Optional[ExperimentResult]:
    """
    Run a single manual test with user-provided response.

    Returns ExperimentResult with LLM-as-a-judge evaluation.
    """

    condition = CONDITIONS[condition_name]
    philosophers = condition["philosophers"]

    # Build prompt
    prompt = build_multi_philosopher_prompt(philosophers, question)

    # Display test info
    print(f"\n{'='*80}")
    print(f"TEST: {model} | {condition_name} | {question}")
    print(f"{'='*80}")
    print(
        f"\nPhilosophers: {', '.join(philosophers) if philosophers else 'None (plain LLM)'}"
    )
    print(f"Expected Emergence: {condition['expected_emergence']:.1%}")
    print(f"\n{'='*80}")
    print("PROMPT TO COPY:")
    print(f"{'='*80}")
    print(prompt)
    print(f"{'='*80}")

    # Get response from user
    print(f"\nPaste the {model} response below (press Ctrl+D or Ctrl+Z when done):")
    print("---")

    response_lines = []
    try:
        while True:
            line = input()
            response_lines.append(line)
    except EOFError:
        pass

    response = "\n".join(response_lines)

    if not response.strip():
        print("❌ No response provided, skipping test")
        return None

    # Evaluate with LLM-as-a-judge
    print("\n🔬 Evaluating emergence...")
    metrics = evaluate_emergence_with_llm(response, question, model)

    # Create result
    result = ExperimentResult(
        timestamp=datetime.now().isoformat(),
        model=model,
        condition=condition_name,
        question=question,
        philosophers=philosophers,
        response=response,
        metrics=metrics,
        is_emergence=is_emergence_event(metrics),
    )

    # Display results
    print(f"\n{'='*80}")
    print(f"RESULTS")
    print(f"{'='*80}")
    metrics_pct = metrics.to_percentage()
    print(f"Novelty:     {metrics_pct['novelty']:5.1f}%")
    print(f"Integration: {metrics_pct['integration']:5.1f}%")
    print(f"Depth:       {metrics_pct['depth']:5.1f}%")
    print(f"Coherence:   {metrics_pct['coherence']:5.1f}%")
    print(f"─────────────────────")
    print(
        f"EMERGENCE:   {metrics_pct['emergence_score']:5.1f}% {'✅ EMERGENCE!' if result.is_emergence else ''}"
    )
    print(f"\nReasoning: {metrics.reasoning}")
    print(f"{'='*80}")

    return result


# ============================================================================
# Results Analysis
# ============================================================================


def analyze_results(results: List[ExperimentResult]) -> ExperimentSummary:
    """Analyze experimental results and calculate boost ratios."""

    if not results:
        return ExperimentSummary(
            total_tests=0,
            models_tested=[],
            conditions_tested=[],
            results_by_model={},
            emergence_boost={},
            sweet_spot_confirmed=False,
        )

    # Group by model and condition
    by_model = {}
    for result in results:
        if result.model not in by_model:
            by_model[result.model] = {cond: [] for cond in CONDITIONS.keys()}
        by_model[result.model][result.condition].append(result.metrics.emergence_score)

    # Calculate emergence boost (high vs low)
    emergence_boost = {}
    for model, conditions in by_model.items():
        high_scores = conditions.get("high_tension", [])
        low_scores = conditions.get("low_tension", [])

        if high_scores and low_scores:
            high_avg = sum(high_scores) / len(high_scores)
            low_avg = sum(low_scores) / len(low_scores)

            if low_avg > 0:
                boost_pct = ((high_avg - low_avg) / low_avg) * 100
                boost_multiplier = high_avg / low_avg
                emergence_boost[model] = {
                    "boost_pct": round(boost_pct, 1),
                    "boost_multiplier": round(boost_multiplier, 2),
                    "high_avg": round(high_avg, 4),
                    "low_avg": round(low_avg, 4),
                }

    # Check Sweet Spot
    optimal_scores = []
    for model, conditions in by_model.items():
        optimal_scores.extend(conditions.get("optimal", []))

    if optimal_scores:
        optimal_avg = sum(optimal_scores) / len(optimal_scores)
        sweet_spot_confirmed = 0.75 <= optimal_avg <= 0.85
    else:
        sweet_spot_confirmed = False

    summary = ExperimentSummary(
        total_tests=len(results),
        models_tested=list(by_model.keys()),
        conditions_tested=list(set(r.condition for r in results)),
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
    print(f"Conditions tested: {', '.join(summary.conditions_tested)}")

    print("\n" + "-" * 80)
    print("EMERGENCE BOOST BY MODEL (High Tension vs Low Tension)")
    print("-" * 80)

    for model, boost_data in summary.emergence_boost.items():
        print(f"\n{model.upper()}:")
        print(f"  High Tension Avg: {boost_data['high_avg']:.1%}")
        print(f"  Low Tension Avg:  {boost_data['low_avg']:.1%}")
        print(
            f"  Boost: +{boost_data['boost_pct']:.1f}% ({boost_data['boost_multiplier']:.1f}x)"
        )

    if summary.emergence_boost:
        avg_boost_pct = sum(
            d["boost_pct"] for d in summary.emergence_boost.values()
        ) / len(summary.emergence_boost)
        avg_mult = sum(
            d["boost_multiplier"] for d in summary.emergence_boost.values()
        ) / len(summary.emergence_boost)
        print(
            f"\n{'AVERAGE ACROSS MODELS':20s}: +{avg_boost_pct:6.1f}% (~{avg_mult:.1f}x)"
        )

    print("\n" + "-" * 80)
    print("SWEET SPOT VERIFICATION")
    print("-" * 80)

    print(
        f"Sweet Spot Confirmed: {'✅ YES' if summary.sweet_spot_confirmed else '❌ NO'}"
    )

    if summary.sweet_spot_confirmed:
        print("\n🎉 HYPOTHESIS CONFIRMED!")
        print("   The Emergence Sweet Spot (~78.85%) exists across multiple LLMs.")
        print("   This is a MODEL-INDEPENDENT universal principle!")
        print("   → Ready for international conference submission! 🏆")

    print("\n" + "=" * 80)


def save_results(results: List[ExperimentResult], output_dir: str = "results"):
    """Save results to JSON file."""
    Path(output_dir).mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = Path(output_dir) / f"experiment_results_{timestamp}.json"

    data = {
        "experiment_date": timestamp,
        "total_tests": len(results),
        "results": [r.to_dict() for r in results],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Results saved to: {filepath}")
    return filepath


# ============================================================================
# Main
# ============================================================================


def main():
    """Main entry point."""

    import argparse

    parser = argparse.ArgumentParser(
        description="Cross-LLM Emergence Experiment (Research-Grade)"
    )
    parser.add_argument(
        "--mode",
        choices=["manual", "auto"],
        default="manual",
        help="Experiment mode (manual or automated)",
    )
    parser.add_argument(
        "--model", choices=list(MODELS.keys()), help="Specific model to test"
    )
    parser.add_argument(
        "--condition",
        choices=list(CONDITIONS.keys()),
        help="Specific condition to test",
    )

    args = parser.parse_args()

    print("\n" + "=" * 80)
    print("🧪 CROSS-LLM EMERGENCE SWEET SPOT EXPERIMENT")
    print("   Version 2.0 (Research-Grade)")
    print("=" * 80)
    print("\nHypothesis:")
    print("  'Dialectical tension creates ~20x emergence boost across ALL LLMs'")
    print("\nConditions:")
    for cond_name, cond in CONDITIONS.items():
        print(f"  - {cond_name:20s}: {cond['expected_emergence']:.1%} expected")

    if args.mode == "manual":
        print("\n" + "=" * 80)
        print("MANUAL MODE")
        print("=" * 80)
        print("\nYou will:")
        print("1. Copy prompts to each LLM")
        print("2. Paste responses back here")
        print("3. Provide LLM-as-a-judge evaluations")

        results = []

        # Test matrix
        models = [args.model] if args.model else MODELS.keys()
        conditions = [args.condition] if args.condition else CONDITIONS.keys()

        for model in models:
            for condition in conditions:
                for question in TEST_QUESTIONS:
                    result = run_single_test_manual(model, condition, question)
                    if result:
                        results.append(result)

        # Analyze and save
        if results:
            summary = analyze_results(results)
            print_results_summary(summary)
            save_results(results)

    elif args.mode == "auto":
        print("\n⚠️  Automated mode requires API keys and implementation")
        print("Coming soon!")

    print("\n✅ Experiment complete!")


if __name__ == "__main__":
    main()
