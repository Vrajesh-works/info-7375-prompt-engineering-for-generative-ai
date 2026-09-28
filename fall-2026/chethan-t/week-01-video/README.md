# Inside One Prediction Step: INFO7375 Week 01 video

**Name:** Chethan Gowda
**Concept:** What happens inside one prediction step of a transformer, and why we can't explain its behavior.
**Why:** Every chatbot answer is this one step run in a loop. Knowing exactly which parts were designed and which were fitted shows why "the model decided X because Y" is a story, not a measurement.
**Runtime:** 4 min 04 s (244.0 s), 3840×2160, H.264/AAC
**Video file:** `one-prediction-step.mp4` (SHA-256 `7291e3b27394a0c9b4adde197f850b4a7f22da410ee51cc9bac60be26b686366`)

## Files

| File | What it is |
|---|---|
| `one-prediction-step.mp4` | The rendered video |
| `beat_sheet.json` | The reviewed narration and visual plan: 17 beats, each with its narration and an on-screen `show` list (approved 2026-09-27) |
| `BUILD-PROMPT.md` | The prompts and commands that rebuild it |
| `SOURCES.md` | What I used, what I made, what Claude contributed, third-party assets and licences |
| `FRICTIONAL.md` | Dated log of what got in the way |

## How to rebuild the video from this folder

Everything is free and local: Kokoro voice, Manim, Remotion. No API keys, no accounts.

1. **Toolkit at the version used:**
   ```bash
   git clone https://github.com/nikbearbrown/brutalist.art
   cd brutalist.art && git checkout 29ba0e8
   python3 -m venv .venv && source .venv/bin/activate   # Python 3.12; manim 0.18 won't run on 3.13
   ./setup --install
   ```
2. **Working copy:** copy this folder somewhere outside the toolkit.
3. **Rebuild:** run Claude Code in the toolkit and paste the prompt in `BUILD-PROMPT.md` §2. It:
   - generates the narration audio (the timing clock);
   - rebuilds the 5 Claude-app beats (B00, B01, B08, B11, B12) directly from `beat_sheet.json`;
   - writes `scenes.py` for the 12 drawn beats from each beat's `show` list;
   - creates the three short work-order files the toolkit requires;
   - renders with every QC gate on.

   The drawn scenes' source isn't among the six required files, so a rebuild follows the same plan and numbers but won't be pixel-identical.
4. **Clean master:** `./art final <folder> --out <folder>`

## The numbers, checkable by hand

Every fact and number comes from my brief, kept as stated: 2017; hundreds of billions of tokens; 12,288 numbers per token; 96 heads in each of 96 layers; about 50,000 vocabulary tokens; 2025. The encoder–decoder detail (masked self-attention and cross-attention) was added at my request.

The only derived value:
- **Softmax of [1, 2, 3]:**
  - e¹, e², e³ = 2.718, 7.389, 20.086;
  - total = 30.193;
  - divide each by the total → **0.09, 0.24, 0.67** (recorded run in B08).

Everything that could look like data (the "bat" arrows, attention arrow thickness, the parameter bar, the logit bars, the parallel pathways) is labelled schematic, illustrative, or not to scale on screen.

## Honesty notes

- The narration is an AI voice (Kokoro `am_onyx`), disclosed in the first beat. The script was written with Claude's help (see `SOURCES.md`).
- The closing line, "The model decided X because Y is a story, not a measurement", ends the verdict beat. The repo's Your-turn prompt and a title card follow it.
