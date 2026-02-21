# **Po\_self API Extended Defense Design Document: Security Enhancement Template**

# **1. Overview**

#

# **This document presents an extended design proposal for achieving a secure intellectual interface for the production operation of the Po\_self API by introducing multilayered defense mechanisms such as API key authentication, JWT control, and request abuse prevention. The goal is to realize reliability, restriction, and scalability.**

#

# **2. API Key + Domain/IP Restriction**

#

# **Even if the API key matches, requests are blocked unless they come from trusted source domains or IP addresses.**

#

# **Implementation Layer: FastAPI’s Depends function or WAF/API Gateway (e.g., Cloudflare)**

#

# **Implementation Example (FastAPI):**

#

# **TRUSTED\_IPS = {"203.0.113.42", "192.168.1.100"}**

#

# **async def verify\_ip(request: Request):**

# **client\_ip = request.client.host**

# **if client\_ip not in TRUSTED\_IPS:**

# **raise HTTPException(status\_code=403, detail="Access denied from IP")**

#

# **3. Embedding Viewer Mode in JWT Claims**

#

# **By including fields such as mode and role in the JWT payload, UI-specific behaviors can be restricted.**

#

# **Example:**

#

# **{**

# **"sub": "viewer\_1138",**

# **"mode": "viewer",**

# **"role": "readonly",**

# **"exp": 1723456000**

# **}**

#

#

# **Access Control Example:**

# **if token\_payload.get("role") != "admin": raise 403**

#

# **4. Rate Limiting (DoS/Abuse Countermeasures)**

#

# **Limit the access frequency for each client (API key or IP).**

#

# **Library: slowapi (can be linked with Redis)**

#

# **Implementation Example:**

#

# **from slowapi import Limiter**

# **from slowapi.util import get\_remote\_address**

#

# **limiter = Limiter(key\_func=get\_remote\_address)**

#

# **@app.get("/api/chains")**

# **@limiter.limit("60/minute")**

# **def get\_chains(...):**

# **...**

#

# **5. Recommended Implementation Stages**

#

# **Phase 1: API key + IP restriction (immediate implementation)**

#

# **Phase 2: JWT + UI restriction (mid-term construction)**

#

# **Phase 3: Rate Limiting (stabilizing access)**
