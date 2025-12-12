# Po_viewer Visualization Guide

**Advanced visualization capabilities for Po_core philosophical reasoning**

🎨 Transform philosophical reasoning into beautiful, insightful visualizations

---

## Table of Contents

- [Overview](#overview)
- [Visualization Types](#visualization-types)
- [Quick Start](#quick-start)
- [CLI Usage](#cli-usage)
- [Python API](#python-api)
- [Examples](#examples)
- [Customization](#customization)
- [Export Formats](#export-formats)
- [Troubleshooting](#troubleshooting)

---

## Overview

Po_viewer provides comprehensive visualization tools to understand and explore philosophical reasoning:

- **Tension Maps**: Heatmap visualization of philosophical tensions
- **Metrics Timeline**: Track reasoning evolution across sessions
- **Network Graphs**: Philosopher interaction networks
- **Interactive Dashboards**: Multi-view comprehensive analysis

### Key Features

✨ **Beautiful**: Professional, publication-ready visualizations
📊 **Insightful**: Reveals patterns in philosophical reasoning
🎯 **Interactive**: Explore with Plotly's interactive dashboards
💾 **Exportable**: PNG, SVG, PDF, and HTML formats
🚀 **Easy to Use**: Simple CLI and Python API

---

## Visualization Types

### 1. Tension Map (Heatmap)

**What it shows**: Philosophical tensions across three key metrics for all philosophers in a session.

**Metrics visualized**:
- **Freedom Pressure**: Responsibility weight of reasoning
- **Semantic Delta**: Meaning evolution
- **Blocked Tensor**: What was not said (trace)

**Use cases**:
- Compare philosopher contributions
- Identify dominant philosophical perspectives
- Understand tension distribution

**Format**: PNG, SVG, PDF

![Tension Map Example](../examples/screenshots/tension_map_example.png)

### 2. Metrics Timeline

**What it shows**: How philosophical metrics evolve across multiple sessions.

**Features**:
- Track multiple sessions simultaneously
- Interactive hover details
- Trend analysis
- Session comparison

**Use cases**:
- Monitor reasoning consistency
- Detect anomalies
- Study long-term patterns

**Format**: HTML (interactive), PNG, SVG

### 3. Philosopher Network Graph

**What it shows**: Relationships between philosophers based on tension field interactions.

**Node features**:
- **Size**: Proportional to Freedom Pressure + Semantic Delta
- **Color**: Unique color per philosopher
- **Position**: Similarity-based layout

**Edge features**:
- **Width**: Philosophical similarity strength
- **Presence**: Only shown if similarity > 30%

**Use cases**:
- Discover philosophical alliances
- Identify complementary perspectives
- Understand interaction patterns

**Format**: PNG, SVG, PDF

### 4. Interactive Dashboard

**What it shows**: Comprehensive multi-view analysis combining:
- Tension metrics bar chart
- Freedom pressure distribution (box plot)
- Semantic vs Freedom pressure scatter plot
- Philosopher contribution pie chart

**Features**:
- Fully interactive (zoom, pan, hover)
- Integrated views
- Professional layout

**Use cases**:
- Comprehensive session analysis
- Presentation and reporting
- Deep exploration

**Format**: HTML (interactive), PNG

---

## Quick Start

### Using the Demo Script

The fastest way to see all visualizations:

```bash
python examples/visualization_demo.py
```

This will:
1. Generate 3 philosophical reasoning sessions
2. Create all visualization types
3. Export to `./visualization_outputs/`
4. Show CLI usage examples

### Using CLI Commands

```bash
# View available sessions
po-viewer sessions

# Generate tension map
po-viewer tension-map <session_id> -o tension.png

# Generate network graph
po-viewer network <session_id> -o network.png

# Generate interactive dashboard
po-viewer viz-dashboard <session_id> -o dashboard.html

# Export all visualizations
po-viewer export-all <session_id> -d ./my_visualizations
```

---

## CLI Usage

### Available Commands

#### `po-viewer tension-map`

Generate tension map heatmap visualization.

```bash
po-viewer tension-map <session_id> [OPTIONS]

Options:
  -o, --output PATH        Output file path
  -f, --format [png|svg|pdf]  Output format (default: png)

Examples:
  po-viewer tension-map abc123def456 -o tension.png
  po-viewer tension-map abc123def456 -o tension.svg -f svg
```

#### `po-viewer timeline`

Generate metrics timeline across multiple sessions.

```bash
po-viewer timeline <session_id1> <session_id2> ... [OPTIONS]

Options:
  -o, --output PATH           Output file path
  -f, --format [html|png|svg] Output format (default: html)
  -t, --title TEXT            Custom plot title

Examples:
  po-viewer timeline abc123 def456 ghi789 -o timeline.html
  po-viewer timeline abc123 def456 -t "My Analysis" -o timeline.html
```

#### `po-viewer network`

Generate philosopher interaction network graph.

```bash
po-viewer network <session_id> [OPTIONS]

Options:
  -o, --output PATH        Output file path
  -f, --format [png|svg|pdf]  Output format (default: png)

Examples:
  po-viewer network abc123def456 -o network.png
  po-viewer network abc123def456 -o network.pdf -f pdf
```

#### `po-viewer viz-dashboard`

Generate comprehensive interactive dashboard.

```bash
po-viewer viz-dashboard <session_id> [OPTIONS]

Options:
  -o, --output PATH      Output file path
  -f, --format [html|png]   Output format (default: html)

Examples:
  po-viewer viz-dashboard abc123def456 -o dashboard.html
  po-viewer viz-dashboard abc123def456 -o dashboard.png -f png
```

#### `po-viewer export-all`

Export all visualizations for a session.

```bash
po-viewer export-all <session_id> [OPTIONS]

Options:
  -d, --output-dir PATH         Output directory (default: ./visualizations)
  -f, --formats [png|svg|html]  Output formats (can specify multiple)

Examples:
  po-viewer export-all abc123def456 -d ./output
  po-viewer export-all abc123def456 -f png -f html -f svg
```

---

## Python API

### Basic Usage

```python
from po_core.po_self import PoSelf
from po_core.visualizations import PoVisualizer
from pathlib import Path

# Generate philosophical reasoning
po_self = PoSelf(enable_trace=True)
result = po_self.generate("What is freedom?")
session_id = result.log["session_id"]

# Create visualizer
visualizer = PoVisualizer(po_trace=po_self.po_trace)

# Generate visualizations
visualizer.create_tension_map(
    session_id=session_id,
    output_path=Path("tension.png")
)

visualizer.create_philosopher_network(
    session_id=session_id,
    output_path=Path("network.png")
)

visualizer.create_comprehensive_dashboard(
    session_id=session_id,
    output_path=Path("dashboard.html")
)
```

### Advanced: Multiple Sessions Timeline

```python
# Generate multiple sessions
session_ids = []
for prompt in prompts:
    result = po_self.generate(prompt)
    session_ids.append(result.log["session_id"])

# Create timeline
visualizer.create_metrics_timeline(
    session_ids=session_ids,
    output_path=Path("timeline.html"),
    title="Reasoning Evolution"
)
```

### Batch Export

```python
# Export all visualizations at once
results = visualizer.export_session_visualizations(
    session_id=session_id,
    output_dir=Path("./visualizations"),
    formats=['png', 'svg', 'html']
)

# Results is a dict mapping viz name to file path
for name, path in results.items():
    print(f"{name}: {path}")
```

---

## Examples

### Example 1: Quick Tension Analysis

```bash
# Generate reasoning
po-core prompt "What is justice?" -p aristotle,nietzsche,levinas

# Get session ID from output, then visualize
po-viewer tension-map <session_id> -o justice_tension.png
```

### Example 2: Multi-Session Comparison

```python
from po_core.po_self import PoSelf
from po_core.visualizations import PoVisualizer

po_self = PoSelf(enable_trace=True)

# Generate multiple sessions
questions = [
    "What is truth?",
    "What is beauty?",
    "What is goodness?"
]

session_ids = []
for question in questions:
    result = po_self.generate(question)
    session_ids.append(result.log["session_id"])

# Create timeline
visualizer = PoVisualizer(po_trace=po_self.po_trace)
visualizer.create_metrics_timeline(
    session_ids=session_ids,
    output_path="evolution.html",
    title="Transcendental Trilogy"
)
```

### Example 3: Research Export

```bash
# Export complete visualization suite for research
po-viewer export-all <session_id> \
  -d ./research_outputs/session_001 \
  -f png -f svg -f html
```

---

## Customization

### Figure Size

```python
# Larger tension map
visualizer.create_tension_map(
    session_id=session_id,
    output_path=Path("tension_large.png"),
    figsize=(16, 12)  # width, height in inches
)

# Larger network
visualizer.create_philosopher_network(
    session_id=session_id,
    output_path=Path("network_large.png"),
    figsize=(20, 15)
)
```

### Color Schemes

Modify the color scheme by subclassing `PoVisualizer`:

```python
class CustomVisualizer(PoVisualizer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override philosopher colors
        self.philosopher_colors['aristotle'] = '#FF0000'
        self.philosopher_colors['nietzsche'] = '#00FF00'
```

---

## Export Formats

### Static Formats

**PNG** - Best for:
- Presentations
- Documents
- Quick sharing
- Default choice

**SVG** - Best for:
- Publications
- Scalable graphics
- Professional printing
- Editing in design tools

**PDF** - Best for:
- Academic papers
- Reports
- Archival

### Interactive Formats

**HTML** - Best for:
- Exploration
- Interactive analysis
- Web embedding
- Presentations with zoom/pan

---

## Troubleshooting

### Issue: "Session not found"

**Solution**: Verify session ID exists:
```bash
po-viewer sessions
```

### Issue: "No philosopher data found"

**Cause**: Session has no philosopher events logged.

**Solution**: Ensure tracing is enabled:
```python
po_self = PoSelf(enable_trace=True)
```

### Issue: Matplotlib/Plotly not found

**Solution**: Install visualization dependencies:
```bash
pip install matplotlib plotly networkx
# or
pip install -e ".[viz]"
```

### Issue: "Need at least 2 philosophers for network graph"

**Cause**: Only one philosopher participated in session.

**Solution**: Use multiple philosophers or skip network visualization:
```bash
po-core prompt "Your question" -p aristotle,nietzsche,sartre
```

### Issue: Interactive HTML not displaying

**Cause**: Browser security restrictions or file corruption.

**Solutions**:
1. Open HTML file directly in browser (not through file:// preview)
2. Use a local web server:
   ```bash
   python -m http.server 8000
   # Then open http://localhost:8000/dashboard.html
   ```
3. Re-generate the visualization

---

## Performance Tips

1. **Batch Processing**: Use `export_all` instead of individual commands
2. **Format Selection**: Use PNG for quick previews, SVG for final outputs
3. **Session Management**: Clean up old sessions to improve load times

---

## Integration with Research Workflow

### Typical Workflow

```bash
# 1. Generate reasoning sessions
po-core prompt "Research question" -p philosopher1,philosopher2,philosopher3

# 2. Export visualizations
po-viewer export-all <session_id> -d ./paper_figures -f svg -f png

# 3. Include in LaTeX/Markdown
\includegraphics{paper_figures/tension_map_abc12345.png}

# 4. Share interactive dashboard
# Upload dashboard_abc12345.html to web server
```

---

## Advanced Topics

### Custom Visualization Pipeline

```python
from po_core.visualizations import PoVisualizer
import matplotlib.pyplot as plt

class ResearchVisualizer(PoVisualizer):
    def create_custom_analysis(self, session_id, output_path):
        """Custom visualization for specific research needs."""
        session = self.po_trace.get_session(session_id)

        # Extract custom metrics
        # ... your analysis code ...

        # Create custom plot
        fig, ax = plt.subplots(figsize=(12, 8))
        # ... your plotting code ...

        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
```

---

## Gallery

See [examples/visualization_outputs/](../examples/visualization_outputs/) for example visualizations.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/hiroshitanaka-creator/Po_core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions)
- **Email**: flyingpig0229+github@gmail.com

---

**🐷🎈 Making philosophical reasoning visible, one pig at a time.**

*"A frog in a well may not know the ocean, but it can know the sky."*
