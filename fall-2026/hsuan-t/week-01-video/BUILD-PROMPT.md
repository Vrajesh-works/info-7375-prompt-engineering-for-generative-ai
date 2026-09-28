# Build Prompts

This file documents the key prompts and instructions used to guide the AI agents during the creation and refinement of this video. They demonstrate an iterative, "director-style" workflow rather than zero-shot generation.

## 1. Script & Pacing Adjustments
> "Is my current script too long? Does it exceed four minutes? Because the requirement is 2 - 4 mins... ok, help me update beat_sheet.json and record the changes in frictional.md."
* **Purpose:** Directed the AI to audit the video duration and execute surgical cuts (removing redundant examples) to meet the strict time constraint.

## 2. Visual Directing & Critiquing AI
> "This is the B02 image I just generated. Doesn't this avoid looking like a static display? But I feel mine is better than yours, your B02 video had absolutely nothing to do with the topic."
* **Purpose:** Rejected the AI's generic stock footage generation and provided a custom ChatGPT-generated infographic that actually illustrated the "Myth vs Reality" concept.

## 3. Cinematic Camera Direction
> "Can you pan the camera left and right? Because the left side is an 'x' and then it transitions to the right side which is a 'check mark'?"
* **Purpose:** Directed the AI to write an `ffmpeg` script that specifically panned horizontally across the infographic, perfectly timing the visual transition with the narration.

## 4. Tone and Voice Selection
> "Can we change the voice for this project? Change it to a more energetic narration, something with the excitement of discovering a hidden secret?"
* **Purpose:** Pushed beyond the default TTS voice (`am_onyx`) to find a voice (`am_puck`) that matched the emotional tone of debunking a myth, drastically improving viewer engagement.

## 5. Build Commands
To rebuild this project from scratch, the following command was executed in the terminal:

```bash
# Execute the rendering pipeline and visual QC checks
./art run
```
