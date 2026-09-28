# BUILD-PROMPT — the prompts and commands that rebuild this video

Every command below was actually run on 2026-09-27 on macOS 27.0 (Apple Silicon, arm64).
Where a documented step failed, the failure and the workaround are recorded here and in
FRICTIONAL.md. Cost: **$0.00**. No API key, no paid service, no upload.

| Tool | Version used |
|---|---|
| brutalist.art | commit `cd4bf20904be4e7d63babd9622b17963c2361b27` |
| Python for the evidence script | 3.14.5 (system; standard library only) |
| Python for the toolkit venv | 3.12.13 (via `uv`); see §2 for why 3.13 failed |
| Node / Remotion | 20.19.5 / 4.0.486 |
| ffmpeg / ffprobe | 9.0.2 (Homebrew) |
| kokoro-onnx / faster-whisper / manim | 0.6.1 / 1.2.1 / 0.18.1 (manim installed but unused) |

Paths below assume this layout (the course repo and the toolkit are siblings):

```text
WorkWithMe/
├── brutalist.art/                                   ← toolkit (TK)
└── info-7375-prompt-engineering-for-generative-ai/  ← course repo
    └── fall-2026/shubham-b/week-01-video/           ← this folder (REEL)
```

```bash
export TK=/path/to/brutalist.art
export REEL=/path/to/info-7375-prompt-engineering-for-generative-ai/fall-2026/shubham-b/week-01-video
```

---

## 1. Evidence first (no toolkit needed)

```bash
cd "$REEL/evidence"
python3 preference_toy.py > preference_toy_output.json     # the numbers in the video
python3 -m unittest test_preference_toy -v                 # 9 tests, all pass
python3 seed_spread.py > seed_spread_output.json           # 500-seed robustness check
# The course's own reference, for comparison with the chapter:
python3 ../../../../lessons/01-randomness-and-first-prompts/code/main.py
```

`preference_toy.py` imports `probabilities()` and `sample()` from
`lessons/01-randomness-and-first-prompts/code/main.py`. If run outside the repo it falls back
to `course_main_copy.py`, a verbatim copy that a test checks against the original.

## 2. Install the toolkit

```bash
git clone https://github.com/nikbearbrown/brutalist.art.git "$TK"
cd "$TK"
brew install ffmpeg pkg-config cairo pango      # ffmpeg was missing; cairo/pkg-config for pycairo
uv venv --python 3.12 .venv                     # NOT 3.13; see below
source .venv/bin/activate
uv pip install pip
./setup --install
```

Known failures on this machine, and what fixed them:

1. **Python 3.13 venv:** `ERROR: No matching distribution found for manim<0.19,>=0.18`.
   pip's own log shows why: `0.18.1 Requires-Python >=3.9,<3.13`. Because pip aborts the
   whole requirements file, kokoro-onnx etc. were not installed either. **Fix:** a
   Python 3.12 venv.
2. **pycairo build:** `Dependency lookup for cairo with method 'pkg-config' failed`.
   **Fix:** `brew install pkg-config cairo pango`.
3. **`./setup` exits 1 before the readiness table**, with "ElevenLabs reference found".
   The toolkit's own example reels under `youtube/brutalist/` trip its own guard. I did not
   edit the toolkit. Instead I ran the same checks by hand, and all passed:

```bash
for m in kokoro_onnx mutagen PIL numpy manim manimpango faster_whisper; do
  python3 -c "import $m" && echo "OK $m"; done
ffmpeg -version | head -1
python3 runtime/scripts/setup_smoke_kokoro.py        # "[smoke] kokoro synth OK — mean_volume -21.8 dB"
```

## 3. Install this reel's scenes into the toolkit

```bash
bash "$REEL/scripts/install_scenes.sh" "$TK"
# copies src/scenes/PrefTune.tsx.txt (as scenes/PrefTune.tsx) and applies src/Root.tsx.patch (registers Pt* compositions)
```

## 4. Audio first (the clock), then props from the audio

```bash
cd "$TK" && source .venv/bin/activate
python3 runtime/scripts/generate_audio_kokoro.py "$REEL" --speed 0.9
python3 "$REEL/scripts/set_props.py" "$TK"
```

- `--speed 0.9`: at 1.0 the narration ran about 190 words per minute, which is fast for
  beginners. 0.9 gives 192.3 s of speech.
- `set_props.py` writes `durationSeconds` per beat, word-timed `cues` from faster-whisper
  timestamps on each beat's own mp3, and `runtime/remotion/src/data/prefTuneToy.json`
  (the evidence JSON, the verbatim `nudge()`/`rater_pick()` source, `main.py`'s printed
  probabilities, and the 500-seed result it cites).

## 5. Render, compile, check, final

