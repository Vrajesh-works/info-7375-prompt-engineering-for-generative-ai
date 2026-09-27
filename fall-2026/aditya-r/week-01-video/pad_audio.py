#!/usr/bin/env python3
"""pad_audio.py — apply beat-level `lead_silence_s` / `tail_hold_s` to the
Kokoro MP3s, because this toolkit cut documents both fields (ai-explainer
SKILL.md B01 TIMING; OUTRO-LOCK.md 1.0 s tail) but no runtime script reads them.

Idempotent: the first run stashes the untouched Kokoro output in mp3/_raw/;
every run pads FROM that raw copy, then re-measures and writes the new
duration back to beat_sheet.json (actual_duration_s) and mp3/timings.json.
Re-run after any generate_audio_kokoro.py pass (which overwrites mp3/beat-*.mp3).

Usage: python3 pad_audio.py            (from the reel folder, or pass the path)
"""
import json, shutil, subprocess, sys
from pathlib import Path

reel = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent).resolve()
sheet_p, tim_p = reel / "beat_sheet.json", reel / "mp3" / "timings.json"
sheet = json.loads(sheet_p.read_text())
timings = json.loads(tim_p.read_text())
raw_dir = reel / "mp3" / "_raw"
raw_dir.mkdir(exist_ok=True)


def dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


for b in sheet["beats"]:
    lead, tail = float(b.get("lead_silence_s", 0)), float(b.get("tail_hold_s", 0))
    if not (lead or tail):
        continue
    mp3 = reel / b["audio_file"]
    raw = raw_dir / mp3.name
    # a freshly regenerated mp3 is newer than its stash: re-stash it
    if not raw.exists() or mp3.stat().st_mtime > raw.stat().st_mtime + 1:
        shutil.copy2(mp3, raw)
    filt = f"adelay={int(lead * 1000)}:all=1,apad=pad_dur={tail}"
    tmp = mp3.with_suffix(".tmp.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", filt,
                    "-c:a", "libmp3lame", "-q:a", "2", str(tmp)], check=True)
    tmp.replace(mp3)
    raw.touch()                                   # stash stays newer than the padded file's source
    d = round(dur(mp3), 2)
    b["actual_duration_s"] = d
    timings[b["beat_id"]] = d
    print(f"[pad] {b['beat_id']}: raw {dur(raw):.2f}s + lead {lead}s + tail {tail}s -> {d:.2f}s")

sheet_p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
tim_p.write_text(json.dumps(timings, indent=2) + "\n")
print(f"[pad] total runtime {sum(b.get('actual_duration_s', 0) for b in sheet['beats']):.2f}s")
