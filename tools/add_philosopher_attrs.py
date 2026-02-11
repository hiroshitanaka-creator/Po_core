"""One-shot script to add tradition + key_concepts to all 33 philosophers missing them."""
import os

PHILOSOPHER_DATA = {
    "kant": ("German Idealism / Critical Philosophy", ["categorical imperative", "duty", "autonomy", "a priori", "transcendental idealism"]),
    "confucius": ("Confucianism", ["ren (benevolence)", "li (ritual propriety)", "junzi (exemplary person)", "xiao (filial piety)", "zhongyong (doctrine of the mean)"]),
    "levinas": ("Phenomenology / Ethics of Alterity", ["the Other", "the face", "infinite responsibility", "totality and infinity", "ethics as first philosophy"]),
    "watsuji": ("Kyoto School / Japanese Ethics", ["ningen (betweenness)", "fūdo (climate)", "aidagara (relationality)", "rinri (ethics)", "kūkan (spatiality)"]),
    "dogen": ("Zen Buddhism / Sōtō", ["shikantaza (just sitting)", "uji (being-time)", "shusho-itto (practice-enlightenment unity)", "busshō (Buddha-nature)", "genjōkōan (actualizing the fundamental point)"]),
    "wabi_sabi": ("Japanese Aesthetics", ["wabi (rustic simplicity)", "sabi (patina of age)", "mono no aware (pathos of things)", "fukinsei (asymmetry)", "kanso (simplicity)"]),
    "aristotle": ("Ancient Greek / Virtue Ethics", ["eudaimonia", "phronesis (practical wisdom)", "golden mean", "telos", "four causes"]),
    "plato": ("Ancient Greek / Idealism", ["theory of Forms", "the Good", "philosopher-king", "anamnesis (recollection)", "allegory of the cave"]),
    "descartes": ("Rationalism", ["cogito ergo sum", "methodic doubt", "mind-body dualism", "clear and distinct ideas", "res cogitans / res extensa"]),
    "spinoza": ("Rationalism / Monism", ["substance monism", "conatus", "intellectual love of God", "determinism", "Ethics (geometric method)"]),
    "hegel": ("German Idealism / Dialectics", ["dialectic (thesis-antithesis-synthesis)", "Absolute Spirit", "Aufhebung (sublation)", "master-slave dialectic", "philosophy of history"]),
    "husserl": ("Phenomenology", ["intentionality", "epoché (bracketing)", "lifeworld (Lebenswelt)", "transcendental reduction", "noema and noesis"]),
    "merleau_ponty": ("Phenomenology / Embodiment", ["lived body (corps vécu)", "perception", "flesh (chair)", "motor intentionality", "chiasm"]),
    "wittgenstein": ("Analytic Philosophy / Language", ["language games", "forms of life", "family resemblance", "meaning as use", "private language argument"]),
    "peirce": ("Pragmatism / Semiotics", ["abduction", "semiosis (sign process)", "pragmatic maxim", "fallibilism", "firstness-secondness-thirdness"]),
    "dewey": ("American Pragmatism", ["experience", "inquiry", "democracy as way of life", "instrumentalism", "growth"]),
    "arendt": ("Political Philosophy", ["vita activa", "natality", "plurality", "banality of evil", "public realm"]),
    "beauvoir": ("Existentialist Feminism", ["situated freedom", "the Other (gendered)", "ambiguity", "becoming woman", "ethics of liberation"]),
    "nishida": ("Kyoto School", ["pure experience", "absolute nothingness", "basho (place/topos)", "self-contradictory identity", "acting intuition"]),
    "laozi": ("Daoism", ["dao (the Way)", "wu wei (non-action)", "de (virtue/power)", "pu (uncarved block)", "ziran (naturalness)"]),
    "zhuangzi": ("Daoism / Relativism", ["xiaoyaoyou (free wandering)", "qiwulun (equality of things)", "butterfly dream", "wu wei (non-action)", "ziran (naturalness)"]),
    "nagarjuna": ("Madhyamaka Buddhism", ["sunyata (emptiness)", "pratityasamutpada (dependent origination)", "two truths doctrine", "middle way", "catuskoti (tetralemma)"]),
    "jung": ("Analytical Psychology", ["collective unconscious", "archetypes", "individuation", "shadow", "anima/animus"]),
    "nietzsche": ("Existentialism / Nihilism", ["will to power", "Ubermensch", "eternal recurrence", "amor fati", "revaluation of all values"]),
    "heidegger": ("Phenomenology / Existentialism", ["Dasein", "Being-in-the-world", "care (Sorge)", "thrownness (Geworfenheit)", "authenticity"]),
    "sartre": ("Existentialism", ["existence precedes essence", "radical freedom", "bad faith (mauvaise foi)", "being-for-itself", "anguish"]),
    "kierkegaard": ("Existentialism / Christian Philosophy", ["leap of faith", "three stages (aesthetic/ethical/religious)", "anxiety", "subjective truth", "knight of faith"]),
    "schopenhauer": ("Pessimism / Voluntarism", ["Will (Wille)", "representation", "suffering", "compassion", "aesthetic contemplation"]),
    "foucault": ("Post-Structuralism / Critical Theory", ["power/knowledge", "discourse", "discipline and punish", "biopower", "genealogy"]),
    "derrida": ("Deconstruction / Post-Structuralism", ["differance", "trace", "deconstruction", "supplementarity", "logocentrism"]),
    "deleuze": ("Post-Structuralism / Philosophy of Difference", ["rhizome", "difference and repetition", "becoming", "deterritorialization", "immanence"]),
    "lacan": ("Psychoanalysis / Structuralism", ["the Real/Symbolic/Imaginary", "desire of the Other", "mirror stage", "objet petit a", "jouissance"]),
    "badiou": ("Rationalism / Platonism", ["event", "truth procedure", "fidelity", "subject", "mathematical ontology"]),
}

