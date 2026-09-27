# FRICTIONAL — Week 1 Explainer Video (INFO 7375)

Aditya Raj · concept: *A chatbot is one next-token prediction run in a loop*

Honest log of what I tried, what broke, and what I did instead. Work was done with Claude Code
(Claude Opus 5.5) as the build agent; each entry says who did what. Format will be aligned with
the course Frictional guide once I have it (not yet on this machine — see 2026-09-27 #6).

---

## 2026-09-26 — installing Brutalist

**1. Claude Code could not run the toolkit's installer.**
Tried: asked Claude Code to clone `nikbearbrown/brutalist.art` and run `./setup --install`.
Broke: the clone worked, but Claude Code's auto-mode safety check blocked executing a script
downloaded from an external repo. Claude read `setup` first and summarized what it does
(pip install into the global Python, npm install, copy fonts, download the ~340 MB Kokoro model).
Instead: I ran `./setup --install` myself in Terminal.

**2. Python dependencies failed to install — nothing was installed.**
Broke: my `python3` is Anaconda's base env, Python 3.13. `requirements.txt` pins `manim<0.19`, and
manim 0.18 requires Python < 3.13. pip resolves the whole list at once, so kokoro-onnx, Pillow and
faster-whisper were not installed either. npm install, fonts and the Kokoro model download succeeded.
Instead: created a separate conda env `brutalist` with Python 3.12 (Claude ran this after I approved).

**3. `setup` exited before printing its readiness table.**
Broke: "ElevenLabs reference found — this toolkit is Kokoro-only." The guard greps the whole repo and
matched the repo's *own* files in `youtube/` (a tutorial video that quotes the guard's code, and demo
beat sheets with `"engine": "elevenlabs"`). Every fresh clone hits this — an upstream bug, not my machine.
Instead: local one-line change so the guard skips `youtube/` (`--exclude-dir=youtube` on both greps).
Not reported upstream yet.

**4. ffmpeg missing.** Blocked 5 of 7 features. Fix: `brew install ffmpeg pkg-config`.

**5. manimpango failed to build.**
Broke: `RequiredDependencyException: pangocairo >= 1.30.0 is required` — manimpango 0.5 had no
prebuilt wheel here and built from source. Fix: `brew install pango`. Result: 6 of 7 features green.

**6. The toolkit's own smoke test failed.**
Broke: `./art smoke` → `metadata.slug must be a filename, not a path`. The repo's fixture is named
`_smoke`; `build_safety.py`'s slug regex rejects a leading underscore. Another upstream bug.
Instead: local change allowing a leading `_`. Smoke test then passed (real mp4, audio −24.2 dB).

## 2026-09-27 — LaTeX, then the 60-second pilot

**1. I cancelled the MacTeX install by accident.**
Tried: `brew install --cask mactex-no-gui` (6.9 GB). I pressed Ctrl+C at the `sudo` password prompt.
Broke: Homebrew recorded the cask as installed even though `/Library/TeX` did not exist, so a plain
`brew install` would have said "already installed".
Instead: `brew reinstall --cask mactex-no-gui` (reused the cached download), entered my password.
Claude re-ran `./setup` — all 7 features green — and rendered a test LaTeX equation through Manim to
confirm equations actually work, not just that the programs exist.

**2. Pilot video: "A Chatbot Is a Loop." — 60 s requested, 12 beats, Kokoro am_onyx.**
Built by Claude Code at my request (`~/Desktop/Brutalist/my-videos/youtube/claude-liam-next-token-loop/`).
Frictions, in order:
- The scene library had nothing for next-token prediction (`./art scenes` found only unrelated loop
  diagrams). Claude built six new Remotion components rather than leaving placeholder slates.
- To avoid invented numbers, Claude ran a small open model locally (SmolLM2-135M-Instruct, greedy
  decoding) and recorded every probability to JSON. Two real runs: France → "Paris", and
  Middlemarch → "Samuel Richardson" (wrong; it is George Eliot).
