# Comprehensive Multi-Layer Philosopher Tests

## Overview

This test suite (`test_comprehensive_layers.py`) validates all 20 philosopher modules across 4 critical layers:

### Layer 1: API / Schema Layer
- Tests that `reason(text, context)` returns correct dict structure
- Validates all required fields are present
- Ensures data types are correct
- **Status**: ✅ 17/20 passing (Heidegger, Kierkegaard, Nietzsche have implementation bugs)

### Layer 2: Concept Detection Layer
- Tests that each philosopher's key concepts are properly detected
- Validates concept-specific text triggers correct analysis
- Ensures concept detection is accurate and consistent
- **Coverage**: Arendt (11 tests), Nietzsche (8 tests), Confucius (5 tests), Aristotle (6 tests), Sartre (5 tests)

### Layer 3: Tension / Contradiction Layer
- Tests that `_identify_tension()` correctly detects contradictions
- Validates tension levels are appropriately calculated
- Ensures tension elements are meaningful
- **Status**: ✅ Tests for Arendt, Nietzsche, Confucius

### Layer 4: Reasoning Text Layer
- Tests that reasoning text is consistent with analysis
- Validates reasoning mentions key detected concepts
- Ensures no contradictions between reasoning and analysis
- **Status**: ✅ Tests for all major philosophers

## Concept Detection Tests by Philosopher

### Hannah Arendt
- ✅ Vita Activa (Labor, Work, Action)
- ✅ Natality
- ✅ Public/Private Realm
- ✅ Plurality
- ✅ Banality of Evil
- ✅ Totalitarianism
- ✅ Political Judgment
- ✅ Freedom

### Friedrich Nietzsche
- Will to Power
- Übermensch
- Eternal Recurrence
- Nihilism (Passive/Active)
- Master/Slave Morality
- Ressentiment
- Amor Fati
- Dionysian/Apollonian

**Note**: Nietzsche tests reveal implementation bug - `ressentiment["present"]` should be `ressentiment["presence"]`

### Confucius
- ✅ Ren (Benevolence)
- ✅ Li (Ritual Propriety)
- ✅ Yi (Righteousness)
- ✅ Xiao (Filial Piety)
- ✅ Junzi (Exemplary Person)

### Aristotle
- Virtue (Arete)
- Golden Mean
- Eudaimonia
- Four Causes
- Practical Wisdom (Phronesis)
- Telos

**Note**: Tests reveal that Aristotle's implementation uses different key names than expected

### Jean-Paul Sartre
- Freedom
- Responsibility
- Bad Faith
- Engagement
- Anguish

**Note**: Tests reveal that Sartre's implementation uses different structure than expected

## Known Issues Found by Tests

### Implementation Bugs
1. **Nietzsche** (`nietzsche.py:605`): `KeyError: 'present'`
   - Should be `ressentiment["presence"]` instead of `ressentiment["present"]`

2. **Heidegger** (`heidegger.py:161`): `KeyError: 'past_awareness'`
   - Missing key in temporality analysis

3. **Kierkegaard** (`kierkegaard.py:659`): `KeyError: 'present'`
   - Should be `despair["presence"]` or similar

### Schema Mismatches
- Aristotle: Expected keys like `virtue_present`, `mean_present` don't match implementation
- Sartre: Expected keys like `freedom_present`, `engagement_present` don't match implementation

## How to Run Tests

```bash
# Run all comprehensive tests
PYTHONPATH=/home/user/Po_core/src:$PYTHONPATH pytest tests/unit/test_philosophers/test_comprehensive_layers.py -v

# Run specific layer
PYTHONPATH=/home/user/Po_core/src:$PYTHONPATH pytest tests/unit/test_philosophers/test_comprehensive_layers.py::TestLayer1_APISchema -v

# Run specific philosopher concept tests
PYTHONPATH=/home/user/Po_core/src:$PYTHONPATH pytest tests/unit/test_philosophers/test_comprehensive_layers.py::TestLayer2_ConceptDetection::test_arendt_natality_detection -v
```

## Next Steps

1. **Fix Implementation Bugs**:
   - Correct key names in Nietzsche, Heidegger, Kierkegaard modules

2. **Align Test Expectations**:
   - Update tests to match actual implementation schemas for Aristotle, Sartre
   - OR update implementations to match expected schemas

3. **Expand Coverage**:
   - Add concept detection tests for remaining 15 philosophers
   - Add more edge case tests

4. **AI Testing**:
   - As mentioned in the task description, users can test with Claude, GPT, Gemini, Grok
   - Create example prompts for each philosopher
   - Validate responses against expected concept detections

## Test Statistics

- **Total Tests**: 100+
- **Layer 1 (API/Schema)**: 140 tests (20 philosophers × 7 test cases)
- **Layer 2 (Concept Detection)**: 35 tests (detailed tests for 5 philosophers)
- **Layer 3 (Tension Detection)**: 10 tests
- **Layer 4 (Reasoning Text)**: 10 tests
- **Cross-Layer Integration**: 12 tests

## Contributing

When adding new philosopher concept tests, follow this pattern:

```python
def test_philosopher_concept_detection(self):
    """Test Philosopher detects specific concept."""
    philosopher = Philosopher()
    text = "Text containing concept keywords"
    result = philosopher.reason(text)

    assert "concept_field" in result
    concept = result["concept_field"]
    assert concept["concept_present"] is True
```

Make sure to:
1. Use specific, targeted text that clearly contains the concept
2. Test for the actual field names in the implementation
3. Add descriptive docstrings
4. Test both presence and absence of concepts
