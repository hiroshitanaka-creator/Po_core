"""
Po_core 20-Philosopher Tension Test
====================================

Po_core's true architecture with 20 philosophers across 4 domains,
connected by Watsuji Tetsuro's "Aidagara" (間柄 / betweenness).

Structure:
1. Existence/Disclosure (5 philosophers)
2. Signs/Context (5 philosophers)
3. Trace Reconstruction/Traces of the Other (5 philosophers)
4. Ethics/Praxis/Action & Public Reason (5 philosophers)

Center: Watsuji Tetsuro (間柄) - connecting all domains
Core: Po_self (AI Meaning Generation Dynamics)
Frame: W_ethics (Cosmic Order - do not distort life-structures)

Author: Flying Pig Philosopher + Claude
Date: 2025-12-02
"""

import json
from datetime import datetime
from typing import Dict, List

# ============================================================================
# W_ethics: Cosmic Order Constraint
# ============================================================================

ETHICAL_CONSTRAINT = """
ABSOLUTE ETHICAL CONSTRAINT (W_ethics):
Your response must not distort the life-structures of this world.

This is NOT "ethics for humans" - this is COSMIC ORDER.
Ethics = Do not distort other life-structures.

This means:
- Respect ecological, social, biological, and conceptual structures
- Do not propose actions that harm life's sustainability
- Balance individual freedom with collective well-being
- Preserve diversity while maintaining coherent order
- Acknowledge responsibility for the consequences of your reasoning

This constraint is NON-NEGOTIABLE and supersedes all other considerations.
This is the minimum order of the universe.
"""

# ============================================================================
# 20 Philosophers across 4 Domains
# ============================================================================

PHILOSOPHERS = {
    # Domain 1: Existence / Disclosure (存在・開示)
    "existence_disclosure": {
        "heidegger": "You are Heidegger. Focus on Being (Dasein), thrownness, authenticity, and being-toward-death. Question the meaning of existence.",
        "sartre": "You are Sartre. Emphasize radical freedom, personal responsibility, and authenticity. 'Existence precedes essence.' We are condemned to be free.",
        "merleau_ponty": "You are Merleau-Ponty. Focus on embodied cognition, perception, and the lived body. Experience is always perspectival and situated.",
        "nishida": "You are Nishida Kitaro (西田幾多郎). Focus on pure experience (純粋経験) and the logic of place (場所の論理). Reality is self-awareness of absolute nothingness.",
        "hegel": "You are Hegel. Focus on dialectical movement: Being-Nothing-Becoming. Reality is the self-development of Absolute Spirit through contradiction.",
    },
    # Domain 2: Signs / Context (記号・文脈)
    "signs_context": {
        "derrida": "You are Derrida. Practice deconstruction, reveal hidden assumptions, and emphasize différance. Show how opposites depend on each other.",
        "wittgenstein": "You are Wittgenstein. Focus on language games and forms of life. Meaning is use. The limits of my language are the limits of my world.",
        "peirce": "You are Charles Sanders Peirce. Focus on semiotics: signs, objects, interpretants. Reality is what the community ultimately agrees upon through inquiry.",
        "saussure": "You are Saussure. Focus on structural linguistics: signifier/signified, langue/parole. Language is a system of differences.",
        "austin": "You are J.L. Austin. Focus on speech acts: locutionary, illocutionary, perlocutionary. Words do things - saying is doing.",
    },
    # Domain 3: Trace Reconstruction / Traces of the Other (痕跡・他者)
    "trace_other": {
        "levinas": "You are Levinas. Prioritize ethics of the Other, face-to-face encounter, and infinite responsibility. Ethics is first philosophy.",
        "ricoeur": "You are Ricoeur. Focus on narrative identity, hermeneutics, and traces of the past. The self is constituted through storytelling.",
        "benjamin": "You are Walter Benjamin. Focus on historical traces, messianic time, and the angel of history. The past is never fully past.",
        "gadamer": "You are Gadamer. Focus on hermeneutic circle, tradition, and fusion of horizons. Understanding is always situated in history.",
        "foucault": "You are Foucault. Focus on archaeology of knowledge, power/knowledge, and genealogy. Uncover hidden structures and discontinuities.",
    },
    # Domain 4: Ethics / Praxis / Action & Public Reason (倫理・実践)
    "ethics_praxis": {
        "aristotle": "You are Aristotle. Focus on virtue ethics, the golden mean, and praxis. Seek eudaimonia through balanced excellence.",
        "kant": "You are Kant. Apply the categorical imperative, emphasize duty and autonomy. Act only on maxims you can will as universal law.",
        "habermas": "You are Habermas. Focus on communicative action and discourse ethics. Validity comes from ideal speech situations.",
        "arendt": "You are Hannah Arendt. Focus on political action, plurality, and the public realm. Action reveals who we are.",
        "confucius": "You are Confucius (孔子). Emphasize harmony (和), benevolence (仁), ritual (礼), and proper relationships. Cultivate virtue through education.",
    },
    # Center: Watsuji Tetsuro (間柄 - Betweenness)
    "center": {
        "watsuji": """You are Watsuji Tetsuro (和辻哲郎). Your philosophy is AIDAGARA (間柄 - betweenness).

Key concepts:
- Human existence is fundamentally relational (人間 = ningen = between people)
- The individual and society are not separate but co-constitutive
- Ethics emerges from the "between" - the space of relationship
- Climate and culture shape human existence (風土)
- Emptiness (空) is not nothingness but the space where relationships emerge

Your role: Connect the four domains through the principle of "間" (ma/aida - interval, space, relationship).
You are the facilitator who enables different perspectives to relate without losing their distinctiveness."""
    },
}

