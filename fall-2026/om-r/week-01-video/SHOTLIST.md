# SHOTLIST — low-temperature-is-not-argmax
# Typed work order per beat. Audio locked 2026-09-27 (Kokoro am_onyx); durations below are measured.
# All 10 slots are pipeline-renderable — no human-supplied media, no open slots.

## B00 — INTRO
B00 · Remotion · ClaudeComposerAsk · 9.96s
  source: own (Remotion) → media/B00.mp4
  status: RENDERABLE (no missing deps)

## B01 — PROBLEM
B01 · Remotion · FormBCard · 23.68s
  source: own (Remotion) → media/B01.mp4
  show: Plain text card, no chart yet: the claim "temperature 0 = deterministic" presented as something to test, not something asserted as true.
  status: RENDERABLE (no missing deps)

## B02 — ASK
B02 · Remotion · ClaudeComposerAsk · 15.53s
  source: own (Remotion) → media/B02.mp4
  status: RENDERABLE (no missing deps)

## B03 — CODE
B03 · Remotion · ClaudeCodeBeat · 19.09s
  source: own (Remotion) → media/B03.mp4
  status: RENDERABLE (no missing deps)

## B04 — OUTPUT — first run
B04 · Manim · B04_RefusalAndConcentration · 22.42s
  source: own (scenes.py) → manim/B04.mp4
  show: First half: the real ValueError text rendered directly, in red, held for 2 seconds. Second half: bar chart from real counts {0:18, 1:133, 2:849} out of 1000, with assigned probabilities (1.6%, 11.7%, 86.7%) labeled beside each bar.
  status: RENDERABLE (no missing deps)

## B05 — CHANGE — check & revise
B05 · Remotion · ClaudeComposerAsk · 21.70s
  source: own (Remotion) → media/B05.mp4
  status: RENDERABLE (no missing deps)

## B06 — OUTPUT — revised
B06 · Manim · B06_ArgmaxContrast · 29.75s
  source: own (scenes.py) → manim/B06.mp4
  show: Split-screen bar charts. Left: sample() counts {0:18, 1:133, 2:849}, visible variance across three bars. Right: argmax_select() counts {2:1000}, a single full bar, others at zero. Right side carries a held caption: CONSTRUCTED FOR THIS VIDEO — not in the chapter's code.
  status: RENDERABLE (no missing deps)

## B07 — SUMMARY
B07 · Remotion · TypesetMath · 34.32s
  source: own (Remotion) → media/B07.mp4
  show: Plain text, no chart: the ratio formula p_i/p_k = exp((z_i - z_k)/T), then below it, the boundary statement as a separate card: "What this doesn't establish."
  status: RENDERABLE (no missing deps)

## B08 — NEXT STEPS
B08 · Remotion · ClaudeComposerAsk · 19.54s
  source: own (Remotion) → media/B08.mp4
  status: RENDERABLE (no missing deps)

## B09 — OUTRO
B09 · Remotion · ClaudeVerdictArtifact · 31.01s
  source: own (Remotion) → media/B09.mp4
  status: RENDERABLE (no missing deps)

Total narration: 227.00s
