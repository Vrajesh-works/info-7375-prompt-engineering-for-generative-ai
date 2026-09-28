# SOURCES — Subtract the Max

## What I used

| Source | Used for | Licence / terms |
|---|---|---|
| INFO 7375 Chapter 1, *Randomness and first prompts* (`research/01-randomness-and-first-prompts.md`, course repo [nikbearbrown/info-7375-prompt-engineering-for-generative-ai](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai) @ `149c8e7`) | The concept and the constructed example `[1, 2, 3]` | Course material |
| `lessons/01-randomness-and-first-prompts/code/main.py` (same commit, sha256 `df9940ca…43e5d`) | `probabilities()`: every "shifted"/main.py number in the video. Copied **unchanged** into `code/main.py` | Course repo licence |
| `lessons/01-randomness-and-first-prompts/code/tests/test_main.py` | Input `[1000, 1000]` (test_02) and the "Ran 6 tests, OK" result | Course repo licence |
| [brutalist.art](https://github.com/nikbearbrown/brutalist.art) @ `cd4bf20904be4e7d63babd9622b17963c2361b27` | Kokoro narration script, Remotion scenes `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `ClaudeVerdictArtifact`, `compile.py` assembly | See repo; one local Windows patch (below) |
| Kokoro-82M via kokoro-onnx 0.6.1, voice `am_onyx`; model files from the [kokoro-onnx releases](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0) | Synthetic narration: the voice is **not** Siddi's and not a person's | Apache-2.0 |
| Manim Community 0.19.1 | Body beats B02–B06 and outro | MIT |
| matplotlib 3.11.2 mathtext (STIX fonts) | Equation typesetting (no LaTeX) | matplotlib licence; STIX: OFL |
| Fonts bundled in brutalist.art: EB Garamond, Lato, PT Mono | On-screen type | SIL OFL 1.1 |
| Python 3.13.2 `math`, `decimal` | All computed values | PSF |

No stock footage, music, images, or third-party media were used.

## What I made

- `code/evidence.py`: runs the course's `main.py` next to a direct (un-shifted) softmax and writes `code/evidence.json`
- `scenes.py`: every Manim scene; each number is read from `evidence.json`
- `beat_sheet.json`: narration and visual plan
- `render_manim.sh`, `build/*`: rebuild scripts, the Windows environment, and the patch

## Which inputs are constructed

| Input | Origin | Labelled on screen as |
|---|---|---|
| `[1, 2, 3]` | Chosen by the chapter; no model produced it | "constructed input (Chapter 1)" |
| `[1000, 1000]` | The lesson's test file, test_02 | "lesson test input · test_02" |
| `[1001, 1002, 1003]` | Constructed for this video | "constructed input" |
| `[0, -1000]` | Constructed for this video | "constructed input" |

All outputs shown are real printed values from `code/evidence.py` (Python 3.13.2, Windows 11). The
footer date on each body beat is the date that run happened.

## Claude

- **No Claude response appears in the video.** The two composer frames (B00, BHTF) are the Brutalist
  mock composer. B00 shows a question and the real `python main.py` output, and says "no Claude reply
  shown"; BHTF shows a suggested prompt for the viewer. Both carry the chip "Mock composer · not a real
  session".
- **What Claude (Claude Code, Opus 5.5) contributed:** recommended the concept (Siddi chose it); wrote
  `evidence.py`, the Manim scenes, the beat sheet and narration draft, and the drafts of README, BUILD-PROMPT,
  SOURCES and FRICTIONAL; did the Windows install/debugging and the frame-level QC fixes listed in
  FRICTIONAL.md.
- **What Siddi did:** chose the concept, submission name and course repo; directed the session; made
  the build decisions recorded in FRICTIONAL.md (final built despite the kerning false positive, MP4 on
  Canvas per the repo's rule); reviewed the opening shot and asked for the greeting change to
  "Namaste"; is responsible for every claim in the video.

## Local toolkit changes (not upstream)

- `runtime/scripts/remotion_scenes.py`: resolve `npx` with `shutil.which` (Windows needs `npx.cmd`).
  See `build/remotion_scenes-windows-npx.patch`.
- `manim` pin relaxed from `<0.19` to `0.19.x` for Python 3.13 (`build/requirements-win.txt`).
- Brutalist defaults deliberately **not** used: the "Liam, in for Bear" persona, the `@NikBearBrown`
  chip, and `ClaudeTitleOutro` (it hardcodes that handle). This is a student submission; the course's
  Brutalist prerequisite notes that channel credits don't authorize a student to present as the instructor.
