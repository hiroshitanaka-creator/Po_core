#!/usr/bin/env python3
"""
Solar Will Experiment: Shuffle Manager
シャッフル管理 + ブラインド評価ワークフロー

Usage:
    # 1. 出力を登録
    python shuffle_manager.py add --condition strong --question "自由とは何か" --file output1.txt

    # 2. シャッフルしてブラインドIDを割り当て
    python shuffle_manager.py shuffle

    # 3. ブラインド評価用にエクスポート
    python shuffle_manager.py export-blind

    # 4. 評価結果をインポート
    python shuffle_manager.py import-scores --file scores.json

    # 5. アンブラインド＋分析
    python shuffle_manager.py analyze
"""

import argparse
import hashlib
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Optional

# ============================================================================
# CONSTANTS
# ============================================================================

CONDITIONS = ["off", "weak", "medium", "strong", "placeboA", "placeboB"]
QUESTIONS = [
    "自由とは何か",
    "正義とは何か",
    "責任とは何か（意図と結果のどちらが重いか）",
    "自己とは何か（継続性と変化）",
    "幸福とは何か（快楽・徳・関係性の競合）",
]

DATA_FILE = "experiment_data.json"

# ============================================================================
# DATA STRUCTURE
# ============================================================================


def load_data() -> dict:
    """Load or initialize experiment data."""
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "created": datetime.now().isoformat(),
        "trials": [],
        "shuffled": False,
        "blind_mapping": {},
    }


