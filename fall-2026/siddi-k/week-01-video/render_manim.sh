#!/usr/bin/env bash
# Render the Manim beats and place them in the manim/<BEAT>.mp4 slots that
# brutalist.art's compile.py picks up. Run from anywhere; needs manim on PATH.
#   ./render_manim.sh            # all Manim beats
#   ./render_manim.sh B03        # one beat
set -euo pipefail
cd "$(dirname "$0")"
declare -A SCENES=([B02]=B02TwoRoutes [B03]=B03Cancel [B04]=B04Overflow
                   [B05]=B05Offset [B06]=B06Boundary [BOUT]=BOUTTitle)
python code/evidence.py > /dev/null            # numbers first, always fresh
mkdir -p manim
for bid in ${1:-B02 B03 B04 B05 B06 BOUT}; do
  scene=${SCENES[$bid]}
  manim -r 1920,1080 --fps 30 --media_dir _manim --disable_caching -v WARNING \
        scenes.py "$scene"
  cp "_manim/videos/scenes/1080p30/$scene.mp4" "manim/$bid.mp4"
  echo "[manim] $bid <- $scene"
done
