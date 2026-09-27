#!/usr/bin/env python3
"""fill_props.py — write every DATA prop and every CUE in beat_sheet.json from the evidence.

Nothing on screen that is a number, a token, or a model output is typed by hand: this script
reads evidence/runs/*.json (+ evidence/sample_review.json) and writes the props; cues come from
mp3/words.json (align.py) so each reveal lands on its spoken word.

Run with the evidence venv (the math rows need matplotlib, via the toolkit's typeset_math.py):
  ../.venv-evidence/bin/python fill_props.py
Order after any audio change: generate_audio_kokoro.py → pad_audio.py → align.py → fill_props.py
"""
import json, math, os, re, sys
from pathlib import Path

REEL = Path(__file__).resolve().parent
TOOLKIT = Path(os.environ.get("BRUTALIST_HOME", Path.home() / "Desktop/Brutalist/brutalist.art"))
sys.path.insert(0, str(TOOLKIT / "runtime" / "scripts"))
from typeset_math import typeset  # noqa: E402

ev = lambda name: json.loads((REEL / "evidence" / "runs" / f"{name}.json").read_text())
france, mm, nostop, force, paths, sample = (ev(n) for n in
                                            ("france", "middlemarch", "no_stop", "force_george", "paths", "sample"))
review = json.loads((REEL / "evidence" / "sample_review.json").read_text())
sheet_p = REEL / "beat_sheet.json"
sheet = json.loads(sheet_p.read_text())
words = json.loads((REEL / "mp3" / "words.json").read_text())
FPS = words["fps"]
norm = lambda w: re.sub(r"[^a-z0-9-]", "", w.lower())


def cue(bid, word, nth=1, offset=0.0):
    seen = 0
    for w in words["beats"][bid]:
        if norm(w["text"]) == norm(word):
            seen += 1
            if seen == nth:
                return round(w["startFrame"] / FPS + offset, 2)
    raise SystemExit(f"[fill] {bid}: word {word!r} (#{nth}) not in words.json")


cand = lambda top, n: [{"token": c["token"], "p": c["p"]} for c in top[:n]]
pct = lambda p: f"{p * 100:.0f}%" if p >= 0.1 else f"{p * 100:.1f}%"
STOP_TOKENS = {"<|im_end|>", "<|endoftext|>"}
name_idx = force["name_pass"] - 1
B = {b["beat_id"]: b for b in sheet["beats"]}
P = {bid: b["shot"]["remotion"]["props"] for bid, b in B.items()}

# B02 — the loop diagram's mini bars: pass-1 top 3
P["B02"].update(context="…What is the capital of France?", candidates=cand(france["steps"][0]["top"], 3),
                cueIn=cue("B02", "text"), cueProb=cue("B02", "probability"), cuePick=cue("B02", "pick"),
                cueAppend=cue("B02", "append"), cueAgain=cue("B02", "again"))

# B03 — the exact chat template, split into its lines
lines = []
for chunk in france["chat_template_text"].split("<|im_start|>")[1:]:
    role, _, body = chunk.partition("\n")
    lines.append({"special": "<|im_start|>", "text": role, "kind": "role", "end": ""})
    body = body.rstrip("\n")
    if body:
        text, _, _ = body.partition("<|im_end|>")
        lines.append({"special": "", "text": text, "kind": "question" if role == "user" else "body",
                      "end": "<|im_end|>"})
P["B03"].update(lines=lines, cueDoc=cue("B03", "document"), cueQuestion=cue("B03", "question"),
                cueBlank=cue("B03", "blank", offset=-0.3),
                caption=f"The exact text the model receives — {france['prompt_tokens']} tokens · "
                        f"SmolLM2-135M-Instruct chat template · evidence/runs/france.json")

# B04 / B06 — pass 1 and pass 8 of the France run
P["B04"].update(candidates=cand(france["steps"][0]["top"], 5), cueGrow=cue("B04", "eighty-three"),
                cueRing=cue("B04", "usually"),
                caption=f"Top 5 of {france['vocab_size']:,} possible tokens · pass 1 · evidence/runs/france.json")
P["B06"].update(candidates=cand(france["steps"][7]["top"], 5), cueGrow=cue("B06", "end-of-turn"),
                caption="Top 5 · pass 8 · <|im_end|> = end of turn · evidence/runs/france.json")

# B05 — the unrolled loop
P["B05"].update(steps=[{"token": s["chosen"], "p": s["p_chosen"]} for s in france["steps"]],
                startContext=france["steps"][0]["tokens_in"], cueFirst=cue("B05", "append"),
                cueLast=cue("B05", "paris"),
                caption="Greedy decoding (always the top token) · evidence/runs/france.json")

# B07 — no stop: text segments by pass, a struck chip wherever a stop token was the top pick
segs = []
for s in nostop["steps"]:
    if s["top"][0]["token"] in STOP_TOKENS:
        segs.append({"text": "", "pass": s["pass"], "kind": "stop", "p": s["top"][0]["p"]})
    segs.append({"text": s["chosen"], "pass": s["pass"], "kind": "text", "p": 0})
