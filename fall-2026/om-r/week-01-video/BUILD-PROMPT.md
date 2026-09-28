# BUILD-PROMPT.md — rebuilding this video from scratch

This is the real build sequence, corrected after actually running it start to
finish. An earlier draft of this file guessed at commands that turned out not
to exist. Every fix mentioned briefly here is logged in full in
`FRICTIONAL.md` — this file is the sequence, that one is the why.

## 1. Get the chapter's reference implementation

```bash
git clone https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai
cd info-7375-prompt-engineering-for-generative-ai/lessons/01-randomness-and-first-prompts/code
python3 main.py
```

## 2. Capture the real numbers this video uses

Copy `demo.py` (from the GitHub repo) into that same folder and run it:

```bash
python3 demo.py
```

This prints, verbatim, every number used in the video: the real `ValueError`
at `temperature=0`; real `sample()` counts at `temperature=0.5, seed=7,
count=1000` (`{0: 18, 1: 133, 2: 849}` — matches the chapter's own published
table); and the constructed contrast function `argmax_select()`'s output
(`{2: 1000}`, zero variance by construction).

For the fact-check step (step 7), also run:
```bash
python3 -c "from main import probabilities, sample; print(probabilities([1,2,3], temperature=0.1)); print(sample([1,2,3], count=1000, seed=7, temperature=0.1)); print(probabilities([1,2,3], temperature=0.001))"
```

## 3. Set up Brutalist

```bash
git clone https://github.com/nikbearbrown/brutalist.art
cd brutalist.art
```

If `pip` is missing for your Python install:
```bash
python3.11 -m ensurepip --upgrade
```
If `ffmpeg` is missing (Manim will fail with a clear error naming this):
```bash
brew install ffmpeg
```
Then:
```bash
./setup --install
```

**Known toolkit bug, fixed locally:** `FormBCard` (used in beat B01) looks
for icons in `runtime/remotion/public/form-b-icons/`, a folder that doesn't
exist in a fresh clone. Before rendering B01, copy the icons it needs from
the toolkit's own bundled set:
```bash
mkdir -p runtime/remotion/public/form-b-icons
cp icons/svg/zap.svg icons/svg/target.svg icons/svg/list-checks.svg icons/svg/check-circle.svg \
   runtime/remotion/public/form-b-icons/
```

## 4. Place the reel

```bash
mkdir -p youtube/low-temperature-is-not-argmax
```
Copy in `beat_sheet.json`, `scenes.py`, and `demo.py` (from the GitHub repo).

## 5. Generate narration audio (the master clock)

```bash
python3 runtime/scripts/generate_audio_kokoro.py youtube/low-temperature-is-not-argmax
```
Confirm the voice code is a real Kokoro voice (`--list-voices` lists valid
ones) — a persona/channel name like `claude-liam` in the `voice` metadata
field will fail here.

## 6. Compile the review cut

```bash
ART_FACTS=0 ./art run youtube/low-temperature-is-not-argmax
```
`ART_FACTS=0` is a documented previz-only bypass for the paperwork gate
(`GATE F`) — it is never sufficient for a real final render (step 8 refuses
it). Expect to iterate here: this build hit four separate categories of gate
failure before passing cleanly —
- **Gate A** (static pre-flight): a Manim scene whose shapes never visibly
  change reads as the toolkit's "repeated animation" defect. Fix: make sure
  every meaningful visual change happens as its own `self.play()` call that
  actually adds/removes/transforms mobjects, not a single call with the
  final geometry already baked into the object at construction time.
- **Gate W** (WCAG/text rules): don't put chapter numbers on screen — name
  the topic instead. Also check for accidentally-hardcoded branding (see
  step 6a).
- **Gate B** (layout audit, strict mode): keep edge-anchored text well
  inside the safe area (±6.3 horizontally, ±3.4 vertically), not flush
  against its edges.
- **Gate V** (frame-level canvas-fill, ≥55% of the safe area must be
  covered by content at 50%/85% of every beat): a short, centered line of
  text on an otherwise-empty card will not pass. A slate/placeholder beat
  with no real scene will not pass. A Manim scene stretched far beyond its
  natural animation length by mismatched narration timing will not pass
  either — retime the scene to the actual measured audio duration instead
  of letting the compiler stretch it.

### 6a. Check for accidentally-inherited toolkit branding
If you built your beat sheet from one of Brutalist's own worked examples (as
this build did), check narration and on-screen fields for the toolkit's
default persona ("This is Liam, in for Bear") and its default handle
(`@NikBearBrown`) before treating a clean gate pass as "done" — passing every
gate does not mean the content is actually yours. `ClaudeTitleOutro`
hardcodes this handle in the component itself; swap to a different closing
component (e.g. `ClaudeVerdictArtifact`) rather than editing shared toolkit
source.

## 7. Fact-check every claim before finalizing — this is not optional

`./art final` requires a genuinely-completed `FACTCHECK.md`, not a bypass.
Re-derive every specific, checkable claim in the narration against the actual
reference implementation, not just the one data point shown running on
screen. This build's fact-check caught a real error this way: a claim that
held at `T=0.5` (the only value run live in the video) turned out to be false
at lower temperatures — see `FACTCHECK.md` in the GitHub repo and
`FRICTIONAL.md`'s last entry
for the full correction. Any wording change here means regenerating that
beat's audio and re-rendering it before rerunning step 6.

Also write `SHOTLIST.md` (a typed per-beat work order derived from the beat
sheet) and `PROMPTS.md` (beat-prefixed generation prompts for any open
slots — if every beat renders from this folder's own Remotion/Manim sources,
as this one does, state plainly that there are no open slots).

## 8. Produce the final master

```bash
./art final youtube/low-temperature-is-not-argmax
```
This does not read the previous `./art run`'s results — it runs its own
independent checks: the paperwork (`FACTCHECK.md`, `SHOTLIST.md`, and
`PROMPTS.md` must all be non-empty), approvals, the beat-lint and shape
gates, complete visuals (no slates), sound and duration, a full decode, and a
final-frame inspection of the new export. It refuses to write a master if
any of them fails.
On success it writes the master mp4, a SHA-256 hash of the output plus every
input file, into `build-state.json`.

## Before submitting

Cross-check every on-screen number and spoken claim in the final master
against a real run of `demo.py` (and, for anything about behavior at
temperatures beyond what's shown running on screen, against `FACTCHECK.md`
in the GitHub repo).
If anything doesn't trace back to something actually run, fix the video, not
the write-up.
