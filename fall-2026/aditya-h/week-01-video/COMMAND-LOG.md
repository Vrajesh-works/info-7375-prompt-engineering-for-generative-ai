# Command & friction log: seed-repeatable-not-correct

Raw material for FRICTIONAL.md. Local time (America/New_York). Separate reel from
`softmax-max-subtraction` (that one is finished and untouched). The toolkit docs
(HOW-TO.md, CLAUDE.md, ai-explainer SKILL.md, MATH-TYPESETTING.md,
EXECUTABLE-EVIDENCE.md) were read in full earlier in the same session.

## 2026-09-27: Phase 1 (evidence + beat sheet)

| # | Command | Result |
|---|---|---|
| 1 | `mkdir -p ~/INFO7375/youtube/seed-repeatable-not-correct/evidence` | Reel folder, outside the toolkit (CLAUDE.md rule 3). |
| 2 | wrote `evidence/seeded_sampler.py`; `python3 seeded_sampler.py` | softmax([1,2,3], T=1.0) → probs [0.09, 0.245, 0.665]; `random.Random(7).choices(range(3), weights=probs, k=1000)` → **{0: 102, 1: 268, 2: 630}**, exactly the counts in the brief. |
| 3 | wrote `evidence/capture.sh`; `./capture.sh` | Two separate processes → `run1.txt`, `run2.txt`; both print {0: 102, 1: 268, 2: 630}, exit 0; `diff`: **byte-identical**. ENV: Python 3.13.3, Darwin 24.5.0 arm64, script sha256 `5109526d…`. |
| 4 | fact-check probe → `evidence/factcheck_probe.txt` | Share on outcome 0 (the stipulated "correct" answer) = 0.102 (expected ≈ 0.090). Counterfactual seeds: seed 8 → {0: 76, 1: 239, 2: 685}; seed 42 → {0: 76, 1: 253, 2: 671}. So the seed is what fixes the run. |
| 5 | `for i in $(seq 100); do python3 seeded_sampler.py; done \| sort \| uniq -c` → `evidence/run100.txt` | **100/100 identical** outputs. Backs the narration line "I reran it a hundred times". |
| 6 | `fc-list : family \| grep -i …` | Handwriting fonts available: Noteworthy, Marker Felt, Bradley Hand, Chalkboard. Noteworthy chosen for the sticky note. |
| 7 | wrote `beat_sheet.json`; word-count estimate | ≈ 155 s of narration (B01 33, B02 36, B03 46, B04 24, B05 15), under the ~3 min target. |
| 8 | `grep -rn "lead_silence_s" runtime/scripts/*.py` | **Friction:** ai-explainer SKILL.md documents a per-beat `lead_silence_s`, but no script reads it; there is no built-in way to add silent holds. |

## 2026-09-27: Phase 2 (approved; audio, holds, scenes, render)

User approved: add silent holds, keep the Sydney example. User standing instruction: no git push/pull; no git commands were run.

