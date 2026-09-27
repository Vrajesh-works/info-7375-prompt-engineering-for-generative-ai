# FRICTIONAL — INFO 7375, Week 01 video

Akshit Verma · *What pretraining actually targets (the token that followed, not the truth)*

> **Drafting note (Claude Code, 2026-09-27).** At Akshit's request, Claude organized this
> log from the session's own record — the commands run, their outputs, and the requests
> Akshit made. Every entry is retrospective. Facts below are attributed: **"I"** means
> Akshit; Claude's work is labelled as Claude's. The log records what happened and who did
> what. It does not record Akshit's predictions or reflections: the course policy allows AI
> to organize effort notes but not to supply predictions, understanding, or approvals.
> An earlier draft of this file, written by Claude in Akshit's voice, did not meet that rule
> and was replaced (see Entry 6).

---

## Entry 1 — 2026-09-26 (retrospective, organized 2026-09-27): installing brutalist.art on Windows

**I tried / expected:** I asked Claude to clone `github.com/nikbearbrown/brutalist.art` and run
`./setup -- install`, then report which features were green or red.

**What happened:**
- `-- install` (two tokens) installed nothing: `setup:57` only matches the single token `--install`.
- After `./setup --install`, `./setup` exited 1 and printed **no** readiness table. Its ElevenLabs
  guard (`setup:106`) matched 10 files of the toolkit's own documentation under `youtube/`.
- `./art smoke` then failed three different ways: fixture slug `_smoke` rejected by
  `build_safety.py:186`; ffmpeg's filtergraph broke on the Windows font path
  (`No option name near 'UsersAkshit VermaPromptEngr…'`); a `'charmap'` codec error on `→` when
  output was redirected to a file.

**What I did:** asked for the guard fix and the smoke test. When Claude offered the toolkit's two
documented fixes for the slug bug, I chose renaming the fixture over widening the safety regex. I
asked what exactly the ffmpeg bug was, and whether it was the only change required, before approving
it — and asked for no major changes.

**What Claude contributed:** diagnosed each failure; tested four ffmpeg escaping forms against real
ffmpeg (its first proposed escape did not work); wrote the four fixes; identified the charmap error
as output redirection rather than a code bug (fixed with `PYTHONUTF8=1`).
Accepted: all four fixes.

**Evidence and next step:** `toolkit-changes/toolkit.patch` (applies cleanly to `6a8380ae`). The
repaired smoke test produced a 13.88 s mp4 at `mean_volume −24.2 dB`, matching the toolkit's own
published reference run.

---

## Entry 2 — 2026-09-26 (retrospective): practice reel, not submitted

**I tried / expected:** a 60-second, 12-beat practice explainer on how ribosomes read mRNA.

**What happened:** Claude reported that 60 s and 12 beats were incompatible with the toolkit's
45–70-word body-beat rule, and I chose 12 beats (2m33s). All 12 scenes then failed with
`WinError 2` (`npx` is `npx.CMD` on Windows). After watching, I asked for beat 5's narration to be
cut to 20 words.

**What I did:** chose the runtime trade-off; requested the beat-5 cut.

**What Claude contributed:** the `npx` fix in `remotion_scenes.py`, the reel itself, and a frame
check that found the ribosome body drawn over the tape it was reading — a defect the automated gate
did not report.

**Evidence and next step:** `youtube/brutalist/claude-liam-how-ribosomes-read-mrna/` (practice only;
not part of this submission).

---

## Entry 3 — 2026-09-27 (retrospective): choosing the concept, first cut

**I tried / expected:** I chose *What pretraining actually targets* from the Part 1 list, gave
Claude the assignment text, and set the constraints: 12 beats, Kokoro `am_onyx`, 2–4 minutes, stop
at the review cut, nothing pushed to GitHub without my permission.

**What happened:** no existing scene could show a distribution being fitted. Claude proposed the
demonstration — a **constructed** corpus in which the frequent answer is false (sydney ×7,
canberra ×3) — wrote `code/pretraining_target.py`, and ran it: converged to 0.6989 / 0.2989 /
0.0022, which is 0.0022 from the corpus frequencies and 0.7011 from the truth. Claude flagged that the
toolkit's outro scene hardcodes `@NikBearBrown` and built an author-credit outro instead. First cut: 2:52.

