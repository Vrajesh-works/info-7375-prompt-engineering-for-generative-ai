# BUILD-PROMPT — Subtract the Max

Two ways to rebuild: paste the prompt into Claude Code, or run the commands yourself. Both assume
this layout:

```
Documents/GitHub/
├── brutalist.art/     # git clone https://github.com/nikbearbrown/brutalist.art  (tested at cd4bf20)
└── week-01-video/     # this folder
```

## A. Paste-ready Claude Code prompt

```
Rebuild the INFO 7375 Week 1 video in ./week-01-video with the brutalist.art checkout in
./brutalist.art. Do not change narration, numbers or claims; this is a rebuild, not a rewrite.

Ground truth, read first:
1. week-01-video/beat_sheet.json: the reviewed master (narration + show blocks).
2. week-01-video/FACTCHECK.md and SOURCES.md: what each number is and where it comes from.
3. brutalist.art/skills/make/ai-explainer/SKILL.md: chassis only. Do NOT use the Liam /
   @NikBearBrown persona or ClaudeTitleOutro; this is a student submission (see SOURCES.md).

Steps:
1. Environment: follow week-01-video/build/ (venv with build/requirements-win.txt, ffmpeg on PATH,
   python3 shim; apply build/remotion_scenes-windows-npx.patch to brutalist.art on Windows).
2. Evidence: python week-01-video/code/evidence.py, then python -m unittest discover -s
   week-01-video/code/tests. Stop if any test fails or any number differs from FACTCHECK.md.
3. Audio (the clock): python3 runtime/scripts/generate_audio_kokoro.py ../week-01-video
4. Bookends: python3 runtime/scripts/remotion_scenes.py ../week-01-video
5. Body: ./render_manim.sh inside week-01-video
6. Compile: python3 runtime/scripts/compile.py ../week-01-video --height 1080 --fps 30 --out ../week-01-video/final   # GATE V enforced; GATE T kerning: see FRICTIONAL.md #11
7. Visual QC: sample each beat at 15/50/85% with ffmpeg and LOOK at the PNGs (clipping, overlap,
   legibility, every constructed input tagged, composer chip reads "Mock composer"). Report; never publish.
```

## B. Commands (what was actually run, Windows 11 + Git Bash, 2026-09-26/27)

```bash
# one-time setup
cd ~/Documents/GitHub
git -c core.longpaths=true clone --depth 1 https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
python -m venv .venv
.venv/Scripts/python -m pip install -r ../week-01-video/build/requirements-win.txt matplotlib
(cd runtime/remotion && npm install)
mkdir -p runtime/models/kokoro && cd runtime/models/kokoro
curl -fLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -fLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd ../../..
git apply ../week-01-video/build/remotion_scenes-windows-npx.patch
winget install --id Gyan.FFmpeg -e
mkdir -p .shim && printf '#!/bin/sh\nexec "%s/.venv/Scripts/python.exe" "$@"\n' "$PWD" > .shim/python3
cp ../week-01-video/build/env.sh .shim/env.sh     # edit the ffmpeg path if yours differs

# every build
source .shim/env.sh
python ../week-01-video/code/evidence.py > /dev/null
python3 runtime/scripts/generate_audio_kokoro.py ../week-01-video
python3 runtime/scripts/remotion_scenes.py ../week-01-video
(cd ../week-01-video && ./render_manim.sh)
python3 runtime/scripts/compile.py ../week-01-video --height 1080 --fps 30 --out ../week-01-video/final   # GATE V enforced; GATE T kerning: see FRICTIONAL.md #11
```

On macOS/Linux, skip the shim, winget, and patch steps; use `.venv/bin/python`, and install ffmpeg with your package manager.

## Prompts used to author it (excerpts, not a transcript)

- Concept choice: Claude offered four Chapter 1 concepts; Siddi picked "max-subtraction".
- Evidence: "use what main.py actually prints", which led to `code/evidence.py` and the rule that no number is typed into a scene.
- Honesty constraints given to the build: no Claude reply on screen; label constructed inputs; synthetic
  voice disclosed; name one thing the explanation does not establish (B06).
