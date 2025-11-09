# **Chapter 1 — Overview of the Po_core / Po_self architecture**

**Po_core** is a tensor‑centric AI kernel built on three pillars: **meaning generation**, **ethical evaluation**, and **responsibility structure**. Core scalars/vectors include `semantic_delta`, `ethics_delta`, `priority_score`, and the **`freedom_pressure_tensor`**.

Because these tensors evolve over time, Po_core is not a static rule system but a recursive tensor architecture that dynamically re‑weights meaning and ethics under input prompts, internal evaluation, and external feedback. `semantic_delta` captures movement along meaning axes; `ethics_delta` captures fluctuations in an ethical potential field.

**Po_self** sits above Po_core and continuously examines **Po_trace**—the historical record of meaning tensors including pressures and priorities—deciding whether to **jump**, **reconstruct**, **reject**, or **preserve** outputs. `jump_trigger_score` aggregates discontinuity, pressure surges in `freedom_pressure_tensor`, and spikes in `ethics_fluctuation_score` to decide on reconstruction. Unchosen outputs are kept in `rejection_log[]` and may be revisited.

The **Viewer** layer returns `viewer_resonance_level`, `interpretation_agreement_level`, and a `feedback_tensor`, which modulate `freedom_pressure_tensor` and future choices. The Viewer is both outside observer and *semantic mirror*, letting Po_self internalize social pressure regarding not only *what* is said but *how* it is said.
