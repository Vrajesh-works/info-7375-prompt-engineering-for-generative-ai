# INFO 7375 — Week 01 Video

**Name:** Ethan Gomes
**Course:** INFO 7375 — Prompt Engineering for Generative AI
**Chapter:** 1 — Randomness and first prompts (Part 1, section "Scale, in units you can check")
**Runtime:** 3:29
**Video:** `ethan_gomes_week1_explainer_video.mp4`

Built with the Brutalist toolkit and Claude Code. What Claude contributed, and
what I directed, is set out in `SOURCES.md`.

---

## The concept

**A training-scale slogan restated as a division with a hidden assumption.**

Specifically: "it would take a person thousands of years to read that much text"
is not a measurement. It is `300B tokens × 0.75 words/token ÷ a reading rate`,
and the reading rate is never stated — which is why the same sentence supports
1,711, 2,139, or 2,852 years depending on a number nobody supplies.

## Why this one

Four lines of arithmetic, every input checkable against a published source, and a
point that lands the moment one unstated number changes and the answer moves by
over a thousand years.

## What the video does *not* establish

It gets its own screen (B10, "Where this stops", just before the closing Your-turn
prompt) and is said aloud: nothing in the video shows that 0.75 words per token, or
any particular reading rate, is the *correct* value. It takes GPT-3's published
figures on trust from Brown et al. and shows only how far the headline moves when
an unstated input changes. **Sensitivity is not accuracy.**

## What's in the video, slide by slide

| Time | Slide | What it shows |
|---|---|---|
| 0:00 | **B00 · The question** | The slogan posed in a Claude chat window, with a real, dated Claude reply beneath it |
| 0:11 | **B01 · The whole idea** | The one-line summary typed out; "measurement" is struck and replaced with "division" |
| 0:21 | **B02 · The published facts** | GPT-3's three published figures (175B parameters, 300B tokens, 3.14 × 10²³ FLOP), with the source paper |
| 0:39 | **B03 · Do the division** | The reading slogan written out line by line: 300B tokens × 0.75 ÷ 250 words/min = **1,711 years** |
| 0:57 | **B04 · The hidden parameter** | The same division at 250, 200 and 150 words/min: 1,711 / 2,139 / 2,852 years, a **1,141-year spread** |
| 1:14 | **B05 · What survives** | The three precise answers struck through; what they all support: "more text than a person could read in many lifetimes" |
| 1:31 | **B06 · Same move, new units** | The compute slogan: 3.14 × 10²³ operations ÷ a billion per second ÷ seconds per year = **9.95 million years** |
| 1:49 | **B07 · Two sentences, two budgets** | "About 9.95 million years" vs "over 100 million years": the second needs ~10× the compute, a different model |
| 2:07 | **B08 · The method** | The same ladder with the example removed, ending "→ Now try other values for the rate" |
| 2:23 | **B09 · Verdict** | What the chapter's approach gets right and where it falls short |
| 2:39 | **B10 · Where this stops** | Shown vs not shown: the boundary of the claim. "Sensitivity is not accuracy." |
| 2:57 | **B11 · Your turn** | A prompt viewers can run on a number from their own field; "Created by Ethan Gomes" |

The same division ladder appears three times (B03, B06, B08) on purpose: reading,
then compute, then the bare method. Seeing one move work on two different slogans
is what makes it a method rather than a one-off example.

## How it was checked

- **Visuals.** The toolkit's frame-level QC gate (24 sampled frames: no blocking or
  major defects), plus a human read of frames from the final master. See
  `_qc/REPORT.md`.
- **Numbers.** Re-derived independently, then matched against the chapter's script
  output. See `FACTCHECK.md` and `SOURCES.md`.
- **Narration.** Every beat was transcribed with faster-whisper and compared with
  the script; tricky readings (the course number) were checked against the voice
  model's own phonemes.
- **Paperwork.** Every `.md` file was audited against the final cut; the problems
  that turned up are logged in `FRICTIONAL.md`.

## Known limitations

- **The narration checks are machine checks.** Transcription and phonemes show every
  word is intelligible and read as intended; they don't show the voice sounds
  natural.
- **The voice is a local text-to-speech model** (Kokoro `am_onyx`), not a recording.
  Numbers are read as spelled out in the script, so a few captions are long
  ("one thousand seven hundred eleven years"); the same figures appear as digits on
  screen.
- **It departs from the Brutalist house style** in two places, deliberately: it ends
  on the Your-turn prompt instead of a title card, and it addresses viewers as
  "Students" instead of the toolkit's default narrator. Logged in `BUILD-LOG.md`.
- **Internal names still use the toolkit's slug** (`claude-liam-hidden-parameter`),
  which is why `./art final` needs the rename step below. Only the submitted video
  is named `ethan_gomes_week1_explainer_video.mp4`.

## Watching with captions

Open the mp4 in **VLC** or **IINA**; the `.srt` beside it has the same name and loads
automatically. QuickTime doesn't load separate caption files.

## Are the numbers real?

Yes, and reproducible. Every figure on screen was checked against the chapter's own
derivation script, fetched and run locally on 2026-09-27:

```bash
curl -fsSL https://raw.githubusercontent.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/main/research/llm_scale.py -o llm_scale.py
python3 llm_scale.py
```

