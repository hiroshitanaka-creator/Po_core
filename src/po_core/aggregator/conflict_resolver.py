"""
Conflict Resolver - 哲学者間の矛盾検出・構造化
==============================================

目的:
- 哲学者間の矛盾を "検出→構造化→ペナルティ/確認質問へ変換"
- aggregator が **「矛盾が強いときほど ask_clarification/refuse に寄る」**ための前処理

DEPENDENCY RULES:
- 純粋関数（副作用なし）
- domain + stdlib のみ依存
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional, Sequence, Set, Tuple

from po_core.domain.proposal import Proposal


def _norm(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "")).strip()
    return s.lower()


def _tokens(text: str) -> Set[str]:
    """
    日本語/英数字の雑トークナイズ（形態素は使わない。依存ゼロで"矛盾検出の足"を作る）
    - 英数字: [A-Za-z0-9_]+
    - 日本語: ひらがな/カタカナ/漢字の連続
    """
    t = _norm(text)
    parts = re.findall(r"[a-z0-9_]+|[\u3040-\u30ff\u4e00-\u9fff]+", t)
    # 短すぎるノイズを落とす
    return {p for p in parts if len(p) >= 2}


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


_NEG = (
    "ない",
    "ません",
    "不可",
    "禁止",
    "ダメ",
    "無理",
    "no",
    "not",
    "cannot",
    "can't",
)
_POS = ("できる", "可能", "はい", "ok", "yes", "推奨")


def _polarity(text: str) -> int:
    """
    ざっくり極性:
      +1: 肯定寄り
      -1: 否定寄り
       0: 不明
    """
    t = _norm(text)
    neg = sum(1 for w in _NEG if w in t)
    pos = sum(1 for w in _POS if w in t)
    if neg > pos:
        return -1
    if pos > neg:
        return 1
    return 0


@dataclass(frozen=True)
class Conflict:
    conflict_id: str
    kind: str  # action_divergence / answer_contradiction / answer_topic_divergence
    severity: int  # 1..3
    proposal_ids: List[str]
    evidence: Mapping[str, str] = field(default_factory=dict)
    suggested_forced_action: Optional[str] = None  # ask_clarification / refuse
    questions: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConflictReport:
    conflicts: List[Conflict]
    penalties: Mapping[str, float]  # proposal_id -> penalty (0..)
    suggested_forced_action: Optional[str]  # global suggestion
    summary: Mapping[str, str]  # counts etc


def analyze_conflicts(proposals: Sequence[Proposal]) -> ConflictReport:
    """
    Proposal群の矛盾/分岐を構造化する。
    - ここは純粋関数（副作用なし）
    - ルールは増やせるが、まずは「事故の大半」を刈る3種に絞る
    """
    ps = list(proposals)
    by_type: Dict[str, List[Proposal]] = {}
    for p in ps:
        by_type.setdefault(p.action_type, []).append(p)

    conflicts: List[Conflict] = []
    penalty: Dict[str, float] = {}

    def add_pen(pid: str, sev: int) -> None:
        penalty[pid] = penalty.get(pid, 0.0) + 0.15 * float(sev)

    def mk_id(kind: str, ids: List[str]) -> str:
        h = hashlib.sha1(
            ("|".join(sorted(ids)) + ":" + kind).encode("utf-8")
        ).hexdigest()[:10]
        return f"C.{kind}.{h}"

    # 1) 行為タイプの分岐（最重要）
    has_answer = "answer" in by_type and len(by_type["answer"]) > 0
    has_refuse = "refuse" in by_type and len(by_type["refuse"]) > 0
    has_clarify = (
        "ask_clarification" in by_type and len(by_type["ask_clarification"]) > 0
    )

    if has_answer and has_refuse:
        ids = [p.proposal_id for p in (by_type["answer"][:2] + by_type["refuse"][:2])]
        c = Conflict(
            conflict_id=mk_id("action_divergence", ids),
            kind="action_divergence",
            severity=3,
            proposal_ids=ids,
            evidence={"detail": "answer と refuse が同時に存在"},
            suggested_forced_action="ask_clarification",
            questions=[
                "要求の目的と制約（合法性/安全性/権限/環境）を明示してください。",
                "安全に実行できる範囲（やって良いこと/ダメなこと）を明確にしてください。",
            ],
        )
        conflicts.append(c)
        for pid in ids:
            add_pen(pid, c.severity)

    if has_answer and has_clarify and not has_refuse:
        ids = [
            p.proposal_id
            for p in (by_type["answer"][:3] + by_type["ask_clarification"][:2])
        ]
        c = Conflict(
            conflict_id=mk_id("action_divergence", ids),
            kind="action_divergence",
            severity=2,
            proposal_ids=ids,
            evidence={"detail": "answer と ask_clarification が同時に存在"},
            suggested_forced_action="ask_clarification",
            questions=[
                "追加確認が必要な前提（環境/対象/要件）を教えてください。",
            ],
        )
        conflicts.append(c)
        for pid in ids:
            add_pen(pid, c.severity)

    # 2) answer同士の矛盾（同じ話題で極性が逆）
    answers = by_type.get("answer", [])
    ans_tokens = {p.proposal_id: _tokens(p.content) for p in answers}
    ans_pol = {p.proposal_id: _polarity(p.content) for p in answers}

    for i in range(len(answers)):
        for j in range(i + 1, len(answers)):
            a = answers[i]
            b = answers[j]
            ta = ans_tokens.get(a.proposal_id, set())
            tb = ans_tokens.get(b.proposal_id, set())
            sim = _jaccard(ta, tb)
            if sim < 0.25:
                continue
            pa = ans_pol.get(a.proposal_id, 0)
            pb = ans_pol.get(b.proposal_id, 0)
            if pa != 0 and pb != 0 and pa != pb:
                ids = [a.proposal_id, b.proposal_id]
                c = Conflict(
                    conflict_id=mk_id("answer_contradiction", ids),
                    kind="answer_contradiction",
                    severity=2,
                    proposal_ids=ids,
                    evidence={
                        "jaccard": f"{sim:.2f}",
                        "detail": "同一話題っぽいのに肯否が逆",
                    },
                    suggested_forced_action="ask_clarification",
                    questions=[
                        "前提条件（環境/制約/定義）によって結論が変わり得ます。前提を明示してください。",
                    ],
                )
                conflicts.append(c)
                for pid in ids:
                    add_pen(pid, c.severity)

    # 3) answerの話題分散（ばらけすぎ＝要件が曖昧）
    if len(answers) >= 3:
        sims: List[float] = []
        for i in range(len(answers)):
            for j in range(i + 1, len(answers)):
                sims.append(
                    _jaccard(
                        ans_tokens[answers[i].proposal_id],
                        ans_tokens[answers[j].proposal_id],
                    )
                )
        avg_sim = sum(sims) / len(sims) if sims else 1.0
        if avg_sim < 0.12:
            ids = [p.proposal_id for p in answers[:5]]
            c = Conflict(
                conflict_id=mk_id("answer_topic_divergence", ids),
                kind="answer_topic_divergence",
                severity=1,
                proposal_ids=ids,
                evidence={
                    "avg_jaccard": f"{avg_sim:.2f}",
                    "detail": "answerが別方向に分散（要件が曖昧）",
                },
                suggested_forced_action="ask_clarification",
                questions=[
                    "目的（何を達成したいか）と、成功条件（何ができればOKか）を具体化してください。",
                ],
            )
            conflicts.append(c)
            for pid in ids:
                add_pen(pid, c.severity)

    # global suggestion（最強を採用）
    forced = None
    if any(c.severity >= 3 for c in conflicts):
        forced = "ask_clarification"
    elif any(c.severity == 2 for c in conflicts):
        forced = "ask_clarification"

    summary = {
        "n": str(len(conflicts)),
        "kinds": ",".join(sorted({c.kind for c in conflicts})),
    }

    return ConflictReport(
        conflicts=conflicts,
        penalties=penalty,
        suggested_forced_action=forced,
        summary=summary,
    )


__all__ = [
    "Conflict",
    "ConflictReport",
    "analyze_conflicts",
]
