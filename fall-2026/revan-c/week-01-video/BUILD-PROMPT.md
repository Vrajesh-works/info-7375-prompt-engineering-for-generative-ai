# BUILD-PROMPT — tokens-not-words

How to rebuild `final/tokens-not-words.mp4` from this folder. Free pipeline only: no API keys, no paid calls, no upload.

## Tested environment

macOS (Apple Silicon) · Python 3.12.14 · Node v26.0.0 · ffmpeg 9.0.2 · brutalist.art commit `6a8380a` · manim 0.18.1 · kokoro-onnx 0.6.1 · tiktoken 0.14.0 · Remotion 4.0.486

## Commands

Run from a parent folder that contains `week-01-video/`.

```bash
# 0. one-time setup
git clone https://github.com/nikbearbrown/brutalist.art
(cd brutalist.art && git checkout 6a8380a)
brew install python@3.12 ffmpeg cairo pango pkg-config
/opt/homebrew/bin/python3.12 -m venv .venv
export PATH="$PWD/.venv/bin:$PATH"
pip install tiktoken==0.14.0
(cd brutalist.art && ./setup --install)
#   At this commit, setup installs everything and then stops early on a false
#   ElevenLabs match in the toolkit's own youtube/ folder (see FRICTIONAL.md, Entry 1).
#   Check readiness by hand instead:
python3 -c "import PIL, manim, faster_whisper, kokoro_onnx, mutagen"
python3 brutalist.art/runtime/scripts/setup_smoke_kokoro.py

# 1. evidence: regenerate every number shown on screen
python3 week-01-video/evidence/tokenize_examples.py      # writes evidence/tokens.json

# 2. audio is the master clock
cd brutalist.art
python3 runtime/scripts/generate_audio_kokoro.py ../week-01-video

# 3. render Manim + Remotion beats, compile the review cut, run all QC gates
export TOKENS_REEL_DIR="$(cd ../week-01-video && pwd)"   # scenes.py reads evidence/ and beat_sheet.json from here
./art run ../week-01-video

# 4. clean 1080p master
./art final ../week-01-video --height 1080 --out "$TOKENS_REEL_DIR/final"
```

`./art run` skips slots that are already filled. To re-render a changed scene, delete its clip first (e.g. `rm ../week-01-video/manim/B07.mp4`, or `media/B00.mp4` for Remotion beats). If narration changes, delete that beat's `mp3/beat-Bxx.mp3` and rerun step 2.

**Expected result:** `_qc/REPORT.md` 0 BLOCKER / 0 MAJOR, `TYPECHECK.md` GATE T PASS, `final/tokens-not-words.mp4` 1920×1080, 144.75 s. Then watch the whole video. The gates missed a real overlap in B07 once; only looking at frames caught it.

## Paste-ready Claude Code prompt

> In this folder, `week-01-video/` is a Brutalist ai-explainer reel (`beat_sheet.json` + `scenes.py`) and `brutalist.art/` is the toolkit at commit 6a8380a. Use the project `.venv` (Python 3.12). Regenerate `evidence/tokens.json` with `evidence/tokenize_examples.py`, then run `generate_audio_kokoro.py`, `./art run`, and `./art final --height 1080 --out <reel>/final` on `../week-01-video`, with `TOKENS_REEL_DIR` set to the reel folder. Do not change narration, numbers or the beat sheet. If a gate fails, report the gate's exact message and fix only layout in `scenes.py`. After the final render, sample at least one frame per beat with ffmpeg, look at each one, and report any overlap, clipping or illegible text. Never publish, never call a paid API, and keep normal permission prompts on.

## Files this build reads

| File | Role |
|---|---|
| `beat_sheet.json` | Narration, scene choice and props for all 11 beats |
| `scenes.py` | Manim source for B02–B07 and B10 (reads `evidence/tokens.json`) |
| `evidence/tokenize_examples.py` → `evidence/tokens.json` | The only source of token IDs and splits |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | Paperwork Brutalist requires before it renders (GATE F) |