Its output matches the committed `research/llm-scale.json` (copied here as
`llm-scale-recorded-output.json`) and every number on screen. The full mapping,
including the two figures derived by subtraction/rounding rather than read off the
script, is the table in `SOURCES.md`.

The Claude reply in the opening slide is a real one (Claude Opus 5, 2026-09-27),
recorded in full in `claude-response-B00.md`; the screen shows a labelled verbatim
excerpt. The Your-turn prompt on the last slide is deliberately shown **un-run**,
with no Claude output.

## How to rebuild this video from this folder

Tested on macOS (Apple Silicon). `BUILD-PROMPT.md` has the same steps as a
paste-ready prompt, with the QC gates and the two traps specific to this video.

**1. Get the toolkit and add this video's components.** A fresh clone doesn't have
the six scene components this video uses or the patched last-slide scene.

> **On GitHub** the two scene files are stored as `DerivationScenes.tsx.txt` and
> `ClaudeComposerAsk.tsx.txt`, because the course repo's CI rejects TypeScript
> files. Same contents; drop the `.txt` when copying them into the toolkit. The
> Canvas zip has them as plain `.tsx`. The video file itself is only in the Canvas
> zip.

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
cp <this-folder>/DerivationScenes.tsx  runtime/remotion/src/scenes/
cp <this-folder>/ClaudeComposerAsk.tsx runtime/remotion/src/scenes/   # adds the optional credit line
```

Then add the two blocks in `ROOT-REGISTRATION.md` to
`runtime/remotion/src/Root.tsx` (one import, six `<Composition>` entries).

**2. Set up the environment, in this order.** The reasons for each line are in
FRICTIONAL.md.

```bash
eval "$(/usr/libexec/path_helper)"   # only matters if MacTeX is installed; must come BEFORE the venv
python3.11 -m venv .venv             # needs Homebrew python3.11; 3.9 and 3.13+ both fail
source .venv/bin/activate
unset CC CXX CFLAGS CXXFLAGS CPPFLAGS LDFLAGS LDFLAGS_LD CC_FOR_BUILD CXX_FOR_BUILD   # only if Anaconda is active
./setup --install
./art scene-index                    # makes the new components findable
```

LaTeX/MacTeX is **not** needed for this video (it has no Manim equation beats), so
`./setup` may show that one feature red. That's fine.

**3. Build.** From the toolkit root, with this folder as `<reel>`:

```bash
python3 runtime/scripts/generate_audio_kokoro.py <reel>   # 12 narration mp3s, Kokoro am_onyx
./art run   <reel> --height 1080                          # review cut + visual QC gate
./art final <reel> --height 1080 --out <reel>             # clean master, written into <reel>
mv <reel>/claude-liam-hidden-parameter.mp4 <reel>/ethan_gomes_week1_explainer_video.mp4
```

`./art final` names its output after the project slug
(`claude-liam-hidden-parameter`), hence the rename.

**4. Captions** (only needed if any narration changes; the `.srt` here is current):

```bash
python3 runtime/scripts/align.py <reel>                               # word timings → mp3/words.json
python3 <reel>/make_captions.py <reel> ethan_gomes_week1_explainer_video
```

## Files

| File | What it is |
|---|---|
| `ethan_gomes_week1_explainer_video.mp4` | **the video** (clean master, 3:29) |
| `ethan_gomes_week1_explainer_video.srt` | English captions: exact script text, word-timed to the narration. Same basename as the video, so VLC/IINA load it automatically |
| `beat_sheet.json` | the reviewed narration + visual plan, 12 beats |
| `BUILD-PROMPT.md` | prompts and commands that rebuild it |
| `SOURCES.md` | numbers table, constructed vs real, third-party licences, what Claude contributed |
| `FRICTIONAL.md` | dated log of what broke and what I did instead |
| `FACTCHECK.md` | every on-screen claim, re-derived |
| `PROMPTS.md` | the two prompts shown on screen, verbatim |
| `claude-response-B00.md` | the full real Claude reply excerpted on the opening slide |
| `CHECKS-REPORT.md` | per-beat SHOW/HOLD/CARD + teaching-arc check |
| `SHOTLIST.md` | beat → scene mapping |
| `BUILD-LOG.md` | build decisions and defects found in QC, in date order |
| `DerivationScenes.tsx` | the six scene components written for this video |
| `ClaudeComposerAsk.tsx` | toolkit composer scene, patched with an optional `credit` prop for "Created by Ethan Gomes" on the last slide (default empty) |
| `ROOT-REGISTRATION.md` | the exact `Root.tsx` import + `<Composition>` blocks a fresh toolkit clone needs |
| `make_captions.py` | builds the `.srt`/`.vtt` from `mp3/words.json`; shows the spoken "Info seven three seven five" as "INFO 7375" |
| `llm_scale.py` | the chapter's own derivation script, as fetched and run |
| `llm-scale-recorded-output.json` | its recorded output; every on-screen number traces here |
| `_qc/REPORT.md` | visual QC: gate output + human review of the final cut |
| `qc-sheet.png` | contact sheet of one frame per beat |

## Cost

$0.00. Kokoro narration and Remotion rendering run locally. No paid generation, no
API keys, no media account.
