# BUILD-PROMPT — A training-scale slogan restated as a division with a hidden assumption

Paste-ready prompt that rebuilds this reel end to end. Free path only: Kokoro
`am_onyx`, Remotion-only, no Manim. Never publishes.

---

In the brutalist.art toolkit, rebuild the reel in this folder (call it `<reel>`;
on the original machine it was
`~/Desktop/Prompt_Engineering/reels/claude-liam-hidden-parameter`).

**Fresh clone only:** first do README step 1: copy `DerivationScenes.tsx` and
`ClaudeComposerAsk.tsx` into `runtime/remotion/src/scenes/`, and add the blocks in
`ROOT-REGISTRATION.md` to `runtime/remotion/src/Root.tsx`. Without this, the gate
check below fails.

Environment next, in this order:

    eval "$(/usr/libexec/path_helper)"        # only if MacTeX is installed; must PRECEDE the venv
    source .venv/bin/activate                 # Python 3.11 venv in the toolkit root
    ./setup                                   # all green except possibly LaTeX, which this video doesn't use

(Order matters: `path_helper` rebuilds PATH from /etc/paths and will push the
venv's python3 behind the system one if run afterwards.)

Then, in order:

1. **Gate check.** `./art scenes --check ScaleAnchorCard DerivationLadder
   AssumptionFan SurvivingClaim ClaimAudit ClaudeComposerAsk
   BrutalistHesitantWriter ClaudeVerdictArtifact BoundaryCard` — all must
   report RENDERABLE. If not, `./art scene-index` and re-check.
2. **Audio (the master clock).**
   `python3 runtime/scripts/generate_audio_kokoro.py <reel>`
   Twelve mp3s, `am_onyx`, ~3:29 total. An empty `mp3/` is a FAILED BUILD — stop
   and report, never ship silent.
3. **Render + compile.** `./art run <reel> --height 1080`
   → `claude-liam-hidden-parameter-slate.mp4` beside the reel.
4. **Visual QC (VISUAL QC LAW — the mp4 probe is not QC).** Sample frames
   (`ffmpeg -i <mp4> -vf fps=2 _qc/frames/%05d.png`), READ the PNGs, audit the
   nine-point rubric, log to `_qc/REPORT.md`, fix root causes in scene source,
   re-render until zero BLOCKER and zero MAJOR.
5. **Master + rename.** `./art final <reel> --height 1080 --out <reel>` writes
   `claude-liam-hidden-parameter.mp4` (named after the slug). Rename it:
   `mv <reel>/claude-liam-hidden-parameter.mp4 <reel>/ethan_gomes_week1_explainer_video.mp4`
6. **Captions.** `python3 runtime/scripts/align.py <reel>` writes word timings to
   `mp3/words.json`; then `python3 make_captions.py <reel> ethan_gomes_week1_explainer_video` writes
   `ethan_gomes_week1_explainer_video.srt`
   and `.vtt`. Re-run both only if any narration changes.
7. **Report** runtime, per-beat durations, and any defect left open.

Two traps specific to this reel:
- **B01 is a typed beat.** GATE V samples at 50% and 85% and expects steady
  state, so the typing must COMPLETE before the halfway mark. It is tuned to
  `charMs: 8`, `fontSize: 205`, three lines, stochastic pauses off. If you change
  the text, re-measure both sample frames before trusting a green gate.
- **`triggerWords` must be a single token.** `BrutalistHesitantWriter` tokenises
  on whitespace; a multi-word trigger silently never fires and the BLUF loses its
  correction without any error.

Hard constraints:
- Do not publish. `./art final` is only for the submission master.
- No paid API, no key, no Higgsfield beat. Cost must be $0.00.
- Never fix timing by editing durations — regenerate audio and recompile.
- Every number on screen is re-derivable; see FACTCHECK.md. If you change a
  figure, re-derive it and update that table in the same commit.
