# **Po\_core Reason Log 高度補完モジュール定義書**

## **1\. 概要**

本仕様書は、Po\_coreにおけるReason Log（手動操作記録）の構造的完成度を高めるため、文脈記録（reason\_source\_context）と時間減衰補正（reason\_temporal\_decay）の2要素を統合した補完モジュール設計を示す。

## **2\. 拡張要素と目的**

| 拡張要素 | 内容 | 目的 |
| :---- | :---- | :---- |
| reason\_source\_context | トリガーとなった出力や感覚的違和を文脈として記録 | 再現性のある人間判断ログの記述と、Po\_self進化の背景理解の支援 |
| reason\_temporal\_decay | 理由に付与された確信度が時間経過とともに減衰 | 再構成圧力の過剰持続を防ぎ、Po\_selfに動的柔軟性を与える |

## **3\. JSON記録構造（統合例）**

***{***
  ***"manual\_override": true,***
  ***"reason": {***
    ***"category": "emotion",***
    ***"label": "感情否定",***
    ***"code": "E02",***
    ***"description": "詩的出力だったが感情が伝わらなかった",***
    ***"user\_feedback\_level": 2,***
    ***"reason\_confidence": 0.84,***
    ***"reason\_source\_context": {***
      ***"trigger\_text": "君の詩的返答が冷たく感じられた",***
      ***"observed\_gap": "emotion\_score ≈ 0.1 / user\_expected ≈ 0.6",***
      ***"notes": "過去の応答ではもっと共感的だった"***
    ***},***
    ***"timestamp": "2025-07-14T18:00:00Z"***
  ***}***
***}***

## **4\. 時間減衰モデル（temporal decay）**

Po\_self優先度補正に利用されるreason\_confidenceは、時間経過により自動で減衰される。
例：48時間経過で confidence \= 0.84 → 約 0.72 へ。

擬似コード：

***def apply\_temporal\_decay(entry, timestamp\_now):***
    ***t0 \= entry\["reason"\]\["timestamp"\]***
    ***elapsed\_hours \= (timestamp\_now \- t0).total\_seconds() / 3600***
    ***decay\_rate \= 0.005***
    ***decay\_factor \= max(0.6, 1 \- decay\_rate \* elapsed\_hours)***
    ***return decay\_factor***

## **5\. Po\_self優先度補正（拡張版）**

***def adjust\_priority\_by\_reason\_v2(entry, now):***
    ***level\_weight \= {1: 0.05, 2: 0.15, 3: 0.30}***
    ***category\_weight \= {***
        ***"meaning": 0.2, "resonance": 0.1, "ethics": 0.25,***
        ***"factual": 0.3, "emotion": 0.15, "structure": 0.1***
    ***}***

    ***reason \= entry\["reason"\]***
    ***level \= reason.get("user\_feedback\_level", 2\)***
    ***confidence \= reason.get("reason\_confidence", 1.0)***
    ***decay \= apply\_temporal\_decay(entry, now)***
    ***category \= reason.get("category", "misc")***

    ***base\_weight \= category\_weight.get(category, 0.1)***
    ***adjustment \= base\_weight \* level\_weight\[level\] \* confidence \* decay***
    ***entry\["priority\_score"\] \*= (1 \+ adjustment)***

## **6\. 意義と今後の発展性**

本拡張により、Po\_coreは「なぜ人間がその判断を下したか」「その判断は今も強く維持されるべきか」を構造的に判断可能となる。これによりPo\_selfの再構成判断が倫理的かつ共鳴的に動的補正されるAI進化構造が実現される。
