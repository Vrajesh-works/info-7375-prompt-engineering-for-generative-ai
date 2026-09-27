# SOURCES — A Chatbot Is a Loop. (Aditya Raj · INFO 7375 · Week 1)

## What I made (in this folder)
| Item | What it is |
|---|---|
| `beat_sheet.json` | The reviewed narration and visual plan (17 beats) |
| `evidence/run_experiments.py` | Runs the local model and records every number used in the video |
| `evidence/runs/*.json` | The recorded runs + `manifest.json` (SHA-256 of each file, environment) |
| `evidence/sample_review.json` | Manual review of the sampled answers that mention George Eliot (a judgment, labelled as such) |
| `evidence/claude-response/` | My claude.ai screenshot (2026-09-27, Opus 5.5) + its verbatim transcript and SHA-256 — the source of B13 |
| `evidence/verify.py` | One-command check: hashes, full re-run, every on-screen and spoken number |
| `fill_props.py` | Writes every data prop in the beat sheet from the evidence (no hand-typed numbers) |
| `pad_audio.py` | Adds the lead/tail silences the toolkit documents but does not implement |
| `toolkit-additions/` | The Remotion scenes written for this video + a patch against the toolkit |
| The rendered video | `Raj_Aditya_INFO7375_Week01_Video.mp4` |

## What Claude contributed
Built with **Claude Code (model: Claude Opus 5.5)** as the build agent, on 2026-09-26/27.
- **Claude:** drafted the narration and beat sheet; proposed the six novelty ideas; wrote all code
  (experiments, verification, the 11 Remotion scenes, the padding and props scripts); ran the local model;
  looked up and checked the outside facts; ran the renders and the frame-by-frame visual QC; drafted the paperwork.
- **Me (Aditya):** chose the concept; set the constraints (Kokoro am_onyx, stop at review before submission,
  3-minute target); ran the installer and MacTeX steps that needed my password; approved ideas 1–5 and skipped 6;
  ran the real claude.ai prompt shown in B13; reviewed the cut. I can explain every claim — see FACTCHECK.md.
- No Claude output is shown as if it were something else: the answers in B00–B11 are SmolLM2's (labelled);
  B13 is a real claude.ai response I received, verbatim, with its date.

## Tools and assets I did not make
| Item | Use | Licence |
|---|---|---|
| Brutalist toolkit — github.com/nikbearbrown/brutalist.art @ `6a8380a` | Pipeline, bookend scenes, fonts, logo | No licence file in the repo; used as the course toolkit |
| SmolLM2-135M-Instruct (Hugging Face, `HuggingFaceTB/SmolLM2-135M-Instruct` @ `12fd25f7`) | The model under test | Apache-2.0 |
| Kokoro-82M (`hexgrad/Kokoro-82M`) voice model, voice `am_onyx` | Narration | Apache-2.0 |
| kokoro-onnx 0.6.1 | Runs Kokoro locally | MIT |
| Remotion 4 | Renders every scene | Remotion Free License (individuals) |
| PyTorch 2.14, Transformers 5.17 | Run the model | BSD-3-Clause / Apache-2.0 |
| matplotlib 3.11 (via the toolkit's `typeset_math.py`) | Typesets the B11 equations | Matplotlib licence (PSF-based) |
| faster-whisper | Word timings for on-cue reveals | MIT |
| EB Garamond (bundled with the toolkit) | Serif type | SIL Open Font License |
| Bear Brown logo (`logos/bear-brown/bear-brown-logo-1.svg`, from the toolkit) | Corner mark | Toolkit asset |

## Facts from outside sources (all accessed 2026-09-27)
- Paris population 2022 = 2,113,705 — INSEE, *Populations de référence 2022, Ville de Paris* (January 2025),
  https://www.insee.fr/fr/statistiques/fichier/8290080/PopRef2022_dep75_VILLE%20DE%20PARIS.pdf
- `end_turn`: "The most common stop reason. Indicates Claude finished its response naturally." — Anthropic,
  *Stop reasons and fallback*, https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- `temperature`: "Amount of randomness injected into the response. Defaults to `1.0`." — Anthropic, Messages API
  reference, https://platform.claude.com/docs/en/api/messages
- Middlemarch by George Eliot (1819–1880), published 1871–1872 — Project Gutenberg eBook #145,
  https://www.gutenberg.org/ebooks/145
- Nobel Prize in Literature first awarded 1901 — Wikipedia, "Nobel Prize in Literature" (nobelprize.org refused the request)
- George Eliot's name recorded as "Mary Ann Evans (…; alternatively Mary Anne or Marian)" — Wikipedia, "George Eliot"
- Pulitzer Prizes first awarded 1917; fiction prize "for distinguished fiction by an American author" —
  Wikipedia, "Pulitzer Prize" (pulitzer.org refused the request)

## Context
- The course's own Chapter 1 film illustrates next-token prediction with a constructed probability table
  (flagged in the toolkit's `reports/isdone-2026-09-11/AUDIT.md`, item 09). This video uses measured
  distributions instead and labels its one constructed diagram (B02) on screen.
- The 60-second pilot this video grew from: `~/Desktop/Brutalist/my-videos/youtube/claude-liam-next-token-loop/`
  (not submitted; described in FRICTIONAL.md).
