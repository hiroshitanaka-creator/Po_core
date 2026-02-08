#!/usr/bin/env python3
"""
Po_core API Demo
================

Po_core APIの基本的な使い方を示すサンプルコード
"""

import json
from po_core import __version__, run
from po_core.po_self import PoSelf


def example_1_basic_usage():
    """例1: 基本的な使い方"""
    print("=" * 70)
    print("例1: Po_self 基本的な使い方")
    print("=" * 70)

    # Po_selfインスタンスを作成
    po = PoSelf()

    # 質問に対して推論を実行
    response = po.generate("人工知能は意識を持つことができるか？")

    # 結果を表示
    print(f"\n質問: {response.prompt}")
    print(f"コンセンサスリーダー: {response.consensus_leader}")
    print(f"参加哲学者: {', '.join(response.philosophers)}")
    print(f"\n回答:\n{response.text[:300]}...")
    print(f"\nメトリクス:")
    print(f"  - Freedom Pressure: {response.metrics['freedom_pressure']}")
    print(f"  - Semantic Delta: {response.metrics['semantic_delta']}")
    print(f"  - Blocked Tensor: {response.metrics['blocked_tensor']}")
    print()


def example_2_custom_philosophers():
    """例2: カスタム哲学者の選択"""
    print("=" * 70)
    print("例2: カスタム哲学者の選択")
    print("=" * 70)

    # 特定の哲学者を選択
    philosophers = ["sartre", "heidegger", "derrida"]
    po = PoSelf(philosophers=philosophers)

    response = po.generate("実存とは何か？")

    print(f"\n質問: {response.prompt}")
    print(f"選択した哲学者: {', '.join(philosophers)}")
    print(f"コンセンサスリーダー: {response.consensus_leader}")
    print(f"\n回答:\n{response.text[:300]}...")
    print()


def example_3_json_output():
    """例3: JSON形式での出力"""
    print("=" * 70)
    print("例3: JSON形式での出力")
    print("=" * 70)

    po = PoSelf()
    response = po.generate("倫理的な決定をどのように下すべきか？")

    # JSON形式に変換
    response_dict = response.to_dict()

    print("\nJSON出力:")
    print(json.dumps(response_dict, indent=2, ensure_ascii=False))
    print()


def example_4_run_api():
    """例4: po_core.run() を使用"""
    print("=" * 70)
    print("例4: po_core.run() APIを使用")
    print("=" * 70)

    # run() を直接呼び出し
    result = run(user_input="美とは何か？")

    print(f"\nステータス: {result['status']}")
    print(f"リクエストID: {result['request_id']}")

    if "proposal" in result:
        proposal = result["proposal"]
        print(f"\n提案:")
        print(f"  内容: {str(proposal)[:200]}...")

    print()


def example_5_response_details():
    """例5: 詳細な応答情報"""
    print("=" * 70)
    print("例5: 各哲学者の詳細な応答")
    print("=" * 70)

    po = PoSelf(philosophers=["aristotle", "confucius", "dewey"])
    response = po.generate("教育の目的は何か？")

    print(f"\n質問: {response.prompt}\n")

    # 各哲学者の応答を表示
    for i, resp in enumerate(response.responses, 1):
        print(f"{i}. {resp['name']}")
        print(f"   視点: {resp['perspective']}")
        print(f"   推論: {resp['reasoning'][:150]}...")
        print(f"   Freedom Pressure: {resp['freedom_pressure']}")
        print(f"   Semantic Delta: {resp['semantic_delta']}")
        print(f"   Blocked Tensor: {resp['blocked_tensor']}")
        print()


def example_6_trace_disabled():
    """例6: トレース無効化"""
    print("=" * 70)
    print("例6: Po_trace無効化（軽量モード）")
    print("=" * 70)

    # トレースを無効にして軽量化
    po = PoSelf(enable_trace=False)
    response = po.generate("知識とは何か？")

    print(f"\n質問: {response.prompt}")
    print(f"トレース有効: False（軽量モード）")
    print(f"回答: {response.text[:200]}...")
    print()


def example_7_multiple_prompts():
    """例7: 複数の質問を処理"""
    print("=" * 70)
    print("例7: 複数の質問を連続処理")
    print("=" * 70)

    prompts = [
        "愛とは何か？",
        "正義とは何か？",
        "幸福とは何か？"
    ]

    po = PoSelf()

    results = []
    for prompt in prompts:
        response = po.generate(prompt)
        results.append({
            "prompt": prompt,
            "leader": response.consensus_leader,
            "fp": response.metrics['freedom_pressure']
        })

    print("\n処理結果サマリー:")
    print(f"{'質問':<20} {'リーダー':<30} {'FP':>6}")
    print("-" * 60)
    for r in results:
        print(f"{r['prompt']:<20} {r['leader']:<30} {r['fp']:>6.2f}")
    print()


def main():
    """すべての例を実行"""
    print("\n" + "=" * 70)
    print("🐷🎈 Po_core API Demo")
    print(f"Version: {__version__}")
    print("=" * 70 + "\n")

    try:
        example_1_basic_usage()
        print("\n")

        example_2_custom_philosophers()
        print("\n")

        example_3_json_output()
        print("\n")

        example_4_run_api()
        print("\n")

        example_5_response_details()
        print("\n")

        example_6_trace_disabled()
        print("\n")

        example_7_multiple_prompts()
        print("\n")

        print("=" * 70)
        print("すべてのデモを完了しました！")
        print("=" * 70)

    except Exception as e:
        print(f"\nエラー: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
