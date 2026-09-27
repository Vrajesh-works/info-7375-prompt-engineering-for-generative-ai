# SOURCES — INFO 7375, Week 01 video

Akshit Verma · *What pretraining actually targets (the token that followed, not the truth)*

> **Drafting note (Claude Code, 2026-09-27).** Claude drafted this file at Akshit's request.
> Contributions in §6 are attributed to whoever actually did them. An earlier draft credited Akshit with checks Claude performed; it was
> corrected on 2026-09-27.

---

## 1. The course material this explains

**Chapter 1, Part 1 — "Randomness and First Prompts"**
`github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai` →
`chapters/01-randomness-and-first-prompts.md`, Part 1. Retrieved 2026-09-27.

Part 1 sections: *The unfinished script · One question, asked over and over · The transcript
is the whole trick · Where the numbers come from · Scale, in units you can check · Inside one
prediction step · Stochastic parrots · What Part 1 licenses you to say*.

### Chapter sentences quoted or closely paraphrased in the narration

| Beat | Chapter text |
|---|---|
| B02 | "Take a passage of text. Hide the next token. Ask the model for its distribution. Compare that distribution with the token that actually followed." |
| B02 | "backpropagation to nudge every parameter slightly, so that next time this context arises the true token gets a little more probability and everything else a little less" |
| B02 | "Nothing in this loop is told what is true. The target is what the corpus did next." |
| B08 | "Neither stage receives an answer key." |
| B08 | "Approval and correctness overlap heavily — raters generally prefer accurate answers — but they are different targets, and where they diverge the training signal follows approval." |
| B08 | "A confident, well-organized, wrong answer is exactly the kind of output that can be preferred by a rater who does not know the answer either." |
| B09 | "Nobody — including the people who built it — can read off why a particular prediction was made." |
| B09 | "The mechanism ranks continuations, and ranking a continuation highly is not evidence that it is true." |

Nothing in the video is attributed to the chapter that is not in it.

### Why `main.py` is not the source of this video's numbers

The assignment says Chapter 1's numbers are reproducible via
`lessons/01-randomness-and-first-prompts/code/main.py`. It was fetched and run on 2026-09-27:

```
{"probabilities": [0.09003057317038046, 0.24472847105479764, 0.6652409557748218],
 "counts": {"1": 268, "2": 630, "0": 102}}
```

That is the softmax-and-sampling demo (logits `[1, 2, 3]`, 1000 draws, seed 7) — **Part 2**
material. It computes nothing about the pretraining objective, so it cannot supply a worked
example for this Part 1 concept. The video's numbers instead come from a purpose-built,
deterministic script in this folder (§2). Its softmax uses the same max-subtraction as
`main.py`'s `probabilities()`.

---

## 2. Numbers on screen — where each one came from

Every figure is **computed** by `code/pretraining_target.py` (numpy only, no network, no key).
Its stdout is saved verbatim in `code/OUTPUT.txt`; all 601 steps are in `code/trajectory.json`.
Weights start at zero with no sampling and no seed, so every run prints identical numbers.

```bash
python3 code/pretraining_target.py
```

| Shown in | Value | Source |
|---|---|---|
| B04 | 0.3333 / 0.3333 / 0.3333, loss 1.0986 (= ln 3) | `OUTPUT.txt`, step 0 |
| B05 | every step 1 → 600, e.g. step 5 0.5588, step 20 0.6726 | `trajectory.json` (the named steps also in `OUTPUT.txt`) |
| B05, B06 | 0.6989 / 0.2989 / 0.0022, loss 0.6131 | `OUTPUT.txt`, step 600 |
| B06 | max gap from corpus **0.0022**; from truth **0.7011**; argmax sydney | `OUTPUT.txt` |
| B07 | the 601-point loss curve; floor 0.6131 vs corpus entropy 0.6109 | `trajectory.json`, `OUTPUT.txt` |
| B10 | with sydney = 2: argmax canberra, P = 0.5989 | the same script with `COUNTS["sydney"] = 2` (checked 2026-09-27) |

**Motion stays honest.** Bar heights ease between two adjacent real steps, but every digit on
screen is a real step's value — spot-checked: the step-50 frame shows 0.6878 / 0.2866 / 0.0257,
loss 0.6369, equal to row 50. `trajectory.json` is converted to
`pretraining_trajectory.ts` by a generator, never by hand. "The loss fell the whole way" was
checked: the loss decreases at every one of the 600 steps.

---

## 3. What is CONSTRUCTED, and how the video says so

**The corpus is invented** for this demonstration — designed by Claude, accepted by Akshit. It
is not web text and not a measurement of anything:

