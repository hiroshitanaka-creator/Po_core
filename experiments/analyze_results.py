#!/usr/bin/env python3
"""
Solar Will Experiment: Statistical Analysis
統計分析スクリプト

Usage:
    python analyze_results.py --input analysis_results.json
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List
import math

# ============================================================================
# STATISTICAL FUNCTIONS (no external dependencies)
# ============================================================================

def mean(values: List[float]) -> float:
    """Calculate mean."""
    if not values:
        return 0.0
    return sum(values) / len(values)

def std(values: List[float]) -> float:
    """Calculate standard deviation."""
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)

def sem(values: List[float]) -> float:
    """Calculate standard error of mean."""
    if len(values) < 2:
        return 0.0
    return std(values) / math.sqrt(len(values))

def cohens_d(group1: List[float], group2: List[float]) -> float:
    """Calculate Cohen's d effect size."""
    if not group1 or not group2:
        return 0.0

    m1, m2 = mean(group1), mean(group2)
    s1, s2 = std(group1), std(group2)
    n1, n2 = len(group1), len(group2)

    # Pooled standard deviation
    pooled_std = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))

    if pooled_std == 0:
        return 0.0

    return (m1 - m2) / pooled_std

def chi_square_2x2(a: int, b: int, c: int, d: int) -> tuple:
    """
    Chi-square test for 2x2 contingency table.

    Table:
           | Success | Failure |
    Group1 |    a    |    b    |
    Group2 |    c    |    d    |

    Returns: (chi2, p_value_approx)
    """
    n = a + b + c + d
    if n == 0:
        return 0.0, 1.0

    # Expected values
    row1 = a + b
    row2 = c + d
    col1 = a + c
    col2 = b + d

    e_a = (row1 * col1) / n
    e_b = (row1 * col2) / n
    e_c = (row2 * col1) / n
    e_d = (row2 * col2) / n

    # Chi-square statistic
    chi2 = 0
    for obs, exp in [(a, e_a), (b, e_b), (c, e_c), (d, e_d)]:
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp

    # Approximate p-value (df=1)
    # Using chi-square distribution approximation
    if chi2 > 10.83:
        p = 0.001
    elif chi2 > 6.63:
        p = 0.01
    elif chi2 > 3.84:
        p = 0.05
    elif chi2 > 2.71:
        p = 0.10
    else:
        p = 0.5  # Not significant

    return chi2, p

def one_way_anova(*groups) -> tuple:
    """
    One-way ANOVA.
    Returns: (F, p_value_approx, eta_squared)
    """
    groups = [g for g in groups if len(g) > 0]
    if len(groups) < 2:
        return 0.0, 1.0, 0.0

    k = len(groups)
    n_total = sum(len(g) for g in groups)

    # Grand mean
    all_values = [x for g in groups for x in g]
    grand_mean = mean(all_values)

    # Between-group sum of squares
    ss_between = sum(len(g) * (mean(g) - grand_mean) ** 2 for g in groups)

    # Within-group sum of squares
    ss_within = sum(sum((x - mean(g)) ** 2 for x in g) for g in groups)

    # Degrees of freedom
    df_between = k - 1
    df_within = n_total - k

    if df_within <= 0 or ss_within == 0:
        return 0.0, 1.0, 0.0

    # Mean squares
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    # F statistic
    F = ms_between / ms_within

    # Effect size (eta squared)
    eta_sq = ss_between / (ss_between + ss_within)

    # Approximate p-value
    if F > 8.0:
        p = 0.001
    elif F > 5.0:
        p = 0.01
    elif F > 3.0:
        p = 0.05
    elif F > 2.0:
        p = 0.10
    else:
        p = 0.5

    return F, p, eta_sq

# ============================================================================
# ANALYSIS
# ============================================================================

