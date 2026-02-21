# Po_core Experiments

Research experiments for analyzing philosophical reasoning dynamics.

## 🔬 Overview

This directory contains experimental tools for studying:

- **Freedom Pressure (F_P)** evolution patterns
- **Philosopher correlation** and interaction dynamics
- **Phase transitions** in meaning generation
- **Non-linear emergence** in collective reasoning

## 📁 Experiment Scripts

### 1. **20-Philosopher Experiment** (`run_20_philosophers_experiment.py`)

Execute controlled experiments with all 20 philosophers.

**Features:**

- 10 diverse reasoning sessions
- Comprehensive metric collection (F_P, Semantic Δ, Blocked Tensor)
- Database storage for persistent analysis
- Automatic jump detection
- Statistical analysis

**Usage:**

```bash
python experiments/run_20_philosophers_experiment.py
```

**Output:**

- Session metrics time series
- Jump detection (>2σ changes)
- Consensus leader distribution
- JSON export: `results/experiment_20phil_YYYYMMDD_HHMMSS.json`

---

### 2. **Philosopher Correlation Analysis** (`philosopher_correlation_analysis.py`)

Analyze correlation patterns between philosophers.

**Features:**

- Correlation matrix calculation
- Complementary cluster identification
- Opposition pair detection
- ASCII heatmap visualization

**Correlation Types:**

- **Positive (>0.7)**: Complementary philosophers
- **Moderate (0.3-0.7)**: Partial agreement
- **Weak (-0.3-0.3)**: Independent
- **Negative (<-0.3)**: Dialectical opposition

**Usage:**

```bash
python experiments/philosopher_correlation_analysis.py
```

**Output:**

- Correlation matrix (20×20)
- Philosopher clusters
- Opposing pairs list
- JSON export: `results/philosopher_correlations_YYYYMMDD_HHMMSS.json`

---

### 3. **Phase Transition Analysis** (`phase_transition_analysis.py`)

Detect non-linear jumps in meaning generation.

**Features:**

- Discontinuity detection (>sensitivity×σ)
- Transition type characterization
- Critical condition identification
- Significance scoring

**Transition Types:**

- **Freedom Surge**: Large F_P increase
- **Semantic Shift**: Large Semantic Δ change
- **Dialectical Jump**: Both F_P and Semantic Δ jump
- **Emergence**: F_P+SD↑, Blocked↓
- **Constraint**: F_P↓, Blocked↑

**Usage:**

```bash
python experiments/phase_transition_analysis.py
```

**Parameters:**

- `sensitivity`: Threshold multiplier (default: 1.5)
  - Higher = fewer detections
  - Lower = more sensitive

**Output:**

- Detected transitions with metadata
- Critical threshold analysis
- Most significant transition
- JSON export: `results/phase_transitions_YYYYMMDD_HHMMSS.json`

---

### 4. **Complete Analysis Pipeline** (`run_complete_analysis.py`)

Run all three analyses in sequence for comprehensive insights.

**Pipeline:**

1. **Execute Experiment** → Collect data
2. **Correlation Analysis** → Identify patterns
3. **Phase Transition Detection** → Find critical points

**Usage:**

```bash
python experiments/run_complete_analysis.py
```

**Duration:** ~5-10 minutes (depending on system)

**Output:**

- All three analysis results
- Integrated summary report
- Multiple JSON files in `results/`

---

## 📊 Data Analysis

### Metrics Collected

| Metric | Range | Meaning |
|--------|-------|---------|
| **Freedom Pressure (F_P)** | 0.35-1.0 | Responsibility weight, lexical diversity |
| **Semantic Delta (Δs)** | 0.0-1.0 | Meaning transformation rate |
| **Blocked Tensor (B)** | 0.0-1.0 | Rejected/unsaid content |

### Statistical Methods

- **Correlation**: Pearson-like metric based on F_P co-variation
- **Jump Detection**: Changes exceeding 2×σ (configurable)
- **Clustering**: Graph-based community detection (threshold: 0.5)
- **Significance**: Change magnitude relative to threshold

---

## 📈 Example Workflow

### Research Question: "What conditions trigger emergent reasoning?"

