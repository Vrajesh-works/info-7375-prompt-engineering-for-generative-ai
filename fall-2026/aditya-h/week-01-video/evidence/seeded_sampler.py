"""seeded_sampler.py — softmax weights + a seeded weighted-choice sampler.

Run verbatim for Beat 2 of the seed-repeatable-not-correct reel; the video
shows this script's captured stdout, never retyped numbers.

    python3 seeded_sampler.py
"""
import math
import random
from collections import Counter

SCORES = [1, 2, 3]
TEMPERATURE = 1.0
SEED = 7
COUNT = 1000


def softmax(scores, T):
    m = max(scores)
    w = [math.exp((s - m) / T) for s in scores]
    total = sum(w)
    return [x / total for x in w]


def sample(probs, seed, count):
    rng = random.Random(seed)
    picks = rng.choices(range(len(probs)), weights=probs, k=count)
    return dict(sorted(Counter(picks).items()))


if __name__ == "__main__":
    probs = softmax(SCORES, TEMPERATURE)
    print(f"scores={SCORES} temperature={TEMPERATURE} seed={SEED} count={COUNT}")
    print("probs =", [round(p, 3) for p in probs])
    print("counts =", sample(probs, SEED, COUNT))
