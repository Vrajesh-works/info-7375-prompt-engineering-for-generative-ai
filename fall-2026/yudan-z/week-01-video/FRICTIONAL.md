# FRICTIONAL.md — Week 1 Explainer Video

**Student:** Yudan (Anica) Zhou

> **Status note.** Every entry below records a Claude Code session I ran and
> directed, and each is labelled with when it was written. The reflections, the
> review-round observations and the decisions are mine; Claude declined to write
> them and said so.

---

## 2026-09-21 — scoping the assignment (retrospective, written same day)

**What I was working on.** Understanding what the Week 1 video actually asks
for, and picking a concept.

**I tried / expected.** I expected "pick a concept from Chapter 1" to be the
easy part and the video toolkit to be the hard part. I had Claude Code clone
the course repo and the Brutalist toolkit and read the chapter, the Canvas
brief, and the prerequisite guides alongside me.

**What happened.** The concept choice turned out to be the decision that
mattered. Claude ran `main.py` and reproduced the chapter's tables exactly
(probabilities `0.0900 / 0.2447 / 0.6652`, counts `102 / 268 / 630` at seed 7)
on Python 3.11.15 — the chapter records Python 3.14.6, so the numbers are not
interpreter-specific, which I had assumed they might be. Claude offered three
candidate concepts. I picked max-subtraction because it is the only one of the
three where I can put a *failure* on screen: `math.exp(1000)` raises
`OverflowError`, so the direct route does not merely lose accuracy, it produces
nothing.

**What Claude contributed.** Reading and summarising the briefs; running the
reference code; proposing the three candidates with their evidence and
boundaries; finding the `[0, -1000]` underflow case; drafting the evidence
script and the submission files.

**What I decided.** The concept. Also that the video ends on the limitation
rather than on `[0.5, 0.5]` — the chapter explicitly warns against the
"numerically stable" slogan, and a video that stops at the happy result is
making exactly the overclaim the chapter is about.

**Friction.** Two real blockers, both in the toolkit, both reproduced in a
clean Linux container against brutalist.art commit
`6a8380ae169cca81e0633664a65c958f5c12ab4b`:

1. `./setup --install` aborts building **ManimPango** (`Package 'pangocairo'
   was not found`). Because pip resolves `requirements.txt` as a unit, this also
   stops `kokoro-onnx` installing, so narration fails too — a missing system
   header takes down the audio pipeline, which was not obvious from the error.
   Installing `kokoro-onnx`, `mutagen` and `Pillow` on their own succeeded and
   `runtime/scripts/setup_smoke_kokoro.py` then reported `kokoro synth OK —
   mean_volume -21.8 dB`. Manim is only needed for equation beats, which the
   prerequisite guide tells first-timers to skip anyway.
2. `./setup` never prints its readiness table. Its ElevenLabs guard greps the
   whole checkout and matches the toolkit's *own* bundled example beat sheets
   under `youtube/brutalist/` (24 hits), then `exit 1`. `./art --list` works
   fine, so the builders are unaffected. I am recording this rather than editing
   the toolkit to make the check pass.

**What I understand now.** That the readiness doctor exiting 1 and the pipeline
being broken are different facts, and the prerequisite guide says so directly
("A green readiness table is not proof of a successful video render"). Here the
inverse held: a red doctor, and a working narration path.

**Still unresolved.** Whether the ManimPango failure also appears on macOS after
`brew install pango cairo pkg-config`. I have not tested that yet.

**Evidence.** `evidence/evidence_output.json`; `BUILD-PROMPT.md` §2.

---

## 2026-09-27 — installing Brutalist on my Windows machine (written same day)

**What I was working on.** Getting the toolkit and the evidence script running
on my own machine instead of the container the scaffold was drafted in.

**I tried.** In a Claude Code session I directed, I had Claude clone
brutalist.art (commit `cd4bf20904be4e7d63babd9622b17963c2361b27`) and run
`./setup --install` on Windows 11 with Python 3.14.2.

**What happened.**

1. `pip install -r requirements.txt` failed as a unit again, but for a
   different reason than on 09-21: `manim>=0.18,<0.19` needs Python <3.13, so
   there was no version for 3.14 to install at all. As before, `kokoro-onnx` did
   not install either.
2. `./setup` exited 1 at the ElevenLabs guard (10 hits under `youtube/brutalist/`
   at this commit) before printing the readiness table. I recorded it and did
   not edit the toolkit. `./art --list` worked.
