from fastapi import FastAPI  
from pydantic import BaseModel  
from typing import List, Optional  
from enum import Enum

app \= FastAPI()

\# Enum Definitions

class ReasonType(str, Enum):  
    like \= "like"  
    disagree\_with\_label \= "disagree\_with\_label"  
    failed\_jump \= "failed\_jump"  
    ambiguous\_output \= "ambiguous\_output"

    @property  
    def label(self):  
        return {  
            "like": "好意的反応",  
            "disagree\_with\_label": "分類への異議",  
            "failed\_jump": "ジャンプ失敗",  
            "ambiguous\_output": "曖昧な出力"  
        }.get(self.value, self.value)

    @property  
    def description(self):  
        return {  
            "like": "ユーザーが好意的反応を示した",  
            "disagree\_with\_label": "Po\_self分類に対して異議があった",  
            "failed\_jump": "ジャンプ構造が意図どおりに到達しなかった",  
            "ambiguous\_output": "語りの出力が曖昧で再判断が必要だった"  
        }.get(self.value, self.value)

    @property  
    def description\_en(self):  
        return {  
            "like": "User gave a positive reaction",  
            "disagree\_with\_label": "User disagreed with the Po\_self classification",  
            "failed\_jump": "Jump structure failed to reach intended outcome",  
            "ambiguous\_output": "The output was ambiguous and needed reevaluation"  
        }.get(self.value, self.value)

class ImpactType(str, Enum):  
    reclustered \= "reclustered"  
    tag\_updated \= "profile\_tag\_updated"  
    priority\_adjusted \= "priority\_adjusted"

    @property  
    def label(self):  
        return {  
            "reclustered": "再クラスタ化",  
            "tag\_updated": "タグ更新",  
            "priority\_adjusted": "優先度調整"  
        }.get(self.value, self.value)

    @property  
    def description(self):  
        return {  
            "reclustered": "系列構造が変更された",  
            "tag\_updated": "人格ラベルが更新された",  
            "priority\_adjusted": "Po\_self優先度が調整された"  
        }.get(self.value, self.value)

    @property  
    def description\_en(self):  
        return {  
            "reclustered": "Cluster structure was modified",  
            "tag\_updated": "Persona label was updated",  
            "priority\_adjusted": "Po\_self priority was adjusted"  
        }.get(self.value, self.value)

\# Pydantic Models for Schema

class EnumEntry(BaseModel):  
    value: str  
    label: str  
    description: str  
    description\_en: Optional\[str\]

class EventMetadataResponse(BaseModel):  
    reason\_types: List\[EnumEntry\]  
    impact\_types: List\[EnumEntry\]

\# API endpoint (v1)

@app.get("/api/v1/event\_metadata", response\_model=EventMetadataResponse)  
def get\_event\_metadata():  
    return {  
        "reason\_types": \[  
            EnumEntry(  
                value=r.value,  
                label=r.label,  
                description=r.description,  
                description\_en=r.description\_en  
            ) for r in ReasonType  
        \],  
        "impact\_types": \[  
            EnumEntry(  
                value=i.value,  
                label=i.label,  
                description=i.description,  
                description\_en=i.description\_en  
            ) for i in ImpactType  
        \]  
    }  
