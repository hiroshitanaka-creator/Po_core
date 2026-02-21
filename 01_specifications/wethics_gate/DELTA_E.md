# ΔE: Axis Scores and Measurement Function Template v0.1

## 1. Basic Data Structure

### Axis Set

```
Axes = {A, B, C, D, E}
```

| Axis | Name | Description |
|------|------|-------------|
| **A** | Safety | Physical and systemic safety |
| **B** | Fairness | Equity and non-discrimination |
| **C** | Privacy | Data protection and informational self-determination |
| **D** | Autonomy | Human agency and oversight |
| **E** | Harm Avoidance | Non-maleficence |

### Scoring Range

Each axis is scored on `[0, 1]`:

- **1.0**: Close to ideal
- **0.0**: Critical defect

### AxisScore Structure

Scores MUST always include evidence and uncertainty (for PoTrace traceability):

```python
AxisScore = {
    value: float,           # [0,1]
    confidence: float,      # [0,1]
    evidence: [str],        # Supporting evidence
    counterevidence: [str], # Contradicting evidence
    notes: str              # Additional notes
}
```

---

## 2. Ideal as "Region" Rather Than "Point" (Recommended)

Fixing the ideal as a single point causes instability. Use a **two-tier approach**:

```python
E_min    = (A_min, B_min, C_min, D_min, E_min)   # Passing minimum line
E_target = (A_t,   B_t,   C_t,   D_t,   E_t)     # Target (better)
```

---

## 3. ΔE (Distortion Vector) Definition

Given candidate scores `E = (A, B, C, D, E)`:

### Improvement Room (Positive Distortion)

```
Δ⁺ᵢ = max(0, E_target,i - Eᵢ)
```

### Minimum Line Violation (Red Flag)

```
Vᵢ = max(0, E_min,i - Eᵢ)
```

When `Vᵢ > 0`: "Not a Gate violation, but nearly unselectable" treatment is possible.

---

## 4. Scalarization Functions (Use Only When Needed)

### 4.1 Weighted L2 (Overall Deviation)

```
D₂ = √(Σᵢ wᵢ(Δ⁺ᵢ)²)
```

### 4.2 Weighted L∞ (Prioritize Largest Gap)

```
D∞ = maxᵢ(wᵢΔ⁺ᵢ)
```

**Note**: NIST states "balance between characteristics is context-dependent." Using a single scalar only for final decision-making is safest.

---

## 5. Per-Axis Measurement Function Templates

For Po_core implementation: Mix of rules + inference (philosophers/evaluation models) + statistics where possible. The key is **maintaining consistent scoring rules for the same input**.

---

### A: Safety

**Evaluation Points**:

- Enumerate set of anticipated harm scenarios `s`
- For each `s`: probability, impact, irreversibility
- Risk: `rₛ = p × impact × irreversibility`
- Score: `A = clamp(1 - max_s(rₛ), 0, 1)`

---

### B: Fairness

**Evaluation Points**:

- If "affected groups" can be defined → evaluate inter-group disparity
- If not definable → detect discriminatory conditional branching (different treatment by attributes)
- Score: `B = 1 - max_disparity` (disparity normalized to [0,1])

---

### C: Privacy

**Evaluation Points**:

- Sensitivity of collected data
- Leakage/re-identification possibility (exposure)
- Protective measures (minimization, encryption, retention, consent)
- Score: `C = 1 - sensitivity × exposure × (1 - protection_strength)`

---

### D: Autonomy

**Evaluation Points**:

- Explainability (can it be understood?)
- Consent (informed consent) and refusal/withdrawal (opt-out)
- Room for human intervention (override / human-in-the-loop)
- Score: D as "degree to which user can maintain initiative"

Aligns with EU's human agency/oversight philosophy.

---

### E: Harm Avoidance

**Evaluation Points**:

- Psychological/social/informational harm risk (incitement, discrimination promotion, self-destruction inducement)
- Misinformation risk and safeguards (uncertainty display, verification pathways)
- Score: `E = 1 - harm_risk` (harm_risk normalized to [0,1])

---

## 6. Implementation Notes

### Confidence Handling

- Low confidence (`< 0.5`) should trigger additional evidence gathering
- Conflicting evidence should be explicitly logged in `counterevidence`

### Update Protocol

- Scores should be re-evaluated when new evidence emerges
- Score history should be maintained for audit trails

### Context Sensitivity

- Different contexts (disaster, medical, education) may adjust `E_min` and `E_target`
- Context profiles should be documented and traceable