3. After installing `kokoro-onnx`, `mutagen`, `Pillow`, `numpy` and
   `faster-whisper` on their own, Kokoro still could not synthesize. The first
   checkout was in a deeply nested folder, and espeak-ng's data path came out at
   261 characters, past Windows' 260-character limit. espeak-ng cut the path off
   after `site-packages\` and failed looking for `phontab`. `npm install` for
   Remotion also failed there: esbuild's postinstall could not find
   `esbuild.exe`.

**What I did.** Installed ffmpeg system-wide with winget (the smoke test needs
it), then re-cloned the toolkit into `C:\Users\zyud0\brutalist`. With the short
path, `npm install` succeeded and `runtime/scripts/setup_smoke_kokoro.py`
reported `kokoro synth OK — mean_volume -21.7 dB`. I skipped Manim; it is not
installed. `Pillow` is 12.3.0 rather than the pinned `<11`, which has no build
for Python 3.14.

I also cloned the course repo and re-ran `evidence/max_subtraction_evidence.py`
here. Case A's unshifted values changed in the last two digits (`…046`→`…045`,
`…767`→`…764`), while `max_abs_difference` and cases B and C stayed identical.
`main.py` still reproduced the chapter's tables (`0.0900 / 0.2447 / 0.6652`,
counts `102 / 268 / 630` at seed 7). I kept this run's `evidence_output.json`.

**Still unresolved.** No video has been rendered yet; I have not run
`./art smoke`.

**Evidence.** `evidence/evidence_output.json`; `SCRIPT.md` "Environment
recorded with the run".

---

## 2026-09-27 (evening) — building the reel, and watching it

**What I was working on.** Installing Brutalist on my own machine and building
the explainer.

**I tried / expected.** I thought installing the toolkit would just mean pasting
the prompt from the professor's video and letting it run. In practice there were
many steps I could not have anticipated, because my system and my Python version
differ from the ones the instructions assume — the setup had to be adapted to my
own environment.

**What surprised me most.** Kokoro installed successfully but could not produce
sound, and the cause turned out to be that my folder path was too long. That is
not something I could have predicted. Sometimes a task gets stuck on a detail
this small. Manim's install failed for a related reason — a Python version
mismatch, not anything about the tool itself.

**What I did not understand at first.** When `./setup` exited with an error I
assumed the installation had failed. Later I understood that what failed was the
toolkit's own check script, not the toolkit — `./art --list` ran fine the whole
time.

**What I understand now.** The gap of 1.11e-16 between the shifted and direct
routes, and the last-digit difference between my Windows run and the scaffold's
Linux run, are the same kind of thing: a float can only hold about 16 significant
digits, so where the rounding lands depends on the order of operations and on the
platform's `exp` implementation. Case B and case C are identical across both
platforms because 0.5, 1.0 and 0.0 are exactly representable — there is nothing
to round. That is evidence the 1.11e-16 really is rounding noise and not a second
distribution.

**The review round — what I found by watching, which a frame check could not.**
I watched the full review cut with sound against `SCRIPT.md`. Three things:

- `0:03` — Kokoro read "INFO 7375" as "info seven thousand three hundred seventy-
  five" instead of digit by digit. **This was only catchable by listening**;
  Claude checked frames all evening and could not hear the audio. Fixed by
  writing the narration as "INFO seven three seven five" and re-synthesizing B00.
- `0:30, 0:47, 1:49, 2:16` — the stage-to-stage arrows were too faint to carry
  the "this becomes that" meaning. Made larger and bolder.
- I asked whether the beat-ID slate in the bottom-left survives into the final
  master. It does not — `compile.py` draws it only for `--review` cuts, and the
  final's frames were checked.

Pacing was otherwise fine.

**A decision I made.** Gate V flagged B01's half-typed frame. I chose to shorten
the text rather than pass `ART_STRICT=0` — I would rather fix the frame than
silence the check.

**Known limitation I accepted.** B06's number cells are about 20px at 1080p and
read small. They pass every gate. I chose not to re-render for it, so the
submitted video has a legibility weakness I am aware of and did not fix.

**Still unsure about.**
- I do not fully understand how Remotion turns a beat sheet into rendered frames.
- I do not know whether the font falling back from EB Garamond to Georgia affects
  how the video reads.
- I do not know whether this setup would work on a different machine.

**Evidence.** `build/BUILD-LOG.md` (full QC history), `build/CHECKS-REPORT.md`,
`build/FACTCHECK.md`, `evidence/evidence_output.json`, and the review cut kept at
`reel-week01/week01-max-subtraction-yudan-z-slate.mp4`.