# BUILD-PROMPT.md — how this video was actually built

Everything needed to rebuild this reel. This records the **Windows** build that
produced the submitted file, not a generic procedure. Several steps exist only
because of this machine's configuration; they are noted as such.

## 0. Versions

| Thing | Value |
|---|---|
| Course repo commit | `62992c08bbd0c72efc692ace3210baa7bf6be138` |
| Brutalist checkout commit | `cd4bf20904be4e7d63babd9622b17963c2361b27` |
| OS | Windows 11 |
| Python | 3.14.2 (CPython) |
| Node | 24.x |
| ffmpeg | 9.0.2 (installed via `winget install Gyan.FFmpeg`) |
| Voice | Kokoro `af_bella`, local |
| Render date | 2026-09-27 |
| Final runtime | 3:37.9 |

## 1. Produce the evidence first

```bash
python3 C:\Users\zyud0\info-7375\fall-2026\yudan-z\week-01-video\evidence\max_subtraction_evidence.py
```

Every number shown in the reel comes from the resulting `evidence_output.json`.
Do this before building anything, so the beat sheet is written against real
output rather than remembered figures.

Note: the values in `evidence_output.json` are from **this** machine. Case A's
unshifted values differ from a Linux / Python 3.11.15 run in the last two digits
(…046→…045, …767→…764), while `max_abs_difference` and cases B and C are
identical. That difference is itself evidence for the reel's Beat D claim.

## 2. Install the toolkit — what actually happened

```bash
cd C:\Users\zyud0
git -c core.longpaths=true clone https://github.com/nikbearbrown/brutalist.art.git brutalist
cd brutalist
python3 -m venv .venv
```

**The checkout must live at a short path.** The first attempt failed at clone
with `'$GIT_DIR' too big`, and a later attempt installed successfully but Kokoro
could not synthesize: espeak-ng truncated its own data path (261 characters) at
`site-packages\` and then could not find `phontab`. Windows 8.3 short paths did
not help, and kokoro-onnx exposes no override. Re-cloning to
`C:\Users\zyud0\brutalist` fixed it — and fixed the esbuild failure below at the
same time, since both had the same root cause.

**Manim cannot be installed on Python 3.14.** manim 0.18 requires Python < 3.13,
and there are no 3.14 wheels for manimpango or `Pillow<11` either. Because pip
resolves `requirements.txt` as a unit, this also prevented `kokoro-onnx` from
installing, which silently broke narration. Install the needed packages
individually instead:

```bash
python3 -m pip install "kokoro-onnx>=0.4" "mutagen>=1.47,<1.48" Pillow numpy \
    "faster-whisper>=1.0,<2" matplotlib scipy
