# Week 01 Video — Temperature Is Not a Fact Checker.

**Author:** Mayank B. · INFO 7375, Fall 2026
**Concept (Chapter 1):** Temperature controls how concentrated the choices are; it doesn't check facts.
**Why this one:** "Low temperature = more accurate" is a common belief, and the chapter's own
numbers can disprove it on screen — the ranking never moves, only the confidence does.
**Runtime:** 3 min 13 s (193.1 s) · 1920×1080

> **The video is submitted on Canvas only.** At the instructor's request, no video or audio files are
> published in this repo. Everything needed to rebuild the video is here (see Rebuild).

## What the video shows
| Beat | What you see |
|---|---|
| B00 | The question, and the real output of the chapter's code (no model call) |
| B01 | "creative" typed, then corrected to "concentrated" |
| B01A | How a chatbot picks the next word: every candidate gets a score; softmax turns scores into chances (illustrative, unnumbered) |
| B02 | Three sample scores → the softmax formula (top = your weight, bottom = everyone's total) → what e is (≈ 2.718) and why it's used |
| B02B | Softmax in three moves: weight = e^score → add the weights (30.19) → weight ÷ total = 9.0% / 24.5% / 66.5% |
| B03 | Temperature divides the scores first: T = 0.5 doubles them (2, 4, 6) → 86.7%; T = 2 halves them → 50.6%; ranking unchanged |
| B04 | Why: p_i/p_k = exp((z_i − z_k)/T) → ratios 54.60×, 7.39×, 2.72× |
| B05 | The chapter's real `probabilities()` function; the one line where T enters; T = 0 rejected |
| B06 | 1,000 real seed-7 draws at T = 0.5 (849) and T = 2 (469) |
| B07 | Constructed hypothetical: lowering T makes a wrong answer likelier (the correct one falls 9.0% → 1.6%); the formula, shown on screen, never sees the answer key |
| B08 | What this does **not** establish: how any Claude product sets or exposes temperature |
| BVDT–BOUT | The verdict: low temperature gives more consistent answers, not more correct ones; title outro |

## Rebuild
Everything is free and local (Kokoro, Remotion, ffmpeg; no API keys). Full steps: [BUILD-PROMPT.md](BUILD-PROMPT.md).

```bash
(cd code && python3 run_temperature.py)   # reproduces every number in the video
```

## Files
- `temperature-concentration.mp4` — the video: **on Canvas only**, not in this repo (built by the steps in BUILD-PROMPT.md)
- `beat_sheet.json` — narration + visual plan (show blocks) for all 13 beats
- `BUILD-PROMPT.md` — prompts and commands that rebuild it
- `SOURCES.md` — what I used, what I made, what Claude contributed, licences
- `FRICTIONAL.md` — dated log of what went wrong and what I did instead
- `CHANGELOG.md` — every change since generation started
- `FACTCHECK.md`, `CHECKS-REPORT.md`, `SHOTLIST.md`, `PROMPTS.md`, `_qc/` — gate paperwork and visual QC
- `code/` — the evidence scripts · `remotion-src/` — the seven custom scenes (TypeScript stored as `.txt`; see its README)