full = "".join(x["text"] for x in segs)
claim = "approximately 2.5 million people"
c0 = full.index(claim)
pos = 0
for x in segs:
    if x["kind"] == "text":
        if pos < c0 + len(claim) and pos + len(x["text"]) > c0:
            x["kind"] = "claim"
        pos += len(x["text"])
stop_passes = [x["pass"] for x in segs if x["kind"] == "stop"]
P["B07"].update(segments=segs, totalPasses=len(nostop["steps"]),
                keyframes=[{"at": cue("B07", "ban"), "pass": 0}, {"at": cue("B07", "stop"), "pass": stop_passes[0]},
                           {"at": cue("B07", "fifty-one", offset=-0.2), "pass": stop_passes[1]},
                           {"at": cue("B07", "writing"), "pass": len(nostop["steps"])}],
                cueStop1=cue("B07", "thirty-seven"), cueStop2=cue("B07", "fifty-one"),
                cueClaim=cue("B07", "approximately"), cueFact=cue("B07", "official"),
                caption="Greedy, with the end-of-turn token <|im_end|> banned · evidence/runs/no_stop.json")
assert len(stop_passes) == 2, stop_passes

# B08 — the fluent wrong answer
ans = mm["answer"]
prefix, _, rest = ans.partition(" Samuel")
P["B08"].update(prefix=prefix, wrong="Samuel" + rest, candidates=cand(mm["steps"][name_idx]["top"], 5),
                absentNote="“George” — not in the top 5.", barsHeading=f"At the name — pass {name_idx + 1}",
                cueAsk=cue("B08", "who"), cueName=cue("B08", "samuel"), cueWrong=cue("B08", "wrong"),
                cueTruth=cue("B08", "george"), cuePct=cue("B08", "sixteen"),
                caption=f"Name chosen at pass {name_idx + 1} of {mm['passes']} · evidence/runs/middlemarch.json")

# B09 — force " George"
queue = cand(mm["steps"][name_idx]["top"], 8)
fi = [c["token"] for c in queue].index(" George")
P["B09"].update(prefix=prefix, namePass=name_idx + 1, queue=queue, forcedIndex=fi,
                next=cand(force["steps"][name_idx + 1]["top"], 3), tail=".",
                cueQueue=cue("B09", "was"), cueRing=cue("B09", "eighth"), cueForce=cue("B09", "force"),
                cueNext=cue("B09", "eliot"),
                caption="Probabilities are the model's own, before forcing · evidence/runs/force_george.json")

# B10 — 200 samples
rev = {r["seed"]: r for r in review["runs"]}
marks = [2 if rev.get(r["seed"], {}).get("attributes_to_eliot") else 1 if r["names_george_eliot"] else 0
         for r in sample["runs"]]
answers = {r["seed"]: r["answer"] for r in sample["runs"]}
def verbatim(seed, snippet):
    assert snippet in answers[seed], (seed, snippet)
    return snippet
k, mention = marks.count(2), marks.count(1)
assert k == review["attributes_to_eliot"]
P["B10"].update(marks=marks, countLine=f"{k} of {sample['n']} name George Eliot as the author",
                mentionLine=f"Outlined: seed {[r['seed'] for r in sample['runs'] if marks[r['seed']] == 1][0]} "
                            f"mentions her but credits someone else.",
                receipts=[{"seed": 9, "quote": verbatim(9, "George Eliot, a Nobel Laureate in Literature"),
                           "refute": "First Nobel in Literature: 1901. Eliot died in 1880."},
                          {"seed": 186, "quote": verbatim(186, "Her novel won the Pulitzer Prize for Fiction in 1885"),
                           "refute": "First Pulitzers: 1917 — and the fiction prize is for American authors."}],
                moreLine=f"Also: seed 127 “{verbatim(127, 'first published in 1870')}” (it was 1871–72) · "
                         f"seed 149 “{verbatim(149, '(1811-1885)')}” (she lived 1819–1880)",
                cueFill=cue("B10", "asked"), cueFillEnd=cue("B10", "each"), cueCount=cue("B10", "four"),
                cueReceipts=cue("B10", "invented"),
                caption="Temperature 1.0, no top-k/top-p, 48 tokens max · evidence/runs/sample.json · "
                        "Eliot count: regex + manual review (evidence/sample_review.json)")

