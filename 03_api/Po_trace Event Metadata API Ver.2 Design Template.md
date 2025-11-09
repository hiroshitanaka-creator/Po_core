# **Po\_trace Event Metadata API Ver.2 Design Template (Multilingual, Schema, and Versioning Support)**

# **1. Overview**

# 

# **This template provides the API design specification for retrieving event display metadata for the Viewer in Po\_trace, supporting multilingual, versioning, and explicit schema definitions.**

# 

# **2. Endpoint Definition**

# 

# **Endpoint: /api/v1/event\_metadata**

# 

# **Method: GET**

# 

# **Purpose: Provides event types and their display information for building Viewer options and internationalized UIs**

# 

# **3. Output Format (Example)**

# **{**

#   **"reason\_types": \[**

#     **{**

#       **"value": "like",**

#       **"label": "好意的反応",**

#       **"description": "ユーザーが好意的反応を示した",**

#       **"description\_en": "User gave a positive reaction"**

#     **},**

#     **...**

#   **],**

#   **"impact\_types": \[**

#     **{**

#       **"value": "reclustered",**

#       **"label": "再クラスタ化",**

#       **"description": "系列構造が変更された",**

#       **"description\_en": "Cluster structure was modified"**

#     **}**

#   **]**

# **}**

# 

# **4. Schema Definition (for FastAPI)**

# 

# **By specifying response\_model=EventMetadataResponse in FastAPI, structure information can be automatically displayed in the OpenAPI UI.**

# 

# **class EnumEntry(BaseModel):**

#     **value: str**

#     **label: str**

#     **description: str**

#     **description\_en: Optional\[str]**

# 

# **class EventMetadataResponse(BaseModel):**

#     **reason\_types: List\[EnumEntry]**

#     **impact\_types: List\[EnumEntry]**

# 

# **5. Multilingual Design**

# 

# **Each Enum implements both description (Japanese) and description\_en (English).**

# 

# **In the future, adding description\_zh, etc., will enable easy multilingual expansion.**

# 

# **The Viewer can switch display language according to the lang flag.**

# 

# **6. Significance of Version Control**

# 

# **By adopting the /api/v1/ format, future structural changes (e.g., to /v2/) can be made while maintaining compatibility with existing clients.**

# 

# **Enables phased introduction in documentation, test environments, and production environments.**

