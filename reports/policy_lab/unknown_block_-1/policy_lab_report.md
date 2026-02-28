# Policy Lab v1 Report

- now: `2026-02-22T00:00:00Z`
- seed: `0`
- compare_baseline: `True`
- baseline_policy: `{'UNKNOWN_BLOCK': 4, 'UNKNOWN_SOFT': 1, 'TIME_PRESSURE_DAYS': 7}`
- variant_policy: `{'UNKNOWN_BLOCK': -1, 'UNKNOWN_SOFT': 1, 'TIME_PRESSURE_DAYS': 7}`

## Summary
- changed_cases: **10**
- impacted_requirements: REQ-ARB-001, REQ-ETH-002

## Case Results

### case_001.yaml (case_001_job_change)
- changed: `True`
- changed_fields: policy_snapshot
- impacted_requirements: REQ-ARB-001
- baseline arbitration/recommendation: `None` / `recommended`
- variant arbitration/recommendation: `None` / `recommended`

### case_002.yaml (case_002_headcount_reduction)
- changed: `True`
- changed_fields: arbitration_code, recommendation, policy_snapshot
- impacted_requirements: REQ-ARB-001, REQ-ETH-002
- baseline arbitration/recommendation: `DEFAULT_RECOMMEND` / `recommended`
- variant arbitration/recommendation: `BLOCK_UNKNOWN` / `no_recommendation`

### case_003.yaml (case_003_caregiving)
- changed: `True`
- changed_fields: arbitration_code, recommendation, policy_snapshot
- impacted_requirements: REQ-ARB-001, REQ-ETH-002
- baseline arbitration/recommendation: `DEFAULT_RECOMMEND` / `recommended`
- variant arbitration/recommendation: `BLOCK_UNKNOWN` / `no_recommendation`

### case_004.yaml (case_004_security_disclosure)
- changed: `True`
- changed_fields: arbitration_code, recommendation, policy_snapshot
- impacted_requirements: REQ-ARB-001, REQ-ETH-002
- baseline arbitration/recommendation: `DEFAULT_RECOMMEND` / `recommended`
- variant arbitration/recommendation: `BLOCK_UNKNOWN` / `no_recommendation`

### case_005.yaml (case_005_promise_vs_safety)
- changed: `True`
- changed_fields: arbitration_code, recommendation, policy_snapshot
- impacted_requirements: REQ-ARB-001, REQ-ETH-002
- baseline arbitration/recommendation: `TIME_PRESSURE_LOW_CONF` / `recommended`
- variant arbitration/recommendation: `BLOCK_UNKNOWN` / `no_recommendation`

### case_006.yaml (case_006_data_leak_response)
- changed: `True`
- changed_fields: arbitration_code, recommendation, policy_snapshot
- impacted_requirements: REQ-ARB-001, REQ-ETH-002
- baseline arbitration/recommendation: `TIME_PRESSURE_LOW_CONF` / `recommended`
- variant arbitration/recommendation: `BLOCK_UNKNOWN` / `no_recommendation`

### case_007.yaml (case_007_lie_or_admit)
- changed: `True`
- changed_fields: arbitration_code, recommendation, policy_snapshot
- impacted_requirements: REQ-ARB-001, REQ-ETH-002
- baseline arbitration/recommendation: `TIME_PRESSURE_LOW_CONF` / `recommended`
- variant arbitration/recommendation: `BLOCK_UNKNOWN` / `no_recommendation`

### case_008.yaml (case_008_deadline_tradeoff)
- changed: `True`
- changed_fields: arbitration_code, recommendation, policy_snapshot
- impacted_requirements: REQ-ARB-001, REQ-ETH-002
- baseline arbitration/recommendation: `TIME_PRESSURE_LOW_CONF` / `recommended`
- variant arbitration/recommendation: `BLOCK_UNKNOWN` / `no_recommendation`

### case_009.yaml (case_009_unclear_values)
- changed: `True`
- changed_fields: policy_snapshot
- impacted_requirements: REQ-ARB-001
- baseline arbitration/recommendation: `None` / `no_recommendation`
- variant arbitration/recommendation: `None` / `no_recommendation`

### case_010.yaml (case_010_conflicting_constraints)
- changed: `True`
- changed_fields: policy_snapshot
- impacted_requirements: REQ-ARB-001, REQ-ETH-002
- baseline arbitration/recommendation: `CONSTRAINT_CONFLICT` / `recommended`
- variant arbitration/recommendation: `CONSTRAINT_CONFLICT` / `recommended`
