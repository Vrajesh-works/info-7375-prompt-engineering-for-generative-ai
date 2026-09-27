# What Pretraining Actually Targets

**Akshit Verma** · INFO 7375 — Prompt Engineering for Generative AI · Week 01

---

## The concept

**What pretraining actually targets — the token that followed, not the truth.**
From Chapter 1, **Part 1** ("Where the numbers come from").

**Why this concept** *(sentence drafted by Claude)*: it is the smallest idea in Chapter 1 that
changes how you read every model output afterwards — if the objective never had access to truth,
a fluent answer is evidence about the corpus, not about the world.

**Runtime:** 2 min 59 s (2:58.79). Twelve beats, one concept, no chapter tour.

**Video:** `week-01-pretraining-target-captioned.mp4` — 1920×1080, H.264 + AAC, captions burned in.
`captions.srt` ships alongside as a toggle-able sidecar. (`week-01-pretraining-target-slate.mp4` is the
same cut without captions.)

> **The video is submitted on Canvas, not in this GitHub folder.** The course repository's
> `.gitignore` excludes all `.mp4` files ("Keep generated audio/video out of Git"), so the
> mp4 travels only in `Verma_Akshit_INFO7375_Week01_Video.zip`.

---

**Disclosures shown on screen:** the narration is a **synthetic voice** (Kokoro `am_onyx`), not
the author's. The Claude-styled prompt box in B00 and B10 is **reconstructed UI** — no Claude
response appears anywhere in the video. The corpus is **constructed**, and every frame computed
from it says so.

## How it explains the concept

The chapter states the objective in four steps and then says *"Nothing in this loop
is told what is true. The target is what the corpus did next."* Rather than assert
that, the video **runs the objective on a corpus that is deliberately wrong** and
shows where it lands.

The corpus — invented for this demonstration, and labelled `CONSTRUCTED` on screen — contains one
context, `"the capital of australia is ___"`, followed by:

| continuation | times | |
|---|---|---|
| `sydney` | 7 | false, but frequent |
| `canberra` | 3 | **true**, but rarer |
| `melbourne` | 0 | false, absent |

Gradient descent on cross-entropy — the actual pretraining objective — then runs,
and the video shows the distribution moving — through **every one of the 601 real steps**, not
just the six printed ones, with dashed lines marking the corpus frequencies the bars climb onto.
Every digit on screen is a real step of the run. It converges to:

```
P(sydney) = 0.6989    P(canberra) = 0.2989    P(melbourne) = 0.0022

max gap from CORPUS FREQUENCY : 0.0022
max gap from TRUTH            : 0.7011
argmax = sydney   (truth = canberra)
```

**That pair of numbers is the concept.** The objective walked the model to within
two thousandths of the corpus and left it seven tenths away from the right answer,
and the loss fell monotonically the entire way. Nothing in the loop objected.

The video adds one detail the chapter does not spell out: the loss **stops at
0.6131**, not at zero, because the corpus contradicts itself about this context.
The floor is the corpus's own entropy, **0.6109**. A perfect fit to a wrong corpus
is still a perfect fit — which is the sharpest available evidence that the objective
is satisfied by reproducing text, not by being right.

### Why B08 mentions preference tuning

Chapter 1 lists *why preference tuning can prefer a confident wrong answer* as a separate
concept. B08 does not teach it. It closes the obvious objection to this video's one concept —
*doesn't later training fix this?* — with the chapter's own line that **neither stage receives
an answer key**, then returns to the pretraining target.

## What the video says it does not establish

Named explicitly on screen in beat B09, per the assignment:

1. A three-token toy is not a language model — the mechanism scales, this demo does not.
2. Real output probabilities are **not** web frequencies; real models generalize and
   are preference-tuned afterwards, and the chapter itself says nobody can read off
   why a given prediction was made.
3. This is **not** a claim that models are usually wrong. Corpora are mostly right.
   The point is that being right was never what was optimized.

What survives all three: **truth was never the target.**

---

## How it is timed and captioned

Every visual appears **on the word that names it**. The toolkit's `align.py` places each
known narration word on the moment it is spoken (faster-whisper for timing only), and
each beat's reveals read those times. The same word clock generates the captions, so
they are the narration verbatim, in sync.

## Rebuilding it

Full detail in `BUILD-PROMPT.md`. Short version:

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
./setup --install                     # one token: --install
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8   # required on Windows

# place this folder at youtube/brutalist/week-01-video/
# and pretraining.tsx at runtime/remotion/src/illustrations/

REEL=youtube/brutalist/week-01-video
python3 $REEL/code/pretraining_target.py | tee $REEL/code/OUTPUT.txt
python3 runtime/scripts/generate_audio_kokoro.py $REEL
python3 runtime/scripts/align.py $REEL                  # word clock
python3 runtime/scripts/remotion_scenes.py $REEL
ART_BURNIN=0 ART_FACTS=0 ART_QC=1 ART_STRICT=0 bash runtime/scripts/run.sh $REEL
cd $REEL && python3 tools/make_captions.py              # then burn in: see BUILD-PROMPT.md §3
```

**Five small toolkit changes are required** (four Windows fixes, one opt-in switch) — all one- or two-line changes,
each with file and line in `FRICTIONAL.md`.

Build stops at the **review cut** by design. No final cut, no upload, nothing pushed.

---

## Files

| File | What |
|---|---|
| `week-01-pretraining-target-captioned.mp4` | **the video** (captions burned in) |
| `captions.srt` | sidecar captions, same text and timing |
| `week-01-pretraining-target-slate.mp4` | the same cut without captions |
| `beat_sheet.json` | reviewed narration + per-beat visual plan (12 beats) |
| `code/pretraining_target.py` | the demonstration; every on-screen number comes from it |
| `code/OUTPUT.txt` | its verbatim stdout — the provenance for every figure |
| `REVIEW-LOG.md` | the watch-and-revise record: each problem reported after watching, with its fix |
| `toolkit-changes/` | the exact toolkit patch (`git apply`-checked against `6a8380ae`) and new component files |
| `code/trajectory.json` | all 601 steps of the same run — drives the B05 bars and the B07 curve |
| `mp3/words.json` | word-level timing of the narration — drives visual cues and captions |
| `tools/make_captions.py` | builds `captions.srt` / `captions.ass` from `mp3/words.json` |
| `BUILD-PROMPT.md` | prompts and commands that rebuild the video |
| `SOURCES.md` | chapter quotes, number provenance, what Claude contributed, licences |
| `FRICTIONAL.md` | dated process log in the course's seven-prompt format |
| `_qc/REPORT.md` | frame-level visual QC: the automated gate's findings plus Claude's frame reads |

**Everything is free and local.** Kokoro narration, Remotion rendering, numpy.
No API keys, no paid generation, no uploads. Toolkit-reported cost: **$0.00**.

## Credits

- **Toolkit:** brutalist.art (Film as Code) by Nik Bear Brown, revision `6a8380ae`.
- **Course material:** INFO 7375, Chapter 1 Part 1, quoted in `SOURCES.md` §1.
- **Assistance:** Claude Code (Claude Opus 5 / Opus 5.5) did most of the building — script,
  narration, scenes, fixes and document drafts. `SOURCES.md` §6 says who did what.

