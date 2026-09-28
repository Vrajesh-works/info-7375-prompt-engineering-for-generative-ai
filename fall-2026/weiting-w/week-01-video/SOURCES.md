# SOURCES — One Word, Same Answer

## What I made

The design and the judgment calls in this project are mine:

- **Experiment design.** I recognized that the chapter's original comparison (a one-sentence deck prompt vs. a one-word capital prompt) changes two variables at once — the question *and* the output format — so a difference in the answers cannot be attributed to either alone. I added a control: the same capital question with **no** format rule, so each comparison changes only one thing.
- **Two-run structure.** I decided to run the whole set twice — once in a normal account (Run 1) and once in incognito with memory off (Run 2), personal preferences on in both — to separate the effect of the prompt from the effect of the account/environment.
- **Running the evidence.** I sent all 24 prompts myself, in brand-new chats, kept the first reply in each with no regeneration, captured the screenshots (A1–D4 per run), and transcribed them verbatim into `evidence/run*/responses.json`.
- **Finding and interpreting the result.** I noticed from the real data that Run 1's free answers were already short (~6 words, 2 distinct) while Run 2's were ~30 words and varied, and I concluded that something outside the prompt was already narrowing the answers in the normal account. That became the video's main point.
- **The boundary.** I decided what the video does **not** establish — that the cause of the short Run-1 replies is not isolated (incognito may change more than memory) — and made that the B07 "NOT ESTABLISHED" column.
- **Direction during the build.** The build code (below) was written by Claude, but the decisions about what to change and how — which quality-gate failures to fix, how to fix them, and the call to ship with the residual serif kerning rather than restructure everything under the deadline — were mine. I directed those edits.

## What Claude contributed

I used Claude (claude.ai) throughout, and I remain responsible for the whole submission.

- **As the subject under test:** the 24 replies shown in the video are real Claude outputs (claude.ai, Opus 5.5 Medium, 2026-09-27). They are evidence, not narration.
- **As a build assistant, working to my direction:** Claude wrote the code for `beat_sheet.json`, `scenes.py`, and `analyze_responses.py`, helped word the narration, and helped read the toolkit's error output to locate gate failures — but the design it implemented and the edit decisions it carried out were mine. Every number this code produces is recomputed from my evidence by `analyze_responses.py`, and `scenes.py` refuses to render if a figure drifts from `evidence/analysis.json`, so the code cannot silently change a result.

## Tools and libraries (all free / local)

- **Brutalist toolkit** — Nik Bear Brown, https://github.com/nikbearbrown/brutalist.art (course toolkit).
- **Kokoro** — local text-to-speech; narration voice `af_bella`. Synthetic voice, disclosed on the end card and in the narration.
- **Manim Community v0.18.1** — the graphic beats (B01–B07, B09).
- **Remotion** — the composer/bookend beats (B00, B08) and the title outro.
- **Python standard library** — `analyze_responses.py` (json, re, math); no third-party data packages.
- **EB Garamond** (serif) and **Helvetica Neue / Inter** (sans) — fonts bundled with / resolved by the toolkit.

## Third-party assets

None. No generated images, no stock media, no music bed. Every beat is rendered locally by Manim or Remotion. No paid generation, no API keys, no media accounts.

## External facts cited (checked 2026-09-27)

- Canberra is the capital of Australia — https://en.wikipedia.org/wiki/Canberra
- Incognito does not use Claude's existing memory — https://support.claude.com/en/articles/12260368
- log2(52!) = 225.58 — computed in `analyze_responses.py` as `math.lgamma(53)/math.log(2)`.
