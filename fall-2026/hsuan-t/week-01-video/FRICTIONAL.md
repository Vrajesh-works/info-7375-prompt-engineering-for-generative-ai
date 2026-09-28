# Frictional.md — the-unit-is-token-not-word

Scope: this video only. Backfilled 2026-09-23 when this scope was registered with friction-log.

---

### 2026-09-21 — Research before writing the script

**What I tried**
Picked a topic — language models operate on tokens, not words, and that's why they botch letter-counting ("how many r's in strawberry") — and did real research before writing any narration, instead of just going off memory.

**What happened**
Ran an actual tokenizer against a handful of test strings rather than guessing. The word "strawberry" on its own splits into a few pieces, as most people expect — but the same word with a leading space, which is how it actually appears mid-sentence, collapses into a single, unsplittable token. That's a sharper and less obvious fact than the usual "str-aw-berry" explanation, and it became the spine of the whole script.

**What I learned**
Checking real behavior before writing, even for a topic that feels already-understood, turned up a better and more surprising angle than the common explanation would have.

**What I'll change next**
Build the beat sheet and script around the mid-sentence single-token finding.

---

### 2026-09-21 — Building the review cut: Render crash & Visual QC warnings

**What I tried**
Wrote the full 18-beat script and narration, then ran `./art run` to compile a review cut.

**What happened**
Initially, one beat crashed on render because a visual component expected a list of values but got a single text string instead. I fixed the mismatch and re-rendered. The video then successfully compiled (~3:44). 
However, the system automatically ran its visual quality check (GATE V) right after, flagging 16 MAJOR warnings for "underfill". 

- B02, B03, B04, B11, B12, B13 were plain text SLATEs with too little text, leaving >50% of the screen empty.
- B01 and B15 used real components, but the text was so short it looked tiny on screen.

**What I learned**

The automated GATE V check is strict about visual density. It flags plain SLATEs and sparse text because the system considers the frame "too empty/dry."

**What I'll change next**
Instead of just enlarging the text, I will replace those boring SLATE beats (B02-B04, etc.) with real visual components (like `ExecutedData` or animations) to satisfy both the GATE V density check and the assignment's "Show the mechanism" rubric requirement.

---

### 2026-09-23 — Script refinement and visualizing mechanisms

**What I tried**
Critiqued the script draft with my AI assistant. I pointed out that the narration was too academic, failed to explain *why* AI uses tokens instead of letters, and that the BPE explanation was hard to visualize as an empty SLATE.

**What happened**
Through an iterative back-and-forth, we overhauled the script's flow. I directed the AI to insert a new beat answering "why not letters" (speed vs precision) and to rewrite the abstract concepts into intuitive metaphors (like tokens being "sealed boxes"). 
To fix the GATE V warnings and meet the rubric's "Show the mechanism" requirement, we brainstormed ways to replace the SLATEs. We settled on using `ExecutedData` tables to visually compare letters merging into tokens (`t+h -> th`) and contrasting processing speed (22 letter steps vs 5 token steps).

**What I learned**
1. Agentic iteration works best as a tennis match. The AI can generate the JSON/code, but as the director, I had to catch the pacing issues and demand deeper technical explanations.
2. Leveraging generic components like `ExecutedData` for side-by-side comparisons is a highly effective way to turn abstract text into vivid visual mechanisms, bypassing the need for custom animation code.

**What I'll change next**
Run `./art run` again to compile the updated `ExecutedData` animations and verify that the GATE V "underfill" warnings are resolved.

---

### 2026-09-27 — Timing audit and Rubric alignment

**What I tried**
Ran a script to sum the exact durations of the synthesized audio files because the pacing felt slow. I realized the video was ~4m11s, which exceeds the assignment's strict 4-minute maximum constraint. I also audited the script against the rubric and realized the required "boundary statement" was missing.

**What happened**
I aggressively trimmed the redundant "Generalize" and "Nuance" beats (which had overlapping information with the Recap beat), saving about 33 seconds. In their place, I inserted a new 10-second beat to explicitly fulfill the rubric's "Name one thing the explanation does not establish" requirement, stating that this explanation does not establish whether future AI architectures will abandon tokens entirely.

**What I learned**
1. Trusting my intuition on pacing was crucial. Measuring the actual synthesized audio duration caught a rule violation early.
2. Cutting redundant examples (like the prompting bypass) actually makes the core mechanism (the code bypass) hit much harder.

