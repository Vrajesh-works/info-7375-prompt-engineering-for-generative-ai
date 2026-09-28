# FRICTIONAL — Week 1 video (max subtraction)

Omkar Salian · INFO 7375 Fall 2026 · Week 1 explainer video

> **Who wrote what.** Entries 1–4c were drafted by Claude Code during the build sessions (2026-09-24 to 2026-09-27), from what actually happened in those sessions (commands, errors and outputs are all preserved in this folder). They describe Claude's actions on my request. Entry 5 is my own review, written by me after watching the video.

---

## Entry 1 — 2026-09-24 · setting up, finding the evidence

**I tried / expected:** I asked Claude Code to complete the Week 1 video assignment end to end, without pushing to GitHub. I expected the course's `main.py` to already be on my machine and the Brutalist setup to be one command.

**What happened:** `lessons/01-randomness-and-first-prompts` was not on disk. Of Professor Bear's five INFO 7375 repos, only `info-7375-prompt-engineering-for-generative-ai` returned the lesson folder (checked through the GitHub contents API), so we cloned that one at commit `e6c6c49`. `fall-2026/omkar-s/` already existed there, holding only a README.

**What I did:** We ran `python3 main.py` and the six lesson tests, then saved both outputs verbatim (`evidence/main_py_output.txt`, `evidence/tests_output.txt`). The printed probabilities (0.09003…, 0.24472…, 0.66524…) and counts (102/268/630) match Chapter 1's tables.

**What Claude or another person contributed:** Claude located the repo, cloned it, and ran and saved everything. I chose nothing yet.

**What I understand now / still do not understand:** The chapter's numbers are reproducible on Python 3.14.2. I have not checked other Python versions.

**Evidence and next step:** `evidence/course-commit.txt`, `evidence/*_output.txt`. Next: pick one concept.

---

## Entry 2 — 2026-09-24 · choosing the concept, and a correction

**I tried / expected:** We chose "why subtracting the maximum changes the intermediates but not the distribution," because every number in it can come from running code, and it has a real failure to show (overflow) instead of a made-up one.

**What happened:** `evidence/max_shift_evidence.py` imports the course's own `probabilities()` and compares it with a naive softmax. Three things surprised us:
- (a) For [1, 2, 3] the naive and shifted results are **not bit-identical**: 0.09003057317038045 vs 0.09003057317038046.
- (b) `math.exp(1003)` raises `OverflowError: math range error`, while the shifted route returns exactly the [1, 2, 3] probabilities (`A == B exactly: True`).
- (c) [0, −1000] returns exactly `0.0` for a probability that is mathematically positive (e^−1000 ≈ 10^−434, below the smallest float 5e−324).

**What I did:** We turned (a) into its own beat (B06), so the video claims "same up to rounding" instead of "identical." We used (c) as the one thing the explanation does not establish (B07). The first draft said the numbers differ in the "17th" significant digit. Counting showed 16 digits, so the narration and label were corrected to "16th" (FACTCHECK row 16).

**What Claude or another person contributed:** Claude proposed the concept, wrote the evidence script, and caught and fixed its own digit-count error before rendering.

**What I understand now / still do not understand:** Max-subtraction guards the largest weight against overflow. It does nothing about underflow of tiny weights. Still open: whether a log-softmax formulation would keep that e^−1000 as a finite log-probability. I have not tested that.

**Evidence and next step:** `evidence/max_shift_evidence.py`, `evidence/max_shift_output.txt`, `FACTCHECK.md`.

---

## Entry 3 — 2026-09-24 · the Brutalist toolkit on this Mac

**I tried / expected:** Following `prerequisites/brutalist-video.md`: clone `brutalist.art` (commit `6a8380a`), create a venv, run `./setup --install`.

**What happened (in order):**
1. `ffmpeg` was missing, so we ran `brew install ffmpeg cairo pkg-config`.
2. System Python is 3.14, where Manim 0.18 will not build, so we made a Python 3.12 venv with `uv venv --python 3.12 .venv`.
3. `./setup --install` reported success for npm, fonts, and the 340 MB Kokoro model, but the Python packages were not actually installed. Setup then **exited on its own ElevenLabs guard**, flagging ten files inside the toolkit's own `youtube/brutalist/` folder, before it could print a readiness table.
4. Installing the requirements directly failed: `manimpango` needed `pangocairo`. We ran `brew install pango` and retried, and it installed. Kokoro smoke synthesis: `mean_volume -21.8 dB`, OK.
5. `./art smoke` failed immediately: `metadata.slug must be a filename, not a path`. The toolkit's own fixture slug `_smoke` breaks its own slug regex (`[A-Za-z0-9][A-Za-z0-9._-]*`, `runtime/scripts/build_safety.py:186`). Our slug does not start with `_`, so this does not affect us. We did not patch the toolkit.
6. There is no LaTeX (installing it needs an admin password), so there are no Manim equation beats. The course guide advises avoiding them for a first video anyway. The cancellation is shown with real numbers instead of typeset algebra.

