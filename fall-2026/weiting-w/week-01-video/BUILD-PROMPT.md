# BUILD-PROMPT — One Word, Same Answer

The commands that rebuild this video from the files in this folder. The prompts sent to Claude *as the subject under test* (the experiment) are in `PROMPTS.md`; this file is the build recipe. It assumes a reader who has already set up the Brutalist toolkit.

## 0. Prerequisites

Free local pipeline only — no API keys, no paid generation, no upload.

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
# toolkit prerequisites, already installed: Manim Community 0.18.x, Remotion (Node),
# Kokoro TTS (bundled at runtime/models/kokoro/), ffmpeg
source .venv/bin/activate    # if the toolkit uses a virtualenv; skip if not
```

`scenes.py` must be able to resolve **EB Garamond** on this machine (its font-registration block looks for the toolkit's bundled font files).

## 1. Place the files as a reel

The toolkit renders a *reel* folder. Copy this submission's build files into a reel path inside the checkout:

```bash
REEL=youtube/weiting/one-word-same-answer
mkdir -p "$REEL"
cp beat_sheet.json scenes.py analyze_responses.py \
   FACTCHECK.md SHOTLIST.md PROMPTS.md "$REEL"/
cp -R evidence "$REEL"/evidence
```

The reel now holds the scenes, the reviewed plan, the evidence (including the 24 `A1`–`D4` screenshots B03 needs), and the fact/shot/prompt sheets.

Note: `beat_sheet.json` already carries `qc.sparse_by_design` on B02 and B03, each with a written reason. These beats reveal content gradually, so a mid-beat frame is partially populated by design; the flag waives only the underfill check (edge-bleed and contrast are still enforced). Keep it — without it the strict final gate rejects those two beats.

## 2. Generate narration (Kokoro, local)

Beat durations are driven by the narration, so audio comes first. Voice is `af_bella` (female), set in `beat_sheet.json` metadata. From the toolkit root:

```bash
python3 runtime/scripts/generate_audio_kokoro.py youtube/weiting/one-word-same-answer
```

This writes `mp3/beat-B00.mp3 … beat-B09.mp3` into the reel and stamps each beat's measured duration back into `beat_sheet.json`. All on-screen timing follows these files; never hand-tune durations. (If the original per-beat `mp3/` from this project is reused instead, the runtime reproduces exactly, 198.5 s.)

## 3. Render the ten beats

```bash
ART_STRICT=0 ./art run youtube/weiting/one-word-same-answer
```

`ART_STRICT=0` downgrades gate *warnings* to non-blocking (blocking errors still stop the build). This runs the pre-flight gates, renders every Manim scene (B01–B07, B09) and Remotion beat (B00, B08), audits each, and writes a labeled review cut `youtube/.../weiting-one-word-same-answer-slate.mp4`. The corner label is expected in the *review* cut only.

## 4. Write the clean master

```bash
./art final youtube/weiting/one-word-same-answer
```

`final` runs GATE T (type-lock) and a strict, non-lenient GATE V (frame-level QC), assembles the beats that `run` rendered, and writes the clean, label-free master to `renders/weiting-one-word-same-answer.mp4`. Rename it for submission:

```bash
cp renders/weiting-one-word-same-answer.mp4 \
   <submission-folder>/Wang_Weiting_INFO7375_Week01_Video.mp4
```

## 5. Verify the numbers (optional, self-checking)

```bash
python3 analyze_responses.py     # recomputes every on-screen figure from evidence/
```

`scenes.py` also asserts against `evidence/analysis.json` at render time and refuses to render if any count drifts, so a wrong number cannot reach the screen.

## Verified output

- Duration: 198.5 s (3:18)
- sha256: `2aff490b2d4f0b1550eb65212813f4af454427324f652687f73e6d7e8d58b0f9`
- Written: 2026-09-28 (UTC)
