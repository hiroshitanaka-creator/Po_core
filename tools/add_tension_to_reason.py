"""Add tension key to reason() return dict for 11 philosophers missing it."""
import os

MISSING_TENSION = [
    "levinas", "watsuji", "wabi_sabi", "merleau_ponty", "wittgenstein",
    "peirce", "dewey", "foucault", "deleuze", "lacan", "badiou",
]

# Tension descriptions for each philosopher
TENSION_TEMPLATES = {
    "levinas": {
        "description": "Tension between totality and infinity, self and Other",
        "elements": [
            "The face of the Other demands infinite responsibility",
            "Totality seeks to reduce the Other to the Same",
            "Ethical relation precedes ontological comprehension",
        ],
    },
    "watsuji": {
        "description": "Tension between individual and relational existence",
        "elements": [
            "Ningen as dual: individual person and relational being",
            "Climate shapes ethical sensibility",
            "Betweenness (aidagara) resists pure individuality",
        ],
    },
    "wabi_sabi": {
        "description": "Tension between perfection and impermanence",
        "elements": [
            "Beauty found in imperfection conflicts with desire for completeness",
            "Transience gives meaning yet evokes loss",
            "Simplicity opposes the complexity of modern existence",
        ],
    },
    "merleau_ponty": {
        "description": "Tension between body and consciousness, perception and thought",
        "elements": [
            "The lived body resists Cartesian mind-body separation",
            "Perception is primary yet shaped by habit and culture",
            "Ambiguity of embodied existence defies clear categorization",
        ],
    },
    "wittgenstein": {
        "description": "Tension between saying and showing, rule and practice",
        "elements": [
            "Language games have boundaries yet resist precise definition",
            "Rules require interpretation yet cannot be infinitely regressed",
            "What can be shown cannot always be said",
        ],
    },
    "peirce": {
        "description": "Tension between fallibilism and truth-seeking",
        "elements": [
            "All knowledge is fallible yet inquiry aims at truth",
            "Abduction introduces novelty but lacks deductive certainty",
            "Signs mediate reality yet never fully capture it",
        ],
    },
    "dewey": {
        "description": "Tension between individual growth and social conditions",
        "elements": [
            "Experience is both personal and shaped by environment",
            "Democracy requires both freedom and shared inquiry",
            "Education aims at growth yet must prepare for existing society",
        ],
    },
    "foucault": {
        "description": "Tension between power and resistance, knowledge and control",
        "elements": [
            "Power produces knowledge yet knowledge reinforces power",
            "Discourse shapes subjects who may resist that shaping",
            "Freedom exists only within relations of power",
        ],
    },
    "deleuze": {
        "description": "Tension between deterritorialization and reterritorialization",
        "elements": [
            "Lines of flight create new possibilities yet risk capture",
            "Difference resists representation yet must be expressed",
            "Becoming opposes being yet requires actual occasions",
        ],
    },
    "lacan": {
        "description": "Tension between desire and the symbolic order",
        "elements": [
            "Desire is structured by language yet exceeds it",
            "The subject is split between conscious and unconscious",
            "The Real resists symbolization yet insists on expression",
        ],
    },
    "badiou": {
        "description": "Tension between situation and event, being and truth",
        "elements": [
            "Events rupture the situation yet require fidelity to sustain",
            "Truth is universal yet emerges from particular situations",
            "The subject arises through commitment yet risks betrayal",
        ],
    },
}

BASE_DIR = "/home/user/Po_core/src/po_core/philosophers"

modified = []

for pid in MISSING_TENSION:
    filepath = os.path.join(BASE_DIR, f"{pid}.py")
    if not os.path.exists(filepath):
        print(f"SKIP {pid}: not found")
        continue

    with open(filepath, "r") as f:
        content = f.read()

    # Find the return { ... } block in reason() method
    # Strategy: find `"metadata":` line, then insert tension before it
    lines = content.split("\n")
    insert_idx = None
    indent = ""

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith('"metadata"') and ":" in stripped:
            insert_idx = i
            indent = line[: len(line) - len(stripped)]
            break

    if insert_idx is None:
        print(f"SKIP {pid}: no metadata line found")
        continue

    t = TENSION_TEMPLATES[pid]
    elements_str = repr(t["elements"])

    tension_lines = [
        f'{indent}"tension": {{',
        f'{indent}    "level": "Medium",',
        f'{indent}    "description": "{t["description"]}",',
        f'{indent}    "elements": {elements_str},',
        f'{indent}}},',
    ]

    new_lines = lines[:insert_idx] + tension_lines + lines[insert_idx:]
    new_content = "\n".join(new_lines)

    with open(filepath, "w") as f:
        f.write(new_content)

    modified.append(pid)
    print(f"OK {pid}")

print(f"\nModified {len(modified)} files")