**What I did:** We worked around each problem as listed and recorded it here instead of hiding it.

**What Claude or another person contributed:** Claude diagnosed each failure and chose each fix. The Homebrew installs changed my machine: ffmpeg, cairo, pkg-config, pango.

**What I understand now / still do not understand:** A green setup table would not have proved a render works. Here, setup could not even produce the table. I do not know whether the ElevenLabs-guard failure is a known upstream issue.

**Evidence and next step:** Commands are in `BUILD-PROMPT.md`.

---

## Entry 4 — 2026-09-24 · building, gates, and deviations

**I tried / expected:** We used the `ai-explainer` builder's pipeline: audio first, one Manim scene per beat, `./art run`, then `./art final`.

**What happened:**
- **Deliberate deviation:** `ai-explainer` requires a reconstructed Claude-app cold open whose "ask lands answered," plus a "Liam, in for Bear" narrator and an @NikBearBrown chip. The assignment forbids showing any Claude response that is not a real, dated one, and the prerequisite forbids implying the narrator is Bear. We dropped those bookends and kept the pipeline: Kokoro `af_bella` audio as the clock, Manim beats, `compile.py`, and the QC gates.
- Narration measured 193.95 s over 9 beats (`mp3/timings.json`).
- The first `./art run` stopped at GATE A. Two causes:
  - Our scenes used Manim's `NORMAL`/`BOLD` constants, which the gate's stand-in doesn't define. We replaced them with the literal strings.
  - The gate copies `scenes.py` alone into a temp folder, so it could not find `beat_sheet.json`. We added a fallback.
- After those fixes, three scenes still "failed" GATE A for reasons in the stand-in, not the scenes: its `NumberLine` returns empty coordinates, and a "shapes never change" heuristic is written for a different genre of video.
- We then ran the real, rendering layout audit (GATE B, `manim_layout_audit.py --curve-strict`) on every scene. It found actual defects, and we fixed all of them:
  - weights stacked on top of each other while flying into the total (B01, B02)
  - strike-through lines drawn over text (B03)
  - `÷` labels crossing the divider (B03)
  - text outside the safe area (B00, B04, B07, B08)
  - boxes touching digits (B06)
- All nine scenes ended clean on GATE B and GATE W.
- We pre-rendered each beat at 1920×1080 with `run.sh`'s own Manim command and placed it in `manim/`. `run.sh` then skips the stand-in gate for filled slots, and still compiles and runs GATE V (frame-level QC).
- The course guide asks for a 1080p master, so beats were rendered at 1080p, not the toolkit's 4K default.

**What Claude or another person contributed:** Claude wrote the beat sheet, all narration, `scenes.py`, and the paperwork, then ran and fixed every gate. Claude inspected contact sheets of rendered frames, but it cannot hear the audio or judge whether the video teaches.

**What I understand now / still do not understand:** Claude cannot hear the audio or judge pacing; that needs a person watching the video.

**Evidence and next step:** `beat_sheet.json`, `scenes.py`, `FACTCHECK.md`, `_qc/` (from `./art run`), `BUILD-PROMPT.md`.

---

## Entry 4b — 2026-09-24 into 2026-09-25 · visual QC and type check

**I tried / expected:** After Gate B was clean, we expected `./art run` and `./art final` to pass.

**What happened:**
- **GATE V round 1** (frame-level QC on the compiled cut) flagged 5 "underfill" frames: B03, B04, B05, B06 and B08 were mostly empty at the 50% or 85% sample points. Looking at the contact sheet showed a worse, real defect the gate had not named: in B03 the `÷ 20.085537` arrows ran straight through the dimmed probability and score columns, striking out `0.0900` and "total."
- **GATE V fixes:**
  - Cleared the arrow path in B03 (faded those columns out) and enlarged its fraction.
  - Brought the reference elements in at the start of their beats: the axis in B04, the test assertion in B05, the evidence caption in B06, and the sources card in B08.
  - B03 at 85% was still underfilled, so the two check-divisions now appear with the fraction.
  - Result: GATE V 0 blockers, 0 majors.
