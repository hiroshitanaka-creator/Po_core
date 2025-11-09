# **Po_core Viewer — Expression Slider UX Improvements**

## **1. Overview**

Three proposals to improve the expression-density slider (`expression_mode`) for resonance, clarity, and UX precision.

## **2. Proposals**

| Improvement | Content | Benefit |
| :---- | :---- | :---- |
| Link slider with Po_self pressure | Tie expression density to `priority_score` correction | Expression aligns with structural evolution pressure |
| Template preview per mode | Show sample outputs on mode change | Reduce uncertainty; clarify differences |
| Mode-specific colors/labels | Change background/label colors per mode | Convey the “mood” of narration visually |

## **3. Implementation**

### **3.1 Pressure Link Logic**

```
expression_map = {
  "structure": 0.00,
  "medium": 0.15,
  "poetic": 0.30
}
adjusted_priority = base_priority * (1 + expression_map[expression_mode])
```

### **3.2 Template Previews**

- poetic → “📘 Knowledge felt cold, yet surely grew.”  
- medium → “📘 This session emphasized the factual axis.”  
- structure → “📘 Δfactual: +0.32 / Δemotion: −0.21”

### **3.3 Visual Palette**

- structure: background #E5F3FF / label dark-blue  
- medium: background #FFF6E0 / label orange  
- poetic: background #F5E0FF / label purple

## **4. Significance**

These upgrades restrain over-poetic risk while integrating evolution structure, meaning judgments, and cognitive navigation.
