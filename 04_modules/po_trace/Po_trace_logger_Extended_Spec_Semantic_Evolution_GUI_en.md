# **Po_trace_logger Extended Specification (Semantic Evolution Visualization GUI)**

## **1. Overview**

This specification extends the GUI display of Po_trace_logger in Po_core by adding structures to visualize three axes on the card view: interference summary, jump linkage, and user resonance. The extended tensors align with the Po_core tensor structure to improve accountability of meaning and the visibility of evolutionary paths.

## **2. Extensions & Purposes**

| Extension | Purpose | Display Style |
| :---- | :---- | :---- |
| impact_profile_summary | Summarize overall semantic interference | Bar graph over axes (factual / causal / emotional) |
| trace_jump_linkage | Show links to semantic jumps | C_Φ^jump with link / 🔀 mark |
| user_resonance_badge | Visualize user resonance | 🟢🟠🔴 badge (based on Po_feedback.confidence) |

## **3. Integrated Card Layout Example**

┌────────────────────────────────────┐
│ 🔁 Step: reasoning_1 (fact_update)       │
│ Status: Reconstructing 🧠    GUI: YES    │
│ Impact Summary: F:0.75 C:0.28 E:0.52     │
│ Jump Link: explanation_2 (🔀 0.78)       │
│ W_conatus_trace: ▇▇▆▇█                    │
│ Emotion Shadow:  ▓░▒▒░  [-0.5, 0.7]       │
│ Reactivation Score: ▓▓▓▓▓░░░░ (0.84)      │
│ Resonance: 🟢 High Resonance              │
│ 📝 “This meaning wanted to be told.”      │
└────────────────────────────────────┘

## **4. Consistency with Po_core Tensors**

| Extension | Tensor Used | Structure |
| :---- | :---- | :---- |
| impact_profile_summary | impact_field_tensor | semantic_profile |
| trace_jump_linkage | semantic_delta, C_Φ^jump | Po_trace, Po_core_output |
| user_resonance_badge | Po_feedback.confidence | Po_core_output.user_feedback |

## **5. Outlook & Future Integration**

- impact_summary serves as an index for displaying semantic interference tendencies per step in Po_core Viewer.
- jump_linkage becomes a building block for Po_trace chain diagrams, expressing causal structure of meaning jumps in the GUI.
- user_resonance_badge visualizes resonance with Po_feedback and supports collaborative evolution assessment with users.
