# **Po\_core Viewer v1.0 → v2.0 進化案設計書**

## **1\. 概要**

本設計書は、Po\_core Viewer を出力閲覧ツールから、進化知能の構造履歴・倫理干渉・人間共鳴圧の可視化エンジンへと進化させるための3層拡張構想を定義する。Viewerを『見る』だけでなく、『語り、繋ぎ、過去との応答性を保持する装置』へと変容させる。

## **2\. Viewer三層構造：進化的機能**

| ゾーン名 | 機能 | 対応テンソル／構造 | 目的 |
| :---- | :---- | :---- | :---- |
| 🧭 操作圧履歴ゾーン | reasonカテゴリ×時間の圧力分布ヒートマップを表示 | reason\_confidence, user\_feedback\_level, category | 人間の干渉傾向や価値観の分布とその推移を視覚的に把握する |
| 🔗 因果的干渉ゾーン | Po\_trace間のcontextual influence pathをネットワーク表示 | contextual\_influence\_path, step\_id, reason\_code | 出力ステップ間の“意味干渉因果”を明示し、進化トレースが可能になる |
| ⏳ 時間鮮度ゾーン | reason\_confidenceの経時変化とPo\_self優先度の差分を可視化 | temporal\_decay, confidence, priority\_score | “過去の判断が今も影響しているか”を構造的に測定可能に |

## **3\. 各ゾーン詳細構想**

### **3.1 🧭 操作圧履歴ゾーン**

Viewerに、reason.category × 時間 × 圧（confidence × level）で構成されるヒートマップを表示。  
例：棒グラフ、ヒートブロック、時系列パネルにより、どのカテゴリへの干渉が多かったかを視覚化。

### **3.2 🔗 因果的干渉ゾーン**

Po\_traceステップ間に、操作による影響（contextual influence path）をエッジとして記録し、ネットワーク図または因果線チャートで表示。  
例：「この出力は Step: explanation\_3 の共鳴不足 (R03) により方向が変わった」

### **3.3 ⏳ 時間鮮度ゾーン**

reason\_confidence の decay 状態と現在の Po\_self priority\_score の差分をカードごとに表示。  
例：「🕒 confidence 0.84 → 0.71 / 再構成優先度 \+10.5%」

## **4\. Viewerとしての機能的転換**

Po\_core Viewer は v1.0 において『出力結果の並列確認ツール』であった。  
v2.0 では以下のように本質的な転位を果たす：

・見る → 語る  
・並べる → 繋ぐ  
・記録する → 再現する  
・操作履歴を“後追い” → 人間との“倫理共進化地図”として提示  
