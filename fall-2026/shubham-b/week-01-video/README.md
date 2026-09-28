# Week 1 Explainer Video — Preference Tuning Follows the Votes

| | |
|---|---|
| **Student** | Shubham Bagwe · INFO 7375 · Fall 2026 |
| **Assignment** | Week 1 Explainer Video — Explain One Concept from Chapter 1 (25 points) |
| **Concept** | *Why preference tuning can prefer a confident wrong answer*. This is listed under "From Part 1" in the assignment's concept list; source: Chapter 1, Part 1, "Where the numbers come from", and Figure 1.3 |
| **Why this concept** | It is the Chapter 1 idea every chatbot user runs into: the training step that makes a model "helpful" follows what reviewers pick, not what is true, so sounding sure can beat being right. |
| **Runtime** | **3:19** (199.0 s) · 1920×1080 · 24 fps · H.264 + AAC |
| **Video** | `Bagwe_Shubham_INFO7375_Week01_Video.mp4`, **submitted on Canvas only** (the repo's `.gitignore` keeps video out of Git) · sha256 `909e544df12fe48d217686abcbe671cb1617a51be919702161b66bb14f311b83` |
| **Narration** | Synthetic, local Kokoro voice `am_onyx` ("Liam"). Not my voice, not Professor Bear's, and no endorsement is implied |
| **Built with** | brutalist.art (commit `cd4bf20`), free local pipeline, $0.00, no API keys, not uploaded anywhere |

## What the video teaches, in one paragraph

A chatbot is trained in two stages. Pre-training nudges it toward the text that really
came next; preference tuning nudges it toward the reply a person picked. **Neither stage is
given an answer key.** A small offline Python toy shows the mechanism. Two replies to "What
is the capital of Australia?" (hedged-correct Canberra, confident-wrong Sydney) start at
50/50 through the chapter's own `probabilities()`. The toy's update function takes only
the scores, the reviewer's pick, and a step size. With 3 in 10 constructed reviewers able
to check, 1,000 seeded votes end at **Canberra 32.6% / Sydney 67.4%**. Changing only how
many reviewers can check (20% → 80%) moves the learned chance of the correct reply from
22.5% to 81.7%, landing near its share of the votes. Canberra was correct in every run.
Across 500 seeds, the wrong reply wins in 500 of 500 runs at 30%. **Named limitation:**
the toy shows this *can* happen, not how *often* it happens in real training, and it says
nothing about how Claude was trained. For real-world evidence the video quotes Hosking,
Blunsom & Bartolo (2023) verbatim: the assertiveness of an answer skews how many factual
errors people perceive in it.

## Where the numbers come from (and why not only `main.py`)

The brief says to use what `lessons/01-randomness-and-first-prompts/code/main.py` prints.
That program implements only Part 2's softmax and sampler, so it computes no preference
update. This concept is from Part 1. So:

- the toy **imports `probabilities()` from `main.py` unchanged** and adds only the update rule;
- B03 shows `main.py`'s own printed output for the chapter's scores [1, 2, 3]
  (`0.090, 0.245, 0.665`, saved in `evidence/course_main_output.txt`);
- the 50/50 start is the chapter's own equal-scores property (`[1000, 1000] → [0.5, 0.5]`);
- every other number is printed by `evidence/preference_toy.py` or `evidence/seed_spread.py`,
  checked by 9 tests, and labelled CONSTRUCTED on screen.

## Beat list (3:19)

| Time | Beat | What you see |
|---|---|---|
| 0:00 | INTRO | "Hi, I'm Liam…" then "Today's one idea: Preference Tuning — why it can prefer a confident wrong answer" (added after my watch-through) |
| 0:12 | B00 Cold open | Two replies, one right-but-unsure, one wrong-but-sure; learned preference bar (CONSTRUCTED) |
| 0:23 | B01 Overview | "rewards the ~~correct~~ **preferred** answer" typed and corrected; glossary |
| 0:37 | B02 Framework | The two training stages from Figure 1.3; ANSWER KEY "not an input to either stage" |
| 0:57 | B03 Mechanism | The real `nudge()` code, tied to `main.py`'s printed output; three inputs boxed; no answer key |
| 1:16 | B04 Assumption | 3 in 10 reviewers can check; labelled CONSTRUCTED ASSUMPTION |
| 1:33 | B05 Worked example | Bars step through recorded checkpoints to 336/664 votes and 32.6% / 67.4% |
| 1:53 | B06 One knob | Learned chance vs share who can check (7 runs); correct in every run; not just seed 7 |
| 2:12 | B07 Limitation | Shows it CAN win · does NOT show how OFTEN / Claude's training / the typical real pipeline |
| 2:31 | B08 Real evidence | Hosking et al. 2023, two verbatim abstract sentences; Sharma et al. 2023 as related |
| 2:47 | B09 Verdict | Three lines |
| 2:58 | B10 Your turn | Suggested prompt in a reconstructed composer, **no response shown** |
| 3:15 | B11 Outro | Title, name, disclosures |

Times are beat starts from the measured narration (199.5 s including B01's 0.8 s lead-in).
The compiled file is 199.0 s.

## Folder contents

| Path | What it is |
|---|---|
| `Bagwe_Shubham_INFO7375_Week01_Video.mp4` | The rendered video: the toolkit's final master, renamed. **In the Canvas zip only, not on GitHub.** The sha256 above and in `final/*.verified.json` lets a reviewer confirm the Canvas file is this build |
| `beat_sheet.json` | Reviewed narration and visual plan: 13 beats, `show` blocks, measured durations, word-timed cues |
| `BUILD-PROMPT.md` | Every command and the Claude Code prompt that rebuild the video, including the failures and fixes |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated entries (Frictional guide) |
| `FACTCHECK.md` | Every narrated claim → verdict → source, including what changed after review |
| `DEFENSE-NOTES.md` | How to explain each part, including the one bit of maths and likely questions |
| `SHOTLIST.md`, `PROMPTS.md` | Typed work order and per-beat scene requests (toolkit GATE F paperwork) |
| `TYPECHECK.md`, `_qc/REPORT.md`, `qc-sheet.png`, `_qc/final/` | Toolkit gate reports; my 1 fps frame sheets of the final |
| `evidence/preference_toy.py` | The constructed toy (standard library, offline, seed 7) |
| `evidence/test_preference_toy.py` | 9 tests; output in `preference_toy_tests_output.txt`, and the first **failed** run kept |
| `evidence/preference_toy_output.json` | The numbers shown in the video |
| `evidence/seed_spread.py`, `seed_spread_output.json` | The same toy over seeds 0–499: how typical seed 7 is |
| `evidence/source_abstracts_2026-09-27.txt` | Raw arXiv abstracts of the papers quoted |
| `evidence/course_main_copy.py`, `course_main_output.txt`, `course_tests_output.txt` | The course's `main.py` (verbatim), its printed output, and its 6 passing tests |
| `evidence/build-logs/` | Trimmed setup/build logs and the narration pronunciation checks |
| `src/scenes/PrefTune.tsx.txt`, `src/Root.tsx.patch` | The 11 custom Remotion scenes, stored as `.txt` because the course repo keeps no TS files, and their registration |
| `scripts/set_props.py`, `scripts/install_scenes.sh` | Audio-clock props and word cues; installs the scenes into a toolkit checkout |
| `final/*.verified.json` | The toolkit's hash receipt for the final master |

Not included, on purpose: regenerable media caches (`media/`, `clips/`, `mp3/`, `mp4/`),
the toolkit itself, and any chat transcript.

## Run the evidence (seconds, no installs)

```bash
cd fall-2026/shubham-b/week-01-video/evidence
python3 preference_toy.py                     # prints the JSON the video shows
python3 -m unittest test_preference_toy -v    # 9 tests, OK
python3 seed_spread.py                        # 500-seed robustness check
```

## Rebuild the video from this folder

Full details, versions and known failures are in **BUILD-PROMPT.md**. In short:

```bash
git clone https://github.com/nikbearbrown/brutalist.art.git && cd brutalist.art
brew install ffmpeg pkg-config cairo pango
uv venv --python 3.12 .venv && source .venv/bin/activate && uv pip install pip
./setup --install
REEL=/path/to/fall-2026/shubham-b/week-01-video
bash "$REEL/scripts/install_scenes.sh" .
python3 runtime/scripts/generate_audio_kokoro.py "$REEL" --speed 0.9
python3 "$REEL/scripts/set_props.py" .
python3 runtime/scripts/remotion_scenes.py "$REEL" --force
./art run "$REEL"
./art final "$REEL" --height 1080 --out "$REEL/final"
```

## Decisions that differ from the toolkit's defaults

- **No Claude composer cold open with "output" lines.** On screen that reads as a Claude
  reply, and the assignment forbids showing any Claude response I didn't actually receive.
  The toolkit's SKIN LINT flags this; the deviation is deliberate.
- **No locked `@NikBearBrown` outro.** The course prerequisite says a student video must
  not imply the instructor's endorsement, so a neutral title-restate outro is used instead.
- **"Reviewers", not "raters", in the voice.** The synthetic voice's "raters" is heard as
  "raiders" (FRICTIONAL entry 4). The screen notes the chapter's term.
- **Accent text is `#A44A32`, not the Claude terracotta.** Terracotta text measures
  2.74–2.96:1 on cream, which fails WCAG AA. The brighter terracotta is kept for fills only.

## Credits

Concept and reference code: INFO 7375 Chapter 1 and `lessons/01-randomness-and-first-prompts/code/main.py`.
Toolkit: brutalist.art by Nik Bear Brown. Build assistance: Claude Code (Claude Opus 5.5).
Exactly what Claude did and what I did is listed in SOURCES.md §5.
Course AI policy: [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).
