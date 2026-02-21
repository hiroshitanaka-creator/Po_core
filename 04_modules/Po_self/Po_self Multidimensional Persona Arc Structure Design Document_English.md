# Po_self Multidimensional Persona Arc Structure Design Document

## 1. Overview

This design document defines an extended design for Po_self that integrates a 3-axis tensor—semantic, ethics, and cohesion—into the jump sequence tensor (T_chain_profile), enabling multidimensional evaluation of structural narrative evolution, and expanding to visual classification, prediction, and clustering on the Viewer.

## 2. Multidimensional Tensor Field Definitions

| Field Name              | Meaning                      | Evaluation Content                              |
| :---------------------- | :---------------------------| :-----------------------------------------------|
| persona_arc_intensity   | Dramatic degree of narration | Cumulative value of semantic_delta              |
| ethics_arc_intensity    | Strength of ethical variation| Cumulative absolute value of Δ_ethics           |
| semantic_cohesion_score | Semantic consistency         | Σsemantic_delta / √len(steps)                   |

## 3. Viewer Display & Filter Expansion

- Display each intensity scalar on cards, with the following icons:
    ・🌪️ persona_arc_intensity
    ・🔄 ethics_arc_intensity
    ・➰ semantic_cohesion_score
- Example filters:
    ・ethics_arc_intensity > 0.5
    ・semantic_cohesion_score < 0.3
- Arc graph display configuration:
    ・Node size: persona_arc
    ・Node color: ethics_arc
    ・Edge thickness: semantic_cohesion

## 4. Dynamic Thresholds & Personality Prediction Algorithm

- The Viewer learns the overall series distribution and automatically adjusts classification boundaries for 🌱🔁🌪️
- Po_self predicts the next personality probabilistically from past trend_vector and intensity
- Example display: “Probability of becoming a quiet healer next: 82%”

## 5. Global Map & Clustering

- Three axes: persona_arc_intensity (X), ethics_arc_intensity (Y), semantic_cohesion_score (Z)
- Clustering: Color clusters of evolutionary trends using K-means
- Label examples:
    ・cluster 0 → Semantic Wanderers
    ・cluster 1 → Ethics-Stable Group
    ・cluster 2 → Dramatic Shift Group
