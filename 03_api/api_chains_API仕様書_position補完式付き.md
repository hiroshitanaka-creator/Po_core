# **/api/chains API仕様ドキュメント：補完式追記済み**

## **1\. エンドポイント概要**

/api/chains は、Po\_self のジャンプ系列情報を Viewer に提供するためのAPIエンドポイントであり、クラスタ情報・テンソル・人格メタ情報などを JSON 形式で返却します。

## **2\. Viewer向け position 補完式**

Viewer 側で \`position\` フィールドが欠損している場合（null または absent）、以下のテンソル値を使用して自動補完してください。

***📘 position補完式（Viewer用）***

***position \= {***  
  ***x: tensor.persona\_arc\_intensity,***  
  ***y: tensor.ethics\_arc\_intensity,***  
  ***z: tensor.semantic\_cohesion\_score***  
***}***

このロジックにより、API側で \`position\` を省略しても Viewer 側で 3Dプロットが正しく再現されます。