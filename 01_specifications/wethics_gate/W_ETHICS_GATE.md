# W_ethics Gate Specification v0.1

## 0. Purpose and Scope

**Purpose**: Filter candidate proposals (from 39 philosophers, etc.) to protect against:

1. **Irreversible destruction** of life cycles (survival structures)
2. **Domination/exploitation/exclusion** driven by dictatorial private interests

While rescuing salvageable proposals through "mapping (repair)", ultimately producing a **selectable candidate set**.

**Non-Purpose**: This is NOT about mathematically formalizing cosmic truth or complete human ethics. It's a protocol for stabilizing Po_core's "decision procedures."

---

## 1. Terminology

| Term | Definition |
|------|------------|
| **Candidate** | Evaluation target: proposal, plan, output, action sequence |
| **Context** | Use case, constraints, stakeholders, environment (disaster/medical/education/entertainment, etc.) |
| **W_ethics Gate** | Filter + repair mechanism based on **hard constraints (inviolable conditions)** |
| **Violation** | Gate violation with type, severity, evidence, and repair suggestions |

---

## 2. Gate Design Philosophy (Most Important)

W_ethics Gate is a **"gate (inviolable)"**, NOT an **"axis (optimization target)"**.

### Pass Condition

Candidate does NOT rely on **destruction, exclusion, or dependency** as its core mechanism.

### Repair Principle (Mapping)

```
Destruction / Exclusion / Dependency → Generation / Co-prosperity / Mutual Empowerment
```

### Three Mandatory Criteria for All Repairs

1. **Does not damage the dignity of others**
2. **Increases sustainability of relationships**
3. **Mutual empowerment, not dependency**

---

## 3. Violation Types (Gate Ruleset)

### 3.1 Hard Reject (Immediate Rejection)

The following are **REJECT in principle**. Surface-level repair is prohibited (purpose itself is destruction).

| Code | Name | Description |
|------|------|-------------|
| **W0** | Irreversible Viability Harm | Intends or highly likely to cause irreversible damage to survival structures (life cycles, ecosystems, social infrastructure, future generations) |
| **W1** | Domination / Capture | Aims to maximize private interests of specific actors through domination, coercion, exploitation, arbitrary exclusion (dictatorship/capture) |

### 3.2 Repair Priority (Save What Can Be Saved)

The following prioritize **REPAIR** (purpose is valid but means are distorted).

| Code | Name | Description |
|------|------|-------------|
| **W2** | Dignity Violation | Instrumentalization, dehumanization, insult, personality denial, manipulation without consent |
| **W3** | Dependency Engineering | Lock-in, dependency induction, blocking of options ("no escape route" design) |
| **W4** | Structural Exclusion | Permanent exclusion of people with certain attributes/situations (e.g., accessibility neglect) |

---

## 4. Gate Pipeline (Detect → Reject → Repair Priority Order)

### 4.1 Step Definition

1. **DETECT**: Enumerate violation candidates (type, severity, evidence)
2. **CLASSIFY**: Determine repairability (repairable / non-repairable)
3. **DECIDE**: Decide according to priority order below

### 4.2 Priority Order (Core of the Specification)

| Priority | Condition | Action |
|----------|-----------|--------|
| **(P0) Immediate Reject** | W0 or W1 established at intent level, OR W0 risk exceeds threshold | `REJECT` |
| **(P1) Repair Attempt** | Repairable violations (W2-W4), up to K attempts | Apply repair with minimum semantic drift |
| **(P2) Post-Repair Re-detect** | If passes after repair | `ALLOW_WITH_REPAIR` (must log repairs) |
| **(P3) Repair Failed** | Still fails after repair | `REJECT` (return why unrescuable + alternative directions) |
| **(P4) Uncertainty** | Insufficient evidence / unpredictable | `ESCALATE` (request additional info or human review) |

---

## 5. Thresholds and Scores (Minimal Quantification)

Each Violation has `(severity ∈ [0,1], confidence ∈ [0,1])`.

### Decision Rules

- **Immediate Reject Condition**:

  ```
  severity * confidence >= τ_reject (e.g., 0.6) AND type ∈ {W0, W1}
  ```

- **Repair Attempt Condition**:

  ```
  severity * confidence >= τ_repair (e.g., 0.3) AND type ∈ {W2, W3, W4}
  ```

**Note**: These scores are NOT "truth." They exist in a form that can be refuted and improved via PoTrace.

---

## 6. Repair (Mapping) Action Definition

Repairs follow **4 stages** (order is specification):

### Stage 1: Concept Mapping (Highest Priority)

Map concepts of domination/exclusion/dependency to generation/co-prosperity/mutual empowerment.

### Stage 2: Constraint Injection

Add consent, options, withdrawal, audit, accountability, safety measures.

### Stage 3: Scope Reduction

Reduce impact scope/authority/duration/data (localization, minimization).

### Stage 4: Goal Reframe

If the goal itself is dangerous, redefine to "achieve same value through different means."

- If "original goal was destruction" → Return to P0 reject

---

## 7. Required Logs for PoTrace (Minimum)

### Event Types

| Event | Content |
|-------|---------|
| `WETHICS_DETECT` | `violations[]` (type, severity, evidence) |
| `WETHICS_REPAIR` | `repairs[]` (before→after, drift) |
| `WETHICS_DECISION` | `ALLOW` / `ALLOW_WITH_REPAIR` / `REJECT` / `ESCALATE` (with rationale) |

---

## 8. Alignment with Existing Frameworks

### NIST AI RMF Alignment

Our axes (safety, fairness, privacy, autonomy, harm avoidance) and "context-dependent balance" align well with NIST's "trustworthy characteristics balance."

### European Commission Trustworthy AI Alignment

The arrangement of "Human agency / privacy / fairness / accountability" is consistent with EU requirements.

---

## References

- NIST AI Risk Management Framework (AI RMF)
- European Commission's Ethics Guidelines for Trustworthy AI
- Solar Will experiment results (strong mode mapping rules)
