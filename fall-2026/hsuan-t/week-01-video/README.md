# Week 1 Explainer Video

* **Name:** Hsuan T.
* **Concept Chose:** The unit is a token, not a word — and why that breaks letter-counting prompts.
* **Why I chose this:** I chose this concept because understanding how an LLM parses text into chunks (tokens) rather than human letters is the most fundamental step to demystifying why these seemingly intelligent models fail at simple character-counting tasks.
* **Runtime:** 3 minutes 57 seconds (03:57)

## How to Rebuild
To rebuild this video from the source files using the `brutalist.art` toolkit, follow these steps:

1. Ensure you have the `brutalist.art` toolkit cloned and its dependencies installed on your local machine.
2. Replace the contents of the default `brutalist.art` folder with the files in this directory (specifically `beat_sheet.json` and the Markdown files).
3. Open your terminal, navigate to the root of the project, and execute the rendering pipeline:
   ```bash
   ./art run
   ```

## Repository Structure & File Overview
Here is a quick guide to the essential files included in this project to fulfill the rubric requirements:

* `beat_sheet.json` — The core narrative script, timing, and visual plan for the video.
* `BUILD-PROMPT.md` — Documents the key prompts and commands used to guide the AI agents in generating and refining the video.
* `SOURCES.md` — Details the hybrid agentic workflow, listing human contributions, Claude/Gemini/ChatGPT contributions, and third-party asset licenses.
* `FRICTIONAL.md` — An honest, dated log of the technical frictions encountered during the Brutalist build process and how they were resolved.
* `the-unit-is-token-not-word-slate.mp4` — The final rendered explainer video (packaged in the Canvas ZIP submission, ignored by Git).
* `qc-sheet.png` / `_qc/` — Visual quality control checks generated during the build pipeline.
