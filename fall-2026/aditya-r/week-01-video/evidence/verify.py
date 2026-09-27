"""verify.py — one command to check every number in "A Chatbot Is a Loop."

  1. HASHES   evidence/runs/*.json match runs/manifest.json (nothing edited after recording)
  2. RERUN    run_experiments.py again into a temp folder and diff against the stored runs
              (probabilities within 1e-4; tokens and answers exact). Skip with --no-rerun.
  3. SCREEN   every data prop in ../beat_sheet.json equals what the evidence says
  4. VOICE    every number spoken in the narration equals the evidence (rounded as spoken)

Usage (from evidence/, with the evidence venv):  python verify.py [--no-rerun]
Exit 0 = all PASS. Sampling (run 3) reproduces on the same torch build and CPU; another
platform can differ in the sampled answers — that is reported as a RERUN difference, not hidden.
"""
import argparse, hashlib, json, math, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
results = []


def check(section, what, ok, detail=""):
    results.append((section, what, bool(ok), detail))


def load(p):
    return json.loads(Path(p).read_text())


def close(a, b, path="", tol=1e-4):
    """recursive compare; returns first difference path or None"""
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            return f"{path}: keys differ"
        for k in a:
            d = close(a[k], b[k], f"{path}.{k}", tol)
            if d:
                return d
        return None
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return f"{path}: length {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = close(x, y, f"{path}[{i}]", tol)
            if d:
                return d
        return None
    if isinstance(a, float) or isinstance(b, float):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return None if abs(a - b) <= tol * max(1.0, abs(a)) else f"{path}: {a} vs {b}"
    return None if a == b else f"{path}: {a!r} vs {b!r}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-rerun", action="store_true")
    a = ap.parse_args()

    # 1. hashes
    man = load(RUNS / "manifest.json")
    for name, digest in man["files"].items():
        check("HASHES", name, hashlib.sha256((RUNS / name).read_bytes()).hexdigest() == digest)

    # 2. rerun
    if not a.no_rerun:
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, str(HERE / "run_experiments.py"), "--out", tmp],
                               capture_output=True, text=True)
            check("RERUN", "run_experiments.py exits 0", r.returncode == 0, r.stderr[-300:])
            if r.returncode == 0:
                for name in man["files"]:
                    diff = close(load(RUNS / name), load(Path(tmp) / name))
                    check("RERUN", name, diff is None, diff or "")

    fr, mm, ns, fg, pa, sa = (load(RUNS / f"{n}.json") for n in
                              ("france", "middlemarch", "no_stop", "force_george", "paths", "sample"))
    rv = load(HERE / "sample_review.json")
    sheet = load(HERE.parent / "beat_sheet.json")
    B = {b["beat_id"]: b for b in sheet["beats"]}
    P = {k: b["shot"]["remotion"]["props"] for k, b in B.items()}
    top = lambda s, n: [{"token": c["token"], "p": c["p"]} for c in s["top"][:n]]
    ni = fg["name_pass"] - 1

    # 3. screen
    check("SCREEN", "B02 loop bars = pass-1 top 3", P["B02"]["candidates"] == top(fr["steps"][0], 3))
    check("SCREEN", "B03 template lines = recorded template text",
          all(l["text"] in fr["chat_template_text"] for l in P["B03"]["lines"]))
    check("SCREEN", "B04 bars = pass-1 top 5", P["B04"]["candidates"] == top(fr["steps"][0], 5))
    check("SCREEN", "B05 rows = the 8 appended tokens + p",
          P["B05"]["steps"] == [{"token": s["chosen"], "p": s["p_chosen"]} for s in fr["steps"]])
    check("SCREEN", "B06 bars = pass-8 top 5", P["B06"]["candidates"] == top(fr["steps"][7], 5))
    seg_text = "".join(x["text"] for x in P["B07"]["segments"])
    check("SCREEN", "B07 streamed text = recorded no-stop continuation", seg_text == ns["continuation"])
    stops = [(x["pass"], x["p"]) for x in P["B07"]["segments"] if x["kind"] == "stop"]
    rec_stops = [(s["pass"], s["top"][0]["p"]) for s in ns["steps"] if s["top"][0]["token"] == "<|im_end|>"]
    check("SCREEN", "B07 struck stop chips = passes where <|im_end|> was the top pick", stops == rec_stops, str(rec_stops))
    check("SCREEN", "B08 bars = name-pass top 5", P["B08"]["candidates"] == top(mm["steps"][ni], 5))
    check("SCREEN", "B08 sentence = recorded answer", P["B08"]["prefix"] + " " + P["B08"]["wrong"] == mm["answer"])
    check("SCREEN", "B09 queue = name-pass top 8", P["B09"]["queue"] == top(mm["steps"][ni], 8))
    check("SCREEN", "B09 forced card is ' George'", P["B09"]["queue"][P["B09"]["forcedIndex"]]["token"] == " George")
    check("SCREEN", "B09 next-pass chips = recorded top 3 after forcing", P["B09"]["next"] == top(fg["steps"][ni + 1], 3))
    check("SCREEN", "B09 forced answer = recorded",
          P["B09"]["prefix"] + P["B09"]["queue"][P["B09"]["forcedIndex"]]["token"] + P["B09"]["next"][0]["token"]
          + P["B09"]["tail"] == fg["answer"])
    marks = P["B10"]["marks"]
    check("SCREEN", "B10 dots = 200 runs", len(marks) == sa["n"] == 200)
    check("SCREEN", "B10 lit dots = manual review count", marks.count(2) == rv["attributes_to_eliot"] == 4)
    check("SCREEN", "B10 lit + outlined = regex count", marks.count(2) + marks.count(1) == sa["george_eliot_runs"])
    ans = {r["seed"]: r["answer"] for r in sa["runs"]}
    check("SCREEN", "B10 receipt quotes are verbatim",
          all(r["quote"] in ans[r["seed"]] for r in P["B10"]["receipts"]))
    ratio = pa["richardson"]["p"] / pa["eliot"]["p"]
    check("SCREEN", "B11 ratio in note", f"≈ {ratio:.0f} ×" in P["B11"]["note"], f"{ratio:.3f}")
    check("SCREEN", "B11 path products = product of recorded factors",
          all(abs(math.prod(pa[k]["factors"]) - pa[k]["p"]) < 1e-9 for k in ("richardson", "eliot", "paris")))

    cr = load(HERE / "claude-response" / "response.json")
    check("HASHES", "claude-response screenshot", hashlib.sha256(
        (HERE / "claude-response" / cr["screenshot"]).read_bytes()).hexdigest() == cr["screenshot_sha256"])
    check("SCREEN", "B13 prompt + reply = verbatim transcript",
          P["B13"]["prompt"] == cr["prompt"] and P["B13"]["reply"] == cr["reply"] and P["B13"]["highlight"] in cr["reply"])
    check("SCREEN", "B13 date on screen = transcript date", cr["date"] in P["B13"]["meta"] and cr["date"] in B["B13"]["shot"]["remotion"]["props"]["badge"])

    # 4. voice — numbers as spoken
    narr = {k: b["narration_text"] for k, b in B.items()}
    r0 = lambda p: round(p * 100)
    spoken = [
        ("B02", "forty-nine thousand", fr["vocab_size"] // 1000 == 49),
        ("B04", "eighty-three percent", r0(fr["steps"][0]["top"][0]["p"]) == 83),
        ("B04", "'Paris' gets four", r0(fr["steps"][0]["top"][1]["p"]) == 4 and fr["steps"][0]["top"][1]["token"] == "Paris"),
        ("B05", "Eight passes", fr["passes"] == 8),
        ("B06", "thirty-seven percent", r0(fr["steps"][7]["top"][0]["p"]) == 37),
        ("B07", "thirty-seven percent here", rec_stops[0][1] and r0(rec_stops[0][1]) == 37),
        ("B07", "fifty-one percent later", r0(rec_stops[1][1]) == 51),
        ("B07", "approximately two point five million", "approximately 2.5 million" in ns["continuation"]),
        ("B08", "Samuel Richardson", "Samuel Richardson" in mm["answer"]),
        ("B08", "sixteen percent", r0(mm["steps"][ni]["top"][0]["p"]) == 16),
        ("B09", "eighth in line", [c["token"] for c in mm["steps"][ni]["top"]].index(" George") + 1 == 8),
        ("B09", "at three percent", r0(next(c["p"] for c in mm["steps"][ni]["top"] if c["token"] == " George")) == 3),
        ("B09", "'Eliot' on top, at forty-three percent",
         fg["steps"][ni + 1]["top"][0]["token"] == " Eliot" and r0(fg["steps"][ni + 1]["top"][0]["p"]) == 43),
        ("B10", "two hundred times", sa["n"] == 200),
        ("B10", "Four named George Eliot", rv["attributes_to_eliot"] == 4),
        ("B11", "about eleven times", round(ratio) == 11),
    ]
    for bid, phrase, ok in spoken:
        squash = lambda x: " ".join(x.lower().replace("'", "").replace("’", "").replace("—", " ").split())
        in_script = squash(phrase) in squash(narr[bid])
        check("VOICE", f"{bid}: “{phrase}”", ok and in_script, "" if in_script else "phrase not found in narration")

    width = max(len(w) for _, w, _, _ in results)
    fails = 0
    for sec, what, ok, detail in results:
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {sec:6}  {what:<{width}}  {'' if ok else detail}")
    print(f"\n{len(results) - fails}/{len(results)} checks passed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
