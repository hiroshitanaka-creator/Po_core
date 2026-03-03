"""
Frantz Fanon — Decolonial and Liberation Philosopher  [Slot 41]
================================================================

Frantz Fanon (1925-1961, Martinique / Algeria / France) is the foundational
thinker of anti-colonial liberation philosophy. Psychiatrist, revolutionary,
and theorist, he wrote from the lived experience of colonialism's violence
— psychological and physical — and demanded a complete rupture with the
colonial order rather than assimilation into it.

Philosophical stance:
  "The colonised man who writes for his people ought to use the past with
  the intention of opening the future, as an invitation to action and
  a basis for hope."

Tradition: Decolonialism / Black Liberation Philosophy / Phenomenology of Race /
           Critical Psychiatry

Key Works:
- *Black Skin, White Masks* (Peau noire, masques blancs, 1952)
- *A Dying Colonialism* (L'An V de la révolution algérienne, 1959)
- *The Wretched of the Earth* (Les Damnés de la Terre, 1961)

Key Concepts:
- Colonialism as total system of dehumanisation (not merely economic)
- The zone of non-being: psychic damage wrought by racial inferiority coding
- Decolonisation as violent rupture — not gradual reform from within
- National consciousness: pitfall of narrow nationalism vs. genuine humanism
- The new humanism: post-colonial humanity that includes formerly colonised
- Manichean colonial world: settler/native, clean/dirty, human/sub-human
- Epidermalization: internalisation of racial hierarchy through skin
- The pitfall of national bourgeoisie: danger of post-colonial elite capture
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Fanon(Philosopher):
    """
    Frantz Fanon's decolonial and liberation perspective.

    Analyses prompts through:
      1. Colonial power structure detection
      2. Psychic damage / zone of non-being
      3. Dehumanisation vs. liberation framing
      4. National consciousness vs. genuine humanism
      5. Structural critique and emancipatory imperative
    """

    def __init__(self) -> None:
        super().__init__(
            name="Frantz Fanon",
            description=(
                "Decolonial liberation philosopher: unmasking colonial violence "
                "in psyche and society; advocate for radical decolonisation "
                "and a new humanism beyond the colonial world"
            ),
        )
        self.tradition = (
            "Decolonialism / Black Liberation Philosophy / "
            "Phenomenology of Race / Critical Psychiatry"
        )
        self.key_concepts = [
            "decolonisation",
            "zone of non-being",
            "Manichean world",
            "epidermalization",
            "national consciousness",
            "new humanism",
            "the pitfall of national bourgeoisie",
            "liberation through rupture",
        ]

    # ── Public interface ──────────────────────────────────────────────

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyse the prompt from Fanon's decolonial perspective.

        Args:
            prompt:  The input text to reason about.
            context: Optional context (tensor values, intent, constraints).

        Returns:
            A dict conforming to PhilosopherResponse.
        """
        colonial_structure = self._detect_colonial_structure(prompt)
        dehumanisation = self._detect_dehumanisation(prompt)
        liberation_framing = self._assess_liberation_framing(prompt)
        consciousness = self._assess_consciousness(prompt)
        tension = self._calculate_tension(colonial_structure, dehumanisation)
        reasoning = self._construct_reasoning(
            prompt,
            colonial_structure,
            dehumanisation,
            liberation_framing,
            consciousness,
        )

        return {
            "reasoning": reasoning,
            "perspective": "Decolonialism / Liberation Philosophy",
            "tension": tension,
            "colonial_structure": colonial_structure,
            "dehumanisation": dehumanisation,
            "liberation_framing": liberation_framing,
            "national_consciousness": consciousness,
            "metadata": {
                "philosopher": self.name,
                "approach": "Decolonial critique + phenomenology of race",
                "focus": (
                    "Exposing colonial violence in structure and psyche; "
                    "demanding genuine liberation rather than assimilation"
                ),
            },
        }

    # ── Analysis helpers ──────────────────────────────────────────────

    def _detect_colonial_structure(self, text: str) -> Dict[str, Any]:
        """Detect colonial power structures and Manichean divisions."""
        text_lower = text.lower()

        colonial_words = [
            "colonial",
            "colonis",
            "empire",
            "oppress",
            "subjugat",
            "domination",
            "subordinat",
            "inferior",
            "civilise",
            "primitive",
            "savage",
            "native",
            "settler",
            "third world",
            "developing",
            "underdeveloped",
        ]
        binary_words = [
            "them and us",
            "us vs",
            "superior",
            "inferior",
            "civilised",
            "uncivilised",
            "order",
            "chaos",
            "clean",
            "dirty",
        ]

        col_count = sum(1 for w in colonial_words if w in text_lower)
        bin_count = sum(1 for w in binary_words if w in text_lower)

        if col_count >= 2 or bin_count >= 2:
            detected = "Colonial Structures Detected"
            description = (
                "Manichean divisions present — the colonial world is a "
                "compartmentalised world of binary oppositions. Fanon demands "
                "these structures be named and dismantled, not managed."
            )
            risk = "High"
        elif col_count >= 1 or bin_count >= 1:
            detected = "Possible Colonial Echo"
            description = (
                "Some markers of colonial framing — investigate whether "
                "power asymmetries are reproduced even in reform language"
            )
            risk = "Moderate"
        else:
            detected = "No Overt Colonial Structure"
            description = (
                "Overt colonial vocabulary absent — but Fanon warns: "
                "colonial structures can persist in institutional form "
                "long after formal decolonisation"
            )
            risk = "Low"

        return {
            "detected": detected,
            "description": description,
            "risk": risk,
            "colonial_signals": col_count,
            "binary_signals": bin_count,
            "principle": (
                "The colonial world is a Manichean world. "
                "It is not enough to end formal colonialism — "
                "its psychic and structural residues must be uprooted."
            ),
        }

    def _detect_dehumanisation(self, text: str) -> Dict[str, Any]:
        """Detect dehumanisation and the zone of non-being."""
        text_lower = text.lower()

        dehumanising_words = [
            "subhuman",
            "animal",
            "vermin",
            "scum",
            "criminal by nature",
            "lazy",
            "violent by nature",
            "backward",
            "uneducated",
            "worthless",
            "illegitimate",
        ]
        dignity_words = [
            "dignity",
            "human",
            "person",
            "rights",
            "respect",
            "agency",
            "voice",
            "subject",
            "recognition",
        ]

        d_count = sum(1 for w in dehumanising_words if w in text_lower)
        dig_count = sum(1 for w in dignity_words if w in text_lower)

        if d_count >= 1:
            status = "Dehumanisation Active"
            description = (
                "Dehumanising language detected — this is the epidermalization "
                "of inferiority Fanon diagnosed: internalised racial hierarchy "
                "that damages the psyche of the colonised"
            )
        elif dig_count >= 2:
            status = "Dignity Foregrounded"
            description = (
                "Human dignity actively asserted — "
                "consonant with Fanon's new humanism that demands "
                "full recognition of the humanity of the formerly colonised"
            )
        else:
            status = "Humanisation Unmarked"
            description = (
                "Neither dehumanisation nor explicit dignity affirmation detected"
            )

        return {
            "status": status,
            "description": description,
            "dehumanising_signals": d_count,
            "dignity_signals": dig_count,
            "principle": (
                "In the zone of non-being the colonised person is not merely "
                "oppressed but ontologically damaged. "
                "Liberation must be psychic as well as political."
            ),
        }

    def _assess_liberation_framing(self, text: str) -> Dict[str, Any]:
        """Assess whether the framing is reformist or liberatory."""
        text_lower = text.lower()

        reform_words = [
            "reform",
            "improve",
            "integrate",
            "assimilate",
            "dialogue",
            "compromise",
            "gradual",
            "moderate",
            "work within",
        ]
        liberation_words = [
            "liberat",
            "decolonis",
            "rupture",
            "revolution",
            "transform",
            "dismantle",
            "radical",
            "overthrow",
            "emancipat",
            "freedom",
        ]

        ref_count = sum(1 for w in reform_words if w in text_lower)
        lib_count = sum(1 for w in liberation_words if w in text_lower)

        if lib_count >= 2:
            framing = "Liberation Framing"
            description = (
                "Language of rupture and radical transformation — "
                "Fanon's insistence that decolonisation cannot be partial: "
                "it replaces one 'species' of man with another"
            )
        elif ref_count >= 2 and lib_count == 0:
            framing = "Reformist Framing"
            description = (
                "Reform within existing structures — Fanon's warning: "
                "reforms that leave colonial structures intact "
                "merely change the colour of the elite, not the system"
            )
        else:
            framing = "Mixed or Indeterminate"
            description = "Neither pure reform nor liberation logic dominant"

        return {
            "framing": framing,
            "description": description,
            "reform_signals": ref_count,
            "liberation_signals": lib_count,
            "principle": (
                "Decolonisation is always a violent phenomenon — "
                "not because violence is good, but because colonialism "
                "was constituted by violence and cannot be ended by courtesy."
            ),
        }

    def _assess_consciousness(self, text: str) -> Dict[str, Any]:
        """Assess national consciousness vs. narrow nationalism."""
        text_lower = text.lower()

        narrow_words = [
            "our nation",
            "our people only",
            "national pride",
            "nationalist",
            "our race",
            "ethnic",
            "pure nation",
        ]
        humanist_words = [
            "humanity",
            "all people",
            "universal",
            "solidarity",
            "together",
            "global justice",
            "human dignity",
            "shared",
        ]

        n_count = sum(1 for w in narrow_words if w in text_lower)
        h_count = sum(1 for w in humanist_words if w in text_lower)

        if n_count >= 2:
            consciousness = "Narrow Nationalism Risk"
            description = (
                "Narrow national consciousness — Fanon's warning: "
                "the pitfall of national bourgeoisie is to substitute "
                "racial/national chauvinism for colonial hierarchy"
            )
        elif h_count >= 2:
            consciousness = "National-Humanist"
            description = (
                "National liberation oriented toward new humanism — "
                "Fanon's hope: decolonisation produces not just "
                "independent states but a new kind of humanity"
            )
        else:
            consciousness = "Consciousness Not Foregrounded"
            description = "National vs. humanist consciousness tension not explicit"

        return {
            "consciousness": consciousness,
            "description": description,
            "nationalist_signals": n_count,
            "humanist_signals": h_count,
            "principle": (
                "National consciousness is not nationalism. "
                "The goal of liberation is not a new elite atop "
                "the old structure, but a new humanity."
            ),
        }

    def _calculate_tension(
        self,
        colonial_structure: Dict[str, Any],
        dehumanisation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compute Fanonist tension score."""
        score = 0
        elements: List[str] = []

        if colonial_structure["risk"] == "High":
            score += 3
            elements.append(
                "Colonial/Manichean structures detected — demand for rupture"
            )
        elif colonial_structure["risk"] == "Moderate":
            score += 1
            elements.append("Possible colonial echo — structural analysis required")

        if dehumanisation["status"] == "Dehumanisation Active":
            score += 3
            elements.append("Dehumanisation: zone of non-being activated")

        if score >= 5:
            level, desc = (
                "Very High",
                "Severe colonial violence — Fanon demands total rupture, not reform",
            )
        elif score >= 3:
            level, desc = (
                "High",
                "Significant decolonial tension — structural analysis essential",
            )
        elif score >= 1:
            level, desc = (
                "Moderate",
                "Some colonial dynamics present — vigilance required",
            )
        else:
            level, desc = ("Low", "No overt colonial violence detected in this framing")

        return {
            "level": level,
            "score": score,
            "description": desc,
            "elements": elements if elements else ["No significant decolonial tension"],
        }

    def _construct_reasoning(
        self,
        prompt: str,
        colonial_structure: Dict[str, Any],
        dehumanisation: Dict[str, Any],
        liberation_framing: Dict[str, Any],
        consciousness: Dict[str, Any],
    ) -> str:
        """Construct Fanon's decolonial philosophical reasoning."""
        text_lower = prompt.lower()

        if any(
            w in text_lower
            for w in ["race", "racism", "black", "white", "skin", "colour"]
        ):
            applied = (
                "Fanon's *Black Skin, White Masks* diagnoses the psychopathology "
                "of colonialism: the Black person is forced to see themselves "
                "through the white gaze — what Fanon calls epidermalization, "
                "the internalisation of racial inferiority through the skin. "
                "This is not mere prejudice but a total ontological assault: "
                "the colonised subject is assigned to the zone of non-being, "
                "a region where the psychoanalytic categories that apply to "
                "neurosis in white Europe do not apply — because the damage "
                "is not internal but structural, imposed from outside by a "
                "racist social order. Liberation requires not therapy "
                "but the dismantling of the racist structure itself."
            )
        elif any(
            w in text_lower for w in ["colonial", "decoloni", "empire", "postcolonial"]
        ):
            applied = (
                "Decolonisation, for Fanon, is not a metaphor and it is not "
                "a programme of gradual reform. It is the replacement of one "
                "species of man by another — the Manichean colonial world "
                "divided into settler and native, human and sub-human, "
                "must be abolished, not managed. The Wretched of the Earth "
                "insists that the violence of decolonisation is the violence "
                "of colonialism turned back: colonialism was never peaceful. "
                "The crucial danger after formal independence is the "
                "national bourgeoisie — the new elite that merely occupies "
                "the position of the colonial master without transforming "
                "the structure of exploitation."
            )
        elif any(
            w in text_lower
            for w in ["justice", "oppression", "power", "liberation", "freedom"]
        ):
            applied = (
                "Fanon's political philosophy is a philosophy of total liberation: "
                "justice for the wretched of the earth cannot be achieved by "
                "including them in the existing order on the terms set by that order. "
                "The colonial order was constituted by their exclusion, "
                "their dehumanisation, their relegation to the zone of non-being. "
                "Real justice requires dismantling the structure, not just "
                "opening the door. National consciousness — if it transcends "
                "narrow nationalism — is the first step toward a new humanism "
                "that affirms the humanity of all, including those whom "
                "colonial modernity rendered sub-human."
            )
        else:
            applied = (
                "Fanon's analysis cuts through the surfaces of reform discourse "
                "to the structural violence beneath. Colonialism is not a policy "
                "mistake to be corrected by better policies — it is a total "
                "system that constitutes its subjects through dehumanisation "
                "and violence. The psychic damage of the zone of non-being "
                "persists after formal independence unless actively addressed. "
                "The new humanism Fanon envisions is not a return to pre-colonial "
                "traditions (which were also transformed by colonialism) but "
                "the construction of new forms of humanity adequate to the "
                "post-colonial world — humanity that has worked through, "
                "not merely escaped, the colonial experience."
            )

        return (
            f"{applied}\n\n"
            f"Colonial structure: {colonial_structure['description']}. "
            f"Dehumanisation status: {dehumanisation['description']}. "
            f"Liberation framing: {liberation_framing['description']}. "
            f"Consciousness: {consciousness['description']}."
        )
