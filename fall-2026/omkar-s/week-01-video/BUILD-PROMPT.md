# BUILD-PROMPT — rebuild "Subtract the Max" from this folder

## 1. The prompt that produced this build

Given to Claude Code (Claude desktop app, 2026-09-24), with the Canvas assignment text pasted in above it:

> please complete the assignment but don't push anything to github

Every decision after that (concept, script, scenes, fixes) is recorded in `FRICTIONAL.md` entries 1–4.

## 2. Paste-ready prompt to rebuild it

```text
Rebuild the Week 1 video in this folder with the free Brutalist pipeline.
Folder: <absolute path to week-01-video>. Toolkit: a sibling brutalist.art checkout.
1. Re-run evidence/max_shift_evidence.py (needs the course repo at ../course, or edit MAIN)
   and diff its output against evidence/max_shift_output.txt. Stop if any number differs.
2. Regenerate narration with Kokoro af_bella from beat_sheet.json (audio is the clock).
3. Render each scene in scenes.py at 1920x1080, 24 fps, into manim/<BEAT>.mp4.
4. Run the layout audit (Gate B) on every scene; fix the scene source, never the gate.
5. ./art run for the review cut (Gate V), then ./art final --height 1080.
6. Sample frames, look at them, and report the output path. No paid calls, no publishing.
```

## 3. Exact commands

From a parent folder that contains both `brutalist.art/` and this reel folder (`reel/` below; in the GitHub copy it is `week-01-video/`).

```bash
# one-time toolkit setup (macOS; see FRICTIONAL entry 3 for why each step exists)
brew install ffmpeg cairo pkg-config pango
git clone https://github.com/nikbearbrown/brutalist.art && cd brutalist.art
git checkout 6a8380ae169cca81e0633664a65c958f5c12ab4b
uv venv --python 3.12 .venv && source .venv/bin/activate
./setup --install                 # npm deps, fonts, Kokoro model (exits on its ElevenLabs guard; see FRICTIONAL)
uv pip install -r requirements.txt  # the Python deps setup did not install
cd ..

# evidence (course repo at ./course, commit e6c6c49d)
git clone https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai course
(cd course && git checkout e6c6c49dd8b65d7f81dd8e72b89fd6c1f6b23738)
(cd course/lessons/01-randomness-and-first-prompts/code && python3 main.py && python3 -m unittest discover -s tests -v)
python3 reel/evidence/max_shift_evidence.py

# 1. audio first: writes mp3/beat-B0*.mp3 and actual_duration_s into beat_sheet.json
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py "$PWD/reel"

# 2. visuals: one Manim scene per beat, timed to the measured audio
cd reel
for s in B00_TheLine B01_NaiveRoute B02_ShiftedRoute B03_WhyItCancels B04_Overflow \
         B05_LessonTest B06_Rounding B07_Boundary B08_Recap; do
  python3 ../brutalist.art/runtime/qc/manim_layout_audit.py scenes.py --class $s --curve-strict   # Gate B
  manim -qh --fps 24 -r 1920,1080 scenes.py $s
  mv "$(find media/videos -name "$s.mp4" | head -1)" manim/${s%%_*}.mp4
done
cd ..

# 3. review cut + frame QC (Gate V), then the clean 1080p master
brutalist.art/art run   "$PWD/reel" --height 1080
brutalist.art/art final "$PWD/reel" --height 1080 --out "$PWD/reel/final"
```

Why the Manim step runs outside `./art run`: GATE A dry-runs scenes against a stand-in for Manim whose `NumberLine` returns empty coordinates, so B04 and B07 crash there. The real rendering audit (Gate B) is run on every scene instead. Filled `manim/` slots make `run.sh` skip only the stand-in check; compile and GATE V still run. Details are in FRICTIONAL entry 4.
