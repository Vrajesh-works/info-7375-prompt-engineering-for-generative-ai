#!/usr/bin/env bash
# publish.sh — push the current iteration of the video to the course repo.
#
#   bash code/publish.sh "v4: slow down B03, clearer ratio beat"
#
# Syncs this folder into fall-2026/mayank-b/week-01-video/ (same exclusions as
# .gitignore), force-adds the mp4 (the course repo ignores *.mp4), commits with
# the given message, rebases on main, pushes, and prints the commit hash.
set -euo pipefail
MSG="${1:?usage: publish.sh \"vN: what changed\"}"
REEL="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$REEL/../info-7375-repo"
DEST="$REPO/fall-2026/mayank-b/week-01-video"

[ -d "$REPO/.git" ] || { echo "no repo clone at $REPO"; exit 1; }
git -C "$REPO" pull -q --rebase origin main
mkdir -p "$DEST"
rsync -a --delete --delete-excluded --exclude-from="$REEL/.gitignore" --exclude '_qc/clean_check.png' \
  --exclude 'mp3/*.mp3' "$REEL/" "$DEST/"

python3 "$REEL/code/check_repo_rules.py" "$DEST" || { echo "blocked: would fail course CI"; exit 1; }

cd "$REPO"
git add -A fall-2026/mayank-b/week-01-video
# v8.1: no media on GitHub (instructor's request). Refuse to push if any slipped in.
if git ls-files fall-2026/mayank-b | grep -qiE '\.(mp4|mov|webm|mp3|wav|m4a)$'; then
  echo "blocked: media files are tracked under mayank-b"; exit 1; fi
if git diff --cached --quiet; then echo "nothing changed — no commit"; exit 0; fi
git diff --cached --stat | tail -1
git commit -q -m "docs(fall-2026): mayank-b Week 01 — $MSG" \
  -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git pull -q --rebase origin main
git push -q origin HEAD:main
echo "pushed $(git rev-parse HEAD)"
