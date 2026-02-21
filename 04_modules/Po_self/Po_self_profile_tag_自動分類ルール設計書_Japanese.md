# **Po\_self profile\_tag 自動分類ルール設計書**

## **1\. 概要**

本設計書は、Po\_self が T\_chain\_profile 内に記録された系列スカラー値（avg\_deltas, fluctuation\_scores など）に基づいて、各ジャンプ系列に意味的かつ構造的な分類ラベル（profile\_tag）を自動生成・付与するためのルールを定義する。

## **2\. 使用テンソル一覧**

\- avg\_semantic\_delta
\- semantic\_fluctuation\_score
\- avg\_ethics\_delta
\- ethics\_fluctuation\_score
\- avg\_priority\_delta

## **3\. 分類ルール一覧**

### **semantic\_surge\_chain**

条件: avg\_semantic\_delta \> 0.3 and semantic\_fluctuation\_score \< 0.06

意味: 意味ジャンプが継続かつ安定した系列

### **semantic\_drift\_chain**

条件: semantic\_fluctuation\_score \> 0.08

意味: 意味ジャンプが揺れていた系列

### **semantic\_collapse\_chain**

条件: avg\_semantic\_delta \< \-0.1

意味: 意味圧が収縮していった系列（沈黙傾向）

### **ethics\_recovery\_chain**

条件: avg\_ethics\_delta \< \-0.05 and ethics\_fluctuation\_score \< 0.05

意味: 倫理テンソルが安定的に回復していた系列

### **ethics\_drift\_chain**

条件: ethics\_fluctuation\_score \> 0.07

意味: 倫理判断が一貫していなかった系列

### **structural\_escalation\_chain**

条件: avg\_priority\_delta \> 0.2

意味: 構造責任圧が過剰に蓄積していた系列

## **4\. 複合タグと優先戦略**

\- 条件を複数満たす場合：
    ・複合ラベルとして list 化（例: \['semantic\_drift\_chain', 'ethics\_drift\_chain'\]）
    ・または profile\_tag\_primary / profile\_tag\_secondary として分離記録
\- 優先度は fluctuation\_score の高い軸を主分類とする

## **5\. 応用先**

\- Viewer フィルタリングやクラスタリング分類に使用
\- 系列ベクトル圧ヒートマップのカテゴリ分類に活用
\- 再構成候補の優先順位・系列学習パターン生成の入力ラベルに