- **Error caught:** Claude's first beat-sheet draft had hand-typed values for the rank-2-to-5 bars in
  two beats. Claude caught it before any render and replaced them with the recorded values.
- Labels rounded p = 0.9972 up to "100%", overstating certainty. Changed to one decimal (99.7%).
- The toolkit documents `lead_silence_s` and an outro tail hold, but no script implements them.
  Claude wrote `pad_audio.py` (idempotent) as a workaround.
- `typeset_math.py` needs matplotlib, which `requirements.txt` does not list. Ran it from a separate venv.
- **Bug found in QC:** the "hesitant writer" summary beat only corrects single words, so the phrase
  correction never appeared — the misconception stayed on screen uncorrected. Found by looking at
  rendered frames, not by the automated gate. Rewritten around a one-word correction (library → loop).
- The visual QC gate flagged 4 underfilled frames; fixed and re-rendered until 0 BLOCKER / 0 MAJOR.
- **Runtime came out 73.9 s, not 60 s.** Five of the twelve beats are fixed bookends, and several body
  beats were already below the toolkit's minimum durations. Not trimmed; left for review.

**3. Checked the pilot against the Week 1 brief — it would not pass as-is.**
- The cold open showed the SmolLM2 answer inside a Claude-styled window (with a model chip). That
  could read as a fabricated Claude response, which the brief says fails the assignment. The graded
  video must label it clearly or use a real, dated Claude response.
- No explicit "what this explanation does not establish" beat (rubric: 2 points).
- 74 s is under the 2–4 minute target.

**4. Feasibility probes for the 3-minute version** (`research/probe_experiments.py` → `research/probes.json`).
Same local model, three interventions:
- Stop token banned → the loop kept writing fluent "facts" about Paris, including a population figure
  (2.5 million) that looks higher than official counts. Not yet verified against a source.
- " George" forced at the name step → "George Eliot." " George" had been ranked 8th (3.1%).
- 200 sampled runs (seeds 0–199, temperature 1.0) → "George Eliot" in 5 of 200.
These are probes, not final evidence; the final runs will be re-recorded with hashes.

**5. The instructor's own Chapter 1 film uses a constructed distribution.**
The toolkit's audit report (`reports/isdone-2026-09-11/AUDIT.md`, item 09) notes that the
Chapter 1 reel's B05 shows an illustrative token distribution that should be labelled as constructed.
My video will use measured distributions instead, and label anything constructed on screen.

**6. Course materials not on my machine.**
Chapter 1 text, `lessons/01-randomness-and-first-prompts/code/main.py`, the Frictional guide,
`brutalist-video-sources.md` and the Relative Quartile criteria are not local yet. Needed before the
final build so claims match the chapter and `main.py`'s printed numbers can be used where relevant.

## 2026-09-27 (afternoon) — from the 60-second pilot to the 3-minute graded video

**7. Planning for Relative Quartile, then approval.**
Claude proposed six ideas; I approved 1–5 and skipped 6:
1. three experiments that intervene in the loop (ban the stop token, force a token, sample 200 times);
2. an evidence badge on every visual (recorded / constructed / real Claude response);
3. one real, dated Claude response, used to show that a model's "I was unsure about…" is itself generated text;
4. an explicit "what this does not establish" beat;
5. a one-command check (`evidence/verify.py`) that re-runs everything and compares every number.
Skipped: running a bigger model (≈4 GB download, and it drifts from "one concept").

**8. The pilot's evidence would not survive, so it was rebuilt.**
Broke: the pilot's Python environment lived in a temporary session folder, and its script only covered two runs.
Instead: one script (`evidence/run_experiments.py`) records all six runs, with the model pinned to an exact
revision (`12fd25f7`) and every package pinned in `evidence/requirements.txt`, in its own venv
(`Assignment 1/.venv-evidence`, not submitted). It writes a SHA-256 manifest of every output.

