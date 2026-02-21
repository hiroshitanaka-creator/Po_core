# **Po\_trace 進化Ver.4 構造テンプレート（多用途・多言語・UI分離対応）**

## **1\. 概要**

本テンプレートは、Po\_trace の TraceEvent を多言語対応・ログ要約・UI分離といった観点で進化させ、Po\_self と Viewer の双方向的かつ意味的なインタフェースとして高精度に拡張するものである。

## **2\. TraceEvent 拡張構造定義（Ver.4）**

***class TraceEvent(BaseModel):***
    ***event\_type: EventType***
    ***source: SourceType***
    ***actor\_id: str***
    ***reason: ReasonType***
    ***impact\_on\_chain: ImpactType***
    ***chain\_id: str***
    ***timestamp: datetime \= Field(default\_factory=lambda: datetime.utcnow())***

    ***def summary(self) \-\> str:***
        ***return f"\[{self.timestamp.isoformat()}\] {self.actor\_id} via {self.source} did {self.event\_type} ({self.reason}) on {self.chain\_id}"***

## **3\. Enum構造：description / description\_en / label の分離**

UI・意味・言語を分離して扱えるよう、以下の構造を採用する。

***class ReasonType(str, Enum):***
    ***like \= "like"***
    ***disagree\_with\_label \= "disagree\_with\_label"***

    ***@property***
    ***def label(self) \-\> str:***
        ***return {***
            ***"like": "好意的反応",***
            ***"disagree\_with\_label": "分類への異議"***
        ***}.get(self.value, self.value)***

    ***@property***
    ***def description(self) \-\> str:***
        ***return {***
            ***"like": "ユーザーが好意的反応を示した",***
            ***"disagree\_with\_label": "Po\_self分類に対して異議があった"***
        ***}.get(self.value, self.value)***

    ***@property***
    ***def description\_en(self) \-\> str:***
        ***return {***
            ***"like": "User gave a positive reaction",***
            ***"disagree\_with\_label": "User disagreed with the Po\_self classification"***
        ***}.get(self.value, self.value)***

## **4\. 意義と展望**

\- \`summary()\` によりログ出力・モニタリングが簡素化される。
\- \`label()\` によりViewer表示が簡潔・一貫化される。
\- \`description()\` と \`description\_en\` によりPo\_selfは意味判断と翻訳を分離しやすくなる。
\- これらにより Po\_trace は「語りと判断のあいだの意味責任装置」として完成に近づく。
