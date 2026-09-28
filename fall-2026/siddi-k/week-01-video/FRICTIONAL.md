# FRICTIONAL — Week 1 video: Subtract the Max

Siddi Kommuri · INFO 7375 · Fall 2026

The build was done in one Claude Code session (Claude Opus 5.5) that Siddi directed. Entries below
marked **[session log]** record what happened in that session: commands, errors and fixes. Entries
marked **[Siddi]** must be written by Siddi, because they are about Siddi's own understanding and
checks, and nobody else can write those honestly. Claude organized these notes but did not invent
any difficulty or timestamp.

---

## 2026-09-26 · Choosing the concept [session log + Siddi]

- **Tried / expected:** Picked one concept from Chapter 1 Part 2: *why subtracting the maximum changes
  the intermediate weights but not the distribution*. Claude recommended it. Siddi chose it from four
  options (max-subtraction, expected vs observed, temperature as ratio, seed ≠ truth).
- **Why this one:** The mechanism can play out on screen with real numbers, and it has a boundary you can show:
  `math.exp(1000)` actually raises `OverflowError`, and `[0, -1000]` actually returns `[1.0, 0.0]`.
- **[Siddi] My prediction before seeing the numbers:** _(write what you expected: e.g. did you expect the
  direct and shifted routes to be bit-identical? did you expect `[0, -1000]` to break?)_

## 2026-09-26 · Getting the real numbers [session log]

- The course repo was not on this machine; only `Downloads/01-randomness-and-first-prompts.md` was.
  Siddi supplied the repo URL, and Claude sparse-cloned `lessons/01-randomness-and-first-prompts` and
  `research` at commit `149c8e7fba1f69a3c88aac09a1be60fe012d04c6`.
- Ran `python main.py` → `[0.09003057317038046, 0.24472847105479764, 0.6652409557748218]`, counts
  `{1: 268, 2: 630, 0: 102}`. This matches the chapter's recorded run (0.6652409558, 630).
