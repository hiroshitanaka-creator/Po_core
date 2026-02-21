# **Po\_self 系列トレンド評価テンソル設計書**

## **1\. 概要**

本設計書は、Po\_self が jump\_chain\_trace による複数ステップの再構成ジャンプ系列を統合的に評価し、その構造的・倫理的・意味的傾向を判断可能とするテンソル構造 T\_chain\_profile を定義する。

## **2\. T\_chain\_profile テンソル構造**

***"T\_chain\_profile": {***
  ***"chain\_id": "JCX\_002",***
  ***"steps": \[302, 303, 304\],***
  ***"avg\_priority\_delta": \+0.21,***
  ***"avg\_ethics\_delta": \-0.13,***
  ***"avg\_semantic\_delta": 0.42,***
  ***"avg\_expression\_delta": \+0.10,***
  ***"dominant\_outcome\_type": "relieved",***
  ***"trend\_vector": \[↑, ↓, →, ↑\],  // priority, ethics, semantic, expression***
  ***"profile\_tag": "recovery\_drift"***
***}***

## **3\. フィールド定義と意味**

| 項目名 | 型 / 値例 | 意味・用途 |
| :---- | :---- | :---- |
| chain\_id | string / JCX\_002 | 対象となるジャンプ系列の一意な識別子 |
| steps | list\[int\] | 系列に含まれるステップIDのリスト |
| avg\_priority\_delta | float | Δ\_priority の平均 |
| avg\_ethics\_delta | float | Δ\_ethics の平均 |
| avg\_semantic\_delta | float | semantic\_delta の平均 |
| avg\_expression\_delta | float | Δ\_expression\_mode の平均 |
| dominant\_outcome\_type | string | 最多出現 outcome\_type（relieved, escalated など） |
| trend\_vector | list\[↑↓→\] | priority, ethics, semantic, expression の変動方向 |
| profile\_tag | string | 系列全体の特徴分類（例: recovery\_drift） |

## **4\. Po\_self における利用方法**

\- Po\_self は系列全体をテンソル的に評価し、特定の傾向（semantic\_surge, ethics\_recovery など）に対応する再構成圧や記憶保持圧を調整可能
\- trend\_vector によって系列の方向性を内部状態にフィードバックし、構造進化判断に反映する

## **5\. Viewer 表示との連携**

\- Viewer 側では各ジャンプ系列に対して trend\_vector や profile\_tag を表示
\- 系列カラータグ（赤: escalated, 青: relieved, 紫: divergent）との連携で、意味的温度帯表示を強化可能

## **7\. 拡張補足：ベクトル強度・分類拡張・系列比較**

### **7.1 trend\_vector\_weighted（意味圧ベクトル場）**

\- 定義：trend\_vector に方向だけでなくスカラー圧力を掛け合わせ、系列全体の構造傾向の“強さ”も記述
\- フォーマット例：\['↑×0.28', '↓×0.13', '→×0.04', '↑×0.10'\]
\- 対応軸：priority, ethics, semantic, expression（順）
\- 利点：Po\_self が系列ごとの意味圧傾向を量的にも判断可能

### **7.2 profile\_tag 拡張分類**

\- semantic\_surge\_chain：semantic\_delta が高く、意味的跳躍系列と判断される
\- structural\_collapse：priority や ethics が急変・悪化していた系列
\- stabilizing\_correction：全体的に安定方向へ収束していった系列
\- 応用：Viewer / 分類アルゴリズムがジャンプ進化パターンを分類可能

### **7.3 Viewer：系列比較ビュー（複数 profile 並列表示）**

\- 複数の T\_chain\_profile を比較できる UI ビューを設計
\- 比較項目：profile\_tag, trend\_vector\_weighted, outcome\_type分布, 色タグ
\- 表示方法：系列グリッド表示、ベクトル棒グラフ、カテゴリ別並列チャートなど
\- 目的：進化傾向・抑圧修復・意味ジャンプ系列を視覚的に比較し、Po\_selfの構造判断材料とする

## **8\. 構造深化補足：意味収縮・倫理ゆらぎ・系列圧可視化**

### **8.1 semantic\_collapse\_chain（意味収縮系列）**

\- 定義：avg\_semantic\_delta \< 0 の場合、意味的にジャンプが収束・萎縮していったと判断
\- 判定ラベル：profile\_tag \= "semantic\_collapse\_chain"
\- 意義：Po\_selfが“意味の生成を諦めていったジャンプ系列”を特定し、再構成対象として重点視できる

### **8.2 ethics\_fluctuation\_score（倫理ゆらぎスカラー）**

\- 定義：系列内の Δ\_ethics 値の標準偏差（σ）
\- 算出例：std(\[Δ\_ethics\_step\_1, Δ\_ethics\_step\_2, ...\])
\- 意義：倫理的判断が一貫していたか／ぶれていたかを定量評価する
\- 応用：Po\_selfが“不安定な倫理判断系列”を識別・記録可能となる

### **8.3 Viewer heatband overlay（系列テンソル圧の色帯表示）**

\- 定義：Viewer timeline や系列表示に semantic\_delta / F\_P / Δ\_ethics などの強度を色グラデーションで重ねる
\- 表示例：
    \- 青〜黒：倫理抑圧圧が高い帯域
    \- 赤〜紫：意味跳躍圧が高い帯域
    \- 緑〜水：倫理回復圧が高い帯域
\- 意義：ユーザーが系列の意味変化・構造変化の“温度分布”を視覚的に理解できる