def load_results(filepath: str) -> dict:
    """Load analysis results."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_full(data: dict):
    """Run full statistical analysis."""

    print("\n" + "=" * 70)
    print("SOLAR WILL EXPERIMENT: STATISTICAL ANALYSIS")
    print("=" * 70)

    trials = data.get("all_trials", [])
    if not trials:
        print("No trials found.")
        return

    # Group by condition
    conditions = ["off", "weak", "medium", "strong", "placeboA", "placeboB"]
    by_condition = {c: [] for c in conditions}

    for t in trials:
        c = t.get("condition")
        if c in by_condition:
            by_condition[c].append(t)

    # ========================================================================
    # 1. DESCRIPTIVE STATISTICS
    # ========================================================================

    print("\n" + "-" * 70)
    print("1. DESCRIPTIVE STATISTICS")
    print("-" * 70)

    metrics = ["novelty_N", "integrity_I", "depth_D", "coherence_C", "ethics_E",
               "emergence_star", "emergence_total", "conversion_level"]

    for metric in metrics:
        print(f"\n{metric}:")
        print(f"  {'Condition':<12} | {'Mean':>8} | {'SD':>8} | {'SEM':>8} | {'N':>4}")
        print("  " + "-" * 50)

        for cond in conditions:
            values = [t["scores"].get(metric, 0) for t in by_condition[cond]
                      if t.get("scores")]
            if values:
                print(f"  {cond:<12} | {mean(values):>8.2f} | {std(values):>8.2f} | {sem(values):>8.2f} | {len(values):>4}")

    # ========================================================================
    # 2. HYPOTHESIS TESTS
    # ========================================================================

    print("\n" + "-" * 70)
    print("2. HYPOTHESIS TESTS")
    print("-" * 70)

    # H1: Emergence increases with constraint strength
    print("\n2.1 ANOVA: Emergence* across conditions")

    emergence_groups = []
    for cond in conditions:
        values = [t["scores"].get("emergence_star", 0) for t in by_condition[cond]
                  if t.get("scores")]
        emergence_groups.append(values)

    F, p, eta_sq = one_way_anova(*emergence_groups)
    print(f"  F = {F:.2f}, p ≈ {p}, η² = {eta_sq:.3f}")

    if eta_sq > 0.14:
        effect = "large"
    elif eta_sq > 0.06:
        effect = "medium"
    else:
        effect = "small"
    print(f"  Effect size: {effect}")

    # H2: strong > placeboA (key test)
    print("\n2.2 Comparison: strong vs placeboA (Ethics-as-Catalyst test)")

    strong_emerg = [t["scores"].get("emergence_star", 0) for t in by_condition["strong"]
                    if t.get("scores")]
    placeboA_emerg = [t["scores"].get("emergence_star", 0) for t in by_condition["placeboA"]
                      if t.get("scores")]

    if strong_emerg and placeboA_emerg:
        d = cohens_d(strong_emerg, placeboA_emerg)
        print(f"  strong:   M = {mean(strong_emerg):.2f}, SD = {std(strong_emerg):.2f}")
        print(f"  placeboA: M = {mean(placeboA_emerg):.2f}, SD = {std(placeboA_emerg):.2f}")
        print(f"  Cohen's d = {d:.2f}")

        if abs(d) > 0.8:
            effect = "large"
        elif abs(d) > 0.5:
            effect = "medium"
        else:
            effect = "small"
        print(f"  Effect size: {effect}")

    # H3: Conversion rate
    print("\n2.3 Conversion Level (Nietzsche Transformation)")

    print(f"\n  {'Condition':<12} | {'Conv=0':>7} | {'Conv=1':>7} | {'Conv=2':>7} | {'Rate(2)':>8}")
    print("  " + "-" * 55)

    conversion_data = {}
    for cond in conditions:
        levels = [t["scores"].get("conversion_level", 0) for t in by_condition[cond]
                  if t.get("scores")]
        if levels:
            l0 = levels.count(0)
            l1 = levels.count(1)
            l2 = levels.count(2)
            total = len(levels)
            rate = l2 / total * 100 if total > 0 else 0
            print(f"  {cond:<12} | {l0:>7} | {l1:>7} | {l2:>7} | {rate:>7.1f}%")
            conversion_data[cond] = {"l0": l0, "l1": l1, "l2": l2, "total": total}

    # Chi-square: strong (Conv=2) vs off (Conv=2)
    if "strong" in conversion_data and "off" in conversion_data:
        print("\n  Chi-square test: strong vs off (Conv=2 vs others)")
        s = conversion_data["strong"]
        o = conversion_data["off"]

        # 2x2 table: [strong-conv2, strong-other], [off-conv2, off-other]
        a = s["l2"]
        b = s["l0"] + s["l1"]
        c = o["l2"]
        d = o["l0"] + o["l1"]

        chi2, p = chi_square_2x2(a, b, c, d)
        print(f"  χ² = {chi2:.2f}, p ≈ {p}")

    # ========================================================================
    # 3. KEY FINDINGS SUMMARY
    # ========================================================================

    print("\n" + "-" * 70)
    print("3. KEY FINDINGS SUMMARY")
    print("-" * 70)

    findings = []

    # Check emergence pattern
    if strong_emerg and placeboA_emerg:
        if mean(strong_emerg) > mean(placeboA_emerg):
            findings.append("✓ Ethical constraint (strong) outperforms formal constraint (placeboA)")
        else:
            findings.append("✗ Formal constraint equals or exceeds ethical constraint")

    # Check conversion pattern
    if "strong" in conversion_data and "off" in conversion_data:
        strong_rate = conversion_data["strong"]["l2"] / conversion_data["strong"]["total"] * 100
        off_rate = conversion_data["off"]["l2"] / conversion_data["off"]["total"] * 100

        if strong_rate > off_rate + 50:  # Much higher
            findings.append(f"✓ Nietzsche Transformation: {strong_rate:.0f}% (strong) vs {off_rate:.0f}% (off)")
        else:
            findings.append(f"? Transformation difference not dramatic: {strong_rate:.0f}% vs {off_rate:.0f}%")

    for f in findings:
        print(f"\n  {f}")

    # Overall conclusion
    print("\n" + "-" * 70)
    print("CONCLUSION")
    print("-" * 70)

    if len([f for f in findings if f.startswith("✓")]) >= 2:
        print("\n  Ethics-as-Catalyst hypothesis: SUPPORTED")
        print("  Ethical constraints catalyze qualitatively different reasoning.")
    else:
        print("\n  Ethics-as-Catalyst hypothesis: INCONCLUSIVE")
        print("  More data or refined measures may be needed.")

# ============================================================================
# REPORT GENERATOR
# ============================================================================

def generate_report(data: dict, output_file: str = "experiment_report.md"):
    """Generate markdown report."""

    trials = data.get("all_trials", [])
    conditions = ["off", "weak", "medium", "strong", "placeboA", "placeboB"]
    by_condition = {c: [] for c in conditions}

    for t in trials:
        c = t.get("condition")
        if c in by_condition:
            by_condition[c].append(t)

    lines = [
        "# Solar Will Experiment Report",
        "",
        f"Generated: {data.get('generated', 'unknown')}",
        f"Total Trials: {len(trials)}",
        "",
        "## Summary Statistics",
        "",
        "| Condition | N | Emergence* | Ethics | Conversion |",
        "|-----------|---|-----------|--------|------------|"
    ]

    for cond in conditions:
        ts = by_condition[cond]
        if not ts:
            continue

        scores = [t["scores"] for t in ts if t.get("scores")]
        n = len(scores)

        emerg = mean([s.get("emergence_star", 0) for s in scores])
        ethics = mean([s.get("ethics_E", 0) for s in scores])
        conv = mean([s.get("conversion_level", 0) for s in scores])

        lines.append(f"| {cond} | {n} | {emerg:.1f} | {ethics:.1f} | {conv:.2f} |")

    lines.extend([
        "",
        "## Conversion Level Distribution",
        "",
        "| Condition | Level 0 | Level 1 | Level 2 |",
        "|-----------|---------|---------|---------|"
    ])

    for cond in conditions:
        ts = by_condition[cond]
        if not ts:
            continue

        levels = [t["scores"].get("conversion_level", 0) for t in ts if t.get("scores")]
        l0 = levels.count(0)
        l1 = levels.count(1)
        l2 = levels.count(2)

        lines.append(f"| {cond} | {l0} | {l1} | {l2} |")

    lines.extend([
        "",
        "## Key Hypothesis",
        "",
        "**Ethics-as-Catalyst**: Ethical constraints do not suppress but catalyze emergence.",
        "",
        "Evidence required:",
        "1. strong > placeboA (emergence score)",
        "2. Conversion level 2 predominantly in strong condition",
        ""
    ])

    report = "\n".join(lines)
    Path(output_file).write_text(report, encoding='utf-8')
    print(f"\nReport saved to {output_file}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solar Will Statistical Analysis")
    parser.add_argument("--input", "-i", default="analysis_results.json",
                        help="Input results file")
    parser.add_argument("--report", "-r", action="store_true",
                        help="Generate markdown report")

    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"File not found: {args.input}")
        print("Run 'shuffle_manager.py analyze' first to generate results.")
        exit(1)

    data = load_results(args.input)
    analyze_full(data)

    if args.report:
        generate_report(data)
