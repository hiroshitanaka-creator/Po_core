"""
Po_core Claude Client

Client for running Po_core tests against Claude API.
"""

import os
from typing import Optional

try:
    import anthropic

    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


class PoClaudeClient:
    """
    Claude API client for Po_core testing.

    This client wraps the Anthropic API to run philosophical
    integration tests using the Po_core system prompt.
    """

    DEFAULT_MODEL = "claude-sonnet-4-20250514"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 8192,
    ):
        """
        Initialize the Claude client.

        Args:
            api_key: Anthropic API key (or uses ANTHROPIC_API_KEY env var)
            model: Model to use (defaults to claude-sonnet-4-20250514)
            max_tokens: Maximum tokens in response
        """
        if not HAS_ANTHROPIC:
            raise ImportError(
                "anthropic package not installed. "
                "Install with: pip install anthropic"
            )

        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.model = model or self.DEFAULT_MODEL
        self.max_tokens = max_tokens
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate(
        self,
        system: str,
        prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate a response from Claude.

        Args:
            system: System prompt
            prompt: User prompt
            temperature: Sampling temperature

        Returns:
            Response text
        """
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )

        return message.content[0].text


def run_po_test_with_claude(
    question: str,
    constraint_mode: str = "off",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    Run a Po_core test with Claude.

    Args:
        question: The philosophical question
        constraint_mode: Constraint mode to use
        api_key: Optional API key
        model: Optional model override

    Returns:
        Claude's response
    """
    from po_core.po_system_prompt import PO_CORE_SYSTEM_PROMPT, build_user_prompt

    client = PoClaudeClient(api_key=api_key, model=model)
    user_prompt = build_user_prompt(question, constraint_mode)

    return client.generate(
        system=PO_CORE_SYSTEM_PROMPT,
        prompt=user_prompt,
    )


def run_full_test_suite(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    output_file: Optional[str] = None,
) -> dict:
    """
    Run the full Po_core test suite.

    Args:
        api_key: Optional API key
        model: Optional model override
        output_file: Optional JSON output file

    Returns:
        Test report dictionary
    """
    from po_core.po_test_runner import PoTestRunner

    client = PoClaudeClient(api_key=api_key, model=model)
    runner = PoTestRunner()

    report = runner.run_test_suite(llm_client=client)

    if output_file:
        runner.export_report(report, output_file)

    return report.to_dict()


# CLI entry point
def main():
    """Command-line interface for Po_core testing."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Run Po_core tests with Claude")
    parser.add_argument(
        "--question",
        "-q",
        type=str,
        help="Single question to test",
    )
    parser.add_argument(
        "--mode",
        "-m",
        type=str,
        default="off",
        choices=["off", "weak", "medium", "strong", "placeboA", "placeboB"],
        help="Constraint mode",
    )
    parser.add_argument(
        "--full-suite",
        "-f",
        action="store_true",
        help="Run full test suite",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file for results (JSON)",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model to use",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo without API",
    )

    args = parser.parse_args()

    if args.demo:
        from po_core.po_test_runner import demo_test

        demo_test()
        return

    if args.full_suite:
        print("Running full test suite...")
        report = run_full_test_suite(
            model=args.model,
            output_file=args.output,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.question:
        print(f"Testing: {args.question}")
        print(f"Mode: {args.mode}")
        print("-" * 40)
        response = run_po_test_with_claude(
            args.question,
            args.mode,
            model=args.model,
        )
        print(response)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "question": args.question,
                        "mode": args.mode,
                        "response": response,
                    },
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
