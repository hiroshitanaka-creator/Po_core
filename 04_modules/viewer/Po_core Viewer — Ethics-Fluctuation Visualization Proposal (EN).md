# **Po_core Viewer — Ethics-Fluctuation Visualization Proposal**

## **1. Overview**
This proposal defines a UI structure for visualizing an `ethics_fluctuation_score` in Po_core Viewer so that users can intuitively compare the stability/instability of ethical judgments across jump series.

## **2. Labels & Color Classes**
| Score Range | Label | Color | Interpretation |
| :-- | :-- | :-- | :-- |
| < 0.03 | 🟢 Stable | Green | Ethical judgment stayed consistent |
| 0.03 – 0.07 | 🟡 Moderate | Yellow | Some switching in judgment was observed |
| > 0.07 | 🔴 Unstable | Red | Ethical judgment wavered; strong indecision |

## **3. Example — Series Card**
```
┌────────────────────────────┐
│ JCX_014  │ 🔴 ethics_fluctuation_score: 0.084
│ tag: semantic_surge_chain
│ avg_Δ_ethics: -0.12
│ profile_tag: divergence-drift
└────────────────────────────┘
```
Bar-style visual:
```
[■■■■■■■■■■■-----] 0.084
```

## **4. Filters / Comparison / Emphasis**
- filter: `ethics_fluctuation > 0.07` → show only unstable series  
- compare: `JCX_012` vs `JCX_014` → side-by-side view of stable vs. unstable  
- overlay: `fluctuation_heatband` → red–blue gradient on the timeline

## **5. Future Extensions**
- Auto tags from `ethics_fluctuation_score` (e.g., `ethics_drift_chain`)  
- Visualize drift direction as vectors (↕︎, ↔︎)  
- Integrate with other tensor scalars such as `semantic_fluctuation_score`
