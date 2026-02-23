# ADR 0006: Recommendation Arbitration Policy v1

- Status: Accepted
- Date: 2026-02-23

## Context
Task B requires that recommendation arbitration rules be centralized and deterministic.
Previously, thresholds and conflict ordering were implicit in the recommendation engine,
which risks drift as new scenarios are added.

Po_core already defines responsibility boundaries:
- parse_input: observation (features extraction)
- recommendation engine: arbitration decision
- other engines: supporting outputs only

## Decision

### Policy location
Introduce `src/pocore/policy_v1.py` as the single source of arbitration thresholds:
- `UNKNOWN_BLOCK`
- `UNKNOWN_SOFT`
- `TIME_PRESSURE_DAYS`

And helper predicates:
- `should_block_recommendation(features)`
- `has_time_pressure_with_unknowns(features)`

### Decision authority
Only `src/pocore/engines/recommendation_v1.py` may import and use `policy_v1.py`.
Other engines must not import `policy_v1.py` and must not change recommendation status.

### Arbitration order (v1)
For non-frozen generic cases:
1. `values_empty == True` ⇒ `no_recommendation` (existing behavior kept)
2. `constraint_conflict == True` ⇒ existing conflict-first behavior kept
3. `unknowns_count >= UNKNOWN_BLOCK` ⇒ `no_recommendation`
4. `days_to_deadline <= TIME_PRESSURE_DAYS` and `unknowns_count > 0`
   ⇒ allow recommendation but reduce confidence (`low`)
5. Otherwise ⇒ existing default recommendation path

### Frozen cases contract
`case_001` and `case_009` remain frozen via explicit branches in recommendation engine.
Policy refactoring must not change these outputs.

## Consequences
- Thresholds become explicit and auditable in one file.
- Unknowns × deadline arbitration is consistent across cases.
- Future threshold tuning can happen by policy update + tests without spreading literals.
- Determinism is preserved because policy depends only on injected features.