- `python -m unittest discover -s tests` → `Ran 6 tests … OK` (pytest isn't installed, so I used unittest).
- Wrote `code/evidence.py` so every on-screen number comes from one script, not from typing.
- **Unexpected result 1:** the direct and shifted routes on `[1, 2, 3]` are **not bit-identical**:
  differences `-1.39e-17, 0.0, 1.11e-16`. The chapter says the factor "cancels", which is true in
  algebra; in floats the last digit can differ. I put this in the video as part of the boundary.
- **Unexpected result 2:** for `[0, -1000]`, the *direct* route also returns `[1.0, 0.0]`. So the
  subtraction neither causes nor fixes underflow. I had assumed the boundary would be "the shifted
  version underflows", but it's more precise to say "the shift only protects the top".
- True value of the lost probability, via `Decimal(-1000).exp()` at 30 digits: `5.0760E-435`.

## 2026-09-26 · Toolkit install on Windows [session log]

Frictional in the literal sense. Each item is a real error and what was done about it:

| What broke | What I did |
|---|---|
| `git clone brutalist.art` into the app's scratch folder failed: `Filename too long` (Windows path limit) | Cloned to `Documents/GitHub/brutalist.art` with `git -c core.longpaths=true` |
| `python3` is a Microsoft Store stub on Windows | Made a `python3` shim pointing at a dedicated venv (`build/env.sh`) |
| `requirements.txt` pins `manim>=0.18,<0.19`; no 0.18 build exists for Python 3.13 | Used `manim 0.19.1` via `build/requirements-win.txt` (only that pin changed) |
| `ffmpeg` not installed | `winget install Gyan.FFmpeg` (ffmpeg 9.0.2); PATH didn't refresh, so added its `bin` to `env.sh` |
| My first background install wrote to an unquoted log path with a space in it, so nothing ran | Re-ran with the path quoted |
| `remotion_scenes.py` → `[WinError 2]` on every beat: Python can't find `npx`, which is `npx.cmd` on Windows | One-line local patch: `shutil.which("npx")`. Saved as `build/remotion_scenes-windows-npx.patch`; not pushed upstream |
| `remotion_scenes.py --only B00 B01 …` rejected (takes one beat) | Ran it without `--only`; it renders every beat with a Remotion pattern |
| No LaTeX for Manim `MathTex` | Used matplotlib mathtext → SVG (the toolkit's own `typeset_math.py` approach) loaded into Manim |

## 2026-09-26/27 · Watch and revise (review record) [session log]

Frame-level checks of the first renders found these, each fixed and re-rendered:

1. **B01 (hesitant writer):** at 9.5 s of a 9.9 s beat the correction "nudges the answer slightly →
   changes the weights, not the answer" had not appeared yet, so the beat's point never landed. Fix: faster typing
   (`charMs 50→26`, `mistakeRate 10→0`).
2. **B00 / BHTF composer** showed a "Fable 5 · High" model chip. That implies a real Claude session with a
   specific model, and there wasn't one. Fix: relabelled to "Mock composer · not a real session". B00's
   running line says "no Claude reply shown · program output below", and the only "output" is the real
   `python main.py` line.
3. **Math rendered as black rectangles** (matplotlib's SVG background patch got filled). Fixed by
   dropping the patch in `M()`.
4. The spark glyph "✱" rendered as tofu boxes (EB Garamond lacks it), so it's now drawn with lines.
5. Tags and error lines ran past the frame edge in B02/B04/B05, and labels collided in B04/B06. Fixed with a smaller type scale and
   a centered `labeled()` helper.
6. **Honesty catch:** B04 had a label "largest float ≈ 1.8e+308" that I typed in myself; it wasn't in
   `evidence.json`. Removed it, since only printed numbers go on screen.
7. **Date drift:** narration originally said "printed by Python on September twenty-sixth", but the
   render re-ran `evidence.py` after midnight, so the footer read 2026-09-27. Changed the narration to
   not state a date; the footer shows whatever date the numbers were actually printed.

8. **`./art final` blocked by GATE T (type check), 2026-09-27 00:23.** 5 beats failed: terracotta
   accent *text* `#D97757` on cream is below WCAG 4.5:1, footer text was 19 px (floor 20 px), math
   sub/superscripts were 8–9 px in B03/B06, and one text run sat outside title-safe in B03. Fixed
   by using `#B4532F` (4.72:1) for accent text and `#8C3B24` (7.21:1) for errors, keeping `#D97757` only for drawn
   marks; footer to 24; larger math; ratio block moved inward. I didn't bypass the gate.
9. **Frame gate (GATE V) failures, 2026-09-27 00:3x–01:0x:** heading and footer crossed the 96 px
   title-safe edge; footer and name bug overlapped (the gate did **not** catch this; I found it on
   the contact sheet); the name bug then collided with long headings, so it was removed from body
   beats (the author is still named in B00, the composer chips and the outro); B01/outro underfilled
   the frame. All fixed; GATE V ended at 0 BLOCKER / 0 MAJOR.
10. **B01 never corrected itself.** The contact sheet showed B01 ending on the misconception ("It
    nudges the answer slightly"). Cause: `BrutalistHesitantWriter` matches `triggerWords` one
    whitespace token at a time, so a multi-word trigger never fires, and `replacementWords` is split on
    commas. Fix: text "It changes the answer." with trigger `answer` → "weights but not the answer".
    Verified on frames: the word is highlighted, deleted and replaced before the cut.
11. **GATE T kerning check left failing, by decision (2026-09-27, Siddi chose this option).** §8.4 measures
    the single densest row of dark ink and fails if ≥30% of the gaps are wide. After the layout fixes,
    that row was a heading's word spaces (B02), monospace number rows like `[1001, 1002, 1003]`
    (B03–B05) or the 130 px outro title. Crops of the exact rows it measured are in
    `_qc/kerning-false-positive.png`; the glyphs are shaped correctly by the named fonts (the bug §8.4 is meant to catch is
    Pango falling back to a system font). So the final was built with the toolkit's own `compile.py`
    (the command `./art final` runs after GATE T), `--height 1080 --fps 30`, with **GATE V still
    enforced** (it passed). `TYPECHECK.md` is kept, showing the FAILs.
12. **Build-record bug I caused.** A background `remotion_scenes.py` run I'd started earlier wrote its
    stale copy of `beat_sheet.json` over my B00 edit (narration text and output line reverted; audio
    had already been regenerated with the new text). Found by checking the master frame; confirmed the
    audio by transcribing `mp3/beat-B00.mp3` with faster-whisper; reapplied the edit with nothing else running,
    re-rendered B00, and recompiled. Lesson: don't edit the sheet while a toolkit script is running.
- **My own watch of the draft (review/revision record), 2026-09-27:**
  - **0:00–0:15 (B00, opening shot):** everything was fine except the greeting, "Namaste, Siddi".
    I asked for just "Namaste". Changed the `greeting` prop in `beat_sheet.json`; only B00 was re-rendered
    (narration and timing unchanged), then the master was recompiled; verified on the frame at 0:08.
  - **[Siddi]** _(rest of the video: add any further timestamps you checked, or note that you watched
    it through and had no other changes)_

## What Claude contributed / what I accepted or changed [session log]

- Claude: concept recommendation, evidence script, beat sheet and narration draft, Manim scenes, all
  install and debugging work above, and the draft of these documents.
- **Decisions I made (2026-09-26/27, in the session):**
  - Chose the concept, max-subtraction, from four options Claude offered. I accepted its recommendation.
  - Chose to submit as **Siddi Kommuri** (my git identity says "Suhas Kommuri").
  - Supplied the course repo, which is what made it possible to use the real `main.py` instead of a
    reconstruction from the chapter text.
  - When GATE T's kerning check kept failing, chose to **build the final anyway and log why**
    (#11) rather than keep redesigning around the check.
  - Chose to push one complete commit instead of a partial one. Then, when the course repo's
    `.gitignore` turned out to keep video out of Git, chose to **follow that rule**: MP4 on Canvas,
    SHA-256 in the README. The alternative was force-adding it as some classmates did.
  - Asked Claude to commit; it declined to commit into the home-directory repo (which would have
    included private files) and made a standalone repo instead. I accepted that.
- **Accepted as drafted:** the narration and beat sheet. I didn't request wording changes in the
  session.
- **Rejected / not used:** the toolkit's default "Liam, in for Bear" persona and @NikBearBrown branding
  (not mine to use on a student submission).
- **[Siddi]** What I still don't fully understand: _(e.g. why exactly exp(−745) is the last nonzero
  double, since it's a subnormal; or why Python raises OverflowError while NumPy returns inf)_

## Learning and next step [Siddi]

- _(What changed in your understanding: e.g. the difference between an algebraic identity and a
  floating-point result.)_
- Next question: _(e.g. does log-softmax / log-sum-exp avoid the underflow that this doesn't?)_
