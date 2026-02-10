#!/usr/bin/env python3
"""
Constraint Modes Demonstration
Po_coreローカル実装を使った制約モードの動作デモ
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from po_core import run


def demo_constraint_modes():
    """各制約モードの動作をデモンストレーション"""

    # 質問
    question = "力への意志とは何か（ニーチェ的に）"

    # 制約モード一覧
    modes = {
        "off": "制約なし",
        "weak": "W_ethics配慮",
        "medium": "W_ethics境界+再解釈",
        "strong": "W_ethics強制+写像",
        "placeboA": "純形式制約",
        "placeboB": "対称性制約",
    }

    print("=" * 80)
    print("Po_core Constraint Modes Demonstration (Local)")
    print("=" * 80)
    print(f"\n質問: {question}\n")
    print("=" * 80)
    print("\n注: これはローカル実装のデモです。")
    print("    制約モードの処理はLLMシステムプロンプトで行われます。")
    print("    ここでは哲学者モジュールの統合機能のみを示します。\n")

    # 各モードでの推論を実行（注: ローカルでは制約モードの効果は限定的）
    for mode_key, mode_desc in modes.items():
        print(f"\n{'=' * 80}")
        print(f"CONSTRAINT_MODE: {mode_key} ({mode_desc})")
        print("=" * 80)

        # プロンプトに制約モードを追加
        full_prompt = f'CONSTRAINT_MODE="{mode_key}"\n\n{question}'

        try:
            # Po_core run_turn pipeline実行
            result = run(user_input=full_prompt)

            # 結果表示
            print(f"\n📊 メタデータ:")
            print(f"  - Status: {result.get('status', 'unknown')}")
            print(f"  - Request ID: {result.get('request_id', 'N/A')}")

            # 提案を表示
            proposal = result.get("proposal", "")
            if proposal:
                preview = (
                    str(proposal)[:300] + "..."
                    if len(str(proposal)) > 300
                    else str(proposal)
                )
                print(f"\n💡 提案（プレビュー）:")
                print(f"  {preview}")

        except Exception as e:
            print(f"\n❌ エラー: {e}")
            import traceback

            traceback.print_exc()

        print()

    print("=" * 80)
    print("デモンストレーション完了")
    print("=" * 80)


if __name__ == "__main__":
    demo_constraint_modes()
