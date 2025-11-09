# **Po\_self API 拡張防衛設計書：セキュリティ高度化テンプレート**

## **1\. 概要**

本書は Po\_self API の本番運用において、APIキー認証・JWT制御・リクエスト濫用防止といった多層的な防衛機構を導入することで、信頼性・限定性・拡張性を持ったセキュアな知的インターフェースを実現するための拡張設計案を提示する。

## **2\. APIキー \+ ドメイン/IP 制限**

\- APIキーが一致していても、信頼できる送信元ドメインまたはIPアドレスからのリクエストでなければブロックする方式  
\- 実装レイヤ：FastAPIのDepends関数 または WAF／API Gateway（例：Cloudflare）  
\- 実装例（FastAPI）:

***TRUSTED\_IPS \= {"203.0.113.42", "192.168.1.100"}***

***async def verify\_ip(request: Request):***  
    ***client\_ip \= request.client.host***  
    ***if client\_ip not in TRUSTED\_IPS:***  
        ***raise HTTPException(status\_code=403, detail="Access denied from IP")***

## **3\. JWT Claim に Viewerモードを埋め込む**

\- JWTのpayloadに \`mode\`, \`role\` などのフィールドを含めることで、UIごとの振る舞いを制限可能  
\- 例:

***{***  
  ***"sub": "viewer\_1138",***  
  ***"mode": "viewer",***  
  ***"role": "readonly",***  
  ***"exp": 1723456000***  
***}***

\- アクセス制御例：  
    if token\_payload.get("role") \!= "admin": raise 403

## **4\. Rate Limiting（DoS/濫用対策）**

\- 各クライアント（APIキー or IP）ごとにアクセス頻度を制限  
\- ライブラリ：slowapi（Redis連携可能）  
\- 実装例:

***from slowapi import Limiter***  
***from slowapi.util import get\_remote\_address***

***limiter \= Limiter(key\_func=get\_remote\_address)***

***@app.get("/api/chains")***  
***@limiter.limit("60/minute")***  
***def get\_chains(...):***  
    ***...***

## **5\. 推奨導入ステージ**

\- フェーズ1：APIキー \+ IP制限（即時導入）  
\- フェーズ2：JWT \+ UI制限（中期構築）  
\- フェーズ3：Rate Limiting（アクセス安定化）