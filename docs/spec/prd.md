# Po_core Product Requirements Document (PRD)

**Version:** 1.0
**Date:** 2026-03-21
**Status:** Current product/design baseline. Release-state truth is governed by `docs/status.md`, not by this PRD.
**Package status note:** repository target version is currently `1.0.3`; latest published public version remains whatever `docs/status.md` and `docs/release/` explicitly evidence.

## 1. Purpose

Po_core is a **philosophy-driven AI decision-support system**. It is designed to help humans deliberate, not to replace human responsibility. It provides structured options, reasons, counterarguments, uncertainty, and additional questions so that users can make more accountable decisions.

Po_core is controlled by **SolarWill** and **W_Ethics Gate**. It prioritizes ethics, accountability, auditability, and structured reasoning. It is **not** a truth oracle, **not** an emotional-care chatbot, and **not** a final-decision replacement for medical/legal/financial judgment.

## 2. Canonical architectural truths

- Formal philosopher count = **42 philosophers**.
- The internal `dummy` slot is a helper / sentinel / compliance slot and is **not** one of the 42.
- Public surfaces must preserve the 42-philosopher truth even when internal runtime helpers or selection budgets differ.
- Release-state claims belong to `docs/status.md`; this PRD defines product intent and architecture, not publication evidence.

## 3. Scope

### In scope

- Structured decision support via options, reasons, counterarguments, uncertainty, and follow-up questions
- Philosophical ensemble deliberation across the formal 42-philosopher roster
- SolarWill and W_Ethics Gate controlled safety and ethical review
- Traceable, auditable reasoning artifacts
- Python API, CLI, and REST API delivery surfaces

### Out of scope

- Truth certification about the external world
- Emotional-care chatbot optimization
- Final human judgment replacement in medical, legal, or financial domains

## 4. Release-truth handling

This PRD intentionally avoids hardcoding mutable publication claims, workflow success claims, or package-index status. When release truth changes, update `docs/status.md` and the exact evidence files under `docs/release/`; do not treat the PRD as a release-status SSOT.

## 5. Implementation notes

- The runtime package version is sourced from `src/po_core/__init__.py` and loaded dynamically by `pyproject.toml`.
- Public manifests and docs must exclude `dummy` from philosopher totals.
- Runtime prompt contract authority is `src/po_core/philosophers/llm_personas.py`. Draft prompt YAML under `docs/philosopher_prompt_drafts/` is documentation-only.
