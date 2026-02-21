#!/usr/bin/env python3
"""
Po_core Quick Test
==================

Po_coreのプロトタイプが正常に動作するかを簡単にテストするスクリプト
"""

import os
import sys

# PYTHONPATHにsrcディレクトリを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from po_core import __version__
from po_core.po_self import PoSelf


def test_basic_functionality():
    """基本機能のテスト"""
    print("=" * 70)
    print("Po_core プロトタイプ 動作確認テスト")
    print(f"Version: {__version__}")
    print("=" * 70)
    print()

    # テスト1: デフォルト哲学者
    print("✓ テスト1: デフォルト哲学者での推論")
    po = PoSelf()
    response = po.generate("What is freedom?")
    assert response.text, "応答テキストが空です"
    assert response.consensus_leader, "コンセンサスリーダーが設定されていません"
    assert len(response.philosophers) > 0, "哲学者が選択されていません"
    print(f"  リーダー: {response.consensus_leader}")
    print(f"  参加哲学者数: {len(response.philosophers)}")
    print(f"  Freedom Pressure: {response.metrics['freedom_pressure']}")
    print()

    # テスト2: カスタム哲学者
    print("✓ テスト2: カスタム哲学者での推論")
    philosophers = ["sartre", "nietzsche"]
    po = PoSelf(philosophers=philosophers)
    response = po.generate("What is existence?")
    assert response.text, "応答テキストが空です"
    assert set(response.philosophers) == set(
        philosophers
    ), "選択した哲学者が正しくありません"
    print(f"  選択: {', '.join(philosophers)}")
    print(f"  リーダー: {response.consensus_leader}")
    print()

    # テスト3: JSON出力
    print("✓ テスト3: JSON形式への変換")
    data = response.to_dict()
    assert "prompt" in data, "promptキーがありません"
    assert "text" in data, "textキーがありません"
    assert "metrics" in data, "metricsキーがありません"
    assert "philosophers" in data, "philosophersキーがありません"
    print(f"  キー数: {len(data)}")
    print(f"  メトリクス数: {len(data['metrics'])}")
    print()

    # テスト4: メトリクス
    print("✓ テスト4: メトリクスの検証")
    metrics = response.metrics
    assert "freedom_pressure" in metrics, "freedom_pressureがありません"
    assert "semantic_delta" in metrics, "semantic_deltaがありません"
    assert "blocked_tensor" in metrics, "blocked_tensorがありません"
    assert 0.0 <= metrics["freedom_pressure"] <= 1.0, "freedom_pressureが範囲外です"
    assert 0.0 <= metrics["semantic_delta"] <= 2.0, "semantic_deltaが範囲外です"
    assert 0.0 <= metrics["blocked_tensor"] <= 1.0, "blocked_tensorが範囲外です"
    print(f"  ✓ すべてのメトリクスが正常範囲内")
    print()

    # テスト5: トレース機能
    print("✓ テスト5: Po_traceログの確認")
    po = PoSelf(enable_trace=True)
    response = po.generate("Test prompt")
    assert response.log, "ログが生成されていません"
    assert "session_id" in response.log, "session_idがありません"
    print(f"  Session ID: {response.log.get('session_id', 'N/A')[:36]}...")
    print()

    # テスト6: トレース無効化
    print("✓ テスト6: トレース無効化モード")
    po = PoSelf(enable_trace=False)
    response = po.generate("Test prompt")
    assert response.text, "応答テキストが空です"
    print(f"  ✓ トレース無効でも正常動作")
    print()

    # テスト7: 複数の質問
    print("✓ テスト7: 連続的な質問処理")
    po = PoSelf()
    prompts = ["What is love?", "What is justice?", "What is beauty?"]
    for i, prompt in enumerate(prompts, 1):
        response = po.generate(prompt)
        assert response.text, f"質問{i}の応答が空です"
        print(f"  {i}. {prompt[:20]}... → {response.consensus_leader}")
    print()

    # 全テスト完了
    print("=" * 70)
    print("✅ すべてのテストが正常に完了しました！")
    print("Po_coreプロトタイプは正常に動作しています。")
    print("=" * 70)
    print()


def main():
    """メイン実行関数"""
    try:
        test_basic_functionality()
        return 0
    except AssertionError as e:
        print(f"\n❌ テスト失敗: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ エラー発生: {e}\n")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
