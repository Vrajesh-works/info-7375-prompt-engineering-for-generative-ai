# FACTCHECK — low-temperature-is-not-argmax

Sources checked:
- `demo.py` (this folder), re-run on Python 3.11.15, 2026-09-27
- `chapters/01-randomness-and-first-prompts.md` (a local copy was used)

Every number in the video was reproduced by running `demo.py`; none were copied
from notes.

## Correction — the "temperature never produces zero variance" claim (2026-09-27)

**The false claim.** Earlier cuts said that no positive temperature ever produces
the zero-variance result argmax gives:
- B06 narration: "Temperature never produces that, at any positive value."
- B06 on-screen verdict: "no positive temperature ever produces this — zero
  variance is a different operation"
- B09 card line 3: "… shows real zero-variance determinism — temperature never
  produces that"
- B09 card line 5: "temperature concentrates probability; it never switches to argmax."
- B05, B07 and B08 narration made the same claim or implied it (B08 dared the
  viewer to check whether the sampler "ever produces zero variance").

**Why it was wrong.** It confuses two separate facts:
1. *Exact math.* For any T > 0, softmax gives every outcome a strictly positive
   probability, so the distribution is never exactly one-hot. This part is true.
2. *Observed output.* A finite sample can still land on one outcome every time,
   and it usually does at low T. Separately, IEEE-754 doubles can't represent
   `exp(-x)` for x > ~745.13, so it underflows to 0.0. With scores [1, 2, 3], that
   makes outcome 1's probability exactly 0 for T < ~0.00134, and outcome 0's for
   T < ~0.00268. Below those temperatures the reference implementation returns
   [0.0, 0.0, 1.0], and `sample()` then behaves exactly like `argmax_select()`.

**The data that disproved it** (real output of the chapter's reference
`probabilities()` / `sample()` via `demo.py`, scores [1, 2, 3], count=1000, seed=7):

| T | `probabilities([1,2,3], T)` | `sample(...)` |
|---|---|---|
| 0.5 | [0.015876239976466765, 0.11731042782619838, 0.8668133321973349] | {2: 849, 1: 133, 0: 18} |
| 0.1 | [2.061060046209062e-09, 4.539786860886666e-05, 0.999954600070331] | **{2: 1000}**: zero observed variance from a positive temperature |
| 0.01 | [1.3838965267367376e-87, 3.720075976020836e-44, 1.0] | **{2: 1000}** |
| 0.001 | **[0.0, 0.0, 1.0]**: the losing probabilities underflow to exactly zero | **{2: 1000}** |

**What the video now says.** `argmax_select()` is deterministic *by construction*.
Sampling is not deterministic by definition, even when a run looks identical, and at
low enough temperatures its output can become numerically identical to argmax's.
The operation stays different; the observed numbers need not. The rewritten beats
are B05, B06 (narration and on-screen verdict), B07, B08 and B09 (narration and
card lines 3 and 5).

## Claims table

