# Subtract the Max — INFO 7375 Week 1 video

**Student:** Siddi Kommuri · **Course:** INFO 7375, Fall 2026 · **Assignment:** Week 1 concept video

**Concept (Chapter 1, Part 2):** why subtracting the maximum score before `exp` changes the intermediate
weights but not the probability distribution. It also covers what that does *not* protect against.

**Why this concept:** it's the smallest idea in the chapter that you can watch happen: the same three
scores go down two routes, the weights differ, the probabilities don't, and `math.exp(1000)` really
crashes.

**Runtime:** 2:49 (`Kommuri_Siddi_INFO7375_Week01_Video.mp4`, 1920×1080, 30 fps, synthetic Kokoro narration)

## Contents

| Path | What it is |
|---|---|
| `Kommuri_Siddi_INFO7375_Week01_Video.mp4` | The rendered video: **in the Canvas zip, not in Git** (the course repo's `.gitignore` keeps generated video out of Git). See *Video file* below |
| `beat_sheet.json` | Reviewed narration and visual plan (one beat per moment; measured audio durations) |
| `code/main.py`, `code/tests/` | The course's `main.py` and tests, copied unchanged (commit `149c8e7`) |
| `code/evidence.py` → `code/evidence.json` | Runs `main.py` next to a direct softmax; **every number on screen comes from here** |
| `scenes.py` | Manim source for beats B02–B06 and the outro; reads `evidence.json` |
| `render_manim.sh` | Renders the Manim beats into the `manim/<BEAT>.mp4` slots |
| `build/` | Windows environment (`env.sh`), relaxed requirements, and the one-line toolkit patch |
| `BUILD-PROMPT.md` | Prompts and commands that rebuild the video |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FACTCHECK.md` | Every narrated claim → verdict → evidence key |
| `SHOTLIST.md`, `PROMPTS.md` | Brutalist paperwork (required by its GATE F) |
| `FRICTIONAL.md` | Dated log: attempts, what broke, fixes, review record |

## Video file

The MP4 is submitted on Canvas. To confirm the Canvas copy matches this GitHub version:

| File | Bytes | SHA-256 |
|---|---:|---|
| `Kommuri_Siddi_INFO7375_Week01_Video.mp4` | 9,513,520 | `9da061f3b680e7a2275ad1315f5bfed2106900937dddf8913088662a7b0a491c` |

```bash
sha256sum Kommuri_Siddi_INFO7375_Week01_Video.mp4
```

## Check the numbers (no video tools needed)

```bash
python code/evidence.py                      # prints and rewrites code/evidence.json
python -m unittest discover -s code/tests    # the lesson's own 6 tests
```

## Rebuild the video

Requires a sibling checkout of [brutalist.art](https://github.com/nikbearbrown/brutalist.art)
(`cd4bf20`) with its setup done (set `BRUTALIST_HOME=/path/to/brutalist.art` if it is not a sibling of this folder, e.g. when this folder sits at `fall-2026/siddi-k/week-01-video/` in the course repo), plus ffmpeg, Node ≥ 20 and Python 3.13. Full steps, including the Windows
fixes, are in `BUILD-PROMPT.md`. In short, from the folder that contains both `brutalist.art/` and this folder:

```bash
source brutalist.art/.shim/env.sh                       # venv + ffmpeg on PATH (see build/env.sh)
cd brutalist.art
python3 runtime/scripts/generate_audio_kokoro.py ../week-01-video   # narration = the clock
python3 runtime/scripts/remotion_scenes.py ../week-01-video         # bookends B00 B01 BVDT BHTF
(cd ../week-01-video && ./render_manim.sh)                           # body B02–B06, BOUT
python3 runtime/scripts/compile.py ../week-01-video --height 1080 --fps 30 --out ../week-01-video/final
# (./art final = GATE T + this command; see FRICTIONAL.md #11 for why GATE T's kerning check was not enforced)
```

## Honesty notes

- No Claude response appears anywhere in the video. The composer frames are labelled "Mock composer ·
  not a real session".
- Constructed inputs are labelled on screen. `[1000, 1000]` is labelled as the lesson's test input.
- The narrator is a synthetic voice (Kokoro `am_onyx`), and B00 says so.
- **What the explanation does not establish (B06):** it isn't protection against every extreme
  input. `[0, -1000]` returns exactly `[1.0, 0.0]` by either route, and the two routes agree in algebra
  but not bit for bit.
