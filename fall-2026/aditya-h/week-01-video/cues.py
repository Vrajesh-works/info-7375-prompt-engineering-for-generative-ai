"""cues.py — beat-local reveal times for each shot.show event (padded clock).

No Whisper model download: each cue is estimated from its character position in
the known narration over the RAW mp3's speech span; cues that begin a sentence
snap to the nearest detected pause end within 1.2 s. Cues are then shifted by
every silent hold inserted before them (mp3/holds.json from pad_holds.py).
Writes mp3/cues.json = {"B01": {"duration": s, "cues": [t, ...], "holds": [...]}}.
"""
import json
import re
import subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parent


def pauses(mp3):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp3), "-af",
                          "silencedetect=noise=-40dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return ([float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)],
            [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)])


def main():
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    timings = json.loads((REEL / "mp3/timings.json").read_text())
    holds = json.loads((REEL / "mp3/holds.json").read_text())
    out = {}
    for beat in sheet["beats"]:
        bid, text = beat["beat_id"], beat["narration_text"]
        raw_dur = holds[bid]["raw_duration"]
        starts, ends = pauses(REEL / f"mp3/raw/beat-{bid}.mp3")
        speech0 = ends[0] if starts and starts[0] < 0.05 else 0.0
        speech1 = starts[-1] if starts and raw_dur - starts[-1] < 1.5 else raw_dur
        cues, cues_raw = [], []
        for ev in beat["shot"]["show"]:
            i = text.find(ev["at"])
            if i < 0:
                raise SystemExit(f"{bid}: cue phrase not in narration: {ev['at']!r}")
            t = speech0 if i == 0 else speech0 + (speech1 - speech0) * i / len(text)
            if i and text[:i].rstrip()[-1:] in ".?!:":
                prev_raw = cues_raw[-1] if cues_raw else -1.0
                near = [e for e in ends if -1.2 <= e - t <= 0.6 and e > prev_raw + 0.3]
                if near:
                    t = min(near, key=lambda e: abs(e - t))
            cues_raw.append(t)
            t += sum(s for at, s in holds[bid]["inserts"] if at <= t)
            cues.append(round(max(0.0, t - 0.15), 2))
        # hold windows on the padded clock, for scenes that want to land a beat
        shifted, acc = [], 0.0
        for at, s in holds[bid]["inserts"]:
            shifted.append([round(at + acc, 2), s]); acc += s
        out[bid] = {"duration": timings[bid], "cues": cues, "holds": shifted}
        print(bid, timings[bid], cues, "holds", shifted)
    (REEL / "mp3/cues.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
