# Toolkit changes needed to rebuild this video

Base revision: **brutalist.art `6a8380ae169cca81e0633664a65c958f5c12ab4b`**
(`git rev-parse HEAD` of the checkout this video was built from).

`toolkit.patch` was applied to a clean worktree of that revision: no conflicts, and the three
new files it creates came out byte-identical to the ones this video was rendered from.

**Why everything is in one patch:** the course repository's CI (`scripts/validate_course.py`)
rejects `.ts` / `.tsx` files, and the course guide asks to keep the Node/Remotion runtime outside
the course. So the new scene sources travel as a patch against the toolkit, not as files here.

## Apply

```bash
cd brutalist.art
git checkout 6a8380ae169cca81e0633664a65c958f5c12ab4b
git apply path/to/week-01-video/toolkit-changes/toolkit.patch
```

## What the patch changes (6 modified files)

| File | Change | Why |
|---|---|---|
| `setup` | `--exclude-dir=youtube` on both ElevenLabs-guard greps | the guard matched the toolkit's own documentation and aborted before printing any readiness table |
| `examples/_smoke/beat_sheet.json` | slug `_smoke` → `smoke` | `build_safety.py` rejects a leading underscore, so `./art smoke` failed on every platform |
| `runtime/scripts/smoke_test.sh` | output name `_smoke-slate.mp4` → `smoke-slate.mp4` | follows the slug rename |
| `runtime/scripts/compile.py` | quote + escape the `drawtext` font path; add opt-in `ART_BURNIN=0` | Windows paths break ffmpeg's filtergraph parser; the switch drops review burn-ins while keeping every gate |
| `runtime/scripts/remotion_scenes.py` | resolve `npx` via `shutil.which` | on Windows `npx` is `npx.CMD`, so a bare `"npx"` raised WinError 2 |
| `runtime/remotion/src/Root.tsx` | register this video's compositions | so `remotion render <id>` can find them |

## What the patch adds (3 new files)

| File | What |
|---|---|
| `pretraining.tsx` | the scene components for this video |
| `pretraining_trajectory.ts` | generated from `../code/trajectory.json` — all 601 real steps |
| `molecular.tsx` | from an earlier practice reel. Included only because `pretraining.tsx` imports its `BrandBug` corner mark and `Root.tsx` registers its compositions; none of its scenes appear in this video |

`package-lock.json` also changed locally, but only because `npm install` rewrote it; it is
not part of these changes.
