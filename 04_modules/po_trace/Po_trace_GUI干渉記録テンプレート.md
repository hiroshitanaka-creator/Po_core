# **Po\_trace × Po\_self GUI干渉記録構造テンプレート**

## **1\. 概要**

本テンプレートは、Po\_traceとPo\_selfのテンソル構造をGUI操作によって横断的に接続・記録するための標準フォーマットである。GUI操作によって再構成されたPo\_traceステップに関する情報を、進化的・責任的観点から記録・検証可能にする。

## **2\. JSON構造テンプレート**

***{***  
  ***"interference\_log": {***  
    ***"step\_id": "reasoning\_1",***  
    ***"po\_id": "po\_3921",***  
    ***"source": "GUI",***  
    ***"action\_type": "allow\_reconstruction",***  
    ***"timestamp": "2025-07-14T15:40:00Z",***  
    ***"conatus\_triggered": true,***  
    ***"reactivation\_metadata": {***  
      ***"S\_conatus": 0.82,***  
      ***"emotion\_shadow\_curve": \[-0.5, \-0.3\],***  
      ***"W\_conatus\_trace": \[0.31, 0.54, 0.68\],***  
      ***"reactivation\_urge\_score": 0.91***  
    ***},***  
    ***"Po\_self\_status": "queued",***  
    ***"Po\_trace\_sync": {***  
      ***"reactivated\_by\_GUI": true,***  
      ***"manual\_override": false***  
    ***}***  
  ***}***  
***}***

## **3\. フィールド定義と解説**

| フィールド | 説明 |
| :---- | :---- |
| step\_id | Po\_traceステップの一意識別子 |
| po\_id | 対応するPo\_core出力のID |
| source | 干渉元（GUI / 自律発火 / API等） |
| action\_type | GUIでの操作種別（例: skip, allow\_reconstruction） |
| timestamp | 操作時のUTCタイムスタンプ |
| conatus\_triggered | S\_conatus \> θ による自律発火が発生したか |
| reactivation\_metadata | 再発芽テンソル群（意志・情動・痕跡） |
| Po\_self\_status | Po\_self側での状態（queued, skipped 等） |
| Po\_trace\_sync.reactivated\_by\_GUI | GUIから明示的に再構成されたか |
| Po\_trace\_sync.manual\_override | 手動でpriorityが変更されたか |

## **4\. 応用先と活用例**

• Po\_self\_recursor：優先度操作と再構成キュー管理

• Po\_trace\_logger：GUI介入履歴の記録・可視化

• audit\_dashboard：人的干渉 vs 自律進化の割合可視化

• final\_output.explanation：構造的判断の由来説明に挿入