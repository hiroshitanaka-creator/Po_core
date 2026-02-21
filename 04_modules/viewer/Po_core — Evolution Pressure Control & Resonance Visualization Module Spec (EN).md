# **Po_core — Evolution Pressure Control & Resonance Visualization Module Spec**

## **1. Overview**

Three new modules enhance recording/analysis/control of meaning evolution and user resonance. They refine Po_trace jump structures, meaning pressure, and resonance, improving coordination with Po_self reconstruction, Po_feedback, and Po_trace visualization.

## **2. Modules & Goals**

| Module | Function | Purpose |
| :-- | :-- | :-- |
| `semantic_delta_threshold` | Exclude steps below a jump-strength threshold from `C_Φ^jump` chains | Improve precision and jump reliability |
| `Po_core_pressure_map` | Heat-map `priority_score × alert_level` | Composite evaluation of meaning pressure × action pressure |
| `feedback-influenced_trace_ordering` | Reorder Po_trace by high resonance (🟢) | Present evolution history prioritized by empathy |

## **3. Details**

### 3.1 `semantic_delta_threshold`

If `C_Φ^jump.strength` < threshold (e.g., 0.2), exclude the step from `jump_map` and network visualizations (`trace_jump_linkage`). Removes low-meaning jumps as noise.

### 3.2 `Po_core_pressure_map`

Multiply `priority_score` and `alert_level` per step to show “total pressure” as a heatmap/bar chart. Explains Po_self reconstruction priority and risk.

### 3.3 `feedback-influenced_trace_ordering`

Sort Po_trace by `Po_feedback.confidence` (🟢=+0.12, 🟠=+0.05, 🔴=+0.00). Optionally reflect the order in Po_self reconstruction.
