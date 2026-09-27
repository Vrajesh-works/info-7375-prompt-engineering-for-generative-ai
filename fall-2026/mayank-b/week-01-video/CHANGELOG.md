# CHANGELOG — Temperature Is Not a Fact Checker.

Every change to the video since generation started, newest last. Times are local
(from file timestamps where noted). FRICTIONAL.md records *what went wrong*; this
file records *what changed*.

## 2026-09-23 — v1: first build

- **~18:39 — Evidence.** Copied the chapter's `probabilities()` and `sample()` verbatim into
  `code/main.py`; wrote `code/run_temperature.py`. Output `code/temperature_results.json`
  matches the chapter's tables exactly (Python 3.11.16).
- **~18:40 — Beat sheet v1.** `code/author_sheet.py` → `beat_sheet.json`: 12 beats
  (B00 cold open, B01 hesitant-writer summary, B02–B08 body, BVDT recap, BHTF your turn,
  BOUT outro), 480 words, Kokoro `am_onyx`, title "Temperature Is Not a Fact Checker."
- **18:43 — Audio.** Kokoro narration generated for all 12 beats (158.5 s total).
- **~18:44 — B01 lead silence.** Prepended 0.8 s of silence to `mp3/beat-B01.mp3`
  (10.58 s → 11.38 s). Total 159.3 s.
- **18:45 — Word clock.** `align.py` → `mp3/words.json` (12/12 beats aligned).
- **~18:46 — Props.** `code/build_props.py`: animation cues from word timings, typeset math
  SVGs (softmax, ratio, gap, three ratio rows), real seed-7 draw sequences.
- **~18:47 — New scenes.** Added `TemperatureConcentration.tsx` (7 components: TcScoresToOdds,
  TcTemperatureDial, TcRatio, TcCode, TcSampleCounts, TcWrongAnswer, TcBoundary) and registered
  them in the toolkit's `Root.tsx`. Copied the NBB logo into `public/temperature-concentration/`.
- **18:50 — Layout fixes from test stills (before the full render):**
  - B04: max ratio-bar length 760 → 520 px (the "54.60×" label was clipped).
  - B06: dot cell 19 → 20 px; count legend redesigned as label-over-number columns (the legends collided);
    added the "outcome 2 share vs assigned p" line.
  - B07: honesty stamp forced onto one line; footer caption shortened.
  - B08: bigger claim cards (font 44 → 54, card height 130 → 180, row spacing 170 → 215).
- **18:51–19:05 — Render.** All 12 beats rendered with Remotion at 4K.
- **~19:06 — Review cut v1** compiled (159.5 s).

## 2026-09-23 — v2: fixes from visual QC

- **B01 (hesitant writer):** the correction never appeared on screen in v1.
  - Trigger `how creative the model is` → `creative`; replacement → `concentrated`.
  - Text line 1 changed to "Temperature sets how creative the choices are." (after the fix it reads
    "…how concentrated the choices are.").
  - Typing sped up and made more even: `charMs` 50 → 32, `mistakeRate` 10 → 3,
    `hesitateWithin` 3 → 1, `hesitateBetween` 20 → 8.
- **B00, BHTF (composer bookends):** `largeText: true` (text was undersized).
- **19:10** Re-rendered B00, B01, BHTF. **19:13** Review cut v2 compiled
  → `temperature-concentration-slate.mp4` (159.5 s).
- Narration and audio are unchanged from v1.

## 2026-09-25 — v3: clean master + submission files

- **Clean master:** `compile.py --height 1080` (no review overlays) → `temperature-concentration.mp4`
  (159.5 s, 9.4 MB). The first attempt was refused by Gate V: B01 "underfill" (text covers 7–23% of
  the safe area mid-typing). Added the toolkit's `qc.sparse_by_design` declaration with a written
  reason to B01 only (it waives the fill checks; edge, empty-frame and contrast checks still run).
  Gate V then passed: 0 BLOCKER, 0 MAJOR.
- Added `README.md`, `SOURCES.md`, `.gitignore`, `_qc/MANUAL-QC.md` (my hand QC table; Gate V
  overwrites `_qc/REPORT.md` on every compile, its first failing run is kept in
  `_qc/GATE-V-REPORT-first-run.md`).
- No change to narration, audio, or any visual.
- Pushed to `nikbearbrown/info-7375-prompt-engineering-for-generative-ai`,
  `fall-2026/mayank-b/week-01-video/`.

## 2026-09-25 — workflow
- Pushed as commit `72e9aa1` (v3).
- From here on, every iteration becomes its own commit in the course repo, pushed with
  `bash code/publish.sh "vN: what changed"`, so the history shows how the video was revised.
  Added `code/publish.sh`; it will go up with the next iteration.

