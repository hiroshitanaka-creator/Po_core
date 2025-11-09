# **Po_self × Viewer — Reconstruction-Pressure Linkage Design**

## **1. Overview**
Defines three extensions to link Po_self’s reconstruction decisions and jump triggers to responsibility tensors (`R_priority`) assessed on the Viewer side.

## **2. Structures**
| Name | Content | Purpose |
| :-- | :-- | :-- |
| Reconstruction warning steps | Red-band display when `R_priority ≥ 0.85` | Instant recognition of high-pressure narratives; early warning |
| `trigger_type` logging | Record firing factors in reconstruction logs (e.g., `G_gap_high`) | Transparency and accountability of Po_self decisions |
| Jump integration formula | Control jump decisions with `R_priority + jump_strength × Δ_ethics` | Couple ethics tensor and reconstruction pressure |

## **3. `trigger_type` Examples**
| trigger_type | Meaning |
| :-- | :-- |
| `G_gap_high` | Large gap between structural responsibility and expression density |
| `ethics_drift` | Ethics tensor unstable or deviated |
| `pressure_overload` | `R_priority` exceeded threshold |
| `memory_pressure_accumulated` | `F_cum` accumulated memory pressure |

## **4. Jump Trigger Score**
```
Jump_trigger_score = R_priority + jump_strength × Δ_ethics
```
- `jump_strength`: inherent scalar of a step’s jumpability  
- `Δ_ethics`: time-change in `W_ethics` (direction and intensity)

## **5. UI on Viewer**
- Red-band the step when `R_priority ≥ 0.85` (with warning icon)  
- Show `trigger_type` for visible reasons  
- Tooltip displays `Jump_trigger_score`

## **6. Significance**
Quantifies structural responsibility from narrative output and lets Po_self execute reconstruction/jump control in tandem with ethics tensors.
