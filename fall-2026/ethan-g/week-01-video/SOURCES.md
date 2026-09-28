# SOURCES — A training-scale slogan restated as a division with a hidden assumption

## Primary source
Nik Bear Brown, *INFO 7375 — Prompt Engineering for Generative AI*,
Chapter 1, "Randomness and first prompts."
`https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/chapters/01-randomness-and-first-prompts.md`
Fetched 2026-09-26. The reel covers one section — the scale-slogan arithmetic —
not the chapter's softmax/temperature half.

The chapter names its own learning objective in the same words this reel is built
around: "restate a training-scale slogan as an arithmetic derivation with its
assumptions named."

## Cited within the source, and repeated on screen
- Brown et al., *Language Models are Few-Shot Learners*, arXiv:2005.14165 (2020) —
  the GPT-3 figures. Shown as a source line in B02.
- The chapter's own derivation script and recorded output (`research/llm_scale.py`,
  `research/llm-scale.json`) are referenced in B09's verdict as the reason the
  argument is checkable. Not quoted on screen; copies are included in this folder
  as `llm_scale.py` and `llm-scale-recorded-output.json`.

## Corrections and scoping applied (DOUBLE-CHECK LAW)
- Every figure was re-derived independently before scripting; see FACTCHECK.md.
  The 1,141-year spread is computed from the chapter's own three answers rather
  than repeating its looser "more than a thousand years".
- 0.75 words/token is labelled an **assumption** on screen wherever it appears.
  The chapter says "about 0.75" and the reel never upgrades that to a measurement.
- Year arithmetic uses the Julian year (31,557,600 s) consistently across the
  reading and compute derivations, so the two ladders are commensurable.
- The circulating slogans in B03/B06 are set in italic serif and introduced as
  things "you have heard" — they are paraphrases of claims in circulation, not
  quotations from the chapter. Only B05's surviving claim is quoted verbatim.
- No claim is made about any current Claude or frontier model's training scale.

## REBUILD LAW
No figure from the source was reproduced. The chapter's own images are Cajal-brief
SVG/PNG assets; none were lifted. Every graphic here is an original animated
Remotion composition, so no "Redrawn from …" caption is owed.

## Determinism
The only seed is `BrutalistHesitantWriter.seed = "hidden-parameter-b01"`, which
fixes the typing performance. Every other composition is a pure function of the
beat clock; the same sheet renders identically on any machine.

---

## Numbers: where each one came from

Every figure on screen was checked against the chapter's **own derivation script**,
`research/llm_scale.py`, which I fetched and ran locally on **2026-09-27** inside
the project venv. Its output matched the committed `research/llm-scale.json`
exactly. Nothing was eyeballed from the prose.

| On screen | Script output | Note |
|---|---|---|
| 175 billion parameters | `gpt3_parameters: 175000000000` | cited, Brown et al. |
| 300 billion tokens | `gpt3_train_tokens: 300000000000` | cited, Brown et al. |
| 3.14 × 10²³ FLOP | `gpt3_train_flops: 3.14e+23` | cited, Brown et al. |
| 0.75 words per token | `assumptions.words_per_token: 0.75` | **labelled "an assumption" on screen** |
| 1,711 years | `reading_years_by_rate["250"]: 1711.2` | rounded |
| 2,139 years | `reading_years_by_rate["200"]: 2138.9` | rounded |
| 2,852 years | `reading_years_by_rate["150"]: 2851.9` | rounded |
| 1,141 years of spread | 2851.9 − 1711.2 = 1140.7 | **computed by me**, not printed by the script |
| 9.95 million years | `compute_years_at_one_billion_per_second: 9950059.57` | rounded |
| 31,557,600 seconds/year | `assumptions.seconds_per_year: 31557600` | Julian year |
| 3.2 × 10²⁴ operations | script prints `3.15576e+24` | **the chapter's rounding**, which I followed; the script's exact value is slightly lower |

Two honest flags on that table: the **1,141-year spread** is my subtraction of two
of the script's own outputs, not a figure the script or chapter prints; and
**3.2 × 10²⁴** follows the chapter's prose rounding of the script's `3.15576e+24`.

The script also reports a 300 wpm rate (1,426.0 years) that the reel does not use;
I kept to the three rates the chapter discusses.

## Constructed vs. real — what is what on screen

- **Real, obtained, dated.** B00's reply is a genuine Claude response (Claude
  Opus 5, 2026-09-27), recorded in full in `claude-response-B00.md`; the screen
  shows a verbatim excerpt headed `REAL REPLY · Claude Opus 5 · 2026-09-27 ·
  verbatim excerpt`, with `…` marking an elision.
- **Deliberately un-run.** B11 (the last slide) shows a prompt for the viewer to
  run, with **no Claude output**. Showing a result there would mean inventing one.
- **Constructed, and shown as such.** B08's ladder uses bracketed placeholders
  (`[impressive number]`, `a rate`) — it is explicitly the method with the example
  removed, not a derivation of anything.
- **Paraphrase, not quotation.** The slogans in B03 and B06 are set in italic
  serif and introduced as things "you have heard" — they paraphrase claims in
  circulation. The chapter's own phrasing is the source. The one thing quoted
  verbatim from the chapter is B05's "more text than a person could read in many
  lifetimes".
