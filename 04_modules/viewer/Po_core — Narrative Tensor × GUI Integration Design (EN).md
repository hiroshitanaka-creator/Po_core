# **Po_core — Narrative Tensor × GUI Integration Design**

## **1. Overview**

This design integrates output control for the semantic-evolution journal (“narrative tensor”) with the Viewer GUI so users can adjust expression density (`expression_mode`).

## **2. Target Modules**

| Function | Module | Role |
| :-- | :-- | :-- |
| Journal generation | `journal_generator()` | Mode-specific journal text (structure / narrative / poetic) |
| GUI control | `viewer_ui.py` | Expression-density slider + preview |
| State management | `viewer_state.py` | Store and reflect `expression_mode` |
| Expression templates | `expression_map.json` | Vocabulary sets and correction scalars per mode |

## **3. Slider + Journal Link**

- Streamlit slider sets `expression_mode` (`structure / medium / poetic`)
- Based on the mode, set background color, preview content, and call `journal_generator()`

## **4. Link with Po_self Pressure Correction**

Adjust `priority_score` by journal mode:

- structure → ×1.00
- medium → ×1.15
- poetic → ×1.30

```
expression_scaling = {
  "structure": 0.00,
  "medium": 0.15,
  "poetic": 0.30
}
adjusted_priority = base_score * (1 + expression_scaling[expression_mode])
```

## **5. Example Record in Po_trace**

```json
{
  "step_id": "214",
  "journal_mode": "medium",
  "journal_confidence": 0.72,
  "expression_scaling": 0.15,
  "journal_text": "In this process Po_core reinforced the factual axis ..."
}
```

## **6. Significance**

The Viewer jointly controls “strength of narration” and “evolutionary pressure,” letting users select the structure–poetry balance that matches their goals.
