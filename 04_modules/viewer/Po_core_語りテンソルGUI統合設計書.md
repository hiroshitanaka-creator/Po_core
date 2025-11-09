# **Po\_core 語りテンソルGUI統合設計書**

## **1\. 概要**

本設計書は、Po\_coreにおけるsemantic-evolution-journal（語りテンソル）の出力制御とViewer GUIを統合し、ユーザーが表現濃度（expression\_mode）を調整可能とする構造の全体統合案である。

## **2\. 統合対象モジュール構成**

| 機能名 | モジュール名 | 役割 |
| :---- | :---- | :---- |
| 語り出力生成 | journal\_generator() | モード別journal文生成（構造／ナラティブ／詩的） |
| GUI制御 | viewer\_ui.py | 語り濃度スライダーとプレビュー表示 |
| 状態管理 | viewer\_state.py | expression\_modeの保持・反映 |
| 表現テンプレ | expression\_map.json | 各モードの出力語彙・補正スカラー等定義 |

## **3\. GUIスライダー実装とjournal連動**

\- Streamlitスライダーで expression\_mode を設定（structure / medium / poetic）  
\- そのモードを元に background\_color / プレビュー表示 / journal\_generator() を呼び出し

## **4\. Po\_self圧力補正連動**

journal出力のモードに応じて priority\_score を補正：  
structure → ×1.00  
medium → ×1.15  
poetic → ×1.30

***expression\_scaling \= {***  
    ***"structure": 0.00,***  
    ***"medium": 0.15,***  
    ***"poetic": 0.30***  
***}***  
***adjusted\_priority \= base\_score \* (1 \+ expression\_scaling\[expression\_mode\])***

## **5\. 表示構造例とテンソル出力**

Po\_traceテンソル内に以下のように記録される：

{  
  "step\_id": "214",  
  "journal\_mode": "medium",  
  "journal\_confidence": 0.72,  
  "expression\_scaling": 0.15,  
  "journal\_text": "Po\_coreはこの過程で factual 軸を補強し..."  
}

## **6\. 最終意義と展望**

この統合により、Po\_core Viewerは“語りの強度”と“進化構造の圧力”を同時に制御可能となり、ユーザーは詩的・構造的なバランスを自らの目的に応じて選択可能となる。