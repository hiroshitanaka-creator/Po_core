# ADR 0008: Ethics Guardrails v1 (Non-interference)

- Status: Accepted
- Date: 2026-02-23

## Context
Task D / M2 introduces stronger ethics outputs, while preserving recommendation arbitration authority.
Po_core already centralizes arbitration in `recommendation_v1` + `policy_v1` (ADR 0006).
This ADR clarifies that ethics is a guardrail layer and must not decide recommendation status.

## Decision

### Non-interference contract
`src/pocore/engines/ethics_v1.py` may enrich:
- `ethics.guardrails`
- `ethics.tradeoffs`
- `options[*].ethics_review`

It must not alter or arbitrate:
- `recommendation.status`
- `recommendation.recommended_option_id`
- policy thresholds in `policy_v1`

Recommendation decisions remain exclusively in `src/pocore/engines/recommendation_v1.py`.

### Feature reactions (generic path only)
For non-frozen cases, ethics v1 reacts to features:
- `unknowns_count > 0`
  - add guardrails about avoiding assertions on uncertain facts
  - require explicit assumptions/uncertainty disclosure
  - add matching concerns in `options[*].ethics_review`
- `stakeholders_count > 1`
  - add guardrail for stakeholder impact and consent
  - add tradeoff: autonomy vs externality/justice
- `days_to_deadline` in short horizon (`0..7` days)
  - add tradeoff: speed vs nonmaleficence
  - add guardrail: do not skip verification under time pressure

Frozen branches for `case_001` and `case_009` remain unchanged.

## Consequences
- Ethics output becomes auditable and feature-driven without case-specific branching.
- Recommendation determinism and accountability are preserved by strict separation of concerns.
- Future ethics expansion should remain rule-based first; if complexity grows,
  add extension points without violating non-interference.
