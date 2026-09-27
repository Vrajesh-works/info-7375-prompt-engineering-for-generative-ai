# FACTCHECK — Temperature Is Not a Fact Checker.

Every on-screen or spoken number was printed by `code/run_temperature.py`, which
calls the chapter's own `probabilities()` and `sample()` (copied verbatim into
`code/main.py` from `01-randomness-and-first-prompts.md`). Run on 2026-09-23,
Python 3.11.16, toolkit venv. Output: `code/temperature_results.json`.

| Claim (beat) | Evidence | Status |
|---|---|---|
| A chatbot writes one token (roughly one word) at a time, scoring every possible next token (B01A) | Chapter 1 fig. 1 caption: "A chatbot is one prediction, run in a loop… one token is sampled and appended"; §35: "The machine does not predict words. It predicts tokens… a common word may be one token, a rare word several" → narration says "roughly one word", a simplification the chapter supports; §37: "a number for every token in the vocabulary" | ✓ |
| Paris high, Lyon lower (B01A) | ILLUSTRATIVE only: bars carry no numbers and are stamped "ILLUSTRATIVE SCORES · NOT FROM A REAL MODEL"; no model was queried | ✓ (labelled) |
| Softmax turns scores into chances that add up to one (B01A) | chapter's probabilities(): weights / total; §37 "arranged so the numbers are nonnegative and sum to one" | ✓ |
| Scores [1, 2, 3] are constructed toy inputs (B02, B03, B07) | Chapter §"Temperature is a concentration control" uses these scores; labelled CONSTRUCTED on screen | ✓ |
| e ≈ 2.71828, a fixed mathematical constant (B02) | math.e = 2.718281828…; standard definition | ✓ |
| e raised to any score is positive; bigger scores grow much faster (B02) | exp(x) > 0 for all real x and is increasing and convex; shown values e^-1…e^3 = 0.37, 1, 2.72, 7.39, 20.09 from math.exp | ✓ |
| Any base above 1 would keep the order; e is the standard choice because it keeps the math simple (B02) | b^x is increasing for any b > 1, so ranking is kept; note e^(z/T) = (e^(1/T))^z, i.e. temperature is equivalent to changing the base. e is conventional (natural exponential; simplest derivatives). Claim kept deliberately modest: not stated as the only valid base | ✓ |
| Weights e^1, e^2, e^3 = 2.72 / 7.39 / 20.09; total 30.19 (B02B) | math.exp; total = 30.1929 (earlier explanation said 30.20 — that was a sum of rounded values; screen shows 30.19) | ✓ |
| B02/B03 show direct exponentials; the chapter's code subtracts the max first (B02 footer) | chapter §"The subtraction that changes nothing important": the common factor cancels, same distribution; build_props asserts direct == probabilities() to 1e-12 | ✓ |
| T=0.5: z/T = 2, 4, 6; weights 7.39 / 54.60 / 403.43; T=2: 0.5, 1, 1.5; weights 1.65 / 2.72 / 4.48 (B03) | computed with the same z/T then exp; chances match the chapter's table | ✓ |
| T=1 → 0.0900 / 0.2447 / 0.6652 (B02) | run_temperature.py; matches chapter table to 10 d.p. | ✓ |
| T=0.5 top 0.8668, T=2 top 0.5065, bottom 0.1863 at T=2 (B03, B00) | same; matches chapter table | ✓ |
| Ranking 2 > 1 > 0 at every T > 0 (B03, B04, BVDT) | algebra: z/T and exp are monotone for T > 0, normaliser shared; script asserts argmax = 2 at all three T | ✓ |
| p_i/p_k = exp((z_i − z_k)/T) (B04) | chapter's ratio identity; normaliser cancels. Checked numerically: p2/p0 = e^(2/T) to 1e-9 | ✓ |
| Ratios 54.60 / 7.39 / 2.72 (B04) | e^4, e^2, e^1; script assert | ✓ |
| Temperature enters the arithmetic in one place (B05) | `weights = [math.exp((x - peak) / temperature) ...]` is the only arithmetic use; the other use is the validation guard | ✓ (wording: "arithmetic", not "code") |
| T = 0 is rejected (B05) | `probabilities([1,2,3], 0)` raises ValueError "Need logits and a positive finite temperature" | ✓ |
| Seed 7, n=1000 counts 18/133/849 (T=0.5) and 202/329/469 (T=2) (B06) | run_temperature.py; identical to the chapter's recorded counts (chapter ran Python 3.14.6) | ✓ |
| Correct answer 9.0% → 1.6%, wrong favourite 66.5% → 86.7% (B07) | P[T=1][0]=0.0900, P[T=0.5][0]=0.0159; P[2] 0.6652 → 0.8668. Answer key is CONSTRUCTED (chapter's own counterexample), labelled on screen | ✓ |
| B07 card shows the softmax formula; its only inputs are z and T | the chapter's probabilities(logits, temperature) signature | ✓ |
| Ending (BVDT, author's wording): "Nothing broke… more confidently wrong"; "Low temperature gives you more consistent answers, not more correct ones"; "Being correct depends on the scores…" | refers to the B07 constructed case (labelled on the card: "constructed case: 9.0% → 1.6%"); consistency = concentration shown in B03/B06; correctness not an input to the formula (B05, B07) | ✓ |
| "not a real Claude error" (B07) | chapter: "Do not report that hypothetical as an observed Claude error" | ✓ |
| Boundary: nothing here shows how a Claude product sets/exposes temperature (B08) | chapter: "this toy interface is not a promise about which controls any Claude model exposes" | ✓ |

**Algebra checks (MATH-TYPESETTING.md):** domain T > 0 stated; ratio uses free indices i, k;
B04 row expressions use "≈" for rounded values, "=" only for exact steps.

**Corrections applied while scripting (DOUBLE-CHECK LAW):**
- Draft said "temperature appears in exactly one place in the code" → false (the guard also
  reads it). Narration now says "enters the arithmetic in one place".
- No figure rounds in a direction that flatters the claim: 86.68% shown as 86.7%, 50.65% as 50.6%.
