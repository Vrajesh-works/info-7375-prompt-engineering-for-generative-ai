# Real Claude response used in B00

**Model:** Claude Opus 5 (Claude Code)
**Date obtained:** 2026-09-27
**Session:** the build session for this reel
**Prompt (exactly as typed on screen in B00):**

> Where does "thousands of years to read the training data" actually come from? Show me the arithmetic, and name every input the sentence doesn't state.

**Response, verbatim and complete:**

---

It comes from a division, not a measurement.

The arithmetic, using GPT-3's published figures (Brown et al. 2020, arXiv:2005.14165):

- 300,000,000,000 training tokens
- × 0.75 words per token = 225,000,000,000 words
- ÷ 250 words per minute = 1,711 years
- ÷ 200 words per minute = 2,139 years
- ÷ 150 words per minute = 2,852 years

The sentence states none of the following inputs:

1. The words-per-token conversion. 0.75 is a convention, not a measurement, and it varies by tokenizer and by language.
2. The reading rate. This is the big one — it moves the answer by 1,141 years across plausible values.
3. That reading is continuous, with no sleep and no rereading.
4. Which model's token count is meant. Later systems trained on far more, and most do not publish the figure.
5. The length of a year, which is needed to turn minutes into years at all.

So "thousands of years" is an illustration with a hidden parameter, not a measured quantity. The claim that survives every choice of rate is the weaker, true one: more text than a person could read in many lifetimes.

---

**Lines excerpted on screen in B00** (verbatim substrings of the above; `…` marks elision):

1. `It comes from a division, not a measurement.`
2. `× 0.75 words per token = 225,000,000,000 words`
3. `÷ 250 words per minute = 1,711 years`
4. `The reading rate … moves the answer by 1,141 years`

**Verification.** Every figure in this response was checked against the chapter's own
derivation script `research/llm_scale.py`, run locally on 2026-09-27. Its recorded
output gives 1,711.2 / 2,138.9 / 2,851.9 years and 9,950,059.57 years — matching to
the rounding shown. See FACTCHECK.md.
