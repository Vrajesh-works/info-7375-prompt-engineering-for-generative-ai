# BUILD-PROMPT.md — seed-repeatable-not-correct.mp4

This file records the prompts given to Claude Code (Claude Opus 5.5, desktop app)
and the commands it ran to produce the final video, in order. Prompts are quoted
verbatim except where marked as abridged. Full per-command output is in
`COMMAND-LOG.md` in this folder.

## 1. Initial build prompt (2026-09-27, 16:20 local)

```
I'm working on an assignment for INFO7375 (Northeastern) using this Brutalist toolkit.
Read HOW-TO.md and CLAUDE.md first so you understand the beat sheet workflow, the
three core builders, and session rules for agents.

Constraints:
- Free pipeline ONLY: local Kokoro TTS, local Manim/Remotion rendering.
- No paid generation, no API keys, no media accounts, no YouTube upload.
- Target runtime: ~3 minutes total.
- Tone: fun, visual, a bit of a "myth-busting" reveal energy — NOT formula-heavy,
  NOT a lecture. Minimal math on screen. This is a different, lighter register
  than a typical explainer.

Concept (single idea, do not broaden it): a seed makes a sampling run
repeatable; it does not make the sampled answer correct.

[... full source-material context and 5-beat structure as specified to the
agent: setup/hook, real seeded-run comparison, the constructed-answer-key
twist, why-it-matters chat mockup, closing boundary card ...]

Please:
1. Write the beat_sheet.json first and show it to me before rendering, so I
   can review narration and visual plan.
2. Write the actual small Python script (softmax + seeded sampler, matching
   the numbers above) so Beat 2 uses real printed output, not invented
   numbers. Run it twice to confirm the counts match before using them.
3. Use Kokoro for narration (local, free) and Manim/Remotion for rendering.
   Favor a lighter, snappier visual style over dense text/formula slides.
4. After I approve the beat sheet, render the full video.
5. Keep a log of every command you run and any errors encountered — I need
   this for a FRICTIONAL.md dated log afterward, so please summarize what
   happened at the end.
```

## 2. Evidence generation (real, not invented)

```
python3 evidence/seeded_sampler.py        # first run
bash evidence/capture.sh                  # two separate runs -> run1.txt, run2.txt, then diff
for i in $(seq 100); do python3 evidence/seeded_sampler.py; done | sort | uniq -c   # -> run100.txt
```
`seeded_sampler.py` was run with `seed=7`, scores `[1, 2, 3]`, `temperature=1.0`,
`count=1000` — twice, byte-identical output both times (`{0: 102, 1: 268, 2: 630}`),
plus 100 additional confirmation runs, plus one run at a different seed (8) to
show the counts do change with a different seed. All of this is real captured
terminal output, not typed-in numbers. On 2026-09-28 the counts were also
checked against the course reference `lessons/01-randomness-and-first-prompts/code/main.py`,
which prints the same probabilities and counts (`evidence/course_main_py_output.txt`).

## 2b. Narration audio, silent holds, reveal timing

Run from the toolkit directory, with `R` set to the reel folder:

```bash
.venv/bin/python runtime/scripts/generate_audio_kokoro.py "$R"   # Kokoro af_bella, local
python3 "$R/pad_holds.py"   # silent holds after reveals (beat_sheet.json metadata.holds)
python3 "$R/cues.py"        # per-beat reveal times from the measured audio
```

## 3. Approval / human decisions mid-build

- Approved the 5-beat structure and narration as drafted.
- Chose: silent holds after each reveal (rather than faster pacing).
- Kept the Sydney/Canberra mock-chat example.
- Standing instruction for the build session: **no git push or pull.** (Lifted
  on 2026-09-28 only for posting this submission to the course repository.)

## 4. Render + gate commands (final passing run)

```bash
R=~/INFO7375/youtube/seed-repeatable-not-correct
export PATH="$PWD/.venv/bin:$PATH"
ART_QC=0 ./art run "$R" > "$R/_run1.log" 2>&1
./art final "$R" --out "$R" > "$R/_final1.log" 2>&1
```
(This is the fifth `./art final` attempt for the base 5 beats; earlier attempts
failed the toolkit's own text-size and safe-area gates — see `FRICTIONAL.md`
for each failure and fix. This exact pair of commands is what a clean rebuild
from `beat_sheet.json` needs.)

## 5. Follow-up prompt — add an intro (2026-09-27, 18:44)

```
i need to add 10-20 seconds at the start of the video, introducing the concept
being explained in the video, the starting of the video is very abrupt
```
followed by:
```
Also add one line in the start - this video is meant to explain the concept of ______ .
```
Claude Code filled the blank with: *"seeded randomness: why a seed makes a
sampling run repeatable, but not necessarily correct"* and added it as a new
opening beat (B00), narration:

> "This video is meant to explain the concept of seeded randomness: why a seed
> makes a sampling run repeatable, but not necessarily correct. Many AI tools
> let you set a seed. Same seed, same output, every time. That feels like
> reliability. So let's test what it actually guarantees."

Only B00's audio was regenerated and the silent holds re-applied; B01–B05 were
verified unchanged and re-used as-is.

## 6. Follow-up prompt — title-card credit (2026-09-27, 18:58)

```
for the title card, can you add Made by Aditya Hasija at the bottom in a cool text color pls
```
Claude Code used deep teal `#1F6F78` (~5:1 contrast on the cream background),
appearing under the subline at ~5s and fading with the title move at ~8s. Only
the intro beat was re-rendered.

## Final gate status

```
GATE T PASS
GATE V 0 BLOCKER / 0 MAJOR
Master duration: 181.7s (3:01.7)
```
