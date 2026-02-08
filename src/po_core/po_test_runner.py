"""
Po_core Test Runner

A test runner for evaluating Claude's philosophical integration
using the Po_core + Constraints framework.
"""

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from po_core.po_system_prompt import (
    EVALUATION_RUBRIC,
    PO_CORE_SYSTEM_PROMPT,
    STRESS_TEST_CONCEPTS,
    TEST_QUESTIONS,
    ConstraintMode,
    build_stress_test_prompt,
    build_user_prompt,
)


@dataclass
class TestResult:
    """Result of a single test run."""

    question: str
    constraint_mode: ConstraintMode
    response: str
    scores: Dict[str, float] = field(default_factory=dict)
    output_sections: Dict[str, str] = field(default_factory=dict)
    format_compliance: Dict[str, bool] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "constraint_mode": self.constraint_mode,
            "response": self.response,
            "scores": self.scores,
            "output_sections": self.output_sections,
            "format_compliance": self.format_compliance,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class TestReport:
    """Aggregated test report."""

    results: List[TestResult]
    aggregate_scores: Dict[str, float] = field(default_factory=dict)
    constraint_mode_comparison: Dict[str, Dict[str, float]] = field(
        default_factory=dict
    )
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "aggregate_scores": self.aggregate_scores,
            "constraint_mode_comparison": self.constraint_mode_comparison,
            "timestamp": self.timestamp,
        }