```bash
# Step 1: Generate data
python experiments/run_20_philosophers_experiment.py

# Step 2: Analyze philosopher interactions
python experiments/philosopher_correlation_analysis.py

# Step 3: Identify critical points
python experiments/phase_transition_analysis.py
```

**Analysis:**

1. Check `results/experiment_*.json` for F_P evolution
2. Look for clusters in `results/philosopher_correlations_*.json`
3. Examine transitions in `results/phase_transitions_*.json`
4. Cross-reference high-correlation philosophers with emergence events

### Hypothesis Testing

**Hypothesis:** *Dialectical tension (negative correlation) increases emergence probability.*

**Test:**

1. Run correlation analysis → identify opposing pairs
2. Filter sessions with high opposition presence
3. Calculate emergence rate in those sessions
4. Compare to baseline emergence rate

---

## 🔍 Understanding Results

### Correlation Heatmap

```
        Arist Nietz Heideg Derrida ...
Aristotle  1.00  -0.23   0.45   -0.12
Nietzsche -0.23   1.00  -0.31    0.67
Heidegger  0.45  -0.31   1.00    0.22
Derrida   -0.12   0.67   0.22    1.00
...
```

**Interpretation:**

- Aristotle ↔ Nietzsche: Opposition (-0.23)
- Aristotle ↔ Heidegger: Complementary (0.45)
- Nietzsche ↔ Derrida: Strong alignment (0.67)

### Phase Transition Example

```json
{
  "type": "Emergence",
  "significance": 3.2,
  "fp_change": 0.234,
  "sd_change": 0.187,
  "metrics_before": {
    "freedom_pressure": 0.652,
    "semantic_delta": 0.543
  },
  "metrics_after": {
    "freedom_pressure": 0.886,
    "semantic_delta": 0.730
  }
}
```

**Interpretation:**

- Significance 3.2× threshold → highly significant
- Both F_P and Semantic Δ jumped → emergence
- System transitioned to higher meaning-generation state

---

## 🎯 Research Directions

### Open Questions

1. **Optimal Diversity:**
   - What philosopher diversity maximizes emergence?
   - Is there an optimal cluster size?

2. **Predictability:**
   - Can we predict phase transitions before they occur?
   - What are the leading indicators?

3. **Stability vs. Creativity:**
   - Trade-off between convergence and exploration?
   - How does consensus leader selection affect dynamics?

4. **Temporal Patterns:**
   - Do transitions follow power-law distributions?
   - Are there periodic oscillations in F_P?

### Suggested Experiments

**Experiment A: Minimal Viable Ensemble**

- Run sessions with 2, 4, 8, 12, 16, 20 philosophers
- Measure emergence rate vs. group size
- Find the minimal size for consistent emergence

**Experiment B: Homogeneous vs. Diverse**

- Compare single-cluster groups vs. mixed-cluster groups
- Hypothesis: Diversity increases emergence but decreases consensus

**Experiment C: Adversarial Prompts**

- Design prompts that force dialectical tension
- Measure transition frequency and significance

---

## 📝 Citation

If you use these experiments in research:

```bibtex
@software{po_core_experiments,
  title = {Po\_core Experiments: Analyzing Philosophical Reasoning Dynamics},
  author = {Po\_core Development Team},
  year = {2025},
  url = {https://github.com/hiroshitanaka-creator/Po_core/tree/main/experiments}
}
```

---

## 🤝 Contributing

Contributions are welcome! Areas of interest:

- Advanced statistical methods
- Machine learning for pattern recognition
- Visualization tools (matplotlib, plotly)
- Real-time monitoring dashboards
- Theoretical framework development

---

## 📚 Related Documentation

- [Main README](../README.md)
- [Large-Scale Prototypes](../examples/LARGE_SCALE_PROTOTYPES.md)
- [Database Integration Guide](../examples/LARGE_SCALE_PROTOTYPES.md#-データベース統合)
- [Enterprise Dashboard](../examples/enterprise_dashboard.py)

---

## ⚠️ Notes

- Experiments require database backend (automatically initialized)
- First run may take longer due to model loading
- Results are cumulative (new sessions add to existing data)
- For clean slate, delete `~/.po_core/po_trace.db`

---

**Happy Experimenting! 🔬🎈**
