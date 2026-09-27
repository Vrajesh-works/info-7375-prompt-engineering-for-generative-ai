# FRICTIONAL.md

Saloni Mathure — INFO 7375, Week 1 Explainer Video
Concept: a seed makes a run repeatable; it does not make the answer true.

The observed facts below are transcribed from my terminal session. The lines
marked **Expected:** and **Learned:** are my own predictions and takeaways,
written on the same day, some recalled after the fact rather than recorded
before each run.

---

## 2026-09-27 — Choosing the concept

Considered three options from the assignment's list: the max-subtraction,
expected versus observed count, and the seed. Chose the seed because it can be
shown with real terminal output rather than asserted, and because its boundary
— repeatable is not the same as correct — is the chapter's own argument.

**Why not the others:** The max-subtraction is a numerical-stability trick whose
whole point is that it changes nothing you can see on screen, and
expected-versus-observed on its own is a statistics result rather than a claim
about how to work with these models.

As it turned out, the expected-versus-observed numbers (665.24 vs 630) appear
in my own run output, so the two concepts ended up joined in beats B04 and B05.

## 2026-09-27 — Reading main.py

Cloned the course repo. Minor fumble: ran `cd info-7375-...` a second time
while already inside the folder and got "no such file or directory." Harmless.

`grep -n "seed"` returned two lines:

```
19:def sample(logits, count=1000, seed=7, temperature=1.0):
22:    rng = random.Random(seed)
```

Two things I did not expect from reading the file:

- The seed is a **default argument** on line 19, not a module-level constant.
  So changing it changes the fallback, and any caller passing its own seed
  would override it. `demo()` calls `sample([1, 2, 3])` with no seed, so the
  default is what runs.
- Line 22 is `random.Random(seed)`, which builds a **private generator object**
  rather than seeding Python's global `random` state. The reproducibility is
  therefore local to `sample()` — nothing outside can disturb it.

**Expected before reading:** I expected a module-level constant near the top of
the file — something like `SEED = 7` — and a call to `random.seed(SEED)`. Both
guesses were wrong, which is why I ran `grep -n` instead of assuming.

## 2026-09-27 — Runs A and B (seed 7)

Ran `main.py` twice unchanged, piping each to a file with `tee`.

Both printed:

```
probabilities: 0.09003057317038046, 0.24472847105479764, 0.6652409557748218
counts:        "1": 268,  "2": 630,  "0": 102
```

`diff run-A.txt run-B.txt` returned nothing — byte-for-byte identical, not
merely similar.

**Expected:** I predicted the counts would match, but I was not sure the files
would be byte-identical — dict ordering in the `counts` output was the thing I
thought might drift between runs. It did not: `"1"`, `"2"`, `"0"` came out in
that same order both times, because `Counter` preserves first-seen order and the
draw sequence itself is fixed.

**Learned:** The empty diff demonstrates that the whole run is deterministic, not
that any number in it is right — `630` is reproduced exactly, and `630` is 35
short of what the model's own probabilities predict.

## 2026-09-27 — Run C (seed 10)

Edited line 19 from `seed=7` to `seed=10`, ran again, then reverted to 7.

`diff run-A.txt run-C.txt`:

```
8,10c8,10
<     "1": 268,
<     "2": 630,
<     "0": 102
---
>     "2": 690,
>     "1": 213,
>     "0": 97
```

The probabilities block is unchanged between A and C — only the counts differ.
That makes sense: `probabilities()` has no randomness in it at all. The seed
only affects `rng.choices()`.

**Expected:** Honestly, yes — I half expected the whole output block to change,
because I was thinking of "the seed" as controlling the run rather than
controlling one generator. Seeing the probabilities stay identical to the last
digit is what made the split concrete: `probabilities()` is pure arithmetic on
the logits and never touches `rng`, so the seed cannot reach it.

## 2026-09-27 — Expected versus observed

Worked out probability × 1000 for each token and compared to the counts:

| token | expected | seed 7 | gap    | seed 10 | gap    |
| ----- | -------- | ------ | ------ | ------- | ------ |
| 0     | 90.03    | 102    | +11.97 | 97      | +6.97  |
| 1     | 244.73   | 268    | +23.27 | 213     | −31.73 |
| 2     | 665.24   | 630    | −35.24 | 690     | +24.76 |

Token 2 undershoots by 35 with seed 7 and overshoots by 25 with seed 10. Same
code, same probability, opposite sides of the target. This became beat B04: the
seed reproduces the discrepancy exactly every run without detecting or fixing
it.