# B11 — the chain rule on the two Middlemarch answers
rf, ef = paths["richardson"]["factors"], paths["eliot"]["factors"]
f3 = lambda x: f"{x:.3f}"
ratio = paths["richardson"]["p"] / paths["eliot"]["p"]
rows = [
    (r"P(x_1,\ldots,x_T \mid c) \;=\; \prod_{t=1}^{T}\, p(x_t \mid c,\, x_{<t})", 0.0),
    (r"\mathrm{Richardson}\quad " + rf"{f3(rf[0])} \times {f3(rf[1])} \times \cdots \times {f3(rf[-1])} \;\approx\; "
     + f"{paths['richardson']['p']:.2g}", cue("B11", "samuel")),
    (r"\mathrm{Eliot}\quad " + rf"{f3(ef[0])} \times \cdots \times {f3(ef[name_idx])} \times {f3(ef[name_idx + 1])}"
     + rf" \times \cdots \times {f3(ef[-1])} \;\approx\; " + f"{paths['eliot']['p']:.2g}".replace("e-05", r"\times 10^{-5}").replace("e-04", r"\times 10^{-4}"),
     cue("B11", "george")),
]
math_rows = []
import base64, xml.etree.ElementTree as ET
for expr, at in rows:
    r = typeset(expr)
    r["at"] = at
    r["h"] = float(ET.fromstring(base64.b64decode(r["src"].split(",", 1)[1])).attrib["viewBox"].split()[3])
    math_rows.append(r)
P["B11"].update(rows=math_rows, note=f"Richardson ≈ {ratio:.0f} × Eliot. No factor is a fact-check.",
                caption=f"Each factor = the model's probability for the token appended at that pass · "
                        f"{paths['richardson']['passes']} passes each · evidence/runs/paths.json")

# B12 — the boundary
P["B12"].update(cards=[
    {"tag": "MEASURED", "title": "A 135-million-parameter open model (SmolLM2) on this Mac",
     "detail": "Greedy and sampled runs, recorded to evidence/runs/ — rerun with evidence/verify.py",
     "at": cue("B12", "measured")},
    {"tag": "NOT MEASURED", "accent": True, "title": "Claude. Its probabilities are not visible to us.",
     "quote": "end_turn: “Indicates Claude finished its response naturally.”",
     "source": "Anthropic docs, Stop reasons and fallback", "at": cue("B12", "claude")},
    {"tag": "NOT EXPLAINED", "title": "Why the probabilities are what they are",
     "detail": "That is pretraining and attention — separate Chapter 1 ideas.", "at": cue("B12", "why")},
], caption="platform.claude.com/docs/en/build-with-claude/handling-stop-reasons · accessed 2026-09-27")

# B13 — the real Claude response, read from its verbatim transcript (never typed here)
cr = json.loads((REEL / "evidence" / "claude-response" / "response.json").read_text())
if "B13" in words["beats"]:
    hl = 'The word I was least sure of is "Ann."'
    assert hl in cr["reply"], "highlight must be verbatim"
    P["B13"].update(prompt=cr["prompt"], reply=cr["reply"], highlight=hl,
                    meta=f"claude.ai · {cr['model_shown']} · {cr['date']} · transcribed verbatim from Aditya's screenshot",
                    annotation="That “least sure” is also text the loop produced — a sentence about confidence, "
                               "not a readout of Claude's probabilities.",
                    cueReply=cue("B13", "answer"), cueHighlight=cue("B13", "least"), cueNote=cue("B13", "report"),
                    caption="Screenshot: evidence/claude-response/claude-ai-2026-09-27.png · her name is recorded as "
                            "Mary Ann, Mary Anne or Marian (Wikipedia, “George Eliot”)")

# BVDT — verdict lines, every number from the evidence
g = next(c for c in mm["steps"][name_idx]["top"] if c["token"] == " George")
eliot_next = force["steps"][name_idx + 1]["top"][0]
P["BVDT"]["artifactLines"] = [
    f"Each pass predicts one next token: a probability for each of {france['vocab_size']:,} tokens.",
    f"The winner is appended and everything goes back in — until the end-of-turn token wins "
    f"(pass 8, {pct(france['steps'][7]['top'][0]['p'])}).",
    f"Ban that token and the loop kept going for all {len(nostop['steps'])} passes we allowed: “approximately 2.5 million people” for Paris "
    f"(INSEE 2022: 2,113,705).",
    f"The right author was in the distribution — “George”, #{fi + 1} at {pct(g['p'])}. "
    f"Forced in, “Eliot” followed at {pct(eliot_next['p'])}.",
    f"Sampled {sample['n']} times: {k} named George Eliot, each with an invented fact.",
    "All measured on SmolLM2-135M-Instruct — not Claude.",
]

# durations for the duration-driven scenes
for bid, b in B.items():
    pat = b["shot"]["remotion"]["pattern"]
    if (pat.startswith("Ntl") or pat == "BrutalistHesitantWriter") and b.get("actual_duration_s"):
        P[bid]["durationSeconds"] = b["actual_duration_s"]

sheet_p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
for bid in P:
    cues = {k: v for k, v in P[bid].items() if k.startswith("cue")}
    print(f"[fill] {bid:4} {B[bid]['shot']['remotion']['pattern']:24} {cues}")
print(f"[fill] ratio richardson/eliot = {ratio:.2f}; eliot count = {k}; stop passes = {stop_passes}")
