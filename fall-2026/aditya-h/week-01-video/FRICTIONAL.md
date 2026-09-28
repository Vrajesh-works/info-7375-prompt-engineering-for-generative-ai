# FRICTIONAL.md: INFO7375 Brutalist toolkit videos

**Author:** Aditya Hasija · **Agent:** Claude Code (Claude Opus 5.5), desktop app
**Dates:** 2026-09-26 23:51 → 2026-09-27 20:30 (US Eastern)
**Toolkit:** `~/brutalist.art` (public cut of the Brutalist toolkit) · **Reels:** `~/INFO7375/youtube/`

A dated log of every point where the work did not go straight through: toolkit
bugs, missing dependencies, pipeline gates that blocked a render, and mistakes
made by the agent. Each entry states what happened, how it was resolved, and
where the evidence is. The full per-command record for this video is
`COMMAND-LOG.md` in this folder. The complete chat transcript is kept locally
and not posted (the brief asks to omit private conversation transcripts).

*How this log was written:* drafted by Claude Code from the session's command
logs and timestamps, at my request; the decisions marked `HUMAN` are mine. This
submission is the seed video; the softmax video entries are kept because they
are the same toolkit session and the friction carried over.

**Categories:** `TOOLKIT` bug or gap in brutalist.art · `ENV` missing software on
this Mac · `GATE` a toolkit quality gate blocked a render (working as designed) ·
`AGENT` a mistake by Claude · `DESIGN` a layout or visual iteration · `DATA` a
finding in the real computed output that changed the script · `HUMAN` a
decision made by me.

---

## Outcomes at a glance

| Deliverable | Result | Final gates |
|---|---|---|
| `softmax-max-subtraction.mp4` | 2:43, 3840×2160, 4 beats | GATE T PASS · GATE V 0 BLOCKER / 0 MAJOR |
| `seed-repeatable-not-correct.mp4` | 3:02, 3840×2160, 6 beats (incl. intro) | GATE T PASS · GATE V 0 BLOCKER / 0 MAJOR |
| Session transcript (.docx) | 14 prompts, all replies, 218 steps | Word-structure validator PASS |

| Measure | Softmax reel | Seed reel |
|---|---|---|
| Time, first command → final master | 51 min (23:52 → 00:43) | 40 min (16:20 → 17:00), plus 2 follow-up edits |
| `./art final` attempts until PASS | 4 | 5 (then 1 each for the intro and the credit) |
| Low-res QC render passes | 3 | 3 |
| Cost | $0.00 (Kokoro + Manim, local) | $0.00 |
| Uploads / git push or pull | none | none during the build (submission pushed 2026-09-28) |

---

## 2026-09-26 (Sat): Softmax max-subtraction video

**23:51 · HUMAN.** Pasted the brief: a 3-beat video on the max-subtraction trick,
free pipeline only, show the beat sheet before rendering, keep a command log.

**23:52 · ENV.** The session had started in an empty scratch folder, not in the
toolkit. Claude searched the disk (`mdfind -name HOW-TO.md`), found
`~/brutalist.art`, and moved the session there. *Cost: under 1 min.*

**23:52 · TOOLKIT.** `./setup` (the documented readiness check) **exits 1 before
checking anything**: its "ElevenLabs guard" greps the repo and matches 10 of the
toolkit's *own* example files under `youtube/brutalist/…`. A clean checkout fails
its own setup. *Workaround:* dependencies checked by hand. The toolkit was not
edited, since it is the public copy.

**23:53 · ENV.** No LaTeX or `dvisvgm` on this Mac, so Manim's `MathTex` is
unavailable. The toolkit's no-LaTeX math route (`runtime/scripts/typeset_math.py`,
matplotlib mathtext) needs **matplotlib, which is missing from the toolkit's own
`.venv`** and from `requirements.txt`. *Fix:* `.venv/bin/pip install matplotlib`
(free, local).

**23:54 · TOOLKIT.** The toolkit's `ai-explainer` skill requires Claude-branded
bookends (a Claude-interface cold open, an overview beat, a "Your Turn" handoff,
an @NikBearBrown outro). The assignment asked for exactly 3 beats plus a card.
*Resolution:* bookends omitted and the deviation documented in the beat sheet;
the compiler later printed matching `SKIN LINT` warnings, which don't block.

**23:55 · DATA.** Ran `evidence/softmax_demo.py` on `[1000, 1000]`. The brief
expected an overflow error; **the real NumPy behaviour is two `RuntimeWarning`s,
`[nan nan]`, and exit code 0.** The program does not crash. *Resolution:* the
narration says exactly that. (Pure-Python `math.exp(1000)` does raise
`OverflowError`; logged, not shown.)

