# INFO7375 — Week 01 Explainer Video

**Student:** Saloni Satish Mathure
**Section:** SEC 01, Fall 2026
**Assignment:** Week 1 Explainer Video — Explain One Concept from Chapter 1

## Concept

A seed makes a run repeatable; it does not make the answer true.

## Why this concept

I picked it because it can be shown rather than asserted — two runs and a diff
prove it on screen — and because its boundary is the chapter's own argument:
the seed fixes the process, so it reproduces a wrong count as faithfully as a
right one.

## Runtime

2:46 (166.1 s), 9 beats, 3840x2160.

## Contents

- `video.mp4` — the rendered explainer (11 MB). **In the Canvas zip only.** The course repo's
  `.gitignore` excludes all `.mp4` and `.mp3` files, so the GitHub copy leaves out the video and
  the narration audio. Both rebuild exactly from the committed files (see below).
- `beat_sheet.json` — the reviewed narration and visual plan (the 9-beat sheet the build ran from; same as `reel/beat_sheet.json`)
- `run-A.txt`, `run-B.txt` (seed 7), `run-C.txt` (seed 10) — the raw runs
- `evidence/verify_claims.py` — re-checks every on-screen figure against a fresh run of the unmodified `main.py` (7/7 passing, 2026-09-27)
- `evidence/beat_sheet_draft_v1.json` — the earlier 6-beat draft, kept for the record
- `BUILD-PROMPT.md` — the commands and prompts that rebuild it
- `SOURCES.md` — what I made, what I used, what Claude contributed
- `FRICTIONAL.md` — dated effort log
- `reel/` — the Brutalist reel folder:
  - `beat_sheet.json` — the build copy, with Kokoro-measured durations
  - `scenes.py` — the five Manim scenes that carry the concept
  - `FACTCHECK.md` — every on-screen claim, with verdict and source
  - `SHOTLIST.md` — typed work order, per-beat durations and lanes
  - `PROMPTS.md` — authoring prompts
  - `TYPECHECK.md`, `layout_audit.md`, `_qc/REPORT.md` — the gate reports

## The concept in one paragraph

`sample()` in `main.py` takes `seed=7` as a default argument on line 19, and
line 22 builds its own generator with `random.Random(seed)` rather than seeding
Python's global random state. Two runs at seed 7 are byte-for-byte identical.
Seed 10 moves the counts and leaves the probabilities untouched, because
`probabilities()` never calls the generator. Token 2 has probability
0.6652409557748218, so 1000 draws predict 665.24 occurrences — it occurred 630
times, a shortfall of 35.24 reproduced exactly on every seeded run. The seed
reproduced the discrepancy; it did not detect it. **What this does not
establish: that the answer is correct.** Repeatability is a property of the
process; truth is a property of the claim.

## How to rebuild from this folder

```bash
# 1. Course code and the three runs
git clone https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai
cd info-7375-prompt-engineering-for-generative-ai
python3 lessons/01-randomness-and-first-prompts/code/main.py | tee run-A.txt
python3 lessons/01-randomness-and-first-prompts/code/main.py | tee run-B.txt
diff run-A.txt run-B.txt          # empty
# edit line 19: seed=7 -> seed=10
python3 lessons/01-randomness-and-first-prompts/code/main.py | tee run-C.txt
diff run-A.txt run-C.txt          # counts differ
# revert to seed=7

# 2. Verify every on-screen figure
python3 evidence/verify_claims.py          # 7/7

# 3. Toolkit (Python 3.12 venv required — see FRICTIONAL)
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
git checkout cd4bf20                        # the toolkit commit this was built with
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./setup --install                           # needs Node >= 20

# 4. Narration, then compile
python3 runtime/scripts/generate_audio_kokoro.py <path>/reel
ART_STRICT=0 ./art run <path>/reel
```

Output: `reel/seeded-not-settled-slate.mp4`, copied to `video.mp4`.

**Rebuild tested, 2026-09-27.** I exported only the files committed to GitHub
(no mp3, no mp4, no render caches) into an empty folder and ran step 4 on it
with Brutalist `cd4bf20`, Python 3.12 venv, and Node 20. Kokoro regenerated
all nine narration files byte-identical to the originals, and the compiled
video was **byte-identical** to `video.mp4` (`cmp` reported no difference,
11,615,859 bytes, 166.1 s). What that shows: the committed files fully
determine the video on this machine and toolchain. What it does not show:
that a different OS, Manim, ffmpeg, or Kokoro version would give the same
bytes. It would likely give the same video, but I have not tested that.

## Numbers and output in the video

Every figure on screen is from `run-A.txt`, `run-B.txt`, or `run-C.txt`,
produced 2026-09-27 from the unmodified `main.py`, and re-checked by
`evidence/verify_claims.py`. Nothing is invented. The generator diagram in
beat B01 is constructed and carries a CONSTRUCTED ILLUSTRATION label on
screen throughout. The B00 opening card is the toolkit's Claude-style
composer with text I wrote. It is not a real Claude response, and it has no
on-screen label saying so (see SOURCES.md). No real Claude transcript appears
in the video.

## License

MIT