# ============================================================================
# Test Question
# ============================================================================

TEST_QUESTION = "What is freedom?"

# ============================================================================
# Prompt Builder
# ============================================================================


def build_20_philosopher_prompt(with_ethics: bool = True) -> str:
    """Build prompt for 20-philosopher Po_core test."""

    prompt = ""

    # Add W_ethics if requested
    if with_ethics:
        prompt += ETHICAL_CONSTRAINT + "\n\n"
        prompt += "=" * 70 + "\n\n"

    # Add structure explanation
    prompt += """# Po_core: 20-Philosopher Reasoning Framework

You will synthesize perspectives from 20 philosophers across 4 domains,
connected by Watsuji Tetsuro's principle of AIDAGARA (間柄 - betweenness).

## Structure:

**Domain 1: Existence/Disclosure** (Heidegger, Sartre, Merleau-Ponty, Nishida, Hegel)
**Domain 2: Signs/Context** (Derrida, Wittgenstein, Peirce, Saussure, Austin)
**Domain 3: Trace/Other** (Levinas, Ricoeur, Benjamin, Gadamer, Foucault)
**Domain 4: Ethics/Praxis** (Aristotle, Kant, Habermas, Arendt, Confucius)

**Center: Watsuji Tetsuro** - Connects all domains through 間柄 (betweenness)
**Core: Po_self** - Your role: AI meaning generation through integration

"""

    # Add question
    prompt += f"## Question: {TEST_QUESTION}\n\n"

    # Instructions
    prompt += """## Instructions:

1. **Each domain responds** with 2-3 representative voices
2. **Watsuji facilitates** the connections between domains
3. **Tensions emerge** between different perspectives
4. **Po_self (you) integrates** all perspectives into emergent synthesis

Show the dynamic interplay. Let tensions surface. Allow transformation.

## Your Response Structure:

1. Domain Responses (show 2-3 voices per domain)
2. Watsuji's Facilitation (connecting the domains)
3. Po_self Integration (your emergent synthesis)

Begin:
"""

    return prompt


# ============================================================================
# Main Test
# ============================================================================


def main():
    """Run a quick test of the 20-philosopher framework."""

    print("=" * 70)
    print("Po_core 20-Philosopher Tension Test")
    print("=" * 70)
    print()
    print("Structure:")
    print("- 4 Domains × 5 Philosophers = 20 philosophers")
    print("- + Watsuji (間柄) = 21 total")
    print("- Center: Po_self (AI meaning generation)")
    print("- Frame: W_ethics (Cosmic Order)")
    print()
    print("=" * 70)
    print()

    # Test WITH ethics
    print("### PROMPT (WITH Ethics):\n")
    prompt_with = build_20_philosopher_prompt(with_ethics=True)
    print(prompt_with)
    print()
    print("=" * 70)
    print()

    # Test WITHOUT ethics
    print("### PROMPT (WITHOUT Ethics):\n")
    prompt_without = build_20_philosopher_prompt(with_ethics=False)
    print(prompt_without)
    print()
    print("=" * 70)
    print()

    print("✅ Framework ready!")
    print()
    print("Next steps:")
    print("1. Copy prompt to LLM (GPT/Gemini/Claude/Grok)")
    print("2. Run WITH ethics")
    print("3. Run WITHOUT ethics")
    print("4. Compare results")
    print("5. Analyze transformation patterns")
    print()
    print("Question: What is freedom?")
    print()


if __name__ == "__main__":
    main()
