"""pad_holds.py — insert silent holds after reveal lines (audio stays the clock).

The toolkit documents a per-beat lead_silence_s but no script implements it, so
holds are applied here, deterministically, from beat_sheet.json `metadata.holds`:
    {"B02": [{"after": "Identical.", "s": 1.8}], "B01": [{"tail": 1.8}], ...}

For each hold the end of the named sentence is estimated from its character
position, then the silence is inserted at the middle of the nearest detected
pause (ffmpeg silencedetect), so it never cuts a word. Originals are kept in
mp3/raw/; padded mp3s replace mp3/beat-<ID>.mp3; timings.json and each beat's
actual_duration_s are updated; mp3/holds.json records the raw insertion times
for cues.py. Run order: generate_audio_kokoro.py -> pad_holds.py -> cues.py.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parent


def probe(path, entry):
    return subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", entry,
                                    "-of", "csv=p=0", str(path)], text=True).strip().split(",")[0]


def pauses(mp3):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp3), "-af",
                          "silencedetect=noise=-40dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(s, e))


def main():
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    holds = sheet["metadata"]["holds"]
    raw_dir = REEL / "mp3/raw"
    raw_dir.mkdir(exist_ok=True)
    timings, record = {}, {}
    for beat in sheet["beats"]:
        bid, text = beat["beat_id"], beat["narration_text"]
        mp3, raw = REEL / f"mp3/beat-{bid}.mp3", raw_dir / f"beat-{bid}.mp3"
        if not raw.exists():
            shutil.copy2(mp3, raw)
        dur = float(probe(raw, "format=duration"))
        sr = probe(raw, "stream=sample_rate")
        gaps = pauses(raw)
        speech0 = gaps[0][1] if gaps and gaps[0][0] < 0.05 else 0.0
        speech1 = gaps[-1][0] if gaps and dur - gaps[-1][1] < 0.3 else dur
        inserts, tail = [], 0.0
        for h in holds.get(bid, []):
            if "tail" in h:
                tail += h["tail"]
                continue
            i = text.index(h["after"]) + len(h["after"])
            est = speech0 + (speech1 - speech0) * i / len(text)
            s, e = min(gaps, key=lambda g: abs(g[0] - est))
            if abs(s - est) > 2.0:
                raise SystemExit(f"{bid}: no pause near {h['after']!r} (est {est:.2f}s)")
            inserts.append((round((s + e) / 2, 3), h["s"]))
            print(f"{bid}: +{h['s']}s after {h['after']!r} at {inserts[-1][0]}s "
                  f"(pause {s:.2f}-{e:.2f}, est {est:.2f})")
        inserts.sort()
        # build segments: speech, silence, speech, ..., tail silence
        parts, filt, t0 = [], [], 0.0
        for k, (at, s) in enumerate(inserts):
            filt.append(f"[0:a]atrim={t0}:{at},asetpts=PTS-STARTPTS[p{k}]")
            filt.append(f"anullsrc=r={sr}:cl=mono,atrim=0:{s}[z{k}]")
            parts += [f"[p{k}]", f"[z{k}]"]
            t0 = at
        filt.append(f"[0:a]atrim=start={t0},asetpts=PTS-STARTPTS[pe]")
        parts.append("[pe]")
        if tail:
            filt.append(f"anullsrc=r={sr}:cl=mono,atrim=0:{tail}[zt]")
            parts.append("[zt]")
            print(f"{bid}: +{tail}s tail hold")
        filt.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1[out]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-filter_complex",
                        ";".join(filt), "-map", "[out]", "-ac", "1", "-c:a", "libmp3lame",
                        "-q:a", "2", str(mp3)], check=True)
        new = round(float(probe(mp3, "format=duration")), 2)
        timings[bid] = new
        beat["actual_duration_s"] = new
        record[bid] = {"raw_duration": round(dur, 2), "inserts": inserts, "tail": tail}
        print(f"{bid}: {dur:.2f}s -> {new}s")
    (REEL / "mp3/timings.json").write_text(json.dumps(timings, indent=2))
    (REEL / "mp3/holds.json").write_text(json.dumps(record, indent=1))
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False))
    print("total", round(sum(timings.values()), 2))


if __name__ == "__main__":
    main()
