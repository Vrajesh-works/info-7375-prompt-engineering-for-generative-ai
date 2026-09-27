# BUILD-PROMPT.md

The commands and prompts that rebuild `video.mp4` from this folder.
Everything is local and free: Kokoro narration, Manim and Remotion renders.
No API keys, no paid generation, no upload.

## 1. Capture the evidence

```bash
git clone https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai
cd info-7375-prompt-engineering-for-generative-ai

python3 lessons/01-randomness-and-first-prompts/code/main.py | tee run-A.txt
python3 lessons/01-randomness-and-first-prompts/code/main.py | tee run-B.txt
diff run-A.txt run-B.txt

# edit the default argument on line 19: seed=7 -> seed=10
python3 lessons/01-randomness-and-first-prompts/code/main.py | tee run-C.txt
diff run-A.txt run-C.txt
# revert line 19 to seed=7
```

Where the seed is (`grep -n "seed" main.py`):

```
19:def sample(logits, count=1000, seed=7, temperature=1.0):
22:    rng = random.Random(seed)
```

diff A/B result: empty. The files are byte-for-byte identical.

diff A/C result:
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

Expected versus observed, used in B04 and B05 (probability × 1000):

| token | expected | observed (seed 7) | gap | observed (seed 10) | gap |
|-------|----------|-------------------|-----|--------------------|-----|
| 0 | 90.03 | 102 | +11.97 | 97 | +6.97 |
| 1 | 244.73 | 268 | +23.27 | 213 | -31.73 |
| 2 | 665.24 | 630 | -35.24 | 690 | +24.76 |

The seed-7 gaps sum to zero, because the counts total 1000 and the
probabilities total 1. So the three deviations are constrained rather than
three independent observations.

Check every on-screen figure against a fresh run:

```bash
# from this folder; set INFO7375_MAIN if the course repo is not in ~
INFO7375_MAIN=<course-repo>/lessons/01-randomness-and-first-prompts/code/main.py \
  python3 evidence/verify_claims.py      # 7/7
```

## 2. Toolkit setup

Brutalist commit used: `cd4bf20904be4e7d63babd9622b17963c2361b27`
(2026-09-26). See FRICTIONAL.md for why each of these steps was needed.

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art

brew install python@3.12                # manim<0.19 and kokoro-onnx need < 3.13
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

nvm install 20 && nvm use 20            # Remotion needs Node >= 20
./setup --install                       # downloads the Kokoro model (~340 MB)

python3 runtime/scripts/generate_audio_kokoro.py --list-voices   # confirm am_onyx
```

## 3. Build the reel

The reel folder is `reel/`. The build is driven by `reel/beat_sheet.json`,
with `beat_sheet.json` at the top level as a copy of it. Nine beats: five
Manim scenes in `reel/scenes.py` and four stock Brutalist Remotion patterns.

```bash
# (a) narration first — Kokoro am_onyx, durations written back into the sheet
python3 runtime/scripts/generate_audio_kokoro.py <path>/reel

# (b) optional quick preview of one Manim scene
cd <path>/reel && manim -ql scenes.py B04_ExpectedVsObserved && cd -

# (c) gates + render + compile. ART_STRICT=0 turns the remaining GATE V
#     underfill MAJORs into warnings (blockers were fixed first; see FRICTIONAL)
ART_STRICT=0 ./art run <path>/reel
```

Output: `reel/seeded-not-settled-slate.mp4` (the review cut, 9/9 slots filled,
no slates). Copy it to the top level:

```bash
cp reel/seeded-not-settled-slate.mp4 video.mp4
```

`./art final` refused at `final_frame_check.py` without printing a reason.
That is logged in FRICTIONAL.md and was not diagnosed.

## 4. Prompts used

I did not keep the verbatim text of the Claude prompts. Below are the
purpose, the substance, and what happened to each result. `reel/PROMPTS.md`
has the per-beat detail.

### Prompt 1: choosing the concept
Asked Claude which Chapter 1 concept could be shown with real terminal output
rather than asserted, and why it would fit the rubric.
Result: accepted (the seed). Rejected: an opening that defined
pseudo-randomness in the abstract, because the diff makes the point faster.

### Prompt 2: first beat sheet and narration
Asked Claude to draft a beat sheet around the three runs.
Result: revised. The 6-beat draft (kept as
`evidence/beat_sheet_draft_v1.json`) was restructured into the 9-beat
`ai-explainer` spine: Brutalist's required ASK / VERDICT / HANDOFF / OUTRO
bookends around five concept beats. The seed-10 beat became B03, and the
draft's "+24.76 overshoot" comparison was cut from it. The boundary statement moved from the last concept beat
into the verdict (BVDT).

### Prompt 3: expected versus observed
Claude pointed out that 630 in my own run matched a figure on the
assignment's concept list, and that p × 1000 = 665.24.
Result: accepted after checking. I computed the per-token table and the
sum-to-zero check, and `verify_claims.py` confirms both.

### Prompt 4: Manim scenes
Asked Claude to write the five scene classes in `reel/scenes.py` using the
real figures.
Result: revised six times, one round per gate failure (LaTeX, GATE A
namespace, GATE A static frames, GATE B layout, GATE V). The details are in
FRICTIONAL.md.

### Prompt 5: bookend props
The ASK (B00) and HANDOFF (BHTF) composer text and the three B00 "output"
lines were written as props for the stock `ClaudeComposerAsk` pattern.
**They are not a Claude conversation.** See SOURCES.md.

## 5. Screen captures

None. The video has no terminal recordings. The evidence beats (B02–B05) are
Manim animations that typeset the figures from `run-A/B/C.txt`, and
`verify_claims.py` checks those figures against a fresh run of `main.py`.

## 6. Pre-submit checklist

- [x] No template brackets left in any deliverable
- [x] Every on-screen figure matches run-A/B/C.txt (verify_claims.py 7/7)
- [x] B01 diagram labelled CONSTRUCTED ILLUSTRATION on screen
- [x] Runtime 2:46 (166.1 s)
- [x] The "does not establish" line is spoken in BVDT and shown on the verdict card
- [x] Seed reverted to 7 in the course repo copy
- [ ] Zip named correctly, GitHub pushed, final commit hash in Canvas