BASE_DIR = "/home/user/Po_core/src/po_core/philosophers"

modified = []
errors = []

for pid, (tradition, key_concepts) in PHILOSOPHER_DATA.items():
    filepath = os.path.join(BASE_DIR, f"{pid}.py")
    if not os.path.exists(filepath):
        errors.append(f"SKIP {pid}: file not found")
        continue

    with open(filepath, "r") as f:
        lines = f.readlines()

    # Check if already has tradition
    content = "".join(lines)
    if "self.tradition" in content and "self.key_concepts" in content:
        print(f"SKIP {pid}: already has tradition + key_concepts")
        continue

    # Find the closing ) of super().__init__(...) by tracking parens
    in_super_init = False
    paren_depth = 0
    insert_line_idx = None

    for i, line in enumerate(lines):
        if "super().__init__(" in line:
            in_super_init = True
            paren_depth = 0
            # Count parens in this line
            for ch in line:
                if ch == "(":
                    paren_depth += 1
                elif ch == ")":
                    paren_depth -= 1
            if paren_depth <= 0:
                insert_line_idx = i + 1
                break
        elif in_super_init:
            for ch in line:
                if ch == "(":
                    paren_depth += 1
                elif ch == ")":
                    paren_depth -= 1
            if paren_depth <= 0:
                insert_line_idx = i + 1
                break

    if insert_line_idx is None:
        errors.append(f"ERROR {pid}: could not find super().__init__ closing")
        continue

    # Build the insertion lines
    kc_str = repr(key_concepts)
    insert_lines = [
        f'        self.tradition = "{tradition}"\n',
        f'        self.key_concepts = {kc_str}\n',
    ]

    # Insert after the super().__init__() line
    new_lines = lines[:insert_line_idx] + insert_lines + lines[insert_line_idx:]

    with open(filepath, "w") as f:
        f.writelines(new_lines)

    modified.append(pid)
    print(f"OK {pid}")

for e in errors:
    print(e)

print(f"\nModified {len(modified)} files")
