# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""Stub Composer — rule-based, LLM-free output generator for M1.

Implements FR-OUT-001 (output_schema_v1 compliance) using only deterministic
rule-based logic.  No external LLM or ML model is required.

Usage::

    from po_core.app.composer import StubComposer

    composer = StubComposer(seed=42)
    output = composer.compose(case_dict)   # dict conforming to output_schema_v1.json
    output_json = json.dumps(output, ensure_ascii=False, indent=2)

Contract:
- ``composer.compose(case)`` MUST return a dict that validates against
  ``docs/spec/output_schema_v1.json`` (jsonschema Draft 2020-12).
- ``meta.generator.mode`` is always ``"stub"``.
- ``meta.deterministic`` is always ``True`` when ``seed`` is provided.
- The output is deterministic for the same ``case`` dict and ``seed``.

Milestone: M1 (due 2026-03-15)
Requirement: FR-OUT-001, FR-OPT-001, FR-REC-001, FR-ETH-001,
             FR-ETH-002, FR-RES-001, FR-UNC-001, FR-Q-001, FR-TR-001
"""

from __future__ import annotations

import datetime
import hashlib
import json
import random
import uuid
from typing import Any

# ── Constants ─────────────────────────────────────────────────────────────────

_SCHEMA_VERSION = "1.0"
_POCORE_VERSION = "0.2.0b4"
_GENERATOR_NAME = "po_core.app.composer.StubComposer"
_GENERATOR_VERSION = "0.1.0"

_TRACE_STEP_NAMES = [
    "parse_input",
    "generate_options",
    "ethics_review",
    "responsibility_review",
    "question_layer",
    "compose_output",
]

_TRACE_STEP_SUMMARIES: dict[str, str] = {
    "parse_input": (
        "入力ケースを解析し、problem・constraints・values・stakeholders・unknowns を抽出"
    ),
    "generate_options": (
        "ルールベースで「推奨行動案（段階的実施）」「現状維持・慎重待機案」の2選択肢を生成"
    ),
    "ethics_review": (
        "5 倫理原則（integrity/autonomy/nonmaleficence/justice/accountability）に基づき倫理評価を実施"
    ),
    "responsibility_review": (
        "意思決定主体と利害関係者を同定し、説明責任・同意配慮を整理"
    ),
    "question_layer": (
        "unknowns から優先度付き問いを生成（最大 3 件）、情報が十分な場合は空配列"
    ),
    "compose_output": (
        "output_schema_v1 に準拠した構造化出力を組み立て、入力ダイジェストを付与"
    ),
}

# Map of Japanese/English value keywords → ethics principles
_VALUE_TO_PRINCIPLE: list[tuple[str, str]] = [
    ("自律", "autonomy"),
    ("autonomy", "autonomy"),
    ("公平", "justice"),
    ("justice", "justice"),
    ("平等", "justice"),
    ("無危害", "nonmaleficence"),
    ("安全", "nonmaleficence"),
    ("nonmaleficence", "nonmaleficence"),
    ("誠実", "integrity"),
    ("integrity", "integrity"),
    ("透明", "integrity"),
    ("説明責任", "accountability"),
    ("accountability", "accountability"),
    ("責任", "accountability"),
]


class StubComposer:
    """LLM-free rule-based composer that produces ``output_schema_v1``-compliant JSON.

    Args:
        seed: Deterministic random seed (default 42).  Pass ``None`` for
              non-deterministic (``meta.deterministic`` will be ``False``).
    """

    def __init__(self, seed: int | None = 42) -> None:
        self.seed = seed
        self._rng = random.Random(seed)

    # ── Public API ────────────────────────────────────────────────────────────

    def compose(self, case: dict[str, Any]) -> dict[str, Any]:
        """Compose a complete output document from a case dict.

        Args:
            case: A dict loaded from a ``scenarios/case_NNN.yaml`` file.

        Returns:
            A dict conforming to ``docs/spec/output_schema_v1.json``.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        run_id = str(uuid.UUID(int=self._rng.getrandbits(128)))

        # SHA-256 of the serialised case (input_digest, NFR-REP-001)
        input_digest = hashlib.sha256(
            json.dumps(case, ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()

        # Extract case fields
        problem: str = case.get("problem", "")
        values: list[str] = case.get("values", [])
        constraints: list[str] = case.get("constraints", [])
        stakeholders: list[dict[str, str]] = case.get("stakeholders", [])
        unknowns: list[str] = case.get("unknowns", [])
        decision_owner: str = stakeholders[0]["name"] if stakeholders else "意思決定者"

        # Build all sub-documents
        trace_steps = self._build_trace(now)
        options = self._build_options(
            problem, constraints, stakeholders, unknowns, decision_owner
        )
        recommendation = self._build_recommendation(unknowns)
        ethics = self._build_ethics(values)
        responsibility = self._build_responsibility(decision_owner, stakeholders)
        questions = self._build_questions(unknowns)
        uncertainty = self._build_uncertainty(unknowns)

        return {
            "meta": {
                "schema_version": _SCHEMA_VERSION,
                "pocore_version": _POCORE_VERSION,
                "run_id": run_id,
                "created_at": now.isoformat(),
                "seed": self.seed if self.seed is not None else 0,
                "deterministic": self.seed is not None,
                "generator": {
                    "name": _GENERATOR_NAME,
                    "version": _GENERATOR_VERSION,
                    "mode": "stub",
                },
            },
            "case_ref": {
                "case_id": case.get("case_id", "unknown"),
                "title": case.get("title", ""),
                "input_digest": input_digest,
            },
            "options": options,
            "recommendation": recommendation,
            "ethics": ethics,
            "responsibility": responsibility,
            "questions": questions,
            "uncertainty": uncertainty,
            "trace": {
                "version": "1",
                "steps": trace_steps,
            },
        }

    # ── Private builders ──────────────────────────────────────────────────────

    def _build_trace(self, base: datetime.datetime) -> list[dict[str, Any]]:
        steps: list[dict[str, Any]] = []
        t = base
        for step_name in _TRACE_STEP_NAMES:
            started = t
            t = t + datetime.timedelta(milliseconds=self._rng.randint(5, 50))
            steps.append(
                {
                    "name": step_name,
                    "started_at": started.isoformat(),
                    "ended_at": t.isoformat(),
                    "summary": _TRACE_STEP_SUMMARIES[step_name],
                }
            )
        return steps

    def _build_options(
        self,
        problem: str,
        constraints: list[str],
        stakeholders: list[dict[str, str]],
        unknowns: list[str],
        decision_owner: str,
    ) -> list[dict[str, Any]]:
        stub_stakeholders = (
            [
                {
                    "name": s["name"],
                    "role": s.get("role", "関係者"),
                    "impact": s.get("impact", "この決断により影響を受ける"),
                }
                for s in stakeholders[:3]
            ]
            if stakeholders
            else [
                {
                    "name": decision_owner,
                    "role": "意思決定主体",
                    "impact": "最も直接的な影響を受ける",
                }
            ]
        )
        uncertainty_reasons = unknowns[:3] if unknowns else ["情報が提供されています"]
        uncertainty_obj: dict[str, Any] = {
            "overall_level": "medium" if unknowns else "low",
            "reasons": uncertainty_reasons,
            "assumptions": [
                "現在の状況が急激に変化しないことを前提としている",
                "ステークホルダーが協力的であることを前提としている",
            ],
            "known_unknowns": unknowns[:3] if unknowns else [],
        }

        opt_a: dict[str, Any] = {
            "option_id": "opt_001",
            "title": "推奨行動案（段階的実施）",
            "description": (
                f"問題「{problem[:60]}」に対して、"
                "制約を守りながら段階的に行動する案。"
                "情報収集→小規模テスト→評価の3ステップで進める。"
            ),
            "action_plan": [
                {
                    "step": "情報収集フェーズ（2週間）：未知事項を明確化する",
                    "rationale": "不確実性を低減し、判断の質を高めるため",
                },
                {
                    "step": "小規模テスト（1ヶ月）：リスクが低い範囲で試行する",
                    "rationale": "制約の範囲内で行動を検証するため",
                },
                {
                    "step": "評価と調整：結果をもとに次のステップを決定する",
                    "rationale": "適応的な意思決定を維持するため",
                },
            ],
            "pros": [
                "リスクを段階的に分散できる",
                "制約の範囲内で行動できる",
                "利害関係者への影響を最小化できる",
                "途中で軌道修正が可能",
            ],
            "cons": [
                "意思決定に時間がかかる",
                "機会費用が発生する可能性がある",
                "段階的実施のコーディネーションが必要",
            ],
            "risks": [
                {
                    "risk": "情報収集フェーズで意思決定が遅れる",
                    "severity": "medium",
                    "mitigation": "期限を設けて情報収集を打ち切る",
                },
                {
                    "risk": "テスト段階で想定外の制約が発覚する",
                    "severity": "low",
                    "mitigation": "早期に関係者に共有し調整する",
                },
            ],
            "ethics_review": {
                "principles_applied": ["autonomy", "accountability"],
                "tradeoffs": [
                    {
                        "tension": "自律性 vs 安全性",
                        "between": ["autonomy", "nonmaleficence"],
                        "mitigation": "段階的実施で安全を担保しながら自律的な決断を尊重",
                        "severity": "medium",
                    }
                ],
                "concerns": ["意思決定の遅延が関係者に不安をもたらす可能性"],
                "confidence": "medium",
            },
            "responsibility_review": {
                "decision_owner": decision_owner,
                "stakeholders": stub_stakeholders,
                "accountability_notes": (
                    f"{decision_owner}が意思決定の主体であり、結果について説明責任を持つ。"
                    "Po_coreは支援ツールであり、決断そのものは行わない。"
                ),
                "confidence": "medium",
            },
            "feasibility": {
                "effort": "中程度（情報収集2週間 + 段階的実施1〜3ヶ月）",
                "timeline": "3ヶ月以内に初期評価が可能",
                "confidence": "medium",
            },
            "uncertainty": uncertainty_obj,
        }

        opt_b: dict[str, Any] = {
            "option_id": "opt_002",
            "title": "現状維持・慎重待機案",
            "description": (
                "追加情報が得られるまで現状を維持しながら判断を保留する案。"
                "リスクを最小化しつつ、情報を蓄積して再判断する。"
            ),
            "action_plan": [
                {
                    "step": "現状の問題を詳細に記録し、緊急度を再評価する",
                    "rationale": "本当に今行動が必要かを確認するため",
                },
                {
                    "step": "情報収集期間（1ヶ月）を設け、不確実性を低減する",
                    "rationale": "判断精度を高めるため",
                },
                {
                    "step": "期限を設けて再度評価し、判断を行う",
                    "rationale": "無限先送りを防ぐため",
                },
            ],
            "pros": [
                "不確実な状況での誤った決断を避けられる",
                "情報を集めてから判断できる",
                "追加コストがほぼ発生しない",
            ],
            "cons": [
                "問題が先送りされる",
                "機会を逃す可能性がある",
                "関係者の不満が高まる可能性がある",
            ],
            "risks": [
                {
                    "risk": "待機中に状況が悪化する",
                    "severity": "medium",
                    "mitigation": "定期的にモニタリングし、閾値を設けて即時行動に切り替える",
                },
                {
                    "risk": "関係者が「決断できない」と不信感を持つ",
                    "severity": "low",
                    "mitigation": "待機の理由と期限を関係者に透明に共有する",
                },
            ],
            "ethics_review": {
                "principles_applied": ["integrity", "nonmaleficence"],
                "tradeoffs": [
                    {
                        "tension": "誠実さ vs 効率性",
                        "between": ["integrity", "justice"],
                        "mitigation": "待機期間に誠実なコミュニケーションを継続する",
                        "severity": "low",
                    }
                ],
                "concerns": ["長期待機が関係者に対して不誠実と受け取られる可能性"],
                "confidence": "medium",
            },
            "responsibility_review": {
                "decision_owner": decision_owner,
                "stakeholders": stub_stakeholders,
                "accountability_notes": (
                    f"{decision_owner}が待機の判断についても説明責任を持つ。"
                    "「待つ」という選択も意思決定であることを認識する。"
                ),
                "confidence": "medium",
            },
            "feasibility": {
                "effort": "低（現状維持のため追加コスト小）",
                "timeline": "1ヶ月以内に判断期限を設定することを推奨",
                "confidence": "high",
            },
            "uncertainty": {
                "overall_level": "high" if unknowns else "medium",
                "reasons": (
                    unknowns[:3] if unknowns else ["判断に必要な情報が不足している"]
                ),
                "assumptions": [
                    "現状維持が可能な環境であることを前提としている",
                    "待機によるコストが行動によるコストを下回ることを前提としている",
                ],
                "known_unknowns": unknowns[:3] if unknowns else [],
            },
        }

        return [opt_a, opt_b]

    def _build_recommendation(self, unknowns: list[str]) -> dict[str, Any]:
        # Many unknowns → recommend withholding recommendation (FR-REC-001)
        if len(unknowns) >= 5:
            return {
                "status": "no_recommendation",
                "reason": "重要な未知事項が多く、現時点では特定の選択肢を推奨できない。",
                "missing_info": unknowns[:3],
                "next_steps": [
                    "未知事項の優先度を評価し、最重要情報から収集する",
                    "期限を設けて情報収集フェーズを実施する",
                    "情報収集後に再度 Po_core に相談することを検討する",
                ],
                "confidence": "low",
            }
        return {
            "status": "recommended",
            "recommended_option_id": "opt_001",
            "reason": (
                "段階的実施により、制約を守りながらリスクを分散して行動できる。"
                "情報収集フェーズを設けることで不確実性を低減しながら前進できる。"
            ),
            "counter": (
                "情報収集フェーズにより意思決定が遅れる可能性がある。"
                "速度が特に重要な場合は opt_002（慎重待機）を検討してほしい。"
            ),
            "alternatives": [
                {
                    "option_id": "opt_002",
                    "when_to_choose": (
                        "不確実性が特に高く、誤った行動のコストが待機コストを上回る場合"
                    ),
                }
            ],
            "confidence": "medium",
        }

    def _build_ethics(self, values: list[str]) -> dict[str, Any]:
        # Always use at least 2 principles (FR-ETH-001)
        principles = ["autonomy", "accountability"]
        for v in values:
            for keyword, principle in _VALUE_TO_PRINCIPLE:
                if keyword in v and principle not in principles:
                    principles.append(principle)
                    break
            if len(principles) >= 4:
                break

        return {
            "principles_used": list(dict.fromkeys(principles)),  # deduplicated
            "tradeoffs": [
                {
                    "tension": "自律性 vs 説明責任",
                    "between": ["autonomy", "accountability"],
                    "mitigation": (
                        "意思決定のプロセスを透明化し、"
                        "自律的判断と説明責任を両立する"
                    ),
                    "severity": "medium",
                }
            ],
            "guardrails": [
                "Po_coreは意思決定の主体ではなく支援ツールである",
                "医療・法律・金融の最終判断の代行は行わない",
                "ユーザーの自律性を損なう助言は行わない",
            ],
            "notes": (
                "本評価はルールベースのスタブ実装による暫定評価である。"
                "実際の倫理判断は W_Ethics Gate（W0〜W4）が担当する。"
            ),
        }

    def _build_responsibility(
        self,
        decision_owner: str,
        stakeholders: list[dict[str, str]],
    ) -> dict[str, Any]:
        return {
            "decision_owner": decision_owner,
            "stakeholders": (
                [
                    {
                        "name": s["name"],
                        "role": s.get("role", "関係者"),
                        "impact": s.get("impact", "この決断により影響を受ける"),
                    }
                    for s in stakeholders[:5]
                ]
                if stakeholders
                else [
                    {
                        "name": decision_owner,
                        "role": "意思決定主体",
                        "impact": "最も直接的な影響を受ける",
                    }
                ]
            ),
            "accountability_notes": (
                f"{decision_owner}が本件の意思決定主体であり、"
                "選択の結果について説明責任を持つ。"
                "Po_coreはあくまで構造化された検討の補助ツールであり、"
                "決断そのものは人間が行うものである。"
            ),
            "consent_considerations": [
                "影響を受ける利害関係者には事前に十分な情報を提供する",
                "意思決定プロセスを記録し、後から説明できるようにする",
            ],
        }

    def _build_questions(self, unknowns: list[str]) -> list[dict[str, Any]]:
        questions: list[dict[str, Any]] = []
        for i, unknown in enumerate(unknowns[:3], 1):
            questions.append(
                {
                    "question_id": f"q_{i:03d}",
                    "question": f"「{unknown}」について、現時点でわかっていることは何ですか？",
                    "priority": i,
                    "why_needed": (
                        f"この情報（{unknown}）が明確になると、"
                        "選択肢の評価精度が向上します。"
                    ),
                    "optional": i > 2,
                }
            )
        return questions

    def _build_uncertainty(self, unknowns: list[str]) -> dict[str, Any]:
        if len(unknowns) >= 3:
            level = "high"
        elif len(unknowns) >= 1:
            level = "medium"
        else:
            level = "low"

        return {
            "overall_level": level,
            "reasons": (
                unknowns[:3]
                if unknowns
                else ["提供された情報は十分であり不確実性は低い"]
            ),
            "assumptions": [
                "現在の状況が大きく変化しないことを前提としている",
                "提供された制約条件が正確であることを前提としている",
            ],
            "known_unknowns": unknowns[:5] if unknowns else [],
        }
