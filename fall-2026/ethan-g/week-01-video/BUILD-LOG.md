# BUILD-LOG — A training-scale slogan restated as a division with a hidden assumption

## Brief
"A training-scale slogan restated as a division with a hidden assumption",
12 beats, 2–4 minutes, Kokoro `am_onyx`, stop at the review cut.
Source: INFO 7375 chapter 1. Measured runtime lands inside the requested window
(see the run report); duration remains an output, not a target.

## GATE L — library-first (the punt record)
`./art scenes` was run before authoring, on four phrasings of the needs: an
arithmetic derivation worked line by line; one calculation at three input values;
a headline claim with its citation; two similar claims an order of magnitude
apart. Every candidate returned was a figure built for a different reel —
sleeper-agents bar charts, values axes, economic-index scatters — at low scores.
Nothing in the library illustrates a derivation.

A genuine miss is a design card. Five components were built into
`runtime/remotion/src/scenes/DerivationScenes.tsx` and registered:
`ScaleAnchorCard`, `DerivationLadder`, `AssumptionFan`, `SurvivingClaim`,
`ClaimAudit`. They are deliberately domain-neutral — every figure, label and row
is a prop — because this course turns headline numbers into derivations
repeatedly, and the next chapter should find these rather than rebuild them.
`./art scene-index` re-run so they are discoverable.

Library components reused: `ClaudeComposerAsk` (B00, B10),
`BrutalistHesitantWriter` (B01), `ClaudeVerdictArtifact` (B09),
`ClaudeTitleOutro` (B12).

## Carried forward from the ribosome reel
Two lessons from the previous build were applied at authoring time rather than
discovered again in QC:
- **`BrutalistHesitantWriter` triggers must be single tokens.** The component
  tokenises on whitespace, so a multi-word `triggerWords` entry silently never
  fires. B01 uses `measurement` → `division`, one token, and the swap is the
  reel's thesis rather than a synonym.
- **A typed beat must finish its performance early.** GATE V samples at 50% and
  85% of the beat and expects steady state. B01 is authored at `charMs: 14` with
  the stochastic pauses off, so the correction lands well before the halfway
  sample; the trigger pause itself is kept, because that hesitation is the
  pedagogy.

## Decision: `DerivationLadder` carries three beats
B03 (reading), B06 (compute), B08 (the method with specifics removed). Never two
consecutively. This is deliberate rather than economical: the reel's claim is
that one move generalises, and showing the identical ladder three times with
different contents is what makes it a method instead of an anecdote. Recorded
here against the ILLUSTRATE LAW "same scheme" smell.

## Honesty notes
- The spread figure (1,141 years) is computed here from the chapter's own three
  answers; the chapter states the looser "more than a thousand years". The screen
  shows all three answers the spread comes from, so the arithmetic is auditable.
- B05 exists to stop the reel overclaiming. Without it the falsifying beat reads
  as "the comparison is bogus", which is not what the source argues and not what
  the arithmetic supports.

## Free-path confirmation
Kokoro `am_onyx` throughout, local. No paid API, no Higgsfield beat, no key.
Cost $0.00. Review cut only — `./art run`, never `./art final`, never published.

## Scene QC before first compile
All five new components measured against GATE V's own `analyze_frame` on a
settled frame: 84.2% / 92.8% / 92.7% / 89.9% / 92.7% of SAFE, zero defects.
Two defects were found by eye and fixed before the sheet was authored:
- `AssumptionFan`: the fan paths were drawn with a 520px dash on curves up to
  ~620px, so the lower two branches stopped short of their answer boxes.
- `SurvivingClaim`: same class of bug — the outer converging arrows used a 300px
  dash on ~620px curves and never reached the surviving claim.
Both are draw-on length bugs that a fill metric cannot see; they were caught by
reading the frames.

## 2026-09-27 — author revisions (13 beats)
Changes requested after review, all rebuilt and re-QC'd:
- **Boundary gets its own screen.** "What this video does not establish" moved out of
  the verdict (where it was line 8 plus ~15s of narration) into a dedicated beat, B11,
  just before the outro. Rendered with a new `BoundaryCard` component — two columns,
  SHOWN vs NOT SHOWN — so the limit is shown as a contrast rather than read over a
  slide. The verdict dropped back to 7 lines. The reel is now 13 beats; the original
  brief said 12, and this is the author's deliberate change.
- **Outro renumbered B11 → B12** and given "Created by Ethan Gomes" via a new optional
  `credit` prop on `ClaudeTitleOutro` (empty by default, so channel reels are unchanged).
- **B02:** removed the "later models: undisclosed" header. It is now an optional
  `noteRight` prop on `ScaleAnchorCard`, empty by default.
- **B10:** removed the "not run" chip. The beat still shows no Claude output.

## 2026-09-27 — author revisions: new ending (back to 12 beats)
- **Title outro removed.** The video now ends on the Your-turn prompt (B11), with
  "Created by Ethan Gomes" centred at the bottom, via a new optional `credit` prop on
  `ClaudeComposerAsk` (empty by default).
- **Boundary moved ahead of the prompt:** verdict (B09) → "Where this stops" (B10) →
  Your turn (B11).
- The outro's "Thanks for watching, students" sign-off moved to the end of B11's
  narration so the video still closes rather than stopping on the prompt.
- House-style deviations, deliberate and author-chosen: OUTRO LAW (end on a
  title-restate card) and HANDOFF LAW (handoff is second-to-last) no longer hold.
  Neither is an assignment requirement.
- The `handle`/`credit` patches to `ClaudeTitleOutro` remain in the toolkit but are no
  longer used by this reel, so that file is no longer shipped in the zip.

## 2026-09-27 — title changed
The on-screen header (B00 and B11 segment title, B09 artifact card title, and
`metadata.title`) changed from "The Number Nobody Stated" to the concept's own
wording from the assignment list: "A training-scale slogan restated as a division
with a hidden assumption". Kept in the author's sentence case rather than the house
Title Case, so it matches the assignment list verbatim. Narration unchanged.

## 2026-09-27 — B08 closing line reworded
"= change line 3" read as the division's *answer* (same "=" and mono type as
"= 1,711 years") and referred to a line number that is not shown on screen. Now a
serif instruction set apart with an arrow: "→ Now try other values for the rate —
and see how far the answer moves". Done with three optional `DerivationLadder`
props (`resultPrefix`, `resultSerif`, `resultSize`) that default to the old look, so
B03 and B06 are unchanged. Narration unchanged.

## 2026-09-27 — author credit added to the narration
B11's narration now ends "…This video was created by Ethan Gomes from Info seven three
seven five. Thanks for watching, students." The course number is spelled out digit by
digit on purpose: checked with Kokoro's own phonemiser, "7375" is read as "seven
thousand three hundred seventy-five". "INFO" is read as the word "info", not spelled
out. `make_captions.py` shows the spoken phrase as "INFO 7375" in the captions.
B11 grows from 27.6s to 31.6s; B11's composition is 30s long, so its final ~1.6s is a
freeze-hold of the settled last frame.
