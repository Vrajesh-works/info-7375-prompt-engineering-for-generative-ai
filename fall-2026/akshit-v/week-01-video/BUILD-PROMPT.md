# BUILD-PROMPT — INFO 7375, Week 01 video

Everything needed to rebuild this video from scratch. Never publishes, never uploads.

---

## 0. Prerequisites

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
./setup --install          # --install is ONE token; "-- install" silently does nothing
./setup                    # must exit 0 with all seven rows green
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8   # Windows: required (see FRICTIONAL.md)
```

**Five toolkit changes are needed** — four Windows fixes and one opt-in switch, each
one or two lines, each documented with file and line in `FRICTIONAL.md`:

| File | Change |
|---|---|
| `setup:106,114` | `--exclude-dir=youtube` on both ElevenLabs-guard greps |
| `examples/_smoke/beat_sheet.json:4` + `smoke_test.sh:60` | slug `_smoke` → `smoke` |
| `runtime/scripts/compile.py:~794` | quote + escape the `drawtext` font path |
| `runtime/scripts/remotion_scenes.py:90` | resolve `npx` via `shutil.which` |
| `runtime/scripts/compile.py:40` | `ART_BURNIN=0` opt-in: review cut without burn-ins |

Apply them in one step from `toolkit-changes/` (checked against revision `6a8380ae`):

```bash
git checkout 6a8380ae169cca81e0633664a65c958f5c12ab4b
git apply youtube/brutalist/week-01-video/toolkit-changes/toolkit.patch   # includes the new scene files
```

Place this folder at `youtube/brutalist/week-01-video/` inside the checkout.

---

## 1. The numbers come first

```bash
REEL=youtube/brutalist/week-01-video
python3 $REEL/code/pretraining_target.py | tee $REEL/code/OUTPUT.txt
```

Deterministic (zero init, no sampling, no seed). Expect exactly:

```
   600 |     0.6989       0.2989        0.0022 |  0.6131
   max gap from CORPUS FREQUENCY : 0.0022
   max gap from TRUTH            : 0.7011
   argmax = sydney   (truth = canberra)
   entropy of the corpus   = 0.6109
   full trajectory (601 steps) -> code/trajectory.json
```

`code/trajectory.json` is regenerated into
`runtime/remotion/src/illustrations/pretraining_trajectory.ts` (every row, no edits).
If any value changes, regenerate that file — never hand-tune a number to fit a frame.

---

## 2. The paste-ready rebuild prompt

```
From my brutalist.art toolkit root, rebuild the reel at
youtube/brutalist/week-01-video end to end. Do not publish, do not upload,
do not push to GitHub.

1. GATE CHECK. export PYTHONUTF8=1 PYTHONIOENCODING=utf-8; ./setup must show all
   seven rows green. Read FRICTIONAL.md first — five toolkit changes are required.

2. NUMBERS. Run code/pretraining_target.py and diff against code/OUTPUT.txt.
   If it differs, stop and tell me.

3. AUDIO (the master clock). python3 runtime/scripts/generate_audio_kokoro.py <reel>
   12 beats, am_onyx, $0.00, ~176s.

4. WORD CLOCK. python3 runtime/scripts/align.py <reel>  -> mp3/words.json
   Expect "aligned 12, fallback 0". Recompute every beat's
   shot.remotion.props.cues from words.json (trigger word -> beat fraction, 0.2s
   lead) and re-sync durationSeconds. Print the cue times and check them against
   the transcript before rendering.

5. SCENES. python3 runtime/scripts/remotion_scenes.py <reel>

6. REVIEW CUT, no burn-ins.
   ART_BURNIN=0 ART_FACTS=0 ART_QC=1 ART_STRICT=0 bash runtime/scripts/run.sh <reel> --height 1080
   -> week-01-pretraining-target-slate.mp4. STOP HERE — no final cut.

7. CAPTIONS. cd <reel>; python3 tools/make_captions.py; then burn captions.ass
   into week-01-pretraining-target-captioned.mp4 (command in section 3).

8. DISCLOSURES. Confirm on screen: B00/B10 carry the RECONSTRUCTED UI tag and
   show no reply lines; B00 and B11 disclose the synthetic voice; B04-B07 carry
   the 'computed from the CONSTRUCTED corpus' stamp.

9. VISUAL QC. Sample every beat where its content lands, ACTUALLY READ the PNGs,
   and check the captions sit inside SAFE and collide with nothing. Also verify
   B01 really ends on "the token that followed" — its correction once silently
   failed. Log to _qc/REPORT.md.

10. REPORT duration, the three gates, and every defect with its region.
```

---

## 3. Commands, in order

```bash
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
REEL=youtube/brutalist/week-01-video

python3 $REEL/code/pretraining_target.py | tee $REEL/code/OUTPUT.txt
python3 runtime/scripts/generate_audio_kokoro.py $REEL
python3 runtime/scripts/align.py $REEL
# (recompute props.cues from mp3/words.json — see step 4 above)
python3 runtime/scripts/remotion_scenes.py $REEL
ART_BURNIN=0 ART_FACTS=0 ART_QC=1 ART_STRICT=0 bash runtime/scripts/run.sh $REEL --height 1080

cd $REEL
python3 tools/make_captions.py
ffmpeg -y -i week-01-pretraining-target-slate.mp4 \
  -vf "subtitles=captions.ass:fontsdir=../../../runtime/fonts/Lato/static" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy \
  week-01-pretraining-target-captioned.mp4
```

The `subtitles=` path is relative on purpose: on Windows an absolute path's drive
colon breaks ffmpeg's filtergraph parser (the same bug as `compile.py`'s font path).

**Deliverable:** `week-01-pretraining-target-captioned.mp4` — 1920×1080 (the course guide's
explicit choice over the toolkit's 4K default), captions burned in.
`captions.srt` ships alongside as a toggle-able sidecar.

---

## 4. Files this reel adds to the toolkit

| File | What |
|---|---|
| `runtime/remotion/src/illustrations/pretraining.tsx` | the scene components, all word-cued, including `ReconstructedComposer` (the labelled Claude-styled prompt box for B00/B10) |
| `runtime/remotion/src/illustrations/pretraining_trajectory.ts` | generated from `code/trajectory.json` — all 601 real steps |
| `runtime/remotion/src/Root.tsx` | registers the eight compositions at 1920×1080 |

`SubmissionOutro` exists because `ClaudeTitleOutro` hardcodes `@NikBearBrown`.
`TargetStack` replaces the library `LayerStack` in B08 because `LayerStack`'s reveal
timing is fixed (it cannot follow the voice) and its geometry is 1280×720.

---

## 5. Stopping point

The build stops at the **review cut**. No final cut; `FACTCHECK.md` is deliberately
absent, so `GATE F` refuses a final — which is correct. Nothing uploaded, nothing
pushed.
