# SHOTLIST.md — Seeded, Not Settled

Typed work order. Durations are Kokoro ground truth (measured 2026-09-27),
not estimates. Total 2:45.

| Beat | Act | Lane | Asset | Dur | Status |
|------|-----|------|-------|-----|--------|
| B00 | ASK | Remotion | `ClaudeComposerAsk` | 9.19s | SHOW |
| B01 | MECHANISM | Manim | `B01_SeedMechanism` | 30.27s | SHOW (constructed element labelled) |
| B02 | EVIDENCE — same seed | Manim | `B02_SameSeed` | 12.10s | SHOW |
| B03 | EVIDENCE — different seed | Manim | `B03_DifferentSeed` | 17.09s | SHOW |
| B04 | THE TURN | Manim | `B04_ExpectedVsObserved` | 21.80s | SHOW |
| B05 | CONSTRAINT | Manim | `B05_GapsSumToZero` | 17.41s | SHOW |
| BVDT | VERDICT | Remotion | `ClaudeVerdictArtifact` | 34.72s | SHOW |
| BHTF | HANDOFF | Remotion | `ClaudeComposerAsk` | 20.31s | SHOW |
| BOUT | OUTRO | Remotion | `ClaudeTitleOutro` | 3.03s | SHOW |

**Total: 165.92s = 2:45.** Within the assignment's 2–4 minute window.

## Lane histogram

- Manim: 5 beats, 98.67s (59%) — the concept
- Remotion: 4 beats, 67.25s (41%) — the required Claude bookends

## Per-beat visual intent

**B01** — source lines 19 and 22 fade in, line 22 highlighted in terracotta.
Then a constructed diagram: seed 7 → generator box → a fixed draw sequence.
`CONSTRUCTED ILLUSTRATION` sits in the upper-left for the whole beat.

**B02** — `run-A.txt` and `run-B.txt` side by side, each showing the three
counts. Then the diff command, then the empty result in green.

**B03** — `seed=7` transforms to `seed=10`. Three rows animate the count
changes; token 2's new value in terracotta.

**B04** — `p = 0.6652` then `p x 1000 = 665.24`. A number line 600–700 draws
in with plain Text tick labels. A dashed marker lands at 665.24. The observed
dot lands at 630 in terracotta. The gap bar draws between them, labelled
−35.24. Closing line: the same 630 on every seed-7 run.

**B05** — four-column table, all three tokens, expected / observed / gap.
A rule, then the sum resolving to 0.00 in green, then the reason.

## No slates

Every output beat is filled. Nothing ships as a request card.

## Constraint noted

No LaTeX on this machine, so all Manim text uses `Text()`. `NumberLine`'s
`include_numbers=True` routes through `DecimalNumber` → `MathTex` → LaTeX and
failed; tick labels are placed manually as `Text`. Logged in FRICTIONAL.md.
