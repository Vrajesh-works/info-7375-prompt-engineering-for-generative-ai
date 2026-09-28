# SOURCES.md

**Student:** Yudan (Anica) Zhou · INFO 7375 Week 1 Explainer Video

## What I used (did not make)

| Source | Where | Licence / terms | How it is used |
|---|---|---|---|
| Course reference implementation `probabilities()` / `sample()` | `lessons/01-randomness-and-first-prompts/code/main.py`, [info-7375 repo](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai) | repository `LICENSE` | Imported unmodified by my evidence script; its output is the video's subject. |
| Chapter 1, Part 2, "The subtraction that changes nothing important" | `chapters/01-randomness-and-first-prompts.md` | same repo | Source of the concept, the cancellation identity, the `[1000, 1000]` test case, and the warning to keep the claim narrower than "numerically stable." |
| Brutalist toolkit (`ai-explainer` builder, Remotion scene library, brand assets) | [brutalist.art](https://github.com/nikbearbrown/brutalist.art), commit `cd4bf20904be4e7d63babd9622b17963c2361b27` | repository licence | Produced the video. I wrote no Remotion or Node code. |
| Kokoro-82M ONNX voice model (`am_onyx` / `af_bella`) | [kokoro-onnx releases](https://github.com/thewh1teagle/kokoro-onnx) | Apache-2.0 (model weights: see upstream) | **Synthetic narration.** The voice is not mine, is not Professor Brown's, and implies no endorsement. |
| Fonts installed by `./setup` (Oswald and the toolkit's bundled families) | Google Fonts / toolkit | OFL | On-screen type. |
| Python standard library (`math`, `random`, `decimal`, `json`, `platform`) | — | PSF | All computation. |

No paid service, API key, media account, or direct Claude API call was used.
Nothing was published to YouTube.

## What I made

- `evidence/max_subtraction_evidence.py` — the three cases (agreement on
  moderate scores, overflow on `[1000, 1000]`, underflow at `[0, -1000]`) and
  the decision to include the `decimal` comparison so the on-screen
  `5.07595889755E-435` is reproducible rather than asserted.
- `SCRIPT.md` — the concept choice, the beat order, the narration, and the list
  of claims I must be able to defend.
- The judgement about what the video does **not** establish, and the decision to
  spend a beat on it rather than end on the `[0.5, 0.5]` result.
- `README.md`, `BUILD-PROMPT.md`, this file, and `FRICTIONAL.md`.

## What Claude contributed

Claude was used throughout, as the assignment permits — Claude Opus 5 on
2026-09-21 (drafting the scaffold in a Linux container) and Claude Opus 5.5 via
Claude Code on 2026-09-27 (the actual toolkit install, build and render on my
Windows machine, in sessions I directed step by step).

Claude:

- read the syllabus, the Canvas brief, Chapter 1 and the prerequisite guides, and
  summarised the deliverables and rubric for me;
- ran the lesson's `main.py` and confirmed it reproduces the chapter's tables on
  my machine;
- proposed three candidate concepts with their evidence and their boundaries —
  **I chose max-subtraction**;
- found the `[0, -1000]` underflow case, which became my "what this does not
  establish" beat;
- drafted `evidence/max_subtraction_evidence.py`, `SCRIPT.md`, `README.md`,
  `BUILD-PROMPT.md` and this file;
- diagnosed and worked around the Windows blockers (long paths, Python 3.14,
  the ElevenLabs guard, the npx shim) and recorded them;
- wrote `ArrayPipeline.tsx`, `build_sheet.py` and `cue_times.py`, and ran the
  render, frame QC and gates.

**What I did that Claude could not.** I watched the full review cut with sound
and caught that Kokoro read "INFO 7375" as a single number — Claude checked
frames all evening but cannot hear audio, and said so. I also judged the arrows
too faint, decided to shorten B01 rather than pass `ART_STRICT=0`, declined to
install EB Garamond system-wide, and accepted B06's small cells rather than
re-render.

**What I decided.** The concept. The neutral student framing instead of the
toolkit's default channel identity, so the reel does not present itself as the
instructor's. That the video ends on the limitation rather than on `[0.5, 0.5]`.
That the evidence file records my own Windows run rather than the scaffold's
Linux one.

Claude did not write my `FRICTIONAL.md` entries for 2026-09-27 evening — it
declined to invent an expectation or a reflection, saying those should be my
words — and did not watch the video or judge whether it teaches.

## Responsibility

I am responsible for this submission. I can explain the cancellation identity,
why `[1000, 1000]` raises rather than returns, why case C's `0.0` is a
floating-point result rather than a probability, and what the video does not
establish.
