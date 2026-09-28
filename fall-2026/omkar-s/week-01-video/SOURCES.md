# SOURCES — Week 1 video: "Subtract the Max"

## What I used (not made by me)

| Item | Where | How it was used | Licence / terms |
|---|---|---|---|
| Chapter 1, "The subtraction that changes nothing important" | `chapters/01-randomness-and-first-prompts.md`, course repo `nikbearbrown/info-7375-prompt-engineering-for-generative-ai` @ `e6c6c49` | The concept, and the framing of the limit ("keep the tested claim narrower than 'numerically stable'"). Paraphrased, not quoted on screen. | Course repo, MIT (LICENSE in repo) |
| `probabilities()` from `lessons/01-randomness-and-first-prompts/code/main.py` | same repo | Shown on screen in B00 (excerpt, input checks elided, one line wrapped, both labelled); imported by my evidence script | MIT |
| `lessons/01-randomness-and-first-prompts/code/tests/test_main.py` | same repo | test_02's assertion and its `… ok` result shown in B05 | MIT |
| Brutalist toolkit | `github.com/nikbearbrown/brutalist.art` @ `6a8380a` | Audio pipeline (`generate_audio_kokoro.py`), compile (`./art run` / `./art final`), QC gates (A, B, W, V) | No LICENSE file in this checkout; used as the course instructs, not redistributed |
| Kokoro-82M voice model + `kokoro-onnx` | model files from `thewh1teagle/kokoro-onnx` releases (model-files-v1.0), fetched by `./setup --install` | Synthetic narration, voice `af_bella` | Kokoro-82M: Apache-2.0; kokoro-onnx: MIT |
| Manim Community 0.18.1 | PyPI | Renders every visual beat | MIT |
| Fonts: EB Garamond (bundled with Brutalist); Menlo, Helvetica Neue (macOS system fonts) | local | On-screen type | EB Garamond: SIL OFL (OFL.txt in toolkit); Menlo / Helvetica Neue: Apple system fonts, rendered into the video, not redistributed |

No third-party images, video, music, sound effects or stock footage are used. No paid service, API key or AI video generation was used. Nothing was uploaded.

## What I made (for this submission)

- `evidence/max_shift_evidence.py`: compares the course's `probabilities()` with a naive softmax on four hand-chosen inputs. Its output, `evidence/max_shift_output.txt`, is the source of every number on screen that isn't from `main.py` or the tests.
- `beat_sheet.json` (narration + visual plan), `scenes.py` (one Manim scene per beat), and the paperwork (`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `BUILD-PROMPT.md`, `FRICTIONAL.md`, this file).
- All four score lists ([1,2,3], [1001,1002,1003], [1000,1000], [0,−1000]) are **constructed inputs**, and each is labelled that way on screen where it first appears. [1,2,3] and [1000,1000] come from the chapter and tests; [1001,1002,1003] and [0,−1000] were chosen to show overflow and underflow.

## What Claude contributed

Honest split: Claude Code (Claude Opus 5.5, in the Claude desktop app, 2026-09-24) did most of the production work when I asked it to "complete the assignment":
- It found and cloned the course repo and the toolkit, installed the dependencies, and debugged the setup (see FRICTIONAL entries 3–4).
- It proposed the concept.
- It wrote `max_shift_evidence.py`, the entire narration and beat sheet, all of `scenes.py`, and the first drafts of every Markdown file.
- It ran the gates, fixed the layout defects they found, and inspected rendered frames.
- It caught and corrected one factual error of its own ("17th" → "16th" significant digit).

What I am responsible for: checking every FACTCHECK row against the evidence files, watching the full video with sound, requesting at least one revision, and being able to explain every claim. My review is FRICTIONAL entry 5.

## Claude responses shown in the video

None. The video contains no Claude transcript, no reconstructed Claude interface, and no Claude output presented as evidence. The narrator is a synthetic Kokoro voice and says so (B00 label, B08 narration and card). It does not claim to be me, Professor Bear, or anyone else.
