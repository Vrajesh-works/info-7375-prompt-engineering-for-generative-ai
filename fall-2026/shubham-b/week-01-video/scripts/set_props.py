"""Write per-beat Remotion props from measured audio + evidence.

- durationSeconds  = the beat's measured narration (audio is the clock)
- cues             = seconds at which a named phrase is SPOKEN, from
                     faster-whisper word timestamps on the beat's own mp3,
                     so reveals land on the word (SHOW-DON'T-TELL LAW)
Also copies evidence/preference_toy_output.json + the verbatim nudge() and
rater_pick() source into the toolkit's Remotion data folder, so every number
and code line on screen is read from the evidence, never retyped.

Run inside the brutalist.art venv:
  python3 scripts/set_props.py /path/to/brutalist.art
"""
import inspect, importlib.util, json, re, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
TOOLKIT = Path(sys.argv[1]).resolve()
DATA_OUT = TOOLKIT / "runtime/remotion/src/data/prefTuneToy.json"

# beat -> {cue name: first word of the phrase that triggers it}
# ("a|b" = accept either spelling; whisper writes spoken numbers as digits)
CUES = {
    "INTRO": {"today": "today", "topic": "preference", "why": "why"},
    "B00": {"unsure": "unsure", "confident": "confident", "prefer": "preferring"},
    "B02": {"stage1": "pre|pretraining", "stage2": "preference", "key": "answer", "approval": "approval"},
    "B03": {"prob": "probabilities", "raise": "raises", "inputs": "inputs", "strike": "correct"},
    "B04": {"three": "three|3", "seven": "seven|7", "assume": "assumption"},
    "B05": {"start": "fifty|50", "tally": "canberra|336", "final": "last", "nothing": "nothing"},
    "B06": {"p20": "twenty|20", "p40": "forty|40", "p60": "sixty|60", "p80": "eighty|80", "every": "every", "share": "share"},
    "B07": {"can": "can", "often": "often", "claude": "claude", "pipeline": "reward"},
    "B08": {"quote": "found", "neg": "preliminary"},
    "B09": {"l1": "follows", "l2": "usually", "l3": "when"},
}


def norm(w):
    return re.sub(r"[^a-z0-9-]", "", w.lower())


def main():
    from faster_whisper import WhisperModel
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    sheet_path = REEL / "beat_sheet.json"
    sheet = json.loads(sheet_path.read_text())
    for b in sheet["beats"]:
        props = b["shot"]["remotion"].setdefault("props", {})
        props["durationSeconds"] = round(b["actual_duration_s"] + b.get("lead_silence_s", 0), 2)
        if b["beat_id"] not in CUES:
            continue
        segs, _ = model.transcribe(str(REEL / b["audio_file"]), word_timestamps=True)
        words = [(norm(w.word), w.start) for s in segs for w in s.words]
        cues = {}
        # search after the previous cue, so repeated words resolve in order
        last = 0.0
        for name, target in CUES[b["beat_id"]].items():
            alts = [a.replace("-", "") for a in target.split("|")]
            hits = [st for w, st in words if st >= last and any(
                w.replace("-", "").startswith(a[:6]) for a in alts)]
            if not hits:  # whisper may write numbers as digits; fall back to fraction
                raise SystemExit(f"{b['beat_id']}: cue word {target!r} not heard; words={words}")
            cues[name] = round(float(hits[0]), 2)
            last = hits[0]
        props["cues"] = cues
        print(b["beat_id"], cues)
    sheet_path.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")

    spec = importlib.util.spec_from_file_location("toy", REEL / "evidence/preference_toy.py")
    toy = importlib.util.module_from_spec(spec); spec.loader.exec_module(toy)
    data = json.loads((REEL / "evidence/preference_toy_output.json").read_text())
    data["nudge_source"] = inspect.getsource(toy.nudge)
    course_out = json.loads((REEL / "evidence/course_main_output.txt").read_text())
    data["course_main_probabilities"] = course_out["probabilities"]
    spread = json.loads((REEL / "evidence/seed_spread_output.json").read_text())
    row = [r for r in spread["by_share"] if r["share_who_can_check"] == 0.3][0]
    data["seed_spread_03_wrong_favoured"] = row["share_of_seeds_wrong_reply_favoured"]
    data["rater_pick_source"] = inspect.getsource(toy.rater_pick)
    DATA_OUT.write_text(json.dumps(data, indent=2) + "\n")
    print("wrote", DATA_OUT)


if __name__ == "__main__":
    main()
