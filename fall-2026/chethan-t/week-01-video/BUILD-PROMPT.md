# BUILD-PROMPT: Inside One Prediction Step

## 1. The prompts that made it (Claude Code, 2026-09-27)

My main prompt, verbatim in substance:

> Use the brutalist repo to make a 3-minute explainer video on the topic below. Follow the repo's own conventions for structure, style, and specs.
> Topic: Inside one prediction step of a transformer, and why we can't explain its behavior.
> Content to cover, in this order: [items 1–9: the prediction loop; parallelism (Vaswani et al., 2017); tokens → vectors (12,288 per token in GPT-3) + position; attention (river bank vs savings bank; query/key → scores → softmax → weights; only earlier tokens); feed-forward (most parameters; 96 layers in GPT-3); final vector → ~50,000 logits → softmax, softmax appears twice, build it by hand with [1, 2, 3]; designed operations, not behavior; asking the model doesn't settle it (Anthropic 2025, 36 + 59, carry-the-one); closing line "The model decided X because Y" is a story, not a measurement.]
> Keep every fact exactly as stated above; don't add new claims or numbers.

My decisions when Claude asked:
- Credit the video to me (not the repo's "Liam, in for Bear" / @NikBearBrown default).
- Show the derived softmax values for [1, 2, 3]. (36 + 59 = 95 was shown at first, then removed in favour of "a two-digit addition problem".)
- End the verdict on the closing line.
- Build in `INFO7375/build/`.

I then approved the narration before audio was generated. After watching the first cut I asked for fixes (B00 "Namaskara, CG"; B01 text size; B02 title alignment; B13 full stop) and added item 2b, "the architecture at a glance": the full stack, attention + feed-forward blocks with residual connections, multi-head attention (GPT-3: 96 heads in each of 96 layers), and the 2017 encoder–decoder vs GPT's decoder-only design. That became beats B02A and B02B. A second revision kept the length but tightened B03–B06. It added the encoder–decoder detail (masked self-attention, cross-attention; new beat B02C), swapped the examples to "Alice paid Bob / Bob paid Alice" and "bat after cricket / after fruit", and described the addition case without numbers. Each architecture beat stays under 30 s. The full conversation transcript is not included.

## 2. Paste-ready rebuild prompt

Run Claude Code from a `brutalist.art` checkout at commit `29ba0e8` (`.venv` active), with a working copy of this folder at `/path/to/week-01-video`:

```text
Rebuild the ai-explainer reel in /path/to/week-01-video. Read
skills/make/ai-explainer/SKILL.md first. Do not change any narration_text in
beat_sheet.json (it is approved). Add no facts or numbers beyond those in the
narration and README.md.

1. Write FACTCHECK.md, SHOTLIST.md and PROMPTS.md (GATE F requires them),
   using SOURCES.md.
2. Run runtime/scripts/generate_audio_kokoro.py on the folder.
3. Write scenes.py with one Manim Scene per beat whose graphic.manim names a
   class (B02_Parallel, B02A_Architecture, B02B_EncoderDecoder, B02C_DecoderOnly, B03_Vectors, B04_Context, B05_QueryKey, B06_Layers,
   B07_Output, B09_Designed, B10_Biology, B13_Outro). Follow each beat's
   shot.show list and time each scene to its actual_duration_s.
   - B03–B07 share one pipeline diagram (tokens → vectors → attention →
     feed-forward → scores → softmax, with "repeat, layer after layer" under
     attention + feed-forward), one stage highlighted per beat.
   - Label anything schematic as schematic.
   - Palette: cream #FAF9F5, ink #3D3929, one terracotta #D97757 accent.
     EB Garamond. Keep inside ±6.3 × ±3.4.
   - B13 is a silent title card crediting "Chethan Gowda · INFO7375 · Week 01".
4. Run ./art run with QC gates on. Read frames from every beat at 15/50/85%
   of its length and fix any clipping or overlap in scenes.py.
5. Run ./art final <folder> --out <folder>. Never publish or upload.
   Report the output path, runtime and SHA-256.
```

## 3. The commands

```bash
git clone https://github.com/nikbearbrown/brutalist.art && cd brutalist.art
git checkout 29ba0e8
python3 -m venv .venv && source .venv/bin/activate
./setup --install

python3 runtime/scripts/generate_audio_kokoro.py /path/to/week-01-video   # audio is the clock
./art run   /path/to/week-01-video                                        # review cut + GATE A/W/B/V
./art final /path/to/week-01-video --out /path/to/week-01-video           # clean 3840×2160 master
```

Softmax by hand, as shown in B08:

```python
import math
scores = [1, 2, 3]
weights = [math.exp(s) for s in scores]
total = sum(weights)
print([round(w / total, 2) for w in weights])   # recorded: [0.09, 0.24, 0.67]
```

**Recorded environment:**
- Tools: brutalist.art `29ba0e8`, Python 3.12.14, Manim 0.18.1, Kokoro `am_onyx` via kokoro-onnx.
- Machine: macOS (Apple Silicon).
- Result: 244.0 s, SHA-256 `7291e3b27394a0c9b4adde197f850b4a7f22da410ee51cc9bac60be26b686366`.
