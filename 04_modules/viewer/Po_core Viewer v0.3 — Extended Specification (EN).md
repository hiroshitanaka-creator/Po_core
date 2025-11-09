# **Po_core Viewer v0.3 — Extended Specification**

## **1. Overview**

This document specifies new extension modules for Po_core Viewer v0.3 to visualize, analyze, and control semantic evolution via Po_trace. Three enhancements are integrated.

## **2. Extension List**

| Extension | Purpose | Core Tensors |
| :---- | :---- | :---- |
| Hierarchical view of Po_trace chain graph | Visualize the network structure of meaning jumps | `C_Φ^jump`, `semantic_delta` |
| `feedback_badge` priority adjustment | Modify reconstruction priority by resonance | `Po_feedback.confidence`, `priority_score` |
| `impact_summary` history analyzer | Heatmap the global bias of Po_core | `impact_field_tensor` |

## **3. Details**

### **3.1 Chain Graph (Hierarchical)**

Render the relational network centered on `C_Φ^jump`. Nodes = Po_trace steps; edges = jump strength (`jump_strength`). Node color encodes `impact_axis` (factual/causal/emotional); time hierarchy reveals directional flow.

### **3.2 Priority Adjustment via `feedback_badge`**

Use 🟢🟠🔴 badges based on `Po_feedback.confidence` to auto-adjust `priority_score` (e.g., 🟢=+0.12, 🟠=+0.05, 🔴=+0.00). User resonance directly shapes Po_self reconstruction behavior.

### **3.3 `impact_summary` History Analyzer**

Aggregate the distribution of `impact_field_tensor` across all steps; render a heatmap by time or Po_ID to grasp systemic drift along factual/causal/emotional axes.

## **4. Implementation Hints**

- Chain graph: D3.js or Plotly for interactive networks.  
- Badge adjustment: rule-based weighting in Python.  
- Heatmap: matplotlib for plotting.
