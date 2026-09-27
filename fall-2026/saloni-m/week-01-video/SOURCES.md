# SOURCES.md

## What I made
- The three runs and two diffs (`run-A.txt`, `run-B.txt`, `run-C.txt`),
  run in my own terminal on 2026-09-27
- The expected-versus-observed comparison in beats B04 and B05, computed from
  my own run output. Claude noticed that my observed 630 matched a figure named
  on the assignment's concept list. I worked out the per-token table and the
  sum-to-zero constraint.
- The choice of builder (`ai-explainer` instead of `cli-explainer`) and the
  decision to ship the review cut with `ART_STRICT=0` (reasons in FRICTIONAL.md)
- Final narration wording, revised from a Claude draft
- The fix decisions at each gate failure: `Text` tick labels instead of
  installing LaTeX, the `ValueTracker` counter in B04, explicit safe-area
  coordinates

## What I used
- Course repository, Chapter 1 and `lessons/01-randomness-and-first-prompts/code/main.py`
  https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai
- Brutalist (Film as Code) toolkit, commit `cd4bf20`
  https://github.com/nikbearbrown/brutalist.art. Licence: the repository has
  no LICENSE file at that commit. Used as directed by the assignment, which
  names it as the course toolkit.
- Brutalist playlist (Film as Code), the first videos, per the assignment
- Assets not made by me, all bundled with the toolkit:
  - Kokoro TTS model and the `am_onyx` voice (downloaded by `./setup`), used
    for all narration
  - Lato Regular and Bold fonts, `runtime/remotion/public/fonts/` (SIL Open
    Font License, licence file shipped alongside)
  - Remotion patterns `ClaudeComposerAsk` (B00, BHTF), `ClaudeVerdictArtifact`
    (BVDT) and `ClaudeTitleOutro` (BOUT), used with my own props
  - The "Liam, in for Bear" narrator persona, the `@NikBearBrown` folder label
    and the outro sign-off. These come from the toolkit's `claude-liam` brand
    (`CLAUDE-BRAND.md`), which requires every Liam reel to introduce the voice
    this way. They are not me claiming to be the instructor, and nobody's
    voice was cloned.
- Manim Community and Remotion, rendering locally
- No stock footage, music, or images

## What Claude contributed
Tool: Claude (Anthropic), used through Claude Code in the desktop app on
2026-09-27. The final review and packaging pass used Claude Opus 5.5.

- Suggested the concept and argued why it fit the rubric
- Drafted the first 6-beat structure and narration
  (`evidence/beat_sheet_draft_v1.json`)
- Pointed out the 630 / 665.24 match with the assignment's concept list
- Drafted the sum-to-zero observation used in B05
- Wrote the five Manim scene classes in `reel/scenes.py` and revised them
  through each gate failure
- Drafted `evidence/verify_claims.py`, `reel/FACTCHECK.md`, `reel/SHOTLIST.md`,
  `reel/PROMPTS.md`, and the templates for README, BUILD-PROMPT, SOURCES and
  FRICTIONAL
- Wrote the props text for the B00 and BHTF composer cards
- Build help: diagnosing the Python 3.13 / PEP 668 / Node 18 setup failures and
  the LaTeX dependency
- In the final pass: cross-checked the folder against the assignment, filled in
  this file and BUILD-PROMPT.md from the build record, corrected inaccurate
  statements (listed in FRICTIONAL.md), and packaged the zip

Commands Claude ran: in this folder, Claude Code ran some commands itself. It
queried the GitHub API for the toolkit's licence, ran short `python3`
one-liners, and ran `evidence/verify_claims.py` and `ffprobe` during the
review. The three run files that the video's numbers come from were produced
in my terminal.

What I did with it:
- Ran the three runs and both diffs myself and checked every figure against them
- Confirmed the sum-to-zero result against my own numbers (7.11e-14)
- Rejected a draft opening that defined pseudo-randomness in the abstract
- Cut the draft's seed-10 "+24.76 overshoot" framing and kept B03 to what
  changes and what does not
- Chose where the boundary statement sits (BVDT and the verdict card)

## Verification
- B02–B05: Manim animations whose figures are typeset from run-A/B/C.txt
  (2026-09-27) and re-checked against a fresh run by `verify_claims.py`, 7/7.
  They are **not** screen recordings; the video has no terminal capture.
- B01: the generator diagram is constructed and labelled CONSTRUCTED
  ILLUSTRATION on screen. The two source lines in it are real.
- **B00 is a Claude-style interface, not a real Claude response.** The stock
  `ClaudeComposerAsk` pattern draws a composer box with a model chip and three
  "output" lines under `@NikBearBrown`. The prompt and those lines are props
  written for the video. They summarise the video's own findings and are not
  a conversation with Claude. The frame has no on-screen label saying this,
  because it was rendered before the issue was caught.
- BVDT and BHTF are likewise stock pattern cards with authored text.
- No real Claude transcript appears in the video.
- Not verified:
  - Whether the 35-count shortfall is sampling noise or bias
  - Reproducibility of `random.Random` on other platforms or Python versions
  - Whether `Counter` key order is guaranteed
