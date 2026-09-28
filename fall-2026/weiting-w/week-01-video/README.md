# One Word, Same Answer

**Author:** Weiting Wang
**Course:** INFO 7375 — Prompt Engineering for Generative AI (Fall 2026)
**Assignment:** Week 1 — Explain one concept from Chapter 1
**Concept (Chapter 1, Part 2):** *Constraining the output format narrows the spread without checking anything.*
**Runtime:** 3:18 (198.5 s) — within the 2–4 minute target
**Built with:** the Brutalist toolkit (Kokoro `af_bella` narration, Manim + Remotion), fully local/free.

## Why this concept

Many people assume that telling a model to "answer with one word only" means the model is confirming whether the answer is right. Two real experiments show it is not: the one-word rule only narrows the reply until there is almost no other phrasing left to choose, and it checks nothing. The narrowing also does not have to come from a format rule in the prompt — the account and environment (a normal account vs. an incognito chat) quietly narrow the answers on their own.

## What is in this folder

The files sit flat in this folder. This is the submission package (for viewing and download); it is not the toolkit's working layout — see "How to rebuild" for that distinction.

- `Wang_Weiting_INFO7375_Week01_Video.mp4` — the rendered video (the deliverable).
- `beat_sheet.json` — the reviewed narration + visual plan (10 beats, B00–B09).
- `scenes.py` — the Manim scenes for the graphic beats.
- `analyze_responses.py` — recomputes every on-screen number from the evidence (standard library only).
- `evidence/` — the real Claude replies: `run1-normal/` and `run2-incognito/`, each with `responses.json` (verbatim transcriptions) and `screenshots/` (A1–D4). `analysis.json` holds the computed figures.
- `FACTCHECK.md` — every spoken/shown claim, its verdict, and its source.
- `SHOTLIST.md`, `PROMPTS.md` — the typed work order and the exact prompts sent to Claude.
- `SOURCES.md`, `FRICTIONAL.md`, `BUILD-PROMPT.md` — sources/credits, the friction log, and the build recipe.

## The experiment (what the video shows)

The chapter compares a one-sentence "shuffled deck" prompt with a one-word "capital of Australia" prompt. That comparison changes two things at once (the question *and* the format), so we added a control: the same capital question with **no** format rule. Each prompt was sent in 4 brand-new chats, first reply kept, no regeneration — once in a normal account (**Run 1**) and once in incognito (**Run 2**, memory off; personal preferences on in both). All 24 replies are stored verbatim with screenshots (claude.ai, Opus 5.5 Medium, 2026-09-27).

**Finding.** With the one-word rule, all four replies were "Canberra" in both runs. Without it, Run 2 produced four different ~30-word answers — but Run 1's free answers were already short (~6 words, 2 distinct). Something outside the prompt was already narrowing answers in the normal account. The video names this, and B07 states plainly what the experiment does **not** establish (the cause of the short Run-1 replies is not isolated; incognito may change more than memory).

## How to rebuild the video from this folder

This rebuilds with the Brutalist toolkit's free local pipeline. It assumes a reader who already has the toolkit set up; the exact commands are in `BUILD-PROMPT.md`. Four things to know before running:

1. **Environment.** You need a working Brutalist checkout with Manim Community 0.18.x, Remotion (Node), Kokoro TTS, and ffmpeg installed, and `scenes.py` must be able to resolve **EB Garamond** on the machine (its font-registration block looks for the toolkit's bundled font files). Without this environment the first render step will not run — this is an inherent prerequisite of reproducing the film, not a defect in these files.

2. **Two different layouts — do not confuse them.** This submission folder is flat, for viewing. The toolkit expects a *reel* folder. To rebuild, place `scenes.py`, `beat_sheet.json`, `evidence/`, `FACTCHECK.md`, `SHOTLIST.md`, and `PROMPTS.md` inside a Brutalist checkout as a reel, e.g. `youtube/weiting/one-word-same-answer/`. That path is the rebuild location; it is separate from how this package is arranged.

3. **Evidence must be in place.** Beat B03 draws the 24 screenshots `A1`–`D4` from `evidence/run1-normal/screenshots/` and `evidence/run2-incognito/screenshots/`. Confirm all 24 are present before rendering, or B03 will fall back to empty cells.

4. **Audio drives the timing.** Beat durations come from the Kokoro `af_bella` narration. The per-beat `mp3/` audio is included in this package; reusing it reproduces the exact 198.5 s runtime without regenerating.

Then, from the toolkit root:

```bash
ART_STRICT=0 ./art run youtube/weiting/one-word-same-answer   # render the ten beats
./art final youtube/weiting/one-word-same-answer              # write the clean master to renders/
```

The verified master is 198.5 s with sha256 `2aff490b2d4f0b1550eb65212813f4af454427324f652687f73e6d7e8d58b0f9`.