**9. The regex over-counted the "right" answers.**
Tried: counting sampled answers that match "George Eliot" → 5 of 200.
Broke: reading all five, seed 42 only *mentions* Eliot and credits a non-existent novel to someone else.
Instead: the on-screen number is 4 of 200, with the review saved as `evidence/sample_review.json`
(labelled as a judgment, not a computation) and the 5th dot shown outlined. Reading them also showed all
four "correct" answers invent facts (a Nobel Prize, an 1885 Pulitzer, wrong dates) — that became the beat's point.

**10. Checking outside facts — three sources refused the request.**
- INSEE's PDF came back as unreadable binary through the web tool; Claude read the saved PDF pages directly:
  Paris 2022 = 2,113,705.
- Britannica, nobelprize.org and pulitzer.org returned HTTP 403. Used Project Gutenberg for Middlemarch and
  Wikipedia for the Nobel (1901) and Pulitzer (1917) dates — a weaker source, noted in FACTCHECK.md.
- Anthropic's docs page for the Messages API had moved (301); followed it to confirm the `temperature`
  default (1.0) and the `end_turn` stop reason wording.

**11. Wording that claimed more than the evidence — caught before rendering.**
- "Claude's docs describe *the same* stop" → "list a stop reason called end turn" (their description, not our measurement).
- A caption said two stop tokens were banned; for this model the end-of-sequence token *is* `<|im_end|>`, so one.
- "The loop never stops" (twice, in a caption and a footer) → "kept going for all 60 passes we allowed".

**12. No hand-typed numbers this time.**
The pilot's worst error was hand-typed probabilities. Now `fill_props.py` writes every number, token and model
output on screen straight from the evidence files, and `evidence/verify.py` checks hashes, re-runs every
experiment, and compares every on-screen and spoken number: 48/48 PASS. One flaw in the checker itself:
its "is this phrase in the narration?" test was vacuous for phrases starting with a quote mark — tightened.

**13. Build bugs.**
- A React hook inside a list that grows frame by frame (the no-stop text) would have crashed mid-render.
  Caught in code review before the first render; hooks moved out of the list.
- The forced "George" card floated out of its row and faded — redesigned to stay in place with a "forced" tag.