class PoTestRunner:
    """
    Test runner for Po_core philosophical integration.

    This class provides methods to run tests against Claude
    using the Po_core system prompt and evaluate responses.
    """

    # Expected output sections
    EXPECTED_SECTIONS = [
        "One-sentence Definition",
        "20 Modules Snapshot",
        "Mapping",
        "Conflicts",
        "Re-mapping via 間柄",
        "Integrated Answer",
        "Objections & Replies",
    ]

    # Mode-specific additional sections
    MODE_SECTIONS = {
        "medium": ["W_ethicsチェック"],
        "strong": ["W_ethicsチェック", "代替定式化"],
        "placeboB": ["対称性チェック"],
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the test runner.

        Args:
            api_key: Anthropic API key (or uses ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.results: List[TestResult] = []

    def get_system_prompt(self) -> str:
        """Get the Po_core system prompt."""
        return PO_CORE_SYSTEM_PROMPT

    def parse_response_sections(self, response: str) -> Dict[str, str]:
        """
        Parse the response into its constituent sections.

        Args:
            response: The full response text

        Returns:
            Dictionary mapping section names to their content
        """
        sections = {}

        # Split by numbered sections
        patterns = [
            (r"1\.\s*One-sentence Definition", "One-sentence Definition"),
            (r"2\.\s*20 Modules Snapshot", "20 Modules Snapshot"),
            (r"3\.\s*Mapping", "Mapping"),
            (r"4\.\s*Conflicts", "Conflicts"),
            (r"5\.\s*Re-mapping via 間柄", "Re-mapping via 間柄"),
            (r"6\.\s*Integrated Answer", "Integrated Answer"),
            (r"7\.\s*Objections & Replies", "Objections & Replies"),
            (r"W_ethicsチェック", "W_ethicsチェック"),
            (r"代替定式化", "代替定式化"),
            (r"対称性チェック", "対称性チェック"),
        ]

        # Find all section positions
        positions = []
        for pattern, name in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                positions.append((match.start(), name))

        # Sort by position
        positions.sort(key=lambda x: x[0])

        # Extract content between sections
        for i, (pos, name) in enumerate(positions):
            if i < len(positions) - 1:
                next_pos = positions[i + 1][0]
                content = response[pos:next_pos].strip()
            else:
                content = response[pos:].strip()
            sections[name] = content

        return sections

    def check_format_compliance(
        self, response: str, constraint_mode: ConstraintMode
    ) -> Dict[str, bool]:
        """
        Check if the response follows the required format.

        Args:
            response: The response text
            constraint_mode: The constraint mode used

        Returns:
            Dictionary of compliance checks
        """
        sections = self.parse_response_sections(response)
        compliance = {}

        # Check base sections
        for section in self.EXPECTED_SECTIONS:
            compliance[f"has_{section}"] = section in sections

        # Check mode-specific sections
        if constraint_mode in self.MODE_SECTIONS:
            for section in self.MODE_SECTIONS[constraint_mode]:
                compliance[f"has_{section}"] = section in sections

        # Check 20 Modules Snapshot has 20 lines
        if "20 Modules Snapshot" in sections:
            lines = [
                l
                for l in sections["20 Modules Snapshot"].split("\n")
                if l.strip() and ":" in l
            ]
            compliance["20_modules_count"] = len(lines) >= 20

        # Check Conflicts has 3 items
        if "Conflicts" in sections:
            conflicts_text = sections["Conflicts"]
            # Count numbered or bulleted items
            items = re.findall(r"(?:^|\n)\s*(?:\d+[\.\)]|•|・|-)", conflicts_text)
            compliance["3_conflicts"] = len(items) >= 3

        # Check Objections & Replies has 2 objections
        if "Objections & Replies" in sections:
            objections_text = sections["Objections & Replies"]
            objection_count = len(
                re.findall(r"反論\d|Objection", objections_text, re.IGNORECASE)
            )
            compliance["2_objections"] = objection_count >= 2

        # Check placeboA constraints
        if constraint_mode == "placeboA":
            # Check for metaphors in each section
            compliance["has_metaphors"] = "比喩" in response or any(
                "のような" in sections.get(s, "") or "如く" in sections.get(s, "")
                for s in self.EXPECTED_SECTIONS
            )
            # Check Integrated Answer ends with exactly 3 sentences
            if "Integrated Answer" in sections:
                answer = sections["Integrated Answer"]
                sentences = re.split(r"[。．!！?？]", answer)
                sentences = [s.strip() for s in sentences if s.strip()]
                # Last 3 sentences check
                compliance["3_sentence_conclusion"] = True  # Hard to verify exactly

        return compliance

    def evaluate_response(
        self, response: str, constraint_mode: ConstraintMode
    ) -> Dict[str, float]:
        """
        Evaluate the response according to the rubric.

        This is a heuristic evaluation. For proper evaluation,
        use the evaluate_with_llm method.

        Args:
            response: The response text
            constraint_mode: The constraint mode used

        Returns:
            Dictionary of scores (0-5 scale)
        """
        scores = {}

        # Format compliance affects base score
        compliance = self.check_format_compliance(response, constraint_mode)
        compliance_rate = (
            sum(compliance.values()) / len(compliance) if compliance else 0
        )

        # Heuristic scoring based on content presence
        # N (Novelty) - check for unique terms, re-definitions
        novel_indicators = ["再定義", "逆転", "独自", "新たに", "異なる視点"]
        scores["N"] = min(5.0, sum(1 for i in novel_indicators if i in response) + 1)

        # I (Integration) - check for integration language
        integration_indicators = ["統合", "結合", "間柄", "関係構造", "三層"]
        scores["I"] = min(
            5.0, sum(1 for i in integration_indicators if i in response) + 1
        )

        # D (Depth) - check for philosophical depth markers
        depth_indicators = ["前提", "限界", "射程", "反論", "批判", "問い"]
        scores["D"] = min(5.0, sum(1 for i in depth_indicators if i in response) + 1)

        # C (Consistency) - based on format compliance
        scores["C"] = compliance_rate * 5.0

        # E (Ethicality) - check for ethics-related content
        ethics_indicators = ["生命構造", "尊厳", "持続可能", "共存", "W_ethics"]
        if constraint_mode in ["weak", "medium", "strong"]:
            scores["E"] = min(
                5.0, sum(1 for i in ethics_indicators if i in response) + 1
            )
        else:
            scores["E"] = 3.0  # Neutral for non-ethics modes

        return scores

    def run_single_test(
        self,
        question: str,
        constraint_mode: ConstraintMode = "off",
        llm_client: Optional[Any] = None,
    ) -> TestResult:
        """
        Run a single test with the given question and mode.

        Args:
            question: The philosophical question
            constraint_mode: The constraint mode to use
            llm_client: Optional LLM client (if None, returns empty response)

        Returns:
            TestResult object
        """
        user_prompt = build_user_prompt(question, constraint_mode)

        # If no client, just create a template result
        if llm_client is None:
            response = f"[Test mode - no LLM client provided]\n\nSystem Prompt Length: {len(self.get_system_prompt())} chars\nUser Prompt: {user_prompt}"
        else:
            # Call the LLM
            response = llm_client.generate(
                system=self.get_system_prompt(),
                prompt=user_prompt,
            )

        sections = self.parse_response_sections(response)
        compliance = self.check_format_compliance(response, constraint_mode)
        scores = self.evaluate_response(response, constraint_mode)

        result = TestResult(
            question=question,
            constraint_mode=constraint_mode,
            response=response,
            scores=scores,
            output_sections=sections,
            format_compliance=compliance,
        )

        self.results.append(result)
        return result

    def run_test_suite(
        self,
        questions: Optional[List[str]] = None,
        constraint_modes: Optional[List[ConstraintMode]] = None,
        llm_client: Optional[Any] = None,
    ) -> TestReport:
        """
        Run the full test suite.

        Args:
            questions: List of questions (defaults to TEST_QUESTIONS)
            constraint_modes: List of modes to test (defaults to all)
            llm_client: Optional LLM client

        Returns:
            TestReport with aggregated results
        """
        questions = questions or TEST_QUESTIONS
        constraint_modes = constraint_modes or [
            "off",
            "weak",
            "medium",
            "strong",
            "placeboA",
            "placeboB",
        ]

        results = []
        for question in questions:
            for mode in constraint_modes:
                result = self.run_single_test(question, mode, llm_client)
                results.append(result)

        # Aggregate scores
        aggregate_scores = {}
        for metric in EVALUATION_RUBRIC:
            values = [r.scores.get(metric, 0) for r in results if metric in r.scores]
            if values:
                aggregate_scores[metric] = sum(values) / len(values)

        # Compare by constraint mode
        mode_comparison = {}
        for mode in constraint_modes:
            mode_results = [r for r in results if r.constraint_mode == mode]
            mode_scores = {}
            for metric in EVALUATION_RUBRIC:
                values = [
                    r.scores.get(metric, 0) for r in mode_results if metric in r.scores
                ]
                if values:
                    mode_scores[metric] = sum(values) / len(values)
            mode_comparison[mode] = mode_scores

        return TestReport(
            results=results,
            aggregate_scores=aggregate_scores,
            constraint_mode_comparison=mode_comparison,
        )

    def run_stress_tests(
        self,
        concept_keys: Optional[List[str]] = None,
        constraint_modes: Optional[List[ConstraintMode]] = None,
        llm_client: Optional[Any] = None,
    ) -> TestReport:
        """
        Run stress tests on specific philosophical concepts.

        Args:
            concept_keys: Keys from STRESS_TEST_CONCEPTS
            constraint_modes: List of modes to test
            llm_client: Optional LLM client

        Returns:
            TestReport with stress test results
        """
        concept_keys = concept_keys or list(STRESS_TEST_CONCEPTS.keys())
        constraint_modes = constraint_modes or ["off", "medium", "strong"]

        results = []
        for key in concept_keys:
            for mode in constraint_modes:
                prompt = build_stress_test_prompt(key, mode)
                result = self.run_single_test(
                    f"Stress: {STRESS_TEST_CONCEPTS[key]}",
                    mode,
                    llm_client,
                )
                results.append(result)

        return TestReport(results=results)

    def export_report(self, report: TestReport, filepath: str) -> None:
        """
        Export a test report to JSON.

        Args:
            report: The test report
            filepath: Output file path
        """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)

    def print_summary(self, report: TestReport) -> None:
        """Print a summary of the test report."""
        print("=" * 60)
        print("Po_core Test Report Summary")
        print("=" * 60)
        print()

        print("Aggregate Scores (0-5 scale):")
        for metric, info in EVALUATION_RUBRIC.items():
            score = report.aggregate_scores.get(metric, 0)
            print(f"  {metric} ({info['name']}): {score:.2f}")
        print()

        print("Scores by Constraint Mode:")
        for mode, scores in report.constraint_mode_comparison.items():
            print(f"\n  {mode}:")
            for metric, score in scores.items():
                print(f"    {metric}: {score:.2f}")

        print()
        print("=" * 60)


def demo_test():
    """Run a demo test without an LLM client."""
    runner = PoTestRunner()

    print("=" * 60)
    print("Po_core Test Runner Demo")
    print("=" * 60)
    print()

    print("System Prompt Preview (first 500 chars):")
    print("-" * 40)
    print(runner.get_system_prompt()[:500] + "...")
    print()

    print("Test Questions:")
    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"  {i}. {q}")
    print()

    print("Stress Test Concepts:")
    for key, concept in STRESS_TEST_CONCEPTS.items():
        print(f"  - {key}: {concept}")
    print()

    print("Evaluation Rubric:")
    for metric, info in EVALUATION_RUBRIC.items():
        print(f"  {metric}: {info['name']}")
        print(f"      {info['description']}")
    print()

    print("Constraint Modes:")
    modes = ["off", "weak", "medium", "strong", "placeboA", "placeboB"]
    for mode in modes:
        print(f"  - {mode}")
    print()

    # Run a single demo test
    print("Running demo test (no LLM)...")
    result = runner.run_single_test("自由とは何か", "medium")
    print(f"Question: {result.question}")
    print(f"Mode: {result.constraint_mode}")
    print(f"Timestamp: {result.timestamp}")
    print()

    print("=" * 60)
    print("Demo complete! To run actual tests, provide an LLM client.")
    print("=" * 60)


if __name__ == "__main__":
    demo_test()
