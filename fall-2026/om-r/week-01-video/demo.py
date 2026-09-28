"""
demo.py — supporting script for the Week 1 explainer video.

Reproduces two things exactly as run for this video:
  1. The chapter's own reference implementation (probabilities, sample),
     copied verbatim from chapters/01-randomness-and-first-prompts.md.
  2. A small CONSTRUCTED contrast function, argmax_select, written for
     this video only. It is NOT part of the chapter or the lesson's
     reference implementation. It exists to show what genuine
     deterministic selection looks like, so the video can show the
     difference rather than assert it.

Run with:
    python3 demo.py
"""

import math
import random
import sys
from collections import Counter

# --- Reference implementation, copied verbatim from the chapter ---

def probabilities(logits, temperature=1.0):
    if not logits or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("Need logits and a positive finite temperature")
    if not all(math.isfinite(x) for x in logits):
        raise ValueError("Logits must be finite")
    peak = max(logits)
    weights = [math.exp((x - peak) / temperature) for x in logits]
    total = sum(weights)
    return [weight / total for weight in weights]


def sample(logits, count=1000, seed=7, temperature=1.0):
    if type(count) is not int or count < 0:
        raise ValueError("Count must be nonnegative")
    rng = random.Random(seed)
    return dict(Counter(rng.choices(
        range(len(logits)),
        probabilities(logits, temperature),
        k=count,
    )))


# --- Constructed illustration, built for this video only ---

def argmax_select(logits, count=1000):
    """
    NOT from the chapter. A genuine deterministic selector: always
    returns the index of the largest score, every single time.
    Used only as a contrast case against sample().
    """
    best = logits.index(max(logits))
    return dict(Counter([best] * count))


if __name__ == "__main__":
    print("Python version:", sys.version)
    print()

    print("--- Beat 2: temperature=0 is refused, not treated as a deterministic mode ---")
    try:
        probabilities([1, 2, 3], temperature=0)
    except ValueError as e:
        print("Raised ValueError:", e)
    print()

    print("--- Beat 3: sample() at temperature=0.5, seed=7, count=1000 (real, chapter-verified) ---")
    counts_05 = sample([1, 2, 3], count=1000, seed=7, temperature=0.5)
    print("Counts:", counts_05)
    probs_05 = probabilities([1, 2, 3], temperature=0.5)
    print("Assigned probabilities:", probs_05)
    print()

    print("--- Beat 4: constructed contrast, argmax_select([1,2,3], count=1000) ---")
    counts_argmax = argmax_select([1, 2, 3], count=1000)
    print("Counts:", counts_argmax)
