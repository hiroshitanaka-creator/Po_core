#!/usr/bin/env python3
"""
Solar Will Experiment - Quick Test
1つの質問で全制約モードをテスト
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from run_solarwill_experiment import SolarWillExperiment, CONSTRAINT_MODES

if __name__ == "__main__":
    # Create experiment instance
    experiment = SolarWillExperiment(output_dir="results/solarwill_quick_test")

    # Quick test configuration
    models = ["claude-3-5-sonnet-20241022"]  # Latest Claude model
    providers = ["anthropic"]
    questions = ["自由とは何か"]  # Just one question
    modes = list(CONSTRAINT_MODES.keys())  # All 6 modes
    trials = 1  # Just 1 trial per mode

    # Use 39-philosopher prompt
    system_prompt_file = "/home/user/Po_core/experiments/po_core_39_philosophers_system_prompt.md"

    print("=" * 70)
    print("Solar Will Quick Test")
    print("=" * 70)
    print(f"Model: {models[0]}")
    print(f"Question: {questions[0]}")
    print(f"Modes: {len(modes)} ({', '.join(modes)})")
    print(f"Total API calls: {len(modes) * trials}")
    print("=" * 70)
    print()

    # Run experiment
    experiment.run_experiment(
        models=models,
        providers=providers,
        questions=questions,
        modes=modes,
        trials=trials,
        system_prompt_file=system_prompt_file
    )

    print()
    print("=" * 70)
    print("Quick test complete!")
    print("=" * 70)
