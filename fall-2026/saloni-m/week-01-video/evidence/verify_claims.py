"""
verify_claims.py — checks that every figure shown on screen in the Week 1
explainer video is true of the unmodified course code.

Concept: a seed makes a run repeatable; it does not make the answer true.

Run from the week-01-video folder:
    python3 evidence/verify_claims.py

Requires main.py to be at its shipped seed (7).
"""

import json
import subprocess
import sys
from pathlib import Path
import os


MAIN_PY = Path(os.environ.get(
    "INFO7375_MAIN",
    Path.home() / "info-7375-prompt-engineering-for-generative-ai"
    / "lessons/01-randomness-and-first-prompts/code/main.py"
))

SEED_ORIGINAL = 7
COUNT = 1000

# Figures shown on screen, transcribed from run-A.txt.
ON_SCREEN_PROBABILITIES = [
    0.09003057317038046,
    0.24472847105479764,
    0.6652409557748218,
]
ON_SCREEN_COUNTS = {"0": 102, "1": 268, "2": 630}
ON_SCREEN_EXPECTED_TOKEN2 = 665.24
ON_SCREEN_GAP_TOKEN2 = -35.24


def run_main():
    result = subprocess.run(
        [sys.executable, str(MAIN_PY)],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def check(label, passed, detail=""):
    print(f"[{'PASS' if passed else 'FAIL'}] {label}")
    if detail:
        print(f"       {detail}")
    return passed


def main():
    if not MAIN_PY.exists():
        sys.exit(f"main.py not found at {MAIN_PY}")

    results = []

    a, b = run_main(), run_main()

    # B02: the same seed reproduces output exactly.
    results.append(check(
        "B02 — same seed, two runs, byte-identical output",
        a == b,
        "identical" if a == b else "runs differed; something else is unseeded",
    ))

    data = json.loads(a)

    # B01-B03: the figures on screen are the figures the code prints.
    results.append(check(
        "B01-B03 — on-screen probabilities match a fresh run",
        data["probabilities"] == ON_SCREEN_PROBABILITIES,
    ))
    results.append(check(
        "B02-B04 — on-screen counts match a fresh run",
        data["counts"] == ON_SCREEN_COUNTS,
        f"counts: {data['counts']}",
    ))

    # B04: expected versus observed for token 2.
    expected = data["probabilities"][2] * COUNT
    observed = data["counts"]["2"]
    gap = observed - expected
    results.append(check(
        "B04 — expected count for token 2 is 665.24",
        round(expected, 2) == ON_SCREEN_EXPECTED_TOKEN2,
        f"{expected:.4f}",
    ))
    results.append(check(
        "B04 — observed falls short by 35.24, and by the same amount every run",
        round(gap, 2) == ON_SCREEN_GAP_TOKEN2,
        f"observed {observed}, expected {expected:.2f}, gap {gap:+.2f}",
    ))

    # B05: the three gaps are not independent — they sum to zero, because
    # the counts total 1000 and the probabilities total 1.
    gaps = [data["counts"][str(i)] - data["probabilities"][i] * COUNT
            for i in range(3)]
    results.append(check(
        "B05 — the three gaps sum to zero (a constraint, not a coincidence)",
        abs(sum(gaps)) < 1e-9,
        f"gaps: {[round(g, 2) for g in gaps]}, sum {sum(gaps):.2e}",
    ))

    # The captured file used for the screen recording is that same output.
    captured = Path("run-A.txt")
    if captured.exists():
        results.append(check(
            "run-A.txt is real output, not retyped",
            captured.read_text() == a,
        ))
    else:
        results.append(check("run-A.txt present", False, "capture it with tee"))

    print(f"\n{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