**23:55 · DATA.** Raw and shifted probabilities for `[1, 2, 3]` match to the
printed 6 decimals but **differ by 1.1×10⁻¹⁶ in float64**. *Resolution:* an
on-screen footnote instead of claiming they are identical.

**23:56 · HUMAN.** Reviewed the beat sheet. Approved; kept my name on the
closing card; approved shortening the warning path. Mid-render, instructed:
**no git push or pull.** No git commands were run for the rest of the session.

**23:58 · TOOLKIT / ENV.** The toolkit's word aligner (`align.py`) needs a
faster-whisper model download from HuggingFace. *Workaround (to avoid an
unrequested download):* `cues.py` times reveals from `ffmpeg silencedetect`
pauses plus character-position estimates. Accurate to about ±0.5 s.

## 2026-09-27 (Sun): Softmax video, render and gates

**00:03 · AGENT.** First QC render: B02/B03 crashed with `KeyError: 'python'`
because `ENV.txt` keys are space-padded. *Fix:* strip keys. *Cost: 1 re-render.*

**00:04–00:09 · DESIGN.** Three rounds of contact-sheet frame review:
undersized equation; terminal text crossing panel borders; a footnote off-frame;
low-contrast terracotta text; a clipped caption; Pango silently dropping leading
spaces in code lines (fixed with non-breaking spaces).

**00:10 · GATE.** `run.sh` refuses to render without `FACTCHECK.md`,
`SHOTLIST.md` and `PROMPTS.md` (GATE F). Written before rendering, as designed.

**00:10 · ENV.** `manim` isn't on the system PATH and system `python3` lacks
matplotlib, so every toolkit run needs `PATH="$PWD/.venv/bin:$PATH"` set by hand.
Not documented in HOW-TO.md.

**00:10 · TOOLKIT (silent failure).** The first `./art run` printed "nothing to
render" and **started compiling B01 as a placeholder slate**. Cause: `run.sh`
discovers scenes with the regex `class ([A-Z]…_\w+)\(Scene\)`, which only
matches classes whose base is *literally* named `Scene`; the scenes subclassed a
timing base class. *Fix:* rebind `Scene = Timed`. Stopped the run and deleted
the slate clip.

**00:10 · TOOLKIT / AGENT.** The second run failed GATE A on a phantom scene
`B0x_Name`: the same regex matched example text in a code comment Claude had
written. *Fix:* reworded the comment.

**00:11 · TOOLKIT.** GATE A (`static_scene_check.py`) runs `construct()`
against a stub of Manim that doesn't model `VectorizedPoint` or path-building
calls, which the no-LaTeX math route needs. It cannot pass valid scenes that use
them. *Workaround:* `ART_QC=0` (skips gates A/W/B/V during `./art run`); GATE T
and GATE V still run under `./art final`, plus manual frame review.

**00:17 · GATE.** `./art final` #1: **GATE T FAIL**. B02 text 37 px < 41 px floor
at 4K (a footnote had been auto-shrunk to fit). *Fix:* shorter footnote at full
size. *Cost: ~3 min.*

**00:27 · GATE.** `./art final` #2: **GATE V REFUSED**. B02 caption 0.04 units
below the title-safe line (2× BLOCKER); B04 closing card 47% fill < 55% (MAJOR).

**00:28–00:29 · DESIGN.** B04 fixes took three tries: bigger type overlapped
(font size 56 renders much larger than estimated); then `fit()` made the two
statements different sizes; finally stacked with `next_to` and scaled as a whole.

**00:36 · GATE.** `./art final` #3: GATE V still 1 MAJOR (B04 fill 52%).
*Fix:* measured the fill fraction directly from the Manim layout (the metric
matched the gate at 52.2%), then resized to 63.7%. No more guessing.

**00:42 · PASS.** `./art final` #4: GATE T PASS, GATE V 0/0. Master
`softmax-max-subtraction.mp4`, 162.6 s. Manual 15/50/85% frame review clean.

**00:43 · TOOLKIT (side effect).** `git status` in the toolkit showed
`runtime/remotion/package-lock.json` modified (2 lines: `zod`,
`@remotion/zod-types`) by the pipeline, although the reel had no Remotion beats.
Left for me to revert or keep.

## 2026-09-27 (Sun): Seed video ("repeatable is not the same as correct")

**16:20 · HUMAN.** "Scratch that": new brief. 5 beats, lighter myth-busting
tone, ~3 min, show the beat sheet first.