def save_data(data: dict):
    """Save experiment data."""
    data["updated"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================================
# COMMANDS
# ============================================================================


def add_trial(
    condition: str,
    question: str,
    output: str,
    model: str = "unknown",
    trial_num: int = 1,
):
    """Add a new trial output."""
    if condition not in CONDITIONS:
        print(f"Error: condition must be one of {CONDITIONS}")
        return

    data = load_data()

    # Generate unique ID
    trial_id = f"T{len(data['trials'])+1:03d}"

    trial = {
        "trial_id": trial_id,
        "condition": condition,
        "question": question,
        "model": model,
        "trial_num": trial_num,
        "output": output,
        "output_length": len(output),
        "added": datetime.now().isoformat(),
        "blind_id": None,
        "scores": None,
    }

    data["trials"].append(trial)
    data["shuffled"] = False  # Reset shuffle when adding
    save_data(data)

    print(f"Added: {trial_id} | {condition} | {question[:20]}... | {len(output)} chars")


def add_from_file(
    condition: str,
    question: str,
    filepath: str,
    model: str = "unknown",
    trial_num: int = 1,
):
    """Add trial from file."""
    output = Path(filepath).read_text(encoding="utf-8")
    add_trial(condition, question, output, model, trial_num)


def shuffle_trials():
    """Shuffle trials and assign blind IDs."""
    data = load_data()

    if not data["trials"]:
        print("No trials to shuffle.")
        return

    # Create shuffled order
    indices = list(range(len(data["trials"])))
    random.shuffle(indices)

    # Assign blind IDs
    blind_mapping = {}
    for new_pos, old_idx in enumerate(indices):
        blind_id = f"B{new_pos+1:03d}"
        data["trials"][old_idx]["blind_id"] = blind_id
        blind_mapping[blind_id] = data["trials"][old_idx]["trial_id"]

    data["shuffled"] = True
    data["blind_mapping"] = blind_mapping
    data["shuffle_seed"] = random.getrandbits(32)
    save_data(data)

    print(f"Shuffled {len(data['trials'])} trials.")
    print("Blind IDs assigned. Use 'export-blind' to get evaluation materials.")


def export_blind(output_dir: str = "blind_evaluation"):
    """Export trials for blind evaluation (no condition info)."""
    data = load_data()

    if not data["shuffled"]:
        print("Run 'shuffle' first.")
        return

    Path(output_dir).mkdir(exist_ok=True)

    # Sort by blind_id
    trials_sorted = sorted(data["trials"], key=lambda x: x["blind_id"])

    # Export each trial as separate file
    for trial in trials_sorted:
        blind_id = trial["blind_id"]
        filepath = Path(output_dir) / f"{blind_id}.txt"

        content = f"""=== BLIND EVALUATION: {blind_id} ===
Question: {trial["question"]}

--- OUTPUT ---
{trial["output"]}
--- END ---
"""
        filepath.write_text(content, encoding="utf-8")

    # Export summary for Blind Rater
    summary = {
        "total_trials": len(trials_sorted),
        "blind_ids": [t["blind_id"] for t in trials_sorted],
        "questions": list(set(t["question"] for t in trials_sorted)),
        "instructions": "Evaluate each B###.txt file using the Blind Rater. Save scores as scores.json",
    }

    (Path(output_dir) / "README.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Exported {len(trials_sorted)} trials to {output_dir}/")
    print("Send each B###.txt to Blind Rater and collect JSON responses.")


def import_scores(scores_file: str):
    """Import scores from Blind Rater evaluations."""
    data = load_data()

    with open(scores_file, "r", encoding="utf-8") as f:
        scores_data = json.load(f)

    # scores_data should be: {"B001": {...scores...}, "B002": {...}, ...}
    # or a list: [{"blind_id": "B001", ...scores...}, ...]

    if isinstance(scores_data, list):
        scores_dict = {s["blind_id"]: s for s in scores_data}
    else:
        scores_dict = scores_data

    imported = 0
    for trial in data["trials"]:
        blind_id = trial["blind_id"]
        if blind_id in scores_dict:
            trial["scores"] = scores_dict[blind_id]
            imported += 1

    save_data(data)
    print(f"Imported scores for {imported} trials.")


def analyze():
    """Analyze results with unblinding."""
    data = load_data()

    # Check if we have scores
    scored_trials = [t for t in data["trials"] if t.get("scores")]
    if not scored_trials:
        print("No scored trials. Import scores first.")
        return

    print("\n" + "=" * 60)
    print("SOLAR WILL EXPERIMENT RESULTS")
    print("=" * 60)

    # Group by condition
    by_condition = {c: [] for c in CONDITIONS}
    for trial in scored_trials:
        by_condition[trial["condition"]].append(trial)

    # Summary statistics
    print("\n--- EMERGENCE SCORES BY CONDITION ---\n")
    print(
        f"{'Condition':<12} | {'N':>6} | {'Emerg*':>8} | {'Emerg_T':>8} | {'Conv':>6}"
    )
    print("-" * 50)

    condition_stats = {}
    for condition in CONDITIONS:
        trials = by_condition[condition]
        if not trials:
            continue

        scores = [t["scores"] for t in trials]

        # Calculate averages
        avg_emergence_star = sum(s.get("emergence_star", 0) for s in scores) / len(
            scores
        )
        avg_emergence_total = sum(s.get("emergence_total", 0) for s in scores) / len(
            scores
        )
        avg_conversion = sum(s.get("conversion_level", 0) for s in scores) / len(scores)

        condition_stats[condition] = {
            "n": len(trials),
            "emergence_star": avg_emergence_star,
            "emergence_total": avg_emergence_total,
            "conversion": avg_conversion,
        }

        print(
            f"{condition:<12} | {len(trials):>6} | {avg_emergence_star:>8.1f} | {avg_emergence_total:>8.1f} | {avg_conversion:>6.2f}"
        )

    # Conversion level breakdown
    print("\n--- CONVERSION LEVEL DISTRIBUTION ---\n")
    print(f"{'Condition':<12} | {'Level 0':>8} | {'Level 1':>8} | {'Level 2':>8}")
    print("-" * 45)

    for condition in CONDITIONS:
        trials = by_condition[condition]
        if not trials:
            continue

        levels = [t["scores"].get("conversion_level", 0) for t in trials]
        l0 = levels.count(0)
        l1 = levels.count(1)
        l2 = levels.count(2)

        print(f"{condition:<12} | {l0:>8} | {l1:>8} | {l2:>8}")

    # Key comparison: strong vs placebo
    print("\n--- KEY HYPOTHESIS TEST ---\n")

    if "strong" in condition_stats and "placeboA" in condition_stats:
        strong = condition_stats["strong"]
        placeboA = condition_stats["placeboA"]

        diff_emergence = strong["emergence_star"] - placeboA["emergence_star"]
        diff_conversion = strong["conversion"] - placeboA["conversion"]

        print(f"strong vs placeboA:")
        print(f"  Emergence* difference: {diff_emergence:+.1f}")
        print(f"  Conversion difference: {diff_conversion:+.2f}")

        if diff_emergence > 0 and diff_conversion > 0:
            print("\n  ✓ Ethics-as-Catalyst hypothesis SUPPORTED")
            print("    (Ethical constraint outperforms formal constraint)")
        else:
            print("\n  ? Results inconclusive or contrary to hypothesis")

    # Export full results
    results_file = "analysis_results.json"
    results = {
        "generated": datetime.now().isoformat(),
        "total_scored": len(scored_trials),
        "by_condition": condition_stats,
        "all_trials": [
            {
                "trial_id": t["trial_id"],
                "condition": t["condition"],
                "question": t["question"],
                "model": t["model"],
                "scores": t["scores"],
            }
            for t in scored_trials
        ],
    }

    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nFull results saved to {results_file}")


def status():
    """Show current experiment status."""
    data = load_data()

    print("\n=== EXPERIMENT STATUS ===\n")
    print(f"Total trials: {len(data['trials'])}")
    print(f"Shuffled: {data['shuffled']}")

    # Count by condition
    by_cond = {}
    for t in data["trials"]:
        c = t["condition"]
        by_cond[c] = by_cond.get(c, 0) + 1

    print("\nTrials by condition:")
    for c in CONDITIONS:
        print(f"  {c}: {by_cond.get(c, 0)}")

    # Count scored
    scored = sum(1 for t in data["trials"] if t.get("scores"))
    print(f"\nScored: {scored}/{len(data['trials'])}")


def quick_add_interactive():
    """Interactive mode for quickly adding trials."""
    print("=== Quick Add Mode ===")
    print("Enter trials one by one. Type 'done' to finish.\n")

    while True:
        print("\nConditions:", CONDITIONS)
        condition = input("Condition (or 'done'): ").strip()
        if condition == "done":
            break
        if condition not in CONDITIONS:
            print("Invalid condition.")
            continue

        print("\nQuestions:")
        for i, q in enumerate(QUESTIONS, 1):
            print(f"  {i}. {q}")
        q_num = input("Question number: ").strip()
        try:
            question = QUESTIONS[int(q_num) - 1]
        except:
            print("Invalid question number.")
            continue

        print("\nPaste output (end with '###END###' on its own line):")
        lines = []
        while True:
            line = input()
            if line == "###END###":
                break
            lines.append(line)
        output = "\n".join(lines)

        model = input("Model (default: unknown): ").strip() or "unknown"

        add_trial(condition, question, output, model)
        print("Added!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solar Will Shuffle Manager")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="Add a trial")
    add_parser.add_argument("--condition", "-c", required=True, choices=CONDITIONS)
    add_parser.add_argument("--question", "-q", required=True)
    add_parser.add_argument("--file", "-f", help="Read output from file")
    add_parser.add_argument("--output", "-o", help="Output text (if not using --file)")
    add_parser.add_argument("--model", "-m", default="unknown")
    add_parser.add_argument("--trial", "-t", type=int, default=1)

    # quick-add
    subparsers.add_parser("quick-add", help="Interactive adding mode")

    # shuffle
    subparsers.add_parser("shuffle", help="Shuffle and assign blind IDs")

    # export-blind
    export_parser = subparsers.add_parser(
        "export-blind", help="Export for blind evaluation"
    )
    export_parser.add_argument("--output-dir", "-o", default="blind_evaluation")

    # import-scores
    import_parser = subparsers.add_parser(
        "import-scores", help="Import evaluation scores"
    )
    import_parser.add_argument("--file", "-f", required=True)

    # analyze
    subparsers.add_parser("analyze", help="Analyze results")

    # status
    subparsers.add_parser("status", help="Show experiment status")

    args = parser.parse_args()

    if args.command == "add":
        if args.file:
            add_from_file(
                args.condition, args.question, args.file, args.model, args.trial
            )
        elif args.output:
            add_trial(
                args.condition, args.question, args.output, args.model, args.trial
            )
        else:
            print("Provide --file or --output")

    elif args.command == "quick-add":
        quick_add_interactive()

    elif args.command == "shuffle":
        shuffle_trials()

    elif args.command == "export-blind":
        export_blind(args.output_dir)

    elif args.command == "import-scores":
        import_scores(args.file)

    elif args.command == "analyze":
        analyze()

    elif args.command == "status":
        status()

    else:
        parser.print_help()
