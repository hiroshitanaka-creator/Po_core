# **Viewer — Module README**

Stores design docs for visualization of reasoning processes and the user interface.

## Overview

Po_core Viewer visualizes complex philosophical reasoning so users can grasp it intuitively.

## Key Features

### Basic Viewer (v0.3)

- Show reasoning chains
- Per-step navigation
- Basic interactions

### Evolved Viewer (v2)

- Advanced visualization
- Real-time updates
- Customizable views

### Special Visualizations

- **Ethics fluctuation**: visualize ethical dilemmas
- **Pressure analysis**: visualize `freedom_pressure_tensor`
- **Self-narration structure**: show Po_self structures

## Visualization Types

- **Graphs:** chain flows, philosopher influence, tensor-space projections
- **Heatmaps:** pressure fields, philosophical weights, confidence
- **Timelines:** event order, durations
- **3D:** multi-dimensional tensors, interactive exploration

## External Integration

- **LangChain:** agent visualization, chain tracing, patterns
- **vLLM:** connection, inference display, performance metrics

## Interface Design

- Responsive layouts (desktop/tablet/mobile)
- Usability: intuitive ops, shortcuts, accessibility
- Customization: themes, layouts, visible fields

## Document Structure

- Connection guides, specs (v0.3 / v2), design docs

## Update Flow

```
Run inference → Event → Viewer notified → Data fetch → Visualization update → Display
```

## Distinctive Traits

- Real-time updates
- Multi-layer views
- Interactive exploration

## Notes

- Performance: large graph rendering, virtual scroll, lazy rendering
- Browser compatibility: modern browsers, WebGL fallback
- Data volume: downsampling, dynamic detail, summary views

## Future

- VR/AR, collaboration, custom view plugins
