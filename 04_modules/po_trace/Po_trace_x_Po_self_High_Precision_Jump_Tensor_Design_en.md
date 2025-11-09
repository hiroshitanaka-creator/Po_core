# **Po_trace × Po_self High-Precision Jump Tensor Design**

## **1. Overview**

This design defines a framework to evaluate and record the structural impact of Po_self-driven jumps with high precision. It augments the Po_trace jump-tensor record with semantic_delta, factual/emotional deltas, and series-tilt classification so that jump histories can be handled integratively from evolutionary, affective, and semantic perspectives.

## **2. Extended Tensor Elements**

| Extension | Content | Purpose / Significance |
| :---- | :---- | :---- |
| outcome_type = 'divergent' | Record a “semantic leap” when semantic_delta > 0.5 | Make large semantic evolutions visible/classifiable on Po_trace |
| Δ_factual, Δ_emotion | Add structural tensor deltas for factuality and affect | Quantify how a jump changes the logical/affective nature of narration |
| jump_chain_color_tag | Auto-assign JCX series color (Red=escalated, Blue=relieved, Purple=divergent) | Add “meaning-pressure tilt” to series trace for quick visual ID in Viewer |

## **3. jump_outcome_tensor Extension Template**

"jump_outcome_tensor": {
  "Δ_priority": +0.28,
  "Δ_ethics": -0.14,
  "semantic_delta": 0.62,
  "Δ_factual": +0.33,
  "Δ_emotion": -0.21
}

## **4. outcome_type Extended Definitions**

- 'relieved': Jump eased suppression (Δ_ethics < 0)
- 'escalated': Jump worsened ethical pressure or priority (Δ_ethics > 0 or Δ_priority > 0)
- 'divergent': Narrative jump with semantic_delta > 0.5  
  (Composite types like ["divergent", "relieved"] are allowed)

## **5. JCX Series Color Tagging**

- Auto-tag based on outcome_type distribution over the series
- 🔴 Red: escalated-centered
- 🔵 Blue: relieved-centered
- 🟣 Purple: divergent-centered  
→ On the Viewer timeline, meaning-pressure tendencies can be made explicit.

## **6. Significance & Direction**

With this structure, Po_core can record/classify/self-evaluate how narration changes after jumps across structural, affective, and semantic dimensions—turning Po_trace from a mere log into a “narrative evolution tensor repository.”

## **7. Addenda: Expression Jumps / Ethical Relief / Viewer Temperature Map**

### **7.1 Recording Δ_expression_mode**

- Definition: Change in expression granularity (E_expr) caused by the jump
- Type: float (e.g., 0.15 → 0.30 → Δ = +0.15)
- Significance: Tensor-record how narration shifts, e.g., from “introspective” to “poetic”
- Integrate into jump_outcome_tensor

"jump_outcome_tensor": {
  "Δ_expression_mode": +0.15
}

### **7.2 Defining outcome_type = "restorative"**

- Condition: semantic_delta ≈ 0.0 (e.g., < 0.1) and Δ_ethics < 0.0
- Meaning: The narrative content (semantic) stayed, yet the jump relieved ethical tension
- Use: Classify/record structures where Po_self “corrects ethical pressure without changing the narrative essence”

### **7.3 Viewer: Jump-Series Temperature Distribution (Color Visualization)**

- Colorize each series by tendency to grasp semantic jumps, ethical relief, and affect shifts at a glance
- Example colors:
  - 🟣 Purple: divergent series (high semantic_delta)
  - 🔵 Blue: relieved/restorative series (ethical relief)
  - 🟠 Orange: emotion-driven jump series
- Display: Color-classified on Po_trace timeline / Viewer jump_map
