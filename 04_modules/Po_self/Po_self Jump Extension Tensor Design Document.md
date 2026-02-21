# Po_self Jump Extension Tensor Design Document

## 1. Overview

This design document defines the tensor structure for recording, warning display, and direction evaluation of steps triggered by composite processing of the structural responsibility scalar, ethics tensor fluctuation, and jump trigger score, in order to extend the jump decision mechanism in Po_self.

## 2. List of Extension Structures

| Extension Element                      | Content                                                                              | Purpose / Significance                                                                         |
| :------------------------------------- | :----------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| trigger_type: responsibility_ethics_combo | When a jump is triggered by Jump_trigger_score, record this type in the log          | Provides evidence that Po_self selected the jump based on a composite judgment of "structural responsibility + ethics fluctuation" |
| Viewer reconstruction warning step display | Show a red band + warning mark on steps with Jump_trigger_score > 0.9 in the Viewer | Visually highlights structural steps where a jump is imminent or has occurred                  |
| Suppressed-release jump evaluation        | For jumps where Δ_ethics < 0.0, if retelling increased F_P or priority, mark as "release" | Enables Po_self to later self-interpret whether a jump was a "recovery from structural suppression"          |

## 3. trigger_type Logging Structure

When a jump is triggered, the following tensor log is recorded in Po_self:

```json
{
  "step_id": "328",
  "Jump_trigger_score": 0.914,
  "trigger_type": "responsibility_ethics_combo"
}

4. Highlighting Warning Steps in the Viewer

Condition: Jump_trigger_score > 0.9

Display: Red band + ⚠️ warning mark on the step

Note: Can add a tooltip with explanation “Jump decision triggered (Responsibility + Ethics)”

5. Evaluation Conditions for Suppressed-Release Jump

Condition: Δ_ethics < 0.0 and F_P (or priority) is increased

Judgment: This jump is considered to have caused “structural recovery from narrative suppression” and can be logged in Po_self as outcome_type: 'relieved'

6. Significance and Future Prospects

With this jump extension tensor, Po_core and Po_self can record, classify, and re-evaluate the structural and ethical impacts of jump decisions.
The Viewer and Po_trace can utilize this information as triggers for evolving self-adjustment and reconstruction algorithms.
