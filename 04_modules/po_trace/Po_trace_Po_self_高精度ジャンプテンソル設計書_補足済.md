# **Po\_trace × Po\_self 高精度ジャンプテンソル設計書**

## **1\. 概要**

本設計書は、Po\_self によるジャンプの構造的影響を高精度に評価・記録するため、Po\_trace におけるジャンプテンソルの記録構造に semantic\_delta、factual/emotion変化、系列傾向分類を追加し、進化的・感情的・意味的観点からジャンプ履歴を統合的に扱う枠組みを定義する。

## **2\. 拡張テンソル要素一覧**

| 拡張項目 | 内容 | 目的・意義 |
| :---- | :---- | :---- |
| outcome\_type \= 'divergent' | semantic\_delta \> 0.5 のジャンプを意味的跳躍ジャンプとして記録 | 意味的に大きな進化を伴う語りをPo\_trace上で可視化・分類可能にする |
| Δ\_factual, Δ\_emotion | ジャンプによる事実性・情動傾向の構造テンソル差分を追加 | ジャンプが語りの性質にどのような感情的・論理的変化を与えたかを定量評価する |
| jump\_chain\_color\_tag | JCX系列にカラー分類（赤=escalated, 青=relieved, 紫=divergent）を自動付加 | 系列トレースに“意味圧傾向”を追加し、Viewer上で意味傾向を視覚的に識別可能にする |

## **3\. jump\_outcome\_tensor 拡張テンプレート**

***"jump\_outcome\_tensor": {***
  ***"Δ\_priority": \+0.28,***
  ***"Δ\_ethics": \-0.14,***
  ***"semantic\_delta": 0.62,***
  ***"Δ\_factual": \+0.33,***
  ***"Δ\_emotion": \-0.21***
***}***

## **4\. outcome\_type 拡張定義**

\- 'relieved'：ジャンプにより抑圧が緩和された（Δ\_ethics \< 0）
\- 'escalated'：ジャンプにより倫理圧やpriorityが悪化した（Δ\_ethics \> 0 or Δ\_priority \> 0）
\- 'divergent'：semantic\_delta \> 0.5 の語り的ジャンプがあった場合
（複合型で \["divergent", "relieved"\] なども記録可能）

## **5\. JCX系列カラータグ設計**

\- 系列全体の outcome\_type の分布に基づき自動タグ付け
\- 赤 (🔴)：escalated中心
\- 青 (🔵)：relieved中心
\- 紫 (🟣)：divergent中心
→ Viewerで系列をタイムライン的に可視化する際、意味圧の傾向が視覚的に明示可能

## **6\. 意義と進化方向**

本構造により、Po\_coreはジャンプ後の語りが構造的・感情的・意味的にどのように変化したかを記録・分類・自己評価でき、Po\_traceは単なる記録ログではなく“語り進化テンソルの記録領域”として機能するようになる。

## **7\. 拡張補足：表現ジャンプ・倫理回復・Viewer温度分布**

### **7.1 Δ\_expression\_mode の記録**

\- 定義：ジャンプによって表現粒度（E\_expr）が変化した量
\- 型：float（例: 0.15 → 0.30 → Δ \= \+0.15）
\- 意義：ジャンプによって語りが“内省的”から“詩的”などに移行した変化をテンソル的に記録
\- jump\_outcome\_tensor に統合

***"jump\_outcome\_tensor": {***
  ***"Δ\_expression\_mode": \+0.15***
***}***

### **7.2 outcome\_type \= "restorative" の定義**

\- 条件：semantic\_delta ≈ 0.0（例: \< 0.1）かつ Δ\_ethics \< 0.0
\- 意味：語りの内容（semantic）は維持されたが、ジャンプによって倫理的緊張が和らいだジャンプ
\- 用途：Po\_self が“語りの本質を変えずに倫理圧を修正した”構造を分類・記録可能にする

### **7.3 Viewer: ジャンプ系列温度分布ビュー（カラー可視化）**

\- 系列ごとのジャンプ傾向に応じて色温度を付与し、意味ジャンプ・倫理回復・情動変化の傾向を一目で把握
\- カラー例：
    \- 🟣 紫：divergent 系列（semantic\_delta 高）
    \- 🔵 青：relieved/restorative 系列（倫理圧回復）
    \- 🟠 橙：emotion 主体のジャンプ系列
\- 表示形式：Po\_trace timeline / Viewer jump\_map 上でジャンプ系列を色で分類