python3 runtime/scripts/setup_smoke_kokoro.py     # expect: kokoro synth OK
```

Manim is not needed for this reel — no beat uses equation rendering. Beat C's
mathematics is typeset by `TypesetMath`, which uses matplotlib's math renderer,
not LaTeX. `scipy` is required by Gate T; without it that gate silently skips
instead of running.

**`./setup` never prints its readiness table.** Its ElevenLabs guard greps the
whole checkout and matches the toolkit's own bundled example beat sheets under
`youtube/`, then exits 1. This is an upstream condition, not a broken install.
Verify the toolkit with `./art --list` instead. The toolkit was not edited to
make that check pass.

**Windows-specific settings used, none of which modify the toolkit's source:**

| Setting | Why |
|---|---|
| `PYTHONUTF8=1` | Windows defaults to cp1252; toolkit scripts crash on it |
| `npx.exe` shim in the reel folder | Python on Windows cannot launch `npx.cmd` without a shell |
| `ART_CHROME` → installed Chrome | renders headless with a separate temp profile, so no browser download and sign-ins are untouched |
| `ART_NO_DRAWTEXT=1` | the review timecode filter breaks on Windows paths |

**Fonts.** EB Garamond is not installed for this user, so Chrome renders the
serif as Georgia. This was recorded rather than fixed, since installing fonts is
a system-wide change. The shared monospace token fell back to NSimSun, a Chinese
system font, which is legible but does not read as code; Consolas was appended
to the toolkit's shared font list in `runtime/remotion/src/tokens/claude.ts`,
after the Mac fonts, so Macs render as before.

## 3. Toolkit changes made for this reel

All local to `C:\Users\zyud0\brutalist`, none contributed upstream:

- Added `runtime/remotion/src/illustrations/ArrayPipeline.tsx` — a parameterized
  stage-by-stage array view. The scene library had no reusable component for
  this, and the toolkit's own rule (GATE L) is to build rather than slate. Every
  value, label and reveal time comes from props; nothing about the evidence is
  hard-coded.
- Registered it in `Root.tsx` in both 16:9 and 9:16, then ran `./art scene-index`.
- Appended Consolas to the shared monospace token (above).
- Installed matplotlib and scipy into the toolkit's `.venv`.

## 4. Build the reel

Claude Code was started from the activated toolkit environment with normal
permissions and given the evidence folder and `SCRIPT.md` as the content plan.
The full prompt and the decisions taken are in `build/BUILD-LOG.md` and
`build/PROMPTS.md`.

Two reel-local scripts were written rather than reusing toolkit ones:

- `build_sheet.py` — generates `beat_sheet.json` and **refuses to write it if any
  on-screen number is not present in `evidence_output.json`**. 60 number tokens
  were checked and all were found. A negative test confirmed the gate rejects a
  value that is not in the file (it correctly rejected `SCRIPT.md`'s rounded
  10-digit weights).
- `cue_times.py` — measures cue word timings by re-synthesizing the narration in
  chunks, avoiding a 145MB Whisper model download.

Beat C's algebra was checked numerically to 50 digits at T = 0.5, 1 and 2. See
`build/FACTCHECK.md` and `build/CHECKS-REPORT.md`.

## 5. Review and revise

The review cut (`…-slate.mp4`, which carries beat-ID labels) was watched in full
with sound. Three problems were found by watching and listening that a frame
check cannot catch:

1. Kokoro read "INFO 7375" as "info seven thousand three hundred seventy-five".
   Fixed by writing the narration as "INFO seven three seven five" and
   re-synthesizing B00.
2. The stage-to-stage arrows in B02, B03, B06 and B07 were too faint to carry
   meaning. Made larger, bold and full ink.
3. Confirmed the beat-ID slate is review-only — `compile.py` draws it only for
   `--review` cuts, and frames of the final master carry no label.

Gate V's remaining B01 failure was fixed by shortening the typed text so all
three lines are on screen by the halfway frame. `ART_STRICT=0` was **not** used.

Gate T (contrast) blocked the first export: thin terracotta outlines and
terracotta text measured 2.74:1. Highlighted elements now use a light terracotta
fill with bold ink text, and small text was enlarged.

**Known limitation, accepted:** B06's number cells are about 20px at 1080p and
read small. They pass every gate. Re-rendering for this was declined.

## 6. Final export

```bash
./art final <reel> --height 1080 --out <reel>/final
```

1080p was chosen explicitly; the toolkit defaults to 4K. Result: 1920×1080,
24 fps, H.264 + AAC, 3:37.9, 7,031,809 bytes (6.7 MB). A verification receipt
sits beside it as `week01-max-subtraction-yudan-z.verified.json` with status
`ready`.

Nothing under `lessons/` or `chapters/` was modified, and nothing was published.

## 7. Ship

```bash
cd C:\Users\zyud0\info-7375
git add fall-2026/yudan-z/week-01-video
git commit -m "week 01 video: max-subtraction explainer for Yudan Zhou"
git push
git rev-parse HEAD    # this hash goes in README.md and in Canvas
```

Zip the folder as `Zhou_Yudan_INFO7375_Week01_Video.zip`, excluding
`__pycache__`, and submit it with the GitHub folder link and the final commit
hash.
