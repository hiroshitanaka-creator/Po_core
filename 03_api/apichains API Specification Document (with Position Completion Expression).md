# **/api/chains API Specification Document: With Completion Expression**

# **1. Endpoint Overview**

# 

# **/api/chains is an API endpoint that provides Po\_self jump sequence information to the Viewer, returning cluster information, tensors, persona meta-information, and more in JSON format.**

# 

# **2. Position Completion Expression for Viewer**

# 

# **If the position field is missing (null or absent) on the Viewer side, please automatically complete it using the following tensor values:**

# 

# **📘 Position Completion Expression (for Viewer)**

# 

# **position = {**

#   **x: tensor.persona\_arc\_intensity,**

#   **y: tensor.ethics\_arc\_intensity,**

#   **z: tensor.semantic\_cohesion\_score**

# **}**

# 

# 

# **With this logic, even if position is omitted on the API side, the Viewer can correctly reconstruct the 3D plot.**

