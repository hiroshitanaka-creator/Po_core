# Po_self_seedling GUI Design Specification

## 1. Overview

This specification defines the GUI components and visualization methods for Po_self_seedling (self-sprouting layer) within the Po_core system.  
Po_self_seedling provides an interface that visualizes dormant tensors and reconstruction waiting structures from semantic, emotional, and volitional perspectives, allowing users and developers to intuitively grasp their evolutionary potential.

## 2. GUI Component Definitions

| GUI Component           | Display Tensor             | Visualization Format        | Visual Indicator                              |
| :---------------------- | :------------------------- | :------------------------- | :-------------------------------------------- |
| Seedling Candidate List | Po_self_seedling[]         | Card-style list display    | 🌱 Icon + accent color for "Retrying" display |
| Re-sprout Will Gauge   | S_conatus                  | Gauge / Meter              | Color transition green → yellow → red         |
| Emotion Shadow Heat    | emotion_shadow_curve       | Small curve / stripe       | Visualization of suppressed emotion (blue/yellow) |
| Reevaluation Pressure Timeline | W_conatus_trace    | Time-series bar graph      | Pulse display: Emphasize rising will to re-sprout |

## 3. GUI Structure Image (Pseudo Layout)

┌─────────────────────────────┐
│ 🌱 Seedling Candidate Card: ψ_0921                      │
│ ───────────────────────────   │
│ S_conatus: ▓▓▓▓▓▓▓░░░░░░ 0.73                            │
│ W_conatus_trace: ▇▇▆▇█                                   │
│ emotion_shadow: ░░▚▚▒▒                                 │
│ Comment: "I want to speak again..."                      │
└─────────────────────────────┘


## 4. Operational Guidelines

- Po_self_seedling displays tensors with status=viable, extracted from Po_trace_blocked.
- S_conatus and emotion_shadow_curve are used for visualizing reevaluation pressure, enabling detection of sprouting precursors.
- The user can perform operations such as "Allow Reconstruction" or "Skip" on each candidate, and these GUI actions influence Po_self_recursor.
