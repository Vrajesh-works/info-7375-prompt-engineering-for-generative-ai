"""Build SRT/VTT captions from align.py's words.json, offset by each compiled clip's real length.

Usage: python3 make_captions.py <reel> [video-basename]
Writes <video-basename>.srt/.vtt next to the video (default basename: the reel slug).
"""
import json
import subprocess
import sys
from pathlib import Path

reel = Path(sys.argv[1])
slug = sys.argv[2] if len(sys.argv) > 2 else json.loads((reel / "beat_sheet.json").read_text())["metadata"]["slug"]
words = json.loads((reel / "mp3" / "words.json").read_text())
fps = words.get("fps", 24)
beat_ids = [b["beat_id"] for b in json.loads((reel / "beat_sheet.json").read_text())["beats"]]

def clip_len(bid):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(reel / "clips" / f"{bid}.mp4")],
                         capture_output=True, text=True, check=True).stdout
    return float(out)

MAX_LINE, MAX_CHARS, MAX_DUR = 42, 84, 6.0
cues, offset = [], 0.0
for bid in beat_ids:
    ws = words["beats"].get(bid, [])
    cur = []
    def flush():
        if cur:
            cues.append([offset + cur[0]["startFrame"] / fps, offset + cur[-1]["endFrame"] / fps,
                         " ".join(w["text"] for w in cur)])
            cur.clear()
    for w in ws:
        text = " ".join(x["text"] for x in cur + [w])
        dur = (w["endFrame"] - (cur[0]["startFrame"] if cur else w["startFrame"])) / fps
        if cur and (len(text) > MAX_CHARS or dur > MAX_DUR):
            # a word that closes the sentence may run a little long rather than dangle alone
            if w["text"][-1:] in ".?!" and len(text) <= MAX_CHARS + 8:
                cur.append(w); flush(); continue
            # otherwise split after the last punctuation in the cue, carrying the tail forward
            cut = max((i for i, x in enumerate(cur[:-1]) if x["text"][-1:] in ",.;:—?!"), default=None)
            tail = cur[cut + 1:] if cut is not None and cut >= len(cur) // 3 else []
            del cur[len(cur) - len(tail):]
            flush()
            cur.extend(tail)
        cur.append(w)
        t = " ".join(x["text"] for x in cur)
        if w["text"][-1:] in ".?!" and len(t) >= 18:
            flush()
        elif w["text"][-1:] in ",;:—" and len(t) >= 55:
            flush()
    flush()
    offset += clip_len(bid)

# readability: hold each cue until just before the next (max +0.6s), min 1.0s on screen
master_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                   "csv=p=0", str(reel / f"{slug}.mp4")], capture_output=True, text=True).stdout)
for i, c in enumerate(cues):
    nxt = cues[i + 1][0] if i + 1 < len(cues) else master_len
    c[1] = min(max(c[1] + 0.6, c[0] + 1.0), nxt - 0.04)

# Words spelled out only so the TTS pronounces them right; show them normally on screen.
DISPLAY = {"Info seven three seven five": "INFO 7375"}
for c in cues:
    for spoken, shown in DISPLAY.items():
        c[2] = c[2].replace(spoken, shown)

def wrap(t):
    if len(t) <= MAX_LINE:
        return t
    best = min(range(1, len(t)), key=lambda k: abs(k - len(t) / 2) if t[k] == " " else 1e9)
    return t[:best] + "\n" + t[best + 1:]

def ts(s, sep):
    h, r = divmod(s, 3600); m, r = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(r):02d}{sep}{int(round((r % 1) * 1000)) % 1000:03d}"

srt = "\n".join(f"{i}\n{ts(a, ',')} --> {ts(b, ',')}\n{wrap(t)}\n" for i, (a, b, t) in enumerate(cues, 1))
vtt = "WEBVTT\n\n" + "\n".join(f"{ts(a, '.')} --> {ts(b, '.')}\n{wrap(t)}\n" for a, b, t in cues)
(reel / f"{slug}.srt").write_text(srt)
(reel / f"{slug}.vtt").write_text(vtt)
longest = max(len(l) for _, _, t in cues for l in wrap(t).split("\n"))
print(f"{len(cues)} cues · total {offset:.3f}s · longest line {longest} chars")
