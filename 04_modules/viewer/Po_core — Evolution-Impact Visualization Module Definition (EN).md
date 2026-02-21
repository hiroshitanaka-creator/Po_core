# **Po_core — Evolution-Impact Visualization Module Definition**

## **1. Overview**

Defines three extensions that strengthen structural visualization of evolution history, interference history, and decision pressure. Through temporal decay, influence-path recording, and operation-pressure distribution analysis, users can read Po_self reconstruction grounds and Po_trace firing history dynamically.

## **2. Extension List**

| Element | Content | Purpose |
| :-- | :-- | :-- |
| 🕒 Time-decay label | Show that `reason_confidence` is decaying | Make time-varying reconstruction pressure explicit |
| 🔄 Contextual influence path | Record interference history of what each output reacted to | Clarify causal connections and trace reconstruction routes |
| 🔥 Operation-pressure heatmap | Visualize reasons and pressures recorded in Po_feedback over time | Analyze trends in human intervention and values |

## **3. Details**

### 3.1 🕒 Time-decay Label

When `elapsed_hours > 24` and `decay_factor < 0.9`, display “🕒 Confidence Decaying…” on the Po_trace card.

### 3.2 🔄 Contextual Influence Path

Record in Po_trace (e.g., `context_link`) which past Po_feedback or reason_log changed direction. Display example: “This output was influenced by a reconstruction request (R03 Insufficient Resonance).”

### 3.3 🔥 Operation-Pressure Heatmap

Aggregate `reason_confidence × user_feedback_level` by time × category and show a heatmap in the Viewer.

## **4. Outlook**

These modules integrate Po_trace / Po_self / Po_feedback across time/meaning/ethics to expose the *reasons for structural change* and the *dynamic record of coevolution with humans*.
