#!/usr/bin/env bash
# Put this reel's custom scenes into a brutalist.art checkout so it can render them.
#   bash scripts/install_scenes.sh /path/to/brutalist.art
# The scene source is stored here as src/scenes/PrefTune.tsx.txt because the course
# repository keeps no Node/TypeScript implementation files (AGENTS.md; the course
# validator rejects *.tsx). This copies it into the toolkit as scenes/PrefTune.tsx
# and applies src/Root.tsx.patch (registers the ten Pt* compositions).
# The data file the scenes read is written afterwards by scripts/set_props.py.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TK="$(cd "${1:?usage: install_scenes.sh /path/to/brutalist.art}" && pwd)"
cp "$HERE/src/scenes/PrefTune.tsx.txt" "$TK/runtime/remotion/src/scenes/PrefTune.tsx"
if grep -q "INFO7375-PrefTune" "$TK/runtime/remotion/src/Root.tsx"; then
  echo "Root.tsx already registers the Pt* scenes"
else
  (cd "$TK" && git apply "$HERE/src/Root.tsx.patch")
fi
echo "scenes installed into $TK"
