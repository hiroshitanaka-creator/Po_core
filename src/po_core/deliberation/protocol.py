from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
)

from po_core.domain.keys import AUTHOR, PO_CORE
from po_core.domain.proposal import Proposal


@dataclass(frozen=True)
class ArgumentCard:
    """Minimal normalized argument card for deliberation protocol v1."""

    philosopher: str
    proposal_id: str
    stance: str
    claims: List[str]
    confidence: float
    source: Proposal


@dataclass(frozen=True)
class CritiqueCard:
    """Structured critique emitted by one philosopher toward another card."""

    critic: str
    target: str
    target_proposal_id: str
    weakness: str
    detail: str
    question: str


class SynthesisEngine:
    """Protocol v1 synthesis: summarize disagreements and open questions."""

    def build_report(
        self,
        cards: Sequence[ArgumentCard],
        critiques: Sequence[CritiqueCard],
        axis_spec: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        axis = list(axis_spec.get("axes", [])) if isinstance(axis_spec, Mapping) else []
        disagreements = [
            {
                "between": [c.critic, c.target],
                "weakness": c.weakness,
                "detail": c.detail,
            }
            for c in critiques
        ]
        open_questions = sorted({c.question for c in critiques if c.question})
        return {
            "protocol": "v1",
            "axes": axis,
            "n_cards": len(cards),
            "n_critiques": len(critiques),
            "disagreements": disagreements,
            "open_questions": open_questions,
            "consensus": _consensus_snapshot(cards),
        }


def run_deliberation(
    input: Mapping[str, Any],
    philosophers: Sequence[Any],
    axis_spec: Optional[Mapping[str, Any]],
    settings: Optional[Mapping[str, Any]],
) -> Tuple[List[ArgumentCard], List[CritiqueCard], Dict[str, Any]]:
    """
    Protocol v1: Propose -> Critique -> Synthesize.

    Returns:
        (cards, critiques, report)
    """
    cards = _run_propose(input, philosophers, axis_spec, settings)
    critiques = _run_critique(cards, philosophers, axis_spec, settings)
    report = SynthesisEngine().build_report(cards, critiques, axis_spec=axis_spec)
    return cards, critiques, report


def _run_propose(
    input: Mapping[str, Any],
    philosophers: Sequence[Any],
    axis_spec: Optional[Mapping[str, Any]],
    settings: Optional[Mapping[str, Any]],
) -> List[ArgumentCard]:
    cards: List[ArgumentCard] = []
    for ph in philosophers:
        if hasattr(ph, "propose_card"):
            card = ph.propose_card(input, axis_spec, settings)
            if card is not None:
                cards.append(_coerce_argument_card(card, ph))
            continue

        if hasattr(ph, "propose"):
            proposal = _best_effort_propose(ph, input)
            if proposal is not None:
                cards.append(_proposal_to_card(proposal, _ph_name(ph)))
    return cards


def _run_critique(
    cards: Sequence[ArgumentCard],
    philosophers: Sequence[Any],
    axis_spec: Optional[Mapping[str, Any]],
    settings: Optional[Mapping[str, Any]],
) -> List[CritiqueCard]:
    if len(cards) < 2:
        return []

    max_targets = int((settings or {}).get("max_critiques_per_philosopher", 2))
    max_targets = max(1, min(2, max_targets))

    cards_by_name = {c.philosopher: c for c in cards}
    critiques: List[CritiqueCard] = []
    for ph in philosophers:
        critic = _ph_name(ph)
        src = cards_by_name.get(critic)
        if src is None:
            continue
        targets = _select_targets(src, cards, max_targets=max_targets)

        for target in targets:
            if hasattr(ph, "critique_card"):
                raw = ph.critique_card(target, axis_spec)
                critique = _coerce_critique_card(raw, critic=critic, target=target)
            else:
                critique = _default_critique_card(critic, target)
            critiques.append(critique)

    if not critiques:
        # Failsafe to avoid empty critique stage.
        first, second = cards[0], cards[1]
        critiques.append(_default_critique_card(first.philosopher, second))
    return critiques


def _best_effort_propose(ph: Any, input: Mapping[str, Any]) -> Optional[Proposal]:
    try:
        raw = ph.propose(input, None, None, None)
    except TypeError:
        return None
    except Exception:
        return None
    if not raw:
        return None
    proposal = raw[0]
    return proposal if isinstance(proposal, Proposal) else None


def _proposal_to_card(proposal: Proposal, fallback_name: str) -> ArgumentCard:
    extra = proposal.extra if isinstance(proposal.extra, Mapping) else {}
    po_core_meta = extra.get(PO_CORE, {}) if isinstance(extra, Mapping) else {}
    author = ""
    if isinstance(po_core_meta, Mapping):
        author = str(po_core_meta.get(AUTHOR, ""))
    if not author:
        author = str(extra.get("philosopher", fallback_name))

    claims = _split_claims(proposal.content)
    stance = _infer_stance(proposal.content)
    return ArgumentCard(
        philosopher=author,
        proposal_id=proposal.proposal_id,
        stance=stance,
        claims=claims,
        confidence=float(proposal.confidence),
        source=proposal,
    )


def _coerce_argument_card(raw: Any, ph: Any) -> ArgumentCard:
    if isinstance(raw, ArgumentCard):
        return raw
    if isinstance(raw, Mapping):
        proposal = raw.get("source")
        if not isinstance(proposal, Proposal):
            proposal = Proposal(
                proposal_id=str(raw.get("proposal_id", f"{_ph_name(ph)}:0")),
                action_type="answer",
                content="\n".join(raw.get("claims", [])) if raw.get("claims") else "",
                confidence=float(raw.get("confidence", 0.5)),
                extra={"philosopher": str(raw.get("philosopher", _ph_name(ph)))},
            )
        return ArgumentCard(
            philosopher=str(raw.get("philosopher", _ph_name(ph))),
            proposal_id=str(raw.get("proposal_id", proposal.proposal_id)),
            stance=str(raw.get("stance", _infer_stance(proposal.content))),
            claims=list(raw.get("claims", _split_claims(proposal.content))),
            confidence=float(raw.get("confidence", proposal.confidence)),
            source=proposal,
        )
    raise TypeError("Unsupported propose_card return type")


def _coerce_critique_card(
    raw: Any, *, critic: str, target: ArgumentCard
) -> CritiqueCard:
    if isinstance(raw, CritiqueCard):
        return raw
    if isinstance(raw, Mapping):
        return CritiqueCard(
            critic=str(raw.get("critic", critic)),
            target=str(raw.get("target", target.philosopher)),
            target_proposal_id=str(raw.get("target_proposal_id", target.proposal_id)),
            weakness=str(raw.get("weakness", "insufficient_information")),
            detail=str(raw.get("detail", "Key assumptions are not explicit.")),
            question=str(raw.get("question", "What evidence would change this view?")),
        )
    return _default_critique_card(critic, target)


def _default_critique_card(critic: str, target: ArgumentCard) -> CritiqueCard:
    joined = " ".join(target.claims).lower()
    weakness = "insufficient_information"
    detail = "前提が十分に定義されていません。"
    question = "どの条件が満たされれば主張を支持できますか？"
    if "risk" not in joined and "リスク" not in joined:
        weakness = "risk_not_explicit"
        detail = "リスク・副作用の明示が不足しています。"
        question = "主要な失敗モードと緩和策は何ですか？"
    elif "?" not in joined and "question" not in joined:
        weakness = "questions_missing"
        detail = "検証のための問いが不足しています。"
        question = "反証可能な問いを1つ提示できますか？"

    return CritiqueCard(
        critic=critic,
        target=target.philosopher,
        target_proposal_id=target.proposal_id,
        weakness=weakness,
        detail=detail,
        question=question,
    )


def _select_targets(
    src: ArgumentCard,
    cards: Sequence[ArgumentCard],
    *,
    max_targets: int,
) -> List[ArgumentCard]:
    others = [c for c in cards if c.philosopher != src.philosopher]
    if not others:
        return []

    preferred = sorted(
        others,
        key=lambda c: (
            0 if c.stance != src.stance else 1,
            -float(c.confidence),
            c.philosopher,
        ),
    )
    return preferred[:max_targets]


def _infer_stance(text: str) -> str:
    t = text.lower()
    if "against" in t or "oppose" in t or "reject" in t:
        return "con"
    if "for" in t or "support" in t or "endorse" in t:
        return "pro"
    return "neutral"


def _split_claims(text: str) -> List[str]:
    chunks = [c.strip() for c in text.replace("\n", ". ").split(".")]
    claims = [c for c in chunks if c]
    return claims[:3] if claims else ["(no explicit claim)"]


def _consensus_snapshot(cards: Sequence[ArgumentCard]) -> Dict[str, int]:
    tally: Dict[str, int] = {"pro": 0, "con": 0, "neutral": 0}
    for c in cards:
        stance = c.stance if c.stance in tally else "neutral"
        tally[stance] += 1
    return tally


def _ph_name(ph: Any) -> str:
    return str(getattr(ph, "name", ph.__class__.__name__))