**16:20 · DATA (confirmed).** `seeded_sampler.py` with seed 7 reproduced the
brief's counts exactly: `{0: 102, 1: 268, 2: 630}`. Two separate runs were
byte-identical. *Added evidence:* 100 more runs, all identical (backs a narration
line). A different seed (8) gives different counts.

**16:22 · TOOLKIT.** The ai-explainer SKILL.md documents a per-beat
`lead_silence_s`, but **no script in `runtime/scripts/` reads it**, so there is
no built-in way to add silent holds. Narration came to 2:35, under target.

**16:23 · HUMAN.** Approved the beat sheet; chose silent holds after reveals;
kept the Sydney/Canberra mock-chat example.

**16:24 · AGENT (workaround built).** Wrote `pad_holds.py`: inserts silence
inside real detected pauses (never cutting a word), keeps originals in
`mp3/raw/`, and updates `actual_duration_s`, which the compiler uses as the
clock. Total 2:42.

**16:25 · AGENT.** Cue-timing bug: two B03 cues snapped to the same pause. The
first fix over-corrected, so the red X would have landed ~2.6 s late. *Fix:*
limit forward snapping to 0.6 s. Two iterations within one minute.

**16:31 · ENV / DESIGN.** In the Noteworthy handwriting font the digit **0 is
indistinguishable from the letter O**, which matters on a note that reads
"outcome 0". A glyph test render picked Marker Felt instead.

**16:30–16:34 · DESIGN.** Frame review round 1: overlapping tags, the stamp
hiding run 1's counts (the key evidence), the sticky note covering box 0,
`Indicate(color=…)` flooding chat bubbles solid dark, a badge running off-frame,
a closing card underfilled at its midpoint (redesigned so the whole card shows
from the start, with the active sentence highlighted).

**16:34 · AGENT.** Root cause of "oversized" stamps and badge: Claude's
`slam()` helper ran `animate.scale()` and `FadeIn()` on the same object at once;
FadeIn won, so everything stayed 1.5× too big. *Fix:* a single
`FadeIn(scale=1.5)`.

**16:41 · GATE.** Final #1: **GATE T FAIL**. B03 text 40 px, one pixel under the
41 px floor. *Fix:* enlarged all small B03 text.

**16:45 · GATE.** Final #2: **GATE T FAIL**. Overflow: 2 text runs outside
the 90% title-safe box. *Method that worked:* extract the exact frame GATE T
samples (each beat's midpoint) and overlay the safe box.

**16:49 · TOOLKIT (false positive).** Final #3: **GATE T FAIL**, "terracotta
accent text 2.74:1". The detector classifies text-shaped terracotta blobs as
text; a smaller terracotta box matched. The toolkit's own remedy is a
**hard-coded list of scene names inside `type_check.py`**, i.e. editing the
public toolkit per reel. *Resolution:* removed the accent fill in that beat
instead (it wasn't the beat's focus anyway).

**16:54 · GATE.** Final #4: GATE T PASS; **GATE V REFUSED**, 2 BLOCKER (content
over the top and left safe edges) + 2 MAJOR (underfill while the hook text was
still typing; low-contrast grey dots). Fixed with positions computed from
measured bounds.

**17:00 · PASS.** Final #5: GATE T PASS, GATE V 0/0. Master 162.0 s.

**17:01 · ENV (minor).** zsh aborted a chained command because an `rm` glob
matched nothing. Re-ran without it.

**18:44 · HUMAN (feedback).** "The start of the video is very abrupt." Asked for
a 10–20 s intro, then added: include the line *"this video is meant to explain
the concept of ___"*. Claude filled the blank with "seeded randomness: why a
seed makes a sampling run repeatable, but not necessarily correct".

**18:45–18:47 · DESIGN.** New intro beat B00: the audio was generated for B00
only, holds were re-applied, and B01–B05 were verified identical to before. Two
layout passes (the dot field overlapped the shrunken title and crossed the safe
edges).

**18:47 · AGENT.** Claude launched the render with a shell `&` instead of the
tool's background mode, so no completion notice would arrive. *Recovery:*
confirmed the process with `pgrep`, then waited with a loop that also catches
failure or the process dying. The final passed first try (3:01.7).

**18:58 · HUMAN.** Asked for "Made by Aditya Hasija" on the title card in a cool
colour. Teal `#1F6F78` (≈5:1 contrast on cream). Final passed first try at
19:03.

## 2026-09-27 (Sun): Transcript export to Word

**20:21 · HUMAN.** Asked for the whole chat as a Word document.

