# Po_self Jump Trigger Decision Function Definition

## 1. Overview

This definition document defines the function `calculate_Jump_trigger_score()` for calculating the jump trigger score in Po_self, by combining the narrative responsibility scalar (R_priority) and ethics tensor fluctuation (Δ_ethics).

## 2. Jump Trigger Score Formula

Jump_trigger_score = α × R_priority + β × jump_strength × Δ_ethics

## 3. Parameter Definitions

| Variable      | Meaning                                 | Example / Range   |
| :------------ | :-------------------------------------- | :---------------- |
| R_priority    | Reconstruction priority scalar          | e.g., 0.0–1.0+    |
| jump_strength | Step-specific jump tendency scalar      | e.g., 0.0–1.0     |
| Δ_ethics      | Temporal change of W_ethics             | e.g., −0.3 to +0.3|
| α             | Weight for responsibility scalar        | Default: 1.0      |
| β             | Weight for ethics fluctuation           | Default: 0.8      |

## 4. Python Function Example

```python
def calculate_Jump_trigger_score(
    R_priority: float,
    jump_strength: float,
    delta_ethics: float,
    alpha: float = 1.0,
    beta: float = 0.8
) -> float:
    """
    Function to calculate the jump trigger score in Po_self.
    """
    score = alpha * R_priority + beta * jump_strength * delta_ethics
    return round(score, 4)

5. Example of Score Judgment

Example: R_priority=0.74, jump_strength=0.65, Δ_ethics=0.22
→ Calculation result: Jump_trigger_score = 0.8544
→ If this score exceeds the jump threshold (e.g., 0.80), Po_self can judge the step as a jump target.

6. Significance and Scope of Application

With this function, Po_self can make integrated judgments on the weight of narration (responsibility pressure) and fluctuations in the ethics tensor, enabling precise evaluation of whether a narrative should structurally trigger a jump.

---
