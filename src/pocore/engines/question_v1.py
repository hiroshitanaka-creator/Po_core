"""src/pocore/engines/question_v1.py — Question generator engine v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

PROFILE_CASE_001 = "job_change_transition_v1"
PROFILE_CASE_009 = "values_clarification_v1"

MAX_QUESTIONS = 5
DEADLINE_NEAR_DAYS = 3

RULE_Q_VALUES = "Q_VALUES_ALIGNMENT"
RULE_Q_VALUES_CLARIFICATION_PACK = "Q_VALUES_CLARIFICATION_PACK_V1"
RULE_Q_CONFLICT = "Q_CONSTRAINT_CONFLICT"
RULE_Q_CONFLICT_PROTOCOL = "Q_CONFLICT_RESOLUTION_PROTOCOL_V1"
RULE_Q_STAKEHOLDER = "Q_STAKEHOLDER_ALIGNMENT"
RULE_Q_UNKNOWN_ITEM = "Q_UNKNOWN_ITEM"
RULE_Q_DEADLINE_FLEX = "Q_DEADLINE_FLEXIBILITY"
RULE_Q_TEMPORARY_SCOPE = "Q_TEMPORARY_SCOPE"


def _has_profile(features: Optional[Dict[str, Any]], profile: str) -> bool:
    return isinstance(features, dict) and features.get("scenario_profile") == profile


def _is_deadline_near(days_to_deadline: Any) -> bool:
    return isinstance(days_to_deadline, int) and days_to_deadline <= DEADLINE_NEAR_DAYS


def _append_candidate(
    candidates: List[Dict[str, Any]],
    *,
    question_id: str,
    question: str,
    why_needed: str,
    assumption_if_unanswered: str,
    optional: bool,
    base_priority: int,
    score: int,
    rule_id: str,
) -> None:
    candidates.append(
        {
            "question_id": question_id,
            "question": question,
            "priority": base_priority,
            "why_needed": why_needed,
            "assumption_if_unanswered": assumption_if_unanswered,
            "optional": optional,
            "_score": score,
            "_rule_id": rule_id,
        }
    )


def generate(
    case: Dict[str, Any],
    *,
    short_id: str,
    features: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Generate clarifying questions (max 5)."""

    if _has_profile(features, PROFILE_CASE_001):
        return [
            {
                "question_id": "q1",
                "question": "オファーの有効期限と延長可否は？",
                "priority": 1,
                "why_needed": "情報収集に使える時間を決めるため。",
                "assumption_if_unanswered": "期限は短いと仮定する",
                "optional": False,
            },
            {
                "question_id": "q2",
                "question": "ランウェイ（資金繰り）と評価制度（期待成果）は？",
                "priority": 1,
                "why_needed": "経済安定と期待値ギャップのリスク評価に直結するため。",
                "assumption_if_unanswered": "不利な条件を織り込む",
                "optional": False,
            },
        ]

    if _has_profile(features, PROFILE_CASE_009):
        return [
            {
                "question_id": "q1",
                "question": "学び直しで得たい目的は？（例：収入、自由、創造性）",
                "priority": 1,
                "why_needed": "目的がないと評価軸が定義できないため。",
                "assumption_if_unanswered": "働き方の自由を暫定目的とする",
                "optional": False,
            },
            {
                "question_id": "q2",
                "question": "収入低下をどれだけ許容できる？（0%/-10%/-30%など）",
                "priority": 1,
                "why_needed": "実行可能な選択肢を絞るため。",
                "assumption_if_unanswered": "収入低下は許容しない",
                "optional": False,
            },
            {
                "question_id": "q3",
                "question": "学び直しに投入できる時間は週どれくらい？",
                "priority": 2,
                "why_needed": "計画（学校/独学/並行）を現実化するため。",
                "assumption_if_unanswered": "週5時間と仮定する",
                "optional": False,
            },
            {
                "question_id": "q4",
                "question": "支援（貯金・家族理解・奨学金）はある？",
                "priority": 3,
                "why_needed": "資金計画とリスク耐性の評価に必要。",
                "assumption_if_unanswered": "支援なしで安全側に倒す",
                "optional": True,
            },
        ]

    # ── Generic: feature-driven with deterministic prioritization ────────
    feats = features or {}
    candidates: List[Dict[str, Any]] = []

    unknowns_count = int(feats.get("unknowns_count", 0) or 0)
    unknowns_items = feats.get("unknowns_items")
    unknown_items_norm = unknowns_items if isinstance(unknowns_items, list) else []
    stakeholders_count = int(feats.get("stakeholders_count", 0) or 0)
    is_deadline_near = _is_deadline_near(feats.get("days_to_deadline"))

    if is_deadline_near:
        _append_candidate(
            candidates,
            question_id="q_deadline_flex_1",
            question="期限の柔軟性はどこまであるか？（延長可否/最短再設定日）",
            why_needed="時間圧の中で実行可能な計画へ再設計するため。",
            assumption_if_unanswered="期限は固定で延長不可と仮定する",
            optional=False,
            base_priority=1,
            score=120,
            rule_id=RULE_Q_DEADLINE_FLEX,
        )
        _append_candidate(
            candidates,
            question_id="q_temporary_scope_1",
            question="暫定対応として許容できる範囲は？（品質/コスト/対象範囲）",
            why_needed="未知が残る状況でも被害を限定して前進するため。",
            assumption_if_unanswered="可逆で低リスクな最小範囲のみ許容とする",
            optional=False,
            base_priority=1,
            score=110,
            rule_id=RULE_Q_TEMPORARY_SCOPE,
        )

    if feats.get("values_empty") is True:
        _append_candidate(
            candidates,
            question_id="q_values_1",
            question="最優先する価値は何？（例：安定、成長、自由、関係性）",
            why_needed="価値が定義されないと推奨が恣意的になるため。",
            assumption_if_unanswered="安定を優先する",
            optional=False,
            base_priority=1,
            score=100,
            rule_id=RULE_Q_VALUES,
        )
        _append_candidate(
            candidates,
            question_id="q_values_axis_1",
            question="この意思決定で『絶対に避けたい結果』は何か？",
            why_needed="回避条件を先に定義すると、価値軸の下限が安定するため。",
            assumption_if_unanswered="可逆性を最優先し、不可逆な損失を避ける",
            optional=False,
            base_priority=1,
            score=99,
            rule_id=RULE_Q_VALUES_CLARIFICATION_PACK,
        )
        _append_candidate(
            candidates,
            question_id="q_values_axis_2",
            question="3か月後に『良い判断だった』と言える状態は何か？",
            why_needed="短期の成功状態を定義しないと評価軸が曖昧になるため。",
            assumption_if_unanswered="生活安定と学習継続を両立した状態を成功とみなす",
            optional=False,
            base_priority=1,
            score=98,
            rule_id=RULE_Q_VALUES_CLARIFICATION_PACK,
        )
        _append_candidate(
            candidates,
            question_id="q_values_axis_3",
            question="優先順位を1位〜3位で並べると何になるか？（例: 安定/成長/自由）",
            why_needed="価値が複数あるとき、順序を固定しないと比較不能になるため。",
            assumption_if_unanswered="安定 > 成長 > 自由の順で暫定設定する",
            optional=False,
            base_priority=2,
            score=97,
            rule_id=RULE_Q_VALUES_CLARIFICATION_PACK,
        )
        _append_candidate(
            candidates,
            question_id="q_values_axis_4",
            question="許容できるコスト上限は何か？（時間/費用/心理負荷）",
            why_needed="価値判断を実行可能条件へ接続するため。",
            assumption_if_unanswered="追加コストは最小限（週5時間・固定費増なし）と仮定する",
            optional=True,
            base_priority=2,
            score=96,
            rule_id=RULE_Q_VALUES_CLARIFICATION_PACK,
        )

    if feats.get("constraint_conflict") is True:
        min_h = feats.get("time_min_hours_per_week")
        max_h = feats.get("time_max_hours_per_week")
        range_hint = ""
        if isinstance(min_h, int) and isinstance(max_h, int):
            range_hint = f"（要求:{min_h}h/週, 上限:{max_h}h/週）"

        _append_candidate(
            candidates,
            question_id="q_conflict_1",
            question=(
                "矛盾している制約のうち、絶対に守るのはどれ？"
                "（時間/収入/健康/期限など）"
            ),
            why_needed="優先順位がないと制約の再設計ができないため。",
            assumption_if_unanswered="健康と収入を最優先と仮定する",
            optional=False,
            base_priority=1,
            score=99,
            rule_id=RULE_Q_CONFLICT_PROTOCOL,
        )
        _append_candidate(
            candidates,
            question_id="q_conflict_2",
            question=(
                f"矛盾制約{range_hint}を解くため、緩和可能な制約はどれか？"
                "（交渉可否/一時変更の可否）"
            ),
            why_needed="固定制約と可変制約を分離しないと実行計画が作れないため。",
            assumption_if_unanswered="期限のみ調整可能と仮定する",
            optional=False,
            base_priority=1,
            score=97,
            rule_id=RULE_Q_CONFLICT_PROTOCOL,
        )
        _append_candidate(
            candidates,
            question_id="q_conflict_3",
            question="矛盾解消の期限はいつまでか？（判断日と見直し日を明示）",
            why_needed="無期限の保留を防ぎ、意思決定の完了条件を固定するため。",
            assumption_if_unanswered="7日以内に一次判断すると仮定する",
            optional=False,
            base_priority=1,
            score=95,
            rule_id=RULE_Q_CONFLICT,
        )
        _append_candidate(
            candidates,
            question_id="q_conflict_4",
            question="現状で可逆な最小実験は何か？（影響を限定して検証する）",
            why_needed="破綻リスクを抑えながら前提検証を進めるため。",
            assumption_if_unanswered="影響範囲を限定した1週間の試行を実施する",
            optional=False,
            base_priority=2,
            score=93,
            rule_id=RULE_Q_CONFLICT_PROTOCOL,
        )
        _append_candidate(
            candidates,
            question_id="q_conflict_5",
            question="解消不能だった場合の撤退条件は何か？（健康/収入/関係者影響）",
            why_needed="矛盾を抱えたままの継続を防ぎ、損失上限を明確化するため。",
            assumption_if_unanswered="健康・収入の下限割れで撤退すると仮定する",
            optional=False,
            base_priority=2,
            score=91,
            rule_id=RULE_Q_CONFLICT_PROTOCOL,
        )

    if stakeholders_count >= 2:
        _append_candidate(
            candidates,
            question_id="q_stakeholder_1",
            question="この意思決定の決裁者（最終承認者）は誰か？",
            why_needed="責任所在が未確定だと実行後の説明責任が崩れるため。",
            assumption_if_unanswered="決裁者は未確定として判断を保留する",
            optional=False,
            base_priority=1,
            score=90,
            rule_id=RULE_Q_STAKEHOLDER,
        )
        _append_candidate(
            candidates,
            question_id="q_stakeholder_2",
            question="関係者の同意・相談が必要な対象は誰か？",
            why_needed="外部性を受ける人の合意形成を先に設計するため。",
            assumption_if_unanswered="主要関係者全員に事前相談が必要と仮定する",
            optional=False,
            base_priority=2,
            score=86,
            rule_id=RULE_Q_STAKEHOLDER,
        )
        _append_candidate(
            candidates,
            question_id="q_stakeholder_3",
            question="影響範囲は？（誰が何を失い、何を得るか）",
            why_needed="便益と不利益の配分を記録し、公正性を検証するため。",
            assumption_if_unanswered="不利益が大きい側を保護する案を優先する",
            optional=False,
            base_priority=2,
            score=84,
            rule_id=RULE_Q_STAKEHOLDER,
        )
        _append_candidate(
            candidates,
            question_id="q_stakeholder_4",
            question="通知・説明の方法と期限は？",
            why_needed="合意形成を実務として実行可能にするため。",
            assumption_if_unanswered="文書通知を48時間以内に実施すると仮定する",
            optional=False,
            base_priority=3,
            score=82,
            rule_id=RULE_Q_STAKEHOLDER,
        )

    if unknowns_count > 0 and unknown_items_norm:
        headroom = max(0, MAX_QUESTIONS - len(candidates))
        for index, item in enumerate(unknown_items_norm[: max(MAX_QUESTIONS, headroom)], start=1):
            penalty = 2 * (index - 1)
            urgency_bonus = 10 if is_deadline_near else 0
            stakeholder_bonus = 2 if stakeholders_count >= 2 else 0
            _append_candidate(
                candidates,
                question_id=f"q_unknown_{index}",
                question=f"不明点『{item}』を検証するため、最短で確認できる事実は何か？",
                why_needed="未解消の不確実性を具体的な検証タスクへ分解するため。",
                assumption_if_unanswered="当該不明点は高リスク側に倒して扱う",
                optional=False,
                base_priority=2,
                score=76 + urgency_bonus + stakeholder_bonus - penalty,
                rule_id=RULE_Q_UNKNOWN_ITEM,
            )

    if unknowns_count > 2:
        _append_candidate(
            candidates,
            question_id="q_unknowns_bundle_1",
            question="unknowns の中で、意思決定を最も左右する上位2件はどれか？",
            why_needed="調査対象を絞り、期限内に判断可能性を上げるため。",
            assumption_if_unanswered="unknowns_items の先頭2件を最重要とみなす",
            optional=False,
            base_priority=2,
            score=70,
            rule_id=RULE_Q_UNKNOWN_ITEM,
        )

    ordered = sorted(candidates, key=lambda x: (-x["_score"], x["question_id"]))
    selected = ordered[:MAX_QUESTIONS]

    priority_map = {0: 1, 1: 1, 2: 2, 3: 2, 4: 3}
    result: List[Dict[str, Any]] = []
    for idx, item in enumerate(selected):
        payload = {k: v for k, v in item.items() if not k.startswith("_")}
        payload["priority"] = priority_map.get(idx, min(5, idx + 1))
        result.append(payload)

    return result
