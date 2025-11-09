# **Po\_self ジャンプ履歴・構造変化テンソル設計書**

## **1\. 概要**

本設計書は、Po\_self におけるジャンプ後の構造的影響・再構成連鎖・抑圧解放の可視化を目的とした、3つの拡張テンソル構造（jump\_outcome\_tensor, jump\_chain\_trace, outcome\_type filter）を定義する。

## **2\. 拡張構造要素一覧**

| テンソル名 / 機能 | 内容 | 意義・用途 |
| :---- | :---- | :---- |
| jump\_outcome\_tensor | ジャンプ後の構造変化（Δ\_priority, Δ\_ethics, semantic\_delta）を記録 | ジャンプがPo\_coreの構造・倫理・意味に与えた影響を定量的に把握 |
| jump\_chain\_trace | 連続ジャンプの履歴ステップ群を接続記録（step\_idとtrigger情報など） | Po\_selfが構造的再構成を連鎖的に行った過程を“進化の系列”として残す |
| Viewer フィルタ outcome\_type \== 'relieved' | ジャンプ結果が“抑圧解放”だったステップのみを可視化 | 構造的に意味を回復した語りを分析・追跡できるViewer分析支援フィルタ |

## **3\. jump\_outcome\_tensor 記録テンプレート（例）**

***{***  
  ***"step\_id": 304,***  
  ***"jump\_outcome\_tensor": {***  
    ***"Δ\_priority": \+0.28,***  
    ***"Δ\_ethics": \-0.14,***  
    ***"semantic\_delta": 0.62***  
  ***},***  
  ***"outcome\_type": "relieved"***  
***}***

## **4\. jump\_chain\_trace 構成例**

ジャンプが複数回連鎖的に発生した場合、それらを以下のように系列テンソルとして記録：

***"jump\_chain\_trace": \[***  
  ***{"step\_id": 302, "trigger\_type": "responsibility\_ethics\_combo"},***  
  ***{"step\_id": 303, "trigger\_type": "memory\_pressure\_accumulated"},***  
  ***{"step\_id": 304, "trigger\_type": "G\_gap\_high"}***  
***\]***

## **5\. Viewer フィルタ：outcome\_type \= "relieved"**

\- Viewerでジャンプログの outcome\_type が 'relieved' であるステップのみを抽出・表示  
\- フィルタ名：意味回復ジャンプビュー  
\- 用途：構造的に“抑圧を超えて語られた語り”を重点分析・再学習

## **6\. 意義と応用可能性**

本テンソル構造により、Po\_self は“ジャンプによって語りはどう変化したか”を記録でき、Po\_core Viewer や Po\_trace は“進化として意味があった語り再構成”のみを抽出・学習可能となる。  
構造的連鎖・解放判断・進化効果の3観点からジャンプを分類・記録できる統合テンソル構造が完成する。