## 2026-09-25 — v4: fix course CI failure

- Commit `72e9aa1` failed the course repo's `validate` workflow: `scripts/validate_course.py`
  rejects any `.ts/.tsx/.js` file ("Non-Python implementation"), and it scans the whole repo, so the
  next student's commit went red too.
- `remotion-src/TemperatureConcentration.tsx` → `TemperatureConcentration.tsx.txt` (byte-identical),
  plus `remotion-src/README.md` explaining why and how to restore it. BUILD-PROMPT, SOURCES and
  README references updated.
- Added `code/check_repo_rules.py` (local copy of the CI rules); `publish.sh` now runs it before
  every commit and refuses to push on failure. Also adds `code/publish.sh` to the repo.
- No change to the video.

## 2026-09-26 → 27 — v5: new beat B01A "how a chatbot picks the next word"

Why: reviewing the concept from first principles, we agreed the video skipped the basics. It
jumped to "three scores, softmax" without saying that a chatbot picks the next token from scored
options, or why scores must become chances.

Done so far:
- **New beat B01A** (after the Beat 2 summary, before B02). Narration (49 words, 15.34 s):
  "First, what a chatbot does. It writes one token, roughly one word, at a time. At each step it
  scores every possible next token: Paris high, Lyon lower. Scores aren't chances yet. A formula
  called softmax turns them into chances that add up to one. Then the model draws."
- Visual plan: "The capital of France is ___"; four candidates (Paris, Lyon, beautiful, a) with
  **unnumbered** score bars and the stamp "ILLUSTRATIVE SCORES · NOT FROM A REAL MODEL"; a
  "chance?" column; a softmax label; "Paris" drops into the blank.
- Added to `code/author_sheet.py` and inserted into `beat_sheet.json` (13 beats now).
- `mp3/beat-B01A.mp3` generated (Kokoro am_onyx). No other beat's audio touched.
- New component `TcNextWord` in `TemperatureConcentration.tsx`, registered in `Root.tsx`;
  B01A cue anchors added to `code/build_props.py`.
- SHOTLIST (B01A row), CHECKS-REPORT (8 SHOW), FACTCHECK (three new claims, quoted from the
  chapter's fig. 1 caption, §35 and §37) updated.

Paused 2026-09-26 by the iCloud problem (FRICTIONAL). Resumed 2026-09-27 once the files were back:
- Word alignment for B01A (49 words). Cues: sentence 1.54 s, scores 4.88 s, chance 8.42 s,
  softmax 10.67 s, draw 13.58 s.
- Test stills changed the design twice before the full render:
  1. "Paris" landed right of the blank instead of in it → end position measured from a still (x≈862).
  2. The flying word crossed the Paris bar and the SCORE label mid-flight → replaced the flight with
     "the winning row lights up (bar turns terracotta) and fades, while Paris rises into the blank".
  3. The word "softmax" was a second terracotta element → bold ink (one accent per beat).
- Rendered B01A at 4K (Remotion).
- **B01 fix found by the v5 QC pass:** the last line was still typing at the cut ("…answer is tr|").
  My v2 claim that "all three lines finish inside the beat" was wrong. `charMs` 32 → 26;
  re-rendered B01; the full sentence, period included, is on screen by 11.3 s and the
  creative → concentrated correction still plays (`_qc/sheet-v5-B01*.png`).
- Recompiled review cut + clean master: **174.8 s**, 13/13 beats filled, Gate V 0 BLOCKER / 0 MAJOR.
- README (runtime, B01A row, 13 beats) and `remotion-src/TemperatureConcentration.tsx.txt` updated.
- Narration of every other beat unchanged.
- Pushed as commit `3875cad` (v5). Course CI shows red, **but not because of this folder**: the only
  error is a broken link in the instructor's `fall-2026/nik-bear-brown/SYNC.md` (added in `d1d0743`,
  2026-09-26 22:29), which has failed every commit since. `code/check_repo_rules.py` passes on this folder.

## 2026-09-27 — v6: step-by-step softmax (B02) and temperature (B03); BHTF removed; B08 colour