**What I did:** accepted the constructed-corpus approach and the outro change.

**What Claude contributed:** the demonstration design, the script, the narration, the scene
components, and first drafts of every document. **Process gap:** the course video guide asks Claude
to show narration and evidence *before* building and wait for review. Here it built first, and I
reviewed the rendered cut.

**Evidence and next step:** `code/OUTPUT.txt`, `beat_sheet.json`.

---

## Entry 4 — 2026-09-27 (retrospective): first watch — overlapping text in B03

**I tried / expected:** watched the review cut.

**What happened:** at **00:00:52.8** (B03) the `CONSTRUCTED` banner overlapped the title line above
it. I sent Claude a screenshot. Claude had sampled B03 earlier and missed it; the automated QC gate —
24 BLOCKERs, every one a false positive from the timecode overlay — missed it too.

**What I did:** asked for a fix. The banner moved from `top: 66` to `top: 120`.

**What Claude contributed:** measured the cause (the title line runs to y≈100) and checked that no
other scene in the file had the same collision.

**Evidence and next step:** `_qc/REPORT.md` (defect table); `REVIEW-LOG.md`.

---

## Entry 5 — 2026-09-27 (retrospective): watch and revise — six changes

**I tried / expected:** after watching, I asked for: a student greeting in B00 and removal of its
"reading chapter 1" line; audio/video sync in B02 ("audio is fast while video is taking time to match
that speed"); smoother, more visual transitions in B05; a correctly built graph in B07; an author
credit in B11; captions throughout; and removal of the per-frame footer.

**What happened:**
- Measured against word timings, B02's step 4 trailed the voice by **2.56 s**. Every custom scene had
  used evenly spaced timings rather than the narration's actual pace.
- B07 plotted 6 points on an x-axis that spaced steps 0, 1, 5, 20, 100, 600 **evenly**, with no y ticks.
- While fixing sync, Claude found that B01's correction had **never fired**: a multi-word trigger can't
  match the component's one-word comparison, so the summary beat displayed *"Training teaches a model
  what is true"* — the claim the video argues against.

**What I did:** approved the full revision.

**What Claude contributed:** word-level cues from `align.py`; B05 and B07 rebuilt on the full
601-step run (`code/trajectory.json`); the B01 fix, timed to land on the spoken "followed"; a native
B08 scene; the caption builder; the `ART_BURNIN=0` switch. Its frame check then found three more label
collisions (B05, B07), fixed before this cut.

**Evidence and next step:** `mp3/words.json`, `code/trajectory.json`, `REVIEW-LOG.md`.

---

## Entry 6 — 2026-09-27 (retrospective): checking the submission against the rules

**I tried / expected:** asked Claude to re-check the video and files against every assignment
constraint.

**What happened:** Claude read the course's Frictional guide, AI-disclosure page, and prerequisites
for the first time, and found:
- B00 and B10 showed a Claude-styled prompt box with reply-like lines and a model chip — unlabelled,
  and not a real Claude exchange;
- the synthetic narrator said *"This is Akshit Verma"*, with no synthetic-voice disclosure;
- numbers were stamped "measured" although computed on the constructed corpus;
- the video was 4K, where the course guide specifies a 1080p master;
- **this log and SOURCES.md §5 had been drafted by Claude in my voice**, crediting me with checks
  that Claude performed;
- `main.py` was never documented. Run on 2026-09-27, it prints softmax `[0.0900, 0.2447, 0.6652]`
  and sample counts `{0: 102, 1: 268, 2: 630}` — Part 2 material with no numbers about the
  pretraining objective;
- no toolkit revision was recorded, and the folder could not rebuild on its own.

**What I did:** chose to fix all of it, and to keep B08 (preference tuning) with a written
justification rather than cut it.

**What Claude contributed:** the audit, the on-screen fixes, the toolkit patch, and this restructured
log.

**Evidence and next step:** `toolkit-changes/`; `SOURCES.md` (main.py, contributions, disclosures).