- **GATE T** (type check, runs before `./art final`) then failed three beats. Cropping the flagged blobs showed three causes:
  - the `^` carets in B07's `10^-400` labels (tiny separate blobs)
  - pieces of Menlo's slashed zero in B06's giant numbers
  - green text (`#2F6B4F`) that the checker's text mask only partly matched, so it broke into sub-floor fragments
  - B04's contrast fail was the light-terracotta tag border read as text.
- **GATE T fixes:**
  - B07 now uses Python notation `1e-400` and `exp(-1000) is about 5.1e-435` (a first version wrote "=" for this rounded value; corrected). The value was checked with `decimal`: 5.07596e−435. Narration is unchanged ("about ten to the minus 434").
  - B06's numbers now use Helvetica Neue.
  - All green text is now ink on a pale green plate.
  - The tag border is darker.
  - Result: GATE T PASS.
- **GATE V round 2** then flagged B06 low contrast: the big pale plate behind the numbers lowered the frame's measured ink separation. We replaced it with a thin green underline plus an ink label, "these digits agree."

**What Claude or another person contributed:** Claude read the reports, cropped and magnified the flagged regions to find the actual glyphs, and made every fix in the scene source. No gate was loosened, no threshold edited, and `ART_STRICT` was never turned off.

**What I understand now / still do not understand:** The gates caught one real teaching defect: the strike-through in B03 would have made "0.0900" look wrong. The rest was mostly typography. I have not judged pacing or audio. Only a person watching can.

**Evidence and next step:** `_qc/REPORT.md`, `TYPECHECK.md`, `qc-sheet.png` (in the working reel folder, not committed); the diff history of `scenes.py`.

---

## Entry 4c — 2026-09-27 · swapped commit hashes

**What happened:** Before submitting, I asked whether the assignment was complete. Claude re-checked `git rev-parse HEAD` in both checkouts and found that every document and two on-screen captions (B00, B08) had the course repo and Brutalist commits **swapped**. The saved files `evidence/course-commit.txt` (`e6c6c49`) and `evidence/brutalist-commit.txt` (`6a8380a`) were always correct. The error came from reading them back with `cat *commit.txt`, which prints them in alphabetical order (brutalist first), and then pairing them in the wrong order.

**What I did:** Claude swapped the hashes in README, SOURCES, FACTCHECK, FRICTIONAL, BUILD-PROMPT, `beat_sheet.json` and `scenes.py`, then re-rendered B00 and B08 and re-exported the video. Correct pairing: course `e6c6c49`, Brutalist `6a8380a`.

**What I understand now:** A provenance value is only as good as the step that copied it. The next check is to compare every hash in the docs against `git rev-parse` directly, not against a transcript of it.

---

## Entry 5 — 2026-09-27 · my review and decisions

**I tried / expected:** I asked Claude Code to complete the whole assignment for me and told it not to push anything to GitHub. I expected that once it said "done", the assignment was ready to submit.

**What happened:** When I asked, "Is my assignment complete?", it said no. Checking that led Claude to re-run `git rev-parse` and find that the course and Brutalist commit hashes were swapped in every document and in two on-screen captions (entry 4c). I would not have caught that myself.

**What I did:** I had Claude fix the hashes and re-export the video. I kept control of git: I told Claude not to commit or push anything until I said so. I checked where the submission belongs (`fall-2026/omkar-s/week-01-video/` in the course repo, where my account has push access) before deciding to push.

**I watched the full video with sound on:** yes, on 2026-09-27.

**One thing I noticed:** Nothing needed fixing. I checked the pacing, the pronunciation, and that each number shows up on screen when it's spoken.

**Can I explain every claim?** Yes.

**What Claude or another person contributed:** Claude chose the concept, wrote the evidence script, narration, scenes, and all the paperwork, and did the whole build and QC. I accepted the concept and the numbers. My contributions were the decisions about checking completeness, git, and submission.

**What I understand now / still do not understand:** The main idea: subtracting the max divides every weight and the total by the same factor, so the probabilities don't change, but it only protects against overflow, not underflow. Nothing is still open for me on this topic.

**Evidence and next step:** entry 4c, `FACTCHECK.md`, `evidence/max_shift_output.txt`. Next: commit and push `fall-2026/omkar-s/week-01-video/`, then put the folder link and commit hash in Canvas.
