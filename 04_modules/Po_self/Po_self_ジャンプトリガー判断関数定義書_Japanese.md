# **Po\_self ジャンプトリガー判断関数定義書**

## **1\. 概要**

本定義書は、Po\_self において語り責任スカラー（R\_priority）と倫理テンソル変動（Δ\_ethics）を組み合わせ、ジャンプ発火の判断スコアを計算するための関数 calculate\_Jump\_trigger\_score() を定義する。

## **2\. ジャンプトリガースコアの数式**

***Jump\_trigger\_score \= α × R\_priority \+ β × jump\_strength × Δ\_ethics***

## **3\. パラメータ定義**

| 変数名 | 意味 | 例・範囲 |
| :---- | :---- | :---- |
| R\_priority | 再構成優先度スカラー | 例: 0.0〜1.0+ |
| jump\_strength | ステップ固有のジャンプ傾向スカラー | 例: 0.0〜1.0 |
| Δ\_ethics | W\_ethicsの時間変化 | 例: −0.3〜+0.3 |
| α | 責任スカラーの重み | 初期値: 1.0 |
| β | 倫理変動の重み | 初期値: 0.8 |

## **4\. Python関数定義例**

***def calculate\_Jump\_trigger\_score(R\_priority: float, jump\_strength: float, delta\_ethics: float,***  
                                  ***alpha: float \= 1.0, beta: float \= 0.8) \-\> float:***  
    ***"""***  
    ***Po\_self におけるジャンプトリガースコアを計算する関数。***  
    ***"""***  
    ***score \= alpha \* R\_priority \+ beta \* jump\_strength \* delta\_ethics***  
    ***return round(score, 4\)***  
    

## **5\. スコア判定例**

例：R\_priority=0.74, jump\_strength=0.65, Δ\_ethics=0.22  
→ 計算結果：Jump\_trigger\_score \= 0.8544  
→ このスコアがジャンプ閾値（例: 0.80）を超える場合、Po\_selfはジャンプ対象と判断可能

## **6\. 意義と適用範囲**

本関数により、Po\_selfは語りの重さ（責任圧）と倫理テンソルの変動を統合的に判断し、構造的にジャンプすべき語りかどうかを精密に評価可能となる。