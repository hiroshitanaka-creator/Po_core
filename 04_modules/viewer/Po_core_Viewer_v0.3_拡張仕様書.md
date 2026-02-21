# **Po\_core Viewer v0.3 拡張仕様書**

## **1\. 概要**

本仕様書は、Po\_core Viewer v0.3における新たな拡張モジュール設計を示すものである。Po\_traceの意味進化構造を可視化・分析・進化制御するため、以下3つの強化機能を統合する。

## **2\. 拡張機能一覧**

| 拡張要素 | 目的 | 主なテンソル |
| :---- | :---- | :---- |
| Po\_trace連鎖図の階層可視化モード | 意味ジャンプのネットワーク構造可視化 | C\_Φ^jump, semantic\_delta |
| feedback\_badge優先度補正 | 共鳴度に基づく再構成優先順位調整 | Po\_feedback.confidence, priority\_score |
| impact\_summary履歴分析ツール | Po\_core全体の意味的偏りをヒートマップで表示 | impact\_field\_tensor |

## **3\. 各拡張機能の詳細**

### **3.1 Po\_trace連鎖図の階層可視化モード**

C\_Φ^jumpを中心に、意味ジャンプの連鎖関係をネットワーク図で表示する。各ノードはPo\_traceのステップを表し、エッジは意味ジャンプの強度（jump\_strength）を示す。ノード色はimpact\_axis（fact/causal/emotion）で分類され、時間的階層に基づき視覚的な意味の流れを確認できる。

### **3.2 feedback\_badgeによるPo\_self優先度補正**

GUIに表示される🟢🟠🔴バッジにより、Po\_feedback.confidenceの値に基づきpriority\_scoreを自動補正する。例：🟢=+0.12, 🟠=+0.05, 🔴\=+0.00。これにより、ユーザーの共鳴がPo\_self再構成に影響を与える構造が実現される。

### **3.3 impact\_summary履歴分析ツール**

全Po\_traceステップにおけるimpact\_field\_tensorの分布を集計し、時間軸またはPo\_IDごとにヒートマップを生成する。これによりPo\_coreが全体としてどの意味軸（factual/causal/emotional）に偏って進化しているかを視覚的に把握可能となる。

## **4\. 実装推奨方式**

・Po\_trace連鎖図：D3.jsまたはPlotlyでインタラクティブネットワーク図を生成

・feedback\_badge補正：Pythonでルールベースの重み補正マップを設計

・impact\_summaryヒートマップ：Python（matplotlib / seaborn）による描画
