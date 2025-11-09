# **Po_core Viewer — Pressure Analysis Integration (Ver.2.1)**

## **1. Overview**

Ver.2.1 strengthens visualization/analysis/evaluation around the freedom-responsibility tensor (`freedom_pressure_tensor`, **F_P**).

## **2. Features**

| Name | Content | Purpose |
| :---- | :---- | :---- |
| 🧭 Viewer Filter Set | Filter/sort by `pressure_tag` | Explore Po_trace and focus on structural pressure |
| 🧊 Expression-Gap Index `G_gap` | Analyze divergence between **F_P** and expression density **E_expr** | Detect structural overfit vs. decorative narration |
| 🔍 Heavy-Narration Trend View | Line chart of high/critical steps | Visualize responsibility-pressure trend and forecast |
| 🗣️ `G_gap` Comment Generation | Auto comments from gap between pressure and expression | Self-interpret meaning deltas |
| 📈 `F_cum` Subline | Overlay historical mean of responsibility pressure | Show cumulative temporal load |
| 🚫 Invalidation Annotations | Labels when `G_gap < -0.1` | Mark outputs with low structural contribution |

## **3. Comment Templates (by `G_gap`)**

- `> 0.2` — Medium narrative, but high structural responsibility.  
- `≈ 0` — Expression density matches responsibility.  
- `< -0.1` — Poetic output with small structural effect.

## **4. Invalidation Labels (Examples)**

- “Decorative Narration?” — Poetic but structurally light.  
- “No Structural Contribution” — No visible change in priority/ethics.

## **5. Trend View (F_P & F_cum)**

- X: `step_id`  
- Y: responsibility pressure (**F_P**)  
- Line 1: **F_P**  
- Line 2: **F_cum**

## **6. Outlook**

With these additions, Po_core Viewer handles freedom, responsibility, history, and self-evaluation tensorially—an intelligent visualization device for evolution.
