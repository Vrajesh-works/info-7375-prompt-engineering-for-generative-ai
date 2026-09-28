# Week 1 Explainer Video — INFO 7375

**Student:** Yudan (Anica) Zhou
**Assignment:** Week 1 Explainer Video — Explain One Concept from Chapter 1 (25 points)
**Canvas file:** `Zhou_Yudan_INFO7375_Week01_Video.zip`
**GitHub folder:** `fall-2026/yudan-z/week-01-video/`
**Final commit hash:** `528cda94fc5dd448a6d07508687c44f6beb49d63`

## The concept

**Why the reference implementation subtracts the maximum score before
exponentiating — what that changes and what it does not.**
Chapter 1, Part 2, "The subtraction that changes nothing important."

**Why this one.** It is the smallest idea in the chapter that can be *shown*
rather than asserted: the intermediate weights visibly change while the returned
distribution visibly does not, and the case it exists for (`[1000, 1000]`) fails
loudly enough to put real error output on screen.

**Runtime:** 3:37.9 · 1920×1080 · synthetic narration (Kokoro `af_bella`)

## Contents

| File | What it is |
|---|---|
| `Zhou_Yudan_Week01.mp4` | the rendered video (6.7 MB) |
| `SCRIPT.md` | the reviewed narration and visual plan, plus the claims I must defend |
| `beat_sheet.json` | the beat sheet the builder produced from `SCRIPT.md` |
| `BUILD-PROMPT.md` | the prompts, settings and commands that rebuild it on Windows |
| `SOURCES.md` | what I used, what I made, what Claude contributed, third-party assets and licences |
| `FRICTIONAL.md` | dated log of what I actually tried, hit, and decided |
| `evidence/max_subtraction_evidence.py` | the script that produces every number in the video |
| `evidence/evidence_output.json` | its recorded output, from this machine |
| `build/FACTCHECK.md` | each on-screen claim checked against its source |
| `build/CHECKS-REPORT.md` | the evidence gate, its negative test, and the algebra check |
| `build/BUILD-LOG.md` | the full QC history and every toolkit change |
| `build/SHOTLIST.md` | beat-by-beat shot list |

## Reproduce the numbers

The script imports the course reference implementation in place and does not
modify it. From anywhere inside a checkout of
[`info-7375-prompt-engineering-for-generative-ai`](https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai):

```bash
python3 fall-2026/yudan-z/week-01-video/evidence/max_subtraction_evidence.py
```

It prints three cases and rewrites `evidence/evidence_output.json`. Requires
Python 3.11+ and the standard library only — no API key, no network, no
third-party package.

The recorded run in this folder is from Windows 11 / Python 3.14.2. Case A's
unshifted values differ from a Linux / Python 3.11.15 run in the last two digits;
`max_abs_difference` and cases B and C are identical. That is discussed in
`SCRIPT.md` and `FRICTIONAL.md`.

The lesson's own reference run, for comparison:

```bash
python3 lessons/01-randomness-and-first-prompts/code/main.py
```

## Rebuild the video

See `BUILD-PROMPT.md`. It records the Brutalist checkout revision, the Windows
settings required, the two toolkit changes made, the builder prompt, and the
render commands.

## Verification

Every number on screen is machine-checked against `evidence/evidence_output.json`
by the generator in `build/CHECKS-REPORT.md` — 60 tokens, all present, with a
negative test confirming the gate rejects a value that is not in the file. Beat
C's algebra is checked numerically to 50 digits at three temperatures.

What this does **not** establish is stated in the video itself and in
`SCRIPT.md`: the subtraction does not make the implementation numerically stable.
`[0, -1000]` still underflows to exactly `0.0` for an outcome whose probability
is about `5.08e-435`.

## Credits and AI use

See `SOURCES.md`. Narration is synthetic (local Kokoro `af_bella`); it is not my
voice, not the instructor's, and implies no endorsement. The reel is styled after
the Claude desktop app and is not affiliated with or endorsed by Anthropic.
Claude assisted as recorded in `SOURCES.md`. I am responsible for this submission
and can explain every part of it.
