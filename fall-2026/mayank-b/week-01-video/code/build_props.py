"""Fills computed props into beat_sheet.json after audio lock:
  * durationSeconds  = measured mp3 duration (the master clock)
  * cues (seconds)   = word start times from mp3/words.json (align.py) for each
                       show-block anchor phrase, so reveals land on the word
  * typeset math     = matplotlib mathtext SVGs (runtime/scripts/typeset_math.py)
  * data             = chapter functions in code/main.py (never hand-typed)
Usage: python3 code/build_props.py   (from the reel folder, toolkit venv active)"""
import json, re, sys, random, math
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
TOOLKIT = Path.home() / "Desktop/AgenticAI/brutalist.art"
sys.path.insert(0, str(TOOLKIT / "runtime/scripts")); sys.path.insert(0, str(REEL / "code"))
from typeset_math import typeset
from main import probabilities, sample

PUB = TOOLKIT / "runtime/remotion/public/temperature-concentration"
PUB.mkdir(parents=True, exist_ok=True)
sheet = json.loads((REEL / "beat_sheet.json").read_text())
words = json.loads((REEL / "mp3/words.json").read_text())
FPS = words.get("fps", 24)
B = {b["beat_id"]: b for b in sheet["beats"]}
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("’", "'"))

def cue(bid, phrase):
    """Start time (s) of `phrase` in the beat's aligned words (+ lead silence)."""
    ws = [norm(w["text"]) for w in words["beats"][bid]]
    target = [norm(x) for x in phrase.split()]
    for i in range(len(ws) - len(target) + 1):
        if ws[i:i + len(target)] == target:
            return round(words["beats"][bid][i]["startFrame"] / FPS, 2)
    raise SystemExit(f"{bid}: anchor {phrase!r} not found in aligned words")

def svg(name, expr, color="#3D3929"):
    row = typeset(expr, color=color)
    import base64
    (PUB / f"{name}.svg").write_bytes(base64.b64decode(row["src"].split(",", 1)[1]))
    return {"src": f"temperature-concentration/{name}.svg", "aspect": round(row["aspect"], 4), "expression": expr}

S = [1, 2, 3]
P = {T: probabilities(S, T) for T in (0.5, 1.0, 2.0)}
def props(bid): return B[bid]["shot"]["remotion"]["props"]
for b in sheet["beats"]:
    props(b["beat_id"])["durationSeconds"] = b["actual_duration_s"]

p = props("B01A")
p.update(cues={"sentence": cue("B01A", "writes"), "scores": cue("B01A", "scores every"),
               "chance": cue("B01A", "Scores aren't"), "softmax": cue("B01A", "softmax"),
               "draw": cue("B01A", "Then the model draws")})

p = props("B02")
p.update(scores=S, formula=svg("softmax", r"p_i = \frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}"),
         expRow=[{"x": x, "value": round(math.exp(x), 2), "label": svg(f"ex_{x}", rf"e^{{{x}}}")} for x in (-1, 0, 1, 2, 3)],
         cues={"chips": cue("B02", "three sample values"), "formula": cue("B02", "Softmax is the formula"),
               "labels": cue("B02", "divided by the total"), "e": cue("B02", "Here, e"),
               "positive": cue("B02", "positive number"), "base": cue("B02", "Any base")})

p = props("B02B")
W1 = [math.exp(z) for z in S]
assert all(abs(w / sum(W1) - q) < 1e-12 for w, q in zip(W1, P[1.0]))
p.update(scores=S, probsT1=P[1.0], weights=[round(w, 4) for w in W1], total=round(sum(W1), 4),
         formula=svg("softmax", r"p_i = \frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}"),
         weightHead=svg("ez", r"e^{z}"),
         cues={"table": cue("B02B", "Now the example"), "move1": cue("B02B", "One: raise e"),
               "move2": cue("B02B", "Two: add them up"), "move3": cue("B02B", "Three: divide"),
               "labels": cue("B02B", "Nine")})

p = props("B03")
p.update(scores=S, probsT1=P[1.0], weightHead=svg("ezT", r"e^{z/T}"),
         cues={"divide": cue("B03", "divide every score"), "down": cue("B03", "At T point five"),
               "up": cue("B03", "At T two"), "zoom": cue("B03", "zooms"), "rank": cue("B03", "ranking")})

rows = []
for T in (0.5, 1.0, 2.0):
    r = P[T][2] / P[T][0]
    assert abs(r - math.exp(2 / T)) < 1e-9
    Tt = f"{T:g}"
    rows.append({"T": T, "ratio": round(r, 4),
                 "math": svg(f"ratio_T{Tt}", rf"\frac{{p_2}}{{p_0}} = e^{{2/{Tt}}} = e^{{{2/T:g}}} \approx {r:.2f}")})
p = props("B04")
p.update(ratioFormula=svg("ratio", r"\frac{p_i}{p_k} = \exp\left(\frac{z_i - z_k}{T}\right)"),
         gapFormula=svg("gap", r"z_2 - z_0 = 3 - 1 = 2"), rows=rows,
         cues={"ratio": cue("B04", "Divide"), "gap": cue("B04", "two points apart"),
               "row0": cue("B04", "At T point five"), "rest": cue("B04", "At T two")})

p = props("B05")
p.update(cues={"divide": cue("B05", "divides"), "inputs": cue("B05", "No question"), "guard": cue("B05", "zero is rejected")})

panels = []
for T in (0.5, 2.0):
    rng = random.Random(7)
    seq = rng.choices(range(3), probabilities(S, T), k=1000)
    counts = [seq.count(i) for i in range(3)]
    c = sample(S, count=1000, seed=7, temperature=T)
    assert counts == [c.get(i, 0) for i in range(3)], "draw sequence must match sample()"
    panels.append({"T": T, "draws": "".join(map(str, seq)), "counts": counts, "p2": round(P[T][2], 4)})
p = props("B06")
p.update(panels=panels, caption=f"random.Random(7).choices(…, k=1000) · Python {sys.version.split()[0]} · counts match Chapter 1's recorded run",
         cues={"fill": cue("B06", "draw a thousand"), "left": cue("B06", "eight hundred"),
               "right": cue("B06", "four hundred"), "sort": cue("B06", "Same scores")})

p = props("B07")
p.update(scores=S, correct=0, formula=svg("softmax", r"p_i = \frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}"), cues={"key": cue("B07", "answer key"), "lower": cue("B07", "Lower the temperature"),
                                    "never": cue("B07", "It never saw")})

p = props("B08")
p.update(items=[
    {"text": "How any Claude product sets or exposes temperature", "shown": False, "at": cue("B08", "how any Claude"), "accent": True},
    {"text": "How softmax reshapes three constructed scores", "shown": True, "at": cue("B08", "three-outcome toy")},
    {"text": "The ranking holds for every T > 0", "shown": True, "at": cue("B08", "three-outcome toy") + 0.6},
    {"text": "Seed-7 counts, run offline", "shown": True, "at": cue("B08", "run offline")},
    {"text": "Whether the scores themselves were any good", "shown": False, "at": cue("B08", "scores themselves"), "accent": True},
])
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False))
print("props built;", {k: props(k).get("cues") for k in ("B02", "B03", "B04", "B06", "B07")})
