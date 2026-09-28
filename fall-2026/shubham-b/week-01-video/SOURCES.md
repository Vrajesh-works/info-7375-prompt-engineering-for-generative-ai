# SOURCES — what I used, what I made, what Claude contributed

All links checked on 2026-09-27. The crediting follows `prerequisites/brutalist-video-sources.md`.

## 1. Course material I used (not mine)

| Item | Where | How it is used |
|---|---|---|
| Chapter 1, *Randomness and first prompts*: Part 1 "Where the numbers come from", Figure 1.3 | `chapters/01-randomness-and-first-prompts.md` | The concept, and every claim in B01/B02/B09 (see FACTCHECK.md) |
| `probabilities()` and `sample()` | `lessons/01-randomness-and-first-prompts/code/main.py` (course repo commit `8daaff5`) | Imported unchanged by `evidence/preference_toy.py`. A verbatim copy, `evidence/course_main_copy.py`, lets the script run outside the repo, and a test checks the copy against the original |
| Course reference output and tests | same lesson | Re-run and saved as `evidence/course_main_output.txt`, `evidence/course_tests_output.txt` (6/6 pass) |
| Prerequisite guides: Brutalist video, sources, Frictional, Relative Quartile, GitHub posting, AI policy | `prerequisites/`, `frictional/` | Workflow and honesty rules |
| Brutalist tutorial videos (playlist): Install & Set Up, Your Week in a Folder, The Prompt, What's a Beat Sheet?, plus Make It Move and Watch & Revise | Their beat sheets and `.srt` transcripts in the public `nikbearbrown/humanitarians-youtube` repo, `claude-for-design/hai-brutalist-*` | I read the narration and captions in place of watching; the workflow (audio-first, rebuild-as-motion, watch-and-revise) follows them |

## 2. Published research cited on screen

| Source | Used for | Checked |
|---|---|---|
| Hosking, T., Blunsom, P., Bartolo, M. (2023). *Human Feedback is not Gold Standard.* arXiv:2309.16349. <https://arxiv.org/abs/2309.16349> | B08, the main evidence. Two verbatim abstract sentences: assertiveness "skews the perceived rate of factuality errors"; "preliminary evidence that using human feedback as a training objective disproportionately increases the assertiveness of model outputs" | Raw abstract fetched from the arXiv API 2026-09-27 (`evidence/source_abstracts_2026-09-27.txt`) |
| Sharma, M., Tong, M., Korbak, T., … Perez, E. (2023). *Towards Understanding Sycophancy in Language Models.* arXiv:2310.13548. <https://arxiv.org/abs/2310.13548> | B08 footer, as a *related* finding (sycophancy, not confidence): humans and preference models sometimes prefer convincing sycophantic answers over correct ones | Raw abstract fetched 2026-09-27 |
| Ouyang, L., Wu, J., … Lowe, R. (2022). *Training language models to follow instructions with human feedback.* arXiv:2203.02155. <https://arxiv.org/abs/2203.02155> | B07: real systems train a reward model from human rankings, then fine-tune with RL. DEFENSE-NOTES: the pairwise reward-model loss | Abstract read 2026-09-27 |
| Christiano, P., Leike, J., Brown, T. B., Martic, M., Legg, S., Amodei, D. (2017). *Deep reinforcement learning from human preferences.* arXiv:1706.03741. <https://arxiv.org/abs/1706.03741> | FACTCHECK B01: learning from human preferences between pairs | Abstract read 2026-09-27 |

## 3. Tools and third-party assets (all free and local)

| Asset | Licence | Use |
|---|---|---|
| brutalist.art toolkit, commit `cd4bf20` — <https://github.com/nikbearbrown/brutalist.art> | Public repo by Nik Bear Brown | Pipeline, the library scenes `BrutalistHesitantWriter` (B01) and `ClaudeComposerAsk` (B10), the gates, the Claude palette tokens |
| Kokoro-82M voice model via kokoro-onnx 0.6.1, voice `am_onyx` | Model Apache-2.0; kokoro-onnx MIT | **All narration is synthetic.** It is not my voice, and not Professor Bear's |
| faster-whisper 1.2.1 (`small.en`) | MIT | Pronunciation check of the narration; word timestamps for cue timing. No transcript of any person |
| Remotion 4.0.486 | Remotion licence (free for individuals) | Rendering |
| EB Garamond | SIL Open Font License 1.1 | Serif type |
| ffmpeg 9.0.2 | LGPL/GPL | Encoding, frame extraction |

