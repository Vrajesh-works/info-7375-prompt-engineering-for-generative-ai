# Evidence for the Week 1 video: "Subtract the max — the weights change, the distribution doesn't."
# Imports the course's own probabilities() from lessons/01-randomness-and-first-prompts/code/main.py
# and compares it with a naive softmax that exponentiates the raw scores.
# Every number shown in the video comes from running this file (output saved beside it).
import importlib.util
import math
import sys
from pathlib import Path

LESSON = Path("lessons/01-randomness-and-first-prompts/code/main.py")
# Works both inside the course repo (fall-2026/omkar-s/week-01-video/evidence/)
# and in a working folder that has the course repo cloned as ./course beside it.
MAIN = next(p / LESSON if (p / LESSON).is_file() else p / "course" / LESSON
            for p in Path(__file__).resolve().parents
            if (p / LESSON).is_file() or (p / "course" / LESSON).is_file())
spec = importlib.util.spec_from_file_location("lesson_main", MAIN)
lesson = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lesson)


def naive(logits):
    """Softmax without the shift: exponentiate the raw scores."""
    weights = [math.exp(x) for x in logits]
    total = sum(weights)
    return weights, total, [w / total for w in weights]


def shifted(logits):
    """The lesson's route, with the intermediates exposed."""
    peak = max(logits)
    shifted_scores = [x - peak for x in logits]
    weights = [math.exp(s) for s in shifted_scores]
    total = sum(weights)
    return peak, shifted_scores, weights, total, [w / total for w in weights]


def show(label, logits):
    print(f"== {label}: scores {logits}")
    try:
        w, t, p = naive(logits)
        print(f"naive   weights {[round(x, 6) for x in w]}  sum {t:.6f}")
        print(f"naive   probs   {p}")
    except OverflowError as e:
        print(f"naive   math.exp({max(logits)}) -> OverflowError: {e}")
    m, s, w, t, p = shifted(logits)
    print(f"shifted max {m}  scores-max {s}")
    print(f"shifted weights {[round(x, 6) for x in w]}  sum {t:.6f}")
    print(f"shifted probs   {p}")
    print(f"lesson probabilities() {lesson.probabilities(logits)}")
    print()


print(f"Python {sys.version.split()[0]}")
print(f"largest float: {sys.float_info.max}")
print(f"log(largest float) = {math.log(sys.float_info.max):.4f}  (math.exp overflows above this)")
print()
show("A. the chapter example", [1, 2, 3])
show("B. same gaps, +1000 offset", [1001, 1002, 1003])
show("C. the lesson test case", [1000, 1000])
show("D. boundary: a huge gap", [0, -1000])

# Exact equality check between A and B (not just 'close').
a = lesson.probabilities([1, 2, 3])
b = lesson.probabilities([1001, 1002, 1003])
print("A == B exactly:", a == b)
# What D does NOT establish: the true probability of outcome 1 is e^-1000 > 0,
# but it is below the smallest representable float, so it becomes exactly 0.0.
d = lesson.probabilities([0, -1000])
print("D outcome 1 probability:", d[1], "| is exactly zero:", d[1] == 0.0)
print("smallest positive float:", 5e-324, "| e^-1000 is about 10^%.1f" % (-1000 / math.log(10)))