| # | Beat | Claim (spoken / shown) | Verdict | Evidence |
|---|---|---|---|---|
| 1 | B00 | "set temperature to zero for deterministic output" is a common line | ✅ framing | Presented as a slogan to test, not as a fact |
| 2 | B01 | Production systems are built on the T=0 = deterministic assumption; "The claim / test / risk / proof" card | ✅ framing | Unquantified, no statistic given; card text restates the beat structure |
| 3 | B02 | The chapter's `probabilities()` is "copied exactly" into the demo | ✅ PASS | `probabilities()` and `sample()` in demo.py are byte-identical to the chapter's code blocks (programmatic comparison) |
| 4 | B03 | The guard clause refuses T ≤ 0 or non-finite T before computing anything | ✅ PASS | On-screen code = the chapter's code; the first statement raises before any `exp` |
| 5 | B04 | `probabilities([1,2,3], temperature=0)` raises ValueError | ✅ PASS | demo.py: `ValueError: Need logits and a positive finite temperature` |
| 6 | B04 | At T=0.5 the top outcome is assigned ~87% | ✅ PASS | 0.8668133321973349 (shown as 86.7%) |
| 7 | B04 | It wins 849 of 1000 draws (seed 7), "matching the chapter's own published table exactly" | ✅ PASS | demo.py {2: 849, 1: 133, 0: 18}; chapter table row `0.5 | 18 | 133 | 849 | 1,000` |
| 8 | B04/B09 | "the other one hundred fifty-one draws" | ✅ PASS | 18 + 133 = 151 |
| 9 | B05/B06 | `argmax_select()` returns the top index by construction; 1000 of 1000 identical | ✅ PASS | demo.py {2: 1000}; the function has no randomness (`[best] * count`) |
| 10 | B06 | argmax_select is constructed for this video, not part of the chapter | ✅ PASS | demo.py labels it "NOT from the chapter"; the on-screen caption says so |
| 11 | B06 | Sampling can produce the same identical result, especially at lower temperatures | ✅ PASS | T=0.1 → {2: 1000} (correction table above) |
| 12 | B07 | Ratio p_k/p_i = exp((z_k − z_i)/T) grows without limit as T → 0⁺; in exact math every outcome keeps positive probability | ✅ PASS | Algebra section below |
| 13 | B07 | A run of many draws can land on one outcome every time by chance | ✅ PASS | T=0.1: p(top) = 0.99995 → {2: 1000} |
| 14 | B07 | In floating point, low enough T makes the other probabilities underflow to exactly zero | ✅ PASS | T=0.001 → [0.0, 0.0, 1.0]; thresholds T < ~0.00134 / ~0.00268 for [1, 2, 3] |
| 15 | B07/B09 | Boundary: says nothing about a real product's temperature-zero setting | ✅ PASS | Scope statement; the video tests only the chapter's teaching implementation |
| 16 | B08 | At T = 0.01 the counts will "probably" come back identical | ✅ PASS | T=0.01 → {2: 1000} for [1, 2, 3]; "probably" is right because it depends on the viewer's own score gaps |
| 17 | B08 | Clone the repo, run main.py | ✅ PASS | The chapter links `lessons/01-randomness-and-first-prompts/code/main.py` and "the repository" |
| 18 | B09 | "Argmax_select is deterministic by construction; sampling can look that way at lower temperatures." | ✅ PASS | T=0.1 → {2: 1000} (correction table). Revised 2026-09-27 from "sampling only looked that way in this one run", which the video didn't support: the only on-screen sample (T=0.5) varied, with 151 non-top draws. |
| 19 | B09 card | Lines 1, 2, 4 (T=0 refused; ~87% and 151/1000 at T=0.5; boundary) | ✅ PASS | Rows 5–8 and 15 |
| 20 | B09 card | Line 3 "argmax_select() is deterministic by construction — sampling isn't, even when a run looks identical"; line 5 "can become numerically identical to argmax — but it isn't the same operation by definition" | ✅ PASS | Rows 9, 11, 14 |

## B07 — typeset equations (TypesetMath, per docs/MATH-TYPESETTING.md)

Renderer: `runtime/scripts/typeset_math.py` (matplotlib MathText → outlined SVG).
No LaTeX is installed on this machine, so Manim `MathTex` was not an option.

| Row | Expression | Check |
|---|---|---|
| 1 | p_i = exp(z_i/T) / Σ_j exp(z_j/T) | Same as demo.py `probabilities()`: subtracting the peak cancels between numerator and denominator. j is bound (summation); i is free. Domain T > 0, which is also what the implementation enforces (`temperature <= 0` raises). |
| 2 | p_k / p_i = exp((z_k − z_i)/T) | Follows from row 1: the denominators cancel. Exact equality. |
| 3 | p_k / p_i → ∞ as T → 0⁺, for z_k > z_i | (z_k − z_i)/T → +∞ when z_k − z_i > 0 and T → 0⁺. In exact arithmetic the limit is never reached: for every T > 0 the ratio is finite, so p_i > 0. In float64 the ratio overflows (p_i = 0.0) below the thresholds in row 14 above. The narration now states both. |

Numerical case (demo.py real output, z = [1, 2, 3], T = 0.5):
- p₂/p₁ = 0.8668133 / 0.1173104 = 7.389056 = e² ✓
- p₂/p₀ = 0.8668133 / 0.0158762 = 54.59815 = e⁴ ✓

Algebra corrections: none. The only correction was the observed-output claim above.
