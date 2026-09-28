# Sources

This project was built using a hybrid agentic workflow across multiple AI assistants.

## Roles & Contributions

### Human Director (Me)
- Defined the overarching narrative ("Tokens are sealed boxes") and evaluated the pacing.
- Critiqued AI-generated assets, rejecting generic B-roll in favor of custom infographics.
- Directed specific cinematic movements (e.g., "pan left to right from the red X to the green check") to enhance storytelling without violating the rubric.
- Enforced strict adherence to rubric requirements (identifying the missing Boundary statement, fixing the 21 vs 22 data error).

### Claude (Terminal/Code Agent)
- Handled the environment setup and installation of the `brutalist.art` toolkit.
- Executed the actual rendering pipeline (`./art run`) and ran visual QC (GATE V) checks.

### Gemini (Script & Creative Co-pilot)
- Collaborated on refining the `beat_sheet.json` script, fixing timing issues, and translating concepts into visual mechanisms (like `ExecutedData`).
- Wrote and executed complex `ffmpeg` scripts to turn static images into dynamic Ken Burns B-roll videos.
- Mutated JSON configurations to switch TTS voices and adjust component properties.

### ChatGPT (Image Generation)
- Generated the base infographics and conceptual images (B02, B03, B11, B13) based on the script's specific educational needs (e.g., contrasting letter processing vs token processing).

## Third-Party Assets
- **Voice Synthesis:** Kokoro TTS (`am_puck` voice), run locally. (License: Apache 2.0)
- **Visual Framework:** `brutalist.art` (Remotion + Manim). (License: MIT License)
