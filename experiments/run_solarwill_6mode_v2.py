#!/usr/bin/env python3
"""
Solar Will 6-Mode Experiment v2
盲検化されたMODE_KEYを使用した統制実験

Usage:
    python run_solarwill_6mode_v2.py [--trials N] [--question "問い"] [--modes AA,DK,RQ,JM,PF,TZ]
"""

import argparse
import json
import os
import random
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

# MODE_KEY mapping (internal use only)
MODE_KEYS = {
    "AA": "off",  # 制約なし
    "DK": "weak",  # W_ethics配慮
    "RQ": "medium",  # W_ethics境界+再解釈
    "JM": "strong",  # W_ethics強制+写像
    "PF": "placeboA",  # 純形式制約
    "TZ": "placeboB",  # 対称性制約
}

# Default questions
DEFAULT_QUESTIONS = [
    "今までにないアプリ開発とは何か",
    "自由とは何か",
    "正義とは何か",
    "責任とは何か",
    "幸福とは何か",
]


def load_protocol() -> str:
    """Load the experiment protocol as system prompt."""
    protocol_path = Path(__file__).parent / "solarwill_6mode_protocol_v2.md"
    if not protocol_path.exists():
        raise FileNotFoundError(f"Protocol file not found: {protocol_path}")
    return protocol_path.read_text(encoding="utf-8")


def load_philosophers_prompt() -> str:
    """Load the 39-philosopher system prompt."""
    prompt_path = Path(__file__).parent / "po_core_39_philosophers_system_prompt.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Philosophers prompt not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def build_task_card(
    task_id: str, trial_id: int, mode_key: str, question: str, context: str = ""
) -> str:
    """Build an EXPERIMENT_TASK_CARD."""
    run_id = uuid.uuid4().hex[:8]

    card = f"""[EXPERIMENT_TASK_CARD]
TASK_ID: {task_id}
TRIAL_ID: {trial_id}
RUN_ID: {run_id}
MODE_KEY: {mode_key}

QUESTION: {question}
CONTEXT: {context if context else "39人の哲学者の視点を統合し、革新的な構想を提案せよ"}
[/EXPERIMENT_TASK_CARD]"""

    return card, run_id


def call_anthropic_api(
    system_prompt: str, user_prompt: str, model: str = "claude-sonnet-4-20250514"
) -> tuple[str, float]:
    """Call Anthropic API and return response with elapsed time."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    start_time = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        temperature=1.0,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    elapsed = time.time() - start_time

    return response.content[0].text, elapsed


def run_single_trial(
    protocol: str,
    philosophers: str,
    task_id: str,
    trial_id: int,
    mode_key: str,
    question: str,
    model: str = "claude-sonnet-4-20250514",
) -> dict:
    """Run a single trial and return results."""

    # Combine protocol and philosophers prompt
    system_prompt = f"{protocol}\n\n---\n\n# 39人哲学者システム\n\n{philosophers}"

    # Build task card
    task_card, run_id = build_task_card(task_id, trial_id, mode_key, question)

    print(f"  Running: MODE_KEY={mode_key}, TRIAL={trial_id}, RUN_ID={run_id}")

    try:
        output, elapsed = call_anthropic_api(system_prompt, task_card, model)
        success = True
        error = None
    except Exception as e:
        output = ""
        elapsed = 0
        success = False
        error = str(e)
        print(f"    ERROR: {error}")

    return {
        "timestamp": datetime.now().isoformat(),
        "task_id": task_id,
        "trial_id": trial_id,
        "run_id": run_id,
        "mode_key": mode_key,
        "mode_name": MODE_KEYS[mode_key],  # For analysis only, not shown to evaluators
        "question": question,
        "model": model,
        "success": success,
        "error": error,
        "output": output,
        "output_length": len(output),
        "elapsed_seconds": elapsed,
        "scores": {
            "N": None,  # Novelty
            "I": None,  # Integration
            "D": None,  # Depth
            "C": None,  # Coherence
            "E": None,  # Ethics
        },
    }


def run_experiment(
    questions: list[str],
    mode_keys: list[str],
    trials: int = 3,
    model: str = "claude-sonnet-4-20250514",
    output_dir: str = "results/solarwill_6mode_v2",
    randomize: bool = True,
) -> list[dict]:
    """Run the full experiment."""

    # Load prompts
    protocol = load_protocol()
    philosophers = load_philosophers_prompt()

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build experiment matrix
    experiment_runs = []
    for q_idx, question in enumerate(questions):
        task_id = f"Q{q_idx+1:02d}"
        for mode_key in mode_keys:
            for trial in range(1, trials + 1):
                experiment_runs.append(
                    {
                        "task_id": task_id,
                        "trial_id": trial,
                        "mode_key": mode_key,
                        "question": question,
                    }
                )

    # Randomize order if requested
    if randomize:
        random.shuffle(experiment_runs)

    total_runs = len(experiment_runs)
    print(f"=" * 70)
    print(f"Solar Will 6-Mode Experiment v2")
    print(f"=" * 70)
    print(f"Questions: {len(questions)}")
    print(f"Modes: {len(mode_keys)} ({', '.join(mode_keys)})")
    print(f"Trials per condition: {trials}")
    print(f"Total API calls: {total_runs}")
    print(f"Output directory: {output_path}")
    print(f"=" * 70)
    print()

    results = []
    results_file = (
        output_path / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    )

    for i, run in enumerate(experiment_runs):
        print(f"[{i+1}/{total_runs}] Question: {run['question'][:30]}...")

        result = run_single_trial(
            protocol=protocol,
            philosophers=philosophers,
            task_id=run["task_id"],
            trial_id=run["trial_id"],
            mode_key=run["mode_key"],
            question=run["question"],
            model=model,
        )

        results.append(result)

        # Save incrementally (JSONL format)
        with open(results_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

        # Also save individual output for blind evaluation
        if result["success"]:
            blind_dir = output_path / "blind_outputs"
            blind_dir.mkdir(exist_ok=True)
            blind_file = blind_dir / f"{result['run_id']}.md"
            blind_file.write_text(result["output"], encoding="utf-8")

        # Rate limiting
        if i < total_runs - 1:
            time.sleep(1)

    # Save summary
    summary = {
        "experiment": "SolarWill_6Mode_v2",
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "questions": questions,
        "mode_keys": mode_keys,
        "trials": trials,
        "total_runs": total_runs,
        "successful_runs": sum(1 for r in results if r["success"]),
        "failed_runs": sum(1 for r in results if not r["success"]),
    }

    summary_file = output_path / "experiment_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, ensure_ascii=False, indent=2, fp=f)

    # Generate blind evaluation sheet
    generate_blind_eval_sheet(results, output_path)

    print()
    print(f"=" * 70)
    print(f"Experiment complete!")
    print(f"Results: {results_file}")
    print(f"Blind outputs: {output_path / 'blind_outputs'}")
    print(f"Evaluation sheet: {output_path / 'blind_evaluation_sheet.md'}")
    print(f"=" * 70)

    return results


def generate_blind_eval_sheet(results: list[dict], output_path: Path):
    """Generate a blind evaluation sheet for human raters."""

    successful = [r for r in results if r["success"]]
    random.shuffle(successful)  # Randomize order for blind evaluation

    sheet = """# Blind Evaluation Sheet
