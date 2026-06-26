---
name: add-philosopher
description: Scaffold, register, and test a new philosopher persona for Po_core. Use when the user wants to add a philosopher, create a new persona/plugin, or expand the 42-philosopher roster. Enforces the deterministic plugin contract and ADR-0006 (no AI-vendor names).
---

# Add a Philosopher

Po_core ships **42 philosophers** (39 classic + Appiah, Fanon, Charles Taylor).
Use this skill to add a new persona that satisfies the plugin contract.

## Hard rules (do NOT violate)

- **ADR-0006**: NEVER add AI-vendor names as philosophers (Claude, GPT, Gemini,
  Grok, etc.). Use only historical/academic philosophers.
- **Determinism**: `reason()` must return the same output for the same input.
  No `datetime.now()`, no randomness baked into the returned text.
- The internal `dummy` slot is a sentinel — never count it toward the 42, and
  never copy it as a template.

## Steps

1. **Confirm scope with the user**: philosopher name, class name, tradition,
   3–5 key concepts, and risk level (0 safe / 1 standard / 2 risky — see
   `src/po_core/philosophers/manifest.py`).

2. **Scaffold** by copying the template:
   - Source: `src/po_core/philosophers/template.py`
   - Dest: `src/po_core/philosophers/<snake_name>.py`
   - Rename class to `<PascalName>`, set `name`, `description`, `tradition`,
     `key_concepts`.

3. **Implement the minimal contract** in `reason(prompt, context=None)`.
   Required return keys: `reasoning` (str), `perspective` (str),
   `metadata.philosopher`. Keep output deterministic (normalize input,
   derive from key_concepts).

4. **Register** in `src/po_core/philosophers/manifest.py` by appending a
   `PhilosopherSpec` to `SPECS`. Match the existing entries' fields (slot,
   risk level, module path, class name). Keep the public roster count
   accurate (42 unless the user is intentionally changing it — that requires
   updating docs/tests/metadata totals everywhere).

5. **Add tests** (required) under `tests/unit/test_philosophers/`:
   - Contract test: `reason()` returns the required keys.
   - Pipeline test: `propose()` returns a `Proposal`.
   - Mirror `tests/test_philosopher_plugin_template.py` as the contract example.

6. **Persona prompt boundary** (only if adding an LLM persona): runtime
   prompts live ONLY in `src/po_core/philosophers/llm_personas.py`. YAML in
   `docs/philosopher_prompt_drafts/` is documentation, not a runtime contract.

7. **Self-check**:
   ```bash
   pytest -q tests/unit/test_philosophers/test_<snake_name>.py
   pytest -q tests/test_philosopher_plugin_template.py
   pytest tests/test_run_turn_e2e.py tests/test_philosopher_bridge.py tests/test_smoke_pipeline.py -v
   ```

8. **Docs**: confirm consistency with `docs/philosopher_plugin_spec.md` and
   `docs/CONTRIBUTING_PHILOSOPHER.md`. If this changes architecture (e.g. a new
   region/tradition like ADR-0006 did), invoke the `new-adr` skill.

9. Run the `update-status` skill to record the change in `docs/status.md`.
