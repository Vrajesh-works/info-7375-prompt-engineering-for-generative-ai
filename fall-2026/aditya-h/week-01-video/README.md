# INFO7375 — Week 01 Video

**Name:** Aditya Hasija

**Concept:** A seed makes a sampling run repeatable — it does not make the sampled answer correct. (Chapter 1, Part 2: "A seed makes a run repeatable; it does not make the answer true.")

**Why this concept, in one sentence:** Reproducibility is easy to mistake for trustworthiness, and this is the smallest possible demonstration that they're answers to two completely different questions.

**Runtime:** 3:02 (181.7s), 3840×2160, 6 beats (intro + 5)

> **The video file is submitted on Canvas** (`Hasija_Aditya_INFO7375_Week01_Video.zip`), not in this GitHub folder: the repository's `.gitignore` excludes `.mp4` files. Everything needed to rebuild it is here.

**Numbers are real:** every count on screen comes from recorded runs of `evidence/seeded_sampler.py`, and they match what the course reference `lessons/01-randomness-and-first-prompts/code/main.py` prints (`{0: 102, 1: 268, 2: 630}`; see `evidence/course_main_py_output.txt`).

**Built with:** the public Brutalist toolkit at revision `6a8380ae169cca81e0633664a65c958f5c12ab4b`, using Claude Code (Claude Opus 5.5). What Claude contributed is itemized in `SOURCES.md`.

## What's in this folder

| File | What it is |
|---|---|
| `seed-repeatable-not-correct.mp4` | The rendered video: **in the Canvas zip only, not in this GitHub folder** (the repository's `.gitignore` excludes `.mp4` files) |
| `beat_sheet.json` | The reviewed narration + visual plan (final version, post-intro) |
| `BUILD-PROMPT.md` | The exact prompts/commands used to build and rebuild it |
| `SOURCES.md` | What was used, made, Claude's contribution, and third-party licenses |
| `FRICTIONAL.md` | Dated log of every point the build didn't go straight through |
| `scenes.py` | Manim source for all six beats (reads the evidence files at render time) |
| `pad_holds.py`, `cues.py` | Audio silent holds and reveal timing (run after narration is generated) |
| `evidence/` | `seeded_sampler.py`, `capture.sh`, the recorded runs (`run1.txt`, `run2.txt`, `run100.txt`), `factcheck_probe.txt`, `ENV.txt`, and the course `main.py` output |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | Claim-by-claim fact check and the toolkit's required build paperwork (`./art run` refuses to render without them) |
| `COMMAND-LOG.md` | Command-by-command build log, including failed attempts |
| `qc/` | The toolkit's final gate reports (text legibility, GATE T; frame QC, GATE V) |

## Verify the numbers (no toolkit needed)

```
python3 evidence/seeded_sampler.py        # prints counts = {0: 102, 1: 268, 2: 630}
bash evidence/capture.sh                  # re-runs it twice as separate processes and diffs them
```

## How to rebuild this video from this folder

1. Clone the toolkit at the revision used, and set it up:
   ```
   git clone https://github.com/nikbearbrown/brutalist.art
   cd brutalist.art && git checkout 6a8380ae169cca81e0633664a65c958f5c12ab4b
   ./setup --install
   ```
   (At this revision `./setup` stops early on its own ElevenLabs guard; see `FRICTIONAL.md`. The `.venv` it creates is what the steps below use.)
2. Copy this whole folder to a reel folder outside the toolkit, e.g. `~/INFO7375/youtube/seed-repeatable-not-correct/`.
3. From inside the toolkit directory, put the local venv on PATH (not on PATH by default):
   ```
   export PATH="$PWD/.venv/bin:$PATH"
   R=~/INFO7375/youtube/seed-repeatable-not-correct
   ```
4. Generate narration audio (free, local Kokoro), then apply the silent holds and compute reveal timing:
   ```
   .venv/bin/python runtime/scripts/generate_audio_kokoro.py "$R"
   python3 "$R/pad_holds.py"
   python3 "$R/cues.py"
   ```
5. Render and export the clean master (`ART_QC=0` skips the toolkit's Manim-stub pre-render gates, which can't evaluate these scenes; the final gates still run; see `FRICTIONAL.md`):
   ```
   ART_QC=0 ./art run "$R" > "$R/_run1.log" 2>&1
   ./art final "$R" --out "$R" > "$R/_final1.log" 2>&1
   ```
6. Confirm the output passes the toolkit's own gates before treating it as final:
   ```
   grep -E "GATE T" "$R/_final1.log"; head -5 "$R/_qc/REPORT.md"
   ```
   Expected: `GATE T: PASS`, and `BLOCKER: 0 · MAJOR: 0` in the GATE V report.

Full command-by-command history (including the failed attempts and fixes) is in `FRICTIONAL.md` and `COMMAND-LOG.md`.
