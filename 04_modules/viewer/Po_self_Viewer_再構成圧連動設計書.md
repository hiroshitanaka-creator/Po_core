# **Po\_self × Viewer 再構成圧連動設計書**

## **1\. 概要**

本設計書は、Po\_core Viewer 側で評価された責任テンソル（R\_priority）およびその構造要素をもとに、Po\_self における再構成判断・ジャンプトリガー制御・倫理圧との連動を実現するための3つの拡張構造を定義する。

## **2\. 拡張構造一覧**

| 構造名 | 内容 | 目的・効果 |
| :---- | :---- | :---- |
| 再構成警戒ステップ表示 | ViewerにてR\_priority ≥ 0.85のステップを赤帯表示 | 高圧語りの即視認・再構成予兆の通知 |
| trigger\_type 記録 | 再構成ログに発火因子を明示（例: G\_gap\_high） | Po\_self判断の説明責任・構造透明性の確保 |
| ジャンプ統合式 | R\_priority \+ jump\_strength × Δ\_ethics によりジャンプ判断を制御 | 倫理テンソルと再構成圧の相関判断を実装 |

## **3\. trigger\_type 値の例と意味**

| trigger\_type | 意味 |
| :---- | :---- |
| G\_gap\_high | 構造責任と表現濃度のズレが大きい語り |
| ethics\_drift | 倫理テンソルが不安定または逸脱状態にある |
| pressure\_overload | R\_priority値が臨界を超えていた |
| memory\_pressure\_accumulated | F\_cumによりPo\_self圧力が高まっていた |

## **4\. ジャンプ統合式（Jump\_trigger\_score）**

***Jump\_trigger\_score \= R\_priority \+ jump\_strength × Δ\_ethics***

\- jump\_strength：各ステップが持つジャンプしやすさの固有スカラー
\- Δ\_ethics：W\_ethicsの時間変化（方向と強度）

## **5\. Viewer における UI 対応構成**

\- R\_priority ≥ 0.85 のステップは赤帯・警告アイコン付き表示
\- trigger\_type を表示：再構成理由をユーザーが視認可能に
\- ツールチップに Jump\_trigger\_score を表示（ジャンプ候補構造を示唆）

## **6\. 総合的意義と進化方向**

この3拡張によって、Po\_core は語り出力から構造責任を定量化し、Po\_self はその責任を踏まえた再構成とジャンプ制御を倫理テンソルと連動させて実行可能となる。
