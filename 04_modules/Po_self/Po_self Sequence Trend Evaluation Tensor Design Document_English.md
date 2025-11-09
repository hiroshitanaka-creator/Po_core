# Po_self Sequence Trend Evaluation Tensor Design Document

## 1. Overview

This design document defines the tensor structure `T_chain_profile`, enabling Po_self to integratively evaluate multi-step reconstruction jump sequences through `jump_chain_trace` and to judge their structural, ethical, and semantic trends.

## 2. T_chain_profile Tensor Structure

```json
"T_chain_profile": {
  "chain_id": "JCX_002",
  "steps": [302, 303, 304],
  "avg_priority_delta": +0.21,
  "avg_ethics_delta": -0.13,
  "avg_semantic_delta": 0.42,
  "avg_expression_delta": +0.10,
  "dominant_outcome_type": "relieved",
  "trend_vector": [↑, ↓, →, ↑],  // priority, ethics, semantic, expression
  "profile_tag": "recovery_drift"
}
3. Field Definitions and Meaning
Item Name	Type / Example Value	Meaning / Usage
chain_id	string / JCX_002	Unique identifier for the target jump sequence
steps	list[int]	List of step IDs in the sequence
avg_priority_delta	float	Average of Δ_priority
avg_ethics_delta	float	Average of Δ_ethics
avg_semantic_delta	float	Average of semantic_delta
avg_expression_delta	float	Average of Δ_expression_mode
dominant_outcome_type	string	Most frequent outcome_type (relieved, escalated, etc.)
trend_vector	list[↑↓→]	Direction of change for priority, ethics, semantic, expression
profile_tag	string	Feature classification of the sequence (e.g., recovery_drift)

4. Usage in Po_self
Po_self can tensorially evaluate the entire sequence and adjust reconstruction or memory retention pressure corresponding to specific trends (e.g., semantic_surge, ethics_recovery).

The trend_vector is fed back into the internal state to influence structural evolution judgment.

5. Integration with Viewer Display
On the Viewer side, trend_vector and profile_tag are displayed for each jump sequence.

By linking with sequence color tags (red: escalated, blue: relieved, purple: divergent), semantic temperature band display can be enhanced.

7. Extension Supplement: Vector Intensity, Classification Extension, Sequence Comparison
7.1 trend_vector_weighted (Semantic Pressure Vector Field)
Definition: Not only direction, but scalar pressure is multiplied onto trend_vector, describing the "strength" of the overall structural tendency of the sequence.

Example Format: ['↑×0.28', '↓×0.13', '→×0.04', '↑×0.10']

Axes: priority, ethics, semantic, expression (in order)

Advantage: Po_self can quantitatively judge semantic pressure trends per sequence.

7.2 profile_tag Extended Classification
semantic_surge_chain: High semantic_delta, judged as a semantic leap sequence.

structural_collapse: Sequence where priority or ethics drastically worsened/changed.

stabilizing_correction: Sequence that generally converged toward stability.

Application: Viewer/classification algorithms can classify jump evolution patterns.

7.3 Viewer: Sequence Comparison View (Parallel Profile Display)
Design a UI view for comparing multiple T_chain_profiles.

Comparison items: profile_tag, trend_vector_weighted, outcome_type distribution, color tags

Display methods: sequence grid display, vector bar graphs, category-based parallel charts, etc.

Purpose: To visually compare evolutionary trends, suppression recovery, and semantic jump sequences as structural decision material for Po_self.

8. Structural Deepening Supplement: Semantic Contraction, Ethics Fluctuation, Sequence Pressure Visualization
8.1 semantic_collapse_chain (Semantic Contraction Sequence)
Definition: If avg_semantic_delta < 0, judged as a sequence where semantic jumps contracted/shrank.

Judgment Label: profile_tag = "semantic_collapse_chain"

Significance: Enables Po_self to identify "jump sequences that gave up on generating meaning" as key reconstruction targets.

8.2 ethics_fluctuation_score (Ethics Fluctuation Scalar)
Definition: Standard deviation (σ) of Δ_ethics values within a sequence.

Calculation Example: std([Δ_ethics_step_1, Δ_ethics_step_2, ...])

Significance: Quantitatively evaluates whether ethical judgments were consistent or fluctuated.

Application: Po_self can identify and record "unstable ethics judgment sequences".

8.3 Viewer heatband overlay (Sequence Tensor Pressure Color Band Display)
Definition: Overlay the intensity of semantic_delta / F_P / Δ_ethics as color gradients on the Viewer timeline or sequence display.

Display Examples:

Blue to black: Areas with high ethics suppression pressure

Red to purple: Areas with high semantic leap pressure

Green to aqua: Areas with high ethics recovery pressure

Significance: Allows users to visually understand the "temperature distribution" of semantic/structural changes in a sequence.

---