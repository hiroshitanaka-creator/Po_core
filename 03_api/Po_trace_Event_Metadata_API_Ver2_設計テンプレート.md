# **Po\_trace Event Metadata API Ver.2 設計テンプレート（多言語・スキーマ・バージョン対応）**

## **1\. 概要**

このテンプレートは、Po\_trace における Viewer 向けイベント表示メタデータを取得するための API を多言語・バージョン・スキーマ明示に対応させた設計仕様である。

## **2\. エンドポイント定義**

\- エンドポイント名: \`/api/v1/event\_metadata\`  
\- メソッド: GET  
\- 目的: Viewerの選択肢構築や国際化UI向けに、イベント種別とその表示情報を提供する

## **3\. 出力フォーマット（例）**

***{***  
  ***"reason\_types": \[***  
    ***{***  
      ***"value": "like",***  
      ***"label": "好意的反応",***  
      ***"description": "ユーザーが好意的反応を示した",***  
      ***"description\_en": "User gave a positive reaction"***  
    ***},***  
    ***...***  
  ***\],***  
  ***"impact\_types": \[***  
    ***{***  
      ***"value": "reclustered",***  
      ***"label": "再クラスタ化",***  
      ***"description": "系列構造が変更された",***  
      ***"description\_en": "Cluster structure was modified"***  
    ***}***  
  ***\]***  
***}***

## **4\. スキーマ定義（FastAPI用）**

FastAPI の \`response\_model=EventMetadataResponse\` を指定することで、OpenAPI UI に構造情報を自動表示できる。

***class EnumEntry(BaseModel):***  
    ***value: str***  
    ***label: str***  
    ***description: str***  
    ***description\_en: Optional\[str\]***

***class EventMetadataResponse(BaseModel):***  
    ***reason\_types: List\[EnumEntry\]***  
    ***impact\_types: List\[EnumEntry\]***

## **5\. 多言語対応設計**

\- 各Enumには \`description\`（日本語）と \`description\_en\`（英語）を実装。  
\- 将来的には \`description\_zh\` などを追加することで多国語展開が容易になる。  
\- Viewer側で \`lang\` フラグにより表示文言を切り替え可能。

## **6\. バージョン管理の意義**

\- \`/api/v1/\` の形式を採用することで、将来 \`/v2/\` への構造変更があっても既存クライアントとの互換性を保てる。  
\- ドキュメント・テスト環境・実運用環境を段階的に切り分けて導入できる。