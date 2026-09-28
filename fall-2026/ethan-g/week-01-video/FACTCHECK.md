# FACTCHECK — A training-scale slogan restated as a division with a hidden assumption

Source: Nik Bear Brown, *INFO 7375 — Prompt Engineering for Generative AI*,
Chapter 1 "Randomness and first prompts", §"Scale, and the arithmetic behind the
slogans" (repo `nikbearbrown/info-7375-prompt-engineering-for-generative-ai`,
`chapters/01-randomness-and-first-prompts.md`, fetched 2026-09-26).

DOUBLE-CHECK LAW: every number on screen was re-derived independently before
scripting, not copied from the prose. The reel is written in Teardown register,
not read off the chapter.

| # | Claim (beat) | Status | Independent check |
|---|---|---|---|
| 1 | GPT-3: 175B parameters, ~300B training tokens, 3.14 × 10²³ FLOP (B02) | VERIFIED — as published | Chapter cites Brown et al., arXiv:2005.14165 (2020). Reel repeats the citation on screen. |
| 2 | 300B tokens × 0.75 words/token = 225B words (B03) | RE-DERIVED ✓ | 3.0e11 × 0.75 = 2.25e11 exactly. |
| 3 | 225B words ÷ 250 wpm = 1,711 years (B03) | RE-DERIVED ✓ | 2.25e11 / 250 / (365.25×24×60) = 1,711.2. |
| 4 | ÷ 200 wpm = 2,139 years (B04) | RE-DERIVED ✓ | 2,138.9 → 2,139. |
| 5 | ÷ 150 wpm = 2,852 years (B04) | RE-DERIVED ✓ | 2,851.9 → 2,852. |
| 6 | Spread = 1,141 years (B04) | RE-DERIVED ✓ | 2,851.9 − 1,711.2 = 1,140.7 → 1,141. Chapter says "more than a thousand years"; the reel states the computed figure and the screen shows all three answers it comes from. |
| 7 | 3.14 × 10²³ ÷ 1e9 ops/sec ≈ 9.95 million years (B06) | RE-DERIVED ✓ | 3.14e23/1e9 = 3.14e14 s; ÷ 31,557,600 s/yr = 9.95e6. |
| 8 | 31,557,600 seconds per year (B06) | VERIFIED | 365.25 × 24 × 3600. Julian year, consistent with check #3. |
| 9 | "over 100 million years" requires ≈ 3.2 × 10²⁴ ops (B07) | RE-DERIVED ✓ | 3.2e24/1e9/31,557,600 = 101.4e6 years — i.e. "over 100 million". |
| 10 | That is ≈ 10× GPT-3's budget (B07) | RE-DERIVED ✓ | 3.2e24 / 3.14e23 = 10.19. Stated as "roughly ten times". |
| 11 | Later frontier models are larger and figures often undisclosed | VERIFIED — as stated by the source; **no longer shown on screen** | Chapter: "Later frontier models are substantially larger, and their figures are frequently undisclosed." Earlier cuts showed this in B02's header and a B09 verdict line; both were removed. The B07 narration's "plausible for a later system" is the only remaining reference, and it makes no claim about disclosure. |
| 12 | "more text than a person could read in many lifetimes" is the surviving claim (B05) | VERBATIM | Chapter's own words; shown quoted on screen. |

## Quoted on screen, verbatim
- B05: "more text than a person could read in many lifetimes" — chapter's phrase.
- B02: the Brown et al. citation line.
- B03/B06/B07 slogans are shown in quotation marks as *paraphrased slogans in
  circulation*, not as quotations from the chapter — they are set in italic serif
  and introduced as things "you have heard", which is how the chapter frames them.

## De-sensationalised / scoped
- 0.75 words per token is labelled **an assumption** on screen, because it is one.
  The chapter says "about 0.75"; the reel never presents it as measured.
- Every year-figure is presented as the output of a division whose inputs are
  visible, never as a standalone fact.
- No claim is made about any current Claude model's training scale. GPT-3 is used
  precisely because its figures were published.

## Not claimed (deliberately out of scope)
- Chinchilla-style compute-optimal scaling, tokens-per-parameter ratios.
- Any figure for a post-GPT-3 model.
- Whether the reading comparison is a *good* rhetorical device — only that it is a
  division with an unstated input.
