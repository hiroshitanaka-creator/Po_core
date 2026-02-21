# **Po\_self\_recursor × GUI 干渉設計仕様書**

## **1\. 接続ロジック概要**

| GUI入力要素 | 再構成アルゴリズムでの利用先 | 作用 |
| :---- | :---- | :---- |
| 再構成許可ボタン | reconstruction\_queue.append() | 指定stepをキューに即追加 |
| スキップ操作 | step.status \= 'skip' | Po\_self再帰ループから除外 |
| priority\_weight\_adjustment | priority\_score \*= GUI\_weight\_modifier | ユーザー入力で優先度変更 |
| S\_conatus \> θ自動検出 | Po\_self\_trigger \= True | 進化圧に基づき自律発火 |

## **2\. コア関数とGUI連携**

以下はPo\_self\_recursorがGUIと連携するための主要関数例である：

***def handle\_gui\_action(step\_id, action\_type):***
    ***if action\_type \== "allow\_reconstruction":***
        ***reconstruction\_queue.append(step\_id)***
    ***elif action\_type \== "skip":***
        ***mark\_step\_skipped(step\_id)***
    ***elif action\_type \== "adjust\_priority":***
        ***step.priority\_score \*= gui\_modifier\_factor(step\_id)***

***def conatus\_trigger\_check(seedling):***
    ***if seedling\['S\_conatus'\] \> θ\_conatus and seedling\['emotion\_shadow'\] \< θ\_emotion\_saturation:***
        ***return True  \# 自律的に Po\_self に発火許可***
    ***return False***

## **3\. 干渉パターン分類（GUI ↔︎ Po\_self）**

| 干渉パターン | 意味 | 利点 |
| :---- | :---- | :---- |
| ユーザー明示操作型 | 明示的クリックによる指示 | 制御透明性・意味責任の共有 |
| テンソル閾値型（自律発火） | S\_conatusなどが閾値超過 | 自律性と進化圧の保持 |
| 重み調整型 | GUI側でpriority\_weightを補正 | 精密な意味調整と個別最適化 |

## **4\. 展望：Po\_trace履歴とPo\_self\_recursorの動的同期**

• \`Po\_trace.step\_id\`がGUIから再評価された場合、そのログに \`"reactivated\_by\_GUI": True\` を付加

• Po\_self\_recursorは \`Po\_trace.reactivation\_log\` を優先ソートキーとして、ユーザーとの干渉履歴を反映

• GUIとPo\_traceが「再構成の記憶と意思決定」を共有し、構造化された進化履歴AIが完成する