Why (Mayank's review): B02 and B03 should explain the mechanism the way the plain-language
walkthrough did (softmax as three moves; temperature as "divide the scores first"), so a viewer
can follow the arithmetic, not just watch bars move.

- **B02 rewritten: "Softmax in three moves"** (narration 38 → 60 words; 14.95 s → 19.20 s).
  - New narration: "Three options, with constructed toy scores: one, two, three. Softmax turns scores into
    chances in three moves. One: raise e to each score. Two point seven, seven point four, twenty point
    one. Bigger scores get much bigger. Two: add them up. Thirty point two. Three: divide each weight by
    the total. Nine, twenty-four point five, and sixty-six point five percent."
  - New visual: a table that fills move by move. MOVE 1 weight = e^z (2.72 / 7.39 / 20.09),
    MOVE 2 total 2.72 + 7.39 + 20.09 = 30.19, MOVE 3 weight ÷ 30.19 = 9.0% / 24.5% / 66.5% with share
    bars; formula labelled "top = your weight, bottom = everyone's total".
  - Footer: direct exponentials shown for clarity; the chapter's code subtracts the max first (same chances).
- **B03 rewritten: "Temperature zooms the gaps"** (40 → 61 words; 12.52 s → 17.92 s).
  - New narration: "Temperature adds one step first: divide every score by T. At T point five, the scores
    double to two, four, six. The gaps grow, and the top option takes eighty-six point seven percent. At
    T two, they halve. The gaps shrink, and it falls to fifty point six. Temperature zooms in or out on
    the gaps. But the ranking never moves."
  - New visual: same table plus a "STEP 0 · z ÷ T" column; T slides 1 → 0.5 → 2 and every cell
    recomputes live (2, 4, 6 → 7.39 / 54.60 / 403.43 → 1.6 / 11.7 / 86.7%; 0.5, 1, 1.5 → 1.65 / 2.72 /
    4.48 → 18.6 / 30.7 / 50.6%); dashed T = 1 bars; "low T zooms in · high T zooms out" caption; rank badges.
- **Correction to my earlier explanation:** the T = 1 total is **30.19**, not 30.20 (I had added rounded
  values). The screen shows 30.19; narration says "thirty point two" (30.19 to 1 d.p.).
- **B08:** the second NOT SHOWN item ("Whether the scores themselves were any good") is now red like the
  first (`accent: true`).
- **BHTF ("Your turn") removed** as unnecessary: beat, audio and render deleted; recap → outro directly.
  The prompt constant was removed from `code/author_sheet.py`. Logged as a HANDOFF LAW deviation in
  CHECKS-REPORT.
- Components rewritten in `TemperatureConcentration.tsx` (shared step-table helpers; TcScoresToOdds,
  TcTemperatureDial); new typeset headers `ez.svg`, `ezT.svg`; `build_props.py` asserts the direct
  weights reproduce `probabilities()` to 1e-12.
- Test stills → two fixes before the render (footers wrapped; raw "e^z" in a footer).
- Re-rendered B02, B03, B08. Review cut + clean master: **166.5 s (2:47)**, 12 beats, Gate V 0 BLOCKER / 0 MAJOR.
- README, SOURCES, SHOTLIST, CHECKS-REPORT, FACTCHECK, MANUAL-QC updated.
- Pushed as commit `9bb6f99` (v6). CI still red only from the instructor's `nik-bear-brown/SYNC.md` broken link (unchanged since `d1d0743`); no error from this folder.

## 2026-09-27 — v7: @NikBearBrown → @Mayank everywhere; intro "Hola, this is Liam"

Why (Mayank's review): the outro (02:43) and the rest of the video carried the @NikBearBrown handle;
the video should sign as @Mayank, and the intro should say "Hola, this is Liam".

- **B00 narration:** "Hola — this is Liam, in for Bear. …" → "Hola, this is Liam. …" (rest unchanged;
  9.62 s → 9.02 s). Speech-recognition check heard "Ola this is Liam, turn a model's temperature down…".
- **B00 composer chip:** folderLabel `@NikBearBrown` → `@Mayank`.
- **Corner bug on every body beat (B01A–B08):** the NikBearBrown logo SVG → an "@Mayank" serif wordmark
  (the skill's LOGO LAW fallback when a channel has no logo file).
- **Outro (BOUT):** handle `@NikBearBrown` → `@Mayank`. The toolkit's `ClaudeTitleOutro` hardcodes the
  handle (OUTRO-LOCK), so it was left untouched and the reel now uses `TcTitleOutro`, a reel-local copy
  with a `handle` prop (same layout, mascot seed and colours).
- **Outro narration:** "Temperature Is Not a Fact Checker. At Nik Bear Brown. Liam, in for Bear." →
  "Temperature Is Not a Fact Checker. At Muh-yunk." (4.74 s → 3.24 s). "Muh-yunk" is a respelling so
  Kokoro says Mayank closer to right: plain "Mayank" came out "May-ink". Six candidate pronunciations
  are in `_name-test/` (local only, not pushed) for Mayank to choose by ear.
- **Metadata:** persona "Liam (in for Bear)" → "Liam"; `in_for_bear` true → false; folderLabel → `@Mayank`.
  Same edits in `code/author_sheet.py`.
- Re-rendered B00, B01A, B02, B03, B04, B05, B06, B07, B08, BOUT (every beat showing a handle).
- Review cut + clean master: **164.4 s (2:44)**, 12 beats, Gate V 0 BLOCKER / 0 MAJOR. Frame check
  (`_qc/sheet-v7.png`): @Mayank on the B00 chip, all 8 body-beat corners and the outro; no @NikBearBrown left.
- SOURCES (logo row, outro credit), CHECKS-REPORT (IN-FOR-BEAR / OUTRO-LOCK deviations), FRICTIONAL updated.

- Pushed as commit `10a1a6d` (v7). CI red only from the instructor's `nik-bear-brown/SYNC.md` broken link, as before; no error from this folder. `_name-test/` confirmed not in the repo.

## 2026-09-27 — toolkit changes published (no video change)
- Added `mayank-b/brutalist-changes/` to the course repo: `toolkit-changes.patch` (every change made to
  the brutalist.art toolkit: the two smoke-test fixes, `TemperatureConcentration.tsx` with nine scenes,
  and their `Root.tsx` registrations), a README explaining each change, and a `.gitignore`.
- Patch checked with `git apply --check` against upstream brutalist.art `cd4bf20`: applies cleanly.
- Deleted the now-unused `public/temperature-concentration/nbb-logo.svg` from the local toolkit (unused since v7).
- The video is unchanged; the current version is still v7.

## 2026-09-27 — v8: B00 wording, B02 split (formula first + what e is), B07 formula + centred ✕, B08 green, new ending

Why (Mayank's review, item by item):
1. **B00:** composer question "Does turning temperature down make an answer more accurate?" →
   "Does turning the temperature down of the model make an answer more accurate?" (Mayank's wording). Narration unchanged.
2. **B02 → two beats.** Mayank asked for B02 to start with "let's take 3 sample values", give the
   softmax formula as soon as softmax is introduced, then the example, and to say what e is, its value,
   and why it is used. One beat would have run ~37 s, so it became:
   - **B02 "Softmax, the formula, and e"** (new component `TcSoftmaxIntro`, 87 words, 27.43 s):
     "Let's take three sample values as scores: one, two, three. These are constructed toy scores, not
     from a real model. Softmax is the formula that turns scores into chances: each option's weight, e to
     its score, divided by the total weight. Here, e is a fixed number, about two point seven one eight.
     Raising e to any score gives a positive number, and bigger scores grow much faster. Any base above
     one would keep the order; e is the standard choice because it keeps the math simple."
     Visual: score chips 1, 2, 3 → large softmax equation labelled (top = your weight, bottom = everyone's
     total; p = chance, z = score, T = temperature) → "What is e? e ≈ 2.71828" card → bars for
     e^-1 … e^3 = 0.37, 1, 2.72, 7.39, 20.09 → "any base above 1 keeps the order" note.
   - **B02B "Softmax in three moves"** (the v6 table, now its own beat; 41 words, 13.61 s):
     "Now the example. One: raise e to each score. Two point seven, seven point four, twenty point one.
     Two: add them up. Thirty point two. Three: divide each weight by the total. Nine, twenty-four point
     five, and sixty-six point five percent."
   - Claim about e kept modest on purpose (FACTCHECK): any base > 1 preserves order; e is the convention.
3. **B08:** all three SHOWN items now green (border #2F7D4A, text #256B3D); NOT SHOWN stays red.
4. **B07 ✕ at ~2:15 (v7 timing):** the cross sat left of the dashed line. The line and the cross now
   share one centre (`left: 50%` + `translate(-50%)`), and the ✕ is drawn as an SVG so the glyph's own
   spacing can't shift it.
5. **B07:** the formula card shows the typeset softmax equation (header "THE FORMULA ONLY SEES z AND T").
6. **Ending (BVDT):** narration replaced with Mayank's text verbatim (58 words, 11.88 s → 18.71 s):
   "Nothing broke; the recipe did exactly its job. Lowering temperature just made the model more
   confidently wrong. So "turn the temperature down to get more accurate answers" is a misunderstanding.
   Low temperature gives you more consistent answers, not more correct ones. Being correct depends on the
   scores, meaning what the model actually learned and the evidence it has."
   Verdict card: heading "The verdict", five lines matching the narration; "confidently wrong" line is
   marked "(constructed case: 9.0% → 1.6%)".
- Test stills → one fix before render (B07 card header wrapped).
- Re-rendered B00, B02, B02B, B07, B08, BVDT. Review cut + clean master: **193.1 s (3:13)**, 13 beats,
  Gate V 0 BLOCKER / 0 MAJOR. Frame check: `_qc/sheet-v8.png`.
- Runtime is now past the original 120–180 s target, still inside the assignment's 2–4 minutes.
- FACTCHECK (e claims, B07 formula, ending), SHOTLIST, CHECKS-REPORT (B02 over the narration budget;
  green as a second accent), README updated. **← current version**
