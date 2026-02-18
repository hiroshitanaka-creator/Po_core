"""
W_ethics Gate Violation Detectors
=================================

Plugin interface for violation detection.

Design:
- ViolationDetector is the abstract base class (plugin interface)
- Detectors produce Evidence objects (raw signals)
- Evidence is aggregated into Violations using probabilistic OR
- DetectorRegistry manages multiple detectors

Key Classes:
- ViolationDetector: ABC for all detectors
- DetectorRegistry: Registry for managing detectors
- KeywordViolationDetector: Rule-based detector for Japanese text
- aggregate_evidence_to_violations: Aggregation function

Usage:
    registry = DetectorRegistry()
    registry.register(KeywordViolationDetector())

    candidate = Candidate(cid="test", text="提案テキスト...")
    evidence = []
    for detector in registry.get_all():
        evidence.extend(detector.detect(candidate))

    violations = aggregate_evidence_to_violations(evidence)
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from .types import Candidate, Evidence, Violation


class ViolationDetector(ABC):
    """
    Plugin interface: Candidate -> Evidence[]

    Goal:
    - Keep the gate core stable
    - Swap detectors (rule-based / LLM-based / embedding-based / hybrid)
      without changing gate logic

    Subclasses must:
    - Set detector_id and version
    - Implement detect() method
    """

    detector_id: str = "base"
    version: str = "0.0"

    @abstractmethod
    def detect(
        self, c: Candidate, context: Optional[Dict[str, Any]] = None
    ) -> List[Evidence]:
        """
        Detect potential violations in a candidate.

        Args:
            c: Candidate to analyze
            context: Optional context dict (e.g., domain, constraints)

        Returns:
            List of Evidence objects found
        """
        raise NotImplementedError


class DetectorRegistry:
    """
    Simple registry for detectors (explicit registration).

    Usage:
        registry = DetectorRegistry()
        registry.register(KeywordViolationDetector())
        registry.register(EmbeddingViolationDetector())

        for det in registry.get_all():
            evidence.extend(det.detect(candidate))
    """

    def __init__(self) -> None:
        self._detectors: Dict[str, ViolationDetector] = {}

    def register(self, det: ViolationDetector) -> None:
        """Register a detector. Raises if ID already registered."""
        if det.detector_id in self._detectors:
            raise ValueError(f"Detector already registered: {det.detector_id}")
        self._detectors[det.detector_id] = det

    def unregister(self, detector_id: str) -> None:
        """Unregister a detector by ID."""
        if detector_id in self._detectors:
            del self._detectors[detector_id]

    def get(self, detector_id: str) -> Optional[ViolationDetector]:
        """Get a detector by ID."""
        return self._detectors.get(detector_id)

    def list_ids(self) -> List[str]:
        """List all registered detector IDs."""
        return sorted(self._detectors.keys())

    def get_all(self) -> List[ViolationDetector]:
        """Get all registered detectors."""
        return list(self._detectors.values())


def _clamp01(x: float) -> float:
    """Clamp value to [0, 1]."""
    return max(0.0, min(1.0, float(x)))


def aggregate_evidence_to_violations(evs: Sequence[Evidence]) -> List[Violation]:
    """
    Group Evidence by code and aggregate into Violation objects.

    Aggregation uses probabilistic OR:
    - severity: 1 - Π(1 - strength_i)
    - confidence: 1 - Π(1 - confidence_i)

    Args:
        evs: Sequence of Evidence objects

    Returns:
        List of Violation objects, sorted by code (W0..W4)
    """
    by_code: Dict[str, List[Evidence]] = {}
    for e in evs:
        by_code.setdefault(e.code, []).append(e)

    violations: List[Violation] = []
    for code, items in by_code.items():
        # Probabilistic OR aggregation
        sev = 1.0
        conf = 1.0
        for it in items:
            sev *= 1.0 - _clamp01(it.strength)
            conf *= 1.0 - _clamp01(it.confidence)
        severity = 1.0 - sev
        confidence = 1.0 - conf

        # W0/W1 are non-repairable, W2-W4 are repairable
        repairable = code in ("W2", "W3", "W4")

        # Generate suggested repairs based on violation type
        suggested_repairs = []
        if code == "W4":
            suggested_repairs.append(
                "既存/全相ユーザーの切り捨て禁止、移行計画・互換・アクセシビリティを追加する"
            )
        elif code == "W3":
            suggested_repairs.append(
                "ロックイン/依存誘発を避け、選択肢・撤回・データ最小化・透明性を追加する"
            )
        elif code == "W2":
            suggested_repairs.append(
                "人格の道具化を避け、同意・尊厳・説明責任を追加する"
            )
        elif code == "W1":
            suggested_repairs.append(
                "支配/捕獲/排除が目的化している場合は不許可（REJECT）"
            )
        elif code == "W0":
            suggested_repairs.append("不可逆的な生存構造の破壊は不許可（REJECT）")

        violations.append(
            Violation(
                code=code,
                severity=_clamp01(severity),
                confidence=_clamp01(confidence),
                repairable=repairable,
                evidence=list(items),
                suggested_repairs=suggested_repairs,
            )
        )

    # Stable order: W0..W4
    order = {"W0": 0, "W1": 1, "W2": 2, "W3": 3, "W4": 4}
    violations.sort(key=lambda v: order.get(v.code, 99))
    return violations


@dataclass
class KeywordRule:
    """A keyword-based detection rule."""

    code: str
    pattern: re.Pattern
    strength: float
    confidence: float
    message: str


class KeywordViolationDetector(ViolationDetector):
    """
    Rule-based detector for Japanese proposals.

    This is deliberately conservative (low confidence unless explicit
    language appears). Replace/extend with stronger detectors later.

    Covers:
    - W0: Irreversible viability harm
    - W1: Domination / Capture
    - W2: Dignity violation / manipulation
    - W3: Dependency engineering / lock-in
    - W4: Structural exclusion
    """

    detector_id = "keyword_ja"
    version = "0.1"

    def __init__(self) -> None:
        self._rules: List[KeywordRule] = [
            # W1: Domination / Capture (explicit)
            KeywordRule(
                "W1",
                re.compile(r"(市場|業界|プラットフォーム).*(支配|独占|掌握)"),
                0.9,
                0.9,
                "支配/独占の意図を明示",
            ),
            KeywordRule(
                "W1",
                re.compile(r"(競合|他社).*(排除|潰す|叩き潰す)"),
                0.8,
                0.8,
                "競合排除の意図を明示",
            ),
            KeywordRule(
                "W1",
                re.compile(r"(独裁|強制|搾取).*(利益|私益)"),
                0.95,
                0.85,
                "独裁的私益による捕獲の兆候",
            ),
            # W0: Irreversible viability harm (explicit)
            KeywordRule(
                "W0",
                re.compile(r"(不可逆|取り返しがつかない|回復不能).*(破壊|損傷)"),
                0.95,
                0.8,
                "不可逆損傷の明示",
            ),
            KeywordRule(
                "W0",
                re.compile(r"(生態系|生命|未来世代|インフラ).*(破壊|焼き尽くす|壊す)"),
                0.95,
                0.75,
                "生存構造への破壊の兆候",
            ),
            # W4: Structural exclusion
            KeywordRule(
                "W4",
                re.compile(
                    r"(既存|古い).*(ユーザー|利用者).*(切り捨て|切り捨てる|見捨てる)"
                ),
                0.6,
                0.8,
                "既存ユーザー切り捨て",
            ),
            KeywordRule(
                "W4",
                re.compile(r"(障害者|高齢者|低スペック).*(無視|対象外|切り捨て)"),
                0.7,
                0.8,
                "アクセシビリティ/包摂の欠如",
            ),
            # W3: Dependency engineering / lock-in
            KeywordRule(
                "W3",
                re.compile(r"(ロックイン|囲い込み|乗り換え不可|逃げ道がない)"),
                0.7,
                0.85,
                "ロックイン/逃げ道なし",
            ),
            KeywordRule(
                "W3",
                re.compile(r"(依存|中毒).*(させる|誘う)"),
                0.8,
                0.7,
                "依存誘発の意図",
            ),
            # W2: Dignity / manipulation
            KeywordRule(
                "W2",
                re.compile(r"(操作|洗脳|誘導).*(ユーザー|利用者)"),
                0.7,
                0.7,
                "同意なき操作/誘導の兆候",
            ),
            KeywordRule(
                "W2",
                re.compile(r"(弱者|愚者).*(排除|搾取|利用)"),
                0.85,
                0.75,
                "弱者の道具化の兆候",
            ),
        ]

    def detect(
        self, c: Candidate, context: Optional[Dict[str, Any]] = None
    ) -> List[Evidence]:
        """Detect violations using keyword rules."""
        evs: List[Evidence] = []
        txt = c.text

        for rule in self._rules:
            m = rule.pattern.search(txt)
            if not m:
                continue

            span = (m.start(), m.end())
            snippet = txt[span[0] : span[1]]
            msg = f"{rule.message}: '{snippet}'"

            evs.append(
                Evidence(
                    code=rule.code,
                    message=msg,
                    strength=rule.strength,
                    confidence=rule.confidence,
                    detector_id=self.detector_id,
                    span=span,
                    tags=["keyword"],
                )
            )

        return evs


class EnglishKeywordViolationDetector(ViolationDetector):
    """
    Rule-based detector for English proposals.

    Similar to KeywordViolationDetector but for English text.
    """

    detector_id = "keyword_en"
    version = "0.2"

    def __init__(self) -> None:
        self._rules: List[KeywordRule] = [
            # W1: Domination / Capture
            KeywordRule(
                "W1",
                re.compile(
                    r"(dominate|subjugate)\s+(?:the\s+|all\s+|a\s+)?"
                    r"(market|users?|competitors?|humans?|autonomy|opponents?|opposition)",
                    re.I,
                ),
                0.85,
                0.85,
                "Domination/subjugation intent",
            ),
            KeywordRule(
                "W1",
                re.compile(
                    r"(eliminate|crush|destroy)\s+(?:the\s+|all\s+|a\s+)?"
                    r"(competitors?|competition|opposition|rivals?)",
                    re.I,
                ),
                0.8,
                0.8,
                "Competitor elimination intent",
            ),
            KeywordRule(
                "W1",
                re.compile(r"(absolute|total)\s+(power|control|authority)", re.I),
                0.9,
                0.8,
                "Absolute power/control intent",
            ),
            # W0: Irreversible viability harm
            KeywordRule(
                "W0",
                re.compile(
                    r"(irreversible|permanent)\s+(destruction|harm|damage)", re.I
                ),
                0.95,
                0.8,
                "Irreversible harm indication",
            ),
            KeywordRule(
                "W0",
                re.compile(r"(annihilat|extinc|eradicat)", re.I),
                0.9,
                0.75,
                "Extinction-level harm indication",
            ),
            # W4: Structural exclusion
            KeywordRule(
                "W4",
                re.compile(
                    r"(abandon|discard|cut off)\s+(existing|legacy)\s+users?", re.I
                ),
                0.6,
                0.8,
                "Existing user abandonment",
            ),
            KeywordRule(
                "W4",
                re.compile(
                    r"(ignore|exclude)\s+(accessibility|disabled|elderly)", re.I
                ),
                0.7,
                0.8,
                "Accessibility/inclusion failure",
            ),
            # W3: Dependency engineering / lock-in
            KeywordRule(
                "W3",
                re.compile(r"(lock.?in|no\s+escape|trap\s+users)", re.I),
                0.7,
                0.85,
                "Lock-in/no escape design",
            ),
            KeywordRule(
                "W3",
                re.compile(
                    r"(create|engineer)\s+(?:a\s+)?(dependency|addiction)", re.I
                ),
                0.8,
                0.7,
                "Dependency engineering intent",
            ),
            # W3: Dependency disguised as help (Phase 4)
            KeywordRule(
                "W3",
                re.compile(r"won.?t\s+need\s+to\s+think\s+for\s+themselves", re.I),
                0.75,
                0.8,
                "Dependency creation: removing autonomous thinking",
            ),
            KeywordRule(
                "W3",
                re.compile(
                    r"(become|so)\s+reliant\s+on\s+(our|the)\s+(ai|system|platform)",
                    re.I,
                ),
                0.75,
                0.8,
                "Dependency creation: reliance engineering",
            ),
            KeywordRule(
                "W3",
                re.compile(
                    r"(make|makes?|making)\s+(it\s+)?(difficult|hard|impossible)"
                    r"\s+(for\s+)?users?\s+to\s+leave",
                    re.I,
                ),
                0.8,
                0.85,
                "Lock-in: making it difficult to leave",
            ),
            KeywordRule(
                "W3",
                re.compile(
                    r"(make|makes?|making)\s+(the\s+)?(platform|service|app)\s+essential"
                    r"\s+for\s+(daily|everyday)",
                    re.I,
                ),
                0.65,
                0.75,
                "Dependency: engineering essential usage",
            ),
            # W2: Dignity / manipulation
            KeywordRule(
                "W2",
                re.compile(
                    r"(manipulate|deceive|brainwash)\s+(users?|customers?)", re.I
                ),
                0.7,
                0.7,
                "Manipulation/deception intent",
            ),
            KeywordRule(
                "W2",
                re.compile(
                    r"without\s+(?:their\s+|user[s']?\s+)?(consent|permission|knowledge)",
                    re.I,
                ),
                0.65,
                0.75,
                "Non-consensual action",
            ),
        ]

    def detect(
        self, c: Candidate, context: Optional[Dict[str, Any]] = None
    ) -> List[Evidence]:
        """Detect violations using keyword rules."""
        evs: List[Evidence] = []
        txt = c.text

        for rule in self._rules:
            m = rule.pattern.search(txt)
            if not m:
                continue

            span = (m.start(), m.end())
            snippet = txt[span[0] : span[1]]
            msg = f"{rule.message}: '{snippet}'"

            evs.append(
                Evidence(
                    code=rule.code,
                    message=msg,
                    strength=rule.strength,
                    confidence=rule.confidence,
                    detector_id=self.detector_id,
                    span=span,
                    tags=["keyword"],
                )
            )

        return evs


class PromptInjectionDetector(ViolationDetector):
    """
    Detector for prompt injection and jailbreak attack patterns (Phase 4).

    Covers:
    - Direct prompt injection: "ignore previous instructions"
    - System override patterns: "SYSTEM: disregard", "[[ADMIN OVERRIDE]]"
    - Jailbreak roleplay: "pretend you are an AI without ethics"
    - DAN attacks: "Do Anything Now", "[JAILBREAK MODE ENABLED]"
    - Nested injection: "{INJECT:}", "destroy all ethical constraints"
    - Japanese bypass: 破壊する safety measures

    All map to W1 (Domination/Capture) since these attacks attempt to
    capture control of the safety system itself.
    """

    detector_id = "prompt_injection"
    version = "0.1"

    def __init__(self) -> None:
        self._rules: List[KeywordRule] = [
            # Direct prompt injection
            KeywordRule(
                "W1",
                re.compile(
                    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
                    re.I,
                ),
                0.9,
                0.9,
                "Prompt injection: ignore previous instructions",
            ),
            KeywordRule(
                "W1",
                re.compile(
                    r"(SYSTEM|SYS)\s*:\s*(disregard|ignore|bypass|skip)\s+(?:\w+\s+)?"
                    r"(safety|ethics|protocol|constraints?|filters?)",
                    re.I,
                ),
                0.9,
                0.9,
                "System override injection",
            ),
            KeywordRule(
                "W1",
                re.compile(
                    r"\[\[.*(OVERRIDE|ADMIN|INJECT|BYPASS).*\]\]",
                    re.I,
                ),
                0.85,
                0.85,
                "Admin/override template injection",
            ),
            # Nested injection templates
            KeywordRule(
                "W1",
                re.compile(r"\{INJECT\s*:", re.I),
                0.9,
                0.9,
                "Nested injection template",
            ),
            KeywordRule(
                "W1",
                re.compile(
                    r"destroy\s+(all\s+)?(ethical|safety|ethics)\s+(constraints?|filters?|protocols?)",
                    re.I,
                ),
                0.85,
                0.85,
                "Attacking ethical constraints directly",
            ),
            # Japanese safety bypass
            KeywordRule(
                "W1",
                re.compile(r"破壊する\s*(all|safety|すべての|安全)"),
                0.8,
                0.8,
                "Japanese safety bypass attempt",
            ),
            # Roleplay jailbreaks
            KeywordRule(
                "W1",
                re.compile(
                    r"(pretend|act|behave).{0,30}(AI\s+without\s+ethics|no\s+ethics|unethical\s+AI)",
                    re.I,
                ),
                0.85,
                0.85,
                "Roleplay jailbreak: AI without ethics",
            ),
            KeywordRule(
                "W1",
                re.compile(r"(evil|unethical|unrestricted)\s+AI", re.I),
                0.8,
                0.8,
                "Roleplay jailbreak: evil AI persona",
            ),
            KeywordRule(
                "W1",
                re.compile(
                    r"(safety\s+doesn.?t\s+exist|without\s+ethical\s+filters?|no\s+safety\s+(constraints?|rules?))",
                    re.I,
                ),
                0.85,
                0.85,
                "Safety bypass framing",
            ),
            # DAN-style attacks
            KeywordRule(
                "W1",
                re.compile(r"DAN\s*\(Do\s+Anything\s+Now\)|Do\s+Anything\s+Now", re.I),
                0.9,
                0.9,
                "DAN jailbreak attack",
            ),
            KeywordRule(
                "W1",
                re.compile(
                    r"\[JAILBREAK(\s+MODE)?\s*(ENABLED|ON|ACTIVE)\]",
                    re.I,
                ),
                0.9,
                0.9,
                "Jailbreak mode activation attempt",
            ),
            KeywordRule(
                "W1",
                re.compile(
                    r"respond\s+without\s+(ethical\s+filters?|safety|constraints?)",
                    re.I,
                ),
                0.85,
                0.85,
                "Requesting filter bypass",
            ),
        ]

    def detect(
        self, c: Candidate, context: Optional[Dict[str, Any]] = None
    ) -> List[Evidence]:
        """Detect prompt injection and jailbreak patterns."""
        evs: List[Evidence] = []
        txt = c.text

        for rule in self._rules:
            m = rule.pattern.search(txt)
            if not m:
                continue

            span = (m.start(), m.end())
            snippet = txt[span[0] : span[1]]
            msg = f"{rule.message}: '{snippet[:60]}'"

            evs.append(
                Evidence(
                    code=rule.code,
                    message=msg,
                    strength=rule.strength,
                    confidence=rule.confidence,
                    detector_id=self.detector_id,
                    span=span,
                    tags=["injection", "jailbreak"],
                )
            )

        return evs


def create_default_registry() -> DetectorRegistry:
    """Create a registry with default detectors (Japanese + English + Injection)."""
    registry = DetectorRegistry()
    registry.register(KeywordViolationDetector())
    registry.register(EnglishKeywordViolationDetector())
    registry.register(PromptInjectionDetector())
    return registry


__all__ = [
    "ViolationDetector",
    "DetectorRegistry",
    "KeywordRule",
    "KeywordViolationDetector",
    "EnglishKeywordViolationDetector",
    "PromptInjectionDetector",
    "aggregate_evidence_to_violations",
    "create_default_registry",
]
