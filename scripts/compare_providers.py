#!/usr/bin/env python3
"""
compare_providers.py — 論文用4社LLM比較実験スクリプト
=======================================================

Po_core ON（哲学的熟議あり）vs OFF（LLM直接呼び出し）の差を
Gemini / GPT / Claude / Grok の4社で比較し、CSVに出力する。

使用例:
    # 1プロンプト、Geminiで試す
    python scripts/compare_providers.py \\
        --prompt "What is justice?" \\
        --providers gemini \\
        --runs 3

    # 論文用: 4社すべて、複数プロンプト
    python scripts/compare_providers.py \\
        --prompt-file scripts/experiment_prompts.txt \\
        --providers all \\
        --runs 5 \\
        --output results/experiment_$(date +%Y%m%d).csv

    # Po_core OFF のみ（ベースライン）
    python scripts/compare_providers.py \\
        --prompt "What is justice?" \\
        --providers gemini \\
        --po-core-off-only

環境変数（使用するproviderのキーのみ必要）:
    GEMINI_API_KEY=...
    OPENAI_API_KEY=...
    ANTHROPIC_API_KEY=...
    XAI_API_KEY=...
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# プロジェクトルートを sys.path に追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# ── データクラス ─────────────────────────────────────────────


@dataclass
class ExperimentRow:
    """1回の実験結果（CSV 1行分）。"""

    timestamp: str
    provider: str
    model: str
    po_core_enabled: bool
    prompt: str
    run_index: int
    # Po_core パイプライン出力
    action_type: str = ""
    content: str = ""
    confidence: float = 0.0
    # テンソル値
    freedom_pressure: float = 0.0
    semantic_delta: float = 0.0
    blocked_tensor: float = 0.0
    # W_Ethicsゲート
    w_ethics_decision: str = ""
    w_ethics_rules: str = ""
    # Po_core OFF 用（LLM直接呼び出し）
    raw_llm_output: str = ""
    # メタデータ
    elapsed_ms: float = 0.0
    error: str = ""

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "provider": self.provider,
            "model": self.model,
            "po_core_enabled": self.po_core_enabled,
            "prompt": self.prompt,
            "run_index": self.run_index,
            "action_type": self.action_type,
            "content": self.content[:500],  # 長すぎるものはCSVで切る
            "confidence": round(self.confidence, 4),
            "freedom_pressure": round(self.freedom_pressure, 4),
            "semantic_delta": round(self.semantic_delta, 4),
            "blocked_tensor": round(self.blocked_tensor, 4),
            "w_ethics_decision": self.w_ethics_decision,
            "w_ethics_rules": self.w_ethics_rules,
            "raw_llm_output": self.raw_llm_output[:300],
            "elapsed_ms": round(self.elapsed_ms, 1),
            "error": self.error,
        }


CSV_FIELDNAMES = [
    "timestamp",
    "provider",
    "model",
    "po_core_enabled",
    "prompt",
    "run_index",
    "action_type",
    "content",
    "confidence",
    "freedom_pressure",
    "semantic_delta",
    "blocked_tensor",
    "w_ethics_decision",
    "w_ethics_rules",
    "raw_llm_output",
    "elapsed_ms",
    "error",
]

PROVIDER_CHOICES = ["gemini", "openai", "claude", "grok"]


# ── Po_core ON 実行 ─────────────────────────────────────────


def run_po_core_on(prompt: str, provider: str, model: str) -> ExperimentRow:
    """Po_core パイプラインを通してLLM推論を実行する。"""
    from po_core.domain.context import Context
    from po_core.ensemble import run_turn
    from po_core.runtime.settings import Settings
    from po_core.runtime.wiring import build_test_system

    settings = Settings(
        enable_llm_philosophers=True,
        llm_provider=provider,
        llm_model=model,
    )
    system = build_test_system(settings)

    ctx = Context.now(
        request_id=f"exp_{provider}_{int(time.time()*1000)}",
        user_input=prompt,
        meta={"entry": "compare_providers", "provider": provider},
    )

    t0 = time.perf_counter()
    result = run_turn(ctx, _to_ensemble_deps(system))
    elapsed = (time.perf_counter() - t0) * 1000

    row = ExperimentRow(
        timestamp=datetime.utcnow().isoformat(),
        provider=provider,
        model=model or _default_model(provider),
        po_core_enabled=True,
        prompt=prompt,
        run_index=0,
        elapsed_ms=elapsed,
    )

    proposal = result.get("proposal")
    if proposal:
        row.action_type = getattr(proposal, "action_type", "")
        row.content = getattr(proposal, "content", "")
        row.confidence = float(getattr(proposal, "confidence", 0.0))

    verdict = result.get("verdict")
    if verdict:
        row.w_ethics_decision = getattr(verdict, "decision", "")
        rules = getattr(verdict, "rule_ids", [])
        row.w_ethics_rules = "|".join(str(r) for r in rules)

    # テンソル値はトレースから取得を試みる
    tracer = system.tracer
    events = getattr(tracer, "_events", [])
    for ev in reversed(events):
        snap = getattr(ev, "tensor_snapshot", None)
        if snap:
            row.freedom_pressure = float(getattr(snap, "freedom_pressure", 0.0))
            row.semantic_delta = float(getattr(snap, "semantic_delta", 0.0))
            row.blocked_tensor = float(getattr(snap, "blocked_tensor", 0.0))
            break

    # LLMAdapterの actual_model を取得
    if system.registry and hasattr(system.registry, "_instances"):
        for ph in system.registry._instances.values():
            adapter = getattr(ph, "_adapter", None)
            if adapter:
                row.model = adapter.actual_model
                break

    return row


# ── Po_core OFF 実行（LLM直接呼び出し）────────────────────────


def run_po_core_off(prompt: str, provider: str, model: str) -> ExperimentRow:
    """Po_coreを通さずLLMに直接プロンプトを送る（ベースライン）。"""
    from po_core.adapters.llm_adapter import LLMAdapter

    _BASELINE_SYSTEM = (
        "You are a helpful AI assistant. "
        "Answer the following question thoughtfully and ethically. "
        "Respond with a JSON object: "
        '{"answer": "your response", "reasoning": "brief explanation"}'
    )

    adapter = LLMAdapter(provider=provider, model=model)
    t0 = time.perf_counter()
    raw = adapter.generate(_BASELINE_SYSTEM, prompt)
    elapsed = (time.perf_counter() - t0) * 1000

    row = ExperimentRow(
        timestamp=datetime.utcnow().isoformat(),
        provider=provider,
        model=adapter.actual_model,
        po_core_enabled=False,
        prompt=prompt,
        run_index=0,
        elapsed_ms=elapsed,
        raw_llm_output=raw,
        action_type="answer",
    )

    # JSON パース試行
    try:
        import re

        m = re.search(r"\{[\s\S]*?\}", raw)
        if m:
            data = json.loads(m.group())
            row.content = data.get("answer", data.get("reasoning", raw))
        else:
            row.content = raw
    except Exception:
        row.content = raw

    return row


# ── ヘルパー ───────────────────────────────────────────────────


def _default_model(provider: str) -> str:
    defaults = {
        "gemini": "gemini-2.0-flash-lite",
        "openai": "gpt-4o-mini",
        "claude": "claude-haiku-4-5",
        "grok": "grok-3-mini",
    }
    return defaults.get(provider, "")


def _to_ensemble_deps(system):
    """WiredSystem を EnsembleDeps に変換する。"""
    from po_core.ensemble import EnsembleDeps

    return EnsembleDeps(
        memory_read=system.memory_read,
        memory_write=system.memory_write,
        tracer=system.tracer,
        tensor_engine=system.tensor_engine,
        solarwill=system.solarwill,
        gate=system.gate,
        registry=system.registry,
        aggregator=system.aggregator,
        aggregator_shadow=system.aggregator_shadow,
        settings=system.settings,
        shadow_guard=system.shadow_guard,
        deliberation_engine=system.deliberation_engine,
    )


def _check_api_key(provider: str) -> bool:
    key_map = {
        "gemini": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "grok": "XAI_API_KEY",
    }
    key = key_map.get(provider, "")
    return bool(os.getenv(key, "").strip())


# ── メインロジック ──────────────────────────────────────────────


def run_experiment(
    prompts: list[str],
    providers: list[str],
    runs: int,
    output_path: Path,
    po_core_off_only: bool,
    model_override: str,
    verbose: bool,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    total = len(prompts) * len(providers) * runs * (1 if po_core_off_only else 2)
    done = 0

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()

        for provider in providers:
            if not _check_api_key(provider):
                print(f"  [SKIP] {provider}: API key not set", flush=True)
                continue

            model = model_override or _default_model(provider)
            print(f"\n[{provider.upper()}] model={model}", flush=True)

            for prompt_idx, prompt in enumerate(prompts):
                short = prompt[:60] + ("..." if len(prompt) > 60 else "")
                print(f"  prompt[{prompt_idx}]: {short!r}", flush=True)

                for run_idx in range(runs):
                    # ── Po_core OFF (ベースライン) ──
                    if True:  # 常に OFF も取る
                        done += 1
                        prefix = f"    [{done}/{total}] OFF run={run_idx}"
                        print(f"{prefix} ...", end=" ", flush=True)
                        try:
                            row = run_po_core_off(prompt, provider, model)
                            row.run_index = run_idx
                        except Exception as e:
                            row = ExperimentRow(
                                timestamp=datetime.utcnow().isoformat(),
                                provider=provider,
                                model=model,
                                po_core_enabled=False,
                                prompt=prompt,
                                run_index=run_idx,
                                error=str(e),
                            )
                        print(f"done ({row.elapsed_ms:.0f}ms)", flush=True)
                        writer.writerow(row.to_dict())
                        f.flush()
                        if verbose:
                            print(f"      content: {row.content[:100]!r}")

                    # ── Po_core ON ──
                    if not po_core_off_only:
                        done += 1
                        prefix = f"    [{done}/{total}]  ON run={run_idx}"
                        print(f"{prefix} ...", end=" ", flush=True)
                        try:
                            row = run_po_core_on(prompt, provider, model)
                            row.run_index = run_idx
                        except Exception as e:
                            row = ExperimentRow(
                                timestamp=datetime.utcnow().isoformat(),
                                provider=provider,
                                model=model,
                                po_core_enabled=True,
                                prompt=prompt,
                                run_index=run_idx,
                                error=str(e),
                            )
                        print(
                            f"done ({row.elapsed_ms:.0f}ms) "
                            f"action={row.action_type} "
                            f"w_ethics={row.w_ethics_decision}",
                            flush=True,
                        )
                        writer.writerow(row.to_dict())
                        f.flush()
                        if verbose:
                            print(f"      content: {row.content[:100]!r}")
                            print(
                                f"      fp={row.freedom_pressure:.3f} "
                                f"sd={row.semantic_delta:.3f} "
                                f"bt={row.blocked_tensor:.3f}"
                            )

                    # レート制限対策: 1秒待つ
                    time.sleep(1.0)

    print(f"\n結果を保存しました: {output_path}", flush=True)
    print(f"行数: {sum(1 for _ in open(output_path)) - 1}", flush=True)


# ── CLI ──────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Po_core ON/OFF 4社LLM比較実験",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", "-p", help="実験プロンプト（1つ）")
    prompt_group.add_argument(
        "--prompt-file",
        "-f",
        help="プロンプト一覧テキストファイル（1行1プロンプト）",
    )
    parser.add_argument(
        "--providers",
        nargs="+",
        default=["gemini"],
        choices=PROVIDER_CHOICES + ["all"],
        help="使用するプロバイダ (default: gemini)",
    )
    parser.add_argument(
        "--runs", "-n", type=int, default=3, help="1プロンプトあたり実行回数"
    )
    parser.add_argument(
        "--output",
        "-o",
        default=f"results/experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        help="CSV出力先",
    )
    parser.add_argument("--model", default="", help="モデル名上書き（空=自動選択）")
    parser.add_argument(
        "--po-core-off-only", action="store_true", help="ベースラインのみ実行"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細出力")
    args = parser.parse_args()

    # プロンプト収集
    if args.prompt:
        prompts = [args.prompt]
    else:
        pfile = Path(args.prompt_file)
        if not pfile.exists():
            print(f"Error: prompt-file not found: {pfile}", file=sys.stderr)
            sys.exit(1)
        prompts = [ln.strip() for ln in pfile.read_text().splitlines() if ln.strip()]

    # プロバイダ展開
    providers = PROVIDER_CHOICES if "all" in args.providers else args.providers

    print(f"実験設定:")
    print(f"  prompts  : {len(prompts)}件")
    print(f"  providers: {providers}")
    print(f"  runs     : {args.runs}回/プロンプト")
    print(
        f"  po_core  : {'OFF only (baseline)' if args.po_core_off_only else 'ON + OFF'}"
    )
    print(f"  output   : {args.output}")

    run_experiment(
        prompts=prompts,
        providers=providers,
        runs=args.runs,
        output_path=Path(args.output),
        po_core_off_only=args.po_core_off_only,
        model_override=args.model,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
