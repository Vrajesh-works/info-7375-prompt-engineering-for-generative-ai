# PROMPTS — beat-prefixed prompts

There are **no open slots**. No beat waits on human-supplied or generated media, so
there are no pantry or generation prompts to list. Every visual is a local Remotion
scene driven by `evidence/preference_toy_output.json`.

For traceability (the ASK → RESULT idea), these are the plain-language requests that
produced each custom scene. They were given to Claude Code in this build session;
the exact scene code they produced is `src/scenes/PrefTune.tsx.txt` in this folder.

| Beat | Request that produced the scene |
|---|---|
| INTRO | Shubham's request after watching: "add intro to start saying today we will be discussing about the pref tuning topic". Built as: "Hi, I'm Liam" greeting that cross-fades into "Today's one idea, from Chapter 1 → Preference Tuning. Why it can prefer a confident wrong answer", each landing on its spoken words; synthetic-voice footer. |
| B00 | Two reply cards for "What is the capital of Australia?": hedged-correct A and confident-wrong B, tagged on the spoken words; a preference bar slides from 50/50 to the toy's final 32.6/67.4; CONSTRUCTED pill; synthetic-voice disclosure. |
| B01 | Library `BrutalistHesitantWriter`: type "Preference tuning rewards the correct answer", reconsider "correct", replace it with "preferred". |
| B02 | Two stage cards from Chapter 1 / Figure 1.3 (pre-training target, preference-tuning target); an ANSWER KEY card that stops outside both, stamped "not an input". |
| B03 | Show the real `nudge()` source (docstring trimmed and labelled); highlight the `probabilities()` line, then the `+=`/`-=` lines, then box each argument; a struck `answer_key` callout *below* the code. |
| B04 | Ten reviewer figures, 3 "can check" → A, 7 → B; banner "CONSTRUCTED ASSUMPTION"; the one-line `rater_pick()` rule. |
| B05 | Two horizontal bars stepping through the recorded checkpoints of `train(0.3)`, with recorded tallies; final 32.6% / 67.4%. |
| B06 | Scatter of learned chance vs share of reviewers who can check (7 runs), 50% line, hollow markers for vote share, spoken points labelled on cue. |
| B07 | Two cards: THE TOY SHOWS (can win) vs IT DOES NOT SHOW (how often; Claude's training; the real reward-model + RL pipeline). |
| B08 | Citation card + two verbatim abstract sentences from Hosking, Blunsom & Bartolo 2023 typed on cue; the second underlined; Sharma et al. 2023 as a "Related" footer. (Revised after review; the first version led with Sharma.) |
| B09 | Three verdict lines landing on cue; third line in the accent colour. |
| B10 | Library `ClaudeComposerAsk`, greeting "Your turn.", the suggested prompt typed, no response, labelled reconstructed. |
| B11 | Neutral title-restate outro with name, course, and disclosure lines. |

## Suggested viewer prompt (B10, read aloud in the video)

```text
Give me one question where a confident wrong answer is common. Write a hedged
correct reply and a confident wrong reply. Then tell me what a reviewer would
need to check to pick the right one.
```
