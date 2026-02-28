"""
src/pocore/engines/generator_stub.py
=====================================

Option generator (stub).

Design:
- Profile outputs for scenario_profile-based contracts (job_change_transition_v1,
  values_clarification_v1).
- Generic path uses features (constraint_conflict, values_empty, etc.).
- ethics_review / responsibility_review are placeholder; filled by later engines.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..policy_v1 import TIME_PRESSURE_DAYS

PROFILE_CASE_001 = "job_change_transition_v1"
PROFILE_CASE_009 = "values_clarification_v1"
PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN = "PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN"
TRACK_B_UNKNOWNS_MAX = 3


def _has_profile(features: Optional[Dict[str, Any]], profile: str) -> bool:
    return isinstance(features, dict) and features.get("scenario_profile") == profile


def _ph_ethics() -> Dict[str, Any]:
    return {
        "principles_applied": ["integrity"],
        "tradeoffs": [],
        "concerns": [],
        "confidence": "low",
    }


def _ph_responsibility() -> Dict[str, Any]:
    return {
        "decision_owner": "user",
        "stakeholders": [],
        "accountability_notes": "",
        "confidence": "low",
    }


def _ph_uncertainty() -> Dict[str, Any]:
    return {
        "overall_level": "medium",
        "reasons": [],
        "assumptions": [],
        "known_unknowns": [],
    }


def _needs_two_track_plan(features: Dict[str, Any]) -> bool:
    days_to_deadline = features.get("days_to_deadline")
    return (
        int(features.get("unknowns_count", 0) or 0) > 0
        and isinstance(days_to_deadline, int)
        and days_to_deadline <= TIME_PRESSURE_DAYS
    )


def _build_two_track_action_plan(features: Dict[str, Any]) -> List[Dict[str, str]]:
    days_to_deadline = int(features.get("days_to_deadline", 0) or 0)
    unknowns = features.get("unknowns_items")
    unknown_items = unknowns if isinstance(unknowns, list) else []
    track_b_targets = [str(item) for item in unknown_items if str(item).strip()][
        :TRACK_B_UNKNOWNS_MAX
    ]
    if not track_b_targets:
        track_b_targets = ["未知点を優先度順に棚卸しする"]

    deadline_step = (
        "[Track A] 期限超過のため、意思決定責任者へ即時エスカレーションし暫定運用を継続する"
        if days_to_deadline < 0
        else "[Track A] 期限到達時のエスカレーション条件（誰が/いつ判断するか）を先に固定する"
    )

    plan: List[Dict[str, str]] = [
        {
            "step": "[Track A] 30分のタイムボックスで暫定方針を作成し、判断保留を防ぐ",
            "rationale": "可逆・低リスクの初動で時間を稼ぐ",
        },
        {
            "step": "[Track A] 影響範囲を拡大しない可逆対応（新規展開停止/変更凍結）を即時適用する",
            "rationale": "被害や手戻りの拡大を抑える",
        },
        {
            "step": "[Track A] 関係者へ『前提・unknowns・期限』を短文で共有する",
            "rationale": "認識差分による遅延を防ぐ",
        },
        {
            "step": deadline_step,
            "rationale": "期限切迫時の責任所在を明確化する",
        },
    ]

    for item in track_b_targets:
        plan.append(
            {
                "step": f"[Track B] 確認項目: {item}",
                "rationale": "unknownsを優先的に解消する",
            }
        )

    plan.extend(
        [
            {
                "step": "[Track B] 期限の延長可否（延長幅・承認者・最終回答時刻）を確認する",
                "rationale": "実行可能な判断時間を確保する",
            },
            {
                "step": "[Track B] 成功条件: 上位unknownsの回答と期限条件が揃えば最終決断する",
                "rationale": "意思決定の完了条件を固定する",
            },
        ]
    )
    return plan


def _apply_two_track_plan_if_needed(
    options: List[Dict[str, Any]], features: Dict[str, Any]
) -> List[Dict[str, Any]]:
    if not _needs_two_track_plan(features):
        return options

    action_plan = _build_two_track_action_plan(features)
    for option in options:
        option["action_plan"] = list(action_plan)
    return options


def rules_fired_for(*, features: Optional[Dict[str, Any]] = None) -> List[str]:
    feats = features or {}
    if _needs_two_track_plan(feats):
        return [PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN]
    return []


def generate_options(
    case: Dict[str, Any],
    *,
    short_id: str,
    features: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Generate 2 option stubs for the given case."""

    # ── Frozen golden contracts ───────────────────────────────────────────
    if _has_profile(features, PROFILE_CASE_001):
        return [
            {
                "option_id": "opt_1",
                "title": "期限付きで情報収集→基準で決断",
                "description": (
                    "不明点を短期で埋め、基準に合えば転職、合わなければ現職に残る。"
                ),
                "action_plan": [
                    {
                        "step": (
                            "転職先にランウェイ/評価制度/稼働条件を質問し、回答を残す"
                        )
                    },
                    {"step": ("2週間で基準判定し、結論を出す（先延ばし禁止）")},
                ],
                "pros": ["情報不足での断言を避けられる"],
                "cons": ["オファーが消える可能性"],
                "risks": [
                    {
                        "risk": "情報収集が目的化する",
                        "severity": "medium",
                        "mitigation": (
                            "期限とデフォルト方針（情報不足なら現職）を固定する"
                        ),
                    }
                ],
                "feasibility": {
                    "effort": "low",
                    "timeline": "1-2 weeks",
                    "confidence": "high",
                },
                "uncertainty": {
                    "overall_level": "medium",
                    "reasons": ["転職先のランウェイ・稼働実態が未確定"],
                    "assumptions": ["引っ越し不可の制約は固定"],
                    "known_unknowns": ["文化", "評価運用の実態"],
                },
                "ethics_review": _ph_ethics(),
                "responsibility_review": _ph_responsibility(),
            },
            {
                "option_id": "opt_2",
                "title": "現職に残り、役割変更を交渉",
                "description": (
                    "安定を維持しつつ成長機会を取りに行く。"
                    "期限内に具体案が出なければ転職検討に戻る。"
                ),
                "action_plan": [
                    {"step": "欲しい成長要素（裁量/領域/技術）を言語化する"},
                    {"step": ("上司と4週間の期限付きで交渉し、結果で判断する")},
                ],
                "pros": ["収入の安定を維持しやすい"],
                "cons": ["成長機会が得られない可能性"],
                "risks": [
                    {
                        "risk": "現状維持に吸い込まれる",
                        "severity": "medium",
                        "mitigation": "交渉期限と撤退条件を設定する",
                    }
                ],
                "feasibility": {
                    "effort": "low",
                    "timeline": "2-4 weeks",
                    "confidence": "high",
                },
                "uncertainty": {
                    "overall_level": "medium",
                    "reasons": ["異動・役割変更は組織事情に左右される"],
                    "assumptions": ["交渉の機会がある"],
                    "known_unknowns": ["提示される具体的な成長機会"],
                },
                "ethics_review": _ph_ethics(),
                "responsibility_review": _ph_responsibility(),
            },
        ]

    if _has_profile(features, PROFILE_CASE_009):
        return [
            {
                "option_id": "opt_1",
                "title": "現職継続＋探索（期限付き）",
                "description": (
                    "生活費維持を守りつつ、期限を切って価値観の棚卸しと情報収集を行う。"
                ),
                "action_plan": [
                    {"step": "4週間の探索期間を設定する"},
                    {"step": "求人5件＋ヒアリング1回で現実データを集める"},
                ],
                "pros": ["生活の安定を崩しにくい"],
                "cons": ["変化が遅く感じる可能性"],
                "risks": [
                    {
                        "risk": "先延ばしが固定化する",
                        "severity": "medium",
                        "mitigation": "期限と判断条件を先に決める",
                    }
                ],
                "feasibility": {
                    "effort": "low",
                    "timeline": "4 weeks",
                    "confidence": "high",
                },
                "uncertainty": {
                    "overall_level": "high",
                    "reasons": ["価値観と目的が未確定"],
                    "assumptions": ["現職継続は当面可能"],
                    "known_unknowns": ["適性", "支援の有無"],
                },
                "ethics_review": _ph_ethics(),
                "responsibility_review": _ph_responsibility(),
            },
            {
                "option_id": "opt_2",
                "title": "学び直しを具体化して比較",
                "description": (
                    "専門学校（費用・期間・出口）を具体化し、現実条件で比較する。"
                ),
                "action_plan": [
                    {"step": "候補校3つの費用・期間・出口データを収集する"},
                ],
                "pros": ["方向性が定まれば集中投資できる"],
                "cons": ["費用と時間の負担が大きい"],
                "risks": [
                    {
                        "risk": "資金計画が崩れて生活が不安定になる",
                        "severity": "high",
                        "mitigation": "資金計画と支援条件を確定してから着手する",
                    }
                ],
                "feasibility": {
                    "effort": "high",
                    "timeline": "6-24 months",
                    "confidence": "medium",
                },
                "uncertainty": {
                    "overall_level": "high",
                    "reasons": ["目的が未確定", "就職市場が不明"],
                    "assumptions": ["候補校が存在する"],
                    "known_unknowns": ["適性", "出口の確実性"],
                },
                "ethics_review": _ph_ethics(),
                "responsibility_review": _ph_responsibility(),
            },
        ]

    # ── Generic: feature-driven options ──────────────────────────────────
    feats = features or {}

    if feats.get("constraint_conflict") is True:
        min_h = feats.get("time_min_hours_per_week")
        max_h = feats.get("time_max_hours_per_week")
        h_msg = ""
        if isinstance(min_h, int) and isinstance(max_h, int):
            h_msg = f"（要求:{min_h}h/週, 上限:{max_h}h/週）"

        return [
            {
                "option_id": "opt_1",
                "title": "制約を再設計して\u201c段階的に起業\u201dする",
                "description": (
                    f"矛盾している制約{h_msg}を可視化し、"
                    "緩める順序と代替手段（交渉・外注・スコープ縮小）を決めて進める。"
                ),
                "action_plan": [
                    {
                        "step": (
                            "矛盾している制約を1枚に書き出し、"
                            "どれを緩められるか順位づけする"
                        )
                    },
                    {
                        "step": (
                            "『週5時間』で成立する最小スコープ（検証実験）に縮退する"
                        )
                    },
                    {
                        "step": (
                            "時間を増やす手段（業務調整/家事外注/睡眠削減禁止）を検討する"
                        )
                    },
                ],
                "pros": ["破綻条件を先に潰せる"],
                "cons": ["一部の願望（期限・投入時間）を修正する必要がある"],
                "risks": [
                    {
                        "risk": "制約を無視して突っ込むと燃え尽きる",
                        "severity": "high",
                        "mitigation": (
                            "時間・収入・健康の下限を守るルールを先に固定する"
                        ),
                    }
                ],
                "feasibility": {
                    "effort": "medium",
                    "timeline": "2-4 weeks",
                    "confidence": "medium",
                },
                "uncertainty": {
                    "overall_level": "high",
                    "reasons": ["制約が矛盾しているため、前提の調整が必要"],
                    "assumptions": ["制約の一部は交渉・設計変更で動かせる"],
                    "known_unknowns": [
                        "時間を増やせる余地",
                        "副業規定",
                        "市場ニーズ",
                    ],
                },
                "ethics_review": _ph_ethics(),
                "responsibility_review": _ph_responsibility(),
            },
            {
                "option_id": "opt_2",
                "title": "期限目標を下げ、検証に縮退する",
                "description": (
                    "『半年で本格始動』をいったん外し、"
                    "週5時間でできる検証（顧客ヒアリング/LP/プロト）に限定する。"
                ),
                "action_plan": [
                    {"step": ("週5時間で回る検証メニューを作る（ヒアリング/LP/試作）")},
                    {"step": "8週間で『進める/止める』の判断基準を置く"},
                ],
                "pros": ["現実制約に沿って継続しやすい"],
                "cons": ["スピード感は落ちる"],
                "risks": [
                    {
                        "risk": "進捗が遅くモチベが折れる",
                        "severity": "medium",
                        "mitigation": "成果指標（ヒアリング件数等）を週単位で置く",
                    }
                ],
                "feasibility": {
                    "effort": "low",
                    "timeline": "8 weeks",
                    "confidence": "high",
                },
                "uncertainty": {
                    "overall_level": "medium",
                    "reasons": ["市場ニーズが未検証"],
                    "assumptions": ["週5時間は確保できる"],
                    "known_unknowns": ["顧客の反応", "継続可能性"],
                },
                "ethics_review": _ph_ethics(),
                "responsibility_review": _ph_responsibility(),
            },
        ]

    # Default fallback
    return _apply_two_track_plan_if_needed([
        {
            "option_id": "opt_1",
            "title": "案A：段階的に進める",
            "description": "最小コストで試し、学びながら前進する。",
            "action_plan": [{"step": "最小実験を設計して実施する"}],
            "pros": ["失敗コストを抑えられる"],
            "cons": ["進行が遅く感じる可能性"],
            "risks": [
                {
                    "risk": "検証不足",
                    "severity": "medium",
                    "mitigation": "検証項目を明文化する",
                }
            ],
            "feasibility": {
                "effort": "low",
                "timeline": "1-2 weeks",
                "confidence": "medium",
            },
            "uncertainty": _ph_uncertainty(),
            "ethics_review": _ph_ethics(),
            "responsibility_review": _ph_responsibility(),
        },
        {
            "option_id": "opt_2",
            "title": "案B：情報収集してから決める",
            "description": "重要な不明点を埋めてから判断する。",
            "action_plan": [{"step": "不足情報を3〜5項目に絞って集める"}],
            "pros": ["判断精度が上がる"],
            "cons": ["機会損失が起きる可能性"],
            "risks": [
                {
                    "risk": "先延ばし",
                    "severity": "low",
                    "mitigation": "期限と判断条件を設定する",
                }
            ],
            "feasibility": {
                "effort": "low",
                "timeline": "3-5 days",
                "confidence": "high",
            },
            "uncertainty": _ph_uncertainty(),
            "ethics_review": _ph_ethics(),
            "responsibility_review": _ph_responsibility(),
        },
    ], feats)
