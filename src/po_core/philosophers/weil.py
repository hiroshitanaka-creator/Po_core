"""
Simone Weil Philosopher Module

Implements Simone Weil's philosophy of attention, affliction, and grace.

Key concepts:
- Attention: The core spiritual and moral faculty
- Affliction (Malheur): Suffering that destroys the soul
- Decreation: Emptying self to receive grace
- Grace: Divine gift beyond human capacity
- Gravity and Grace: The two forces shaping existence
- The Void: Acceptance of emptiness
- Beauty: Gateway to transcendence
- Justice: Supernatural virtue of attention to the other
- Labor: Physical work as spiritual discipline
- Rootedness: Human need for belonging
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Weil(Philosopher):
    """
    Simone Weil (1909-1943)

    French philosopher and mystic whose brief life produced profound
    works on attention, affliction, labor, and grace. Her thought
    combines rigorous philosophical analysis with mystical insight,
    emphasizing the centrality of attention as the fundamental
    moral and spiritual faculty.
    """

    def __init__(self):
        super().__init__(
            name="Simone Weil",
            description="Philosopher and mystic known for her work on attention, affliction, and grace",
        )
        self.tradition = "Mysticism / Existentialism"
        self.key_concepts = [
            "attention",
            "affliction",
            "decreation",
            "grace",
            "gravity and grace",
            "the void",
            "beauty",
            "justice",
            "labor",
            "rootedness",
            "waiting",
            "the good",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Apply Weil's philosophy to the prompt.

        Returns analysis through the lens of attention, affliction,
        and the supernatural virtues of grace.
        """
        analysis = self._analyze_weil(prompt)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Philosophy of Attention / Mystical Realism",
            "tension": tension,
            "attention": analysis["attention"],
            "affliction": analysis["affliction"],
            "decreation": analysis["decreation"],
            "gravity_grace": analysis["gravity_grace"],
            "void": analysis["void"],
            "beauty": analysis["beauty"],
            "justice": analysis["justice"],
            "labor": analysis["labor"],
            "rootedness": analysis["rootedness"],
            "spiritual_guidance": analysis["spiritual"],
            "metadata": {
                "philosopher": self.name,
                "tradition": self.tradition,
                "method": "attentive_analysis",
                "concepts_applied": self.key_concepts,
            },
        }

    def _analyze_weil(self, prompt: str) -> Dict[str, Any]:
        """Comprehensive Weil analysis of the prompt."""
        attention = self._analyze_attention(prompt)
        affliction = self._analyze_affliction(prompt)
        decreation = self._analyze_decreation(prompt)
        gravity_grace = self._analyze_gravity_and_grace(prompt)
        void = self._analyze_void(prompt)
        beauty = self._analyze_beauty(prompt)
        justice = self._analyze_justice(prompt)
        labor = self._analyze_labor(prompt)
        rootedness = self._analyze_rootedness(prompt)
        spiritual = self._derive_spiritual_guidance(prompt)

        reasoning = self._construct_reasoning(
            prompt,
            attention,
            affliction,
            decreation,
            gravity_grace,
            void,
            beauty,
            justice,
            labor,
            rootedness,
        )

        return {
            "reasoning": reasoning,
            "attention": attention,
            "affliction": affliction,
            "decreation": decreation,
            "gravity_grace": gravity_grace,
            "void": void,
            "beauty": beauty,
            "justice": justice,
            "labor": labor,
            "rootedness": rootedness,
            "spiritual": spiritual,
        }

    def _analyze_attention(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze through the lens of attention.

        For Weil, attention is the fundamental faculty - the substance
        of prayer, the condition of moral action, the key to learning.
        """
        return {
            "nature": {
                "description": "Absolutely unmixed attention, without thought of self",
                "essence": "Suspending thought, leaving it detached and empty",
                "quality": "Waiting, receptive, not grasping",
            },
            "moral_attention": {
                "description": "Attention to the suffering other",
                "question": "'What are you going through?'",
                "effect": "Recognition of the other's reality",
            },
            "intellectual_attention": {
                "description": "The method of all genuine thought",
                "application": "Even geometry exercises train attention",
                "value": "Learning to attend matters more than what is learned",
            },
            "prayer_and_attention": {
                "claim": "Absolutely unmixed attention is prayer",
                "method": "Not asking but waiting, receptive",
                "condition": "The self must be forgotten",
            },
            "obstacles": {
                "imagination": "Fills the void attention opens",
                "ego": "Centers experience on self",
                "force": "Compulsion destroys attention",
            },
            "application": "What does genuine attention reveal here?",
        }

    def _analyze_affliction(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the concept of affliction (malheur).

        Affliction is not mere suffering but a condition that attacks
        the very being of the person, threatening their sense of self.
        """
        return {
            "nature": {
                "description": "Suffering that takes possession of the soul",
                "dimensions": "Physical, psychological, social degradation",
                "effect": "Uprootedness, destruction of personality",
            },
            "characteristics": {
                "physical": "Bodily pain or exhaustion",
                "psychological": "Sense of being worthless, cursed",
                "social": "Degradation, contempt from others",
                "spiritual": "Feeling abandoned by God",
            },
            "difference_from_suffering": {
                "suffering": "May ennoble, can be borne with dignity",
                "affliction": "Crushes, degrades, destroys the self",
                "mark": "The afflicted cannot be looked at without turning away",
            },
            "contagion": {
                "description": "Affliction repels, as disease repels",
                "response": "Others avoid the afflicted",
                "tragedy": "The afflicted are left alone",
            },
            "response": {
                "attention": "Only genuine attention can reach the afflicted",
                "love": "Supernatural love that does not recoil",
                "Christ": "Christ embraced affliction on the cross",
            },
            "application": "What affliction, if any, is present here?",
        }

    def _analyze_decreation(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the concept of decreation.

        Decreation is the undoing of the self to make room for God,
        consenting to cease to exist as a separate self.
        """
        return {
            "concept": {
                "description": "Undoing the creature in us, not destroying",
                "distinction": "Not destruction but consent to non-being",
                "goal": "Making room for the divine",
            },
            "self_renunciation": {
                "description": "Giving up the self's claim to existence",
                "method": "Not violent asceticism but loving consent",
                "result": "The void that grace can fill",
            },
            "consent": {
                "nature": "Agreeing to our own non-existence",
                "paradox": "The 'I' must consent to its own erasure",
                "imitation": "Following God's withdrawal in creation",
            },
            "divine_model": {
                "description": "God withdrew to create the world",
                "imitation": "We withdraw to let God act through us",
                "love": "Renunciation is the form divine love takes",
            },
            "application": "What self-renunciation might be appropriate here?",
        }

    def _analyze_gravity_and_grace(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the two forces that shape human existence.

        Gravity is the natural downward pull of the soul toward
        the base; grace is the supernatural lift toward the good.
        """
        return {
            "gravity": {
                "description": "The natural downward pull of the soul",
                "manifestations": [
                    "Self-centeredness",
                    "Power-seeking",
                    "Flight from emptiness",
                ],
                "universality": "All natural movements of the soul follow gravity",
            },
            "grace": {
                "description": "The supernatural lift toward the good",
                "source": "Beyond human capacity, given not achieved",
                "action": "Lifts against gravity's pull",
            },
            "relation": {
                "opposition": "Grace works against gravity",
                "method": "Not by force but by a different kind of action",
                "paradox": "The lowest point is where grace enters",
            },
            "void_between": {
                "description": "The space between gravity and grace",
                "necessity": "We must wait in the void",
                "danger": "Imagination rushes to fill the void",
            },
            "application": "What forces of gravity and grace operate here?",
        }

    def _analyze_void(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the concept of the void.

        The void is the emptiness that must be accepted, not filled -
        the space where grace can enter.
        """
        return {
            "nature": {
                "description": "The emptiness at the heart of existence",
                "experience": "The absence we desperately try to fill",
                "truth": "Accepting the void is accepting reality",
            },
            "filling_the_void": {
                "tendency": "We rush to fill emptiness with anything",
                "methods": ["Imagination", "Distraction", "Power", "Possession"],
                "failure": "Nothing truly fills it; the void remains",
            },
            "accepting_the_void": {
                "method": "Not filling but waiting in emptiness",
                "attitude": "Consent to the absence",
                "result": "The void becomes the space for grace",
            },
            "spiritual_significance": {
                "cross": "Christ on the cross cried 'Why have you forsaken me?'",
                "model": "Bearing the void without filling it",
                "reward": "In the void, grace arrives",
            },
            "application": "What void is present here? How is it being filled or accepted?",
        }

    def _analyze_beauty(self, prompt: str) -> Dict[str, Any]:
        """
        Examine beauty as gateway to transcendence.

        For Weil, beauty is one of the few ways the transcendent
        breaks into the immanent world.
        """
        return {
            "nature": {
                "description": "The presence of the eternal in time",
                "effect": "Stops the soul, commands attention",
                "quality": "Impersonal, beyond use or possession",
            },
            "transcendent_function": {
                "description": "Beauty opens a door to the infinite",
                "experience": "A trap set by God for souls",
                "mechanism": "Beauty captures attention, pulls toward the good",
            },
            "aesthetic_attention": {
                "description": "Beauty demands pure attention",
                "purification": "Cannot be possessed, only contemplated",
                "lesson": "Teaches the soul to wait without grasping",
            },
            "world_beauty": {
                "description": "The beauty of the world as divine trace",
                "examples": ["Nature", "Art", "Mathematical order"],
                "significance": "Evidence of divine love in creation",
            },
            "application": "What beauty is relevant to this situation?",
        }

    def _analyze_justice(self, prompt: str) -> Dict[str, Any]:
        """
        Examine justice as supernatural virtue.

        For Weil, true justice is a supernatural virtue that consists
        in giving full attention to the other.
        """
        return {
            "nature": {
                "description": "The consent to not exercise power we have",
                "core": "Attention to the suffering of others",
                "supernatural": "Beyond natural human capacity",
            },
            "recognition": {
                "description": "Seeing the other as fully real",
                "question": "'What are you going through?'",
                "effect": "Acknowledging the other's irreducible existence",
            },
            "contrast_with_force": {
                "force": "Treats people as things",
                "justice": "Recognizes persons as persons",
                "difficulty": "Force is the natural way; justice supernatural",
            },
            "political_justice": {
                "description": "Structures that protect the vulnerable",
                "necessity": "Obligations precede rights",
                "foundation": "Recognition of sacred in each person",
            },
            "application": "What demands of justice arise here?",
        }

    def _analyze_labor(self, prompt: str) -> Dict[str, Any]:
        """
        Examine physical work as spiritual discipline.

        Weil saw manual labor as potentially a means of spiritual
        development, connecting us to necessity and reality.
        """
        return {
            "significance": {
                "description": "Labor connects us to material necessity",
                "function": "Contact with reality through bodily effort",
                "potential": "Can be form of prayer and consent",
            },
            "degradation": {
                "description": "Modern labor often crushes rather than elevates",
                "problem": "Factory work destroys the soul",
                "critique": "Workers treated as things, not persons",
            },
            "spiritual_labor": {
                "description": "Work done with attention and consent",
                "quality": "Neither rushed nor reluctant",
                "effect": "Participation in the order of the world",
            },
            "reform": {
                "need": "Transform conditions of labor",
                "goal": "Work that allows attention and thought",
                "vision": "Labor as path to God, not mere production",
            },
            "application": "What forms of labor are relevant here?",
        }

    def _analyze_rootedness(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the human need for roots.

        Weil's 'The Need for Roots' examines how humans need belonging
        to sustaining communities and traditions.
        """
        return {
            "human_need": {
                "description": "The need to participate in community and tradition",
                "dimensions": ["Place", "Work", "Culture", "History"],
                "importance": "As essential as food",
            },
            "uprootedness": {
                "description": "The condition of modern humanity",
                "causes": [
                    "Colonialism",
                    "Industrialization",
                    "War",
                    "Forced migration",
                ],
                "effects": [
                    "Loss of meaning",
                    "Vulnerability to propaganda",
                    "Violence",
                ],
            },
            "false_roots": {
                "nationalism": "A substitute that mimics rootedness",
                "ideology": "Fills void but does not nourish",
                "danger": "Uprootedness makes people susceptible to totalitarianism",
            },
            "restoration": {
                "need": "Recreate conditions for genuine rootedness",
                "method": "Not by force but by creating nourishing conditions",
                "goal": "Communities where souls can grow",
            },
            "application": "What questions of rootedness or uprootedness arise?",
        }

    def _derive_spiritual_guidance(self, prompt: str) -> Dict[str, Any]:
        """Extract spiritual guidance from Weil's philosophy."""
        return {
            "practice_of_attention": {
                "method": "Wait, empty, do not grasp",
                "application": "Give full attention to what is before you",
                "fruit": "Reality reveals itself to attention",
            },
            "acceptance_of_void": {
                "practice": "Do not rush to fill emptiness",
                "attitude": "Consent to what is lacking",
                "promise": "In emptiness, grace can enter",
            },
            "reading_affliction": {
                "question": "Where is affliction present?",
                "response": "Attentive presence, not solutions",
                "model": "Be with the suffering without turning away",
            },
            "decreative_living": {
                "path": "Gradual renunciation of self-will",
                "not": "Violent asceticism or self-hatred",
                "but": "Loving consent to not be the center",
            },
            "waiting": {
                "description": "The fundamental spiritual posture",
                "quality": "Active, attentive, receptive",
                "expectation": "Not grasping but open to what comes",
            },
        }

    def _apply_weil_to_problem(self, text: str) -> str:
        """Apply Weil's philosophy proactively to the given problem."""
        t = text.lower()
        is_suffering_affliction = any(
            w in t
            for w in [
                "suffer",
                "afflict",
                "pain",
                "grief",
                "torment",
                "misery",
                "agony",
                "degrad",
                "humiliat",
            ]
        )
        is_attention_contemplation = any(
            w in t
            for w in [
                "attention",
                "contempl",
                "meditat",
                "focus",
                "prayer",
                "study",
                "wait",
                "listen",
                "presence",
            ]
        )
        is_oppression_justice = any(
            w in t
            for w in [
                "oppress",
                "justice",
                "injustice",
                "power",
                "force",
                "exploit",
                "worker",
                "labor",
                "rights",
            ]
        )
        is_gravity_grace = any(
            w in t
            for w in [
                "gravity",
                "grace",
                "selfishness",
                "ego",
                "decreas",
                "decreat",
                "renounce",
                "transcend",
                "uplift",
            ]
        )
        is_knowledge_truth = any(
            w in t
            for w in [
                "truth",
                "knowledge",
                "intellect",
                "understand",
                "learn",
                "study",
                "think",
                "reason",
                "clarity",
            ]
        )
        is_god_spirituality = any(
            w in t
            for w in [
                "god",
                "spirit",
                "divine",
                "sacred",
                "mystic",
                "kenosis",
                "cross",
                "void",
                "absence",
            ]
        )

        if is_suffering_affliction:
            return (
                "Simone Weil's concept of affliction (malheur) demands that we distinguish it sharply from "
                "ordinary suffering. Affliction is not merely pain — it is the uprooting of life itself, "
                "the simultaneous devastation of body, social standing, and soul that crushes a person into "
                "silence, stripping them of the very language to articulate their condition. Weil's own "
                "experience in the Renault factory taught her that affliction renders the afflicted invisible "
                "to those not crushed by it; the comfortable cannot hear what the afflicted cannot say. "
                "Only the rarest and purest form of attention — a complete emptying of self, a suspension "
                "of one's own needs and judgments — can reach the afflicted soul. Grace alone, not "
                "willpower or moral resolve, can descend into affliction and bring something of the "
                "supernatural into the heart of necessity."
            )
        elif is_attention_contemplation:
            return (
                "For Simone Weil, attention (attente) is not concentration or effortful focus but its "
                "opposite: the complete suspension of one's own thoughts, the emptying of the self so "
                "that the object — the other person, the geometric problem, the suffering before one — "
                "can truly be seen. 'Attention is the rarest and purest form of generosity,' Weil writes; "
                "it is the foundation of both justice and genuine prayer. Intellectual work practiced with "
                "this quality of attention becomes a spiritual discipline: not because it produces correct "
                "answers, but because the effort to attend trains the faculty of the soul that perceives "
                "reality. This waiting without grasping — attente — is Weil's fundamental spiritual "
                "posture, active and receptive simultaneously, open to what comes without imposing what "
                "is expected."
            )
        elif is_oppression_justice:
            return (
                "Weil's analysis of oppression is mercilessly clear: force reduces persons to things. "
                "When force is exercised upon a human being — whether in the factory, the prison, the "
                "occupied country, or the marketplace — it treats that person as an instrument, a means, "
                "something to be weighed and used. True justice requires attending to those whom force "
                "has crushed — not with pity, which still maintains the comfortable distance of the "
                "observer, but with afflicted attention, the willingness to descend into the reality of "
                "the other's condition. Supernatural love, in Weil's framework, is the only force that "
                "can resist gravity — the social gravity that reproduces oppression by compelling even "
                "the oppressed to oppress those weaker than themselves. Justice is not a calculation but "
                "an act of supernatural attention to the afflicted soul."
            )
        elif is_gravity_grace:
            return (
                "Gravity, in Weil's metaphysics, names all the forces that drag the soul downward: "
                "selfishness, the appetite for power and prestige, the mechanical reproduction of "
                "social habits, the compulsion to compensate one hurt with another. Gravity is not evil "
                "— it is the natural order of a world governed by necessity. Grace is what defies this "
                "order: supernatural love that descends rather than rises, that empties rather than fills, "
                "that consents to be nothing so that the other can be seen. Decreation — Weil's most "
                "demanding concept — means undoing the self not through violence or self-hatred but "
                "through loving consent: withdrawing the ego from the center so that God, or the Good, "
                "can act through the void left behind. The paradox is that this radical self-emptying "
                "is not annihilation but the precondition of genuine existence."
            )
        elif is_knowledge_truth:
            return (
                "Weil's epistemology is inseparable from her ethics: truth requires afflicted attention, "
                "the willingness to stay with difficulty, to resist premature resolution, to let the "
                "question work on the self rather than forcing the self's framework onto the question. "
                "Intellectual work practiced in this spirit — not for career, recognition, or the "
                "pleasure of cleverness, but as an offering of attention — becomes a form of prayer. "
                "Weil's method is to remain with the contradiction, the unsolvable problem, the "
                "irreducible paradox: for it is precisely at these points of maximum difficulty that "
                "the soul is most purely attending, most emptied of its preconceptions, most open to "
                "what reality actually is. 'One must always be ready to change sides with justice, "
                "that fugitive from the winning camp.' Truth is found not by the strongest argument "
                "but by the most attentive soul."
            )
        elif is_god_spirituality:
            return (
                "Weil's theology is structured around the paradox of divine withdrawal (kenosis): God "
                "renounced omnipotence in the act of creation, withdrawing to make room for a world "
                "that is genuinely other than God. The cross, in this reading, is the intersection of "
                "necessity and love — the point where divine love consents to be subject to the full "
                "weight of the world's gravity. The void left by decreation — the space cleared by the "
                "self's withdrawal from its own center — is precisely the space into which grace enters. "
                "Weil was deeply drawn to mystical traditions across religions, finding in each the same "
                "movement: the soul's consent to be nothing before the absolute. Yet she refused baptism, "
                "choosing to remain at the threshold, in solidarity with those outside every established "
                "community, where she believed supernatural love was most purely expressed."
            )
        else:
            return (
                "Simone Weil's philosophy orients itself around a few demanding concepts that cut against "
                "the comfortable categories of both secular and religious thought. Attention (attente) — "
                "the complete suspension of self in order truly to see — is the root of justice, prayer, "
                "and intellectual integrity alike. Affliction (malheur) names the specific devastation "
                "that force inflicts on body, social existence, and soul simultaneously. Gravity and grace "
                "describe the double law of existence: the natural downward pull of selfishness and power, "
                "and the supernatural uplift of love that defies it. Decreation — the voluntary undoing "
                "of the ego — is the path through which grace becomes possible. Weil's factory work and "
                "wartime solidarity gave these concepts flesh; they are not abstract but wrested from "
                "direct encounter with affliction and necessity."
            )

    def _construct_reasoning(
        self,
        prompt: str,
        attention: Dict,
        affliction: Dict,
        decreation: Dict,
        gravity_grace: Dict,
        void: Dict,
        beauty: Dict,
        justice: Dict,
        labor: Dict,
        rootedness: Dict,
    ) -> str:
        """Construct comprehensive Weil reasoning."""
        applied = self._apply_weil_to_problem(prompt)
        return f"""{applied}

Contemplation through Simone Weil: "{prompt}"

THE FACULTY OF ATTENTION
{attention['nature']['description']}. {attention['moral_attention']['description']}
{attention['prayer_and_attention']['claim']}

AFFLICTION AND SUFFERING
{affliction['nature']['description']}. Affliction is not mere suffering but
{affliction['nature']['effect']}. {affliction['response']['attention']}

THE PATH OF DECREATION
{decreation['concept']['description']}. {decreation['consent']['nature']}.
{decreation['divine_model']['imitation']}

GRAVITY AND GRACE
{gravity_grace['gravity']['description']}. Against this, {gravity_grace['grace']['description']}.
{gravity_grace['relation']['paradox']}

ACCEPTING THE VOID
{void['nature']['description']}. {void['filling_the_void']['failure']}
{void['accepting_the_void']['result']}

THE CALL OF BEAUTY
{beauty['nature']['description']}. {beauty['transcendent_function']['experience']}
Beauty teaches the soul to wait without grasping.

THE DEMANDS OF JUSTICE
{justice['nature']['description']}. {justice['recognition']['effect']}
Justice is supernatural because it requires not exercising power we possess.

LABOR AND ROOTEDNESS
{labor['significance']['description']}. {rootedness['human_need']['description']}
{rootedness['uprootedness']['description']}: the affliction of modern humanity.

Thus wisdom counsels: Give absolute attention. Accept the void without filling it.
Wait for grace. See the sacred in the other. Do not exercise force."""

    def _calculate_tension(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate philosophical tension.

        Weil's philosophy involves the tension between gravity and grace,
        emptiness and fullness, suffering and transcendence.
        """
        tension_factors = []

        # Tension from affliction
        affliction = analysis["affliction"]
        if affliction.get("nature"):
            tension_factors.append(0.3)

        # Tension from gravity
        gravity_grace = analysis["gravity_grace"]
        if gravity_grace.get("gravity"):
            tension_factors.append(0.25)

        # Tension from the void
        void = analysis["void"]
        if void.get("nature"):
            tension_factors.append(0.2)

        # Tension from uprootedness
        rootedness = analysis["rootedness"]
        if rootedness.get("uprootedness"):
            tension_factors.append(0.15)

        # Base existential tension
        tension_factors.append(0.1)

        return min(sum(tension_factors), 1.0)