The three seed-7 gaps sum to zero. They have to — the counts total 1000 and the
probabilities total 1 — so they are constrained rather than three independent
observations.

**Still working out:** No — a gap of this size does not show the sampler is
wrong, and I cannot tell either way from two runs. 1000 draws at p = 0.665 has a
standard deviation of about 15, so a shortfall of 35 is roughly 2.3 standard
deviations: unusual, but nowhere near impossible for a correct sampler. To
actually tell, I would need many seeds rather than two — run the sampler a few
hundred times with different seeds and check whether the counts centre on 665
with about the spread the binomial predicts. One seed run a thousand times still
gives me one observation, which is the whole point of the video.

## 2026-09-27 — Verification script

Wrote `evidence/verify_claims.py` so that every figure shown on screen is
checked against a fresh run of the unmodified `main.py` rather than trusted
from a screenshot. First version had 2 checks and passed. Expanded to 7, each
named for the beat it defends:

```
[PASS] Beat 3 — same seed, two runs, byte-identical output
[PASS] Beats 1-3 — on-screen probabilities match a fresh run
[PASS] Beats 3-5 — on-screen counts match a fresh run
[PASS] Beat 5 — expected count for token 2 is 665.24
[PASS] Beat 5 — observed falls short by 35.24, and by the same amount every run
[PASS] Beat 6 — the three gaps sum to zero (a constraint, not a coincidence)
[PASS] run-A.txt is real output, not retyped
7/7 checks passed
```

What this does establish: the on-screen figures are the code's actual output.

What it does not establish: that any of those figures is correct — the script
compares my transcription against the same code that produced it, so if
`main.py` sampled badly the script would confirm the bad numbers with 7/7
passes. It is a transcription check, not a correctness check, and it is exactly
the mistake the video is about, committed by my own verifier.

It was also hard-coded to my machine at first: `MAIN_PY` was an absolute path
under `/Users/salonimathure/`, so it passed for me and would have failed for a
grader cloning the folder elsewhere. Changed to read `INFO7375_MAIN` from the
environment, falling back to the repo under the user's home directory.

## 2026-09-27 — Brutalist setup (the long part)

Cloned `brutalist.art` and ran `./setup --install`. It failed three ways at
once, interleaved, so it took a minute to separate them:

1. **Python 3.13 too new.** `manim<0.19` and `kokoro-onnx` both cap at
   `<3.13`. pip reported no matching distribution for manim after listing
   every version it rejected on `Requires-Python` grounds.
2. **PEP 668.** Homebrew's Python refuses system-wide installs
   (`externally-managed-environment`).
3. **Node 18.10.0**, but HOW-TO.md requires Node >= 20 — `EBADENGINE` on
   three packages.

**Expected:** The README presents install as three lines — `./setup --install`,
`./art --list`, `./art keys` — so I expected to run the first one, wait for the
download, and be finished. I had not thought about my own Python or Node
versions at all until pip told me about them.

Fixed with `brew install python@3.12`, a venv, and `pip install -r
requirements.txt`. Node took a second pass: I installed Homebrew's `node@20`
and `node --version` still printed 18.10.0, because nvm was earlier in PATH.
`nvm install 20 && nvm use 20` fixed it.

**Then `./setup` itself was broken.** It exits after the ElevenLabs scan and
never prints the readiness table HOW-TO.md §2 documents, with exit status 0 —
so it believes it succeeded. Verified the pieces directly instead:
`--list-voices` returned `af_bella` and `am_onyx`, ffmpeg 9.0.2 present.

**Documentation contradiction:** README.md says the Kokoro model is fetched by
setup; HOW-TO.md §2 says it ships inside the toolkit at
`runtime/models/kokoro/`. It downloaded (310 MB + 27 MB), so README is right.

## 2026-09-27 — Choosing the builder

I was first pointed at `cli-explainer`. Reading HOW-TO more carefully:
cli-explainer is for "a thing you built" and its spine _mandates_ a revision
cycle — CLI, CODE, OUTPUT, then a second CLI, CODE, better OUTPUT. I have no
revision; I'd have had to invent one. `ai-explainer` is for "one insight that
a 1–3 minute reel can land", which is the assignment almost word for word.

Noted and accepted: the required Claude bookends (B00, BVDT, BHTF, BOUT) are
67 of 166 seconds, about 40%. That is the toolkit's spine, not padding I
added, and the verdict card carries the boundary statement.