| # | Command | Result |
|---|---|---|
| 9 | `.venv/bin/python runtime/scripts/generate_audio_kokoro.py <reel>` | 5 MP3s, af_bella: B01 32.08, B02 35.66, B03 43.39, B04 24.04, B05 16.49 = 151.7 s; $0.00. |
| 10 | read `runtime/scripts/compile.py` | The compiler takes each beat's length from `actual_duration_s` in beat_sheet.json, so padded audio must update that field. |
| 11 | wrote `pad_holds.py`; added `metadata.holds` to beat_sheet.json; `python3 pad_holds.py` | Holds inserted inside detected pauses (each within 0.5 s of the estimated sentence end): B01 +1.8 tail; B02 +1.8 after "Identical."; B03 +1.5 after "Correct?" and +1.8 tail; B04 +1.8 after "not the answer."; B05 +1.5 tail. Originals kept in mp3/raw/. **Total 161.86 s (2:42).** |
| 12 | wrote `cues.py`; `python3 cues.py` | **Bug:** B03's last two cues ("Identical, yes" / "Correct?") snapped to the same pause (40.04 s). Made snapping monotonic, which **over-corrected:** "Correct?" then snapped forward to the pause after it (43.59 s, so the red X would land late). Limited forward snapping to 0.6 s; "Correct?" now at 40.97 s. |
| 13 | `fc-list` / glyph test render | Noteworthy's zero is indistinguishable from the letter O ("outcome O"). Switched the sticky note to Marker Felt (distinct, narrower zero). |
| 14 | wrote `scenes.py` (5 scenes); `manim -ql` ×5 | All rendered first time; durations match audio within 1–2 frames at 15 fps. |
| 15 | QC pass 1 (contact sheets: cue +1.6 s, 50%, 85%, end) | Defects: B01 tags overlapping; B02 stamp covering run 1's counts line, note off-frame; B03 sticky note covering box 0 and its own arrow, 100-runs cards tiny, diagram output tiny, first X off the left edge; B04 `Indicate(color=INK)` flooding the bubbles solid dark, badge overlapping the chat and off-frame, note colliding with the fact card; B05 underfilled at the 50% frame (only 2 of 3 sentences visible). |
| 16 | fixes + QC pass 2 | B01 tag leader line; B03 re-laid out; B05 now shows the whole card from the start, with the active sentence in full ink plus a terracotta bar (muted text still passes 4.5:1). B02 stamp still covering the caption and note off-frame, and a bar poking out of run 2's panel; fixed. |
| 17 | root cause of "oversized" stamps and badge | My `slam()` helper played `mob.animate.scale(1/1.5)` and `FadeIn(mob)` on the same object at once; FadeIn won, so every stamp stayed at 1.5×. Replaced with a single `FadeIn(mob, scale=1.5)`; same fix for the sticky-note slap. |
| 18 | caption width checks (`Text(...).width`) | B02 caption was 14.6 units at size 28 (would be fit-shrunk, the cause of the softmax reel's GATE T failure). Shortened to 11.2 units. |
| 19 | wrote FACTCHECK.md, SHOTLIST.md, PROMPTS.md | Required by GATE F. |
| 20 | `PATH=.venv/bin:$PATH ART_QC=0 ./art run <reel>` then `./art final <reel> --out <reel>` | Running; logs `_run1.log`, `_final1.log`. `ART_QC=0` for the same reason as the softmax reel (GATE A's Manim stub); GATE T and V still run under `./art final`. |
| 21 | (run 1) 4K render of all 5 beats + `./art final` | Review cut built, 5/5 slots MANIM. **GATE T FAIL:** B03 smallest text run 40 px < 41 px floor. Enlarged the grid caption (26→32), widened the 100-runs cards, gave the HYPOTHETICAL tag more room, and enlarged the sticky-note text and paper. |
| 22 | (run 2) + final | B03 size now passes. **GATE T FAIL:** B03 overflow §8.2, 2 text runs outside the 90% title-safe box. Extracted the exact midpoint frame (GATE T samples each beat at 50%) with a safe-box overlay: the grid caption dipped below y = −3.6, the tag box touched the left edge, box 2 touched the right edge. Pulled all inside. |
| 23 | (run 3) + final | Overflow passes. **GATE T FAIL:** B03 contrast §8.3, "terracotta accent text on cream 2.74:1". False positive: the check classifies text-like terracotta blobs as text, and the smaller box 2 fill in B03 matched (B01's taller box did not). The toolkit's own remedy is a hard-coded scene-name exemption list inside `type_check.py` (public toolkit, not edited). Instead B03's lottery drops the accent fill, since box 0 is that beat's focus. |
| 24 | (run 4) + final | **GATE T PASS.** **GATE V REFUSED** (10 frames): B01@85% BLOCKER edge-bleed top plus MAJOR underfill 49% (hook text still typing at that instant); B03@50% MAJOR low-contrast (pale grey "miss" dots, luminance separation 0.26 < 0.30); B03@85% BLOCKER edge-bleed left (input chips). Fixes: shrunk group positioned from its measured top; first hook line fades in with the shrink instead of typing; second line fitted to width; miss dots darkened to #A39B86; chips anchored by their right edge and width-fitted. Verified at those exact timestamps with safe-box overlays. |
| 25 | (run 5) + `./art final` | **PASS.** GATE T PASS; GATE V 0 BLOCKER / 0 MAJOR (10 frames). Master `seed-repeatable-not-correct.mp4`: 3840×2160, 24 fps, H.264 + AAC, 162.0 s; mean −24.3 dB, peak −4.2 dB. Manual review of 13 key frames of the master (reveals and holds) is clean (`_qc/final_sheet.png`). |
| 26 | `rm -f _qc/final/*.png && …` | Minor: zsh aborts on an unmatched glob, so the chained command stopped; re-ran without the `rm`. |
| 27 | `git status` in the toolkit | No changes from this reel (see summary). No git push/pull or other remote git commands run. Nothing uploaded. |

## 2026-09-27: Phase 3 (user-requested 10–20 s intro)

User feedback: the start was abrupt; add a 10–20 s intro that states the concept, including the line "this video is meant to explain the concept of ___". Blank filled with "seeded randomness: why a seed makes a sampling run repeatable, but not necessarily correct".

| # | Command | Result |
|---|---|---|
| 28 | inserted beat `B00` at the top of beat_sheet.json; `metadata.holds.B00 = [{tail: 1.0}]` | Narration 47 words. |
| 29 | `generate_audio_kokoro.py <reel> --only B00` | beat-B00.mp3 18.67 s; other beats untouched. |
| 30 | `python3 pad_holds.py` then `python3 cues.py` | B00 → 19.67 s. B01–B05 rebuilt from mp3/raw/ and verified identical to the previous timings. **Total 181.53 s (3:01.5).** |
| 31 | wrote `B00_Intro` in scenes.py; `manim -qm` + safe-box frame checks | Pass 1: dot field overlapping the shrunken title card and crossing the left/bottom safe edges; "reliable?" and the tag below the safe line; shrunken card text too small. Fix: the subline fades out and only the title shrinks (to 0.62), with three separate regions. Pass 2: the tag touched the "reliable?" box; shifted the box right. |
| 32 | `ART_QC=0 ./art run` + `./art final` (launched with a shell `&` by mistake, so no automatic completion notice; confirmed it was alive with `pgrep` and waited with an `until` loop that also catches failure or the process dying) | **PASS** first try: GATE T PASS; GATE V 0 BLOCKER / 0 MAJOR (12 frames). Master 181.7 s, 3840×2160. Opening frames of the master reviewed (`_qc/intro_sheet.png`). |
| 33 | added the "Made by Aditya Hasija" credit to the B00 title card (user request): teal #1F6F78 (≈5:1 on cream), italic serif under a thin teal rule; fades out with the subline | Low-res safe-box check clean. |
| 34 | `ART_QC=0 ./art run` + `./art final` (proper background run) | **PASS** first try: GATE T PASS; GATE V 0 BLOCKER / 0 MAJOR (12 frames). Master 181.7 s; title-card frame of the master verified (`_qc/credit_final.png`). |
