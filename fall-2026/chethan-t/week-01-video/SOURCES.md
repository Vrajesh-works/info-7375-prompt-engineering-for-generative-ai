# SOURCES: Inside One Prediction Step

## What I used

| Source | Used for | Licence / terms |
|---|---|---|
| My written brief (items 1–9) | Every fact and number in the video, in this order | Mine |
| Vaswani et al., 2017, *Attention Is All You Need*, arXiv:1706.03762 | The transformer and its parallelism (B02); residual connections, multi-head attention, and the original encoder–decoder design for translation, with masked self-attention and cross-attention (B02A–B02C) | Cited, not reproduced |
| Anthropic, 2025, *On the Biology of a Large Language Model* | Its two-digit addition case (the paper's example is 36 + 59; shown without numbers at my request): parallel internal pathways vs. the model's carry-the-one explanation (B10) | Cited, not reproduced; drawn schematically |
| GPT-3 figures (12,288 numbers per token, 96 layers, 96 heads per layer, ~50,000-token vocabulary) | B02A, B03, B06, B07 | Figures as given in my brief |
| brutalist.art toolkit, github.com/nikbearbrown/brutalist.art @ `29ba0e8` | `ai-explainer` skill; Remotion scenes ClaudeComposerAsk, BrutalistHesitantWriter, ClaudeCodeBeat, ClaudeVerdictArtifact; compile pipeline and QC gates | No LICENSE file in the repository at this commit; used as the course instructs |
| Kokoro-82M via kokoro-onnx, voice `am_onyx` | All narration (AI voice, local, free) | Apache-2.0 (model); MIT (kokoro-onnx) |
| Manim Community v0.18.1 | Scenes B02, B02A–B02C, B03–B07, B09, B10, B13 | MIT |
| EB Garamond (bundled with the toolkit) | On-screen type | SIL Open Font License 1.1 |

No stock footage, photographs, screenshots, or AI-generated images or video are used.

## What I made

- The brief: topic, the nine points in order, the facts and numbers, and the rule "don't add new claims or numbers".
- The decisions: credit to me; show the two derived values; the closing line ends the verdict; build location.
- Reviewed and approved the narration before audio was generated (2026-09-27).
- Reviewed the first cut and asked for fixes (2026-09-27): greeting "Namaskara, CG" instead of "Namaste, Chethan" (B00); smaller opening text so the cursor stops overlapping the cards (B01); left-aligned lane titles (B02); the full stop after "Step" aligned to the baseline (B13).
- Added the architecture section (item 2b): full stack, residual connections, multi-head attention, encoder vs decoder. It became beats B02A and B02B (2026-09-27).
- Second revision (2026-09-27): chose the new examples (Alice/Bob; cricket bat vs fruit bat), asked for the addition case without specific numbers, and chose the encoder–decoder detail as the extra architecture content, with each architecture beat under 30 s.
- <!-- TODO(Chethan): add your own review notes and any beat changes after watching. -->

## What Claude (Claude Code) contributed

- Turned the brief into the beat sheet: narration wording and every beat's on-screen plan. The on-screen framing that isn't a fact claim is also Claude's: the "Given / Predict / Repeat" cards, the example sentences "She swung the cricket bat hard" and "the cricket bat broke", and the Your-turn prompt.
- Wrote and ran the softmax-by-hand code, and recorded its output: [0.09, 0.24, 0.67].
- Wrote all Manim scene code, including the pipeline diagram, and fixed layout defects after reading rendered frames.
- Ran the toolkit pipeline: Kokoro audio, Manim and Remotion renders, compile, QC gates.
- Fact-checked each claim against its source (the GPT-3 paper for 12,288 and 96, the Anthropic 2025 paper for the addition case).
- Drafted this file, `FRICTIONAL.md`, `README.md` and `BUILD-PROMPT.md` for my review.

## Constructed vs. real

- **Real and reproducible:** softmax([1, 2, 3]) = [0.09, 0.24, 0.67] (the scores are hand-picked; the computation is the real one).
- **Schematic, labelled or drawn as a diagram:** the architecture overview, the residual block, the head fan-out and the encoder/decoder stacks (B02A, B02B).
- **Schematic or illustrative, labelled on screen:**
  - the "bat" vectors (B04);
  - the attention arrow thicknesses (B05);
  - the parameter-share bar, "not to scale" (B06);
  - the 40 logit bars standing in for ~50,000 (B07);
  - the parallel pathways and digit boxes (B10).
