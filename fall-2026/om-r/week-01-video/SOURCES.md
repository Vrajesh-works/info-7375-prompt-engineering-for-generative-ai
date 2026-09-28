# SOURCES — low-temperature-is-not-argmax

## Course material used

- **Chapter text:** `chapters/01-randomness-and-first-prompts.md`, from
  `nikbearbrown/info-7375-prompt-engineering-for-generative-ai`. The concept
  ("low temperature is not argmax") comes from a passage in this chapter that
  is not on the assignment's example list — permitted explicitly by the
  assignment ("If you want a concept not on this list, that is fine — it just
  has to come from Chapter 1").
- **Reference implementation:** `lessons/01-randomness-and-first-prompts/code/main.py`
  from the same repo. `probabilities()` and `sample()` are reproduced verbatim
  in `demo.py` and shown verbatim on screen in the B03 code beat.

## What is real vs. constructed

Every number that appears on screen or in narration was captured by actually
running `demo.py` — none were invented or estimated:

| Claim shown | Real captured value |
|---|---|
| `probabilities([1,2,3], temperature=0)` | raises `ValueError: Need logits and a positive finite temperature` |
| `sample([1,2,3], count=1000, seed=7, temperature=0.5)` | `{0: 18, 1: 133, 2: 849}` — matches the chapter's own published table exactly |
| assigned probabilities at T=0.5 | 1.6% / 11.7% / 86.7% |
| `sample([1,2,3], count=1000, seed=7, temperature=0.1)` | `{2: 1000}` (used only in `FACTCHECK.md` (in the GitHub repo), not shown running on screen) |
| `sample([1,2,3], count=1000, seed=7, temperature=0.001)` | probabilities round to exactly `[0.0, 0.0, 1.0]` — float underflow |

**`argmax_select()`** (in `demo.py` and `scenes.py`) is a function I wrote
myself for this video. It is explicitly labeled on screen — "CONSTRUCTED FOR
THIS VIDEO — not part of the reference implementation" — because it is not
part of the chapter or the lesson's code. It exists only to give the video a
real, run contrast to a genuinely deterministic operation, instead of
asserting what determinism would look like.

No Claude chat transcript appears anywhere in this video. The Claude-styled
composer beats show real shell commands and their real captured terminal
output, not a Claude conversational reply — there was nothing to date or
verify in that sense, since nothing shown is a model output.

## What Claude contributed

Claude contributions came from two sessions: planning, concept selection,
beat sheet drafting, narration wording, and build troubleshooting were done
via claude.ai (Claude Sonnet 5); the actual toolkit build, gate-failure
diagnosis, and file edits were carried out by Claude Code (Claude Opus 5.5).

- Helped identify the off-list concept by reading the chapter text directly
  and locating a passage not covered by the instructor's example list.
- Drafted the beat sheet (`beat_sheet.json`), narration wording, and the
  Manim scene code (`scenes.py`) for beats B04 and B06.
- Wrote `demo.py`, including the `argmax_select()` contrast function.
- Diagnosed and proposed fixes for every build failure logged in
  `FRICTIONAL.md` (a missing-dependency and toolkit-bug list, plus multiple
  Brutalist QA gate failures).
- **Caught a factual error in my own first-draft narration**: the original
  claim "temperature never produces zero variance" is false. Claude Code
  ran the reference implementation at additional temperatures
  (T=0.1, T=0.001) as part of the toolkit's mandatory pre-final fact-check
  step, found that low temperatures both routinely produce and can
  literally float-underflow to zero variance, and proposed the corrected
  wording used in the final video. See `FACTCHECK.md` in the GitHub repo for the full record.
  I reviewed, approved, and in one case (B09) further corrected the proposed
  wording myself before it was finalized.
- All final wording, structural choices (e.g., which beat to swap components
  on, how to handle the removed bookend beats), and the decision to accept
  each fix were mine.

## Third-party assets

- **Icons:** `zap.svg`, `target.svg`, `list-checks.svg`, `check-circle.svg`
  from Brutalist's own bundled icon set (`icons/svg/` in
  `nikbearbrown/brutalist.art`), used in the B01 `FormBCard` beat. These are
  part of the toolkit itself, not third-party assets brought in externally.
- **Voice:** Kokoro `am_onyx`, the toolkit's bundled local/free TTS voice —
  no ElevenLabs, no paid narration service.
- **Fonts:** Oswald (bundled by Brutalist's own `./setup --install`), used via
  an explicit font override in `scenes.py` to work around a text-shaping bug
  (see `FRICTIONAL.md`).
- No other external media, stock footage, AI-generated images, or archival
  material appears in this video.

## Toolkit note

Brutalist (`nikbearbrown/brutalist.art`) was used per the assignment's
instructions: cloned fresh, free pipeline only (Kokoro + Manim + Remotion),
no API keys, no paid generation. Two toolkit-level bugs were worked around
locally without modifying any shared toolkit source file — see
`FRICTIONAL.md` for details (a missing `form-b-icons` asset folder, and the
toolkit's own `cli-explainer` worked examples hardcoding the instructor's
persona/channel branding, which was replaced with neutral content for this
submission).