```
"the capital of australia is sydney"    ×7   (false, but frequent)
"the capital of australia is canberra"  ×3   (TRUE, but rarer)
"the capital of australia is melbourne" ×0   (false, absent)
```

It is built so the false continuation is the frequent one, which makes the objective's target
visible.

**On screen:**
- **B03** opens with a banner, `CONSTRUCTED — corpus invented for this demo, not real web text`,
  before any data appears.
- **B04–B07** carry the stamp `computed from the CONSTRUCTED corpus · code/OUTPUT.txt` on every
  frame that shows a distribution or loss.
- **B09** names the toy scale again as a limit of the explanation.

External fact used: Canberra is Australia's capital; Sydney is the common misconception.

---

## 4. Reconstructed UI, synthetic narration, and what is NOT shown

**No Claude response appears in this video.** B00 and B10 use the toolkit's Claude-styled
composer as set dressing. Both carry an on-screen tag — `RECONSTRUCTED UI · a styled prompt box —
not a real Claude exchange` — with no reply lines and no model chip. Nothing in them was sent to
or returned by Claude. (An earlier cut showed reply-style lines and a "Claude · Sonnet" chip
without a label; they were removed on 2026-09-27.) B10's expected result is stated as what the
script prints, not as a Claude answer.

**The narration is a synthetic voice** — Kokoro `am_onyx`, generated locally. It is not Akshit's
voice. It says so in B00 ("the voice you are hearing is synthetic"), and it is disclosed on screen
in the B00 tag and on the B11 credit card. It does not speak as the author, the instructor, or
the course.

**Captions** are the narration text itself. `runtime/scripts/align.py` places each known word on
the moment it is spoken (faster-whisper supplies timing only), writing `mp3/words.json`;
`tools/make_captions.py` builds `captions.srt` and the burned-in `captions.ass`.

---

## 5. Toolkit revision and changes

Built from **brutalist.art `6a8380ae169cca81e0633664a65c958f5c12ab4b`** (cloned 2026-09-26).
Six toolkit files were changed — four Windows fixes, one opt-in switch, and scene registration —
and three component files were added. The exact patch and new files are in
`toolkit-changes/`. The patch was checked to apply cleanly to that revision. None of these
changes alter what the video claims.

---

## 6. Who did what

Claude Code was used throughout (Claude Opus 5, then Opus 5.5 when the model was switched
mid-session).

**Akshit:**
- chose the concept from the Chapter 1 list, and supplied the assignment text and chapter link
- set the constraints: 12 beats, Kokoro `am_onyx`, 2–4 minutes, stop at the review cut, and no
  GitHub push without permission
- chose between the fixes Claude offered for the toolkit's smoke-test bug (renaming the fixture)
- watched the review cut and reported: overlapping text in B03 (with a screenshot), audio running
  ahead of the video in B02, an incorrect graph in B07, and B05's transitions. Requested the B00
  greeting, the B11 credit, captions, and removal of the footer
- asked for this compliance check, chose to fix everything it found, and chose to keep B08

**Claude:**
- designed the demonstration (the constructed false-frequency corpus), and wrote
  `code/pretraining_target.py`, `tools/make_captions.py` and all scene components
- wrote the narration and beat sheet, and quoted the chapter
- made all toolkit fixes and the `ART_BURNIN=0` switch
- verified every on-screen number against the script output, and every quote against the chapter
- read the rendered frames and found the defects listed in `_qc/REPORT.md`, including B01's
  correction never firing
- drafted every document in this folder

---

## 7. Third-party software, models and fonts

| Asset | Version / origin | Licence |
|---|---|---|
| brutalist.art toolkit | `6a8380ae`, github.com/nikbearbrown/brutalist.art | course toolkit; see its repository |
| Remotion | 4.0.486, rendered locally | Remotion Free License (individuals) — `node_modules/remotion/LICENSE.md` |
| kokoro-onnx | 0.6.1 | not declared in package metadata — see the project repository |
| Kokoro-82M voice model | `kokoro-v1.0.onnx`, downloaded by `./setup --install` | see the model's release page (not re-verified here) |
| faster-whisper | 1.2.1 | MIT |
| Whisper `base` model | downloaded from the Hugging Face Hub on first `align.py` run | see its model card (not re-verified here) |
| onnxruntime | 1.30.0 | MIT |
| numpy | 2.3.2 | BSD |
| EB Garamond, Lato | bundled in `runtime/fonts/` | SIL Open Font License (`OFL.txt`) |

No third-party images, footage, music or B-roll are used. Every frame is rendered from source.
**Free pipeline only**: no paid generation, no API keys, no upload. Toolkit-reported cost: $0.00.
