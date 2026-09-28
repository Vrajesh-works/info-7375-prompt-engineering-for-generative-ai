"""analyze_responses.py — Weiting W, INFO 7375 Week 01 video.

Concept (Chapter 1, Part 2): constraining the output format narrows the spread
without checking anything.

Reads evidence/<run>/responses.json (real Claude replies, typed from the
screenshots next to them) for both runs and turns "these look alike" into
numbers. Standard library only.

  distinct   how many different reply strings (exact match)
  words      word count per reply
  overlap    mean pairwise Jaccard overlap of word sets (1.0 = same words)
  years      four-digit years the replies assert (claims nothing here checked)

It also recomputes one number the deck replies quote: log2(52!).
Usage:  python3 analyze_responses.py   -> prints JSON, writes evidence/analysis.json
"""
import itertools
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = ["run1-normal", "run2-incognito"]


def words(text):
    return re.findall(r"[a-z0-9!^']+", text.lower())


def jaccard(a, b):
    sa, sb = set(words(a)), set(words(b))
    return len(sa & sb) / len(sa | sb)


def summarize(replies):
    wc = [len(words(x)) for x in replies]
    pairs = list(itertools.combinations(replies, 2))
    return {
        "n": len(replies),
        "distinct": len(set(replies)),
        "words_each": wc,
        "mean_words": round(sum(wc) / len(wc), 1),
        "mean_pairwise_overlap": round(sum(jaccard(a, b) for a, b in pairs) / len(pairs), 3),
        "years_asserted": sorted({y for x in replies for y in re.findall(r"\b(1[89]\d\d)\b", x)}),
        "deck_size_phrases": sorted({m for x in replies for m in
                                     re.findall(r"(about \d+ bits|about 2\^\d+|52!)", x)}),
    }


result = {"runs": {}}
for run in RUNS:
    data = json.loads((HERE / "evidence" / run / "responses.json").read_text())
    result["runs"][run] = {
        "model_label_shown": data["model_label_shown"],
        "incognito": data["incognito"],
        "groups": {name: summarize(g["responses"]) for name, g in data["groups"].items()},
    }

result["check_deck_bits"] = {
    "log2_of_52_factorial": round(math.lgamma(53) / math.log(2), 2),
    "note": "Replies say 'about 225 bits', 'about 2^225', 'about 2^226'. All within one bit of the computed 225.58; no prompt rule checked any of them.",
}

if __name__ == "__main__":
    out = json.dumps(result, indent=2)
    print(out)
    (HERE / "evidence" / "analysis.json").write_text(out + "\n")
