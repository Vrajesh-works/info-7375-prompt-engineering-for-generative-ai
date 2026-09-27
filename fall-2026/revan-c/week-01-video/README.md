# Week 1 Explainer Video — Tokens, Not Words.

**Student:** Revan Chonnad (`revan-c`) · INFO 7375, Fall 2026
**Concept:** The unit is a token, not a word — and why that breaks letter-counting prompts (Chapter 1, Part 1, "One question, asked over and over").
**Why this one:** I wanted to know how a model actually reads words, and the strawberry question shows it in one real example.
**Runtime:** 2:25 (144.75 s), 1920×1080
**Video file:** `final/tokens-not-words.mp4` is in the Canvas zip only. Video files are not committed to GitHub (course instruction); everything needed to rebuild it is here.

## What the video shows

Run through an open tokenizer (`o200k_base`), "How many r's are in strawberry?" becomes 8 token IDs, and " strawberry" is one of them: **101830**. There is no letter r in that number to count. The video then shows that the pieces change with a leading space or a capital letter, checks the course reading's `unbelievable` example, and shows that spelling the word out gives each r its own token (**428**, three times).

**What it does not establish:** these are OpenAI's open tokenizers, not Claude's (Claude's is not public), and the video explains why letter-counting is awkward, not that a given model will get it wrong.

Every number on screen comes from `evidence/tokens.json`. Nothing is constructed, and no Claude response is shown. The narrator is a synthetic Kokoro voice, disclosed in the video.

## Contents

| Path | What it is |
|---|---|
| `final/tokens-not-words.mp4` | The rendered video (**Canvas zip only**, not on GitHub) |
| `beat_sheet.json` | Reviewed narration and visual plan (11 beats) |
| `scenes.py` | Manim source for B02–B07 and the B10 outro |
| `evidence/tokenize_examples.py` | Script that produces every on-screen number |
| `evidence/tokens.json` | Its recorded output (tiktoken 0.14.0) |
| `evidence/claude-strawberry-screenshot.png` | My own Claude chat test (logged in FRICTIONAL, not shown in the video) |
| `BUILD-PROMPT.md` | Commands and prompt that rebuild the video |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated work log |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | Brutalist's required paperwork: every claim with its source |
| `_qc/REPORT.md`, `TYPECHECK.md`, `layout_audit.md` | Toolkit QC results for the final build |

## Rebuild

Full steps are in [BUILD-PROMPT.md](BUILD-PROMPT.md). In short, with `brutalist.art/` (commit `6a8380a`) next to this folder and a Python 3.12 venv:

```bash
python3 week-01-video/evidence/tokenize_examples.py
cd brutalist.art
python3 runtime/scripts/generate_audio_kokoro.py ../week-01-video
export TOKENS_REEL_DIR="$(cd ../week-01-video && pwd)"
./art run ../week-01-video
./art final ../week-01-video --height 1080 --out "$TOKENS_REEL_DIR/final"
```

To check only the numbers: `pip install tiktoken==0.14.0 && python3 evidence/tokenize_examples.py`, then compare with `evidence/tokens.json`.

## Why not `main.py`?

The assignment points to `lessons/01-randomness-and-first-prompts/code/main.py`. I ran it (it prints probabilities [0.090, 0.245, 0.665] and counts {0: 102, 1: 268, 2: 630}), but it covers softmax and sampling from Part 2. My concept is tokenization from Part 1, so I wrote `evidence/tokenize_examples.py` to produce real, reproducible token numbers instead.

## Credits

Starting material: the course reading (Chapter 1) and the Brutalist toolkit (github.com/nikbearbrown/brutalist.art). Claude Code wrote most of the code and drafts; details and licences are in [SOURCES.md](SOURCES.md).
