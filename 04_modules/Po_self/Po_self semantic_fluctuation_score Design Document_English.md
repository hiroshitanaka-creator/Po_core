# Po_self semantic_fluctuation_score Design Document

## 1. Overview

This design document presents the definition and classification indicators of the tensor scalar `semantic_fluctuation_score` for quantitatively evaluating semantic fluctuation within jump chain traces in Po_self.

## 2. Definition and Calculation Formula

`semantic_fluctuation_score` is defined as the standard deviation (std) of semantic_delta values within a series:

semantic_fluctuation_score = std([semantic_delta_step_1, ..., step_n])

- Small values: Semantic jumps are stable (minor changes or consistent).
- Large values: Semantic jumps are abrupt/chaotic.

## 3. Classification Labels and Score Interpretation

| Score Range | Label                | Interpretation                                        |
| :---------- | :------------------- | :---------------------------------------------------- |
| < 0.03      | 🟢 Stable            | Jumps are subtle or consistently stable               |
| 0.03 – 0.08 | 🟡 Tendency to Leap  | Has semantic direction, but some fluctuation exists   |
| > 0.08      | 🔴 Unstable          | Semantic mixture/disorder is observed in the series   |

## 4. Application Structure and Extensibility

- Add `semantic_fluctuation_score` to T_chain_profile
- In Viewer display, show as label, color band, and heat bar
- Example of automatic profile_tags: `semantic_drift_chain`, `meaning_pulse_chain`
- Integrated evaluation with other tensors (Δ_expression_mode, Δ_emotion) is also possible