No stock footage, images, music, or sound effects are used. No image or video generation
was used. The "reconstructed interface" in B10 is the toolkit's drawing of a chat composer.
It contains only our suggested prompt and **no response**.

## 4. What I made (new for this submission)

- `evidence/preference_toy.py` and `evidence/test_preference_toy.py`: the constructed toy
  and its 9 tests. Output: `evidence/preference_toy_output.json`.
- `evidence/seed_spread.py`: the same toy over 500 seeds (`seed_spread_output.json`).
  It was added after an independent review questioned whether seed 7 was special.
- `beat_sheet.json`: 13 beats, narration, and a `show` block per beat.
- `src/scenes/PrefTune.tsx.txt`: 11 custom Remotion scenes. `src/Root.tsx.patch` registers them.
- `scripts/set_props.py` (audio-clock props and word cues) and `scripts/install_scenes.sh`.
- FACTCHECK.md, DEFENSE-NOTES.md, SHOTLIST.md, PROMPTS.md, BUILD-PROMPT.md, this file,
  README.md, FRICTIONAL.md.
- The constructed example itself: the question, both reply strings, the "3 in 10 can check"
  rule, seed 7, 1,000 votes, step 0.02. These are **our choices, not data.**

## 5. What Claude contributed

The build was done in a Claude Code session with Claude Opus 5.5, on 2026-09-27, under my
direction. Being specific:

| Claude did | I did |
|---|---|
| Read the assignment, Chapter 1, the guides and the tutorial transcripts; surveyed which concepts classmates had already posted; proposed a concept and plan | Asked for the assignment to be done; **approved the concept** ("go ahead with preference tuning") over the temperature fallback |
| Wrote `preference_toy.py`, the tests, `set_props.py`, `install_scenes.sh` and all ten scenes | Own the submission, and must be able to explain it (see DEFENSE-NOTES.md) |
| Drafted all narration and the beat sheet | Watched the final with sound and asked for a spoken intro, which was added (FRICTIONAL entry 8). My reflection is FRICTIONAL entry 9, drafted with Claude's help from this session and checked by me |
| Installed and debugged the toolkit (Python 3.12 venv, cairo), generated audio, rendered, and ran the gates and frame-level QC | |
| Wrote FACTCHECK/DEFENSE-NOTES/BUILD-PROMPT/SOURCES and the draft of FRICTIONAL | Complete the "in my own words" parts of FRICTIONAL.md |
| Checked the arXiv abstracts, including raw API text for every quote on screen | |
| Ran a fresh-context Claude reviewer against the rubric, then applied most of its findings (FRICTIONAL entry 7) | |

What Claude's output was checked against, and what changed as a result:

- **Every number** on screen is read from the JSON the script prints. None is typed by hand, and a test re-runs the script against the saved file.
- **One claim was weakened** after a test failed: "equal to the vote share" became "near the vote share" (FRICTIONAL, 20:00).
- **The narration was checked** by transcribing it with Whisper. That changed "raters" to "reviewers" and "Pretraining" to "Pre-training" (FRICTIONAL, 20:08).
- **No Claude response appears in the video.**

## 6. Corrections applied to sources (DOUBLE-CHECK)

- The chapter says "raters"; the narration says "reviewers" for pronunciation reasons, and the screen says "the chapter calls them 'raters'".
- The toy collapses the reward model and the chatbot ("policy") into one pair of scores. The video says real systems keep them separate (B07), and DEFENSE-NOTES §4 explains it.
- Sharma et al. is about sycophancy (agreeing with the user), which is related to but not the same as confident-vs-hedged. After review it was moved from the main evidence to a "Related" footer, and Hosking et al. (assertiveness) became the main evidence.
- No quoted finding is turned into a rate.
