"""evidence.py — every number shown in the video comes from this script.

Runs the course's own probabilities() (code/main.py, copied unchanged from
nikbearbrown/info-7375-prompt-engineering-for-generative-ai at commit
149c8e7, sha256 df9940ca...) next to a direct, un-shifted softmax, and writes
evidence.json. The Manim scenes read evidence.json; nothing on screen is typed
in by hand.

    python code/evidence.py            # prints and writes code/evidence.json
"""
import hashlib
import importlib.util
import json
import math
import platform
import sys
import traceback
from datetime import date
from decimal import Decimal, getcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lesson_main", HERE / "main.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def direct(logits):
    """Softmax WITHOUT subtracting the max — the version main.py avoids."""
    weights = [math.exp(x) for x in logits]
    total = sum(weights)
    return {"weights": weights, "total": total, "probs": [w / total for w in weights]}


def shifted(logits):
    """The intermediates main.py computes (temperature 1)."""
    peak = max(logits)
    shifted_scores = [x - peak for x in logits]
    weights = [math.exp(s) for s in shifted_scores]
    return {"peak": peak, "shifted": shifted_scores, "weights": weights,
            "total": sum(weights), "probs": m.probabilities(logits)}


def attempt(fn, logits):
    try:
        return {"ok": True, **fn(logits)}
    except OverflowError as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


# Inputs. [1, 2, 3] is the chapter's constructed example; [1000, 1000] is the
# lesson's test_02 input; the other two are constructed for this video.
CASES = {
    "chapter": [1, 2, 3],
    "offset": [1001, 1002, 1003],
    "test_02": [1000, 1000],
    "boundary": [0, -1000],
}

out = {
    "run": {
        "date": date.today().isoformat(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "main_py_sha256": hashlib.sha256((HERE / "main.py").read_bytes()).hexdigest(),
    },
    "cases": {name: {"logits": z, "direct": attempt(direct, z), "shifted": shifted(z)}
              for name, z in CASES.items()},
}

# The cancelled factor for [1, 2, 3]: every direct weight times exp(-3).
out["factor_exp_minus_3"] = math.exp(-3)

# Mathematically equal, but are the floats bit-identical?
d, s = out["cases"]["chapter"]["direct"]["probs"], out["cases"]["chapter"]["shifted"]["probs"]
out["chapter_direct_minus_shifted"] = [a - b for a, b in zip(d, s)]

# The overflow edge for math.exp on this machine.
out["exp_709"] = math.exp(709)
try:
    math.exp(710)
    out["exp_710"] = "no error"
except OverflowError as exc:
    out["exp_710"] = f"{type(exc).__name__}: {exc}"
try:
    math.exp(1000)
except OverflowError:
    out["exp_1000_traceback_last_line"] = traceback.format_exc().strip().splitlines()[-1]

# The underflow edge, and the true size of the weight that became 0.0.
out["exp_minus_745"] = math.exp(-745)
out["exp_minus_746"] = math.exp(-746)
getcontext().prec = 30
true_small = Decimal(-1000).exp()
out["true_exp_minus_1000"] = f"{true_small:.4E}"

# The course's own main.py demo, as printed.
out["main_demo"] = m.demo()

# The lesson's own test file, run here (test_02 asserts [1000, 1000] -> [0.5, 0.5]).
import io
import unittest
buf = io.StringIO()
suite = unittest.defaultTestLoader.discover(str(HERE / "tests"))
result = unittest.TextTestRunner(stream=buf, verbosity=0).run(suite)
out["lesson_tests"] = {"ran": result.testsRun, "failures": len(result.failures),
                       "errors": len(result.errors), "ok": result.wasSuccessful()}

if __name__ == "__main__":
    text = json.dumps(out, indent=2)
    (HERE / "evidence.json").write_text(text + "\n", encoding="utf-8")
    print(text)