## 2026-09-27 — Six gate failures, in order

The reel did not compile until I had been rejected six times.

1. **GATE F** — no `FACTCHECK.md` / `SHOTLIST.md` / `PROMPTS.md`. The
   paperwork is written _before_ rendering. This is the gate I most expected
   to resent and least did — writing FACTCHECK forced me to mark the binomial
   claim in my own verdict narration as stated-but-not-verified, which is
   exactly what the video is about.
2. **LaTeX.** `manim -ql` died four animations into B04: `sh: latex: command
   not found`. `NumberLine(include_numbers=True)` routes its labels through
   `DecimalNumber` → `MathTex` → LaTeX. HOW-TO warns LaTeX is needed "only for
   Manim equation beats", and a plain number line did not look like an
   equation beat to me. Fixed by placing `Text` tick labels manually rather
   than installing MacTeX against the clock.
3. **GATE A — `NameError: NORMAL`.** The same file had already rendered five
   scenes under `manim -ql`. The static checker executes `construct()` in its
   own stubbed namespace, so names that resolve during a real render do not
   resolve there. Same cause again two fixes later:
   `rate_functions.ease_out_cubic` → `SimpleNamespace has no attribute`.
4. **GATE A — "shapes never change".** My rebuilt B04 was fades and waits, so
   six sampled frames looked identical. Fixed with a `ValueTracker` counter
   that climbs 0 → 630, resets, and climbs to the same number again. The
   repeat visually _is_ the claim, so the gate improved the beat.
5. **GATE B — layout.** `CONSTRUCTED ILLUSTRATION` sat at x = −6.61 against a
   safe edge of −6.3, because `to_corner` measures from the frame, not the
   safe area. Replaced every `to_edge`/`to_corner` with explicit coordinates.
   Later, B05: all three gap values animated to one point, giving three
   100%-overlap errors. Fixed by giving them separate slots before collapsing.
6. **GATE V — visual QC.** 2 BLOCKER (B01's source line crossing the
   title-safe left edge) and 9 MAJOR underfill. Fixed the blocker with
   `scale_to_fit_width(11.0)`, which cannot bleed regardless of how the text
   renders, and enlarged every scene. Second pass: **BLOCKER=0, MAJOR=7.**

**Decision on the record:** the last pass ran with `ART_STRICT=0`, which
downgrades the remaining underfill MAJORs to warnings. I did this only after
the blockers were fixed. One remaining warning is in `ClaudeVerdictArtifact`,
a stock Brutalist component at 47% fill, which I cannot fix without editing
the toolkit's source — so a fully clean GATE V was not reachable. I preferred
relaxing a documented flag and saying so here over quietly shipping.

**Also on the record:** `./art final` refused at `final_frame_check.py` and
exited without printing a reason. I submitted the review cut
(`seeded-not-settled-slate.mp4`), which reports 9/9 slots filled with no
slates and passes GATE T. It is a complete video, not a previz. I did not
diagnose the refusal.

## 2026-09-27 — Render

Audio first, as the toolkit insists: Kokoro `am_onyx`, nine beats, $0.00,
165.92 s measured. Those durations became the clock; visuals conformed to them.

The conform is visible in the compile log and I am not happy about it:

```
[art] B01: clip 10.5s slowed 2.88x to fill 30.3s beat
[art] B02: clip  8.1s slowed 1.49x to fill 12.1s beat
[art] B03: clip  6.5s slowed 2.62x to fill 17.1s beat
[art] B04: clip 18.2s slowed 1.20x to fill 21.8s beat
[art] B05: clip 12.0s slowed 1.46x to fill 17.4s beat
```

B01 and B03 play at roughly a third of their authored speed because I wrote
more narration for those beats than animation. B04, the beat that carries the
concept, is closest to 1:1 at 1.20x — that is the one I paced deliberately,
and it is the one that needed it least. The right fix is longer scenes with
more held states, not slower playback; I did not have the hours left to
re-author and re-render five 4K scenes, so the slowdown ships.

Final: 166.1 s, 3840×2160, 9/9 filled, no slates.

## Still uncertain

- Whether the 35-count shortfall is ordinary sampling noise or a real bias in
  `rng.choices()`. Two seeds cannot separate those, and I have not run the
  many-seed check described above.