- **No fabricated transcripts anywhere.** An earlier cut of this reel had authored
  output lines in both composer beats; both were removed or replaced with the real
  reply. See FRICTIONAL.md, 2026-09-27.

## What Claude contributed

Claude (Claude Code — Opus 5, Opus 5.5 and Sonnet 5, Sept 2026) was used
throughout, and the work divides roughly as follows.

**Claude did:**
- Drafted the beat sheet — narration, `show` blocks, prop values — from the chapter
  section I chose.
- Wrote all six new Remotion scene components
  (`runtime/remotion/src/scenes/DerivationScenes.tsx`: `ScaleAnchorCard`,
  `DerivationLadder`, `AssumptionFan`, `SurvivingClaim`, `ClaimAudit`,
  `BoundaryCard`) and registered them.
- Patched two toolkit scenes with optional, default-off props: `ClaudeComposerAsk`
  (`credit`, for "Created by Ethan Gomes" on the last slide) and `ClaudeTitleOutro`
  (`handle`, `credit` — added for an earlier ending, no longer used by this video).
- Generated the English captions: word timings from the toolkit's `align.py`, cues
  built by `make_captions.py` (included in this folder).
- Checked the narration. **Claude cannot listen to audio**, so every beat was
  transcribed with faster-whisper and compared with the script, and tricky readings
  were checked against Kokoro's own phonemes. That is how "7375" was caught being
  read as "seven thousand three hundred seventy-five". These checks show the words
  are intelligible; they do not show the voice sounds natural. Listening to the
  final cut is my job.
- Wrote `ROOT-REGISTRATION.md` and audited the paperwork against the final video
  (it found PROMPTS.md still listing the removed, authored output lines).
- Diagnosed and fixed the environment failures in FRICTIONAL.md (Pango, the
  Python 3.9 / `onnxruntime` dead end, the conda toolchain corruption, the
  `path_helper` ordering trap).
- Re-derived every figure independently and built the verification table above.
- Ran the visual QC loop: rendered stills, read frames, found and fixed the
  layout and draw-on defects listed in BUILD-LOG.md.
- Produced the genuine reply quoted in B00, and flagged that the earlier authored
  output lines were fabricated transcripts that would fail the assignment.

**I directed:**
- The concept choice and the source chapter.
- The 12-beat structure, runtime target, voice, and reviewing the cut before
  anything was submitted.
- The decision to use a real dated Claude reply rather than labelling a
  constructed one.
- Presentation: addressing viewers as "Students" instead of the toolkit's default
  narrator persona, the `@EthanGomes14` handle, the "Konnichiwa" greeting, the
  on-screen header wording, and the "Created by Ethan Gomes" credit.
- Structure: giving "what this video does not establish" its own screen, ending on
  the Your-turn prompt, and removing the "later models: undisclosed" and "not run"
  labels.
- Wording and credit: rewording B08's closing line (from "= change line 3" to "→ Now
  try other values for the rate"), the spoken credit "This video was created by
  Ethan Gomes from INFO 7375", reading the course number digit by digit, adding
  captions, and naming the file `ethan_gomes_week1_explainer_video.mp4`.

**Nothing in the video is unverified.** Every number traces to the script output
above, and every claim to FACTCHECK.md. I can explain and defend any frame,
any beat-sheet field, and any line of the scene components.

## Third-party assets and licences

No stock media, images, music, or AI-generated imagery. Everything visible or
audible in the video that I did not make comes from the items below. Licences were
checked on 2026-09-27 against the files actually installed, not from memory.

| Asset | Used for | Licence |
|---|---|---|
| **EB Garamond** (The EB Garamond Project Authors), bundled at `runtime/fonts/EB_Garamond` | all serif text on screen | SIL Open Font License 1.1 (`OFL.txt` ships with the font) |
| **macOS system fonts** (SF Pro / SF Mono, Menlo) | sans-serif labels and monospace figures, picked up by the Chromium renderer | Apple's macOS licence; used only as installed system fonts, not redistributed |
| **Kokoro-82M** model weights (hexgrad) — `kokoro-v1.0.onnx`, `voices-v1.0.bin`, voice `am_onyx` | the narration | Apache-2.0 (Hugging Face model card: `license: apache-2.0`) |
| **kokoro-onnx** (thewh1teagle) | runs the Kokoro model locally | MIT (`LICENSE` in the installed package) |

Tools used to build it, not assets in the video:
- **Remotion 4.0.486** (renders the scenes): Remotion License. Free for individuals,
  non-profits and companies of up to 3 people; a company licence is required above
  that. This is an individual student project.
- **faster-whisper** (caption timing and audio checks): MIT. **ffmpeg** (encoding).
- **brutalist.art** toolkit (`github.com/nikbearbrown/brutalist.art`, commit
  `ba2d0e0`, cloned 2026-09-14): the repository has **no licence file**, so no licence
  is stated. It is the course's own public toolkit, used as the assignment directs.

No paid API was called; total cost $0.00.

The six new scene components were written for this assignment and live in the
toolkit tree; copies of `DerivationScenes.tsx` and the patched
`ClaudeComposerAsk.tsx` are included in this folder, with `ROOT-REGISTRATION.md`,
so the video can be rebuilt from a fresh clone.
