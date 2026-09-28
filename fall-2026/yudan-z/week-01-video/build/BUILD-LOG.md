# BUILD-LOG.md — week01-max-subtraction-yudan-z

Built 2026-09-27 on Windows 11, Python 3.14.2 (toolkit `.venv`), Node 24.11.1, ffmpeg 9.0.2.
brutalist.art checkout `C:\Users\zyud0\brutalist` at `cd4bf20904be4e7d63babd9622b17963c2361b27`
(plus the local change below). Course repo `62992c0`. Reel output: `C:\Users\zyud0\reel-week01`,
outside both repos by the author's choice. The skill's "videos travel with their book" default is not used.

## Toolkit change (made by Yudan Zhou for this reel; local only, not contributed upstream)

`./art scenes` found no reusable scene for "values transformed stage by stage" (hits were
one-off reel figures with hard-coded content), so, as GATE L directs, a component was added:

- **Added** `runtime/remotion/src/illustrations/ArrayPipeline.tsx`. It has one or two lanes of stages.
  Each stage is a label plus up to 4 verbatim string cells, or an error line, revealed at `at` seconds.
  There is one terracotta accent (a stage border or specific cells) and an optional corner `brandLabel`.
  No values are hard-coded; the default props render a "set cells from evidence" warning.
- **Edited** `runtime/remotion/src/Root.tsx` (+10 lines) to register `ArrayPipeline` (1920×1080) and
  `ArrayPipeline916` (1080×1920), duration from `durationSeconds`.
- **Regenerated** by `./art scene-index`: `runtime/remotion/src/scenes.json`, `SCENE-DOC-TODO.md`.
  The large diff in `scenes.json` is the full regeneration on this machine, not hand edits.
- **Side effects, not authored:** `runtime/remotion/package-lock.json` came from `npm install` during
  setup, and the git-ignored `runtime/remotion/_bench/consumers.json` is updated by `remotion_scenes.py`.
- **Edited** `runtime/remotion/src/tokens/claude.ts`: `CLAUDE_FONT.mono` gains `Consolas` before the generic `monospace`.
- **Venv:** `scipy` 1.18.1 installed so GATE T (`type_check.py`) runs instead of skipping.
- **Venv:** `matplotlib` 3.11.2 was installed into the toolkit's `.venv`, as `TypesetMath` needs it
  through `typeset_math.py` (matplotlib mathtext, no LaTeX).

Revert with `git -C C:\Users\zyud0\brutalist checkout -- runtime/remotion/src/Root.tsx runtime/remotion/src/scenes.json SCENE-DOC-TODO.md`
and delete `ArrayPipeline.tsx`.

## Windows workarounds (no toolkit source edited)

| Problem | Workaround |
|---|---|
| Toolkit scripts read UTF-8 files with Windows' cp1252 default (`scene-index` crashed) | `PYTHONUTF8=1` for every toolkit script |
| `remotion_scenes.py` spawns `npx` without a shell; Windows can't run `npx.cmd` that way (`WinError 2`) | reel-local `npx.exe` console-script shim in `tools/.shim-venv` that forwards to `npx.cmd` (`tools/npxshim/`) |
| No Remotion headless browser bundled (the first render would download one) | `ART_CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe`, `ART_CHROME_MODE=chrome-for-testing` (the toolkit's documented override) |
| Chrome's generic `monospace` resolves to NSimSun on this CJK-locale Windows | `ArrayPipeline` names Consolas first; shared token `CLAUDE_FONT.mono` in `tokens/claude.ts` now lists Consolas after Menlo (fixes B00/B05/B09; macOS stacks unchanged) — author-approved toolkit edit, 2026-09-27 |
| EB Garamond is not installed system-wide, and Remotion doesn't load it | Serif renders as Georgia everywhere; overlays use Georgia to match. **Kept by author decision** (no system-wide font change) |
| `lead_silence_s` is not implemented by `generate_audio_kokoro.py` or `compile.py` | Kept on B01 as the skill requires. B01's audio is 11.88 s (≥ 9 s); typing sped up (`charMs` 25, no random typos) so the correction lands on screen |
| compile.py's review timecode (`drawtext`) embeds the font path unescaped; ffmpeg rejects `C:\…` | `ART_NO_DRAWTEXT=1` (compile.py's own switch): Pillow labels, no running timecode on the review cut |
| `remotion_scenes.py` and `compile.py` both clock beats from `actual_duration_s`; a `render_duration_s`/`tail_hold_s` override is recomputed away | Outro narration extended instead (see below); no timing edited by hand |
| `TypesetMath` is registered at a fixed 450 frames (15 s) with no duration override | B04 row 3 clamped to 14.5 s. It appears ~0.6 s before the spoken "It cancels" (15.1 s), which would otherwise never render |
| `BrutalistHesitantWriter` splits `replacementWords` on commas and matches triggers per whitespace token | Replacement written with an em dash: `distribution` → `weights — not the distribution` |

