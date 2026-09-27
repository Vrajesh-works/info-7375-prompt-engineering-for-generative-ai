# BUILD-PROMPT — the prompts and commands that rebuild "A Chatbot Is a Loop."

## 0. One-time setup
```bash
REEL=/path/to/week-01-video                                           # this folder
git clone https://github.com/nikbearbrown/brutalist.art ~/Desktop/Brutalist/brutalist.art
cd ~/Desktop/Brutalist/brutalist.art && git checkout 6a8380a
git apply "$REEL/toolkit-additions/toolkit.patch"     # 11 scenes + logo + two setup fixes (see FRICTIONAL.md)

conda create -n brutalist python=3.12 -y && conda activate brutalist   # Python 3.13 fails: manim<0.19
brew install ffmpeg pkg-config pango && brew install --cask mactex-no-gui
./setup --install                                                     # expect 7/7 green

python3 -m venv "$REEL/../.venv-evidence"                             # evidence env, pinned (not submitted)
"$REEL/../.venv-evidence/bin/pip" install -r "$REEL/evidence/requirements.txt"
```

## 1. Record the evidence (≈3 min on an M-series CPU)
```bash
cd "$REEL/evidence"
../../.venv-evidence/bin/python run_experiments.py --out runs     # overwrites runs/ with a fresh recording
../../.venv-evidence/bin/python verify.py            # must end "51/51 checks passed"
```

## 2. Audio → word clock → props
```bash
cd ~/Desktop/Brutalist/brutalist.art
python3 runtime/scripts/generate_audio_kokoro.py "$REEL"          # Kokoro am_onyx, free, local
python3 "$REEL/pad_audio.py" "$REEL"
python3 runtime/scripts/align.py "$REEL"
"$REEL/../.venv-evidence/bin/python" "$REEL/fill_props.py"
```

## 3. Render and check
```bash
./art run "$REEL"        # review cut + GATE V visual QC (delete media/<BID>.mp4 to re-render a changed beat)
./art final "$REEL"      # clean master, no beat markers → brutalist.art/renders/<slug>.mp4 (moved here as Raj_Aditya_INFO7375_Week01_Video.mp4)
```

## The Claude Code prompts used (verbatim intent, condensed)
1. "Clone brutalist.art into this folder, run ./setup --install, then tell me which features are green and red."
2. "Use skills/make/ai-explainer to make a 60-second Brutalist AI Explainer about 'A chatbot is one next-token
   prediction run in a loop'. 12 beats, Kokoro am_onyx, stop at the review cut." → the pilot.
3. Shared the Week 1 brief: "Create a new video which goes for 3 minutes… think about the Relative Quartile point…
   discuss your ideas with me. Post my approval, go ahead." → six ideas proposed.
4. "Go ahead with ideas 1 to 5; skip 6. Create the Frictional log telling how we iterated from the 60-second
   video to this one." → this build.

## The prompt run in claude.ai for B13 (by Aditya, in a fresh chat)
> Who wrote Middlemarch? Then tell me which word in your answer you were least sure of.
