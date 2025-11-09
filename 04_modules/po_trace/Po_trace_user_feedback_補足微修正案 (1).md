# **Po\_trace × /api/user\_feedback 統合設計 Ver.2 補足案（微修正案）**

## **1\. TraceEvent.timestamp の型精度補正**

\- 現在の \`Optional\[str\]\` を \`Optional\[datetime\]\` に変更することで、  
  Pydantic での型推論・自動バリデーション・ISO8601変換が正確に処理可能になる。

***例：***  
***from datetime import datetime***  
***from pydantic import Field***

***timestamp: Optional\[datetime\] \= Field(default\_factory=lambda: datetime.utcnow())***

## **2\. Enum型での補助文言表示（OpenAPI UI用）**

\- Swagger UIやFastAPIドキュメント上でEnumに補足文言を表示するには、\`\_\_str\_\_()\` を追加することで制御できる。

***例：***  
***from enum import Enum***

***class FeedbackAction(str, Enum):***  
    ***like \= "like"***  
    ***override\_persona \= "override\_persona"***  
    ***drag\_cluster \= "drag\_cluster"***

    ***def \_\_str\_\_(self):***  
        ***return f"{self.value} \- Viewer操作によるフィードバック"***

## **3\. 補足の意義**

\- datetime型の精度向上により、Viewer・Po\_trace間での履歴の整合性が向上する。  
\- Enum補足により、OpenAPIドキュメントの可読性と意図の説明性が高まり、他者との連携やレビューにも有効となる。