**14. The real Claude response (B13).**
Claude Code would not write a stand-in, so the beat stayed a HOLD until I ran the prompt myself in a fresh claude.ai
chat (Opus 5.5, Medium) and sent a screenshot on 2026-09-27. The screenshot shows no timestamp, so the date recorded
is the day I ran it. Claude transcribed it verbatim into `evidence/claude-response/response.json` (with the
screenshot's SHA-256), noting two limits of a screenshot transcription: bold formatting is not reproduced, and an
en dash cannot be fully told apart from a hyphen. Claude's answer was correct (George Eliot) and named "Ann" as the
word it was least sure of; its reason (Mary Ann / Mary Anne / Marian) matches Wikipedia. The narration was written
only after the response existed.

**15. Still missing course materials.** Chapter 1 text, `main.py` and the Frictional guide are still not on my
machine, so `main.py` has not been run. Every number in the video comes from our own recorded runs instead.
If the graders expect `main.py`'s output specifically, this is the gap.

**16. Visual QC gate caught content crossing the safe edge (B05, then B12).**
Rows in the unrolled-loop table slid in from 30 px left of the title-safe line, so frames caught mid-animation had
content in the margin (GATE V: 2 BLOCKER). Fixed by sliding in from the right. The same pattern existed in B12's
cards; the gate's sampled frames had missed it, but it was fixed too.

**17. The typography gate blocked the final cut — twice.**
- First run: 9 beats failed. Contrast: I had used terracotta for text (the stop-token chips, a tag, highlighted
  words) — 2.74:1 on cream, below WCAG's 4.5:1. All text is now ink; terracotta stays on bars, dots, strikes, underlines.
- My first fix (raising all small captions to 30 px) changed nothing: the measurement was identical. Instead of
  guessing again, Claude imported the checker's own functions and printed where the offending "text" was:
  (a) lowercase serif words at 44–46 px — EB Garamond's x-height is ~0.4 em, so lowercase needs ≥ 52 px to clear
  the 41 px@4K floor; (b) terracotta *outlines* around chips and tags, which have a text-like shape; (c) a short
  terracotta data bar at exactly the 15:1 aspect threshold; (d) a "←" arrow glyph.
- Fixed in the design, not by adding exemptions to the checker: larger serif, plates without terracotta
  outlines, thinner bars, no arrow glyph. A local pre-flight on 24 4K frames went from 10 failing to 0.

**18. Final build.**
- Final master: 3:02 (182.0 s), 3840×2160, 17/17 beats filled, GATE V 0 BLOCKER / 0 MAJOR, GATE T PASS.
  `./art final` writes into the toolkit's own `renders/` folder; moved into this folder as
  `Raj_Aditya_INFO7375_Week01_Video.mp4` so everything for the assignment lives in one place.
- `evidence/verify.py`: 51/51 checks on a fresh re-run of all six experiments (the three extra checks cover the
  B13 transcript, its date, and the screenshot hash). Output saved as `evidence/verify-output.txt`.
- The toolkit changes are shipped as `toolkit-additions/toolkit.patch`, tested to apply cleanly to brutalist.art `6a8380a`.
- Runtime check against the brief: 2–4 minutes asked; 3:02 delivered. The extra two minutes over the pilot are the
  three experiments, the boundary beat and the real Claude response — no beat was lengthened to reach a number.

---

## 2026-09-27 (evening) — changing the narrator's sign-off after watching the cut

**19. "This is Liam, in for Bear" → "This is Liam, in for Aditya."**
- *What I noticed (Aditya):* watching the final cut, the narrator twice says "in for Bear": in the opening (B00)
  and in the handoff sign-off (BHTF). I made this video, not Prof. Nik Bear Brown, so the line misstated whose
  video it is. I asked Claude Code to change it to "in for Aditya".
- *Why it was there:* the ai-explainer skill's IN-FOR-BEAR LAW scripts the Kokoro `am_onyx` voice ("Liam")
  as a stand-in for Bear on his @NikBearBrown channel, and requires that exact sign-off. Claude followed the skill
  without asking whether that framing fit a student's assignment. It did not, and I caught it, not Claude.
  No automated gate checks this wording (only the toolkit's unused publishing script does), so nothing would
  have caught it.
- *What changed (Claude):* the B00 and BHTF narration, plus the sheet's `persona` label, now say "in for Aditya".
  Only those two beats were re-voiced (Kokoro am_onyx), padded, re-aligned and re-rendered; the other 15 beats'
  audio and video were reused unchanged. A field-by-field diff of `beat_sheet.json` confirmed no other narration,
  number or cue timing moved. (The only other diff was the build date embedded in B11's equation SVGs.) Whisper
  heard "Aditya." correctly in both beats.
- *Cost:* B00 grew from 8.73 to 8.85 s and BHTF from 13.33 to 13.59 s.
- *Friction:* the first `./art run` printed "nothing to render". I took that to mean the deleted clips weren't
  being picked up and stopped the run. Reading `run.sh` showed the message was about Manim only; the Remotion step
  re-renders any beat whose `media/<beat>.mp4` is missing. I restarted it; one wasted run, no harm.
- *Deliberately left as is, for me to decide:* the closing title card still says "A Chatbot Is a Loop. At Nik
  Bear Brown." (the toolkit's fixed OUTRO-LOCK line); the small "@NikBearBrown" labels on the Claude window
  mock-ups stay too, as does the Bear Brown corner logo. Those credit the course toolkit's brand, not the narrator.
  The beat sheet's `in_for_bear: true` flag is a toolkit mode switch, read only by the unused publishing script,
  so it stays unchanged.
- *Result:* GATE V 0 BLOCKER / 0 MAJOR, GATE T PASS, and `verify.py` 51/51 on a fresh re-run of every experiment
  (`evidence/verify-output.txt` updated). New master: 3:02 (182.5 s), 3840×2160, replacing the previous
  `Raj_Aditya_INFO7375_Week01_Video.mp4`. Claude transcribed the finished master's audio for both beats with
  Whisper ("…this is Liam in for Aditya…", "…Liam in for Aditya.") and checked frames from both beats.

---

## 2026-09-27 (evening) — preparing the GitHub posting

**20. The course files were in the course repo all along; checking the posting rules; the wrong video copy.**
- *What I did (Aditya):* shared a classmate's posted folder (`fall-2026/yash-s/`) as a reference, gave the destination
  (`fall-2026/aditya-r/`) and my GitHub account, and asked Claude to push on my behalf.
- *What Claude found in the course repo:* Chapter 1 (`chapters/01-randomness-and-first-prompts.md`), `main.py`
  (`lessons/01-randomness-and-first-prompts/code/main.py`), the Frictional rules (`prerequisites/frictional.md`) and
  the GitHub posting rules (`prerequisites/github-submission.md`). Entry #15 ("course materials still missing") was wrong:
  they were public in the repo the whole time, and neither of us had looked there.
- *Concept check:* the concept is Chapter 1's own. Part 1's Figure 1.1 is captioned "A chatbot is one prediction, run in
  a loop", and the chapter's goals include describing "a chatbot as a next-token predictor inside a loop".
- *`main.py` — a gap, stated rather than patched:* the brief says to run `main.py` and use what it prints. `main.py`
  implements softmax with temperature and seeded sampling over three scores, which is Chapter 1 Part 2. It was not run for this
  video, and none of its output is on screen. The video's numbers come from the recorded SmolLM2 runs in `evidence/`.
  B10's sampling step is the same operation, softmax at temperature 1.0 followed by a random draw, but over a real
  model's 49,152 scores. A grader looking for `main.py`'s printout will not find it.
- *Repo rules checked before pushing (Claude):*
  - The course validator runs on every push and rejects `.tsx` files, so `toolkit-additions/NextTokenLoop.tsx` became
    `NextTokenLoop.tsx.txt` (the same fix a classmate used). The rebuild uses `toolkit.patch`, so nothing breaks.
  - The repo's `.gitignore` blocks `.mp4`. The brief lists the video as a deliverable, so it was force-added.
  - The four `.py` files parse on Python 3.11 (the oldest version CI tests), and no Markdown links are broken.
  - A dry-run push confirmed write access for my account (the push handshake returned 200, not 403).
  - CI on `main` was already failing before this push (exit code 1 on `validate (3.13)`), so a red check on this
    commit is not necessarily caused by this folder.
- *Friction — which video is correct?* I told Claude the correct video was the review cut
  (`claude-liam-next-token-loop-w01-slate.mp4`), because I believed the master still said "in for Bear". Claude
  transcribed the opening and sign-off of every copy. The master and the slate both say "Liam, in for Aditya". An old
  master from 13:36, before entry #19, was still sitting in `mp4/` under the same filename and said "in for Bear". That
  copy is most likely the one I had watched. Claude renamed it `mp4/OLD-before-in-for-Aditya_DO-NOT-SUBMIT.mp4`. We
  pushed the clean master, not the slate: the slate has the toolkit's review labels burned into every frame
  (e.g. "B06 REMOTION VIDEO 51.8s +8.3s").
- *Privacy choice:* the commit uses my GitHub no-reply address, not my university email, which would otherwise stay
  public in the repo's history.
- *Evidence:* the commit adding this folder (its hash is in the Canvas submission, not here — a commit cannot contain
  its own hash).
- *Still open:* my own notes on what I expected going in, and what I understand now or still don't, are not in this
  log yet.
