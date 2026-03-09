"""
Po_core Click CLI

Non-interactive command-line interface for philosophical reasoning.
Provides subcommands: hello, status, version, prompt, log.
"""

import json
import sys

import click

from po_core import __version__
from po_core.app.api import run as _run

# ──────────────────────────────────────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────────────────────────────────────


def _run_reasoning(user_input: str) -> dict:
    """Run reasoning and return a normalised result dict."""
    result = _run(user_input=user_input)
    proposal = result.get("proposal", {})
    return {
        "request_id": result.get("request_id", ""),
        "status": result.get("status", "ok"),
        "prompt": user_input,
        "responses": [
            {
                "philosopher": (
                    proposal.get("proposal_id", "").split(":")[1]
                    if ":" in proposal.get("proposal_id", "")
                    else "unknown"
                ),
                "content": proposal.get("content", ""),
                "action_type": proposal.get("action_type", "answer"),
                "confidence": proposal.get("confidence", 0.0),
            }
        ],
        "metrics": {
            "confidence": proposal.get("confidence", 0.0),
            "action_type": proposal.get("action_type", "answer"),
        },
        "events": [
            {
                "step": "proposal",
                "proposal_id": proposal.get("proposal_id", ""),
                "action_type": proposal.get("action_type", "answer"),
                "confidence": proposal.get("confidence", 0.0),
            }
        ],
    }


# ──────────────────────────────────────────────────────────────────────────────
# CLI root
# ──────────────────────────────────────────────────────────────────────────────


@click.group()
@click.version_option(
    version=__version__,
    prog_name="Po_core",
    message="Po_core %(version)s",
)
def main() -> None:
    """Po_core — Philosophy-Driven AI Deliberation Framework."""


# ──────────────────────────────────────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────────────────────────────────────


@main.command()
@click.option(
    "--sample/--no-sample",
    default=True,
    help="Run a sample reasoning and display results.",
)
def hello(sample: bool) -> None:
    """Print a welcome message for Po_core."""
    click.echo("Po_core — Philosophy-Driven AI Deliberation Framework")
    click.echo(f"Version: {__version__}")
    if sample:
        try:
            data = _run_reasoning("What is justice?")
            resp = data["responses"][0] if data["responses"] else {}
            click.echo(f"Consensus Lead: {resp.get('philosopher', 'unknown')}")
            click.echo(f"Philosophers: 42 active")
            click.echo(
                f"Metrics: confidence={data['metrics'].get('confidence', 0):.3f}"
            )
        except Exception as exc:  # pragma: no cover
            click.echo(f"[sample error: {exc}]", err=True)


@main.command()
@click.option("--sample", is_flag=True, help="Include a sample run in the output.")
def status(sample: bool) -> None:
    """Show project and philosophical framework status."""
    click.echo("Project Status")
    click.echo(f"  Version        : {__version__}")
    click.echo(f"  Philosophers   : 42")
    click.echo("Philosophical Framework")
    click.echo("  SolarWill axiom : do not distort survival structures")
    click.echo("  SafetyModes     : NORMAL / WARN / CRITICAL")
    click.echo("Documentation")
    click.echo("  Specs  : docs/spec/")
    click.echo("  ADRs   : docs/adr/")
    if sample:
        try:
            data = _run_reasoning("Demonstrate ethical reasoning.")
            resp = data["responses"][0] if data["responses"] else {}
            click.echo(f"Consensus Lead: {resp.get('philosopher', 'unknown')}")
        except Exception as exc:  # pragma: no cover
            click.echo(f"[sample error: {exc}]", err=True)


@main.command(name="version")
def version_cmd() -> None:
    """Print the current Po_core version."""
    click.echo(__version__)


@main.command(name="prompt")
@click.argument("prompt_text")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["json", "text"], case_sensitive=False),
    default="json",
    help="Output format (json or text).",
)
def prompt_cmd(prompt_text: str, fmt: str) -> None:
    """Run philosophical reasoning on PROMPT_TEXT."""
    if not prompt_text:
        data = {"prompt": "", "responses": [], "metrics": {}}
        if fmt == "json":
            click.echo(json.dumps(data))
        else:
            click.echo("(empty prompt)")
        return
    try:
        data = _run_reasoning(prompt_text)
    except Exception as exc:  # pragma: no cover
        click.echo(json.dumps({"error": str(exc)}), err=True)
        sys.exit(1)

    if fmt == "json":
        click.echo(
            json.dumps(
                {
                    "prompt": data["prompt"],
                    "responses": data["responses"],
                    "metrics": data["metrics"],
                }
            )
        )
    else:
        click.echo(f"Prompt  : {data['prompt']}")
        for resp in data["responses"]:
            click.echo(f"Response: [{resp['philosopher']}] {resp['content'][:120]}")
        click.echo(f"Metrics : confidence={data['metrics'].get('confidence', 0):.3f}")


@main.command(name="log")
@click.argument("prompt_text")
def log_cmd(prompt_text: str) -> None:
    """Run reasoning on PROMPT_TEXT and emit the trace log as JSON."""
    try:
        data = _run_reasoning(prompt_text)
    except Exception as exc:  # pragma: no cover
        click.echo(json.dumps({"error": str(exc)}), err=True)
        sys.exit(1)
    click.echo(json.dumps({"prompt": data["prompt"], "events": data["events"]}))
