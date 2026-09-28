# Narration and visual plan — Week 1 explainer

**Student:** Yudan (Anica) Zhou · INFO 7375 · Fall 2026
**Concept (one):** Why the reference implementation subtracts the maximum score
before exponentiating — what that changes, and what it does not.
**Source:** Chapter 1, Part 2, "The subtraction that changes nothing important."
**Target runtime:** 2:30–3:10.

This file is the reviewed content plan. It is **not** a renderable beat sheet —
the Brutalist `ai-explainer` builder maps it onto the current schema and writes
`beat_sheet.json`. Every number below comes from `evidence/evidence_output.json`,
produced by `evidence/max_subtraction_evidence.py`. Nothing here is invented or
illustrative, so no beat needs a "constructed" label.

The builder supplies fixed bookends (Claude composer hello; a typed overview;
"Your turn"; a channel card). Beats A–F below are the teaching middle.

---

## Beat A — The move nobody explains

**Narration**
> The course's reference implementation does not exponentiate your scores. It
> finds the largest one and subtracts it from all of them first. Scores one,
> two, three become minus two, minus one, zero. That is the whole of this
> video: what did that subtraction change?

**On screen:** `[1, 2, 3]` → `peak = 3` → `[-2, -1, 0]`. The subtraction
animates; nothing else on screen yet.

---

## Beat B — Watch the numbers move

**Narration**
> Each shifted score goes through the exponential. The largest score is now
> exactly zero, so its weight is exactly one. Every other weight is smaller
> than one. Add them: one point five oh three two. Divide each weight by that
> total, and those are the probabilities.

**On screen (all real, from case A):**

| step | value |
|---|---|
| shifted | `[-2, -1, 0]` |
| weights | `[0.1353352832, 0.3678794412, 1.0]` |
| total | `1.5032147244` |
| probabilities | `[0.0900305732, 0.2447284711, 0.6652409558]` |

Weights fill in one at a time; the total accumulates; the division runs last.

---

## Beat C — Why it is allowed

**Narration**
> Here is the reason it is safe. Exponentiating a difference splits into a
> product: e to the z over T, times e to the minus m over T. That second factor
> is the same in every numerator — and it is in every term of the denominator
> too. It cancels. The intermediate weights changed. The ratio between any two
> of them did not, and the ratio is the whole distribution.

**On screen:** the identity from the chapter, with `exp(-m/T)` highlighted top
and bottom and then struck through:

```
exp((z_i - m)/T)            exp(z_i/T) · exp(-m/T)
-------------------  =  ------------------------------
Σ_j exp((z_j - m)/T)     exp(-m/T) · Σ_j exp(z_j/T)
```

---

## Beat D — Both routes, same answer

**Narration**
> That is the algebra. Here is the run. I computed the same distribution twice
> for scores one, two, three — once the shifted way, once straight from the
> original scores. Largest absolute difference between them: one point one one
> times ten to the minus sixteen. That is floating-point noise, not a different
> distribution.

**On screen:** real terminal output, case A — `reference_shifted`,
`direct_unshifted`, and `max_abs_difference: 1.1102230246251565e-16`.

---

## Beat E — Where the direct route stops existing

**Narration**
> Now the case the shift is actually for. Two equal scores of one thousand.
> Straight exponentiation does not return a wrong answer — it does not return
> at all. OverflowError, math range error. Subtract the maximum and the same
> input becomes zero, zero; weights one, one; total two; one half and one half.
> The thousand was in both entries. It never carried any information about
> which outcome is preferred, and it never needed to reach the exponential.

**On screen:** split. Left — `math.exp(1000)` raising
`OverflowError: math range error`. Right — `[1000, 1000]` → `[0, 0]` →
`[1.0, 1.0]` → `total 2.0` → `[0.5, 0.5]`.

---

## Beat F — What this does not establish

**Narration**
> One boundary, and the chapter names it: keep the claim narrower than
> "numerically stable." Take scores zero and minus one thousand. The maximum is
> already zero, so subtracting it changes nothing, and e to the minus one
> thousand underflows to exactly zero point zero. The function returns one and
> zero. The real second probability is about five times ten to the minus four
> hundred thirty-five — vanishingly small, but not zero. Subtracting the
> maximum removes overflow at the top. It does nothing about underflow at the
> bottom, and it does not tell you it happened.

**On screen:** case C — `probabilities([0, -1000])` → `[1.0, 0.0]`, beside
`float exp(-1000) = 0.0` and `decimal exp(-1000) = 5.07595889755E-435`.

---

## Claims I must be able to defend

1. Max-subtraction changes the intermediate weights, not the returned
   distribution — because the common factor `exp(-m/T)` cancels.
2. The cancellation is an identity in exact arithmetic; the `1.11e-16` gap in
   case A is a floating-point artifact of the two computation orders, not
   disagreement between the two formulas.
3. `[1000, 1000]` is not a case where the direct route is *less accurate*; it is
   a case where it raises and produces nothing.
4. The demonstration does not establish general numerical stability. Case C is
   my counterexample: the shift does not prevent underflow, and the returned
   `0.0` is a float result, not the value of the expression.
5. None of this says anything about whether an outcome is *correct*. It is a
   claim about a normalization, and no answer key enters this function.

## Environment recorded with the run

Python 3.14.2 (CPython), Windows 11. The chapter's recorded run used Python 3.14.6
and reports the same probabilities; my run reproduces them.

Against the scaffold's earlier Linux run (Python 3.11.15), case A's unshifted
values differ in the last two digits (`…046`→`…045`, `…767`→`…764`), while
`max_abs_difference` and cases B and C are identical.