**20:22 · ENV.** The app's transcript export worked (54 MB zip in Downloads,
mostly screenshots). Converting it hit three missing tools: **pandoc not
installed**, **the `docx` npm library not installed** (the Word skill assumes it
is preinstalled), and **LibreOffice / pdftoppm not installed**, so pages couldn't
be rendered for review. The skill's validator also needed a missing Python module
(`defusedxml`).
*Workarounds:* installed `docx` and `defusedxml` into a temporary folder only;
wrote a small Markdown→Word converter; validated the structure (PASS); previewed
with macOS Quick Look (page 1 plus a sample reply with a table and lists).

**20:23 · DATA.** The mid-render "don't push or pull" message wasn't stored as a
normal user message but as a queued-prompt attachment. Found and included it, so
all 14 prompts are in the document.

---

## Patterns worth noting

1. **The quality gates earned their keep.** GATE T and GATE V together blocked 7
   renders across the two reels, and each block was a real defect (text too
   small, outside the safe area, underfilled, low-contrast), except one false
   positive. Neither reel shipped with a known layout defect.
2. **Most time went into iteration on layout, not on the core idea.** The
   evidence (script runs, fact-checks) took minutes. Getting every frame inside
   the safe area at legible sizes took the majority of the time.
3. **Measuring beat guessing.** Two late fixes worked first time because they
   used the gate's own inputs: extracting the exact frame the gate samples,
   and computing the fill fraction from the layout before rendering.
4. **Toolkit gaps a first-time user would hit:** setup fails on a clean checkout;
   the venv must be put on PATH by hand; matplotlib is missing from the venv;
   `lead_silence_s` is documented but unimplemented; scene discovery is a
   fragile regex that fails silently into slates; GATE A cannot run the
   toolkit's own no-LaTeX math approach; per-reel contrast exemptions require
   editing the toolkit.
5. **Agent mistakes (all caught before delivery):** an ENV-parsing bug, a
   comment that triggered the scene regex, a double-animation bug that made
   stamps 1.5× too big, two cue-timing bugs, and a background job launched the
   wrong way. Each was found by frame review or log checks, not by the viewer.
6. **Honesty constraints held throughout:** on-screen numbers are read from
   recorded output files at render time; constructed elements (the answer key,
   the mock chat, the `[1000, 1000]` stress test) are labelled as constructed; and
   two places where the real output differed from the brief (no crash on
   overflow; probabilities equal only to printed precision) are said plainly.

## 2026-09-28 (Mon): Preparing the GitHub submission

**HUMAN.** Gathered README.md, BUILD-PROMPT.md, SOURCES.md, FRICTIONAL.md and
beat_sheet.json in a folder and asked Claude Code to check them against the
assignment brief and push to `fall-2026/aditya-h/week-01-video/`.

**DATA (check).** The brief says to use what the course's
`lessons/01-randomness-and-first-prompts/code/main.py` prints. The video's
numbers came from our own `seeded_sampler.py`, so we ran `main.py` too: it
prints the same probabilities and the same counts `{0: 102, 1: 268, 2: 630}`
(`evidence/course_main_py_output.txt`). No change to the video needed.

**AGENT (checks before pushing).** The folder as first gathered could not
rebuild the video (no `scenes.py`, evidence scripts or recorded runs, and the
mp4 was listed but missing). Those were added. The README's rebuild steps
skipped `pad_holds.py` and `cues.py`. BUILD-PROMPT.md listed the narration
command as the evidence command, and paraphrased two follow-up prompts as if
quoted; they are now verbatim. SOURCES.md described `seeded_sampler.py` as my
own implementation; it was written by Claude Code, and now says so. Remotion
was listed but not used in this video. All Python files were checked to parse
on Python 3.11 (the oldest version the repo's CI tests), and no Markdown file
has a relative link that CI would flag as broken.

**HUMAN · Learning and uncertainty** *(retrospective, written by me on 2026-09-28; wording tidied by Claude Code)*

- **AI is far more capable than I expected.** Claude Code read the toolkit's
  documentation, wrote the sampler, the Manim scenes and the audio scripts, and
  found and fixed its own bugs across several render-and-check rounds.
- **But it still needs direction to do the right thing by itself.** The choices
  that shaped the video came from my prompts and review points: the brief and its
  constraints, approving the beat sheet, choosing silent holds, keeping the
  Sydney example, and noticing the opening was too abrupt and asking for an intro.
- **Using Claude Code was eye-opening,** and I learned that understanding the
  mechanisms working in the background is crucial to getting the best out of AI.
  In this project that meant knowing what a seed actually controls (the run, not
  the answer) and what the toolkit's quality gates were checking when they blocked
  a render.

