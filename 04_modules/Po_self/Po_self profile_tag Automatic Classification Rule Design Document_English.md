# **# Po\_self profile\_tag Automatic Classification Rule Design Document**

#

# **## 1. Overview**

#

# **This design document defines the rules for Po\_self to automatically generate and assign semantic and structural classification labels (profile\_tags) to each jump series, based on series scalar values (such as avg\_deltas and fluctuation\_scores) recorded in T\_chain\_profile.**

#

# **## 2. List of Tensors Used**

#

# **- avg\_semantic\_delta**

# **- semantic\_fluctuation\_score**

# **- avg\_ethics\_delta**

# **- ethics\_fluctuation\_score**

# **- avg\_priority\_delta**

#

# **## 3. List of Classification Rules**

#

# **### semantic\_surge\_chain**

#

# **Condition: avg\_semantic\_delta > 0.3 and semantic\_fluctuation\_score < 0.06**

#

# **Meaning: A series where semantic jumps are continuous and stable.**

#

# **### semantic\_drift\_chain**

#

# **Condition: semantic\_fluctuation\_score > 0.08**

#

# **Meaning: A series where semantic jumps were unstable.**

#

# **### semantic\_collapse\_chain**

#

# **Condition: avg\_semantic\_delta < -0.1**

#

# **Meaning: A series where semantic pressure was contracting (tendency towards silence).**

#

# **### ethics\_recovery\_chain**

#

# **Condition: avg\_ethics\_delta < -0.05 and ethics\_fluctuation\_score < 0.05**

#

# **Meaning: A series where the ethics tensor was stably recovering.**

#

# **### ethics\_drift\_chain**

#

# **Condition: ethics\_fluctuation\_score > 0.07**

#

# **Meaning: A series where ethical judgments were inconsistent.**

#

# **### structural\_escalation\_chain**

#

# **Condition: avg\_priority\_delta > 0.2**

#

# **Meaning: A series where structural responsibility pressure was excessively accumulating.**

#

# **## 4. Composite Tags and Priority Strategy**

#

# **- When multiple conditions are met:**

# **・List as composite labels (e.g., \['semantic\_drift\_chain', 'ethics\_drift\_chain'])**

# **・Alternatively, record as profile\_tag\_primary / profile\_tag\_secondary separately**

# **- The axis with the highest fluctuation\_score is set as the main classification.**

#

# **## 5. Applications**

#

# **- Used for viewer filtering and clustering classification**

# **- Utilized for category classification in series vector pressure heatmaps**

# **- Used as input labels for prioritizing reconstruction candidates and generating series learning patterns**

#
