# FACTCHECK.md — Seeded, Not Settled

Every factual claim spoken or shown, with its verdict, source, and any fix.
Source of record: `run-A.txt`, `run-B.txt` (seed 7), `run-C.txt` (seed 10),
produced 2026-09-27 from the unmodified
`lessons/01-randomness-and-first-prompts/code/main.py` (logits `[1,2,3]`,
`count=1000`). Re-checked by `evidence/verify_claims.py` — 7/7 passing.

| # | Beat | Claim | Verdict | Source | Fix |
|---|------|-------|---------|--------|-----|
| 1 | B01 | The seed is a default argument on line 19, not a module constant | VERIFIED | `grep -n "seed" main.py` → `19:def sample(logits, count=1000, seed=7, temperature=1.0)` | — |
| 2 | B01 | Line 22 builds its own generator rather than seeding the global random state | VERIFIED | `22:    rng = random.Random(seed)`; `random.Random(n)` instantiates a separate Random object | — |
| 3 | B01 | `demo()` does not override the default seed | VERIFIED | `demo()` calls `sample([1, 2, 3])` with no seed argument | — |
| 4 | B01 | The generator diagram is constructed | ACKNOWLEDGED | Not from any run; drawn to illustrate | Carries CONSTRUCTED ILLUSTRATION label on screen throughout the beat |
| 5 | B02 | Counts at seed 7 are 102, 268, 630 | VERIFIED | `run-A.txt`, `run-B.txt` | — |
| 6 | B02 | Two runs at seed 7 are byte-for-byte identical | VERIFIED | `diff run-A.txt run-B.txt` returns empty; `verify_claims.py` check 1 compares two fresh runs | — |
| 7 | B03 | Seed 10 gives 97, 213, 690 | VERIFIED | `run-C.txt` | — |
| 8 | B03 | The probabilities block is unchanged between seeds | VERIFIED | `diff run-A.txt run-C.txt` shows hunk `8,10c8,10` — counts only; `probabilities()` contains no call to `rng` | — |
| 9 | B04 | p for token 2 is 0.6652 (0.6652409557748218) | VERIFIED | `run-A.txt`; `verify_claims.py` check 2 | Narration rounds to 4 dp; full value is on screen in B01's source and in the sheet |
| 10 | B04 | Expected count is 665.24 | VERIFIED | 0.6652409557748218 × 1000 = 665.2410; `verify_claims.py` check 4 | — |
| 11 | B04 | Observed is 630, a shortfall of 35.24 | VERIFIED | 630 − 665.2410 = −35.2410; `verify_claims.py` check 5 | — |
| 12 | B04 | The shortfall is identical on every seed-7 run | VERIFIED | Follows from claim 6 (identical output); checked directly across two fresh runs | — |
| 13 | B05 | Gaps are +11.97, +23.27, −35.24 | VERIFIED | Computed from `run-A.txt`; `verify_claims.py` check 6 | — |
| 14 | B05 | The three gaps sum to zero | VERIFIED | Sum is 7.11e-14, i.e. zero to floating-point precision. Necessarily so: counts sum to 1000 and probabilities sum to 1 | Narration says "sum to zero", which is the mathematical claim; the residual is float representation |
| 15 | B05 | The deviations are not three independent observations | VERIFIED | Direct consequence of claim 14 — two gaps determine the third | — |
| 15a | B05 | "They are one observation wearing three hats" | LOOSE | The constraint leaves **two** free gaps, not one. "One observation" is true only in the sense that it is one sample of 1000 draws | "Not three independent" (row 15) is the claim to defend. The "one observation" wording is a figure of speech; not re-rendered |
| 18 | B00 | Composer card with a prompt, a model chip and three "output" lines | CONSTRUCTED, NOT LABELLED ON SCREEN | Stock `ClaudeComposerAsk` pattern; the prompt and output lines are authored props summarising the video, not a Claude response | Disclosed in SOURCES.md. It should carry an on-screen "constructed" label on any re-render |
| 16 | BVDT | A gap this size is ordinary sampling noise at n=1000 | OVERSTATED, NOT VERIFIED | SD of a binomial count at n=1000, p=0.665 is √(1000·0.665·0.335) ≈ 14.92, so −35.24 is ≈ 2.36 SD (two-sided p ≈ 0.018 under a correct sampler). That is unusual, not "ordinary". Not computed in the course code | The narration states it more strongly than the numbers support. The defensible version: "could be sampling noise; two seeds cannot tell." Not re-rendered; disclosed here and in FRICTIONAL.md |
| 17 | BVDT | Repeatability is a property of the process; truth is a property of the claim | INTERPRETATION | The video's thesis, not a measurement | Delivered as the boundary statement, not as a finding |

## Claims deliberately NOT made

- That the sampler is biased or broken. Two seeds cannot establish it.
- That 630 is "wrong". It is one draw from a distribution.
- That matching 665.24 would have validated anything.
- Any claim about Claude's behaviour. No real Claude output appears in this video.
  The B00 composer card imitates the Claude interface with authored text (row 18).

## Not verified

- Cross-platform and cross-version reproducibility of `random.Random`. Tested on one machine, Python 3.13 (course run) only.
- Whether `Counter` key order is guaranteed or incidentally stable across versions.
