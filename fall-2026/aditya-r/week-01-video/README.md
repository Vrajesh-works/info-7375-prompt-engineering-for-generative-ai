# A Chatbot Is a Loop. — Week 1 Explainer Video

**Aditya Raj** · INFO 7375 Prompt Engineering · Week 1 · Chapter 1, Part 1

**Concept:** A chatbot is one next-token prediction run in a loop.

**Why this one:** once you can see the loop — predict one token, append it, repeat, until the model predicts
"stop" — you can see why a chatbot's fluency is no evidence that its answer is true.

**Runtime:** 3:02 (182.5 s) · 17 beats · narration: Kokoro `am_onyx` (local, free) · 3840×2160

**Video:** `Raj_Aditya_INFO7375_Week01_Video.mp4`

## What the video shows
Every number comes from a small open chat model (SmolLM2-135M-Instruct) that I ran locally and recorded:
1. The loop, and the chat as one document the model continues.
2. The worked example: "The capital of France is Paris." built in 8 passes, ending when the end-of-turn token wins at 37%.
3. **Experiment 1 — ban the stop token:** the model keeps writing, including a Paris population it never checked
   ("≈2.5 million"; INSEE's 2022 count is 2,113,705).
4. The fluent wrong answer: "Middlemarch is written by Samuel Richardson." (It's George Eliot.)
5. **Experiment 2 — force one token:** "George" was 8th at 3.1%; forced in, "Eliot" follows at 43%.
6. **Experiment 3 — sample 200 times:** 4 of 200 name George Eliot, and all four invent facts around her.
7. The chain rule: the model rates the Richardson answer ≈11× more likely than the Eliot answer.
8. **What this does not establish:** we measured SmolLM2, not Claude; the loop shows how text is produced, not why
   the probabilities are what they are.
9. A real, dated Claude response — and why its "I was least sure of…" is itself generated text.

Every visual carries an evidence badge: **Recorded** (solid outline), **Constructed** (dashed), **Real Claude response** (filled).

## Check it in one command
```bash
cd evidence && python verify.py      # hashes + full re-run + every on-screen and spoken number
```

## Rebuild from this folder
See **BUILD-PROMPT.md** (toolkit commit, patch, environments, and the exact commands). In short:
`run_experiments.py` → `verify.py` → Kokoro audio → `pad_audio.py` → `align.py` → `fill_props.py` → `./art run` → `./art final`.

## Files
| File | |
|---|---|
| `beat_sheet.json` | Narration and visual plan (every data prop written by `fill_props.py`) |
| `BUILD-PROMPT.md` | Prompts and commands that rebuild it |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated log, from the 60-second pilot to this version |
| `FACTCHECK.md` | Every claim, its verdict and its source |
| `evidence/` | The experiment code, recorded runs, manual review, verifier |
| `toolkit-additions/` | The 11 Remotion scenes written for this video, as a patch against brutalist.art `6a8380a`. `NextTokenLoop.tsx.txt` is a readable copy of the scene file; it is saved as `.txt` because the course repo's validator rejects `.tsx` files. The rebuild uses `toolkit.patch`, which already contains it. |
