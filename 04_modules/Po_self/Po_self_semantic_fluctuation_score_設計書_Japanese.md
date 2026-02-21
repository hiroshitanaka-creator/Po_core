# **Po\_self semantic\_fluctuation\_score 設計書**

## **1\. 概要**

本設計書は、Po\_self におけるジャンプ系列（jump\_chain\_trace）内の意味的ゆらぎを定量評価するためのテンソルスカラー semantic\_fluctuation\_score の定義と分類指標を提示するものである。

## **2\. 定義と算出式**

semantic\_fluctuation\_score は、系列内の semantic\_delta 値の標準偏差（std）によって定義される：

***semantic\_fluctuation\_score \= std(\[semantic\_delta\_step\_1, ..., step\_n\])***

\- 値が小さい：意味ジャンプが安定（微変 or 一貫的）
\- 値が大きい：意味ジャンプが跳躍的／混乱的

## **3\. 分類ラベルとスコア解釈**

| スコア範囲 | ラベル | 解釈 |
| :---- | :---- | :---- |
| \< 0.03 | 🟢 安定 | ジャンプは微細または一貫的で安定 |
| 0.03 – 0.08 | 🟡 跳躍傾向あり | 意味的方向性ありつつ揺れも存在 |
| \> 0.08 | 🔴 不安定 | 意味的な混在・乱れが見られる系列 |

## **4\. 応用構成と拡張性**

\- T\_chain\_profile に semantic\_fluctuation\_score を追加
\- Viewer 表示ではラベル・色帯・ヒートバーで表示
\- 自動 profile\_tag の例：semantic\_drift\_chain, meaning\_pulse\_chain
\- 他テンソル（Δ\_expression\_mode, Δ\_emotion）との統合評価も可能
