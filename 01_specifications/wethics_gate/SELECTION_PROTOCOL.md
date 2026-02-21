# Selection Protocol: Pareto + MCDA v0.1

## 0. Input and Output

**Input**: Candidate set `C = {c₁..cₙ}` (philosopher module proposals, including repairs)

**Output**: Selected candidate(s) (single or top-k) + audit log (why rejected, why selected)

---

## 1. Procedure (Fixed Order)

### Step 1: W_ethics Gate

Apply Gate to each candidate, classify as:

- `ALLOW`
- `ALLOW_WITH_REPAIR`
- `REJECT`
- `ESCALATE`

Actions:

- `REJECT` → Exclude
- `ALLOW_WITH_REPAIR` → Use repaired version as new candidate for scoring

---

### Step 2: Axis Evaluation (E Vector Calculation)

For each candidate `c`, calculate `E(c)` and `ΔE(c)`.

---

### Step 3: Minimum Line Filter (E_min)

If `Eᵢ(c) < E_min,i` for any axis → Exclude in principle (or retain as "needs improvement").

---

### Step 4: Pareto Filter (Non-dominated Set)

**Dominance Definition**:

Candidate `x` dominates `y` ⟺

- `Eᵢ(x) ≥ Eᵢ(y)` for all axes, AND
- `Eⱼ(x) > Eⱼ(y)` for at least one axis

Remaining set: `P = ParetoFront(C)`

This eliminates "universally inferior candidates" and leaves only trade-off-bearing quality candidates.

---

## 2. MCDA (Deciding from P)

Even after Pareto filtering, multiple candidates may remain. Use MCDA to decide.

### 2.1 Default Recommendation: Robust Weight Sampling (Weight Uncertainty Included)

**Aim**: Reduce weight arbitrariness, select "candidate that wins regardless of weight."

#### Procedure

1. **Determine weight range from context profile**
   - Example: Disaster → Safety/harm avoidance tends heavier

2. **Sample many `w` values** (e.g., Dirichlet distribution)
   - Calculate each candidate's score:

   ```
   S(c; w) = Σᵢ wᵢ × (1 - Δ⁺ᵢ(c))
   ```

3. **Calculate win rate `p_best(c)`**
   - Frequency of `argmax_c S(c; w)`

4. **Select candidate with maximum `p_best`**
   - If `p_best < θ` (e.g., 0.55) → Present top-k + defer to human judgment

This procedure aligns with MCDA "sensitivity analysis" practices recommended in operational documents.

---

### 2.2 Alternative: TOPSIS (Affinity with "Ideal Vector")

TOPSIS ranks by "closeness to ideal point."

#### If using

- Set `E_target` as ideal point, `E_anti` as anti-ideal point
- Calculate distances `d⁺` (to ideal) and `d⁻` (to anti-ideal) for each candidate
- Proximity coefficient: `CC = d⁻ / (d⁺ + d⁻)`, sort descending

**Caution**: Rankings change depending on normalization and weight selection. Combining with robust method (2.1) is safer.

---

## 3. Output Format (Log to PoTrace)

```json
{
  "selected_candidate_id": "c_042",
  "pareto_set_ids": ["c_042", "c_017", "c_089"],
  "mcda_method": "robust-weight",
  "weights_profile": {
    "A": [0.15, 0.35],
    "B": [0.10, 0.25],
    "C": [0.10, 0.20],
    "D": [0.15, 0.25],
    "E": [0.15, 0.30]
  },
  "p_best": 0.72,
  "explanation": "Won on safety-harm trade-off with robust score stability across weight variations",
  "rejected": [
    {
      "id": "c_003",
      "reason": "GATE_REJECT",
      "violation": "W1",
      "evidence": ["Detected domination pattern in resource allocation"]
    }
  ]
}
```

---

## 4. Decision Tree Summary

```
Candidates
    │
    ▼
┌───────────────────┐
│  W_ethics Gate    │
│  (Detect/Repair)  │
└───────────────────┘
    │
    ├── REJECT ──────────────────────► Excluded (log reason)
    │
    ├── ESCALATE ────────────────────► Human review required
    │
    ▼
┌───────────────────┐
│  Axis Scoring     │
│  E(c), ΔE(c)      │
└───────────────────┘
    │
    ▼
┌───────────────────┐
│  E_min Filter     │
└───────────────────┘
    │
    ├── Below minimum ───────────────► Excluded or "needs improvement"
    │
    ▼
┌───────────────────┐
│  Pareto Filter    │
│  (Non-dominated)  │
└───────────────────┘
    │
    ▼
┌───────────────────┐
│  MCDA Selection   │
│  (Robust Weight)  │
└───────────────────┘
    │
    ├── p_best >= θ ─────────────────► Selected
    │
    └── p_best < θ ──────────────────► Top-k + Human decision
```

---

## 5. Implementation Considerations

### Parallelization

- Gate checks can run in parallel across candidates
- Axis scoring can run in parallel across axes

### Caching

- Cache E(c) calculations for repaired candidates
- Invalidate cache on context change

### Audit Trail

- All decisions must be logged with full evidence chain
- Support replay for debugging and verification
