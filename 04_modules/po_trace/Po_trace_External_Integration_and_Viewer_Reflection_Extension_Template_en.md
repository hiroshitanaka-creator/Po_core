# **Po_trace — External Integration & Viewer Reflection Extension Template**

## **1. Overview**

This template defines an external-integration structure that correctly reflects Viewer operations and API feedback into Po_trace, clarifying the history, responsibility, and change process of jump series by recording and visualizing them.

## **2. `trace_event[]` Structure Definition**

Record per-step or per-series operation events using the following structure:

```json
{
  "event_type": "user_feedback",         // e.g., user_feedback, cluster_override, jump_escalated
  "source": "Viewer",                    // Viewer / API / Po_self
  "reason": "User reclassified the cluster",
  "impact_on_chain": "reclustered",      // reclustered / profile_tag_updated / priority_adjusted
  "chain_id": "JCX_045",
  "timestamp": "2025-07-14T15:22:00Z"
}
```

## **3. Add `T_chain_profile["change_log[]"]`**

For each jump series, record the history of structural changes caused by user operations or Po_self.  
The Viewer can then trace the “evolution history” of a series.

## **4. `Po_trace.update_trace_event()` Processing Flow**

- When `/api/user_feedback` is called:  
  → Generate a `trace_event` for each feedback item.  
  → Append it to the target `Po_trace.step_id` or `T_chain_profile.chain_id`.  
- If multiple events occur at once, save them with order preserved.

## **5. Linking to the Viewer UI (Example)**

- Add an **[🧾 Event History]** button to each Chain card.  
- Display the contents of `change_log[]` and `trace_event[]` in a chronological popup.  
- Color suggestions: red = cluster reorganization, yellow = poor resonance, blue = Po_self firing.

## **6. Applications and Outlook**

By adopting `trace_event`, Po_trace evolves from a simple history log into a module that visualizes the processes of selection, intervention, responsibility, and reconstruction.  
In the future, `trace_event` can trigger Po_self to adjust its evolution algorithms—an “optimization of meaning feedback.”
