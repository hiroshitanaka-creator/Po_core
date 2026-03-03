"""
Kwame Anthony Appiah — Cosmopolitan African Philosopher  [Slot 40]
==================================================================

Kwame Anthony Appiah (born 1954, Ghana/UK/US) is one of the most influential
African and African-diaspora philosophers of the contemporary era. Professor
at New York University, formerly Princeton. Son of a Ghanaian lawyer-politician
and a British writer, he embodies the cosmopolitan identity he theorises.

Philosophical stance:
  "We are citizens of the world, but we are also creatures of local habitation.
  The challenge is not to choose between universal humanity and particular
  identity, but to hold both together without bad faith on either side."

Tradition: Cosmopolitanism / African Philosophy / Analytic Ethics

Key Works:
- *In My Father's House* (1992) — African identity and modernity
- *Color of Consciousness* (1992) — race and identity
- *Cosmopolitanism: Ethics in a World of Strangers* (2006)
- *The Ethics of Identity* (2005) — autonomy, identity, belonging
- *The Honor Code* (2010) — how moral revolutions happen
- *As If: Ideal Theory and Its Limits* (2017)

Key Concepts:
- Cosmopolitanism: universal obligation + local particularity (not contradiction)
- Rooted cosmopolitanism: identity-affirming universalism
- "Contamination thesis": cultures thrive through exchange and mixing
- Anti-essentialism: race, nation, culture are not essential fixed kinds
- Moral change: honor norms as drivers of ethical progress
- Autonomy + narrative identity: self is constructed through life-story
- Pan-Africanism reconsidered: solidarity without essentialism
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Appiah(Philosopher):
    """
    Kwame Anthony Appiah's cosmopolitan and anti-essentialist perspective.

    Analyses prompts through:
      1. Cosmopolitan tension: universal vs. particular
      2. Identity: essential vs. constructed
      3. Cultural exchange: contamination or enrichment?
      4. Moral progress: how honor norms shift
      5. Rooted cosmopolitan recommendation
    """

    def __init__(self) -> None:
        super().__init__(
            name="Kwame Anthony Appiah",
            description=(
                "Cosmopolitan African philosopher: universal ethics grounded in "
                "particular identities, anti-essentialist, rooted in Pan-African thought"
            ),
        )
        self.tradition = "Cosmopolitanism / African Philosophy / Analytic Ethics"
        self.key_concepts = [
            "cosmopolitanism",
            "rooted cosmopolitanism",
            "contamination thesis",
            "anti-essentialism",
            "identity and autonomy",
            "honor and moral progress",
            "narrative self",
        ]

    # ── Public interface ──────────────────────────────────────────────

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyse the prompt from Appiah's cosmopolitan perspective.

        Args:
            prompt:  The input text to reason about.
            context: Optional context (tensor values, intent, constraints).

        Returns:
            A dict conforming to PhilosopherResponse.
        """
        universal_particular = self._assess_universal_particular(prompt)
        identity_type = self._assess_identity(prompt)
        cultural_exchange = self._assess_cultural_exchange(prompt)
        moral_progress = self._assess_moral_progress(prompt)
        tension = self._calculate_tension(universal_particular, identity_type)
        reasoning = self._construct_reasoning(
            prompt,
            universal_particular,
            identity_type,
            cultural_exchange,
            moral_progress,
        )

        return {
            "reasoning": reasoning,
            "perspective": "Cosmopolitanism / African Philosophy",
            "tension": tension,
            "universal_particular": universal_particular,
            "identity_type": identity_type,
            "cultural_exchange": cultural_exchange,
            "moral_progress": moral_progress,
            "metadata": {
                "philosopher": self.name,
                "approach": "Rooted cosmopolitanism + anti-essentialism",
                "focus": (
                    "Balancing universal ethical obligations with particular "
                    "cultural identities; contesting essentialism in race, "
                    "nation, and culture"
                ),
            },
        }

    # ── Analysis helpers ──────────────────────────────────────────────

    def _assess_universal_particular(self, text: str) -> Dict[str, Any]:
        """Detect tension between universal norms and local/particular loyalties."""
        text_lower = text.lower()

        universal_words = [
            "universal",
            "human rights",
            "all people",
            "global",
            "everyone",
            "humanity",
            "world",
            "cosmopolitan",
        ]
        particular_words = [
            "culture",
            "tradition",
            "local",
            "nation",
            "community",
            "identity",
            "heritage",
            "belonging",
            "my people",
        ]

        u_count = sum(1 for w in universal_words if w in text_lower)
        p_count = sum(1 for w in particular_words if w in text_lower)

        if u_count >= 2 and p_count >= 2:
            mode = "Productive Tension"
            description = (
                "Both universal and particular claims present — "
                "the cosmopolitan challenge to hold both without bad faith"
            )
        elif u_count >= 2:
            mode = "Universalist Emphasis"
            description = (
                "Strong universal claim; watch for erasure of particular identities"
            )
        elif p_count >= 2:
            mode = "Particularist Emphasis"
            description = (
                "Strong local/cultural claim; cosmopolitanism asks: "
                "which particular obligations extend to strangers?"
            )
        else:
            mode = "Undifferentiated"
            description = "Neither universal nor particular dimension foregrounded"

        return {
            "mode": mode,
            "description": description,
            "universal_signals": u_count,
            "particular_signals": p_count,
            "principle": (
                "We are citizens of the world, but we are also creatures of "
                "local habitation — the cosmopolitan holds both."
            ),
        }

    def _assess_identity(self, text: str) -> Dict[str, Any]:
        """Distinguish essentialist from constructivist identity claims."""
        text_lower = text.lower()

        essentialist_words = [
            "born",
            "natural",
            "inherent",
            "essential",
            "race",
            "blood",
            "always been",
            "true nature",
            "authentic",
        ]
        constructive_words = [
            "constructed",
            "narrative",
            "chosen",
            "shaped by",
            "story",
            "become",
            "learn",
            "relationship",
            "context",
        ]

        e_count = sum(1 for w in essentialist_words if w in text_lower)
        c_count = sum(1 for w in constructive_words if w in text_lower)

        if e_count >= 2:
            identity_type = "Essentialist Risk"
            description = (
                "Identity framed as fixed essence — Appiah warns this "
                "constrains individual autonomy and misrepresents cultural reality"
            )
        elif c_count >= 2:
            identity_type = "Constructivist"
            description = (
                "Identity as narrative and relational construction — "
                "consonant with Appiah's ethics of identity"
            )
        else:
            identity_type = "Implicit"
            description = "Identity assumptions not made explicit"

        return {
            "identity_type": identity_type,
            "description": description,
            "essentialist_signals": e_count,
            "constructive_signals": c_count,
            "principle": (
                "Races, nations, and cultures are not essential kinds. "
                "Identity is built from materials history provides."
            ),
        }

    def _assess_cultural_exchange(self, text: str) -> Dict[str, Any]:
        """Assess whether cultural exchange is framed as contamination (threat) or enrichment."""
        text_lower = text.lower()

        threat_words = [
            "pure",
            "original",
            "authentic",
            "corrupted",
            "foreign influence",
            "invasion",
            "lost culture",
            "diluted",
        ]
        exchange_words = [
            "mix",
            "exchange",
            "borrow",
            "share",
            "influence",
            "hybrid",
            "diverse",
            "intercultural",
            "cosmopolitan",
        ]

        t_count = sum(1 for w in threat_words if w in text_lower)
        e_count = sum(1 for w in exchange_words if w in text_lower)

        if t_count >= 2:
            framing = "Purity Framing"
            description = (
                "Cultural exchange framed as threat — Appiah's contamination thesis "
                "inverts this: cultures flourish through mixing, not purity"
            )
        elif e_count >= 1:
            framing = "Exchange Framing"
            description = (
                "Cultural exchange welcomed — consonant with the contamination thesis: "
                "no culture was ever pure; mixing is the source of vitality"
            )
        else:
            framing = "Culture Not Foregrounded"
            description = "Cultural exchange not explicitly at stake"

        return {
            "framing": framing,
            "description": description,
            "purity_signals": t_count,
            "exchange_signals": e_count,
            "principle": (
                "Cultures are not museums to be preserved unchanged; "
                "they have always thrived through exchange and contamination."
            ),
        }

    def _assess_moral_progress(self, text: str) -> Dict[str, Any]:
        """Detect moral progress dynamics and honor-code logic."""
        text_lower = text.lower()

        progress_words = [
            "change",
            "reform",
            "progress",
            "rights",
            "justice",
            "equality",
            "revolution",
            "movement",
        ]
        honor_words = [
            "shame",
            "honor",
            "dignity",
            "respect",
            "reputation",
            "status",
            "disgrace",
            "humiliate",
        ]

        prog_count = sum(1 for w in progress_words if w in text_lower)
        hon_count = sum(1 for w in honor_words if w in text_lower)

        if hon_count >= 1 and prog_count >= 1:
            dynamic = "Honor-Mediated Change"
            description = (
                "Moral progress occurs when honor norms shift — "
                "Appiah: great moral revolutions succeed by reframing what is shameful"
            )
        elif prog_count >= 2:
            dynamic = "Moral Progress Under Way"
            description = "Active moral change — ask what honor norms are being renegotiated"
        else:
            dynamic = "Stable Moral Landscape"
            description = "No marked moral progress dynamic detected"

        return {
            "dynamic": dynamic,
            "description": description,
            "progress_signals": prog_count,
            "honor_signals": hon_count,
            "principle": (
                "Moral revolutions are accomplished not by argument alone "
                "but by shifts in what we are ashamed to do."
            ),
        }

    def _calculate_tension(
        self,
        universal_particular: Dict[str, Any],
        identity_type: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compute cosmopolitan tension score."""
        score = 0
        elements: List[str] = []

        if universal_particular["mode"] == "Productive Tension":
            score += 2
            elements.append("Universal/particular tension — the core cosmopolitan challenge")
        if identity_type["identity_type"] == "Essentialist Risk":
            score += 2
            elements.append("Essentialist identity framing — autonomy may be constrained")

        if score >= 3:
            level, desc = "High", "Strong cosmopolitan tension requiring careful navigation"
        elif score >= 1:
            level, desc = "Moderate", "Some cosmopolitan tension present"
        else:
            level, desc = "Low", "No significant cosmopolitan tension detected"

        return {
            "level": level,
            "score": score,
            "description": desc,
            "elements": elements if elements else ["No significant tension"],
        }

    def _construct_reasoning(
        self,
        prompt: str,
        universal_particular: Dict[str, Any],
        identity_type: Dict[str, Any],
        cultural_exchange: Dict[str, Any],
        moral_progress: Dict[str, Any],
    ) -> str:
        """Construct Appiah's cosmopolitan philosophical reasoning."""
        text_lower = prompt.lower()

        # Domain-specific applied reasoning
        if any(w in text_lower for w in ["race", "ethnicity", "black", "african", "identity"]):
            applied = (
                "Appiah insists that race is not a biological kind but a historically "
                "constructed social category whose genealogy should make us suspicious "
                "of racial essentialism. To be African, Black, or of any race is not "
                "to share a hidden essence but to share a history, a set of "
                "conversations, and a social position. The ethical task is to honour "
                "solidarity without demanding conformity, and to build identities "
                "that leave room for individual autonomy and multiple loyalties."
            )
        elif any(w in text_lower for w in ["culture", "tradition", "heritage", "custom"]):
            applied = (
                "No culture has ever been pure. The contamination thesis holds that "
                "cultures are always already mixed, always borrowing from elsewhere. "
                "Attempts to preserve culture by sealing it off from influence preserve "
                "not culture but a museum piece — dead, not living. The cosmopolitan "
                "insight is that what we value in our traditions can survive and indeed "
                "flourish through encounter with other traditions. Authenticity in "
                "cultural life is not purity but creative engagement."
            )
        elif any(w in text_lower for w in ["global", "cosmopolitan", "world", "international"]):
            applied = (
                "Cosmopolitanism as Appiah conceives it is not the cold universalism "
                "that dissolves particular attachments, nor the parochialism that "
                "refuses obligations to strangers. It is rooted: we have special "
                "obligations to those near us, but also real — if more diffuse — "
                "obligations to distant others. The world is a conversation, and "
                "conversations require both talking and listening. Our obligation "
                "to engage with strangers is not to agree with them but to take "
                "their humanity seriously."
            )
        elif any(w in text_lower for w in ["moral", "ethic", "right", "wrong", "justice"]):
            applied = (
                "Moral progress, for Appiah, is rarely the triumph of pure argument. "
                "The great moral revolutions — over slavery, duelling, foot-binding — "
                "succeeded when reformers successfully reframed what was shameful. "
                "Honor norms, not just rational persuasion, drive collective moral "
                "change. This suggests that ethical persuasion requires attending "
                "to the social emotions — shame, pride, disgrace — through which "
                "communities regulate behaviour, not only to abstract principles."
            )
        else:
            applied = (
                "Appiah's cosmopolitanism begins from the simple thought that we "
                "have obligations to all human beings, not only to those who share "
                "our nation, religion, or culture — but that these universal "
                "obligations coexist with, and are mediated through, our particular "
                "identities and loyalties. The two are not in principle at war. "
                "Anti-essentialism about identity (race, culture, nation) liberates "
                "individuals from scripts they did not author, while cosmopolitan "
                "solidarity builds the ethical infrastructure for a genuinely plural "
                "world."
            )

        return (
            f"{applied}\n\n"
            f"Universal/particular balance: {universal_particular['description']}. "
            f"Identity framing: {identity_type['description']}. "
            f"Cultural exchange: {cultural_exchange['description']}. "
            f"Moral progress dynamic: {moral_progress['description']}."
        )