## Visual QC log (frames read at 15/50/85% of every beat; details in `_qc/`)

| Round | Found | Fix |
|---|---|---|
| 1 | ArrayPipeline number cells in NSimSun (CJK default monospace); small cells in full-width boxes | Consolas first in the stack; content-sized boxes, larger max size |
| 2 | B06/B07 lane headings collided with the title; rows overran the footnote; mismatched lane sizes; B01 correction never landed; B04 row 3 never shown; B05 "recorded output" label invisible; B08 number wrapped across lines; B10 corner label mis-scaled (the FormACard clip is 8K) | Shared height+width fit; top-aligned lanes; auto-fit labels; faster typing; row-3 clamp; label moved to the spark line; four verdict lines; overlay reads clip size |
| 3 | B01 replacement cut at the comma ("It changes the weights."); B06 type too small; B01 underfill | Em-dash replacement; tighter arrows and gaps |
| 4 | B01 corrected line crossed title-safe (Gate V BLOCKER); B02 arrows misaligned and figure in the left half | B01 font 88 → 72; lane blocks centered, arrows aligned to the boxes |
| 6 | Author review: "INFO 7375" spoken as a number; arrows too faint; NSimSun in B00/B05/B09; B01_50 underfill | B00 narration says "INFO seven three seven five" (re-synthesized); arrows 44u, bold, full ink; mono token fix; B01 line 1 → "Why subtract the max first?" and no between-word hesitation. Gate V clean (0/0) without ART_STRICT=0 |
| 7 | GATE T blocked the final: B05 §8.12b/§8.13 (non-filename title; corner label flush with the card edge read as clipped text), B06/B07 §8.3 (thin terracotta outlines read as terracotta text), B07 §8.1 (spark-line x-height 37px < 41px) | B05 title `evidence_output.json`, corner label by inset overlay; accents are a terracotta wash + bold ink; spark line 48u; labels/footnote ≥30u. GATE T PASS, Gate V 0/0. **Known:** B06's number cells are small (~20u) at 1080p |
| 5 | B01 at 72 underfilled (MAJOR at 50% and 85%) | B01 font 80: the final line fits title-safe and the 85% frame passes. **Open:** Gate V still flags B01_50 (MAJOR underfill) — the frame is mid-typing, with ~1.5 of 3 lines written. Not bypassed with ART_STRICT=0; left for the author to decide |

## Narration changes after the 2026-09-27 review (not yet reviewed by the author)

- B00 and B09 trimmed further to reach ~3:30 (texts in `build_sheet.py`).
- B10 (outro): "What Subtracting the Maximum Changes." → "What Subtracting the Maximum Changes. A Week 1 explainer by
  Yudan Zhou." A 2.2 s outro showed the synthetic-narration and affiliation lines for under half a second.

## Timing

Reveal times come from `cue_times.py`. It re-synthesizes each beat in chunks at its cue phrases with the
same Kokoro voice, scaled to the measured mp3. No speech-recognition model is downloaded.
Measured audio after the B10 change: **218.75 s = 3:38.8** (the compiled review cut reports 218.8 s).

## Deviations from the skill, decided by the author

See `CHECKS-REPORT.md`. There is no channel identity or Liam, the outro is a plain FormACard, and the
B01 correction is a single word (the component matches triggers per word).

## Final master (2026-09-27)

`./art final <reel> --height 1080 --out C:\Users\zyud0\reel-week01\final` wrote
`final\week01-max-subtraction-yudan-z.mp4`: 1920×1080, 24 fps, H.264 + AAC, 217.92 s, 7,031,809 bytes,
sha256 `282599e5d226af8849b45867d9288e014f90f06c8b95ee71a8e48ad9bebbe2a1`. The receipt
`week01-max-subtraction-yudan-z.verified.json` reports status `ready`. GATE T PASS; no review labels in the master.