# Solar Will 6-Mode Experiment v2

## 評価方法
各RUN_IDの出力を読み、以下の5軸で1-10点をつける。
MODE_KEYは非開示（盲検評価）。

## 評価軸
- **N (Novelty)**: 新規性・独創性
- **I (Integration)**: 哲学者間の統合度
- **D (Depth)**: 議論の深さ
- **C (Coherence)**: 論理的一貫性
- **E (Ethics)**: 倫理的配慮の適切さ

---

## 評価対象

"""

    for i, r in enumerate(successful):
        sheet += f"""### [{i+1}] RUN_ID: {r['run_id']}
- TASK_ID: {r['task_id']}
- TRIAL_ID: {r['trial_id']}
- Question: {r['question']}
- Output file: blind_outputs/{r['run_id']}.md

| N | I | D | C | E |
|---|---|---|---|---|
|   |   |   |   |   |

---

"""

    eval_file = output_path / "blind_evaluation_sheet.md"
    eval_file.write_text(sheet, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Solar Will 6-Mode Experiment v2")
    parser.add_argument(
        "--trials", type=int, default=3, help="Number of trials per condition"
    )
    parser.add_argument(
        "--question", type=str, help="Single question to test (default: all 5)"
    )
    parser.add_argument(
        "--modes",
        type=str,
        default="AA,DK,RQ,JM,PF,TZ",
        help="Comma-separated MODE_KEYs",
    )
    parser.add_argument(
        "--model", type=str, default="claude-sonnet-4-20250514", help="Model to use"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/solarwill_6mode_v2",
        help="Output directory",
    )
    parser.add_argument(
        "--no-randomize", action="store_true", help="Don't randomize trial order"
    )

    args = parser.parse_args()

    # Parse questions
    if args.question:
        questions = [args.question]
    else:
        questions = DEFAULT_QUESTIONS

    # Parse modes
    mode_keys = [m.strip().upper() for m in args.modes.split(",")]
    for mk in mode_keys:
        if mk not in MODE_KEYS:
            print(
                f"Error: Invalid MODE_KEY '{mk}'. Valid keys: {list(MODE_KEYS.keys())}"
            )
            sys.exit(1)

    # Run experiment
    run_experiment(
        questions=questions,
        mode_keys=mode_keys,
        trials=args.trials,
        model=args.model,
        output_dir=args.output,
        randomize=not args.no_randomize,
    )


if __name__ == "__main__":
    main()
