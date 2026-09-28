# SOURCES.md — seed-repeatable-not-correct.mp4

## Course material used (not created by me)

- **Concept and framing:** "A seed makes a run repeatable; it does not make
  the answer true" — Chapter 1, Part 2 ("Randomness and first prompts"),
  course textbook.
- **Numbers used as evidence:** the sampling counts for scores `[1, 2, 3]` at
  temperature 1.0, seed 7, count 1000 (`{0: 102, 1: 268, 2: 630}`) are the
  chapter's own reference figures. They were reproduced by running
  `evidence/seeded_sampler.py` (not copied from a printed table), and on
  2026-09-28 checked against the course reference
  `lessons/01-randomness-and-first-prompts/code/main.py`, which prints the same
  counts and probabilities (`evidence/course_main_py_output.txt`).

## What I made (with Claude Code, as noted)

- **`evidence/seeded_sampler.py`** — softmax + weighted-sampling script
  written by Claude Code at my request, from the chapter's description and my
  prompt (it was not copied from the course's `main.py`, though it computes the
  same thing and prints the same numbers), used to independently regenerate
  the counts above. Run twice to confirm byte-identical output, plus 100 additional
  confirmation runs and one run at a different seed (8) to show the counts do
  change under a different seed.
- **The hypothetical "outcome 0 is correct" answer key** — this is a labeled,
  on-screen, hand-drawn-style construction I designed for the video (styled
  as a sticky note) specifically to demonstrate that the sampler has no
  access to any ground truth. It is explicitly marked on screen as
  constructed, not a real fact-check, and is called out again on the closing
  card.
- **The mock chat-bubble example (Sydney/Canberra)** — a constructed
  illustration of a confident AI answer, not a real transcript from any
  model. Not labeled as a real Claude output because it never claims to be
  one; it's a generic illustrative mockup.
- **Beat sheet, narration script, on-screen text, and visual layout** —
  drafted collaboratively with Claude Code (see `BUILD-PROMPT.md`), reviewed
  and approved by me before rendering.

## What Claude (Claude Code, Opus 5.5) contributed

- Drafted `beat_sheet.json` (narration and visual plan) from my brief; I
  reviewed it and approved it, choosing the silent holds and keeping the
  Sydney/Canberra example.
- Wrote `evidence/seeded_sampler.py` and `evidence/capture.sh`, ran them, and
  kept the recorded output.
- Wrote the Manim scene code (`scenes.py`) implementing the approved beat sheet.
- Wrote `pad_holds.py` (silent holds) and `cues.py` (reveal timing), and ran the
  Kokoro narration step.
- Drafted `FRICTIONAL.md`, `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` and
  `COMMAND-LOG.md` from the session's command logs.
- Diagnosed and fixed toolkit bugs encountered during the build (regex scene
  discovery, ENV-parsing bug, oversized stamp/badge animation bug, cue-timing
  bugs) — full list in `FRICTIONAL.md`.
- Ran the toolkit's own quality gates (GATE T for text legibility, GATE V for
  safe-area/contrast/fill) and iterated on layout until both passed.
- Did **not** independently decide the video's concept, the constructed
  answer-key framing, or approve its own work for submission — those
  decisions were mine at each review point logged in `FRICTIONAL.md` /
  `BUILD-PROMPT.md`.

## Third-party assets and licenses

| Asset | Source | License | Use |
|---|---|---|---|
| Kokoro-82M (via kokoro-onnx) | github.com/hexgrad/kokoro (open weights) | Apache 2.0 | Local, free text-to-speech narration. Voice is a synthetic stock voice bundled with the model, not a cloned or licensed real person's voice. |
| Manim | github.com/ManimCommunity/manim | MIT | Scene/animation rendering (all six beats). |
| ffmpeg | ffmpeg.org | LGPL/GPL | Audio padding, pause detection for reveal timing, and the toolkit's compile step. |
| EB Garamond | Google Fonts (via the toolkit) | SIL Open Font License | Main typeface. |
| Avenir Next, Menlo | Pre-installed macOS fonts | Apple system fonts, not redistributed | Stamp lettering and terminal text. |
| Marker Felt (system font) | Pre-installed macOS font | Apple system font, not redistributed | Used for the sticky-note visual so the digit "0" is distinguishable from the letter "O" (see `FRICTIONAL.md`, 2026-09-27 16:31). |
| Brutalist toolkit itself | github.com/nikbearbrown/brutalist.art, revision `6a8380a` | Public course toolkit (per repo license) | Compilation/gate/render pipeline. Not modified — all workarounds were applied outside the toolkit's own files. (Its Remotion stage ran but had no Remotion beats to render in this video.) |

No paid generation services, no stock footage/image libraries, no music
tracks, and no third-party voice cloning were used anywhere in this video.