```bash
python3 runtime/scripts/remotion_scenes.py "$REEL" --force     # every beat -> media/Bxx.mp4
./art run "$REEL"                                             # review cut + GATE F/L/V
./art final "$REEL" --height 1080 --out "$REEL/final"         # GATE T type-lock, clean master
cp "$REEL/final/preference-tuning-follows-the-votes.mp4" \
   "$REEL/Bagwe_Shubham_INFO7375_Week01_Video.mp4"
```

Final master: 199.0 s. Gates at the final build: GATE F (paperwork) pass · GATE L (beat-mix lint) clean · GATE V
(frame QC, 24 frames) 0 BLOCKER / 0 MAJOR · GATE T (type-lock) PASS. The two "SKIN LINT"
notes (cold open is not `ClaudeComposerAsk`; outro is not `ClaudeTitleOutro`) are
deliberate. See README "Decisions".

Re-render one beat after a change: `python3 runtime/scripts/remotion_scenes.py "$REEL" --only B04 --force`
(`--only` takes a single beat id).

## 6. The Claude Code prompt that drove the build

This was the working prompt, adapted from `prerequisites/brutalist-video.md`. The
conversation itself is not included (course rule: no private transcripts).

```text
Help me explain my INFO 7375 Week 1 concept using this brutalist.art checkout.
Read CLAUDE.md, README.md, RENDER-TARGETS.md, and the full
skills/make/ai-explainer/SKILL.md plus its required references.
Use the free beginner ai-explainer path, not an advanced or paid builder.
Concept: "Why preference tuning can prefer a confident wrong answer"
(Chapter 1, Part 1, "Where the numbers come from").
Evidence: a small offline Python toy that reuses the chapter's probabilities()
from lessons/01-randomness-and-first-prompts/code/main.py; seed 7; saved JSON output.
My output reel folder is fall-2026/shubham-b/week-01-video. My name is Shubham Bagwe.
Takeaway: preference tuning follows the votes; votes usually track the truth, but
when reviewers can't check, a confident wrong answer can win.
Limitation: the toy shows it CAN happen, not how OFTEN, and says nothing about how
Claude was trained.
Audience: college students with little or no ML background — plain words.
Use actual code and results; label constructed examples and reconstructed UI.
Never show a Claude response I did not actually receive.
Do not imply the synthetic narrator is me, Bear, or an official endorsement.
Use local Kokoro am_onyx and disclose synthetic narration.
No paid calls, direct Claude API calls, permission bypass, or publishing.
```

**Round 1: defects found by Claude's own frame-level QC during the build** (not requests
from me; each was fixed at the source and re-rendered):

- "B01: the typing never finishes 'Not always.' before the cut." → faster keystrokes.
- "B01: the trigger word 'correct' appears twice, so line 3 would flip too." → reworded line 3.
- "B03: don't put a fake `answer_key` argument inside real code, even struck through." → moved to a callout.
- "B04: 'can check' labels wrap and collide; the legend touches the third tick." → ticks plus one legend line.
- "B05: the voice says 336 while the screen still shows 33." → checkpoints reach 336/664 on the spoken number.
- "B06: ribbon, axis title, 50% label and point labels collide." → re-laid out.
- "GATE T: accent text 2.74:1 contrast; small text; pill outside title-safe." → `#A44A32` accent text, larger captions, pill inside SAFE.

**Round 2: findings from an independent, fresh-context Claude reviewer run against the
rubric** (applied, then all gates re-run; FRICTIONAL entry 7):

- B00 printed tweened percentages the toy never computed → numbers now appear only at the recorded final value.
- B08 led with a sycophancy study as if it were direct evidence → Hosking et al. 2023 (assertiveness) is now the main quote; Sharma et al. is a "Related" footer.
- B10 claimed Claude's answer "came from a model tuned on preferences" with no source → replaced with "check its answer against a real source yourself".
- B07 "Real systems…" → "Many real systems, like InstructGPT…"; B09 "the training" → "the update rule".
- B03 now shows `main.py`'s own printed output; B05 explains 50/50 (no pre-training), 336 vs 300, and "seed 7"; B06 adds the 500-seed result; B07 glosses "reward model" and "reinforcement learning".
- `preference_toy.py` no longer crashes when run outside the repo; `seed_spread.py` added.

**Round 3: my own request after watching the final** (2026-09-27): "everything is perfect but
can you add intro to start saying today we will be discussing about the pref tunning topic".
A new INTRO beat (scene `PtIntro`) was added before B00. B00's "I'm Liam…" line moved into
it so the introduction isn't said twice. Audio for INTRO and B00 was regenerated
(`--only INTRO B00`), cues recomputed, both beats re-rendered, and every gate re-run: GATE V
0/0 on 26 frames, GATE T PASS. Final: 199.0 s.