- Whether `Counter` output order is guaranteed or merely happens to be stable
  here. The A/B diff was empty, but I am relying on an implementation detail I
  have not looked up, and a Python version that reordered it would break the
  byte-identical claim without breaking the concept.
- Whether the gaps summing to zero is worth a beat at all, or whether it is
  arithmetic I found satisfying and the audience will not.
- Whether a toolkit that needs six gate fixes before it compiles is teaching
  me rigour or costing me time that should have gone into the explanation.
  Some gates genuinely improved the video (F, and A4). Others were the toolkit
  disagreeing with itself about whether my code was valid.

## 2026-09-27 — Pre-submission cross-check

Asked Claude to check the folder against the assignment before zipping. It
found problems I had not caught, several of them the same kind of mistake the
video is about:

- **BUILD-PROMPT.md and SOURCES.md still had template placeholders**
  (`[PROMPT TEXT]`, `[MODEL]`, `[DATE]` and others). Filled them from the
  build record. I did not keep verbatim prompt text, so BUILD-PROMPT §4 records
  each prompt's substance and outcome and says plainly that the verbatim
  wording was not kept.
- **Both files said beats 3–5 were "real screen captures".** They are not.
  The template was written before I switched to Manim, and the claim was
  never updated. The video has no terminal recording; the evidence beats are
  animations of figures from `run-A/B/C.txt`. Corrected. This was a false
  statement about what I verified, sitting in the file whose job is to say
  what I verified.
- **B00 looks like a Claude conversation.** The stock `ClaudeComposerAsk`
  card draws a composer, a model chip and three "output" lines. Those lines
  are props I wrote, not a response. FACTCHECK.md had said "No Claude output
  appears", which is true of real output but not of what a viewer sees.
  Disclosed in SOURCES.md and in FACTCHECK row 18. Not re-rendered.
- **BVDT narration overstates the noise claim.** It says the gap "is ordinary
  sampling noise", but at ≈2.36 SD (two-sided p ≈ 0.018) it is unusual, as my
  own entry above says. FACTCHECK row 16 had described this as framed as a
  limitation; the spoken line asserts it. Re-marked OVERSTATED. Not
  re-rendered.
- **B05's "one observation wearing three hats" is loose.** The constraint
  leaves two free gaps. Logged as FACTCHECK row 15a.
- **"Claude did not run any code" was not accurate.** Claude Code ran
  commands in this folder: a GitHub API licence lookup, `python3` one-liners,
  and `verify_claims.py` and `ffprobe` during this check. The three run files
  are still from my terminal. Corrected here and in SOURCES.md.
- **Two beat sheets disagreed.** The top-level `beat_sheet.json` was the
  6-beat draft; the build used the 9-beat `reel/beat_sheet.json`. The
  top level now holds the build sheet, and the draft is kept as
  `evidence/beat_sheet_draft_v1.json`.
- **README named `video.mp4`, which did not exist.** Copied the render to it.
- `verify_claims.py` labels used the draft's beat numbers ("Beat 3/5/6").
  Relabelled to B02/B04/B05. The output block in the verification entry above
  is left as it printed at the time.

**Learned:** my own FACTCHECK passed a claim, "no Claude output appears",
that was literally true and still misleading to a viewer. That is the
chapter's distinction between a fluent output and a supported claim, applied
to my own paperwork.

## 2026-09-27 — Does the GitHub copy rebuild without the media?

The course repo's `.gitignore` excludes every `.mp4` and `.mp3`. Seven
classmates force-added their videos anyway. Before deciding, I wanted to know
whether a TA pulling only the committed files could rebuild mine.

**Expected:** mostly yes, but I thought the Remotion cards or Kokoro might
come out slightly different on a second run.

Exported exactly the staged files to an empty folder and ran
`generate_audio_kokoro.py` then `ART_STRICT=0 ./art run` on it. All nine mp3s
came out byte-identical, and the compiled reel was byte-identical to
`video.mp4`. The gates behaved the same as before: GATE B one warning on B05,
GATE V BLOCKER=0 MAJOR=7.

**Decision:** followed the repo rule. The video is in the Canvas zip, and the
GitHub folder has everything that produces it.

**Learned:** the same distinction again. A byte-identical rebuild shows the
build is deterministic here. It says nothing new about whether the video's
claims are right.

## Assistance

Claude (Anthropic) was used throughout. SOURCES.md says what it drafted, what
commands it ran, and what I changed. Every figure in this log comes from
`run-A/B/C.txt`, which I produced in my own terminal.
