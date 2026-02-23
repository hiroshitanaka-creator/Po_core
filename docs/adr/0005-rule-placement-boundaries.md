# ADR 0005: Rule Placement Boundaries for unknowns/stakeholders/deadline (v1)

- Status: Accepted
- Date: 2026-02-23

## Context
As Po_core adds scenarios, case-specific branching increases risk of spaghetti architecture.
We introduce a strict separation of responsibilities:
- parse_input: observation only
- engines: decisions and generation
- orchestrator: wiring only
- recommendation engine: arbitration only

This ADR focuses on three generalization features:
- unknowns
- stakeholders
- deadline

## Decision

### Observation vs Decision
- parse_input MUST extract observable features (counts, normalized lists, parsed dates, arithmetic like days_to_deadline).
- parse_input MUST NOT embed value judgments or recommendations.

### Engine Responsibilities
- unknowns:
  - question engine generates missing-info questions
  - uncertainty engine summarizes uncertainty
  - recommendation engine decides whether recommendation is allowed
  - ethics engine adds guardrails (no overclaim) and tradeoffs

- stakeholders:
  - responsibility engine owns stakeholder mapping and consent considerations
  - ethics engine documents externalities/justice/consent tradeoffs
  - question engine may ask consent/impact questions

- deadline:
  - generator engine creates time-bounded action plans
  - recommendation engine arbitrates under time pressure
  - uncertainty engine includes deadline risk
  - ethics engine adds speed-vs-safety tradeoff
  - question engine asks deadline flexibility if needed

### Arbitration Rule
Only recommendation engine may decide:
- recommendation.status
- recommended_option_id
Other engines must not change recommendation status.

## Consequences
- Prevents logic duplication and conflicting thresholds across engines.
- Makes ethics v1 implementable without becoming a monolithic “fix everything” function.
- Supports scalable scenario growth with features instead of short_id branching.
