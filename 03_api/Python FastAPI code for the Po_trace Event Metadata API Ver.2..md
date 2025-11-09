from fastapi import FastAPI  

from pydantic import BaseModel  

from typing import List, Optional  

from enum import Enum



app = FastAPI()



\# Enum Definitions



class ReasonType(str, Enum):  

&nbsp;   like = "like"  

&nbsp;   disagree\_with\_label = "disagree\_with\_label"  

&nbsp;   failed\_jump = "failed\_jump"  

&nbsp;   ambiguous\_output = "ambiguous\_output"



&nbsp;   @property  

&nbsp;   def label(self):  

&nbsp;       return {  

&nbsp;           "like": "Positive Reaction",  

&nbsp;           "disagree\_with\_label": "Disagreement with Classification",  

&nbsp;           "failed\_jump": "Jump Failure",  

&nbsp;           "ambiguous\_output": "Ambiguous Output"  

&nbsp;       }.get(self.value, self.value)



&nbsp;   @property  

&nbsp;   def description(self):  

&nbsp;       return {  

&nbsp;           "like": "The user gave a positive reaction",  

&nbsp;           "disagree\_with\_label": "There was disagreement with the Po\_self classification",  

&nbsp;           "failed\_jump": "The jump structure did not reach the intended outcome",  

&nbsp;           "ambiguous\_output": "The narrative output was ambiguous and needed reevaluation"  

&nbsp;       }.get(self.value, self.value)



&nbsp;   @property  

&nbsp;   def description\_en(self):  

&nbsp;       return {  

&nbsp;           "like": "User gave a positive reaction",  

&nbsp;           "disagree\_with\_label": "User disagreed with the Po\_self classification",  

&nbsp;           "failed\_jump": "Jump structure failed to reach intended outcome",  

&nbsp;           "ambiguous\_output": "The output was ambiguous and needed reevaluation"  

&nbsp;       }.get(self.value, self.value)



class ImpactType(str, Enum):  

&nbsp;   reclustered = "reclustered"  

&nbsp;   tag\_updated = "profile\_tag\_updated"  

&nbsp;   priority\_adjusted = "priority\_adjusted"



&nbsp;   @property  

&nbsp;   def label(self):  

&nbsp;       return {  

&nbsp;           "reclustered": "Reclustered",  

&nbsp;           "tag\_updated": "Tag Updated",  

&nbsp;           "priority\_adjusted": "Priority Adjusted"  

&nbsp;       }.get(self.value, self.value)



&nbsp;   @property  

&nbsp;   def description(self):  

&nbsp;       return {  

&nbsp;           "reclustered": "Cluster structure was modified",  

&nbsp;           "tag\_updated": "Persona label was updated",  

&nbsp;           "priority\_adjusted": "Po\_self priority was adjusted"  

&nbsp;       }.get(self.value, self.value)



&nbsp;   @property  

&nbsp;   def description\_en(self):  

&nbsp;       return {  

&nbsp;           "reclustered": "Cluster structure was modified",  

&nbsp;           "tag\_updated": "Persona label was updated",  

&nbsp;           "priority\_adjusted": "Po\_self priority was adjusted"  

&nbsp;       }.get(self.value, self.value)



\# Pydantic Models for Schema



class EnumEntry(BaseModel):  

&nbsp;   value: str  

&nbsp;   label: str  

&nbsp;   description: str  

&nbsp;   description\_en: Optional\[str]



class EventMetadataResponse(BaseModel):  

&nbsp;   reason\_types: List\[EnumEntry]  

&nbsp;   impact\_types: List\[EnumEntry]



\# API endpoint (v1)



@app.get("/api/v1/event\_metadata", response\_model=EventMetadataResponse)  

def get\_event\_metadata():  

&nbsp;   return {  

&nbsp;       "reason\_types": \[  

&nbsp;           EnumEntry(  

&nbsp;               value=r.value,  

&nbsp;               label=r.label,  

&nbsp;               description=r.description,  

&nbsp;               description\_en=r.description\_en  

&nbsp;           ) for r in ReasonType  

&nbsp;       ],  

&nbsp;       "impact\_types": \[  

&nbsp;           EnumEntry(  

&nbsp;               value=i.value,  

&nbsp;               label=i.label,  

&nbsp;               description=i.description,  

&nbsp;               description\_en=i.description\_en  

&nbsp;           ) for i in ImpactType  

&nbsp;       ]  

&nbsp;   }  



