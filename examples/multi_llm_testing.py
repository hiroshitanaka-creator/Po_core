"""
Po_core Multi-LLM Testing Framework

Compare philosophical reasoning quality across different LLMs.
"""
from typing import Dict, List, Optional
import json
from dataclasses import dataclass
from pathlib import Path
import time


@dataclass
class LLMTestResult:
    """Result of testing one LLM on one prompt."""
    llm_name: str
    prompt: str
    response: str
    freedom_pressure: float
    semantic_delta: float
    blocked_tensor: float
    latency_ms: float
    cost_estimate: float
    philosopher_diversity: float  # 0-1, how diverse philosophers' views were


class MultiLLMTester:
    """Test Po_core across multiple LLM backends."""

    def __init__(self):
        self.results: List[LLMTestResult] = []

    def test_llm(
        self,
        llm_name: str,
        prompt: str,
        llm_backend,  # Your LLM interface
        num_runs: int = 3
    ) -> List[LLMTestResult]:
        """Test one LLM multiple times for consistency.

        Args:
            llm_name: Name of the LLM (e.g., "gpt-4", "claude-3.5")
            prompt: The philosophical question
            llm_backend: Interface to the LLM
            num_runs: Number of times to run (for consistency check)

        Returns:
            List of test results
        """
        results = []

        for run in range(num_runs):
            start = time.time()

            # Generate response (you'd implement this based on your backend)
            response_data = llm_backend.generate(prompt)

            latency = (time.time() - start) * 1000  # ms

            result = LLMTestResult(
                llm_name=llm_name,
                prompt=prompt,
                response=response_data["text"],
                freedom_pressure=response_data.get("freedom_pressure", 0.0),
                semantic_delta=response_data.get("semantic_delta", 0.0),
                blocked_tensor=response_data.get("blocked_tensor", 0.0),
                latency_ms=latency,
                cost_estimate=self._estimate_cost(llm_name, response_data),
                philosopher_diversity=self._calculate_diversity(response_data)
            )

            results.append(result)
            self.results.append(result)

        return results

    def _estimate_cost(self, llm_name: str, response_data: Dict) -> float:
        """Estimate cost based on LLM pricing."""
        # Rough estimates (update with actual pricing)
        costs = {
            "gpt-4": 0.03,
            "gpt-4o": 0.005,
            "gpt-4o-mini": 0.0003,
            "claude-3.5-sonnet": 0.003,
            "claude-3.5-haiku": 0.0008,
            "gemini-1.5-pro": 0.00125,
            "ollama": 0.0,  # Free (local)
            "mock": 0.0,
        }

        base_cost = costs.get(llm_name.lower(), 0.01)

        # Estimate tokens (rough)
        prompt_tokens = len(response_data.get("prompt", "").split()) * 1.3
        response_tokens = len(response_data.get("text", "").split()) * 1.3

        return base_cost * (prompt_tokens + response_tokens) / 1000

    def _calculate_diversity(self, response_data: Dict) -> float:
        """Calculate how diverse philosopher perspectives were."""
        philosophers = response_data.get("philosophers_involved", [])
        if len(philosophers) < 2:
            return 0.0

        # Calculate variance in tension metrics
        fps = [p.get("freedom_pressure", 0.5) for p in response_data.get("philosopher_responses", [])]
        if not fps:
            return 0.0

        variance = sum((x - sum(fps)/len(fps))**2 for x in fps) / len(fps)
        return min(variance * 4, 1.0)  # Normalize to 0-1

    def compare_llms(
        self,
        llm_configs: List[Dict],
        test_prompts: List[str]
    ) -> Dict:
        """Compare multiple LLMs on multiple prompts.

        Args:
            llm_configs: List of {"name": "gpt-4", "backend": backend_instance}
            test_prompts: List of questions to test

        Returns:
            Comparison report
        """
        for prompt in test_prompts:
            for config in llm_configs:
                self.test_llm(
                    llm_name=config["name"],
                    prompt=prompt,
                    llm_backend=config["backend"],
                    num_runs=3
                )

        return self.generate_report()

    def generate_report(self) -> Dict:
        """Generate comparison report."""
        if not self.results:
            return {"error": "No results to report"}

        # Group by LLM
        by_llm = {}
        for result in self.results:
            if result.llm_name not in by_llm:
                by_llm[result.llm_name] = []
            by_llm[result.llm_name].append(result)

        # Calculate statistics
        report = {
            "summary": {},
            "details": by_llm,
            "recommendations": []
        }

        for llm_name, results in by_llm.items():
            n = len(results)

            avg_fp = sum(r.freedom_pressure for r in results) / n
            avg_latency = sum(r.latency_ms for r in results) / n
            avg_cost = sum(r.cost_estimate for r in results) / n
            avg_diversity = sum(r.philosopher_diversity for r in results) / n

            # Consistency: standard deviation of freedom_pressure
            fp_values = [r.freedom_pressure for r in results]
            fp_std = (sum((x - avg_fp)**2 for x in fp_values) / n) ** 0.5

            report["summary"][llm_name] = {
                "avg_freedom_pressure": round(avg_fp, 3),
                "consistency": round(1 - fp_std, 3),  # Higher = more consistent
                "avg_latency_ms": round(avg_latency, 1),
                "avg_cost_per_session": round(avg_cost, 4),
                "philosopher_diversity": round(avg_diversity, 3),
                "quality_score": round((avg_fp + avg_diversity + (1-fp_std)) / 3, 3)
            }

        # Add recommendations
        best_quality = max(report["summary"].items(), key=lambda x: x[1]["quality_score"])
        best_cost = min(report["summary"].items(), key=lambda x: x[1]["avg_cost_per_session"])
        best_speed = min(report["summary"].items(), key=lambda x: x[1]["avg_latency_ms"])

        report["recommendations"] = [
            f"Best Quality: {best_quality[0]} (score: {best_quality[1]['quality_score']})",
            f"Best Cost: {best_cost[0]} (${best_cost[1]['avg_cost_per_session']:.4f}/session)",
            f"Best Speed: {best_speed[0]} ({best_speed[1]['avg_latency_ms']:.0f}ms)",
        ]

        return report

    def export_report(self, output_path: Path) -> None:
        """Export report to JSON."""
        report = self.generate_report()

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"Report exported to: {output_path}")


# Example usage
if __name__ == "__main__":
    from po_core.mock_philosophers import MockPoSelf

    tester = MultiLLMTester()

    # Test with mock (for demonstration)
    mock_backend = MockPoSelf(enable_trace=True)

    test_prompts = [
        "What is freedom?",
        "Should AI have rights?",
        "What is the meaning of life?"
    ]

    # Run tests
    for prompt in test_prompts:
        results = tester.test_llm(
            llm_name="mock",
            prompt=prompt,
            llm_backend=mock_backend,
            num_runs=3
        )

        print(f"\nPrompt: {prompt}")
        print(f"  Avg FP: {sum(r.freedom_pressure for r in results) / len(results):.3f}")
        print(f"  Avg Latency: {sum(r.latency_ms for r in results) / len(results):.0f}ms")

    # Generate report
    report = tester.generate_report()
    print("\n" + "="*60)
    print("SUMMARY REPORT")
    print("="*60)
    for llm, stats in report["summary"].items():
        print(f"\n{llm}:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    for rec in report["recommendations"]:
        print(f"  • {rec}")
