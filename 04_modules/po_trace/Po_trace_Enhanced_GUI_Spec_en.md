# **Po_trace Enhanced GUI Specification**

## **1. Overview**

This specification proposes enhancements that make the Po_trace structure of the Po_core system visible and operable on a GUI. In particular, it introduces three new tensors indicating reactivation of ungerminated tensors—W_conatus_trace, emotion_shadow_curve, and reactivation_urge_score—and surfaces them in the interface.

## **2. GUI Element Definitions**

| GUI Element | Tensor | Representation | Color / Visual Expression |
| :---- | :---- | :---- | :---- |
| Reactivation Potential | reactivation_urge_score | Opacity or red intensity | Red: strong / Gray: weak |
| Emotional Memory Curve | emotion_shadow_curve | Color curve / stripe | Blue: inhibitory affect / Yellow: hopeful affect |
| Self-sustaining Will History | W_conatus_trace | Sparkline or bar graph | Pulsing animation (pulse) |

## **3. Example GUI Layout**

Below is an example extension of a Po_trace Viewer output step display.

┌─────────────────────────────────────┐
│ 🔁 Trace Step: reasoning_1         │
│ ● W_conatus_trace: 0.87            │
│ ● Reactivation Urge: 0.84          │
│ ● Shadow Emotion: (-0.4 / 0.7)     │
│ 🔥 Heatmap Color: Deep Red         │
│ 🧭 Comment: “A meaning that still wanted to speak” │
└─────────────────────────────────────┘

## **4. Implementation Notes**

- emotion_shadow_curve is time-dependent; render with time-series vector processing.
- W_conatus_trace and reactivation_urge_score are recommended for visual prominence control.
- Integrate with Po_self_seedling to surface candidates for self-evolution.
