# SOURCES — tokens-not-words

## What I used

| Source | Used for |
|---|---|
| Course reading, Chapter 1 "Randomness and first prompts" (`chapters/01-randomness-and-first-prompts.md` in nikbearbrown/info-7375-prompt-engineering-for-generative-ai), Part 1, "One question, asked over and over" | The concept, and the quoted `unbelievable` example (B05) |
| `lessons/01-randomness-and-first-prompts/code/main.py` | Run once (prints probabilities [0.090, 0.245, 0.665] and counts {0: 102, 1: 268, 2: 630}). **Not used in the video**: it covers sampling (Part 2), and my concept is tokenization (Part 1). |
| tiktoken 0.14.0, encodings `o200k_base` and `cl100k_base` (OpenAI, MIT licence) | Every token split and ID on screen. These are **open OpenAI tokenizers, not Claude's**; the video says so in B07 and B08. |
| Course prerequisites `brutalist-video.md`, `brutalist-video-sources.md`, `ai-policy.md`, `relative-quartile.md`, `github-submission.md`, and the `frictional/` guide | Workflow and disclosure rules (synthetic narration, reconstructed UI, 1080p final) |

## What I made

`beat_sheet.json` (script and scene plan), `scenes.py`, `evidence/tokenize_examples.py` and its output `evidence/tokens.json`, `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `FRICTIONAL.md`, `README.md`, `BUILD-PROMPT.md`, this file. I also ran the video's prompts in Claude myself (`evidence/claude-strawberry-screenshot.png`, discussed in FRICTIONAL Entry 3).

**Constructed illustrations:** none. Every number on screen is real tokenizer output. The B03 letter tiles simply spell the word, and the counts (10 letters, 3 r's) were counted by hand.

**Claude responses shown in the video:** none. B00 shows a build request with the **tokenizer's** output, labelled on screen "tokenizer output, run 2026-09-24 — not a Claude answer". B09 shows a suggested prompt with no response.

**Reconstructed UI:** B00 and B09 use Brutalist's recreation of the Claude app (`ClaudeComposerAsk`). Its model chip reads "Reconstructed UI"; it is not a screenshot of a real session.

**Synthetic narration:** the voice is Kokoro `am_onyx`, introduced in B00 as "Liam, a synthetic voice, narrating for Revan Chonnad". It is not my voice, not Professor Bear's, and not an endorsement.

## What Claude contributed

Claude (Claude Code, model Opus 5.5), 2026-09-23 → 2026-09-27:
- found the Chapter 1 tokens passage in the course repo and suggested the concept shortlist (I rejected its first recommendation, a Part 2 concept)
- wrote `tokenize_examples.py` and ran it
- drafted all narration and `beat_sheet.json`
- wrote `scenes.py`, and diagnosed and fixed each Brutalist gate failure (FRICTIONAL Entry 2)
- audited the cut against the assignment and prerequisite guides and found four problems I approved fixing (FRICTIONAL Entry 3)
- drafted FACTCHECK, SHOTLIST, PROMPTS, README, BUILD-PROMPT and this file, and turned my answers into FRICTIONAL entries

What I did: chose the concept, reviewed the cuts and requested changes (greeting, handle and name, narrator line), ran the Claude and ChatGPT chat tests, answered the FRICTIONAL prompts, and approved the audit fixes.

## Third-party tools and assets (all free, run locally)

| Asset | Licence / terms |
|---|---|
| Brutalist toolkit (github.com/nikbearbrown/brutalist.art, commit `6a8380a`): pipeline and Remotion scenes `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `ClaudeVerdictArtifact` | Course toolkit; the repo has no LICENSE file at this commit |
| Kokoro-82M voice model (`am_onyx`) via kokoro-onnx 0.6.1 | Model: Apache-2.0 (hexgrad/Kokoro-82M); kokoro-onnx: MIT |
| Manim Community 0.18.1 | MIT |
| Remotion 4.0.486 | Remotion Free License (individuals may use it free of charge) |
| EB Garamond font (bundled in brutalist.art `runtime/fonts/EB_Garamond`) | SIL Open Font License 1.1 (`OFL.txt` alongside) |
| Menlo (macOS system font) | Apple system font, used locally for rendering only |
| FFmpeg 9.0.2 | LGPL/GPL |
| faster-whisper 1.2.1 (`base.en`) | MIT; used only to check narration by speech-to-text, not in the video |

No stock footage, music, images or paid generation was used. The B10 outro is my own Manim card; Brutalist's `ClaudeTitleOutro` and its mascot were not used.
