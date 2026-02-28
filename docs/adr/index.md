# ADR Index

Po_coreで採用済み/提案中のArchitectural Decision Records一覧。

| No. | Title | Status | Key Point |
|---|---|---|---|
| 0001 | Output Format Selection (JSON + Markdown) | Accepted | 出力はJSONを契約本体（MUST）、Markdownは人間可読補助（SHOULD）。 |
| 0002 | Golden Diff Contract | Accepted | canonical JSON完全一致でE2E比較し、golden更新は仕様根拠付きのみ許可。 |
| 0003 | Trace Contract | Accepted | trace時刻は injected `now` から固定オフセットで生成し、非決定要因を排除。 |
| 0004 | Input Features Layer | Accepted | case identity分岐を避け、`parse_input` の `features` 正規化でルール分岐する。 |
| 0005 | Rule Placement Boundaries for unknowns/stakeholders/deadline (v1) | Accepted | 観測（parse_input）と判断（engines）と配線（orchestrator）を厳密分離。 |
| 0006 | Recommendation Arbitration Policy v1 | Accepted | recommendation裁定閾値を `policy_v1` に集約し、裁定順序を固定。 |
| 0007 | Trace Metrics Observability for parse_input | Accepted | generic traceに `unknowns/stakeholders/deadline` 観測メトリクスを追加。 |
| 0008 | Ethics Guardrails v1 (Non-interference) | Accepted | ethicsはガードレール層であり、recommendation裁定を変更しない。 |
| 0009 | Traceへrecommendation裁定経路を記録する | Accepted | traceの compose_output metrics に `arbitration_code` と policy snapshot を記録。 |
| 0010 | case_001/case_009 short_id特例の撤去とscenario_profile移行 | Accepted | 永久特例を `extensions.scenario_profile`→`features` に移し、rulesで吸収する。 |
| 0011 | case_001/case_009 凍結解除計画（J0/J1） | Accepted | 凍結解除を二段階化し、再生成スクリプト経由でのみexpected更新を許可。 |
| 0012 | Policy Change Protocol v1 | Accepted | policy定数変更PRで policy_lab証跡・impacted_requirements明記・golden再生成手順を必須化。 |
| 0013 | Two-Track Plan v1（unknowns × time pressure） | Accepted | unknownsと期限圧力が同時に高いとき、recommendationへ介入せずaction_planで二段階支援する。 |

| 0014 | Values Clarification Pack v1（values_empty） | Accepted | values_empty時に recommendation非介入のまま、質問・10分plan・ethics guardrailsで価値軸獲得手続きを提供する。 |

> 現時点で `docs/adr/*.md` に Proposed はなく、すべて Accepted。