**What I'll change next**
Fill in the beats that lack visuals by generating custom images with AI.

---

### 2026-09-27 — Visual Polish: Replacing SLATEs with Custom B-roll

**What I tried**
After running a compilation, I reviewed the contact sheet and noticed several conceptual beats (B02, B03, B11) were still rendering as "needs-fill" SLATE prompts requesting human-provided AI video clips. I initially considered replacing them with simple text cards to avoid the error.

**What happened**
I realized that converting everything to text cards would make the video look like a PowerPoint presentation and violate the "no static slides with voiceover" rubric. Instead, I generated custom infographics (e.g., a diagram contrasting letter-by-letter reading vs token processing) and conceptual images (a sealed box for B11). Then, I directed my AI assistant to use `ffmpeg` to apply a cinematic Ken Burns effect (like panning left-to-right from a red 'X' to a green 'check'). This turned static images into dynamic B-roll video clips. I placed them in the `media/` folder, allowing the system to seamlessly stitch them into the final render.

**What I learned**
1. Static text cards are boring. Pairing custom infographics with subtle camera movements drastically elevates the documentary feel without requiring complex video generation models.
2. During this visual review, I also caught a subtle data error: the string "the strawberry is red" is exactly 21 characters and 4 tokens (without a period), not 22 and 5. Correcting this in the `ExecutedData` component preserved the integrity of the "Use real data" rubric requirement.

**What I'll change next**
Run `./art run` one final time to compile the master cut and verify all content is correct.

---

### 2026-09-27 — Audio Polish: Switching TTS voice for better engagement

**What I tried**
After finalizing the visuals, I listened to the audio track and felt the narration was too dry. The default voice (`am_onyx`) is designed for serious, analytical teardowns, which didn't match the "revealing a hidden secret" vibe of my script.

**What happened**
I directed the AI to swap the text-to-speech voice across all beats in the `beat_sheet.json` from `am_onyx` to `am_puck`. The `am_puck` voice offers a more energetic, youthful, and enthusiastic tone that perfectly fits the script's intention of debunking a myth and showing the audience something surprising. The system automatically regenerated the MP3s on the next compile.

**What I learned**
Voice selection drastically alters the perceived pacing and engagement of a video. A serious voice makes the technical content feel like an academic lecture, whereas an energetic voice makes the exact same content feel like an engaging YouTube explainer.

**What I'll change next**
Run the final compilation with the new voice and submit the project.

---

### 2026-09-27 — Re-render after the visual/audio pass: one real content bug found, and a new set of BLOCKER defects

**What I tried**
Asked for a fresh `./art run` after the voice switch and the newly supplied B-roll clips, flagging that narration text had changed again and video for the missing beats had been filled in.

**What happened**
Same class of problem as the first pass: the script edit had outpaced the audio again, and this time a full beat (B03) had no audio file at all, so the run refused outright before rendering anything. Regenerated all narration, then re-ran. All 17 beats came back filled — the "needs a human-supplied clip" placeholders are gone. Checked each filled beat against its current narration by actually looking at the frames (not just trusting the fill status), and the content lines up correctly across the board — my earlier worry that B12/B13 might have drifted out of sync with their reworded narration turned out to be unfounded.

One real bug did turn up, and it wouldn't have been caught by the automated checks: the outro beat (now renumbered to B16 after the "Your Turn" beat was cut) reused a leftover render file from when that same beat number belonged to a different beat. The video kept showing the old "Your Turn" screen, chopped down to 2 seconds, while the new outro narration played over it. GATE V's checks don't catch this kind of thing — they measure layout, not whether the scene is even the right one — so it took actually pulling a frame from the exported video to see it. Deleted the stale file and re-rendered just that beat; it now shows the correct outro card.

Separately, the visual QC check came back worse than the last pass: 8 blocking defects (up from zero), all on the newly supplied clips — content spilling past the safe frame edges on four of them, and one with text that's hard to read against its background. The long-standing sparse-text warnings on the BLUF and recap beats are still there too, untouched since the first draft.

**What I learned**
A script edit that adds, removes, or renumbers a beat needs a full audio regeneration every time — partial edits keep causing the same desync bug. Also: reusing a beat number for different content is risky specifically because none of the automated gates check "is this the right scene," only "does a file exist" and "does it look reasonably composed" — that gap has to be caught by eye.

**What I'll change next**
Fix the 4 clips with edge-bleed and the 1 with low contrast, and finally address the BLUF/recap beats that have been flagged since the very first draft.
