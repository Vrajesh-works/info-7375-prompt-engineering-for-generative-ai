# Low Temperature Is Not Argmax

**Name:** Om Raut
**Course:** INFO7375 — Week 1 Explainer Video
**Concept:** Chapter 1 (Randomness and First Prompts) — off the instructor's example
list, built from a passage in the chapter's own text rather than one of the
listed concepts.
**Runtime:** 3:47 (227.2s)

> **The video is submitted on Canvas, not in this GitHub folder** — the repo's
> `.gitignore` excludes `.mp4` files, so the video travels only in the Canvas zip.

## Why this concept

The chapter states, almost in passing, that a low but positive temperature is
not the same operation as argmax — and that this is exactly the assumption a
lot of practitioners carry around without ever checking it. That combination
(a real, common misconception; a claim the chapter's own reference code can
directly test; and a natural "constructed contrast" to build) made it a better
fit for this assignment's standard of evidence than a concept that just needed
restating.

## What the video actually shows

1. The chapter's reference implementation (`probabilities()` / `sample()`,
   copied exactly) refuses `temperature=0` outright — it raises a
   `ValueError` rather than treating zero as a request for deterministic
   output.
2. At `temperature=0.5`, real captured output shows 87% concentration on the
   top-scoring outcome, but 151 of 1000 draws still went elsewhere —
   concentrated is not certain.
3. A function I built myself, `argmax_select()` — clearly labeled on screen
   as constructed, not part of the chapter — shows what a genuinely
   deterministic operation looks like: zero variance, by construction, every
   time.
4. **The corrected claim, after fact-checking my own first draft:** in exact
   mathematics, every outcome keeps a positive probability at any T > 0, so
   sampling never *has* to become one-hot. In practice, though, a run can land
   on the same outcome every time by chance, and in real floating-point code,
   low enough temperatures make the other probabilities literally underflow
   to `0.0` — so the computed numbers *can* become identical to argmax's, even
   though the operation that produced them is different. (See
   `FACTCHECK.md` in the GitHub repo for the full correction — my first draft of this video
   overclaimed "temperature never produces zero variance," which is false.)
5. Named boundary: none of this says how a real product's own
   temperature-zero or greedy-decoding setting is implemented — that's a
   separate, documented claim about a separate system.

## How to rebuild this video from scratch

Full command-by-command instructions are in `BUILD-PROMPT.md`. Short version:

```bash
# 1. Get the chapter's reference implementation
git clone https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai
cd info-7375-prompt-engineering-for-generative-ai/lessons/01-randomness-and-first-prompts/code
python3 main.py

# 2. Get Brutalist and set it up (Python 3.10+, ffmpeg, Node ≥20 required)
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
./setup --install

# 3. Place this build's files (from the GitHub repo) into the toolkit's reel folder
mkdir -p youtube/low-temperature-is-not-argmax
# copy in from the GitHub repo: beat_sheet.json, scenes.py, demo.py

# 4. Generate narration audio (measured durations become the timing clock)
python3 runtime/scripts/generate_audio_kokoro.py youtube/low-temperature-is-not-argmax

# 5. Compile the review cut
ART_FACTS=0 ./art run youtube/low-temperature-is-not-argmax
# (ART_FACTS=0 is a previz-only shortcut; a real final requires
#  FACTCHECK.md, SHOTLIST.md, PROMPTS.md — all three are part of the full
#  build and included in the GitHub repo (see below), not in this Canvas zip,
#  which contains only the assignment's named 6 deliverables. They were
#  required for the actual ./art final below.)

# 6. Produce the clean master
./art final youtube/low-temperature-is-not-argmax
```

The rendered master is `low-temperature-is-not-argmax.mp4` (3840×2160, 24fps,
H.264/AAC, SHA-256 recorded in the build's own `build-state.json`).

## Files in this submission

The full build — including `scenes.py`, `demo.py`, `FACTCHECK.md`,
`SHOTLIST.md`, and `PROMPTS.md` — is posted to GitHub; see the link and
commit hash in the Canvas submission. (`scenes.py` contains the Manim scenes
for B04 and B06 only; B07 is a separate Remotion `TypesetMath` card, not part
of `scenes.py`.)

- `low-temperature-is-not-argmax.mp4` — the rendered video
- `README.md` — this file
- `beat_sheet.json` — the full reviewed narration and visual plan
- `BUILD-PROMPT.md` — the exact sequence of commands to rebuild it, including the fixes required to get a clean build — see `FRICTIONAL.md` for the full story behind each one
- `SOURCES.md` — what was used, what was made, what Claude contributed
- `FRICTIONAL.md` — dated log of everything that broke and what fixed it
