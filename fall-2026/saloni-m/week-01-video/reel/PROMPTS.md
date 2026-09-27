# PROMPTS.md — Seeded, Not Settled

Beat-prefixed prompts for open slots.

## Status

**No open slots.** All nine beats are filled — five Manim scenes in
`scenes.py`, four Remotion patterns from the Brutalist component library.
Nothing is slated, so no request cards are outstanding.

This file records the prompts that produced the authored material, per the
course AI policy requirement to name what Claude contributed.

## Authoring prompts (Claude, 2026-09-27)

### Reel-level — concept selection
Asked Claude which Chapter 1 concept could be shown with terminal evidence
rather than asserted. Outcome: accepted the seed concept. Rejected an opening
that defined pseudo-randomness abstractly — the diff makes the point faster.

### B04 — the turn
Claude noticed that the observed count in my own run (630) matched a figure
named on the assignment's concept list, and that p × 1000 = 665.24. I
computed the per-token table and confirmed it with `verify_claims.py`.
Outcome: revised — this became the centre of the video rather than a
side note.

### B05 — the constraint
Claude drafted the sum-to-zero observation. I checked it against my own
numbers (7.11e-14) and decided it earned a beat because it limits what the
gap can be used to argue.

### scenes.py — Manim
Claude wrote the five scene classes against the real figures. First version
used `NumberLine(include_numbers=True)`, which failed on this machine for
lack of LaTeX. Fixed by placing `Text` tick labels manually rather than
installing MacTeX.

### BVDT — the boundary
The verdict card's fourth line — "Does not establish that the answer is
correct" — is the assignment's required boundary statement. The narration
adds the binomial framing as an acknowledged limitation, flagged in
FACTCHECK.md row 16 as stated-but-not-verified.

## Verbatim prompt text

The verbatim prompt text was not kept. `../BUILD-PROMPT.md` §4 records each
prompt's purpose, its substance, and whether the result was accepted,
revised, or rejected.
