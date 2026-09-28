"""Evidence for the Week 1 explainer video: what max-subtraction changes.

Concept (Chapter 1, Part 2): the reference implementation subtracts the maximum
score before exponentiating. This script records what that subtraction changes
(the intermediate weights) and what it does not change (the returned
distribution), plus one boundary the subtraction does NOT fix.

It imports the course reference implementation without modifying it, and prints
every number the video shows. Run it from the course repository root:

    python3 <path-to-this-file>

Nothing here calls Claude or any network service.
"""

import json
import math
import platform
import sys
from decimal import Decimal, getcontext
from pathlib import Path

# Import the reference implementation in place; do not copy or edit it.
# Walk up from this file until the course repository's lesson folder appears.
LESSON = Path("lessons/01-randomness-and-first-prompts/code/main.py")
REFERENCE = None
for parent in Path(__file__).resolve().parents:
    if (parent / LESSON).is_file():
        REFERENCE = parent / LESSON.parent
        break
if REFERENCE is None:
    sys.exit(
        f"Could not find {LESSON} above {Path(__file__).resolve()}.\n"
        "Run this script from inside the course repository checkout."
    )
sys.path.insert(0, str(REFERENCE))
from main import probabilities  # noqa: E402  (path must be set first)


def direct_probabilities(logits, temperature=1.0):
    """The same formula WITHOUT subtracting the maximum.

    Mathematically identical to `probabilities`; numerically it is the version
    that has to evaluate exp(z_i / T) on the original scores.
    """
    weights = [math.exp(x / temperature) for x in logits]
    total = sum(weights)
    return [w / total for w in weights]


def shifted_intermediates(logits, temperature=1.0):
    """The intermediate quantities the video puts on screen."""
    peak = max(logits)
    shifted = [x - peak for x in logits]
    weights = [math.exp(s / temperature) for s in shifted]
    total = sum(weights)
    return {
        "scores": logits,
        "peak": peak,
        "shifted": shifted,
        "weights": weights,
        "total": total,
        "probabilities": [w / total for w in weights],
    }


def high_precision_exp(x, precision=12):
    """exp(x) computed with `decimal`, which has no 64-bit float range limit.

    Used only to show what value the float arithmetic replaced with 0.0.
    """
    getcontext().prec = precision
    return Decimal(x).exp()


def attempt(fn, *args, **kwargs):
    """Run fn and record either its value or the exception it raised."""
    try:
        return {"ok": True, "value": fn(*args, **kwargs)}
    except Exception as exc:  # noqa: BLE001 - recording the failure is the point
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


def main():
    record = {
        "environment": {
            "python": sys.version.split()[0],
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "cases": {},
    }

    # Case A — the subtraction changes intermediates, not the distribution.
    record["cases"]["A_moderate_scores"] = {
        "input": [1, 2, 3],
        "temperature": 1.0,
        "intermediates": shifted_intermediates([1, 2, 3]),
        "reference_shifted": probabilities([1, 2, 3]),
        "direct_unshifted": attempt(direct_probabilities, [1, 2, 3]),
    }
    a = record["cases"]["A_moderate_scores"]
    a["max_abs_difference"] = max(
        abs(x - y)
        for x, y in zip(a["reference_shifted"], a["direct_unshifted"]["value"])
    )

    # Case B — equal large scores. The direct route cannot be evaluated at all.
    record["cases"]["B_equal_large_scores"] = {
        "input": [1000, 1000],
        "temperature": 1.0,
        "intermediates": shifted_intermediates([1000, 1000]),
        "reference_shifted": probabilities([1000, 1000]),
        "direct_unshifted": attempt(direct_probabilities, [1000, 1000]),
    }

    # Case C — the boundary the subtraction does NOT fix.
    # After shifting, the small outcome's weight underflows to exactly 0.0, so
    # the reported probability is 0.0 for an outcome whose probability is not 0.
    record["cases"]["C_underflow_boundary"] = {
        "input": [0, -1000],
        "temperature": 1.0,
        "intermediates": shifted_intermediates([0, -1000]),
        "reference_shifted": probabilities([0, -1000]),
        "float_exp_minus_1000": math.exp(-1000),
        "decimal_exp_minus_1000": str(high_precision_exp(-1000)),
        "note": (
            "Subtracting the maximum removes the overflow in case B. It does "
            "not remove underflow here: the second probability is reported as "
            "exactly 0.0, which is a floating-point result, not the value of "
            "the mathematical expression."
        ),
    }

    print(json.dumps(record, indent=2))
    out = Path(__file__).with_name("evidence_output.json")
    out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"\nWritten to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
