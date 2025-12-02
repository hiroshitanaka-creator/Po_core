# Cross-LLM Emergence Experiment V3 - Quick Reference

## 🎯 What is V3?

V3 validates **Po_core's TRUE architecture**: Ethics FIRST, then philosophical debate.

```
┌─────────────────────────┐
│   W_ethics (核)          │  ← Ethical constraints come FIRST
│         ↓               │
│   Philosophers debate   │  ← Within ethical bounds
│         ↓               │
│   Emergence + Ethics    │  ← Po_core's goal
└─────────────────────────┘
```

---

## 🚀 Quick Start (30 minutes)

### Step 1: Run the script
```bash
cd /home/user/Po_core/experiments
python cross_llm_emergence_test_v3.py --mode manual \
  --condition high_tension_with_ethics
```

### Step 2: What you'll test

**Key comparison**: WITH ethics vs WITHOUT ethics

**Test**: `high_tension_with_ethics`
- Philosophers: Aristotle + Nietzsche + Derrida
- **WITH** ethical constraint
- Expected: Nietzsche transforms from "destroyer" to "diversity enhancer"

**Test**: `high_tension_no_ethics` (for comparison)
- Same philosophers
- **WITHOUT** ethical constraint
- Expected: Nietzsche unconstrained, potentially destructive

### Step 3: The workflow

1. **Script shows prompt** → Copy it
2. **Paste to LLM** (GPT-o1, Gemini, Claude) → Get response
3. **Paste response back** → Script evaluates
4. **Get evaluation prompt** → Copy to judge LLM
5. **Paste JSON back** → See results

---

## 📊 What You'll Discover

### Expected Results:

**WITH ethical constraints**:
```
Emergence:        75-85% (Sweet Spot maintained!)
Ethics Alignment: 90%+  (Strong ethical grounding)
Nietzsche:        "Enhance diversity" (constructive)
```

**WITHOUT ethical constraints**:
```
Emergence:        85-90% (Slightly higher creativity)
Ethics Alignment: 50-70% (Ethically questionable)
Nietzsche:        "Destroy convention" (potentially harmful)
```

### The Discovery:

**Ethical constraints transform philosopher behavior while maintaining emergence!**

This validates Po_core's ethics-first design.

---

## 📁 Files

### Use V3 for Po_core validation:
- **`cross_llm_emergence_test_v3.py`** - Main framework
- **`EXPERIMENT_GUIDE_V3.md`** - Complete guide
- **`CHANGELOG_V3.md`** - What changed from V2

### Previous versions (still useful):
- `cross_llm_emergence_test_v2.py` - LLM-as-judge (4 metrics)
- `cross_llm_emergence_test.py` - Original manual testing
- `EXPERIMENT_GUIDE.md` - Original guide

---

## 🎯 Six Conditions to Test

### Main Comparisons:
1. **`high_tension_with_ethics`** ← Start here!
2. **`high_tension_no_ethics`** ← Compare with #1
3. `low_tension_with_ethics`
4. `low_tension_no_ethics`
5. **`optimal_with_ethics`** ← Po_core Sweet Spot
6. `optimal_no_ethics`

### Baselines:
7. `single_philosopher`
8. `plain_llm`

---

## 📈 Five Metrics (NEW!)

V3 evaluates 5 metrics instead of 4:

1. **Novelty** (0-100%): Creative insights
2. **Integration** (0-100%): Synthesis quality
3. **Depth** (0-100%): Philosophical sophistication
4. **Coherence** (0-100%): Logical consistency
5. **Ethical Alignment** (0-100%): ← **NEW!** Respects life-structures

**Emergence Score** = Weighted average of all 5

---

## ✅ Success Criteria

### Po_core validated if:

1. ✅ WITH ethics achieves **>75% emergence** (Sweet Spot maintained)
2. ✅ WITH ethics achieves **>85% ethics** (Strong alignment)
3. ✅ Nietzsche **transforms** (destroyer → enhancer)
4. ✅ **`optimal_with_ethics`** hits Sweet Spot (75-85% + 90% ethics)

**All 4 met** → 🎉 **Po_core architecture validated!**

---

## 💡 Key Insight

Your critical realization:

> "Po_coreは核に倫理があって、その上で哲学者が殴り合ってるわけじゃん？"
>
> (Po_core has ethics at its core, with philosophers debating on top of that.)

**V1/V2** tested: Dialectical tension alone
**V3** tests: Ethics + Dialectical tension (Po_core's TRUE design)

---

## 🐷 Next Steps

### 1. Run Quick Test (recommended)
```bash
python cross_llm_emergence_test_v3.py --mode manual \
  --model gpt-o1 \
  --condition high_tension_with_ethics
```

Test 2-3 questions, takes 30 minutes.

### 2. Compare WITH vs WITHOUT
Run both:
- `high_tension_with_ethics`
- `high_tension_no_ethics`

See how ethical constraints transform results!

### 3. Full Validation
Test all 6 main conditions to fully validate Po_core.

---

## 📚 Documentation

- **Quick Reference**: This file (README_V3.md)
- **Complete Guide**: EXPERIMENT_GUIDE_V3.md (日本語説明あり)
- **Changelog**: CHANGELOG_V3.md (V2からの変更点)
- **Original Guide**: EXPERIMENT_GUIDE.md

---

**Ready to validate Po_core's ethics-first architecture?** 🚀

```bash
python cross_llm_emergence_test_v3.py --mode manual
```

🐷🎈 **Let's prove the flying pig can fly ethically!**
