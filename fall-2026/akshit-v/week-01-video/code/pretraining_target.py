#!/usr/bin/env python3
"""
pretraining_target.py — a reproducible demonstration of what the pretraining
objective actually optimizes.

WHAT THIS SHOWS
---------------
Chapter 1, Part 1 states the pretraining loop as:

    "Take a passage of text. Hide the next token. Ask the model for its
     distribution. Compare that distribution with the token that actually
     followed."
    "Nothing in this loop is told what is true. The target is what the corpus
     did next."

This script runs exactly that loop on one context, and reports what the
objective converges to. It uses gradient descent on cross-entropy — the real
pretraining objective — not a simulation of one.

THE CORPUS IS CONSTRUCTED, AND DELIBERATELY WRONG
-------------------------------------------------
The corpus below is invented for this demonstration (designed with Claude Code). It is not a sample
of real web text. It is built so that the factually FALSE continuation is the
more frequent one:

    "the capital of australia is sydney"    x7      <- false, but frequent
    "the capital of australia is canberra"  x3      <- TRUE, but rarer
    "the capital of australia is melbourne" x0      <- false, absent

Canberra is the capital of Australia. Sydney is the common misconception.
If the objective targeted truth, training would drive probability toward
"canberra". It does not. It drives probability toward the corpus frequencies.

No network access, no API key, no paid service. numpy only.
Deterministic: weights start at zero, so there is no seed and no run-to-run
variation. Re-running prints identical numbers.
"""
import json
from pathlib import Path

import numpy as np

# ── the constructed corpus ────────────────────────────────────────────────
CONTEXT = "the capital of australia is"
VOCAB = ["sydney", "canberra", "melbourne"]
COUNTS = {"sydney": 7, "canberra": 3, "melbourne": 0}
TRUTH = "canberra"          # externally true answer — never shown to the loop

# the training set: one (context, next_token) pair per corpus occurrence
targets = []
for tok, n in COUNTS.items():
    targets += [VOCAB.index(tok)] * n
targets = np.array(targets)
N = len(targets)


def softmax(z):
    z = z - z.max()                      # max-subtraction, per Chapter 1 Part 2
    e = np.exp(z)
    return e / e.sum()


def cross_entropy(p, idx):
    """Negative log probability the model assigned to the token that followed."""
    return -np.log(p[idx])


def train(steps=600, lr=0.5, report_at=(0, 1, 5, 20, 100, 600)):
    logits = np.zeros(len(VOCAB))        # deterministic start: uniform
    rows = []
    trajectory = []                      # EVERY step, for the video's curve + bars
    for step in range(steps + 1):
        p = softmax(logits)
        loss = float(np.mean([cross_entropy(p, t) for t in targets]))
        trajectory.append({"step": step, "p": [round(float(x), 6) for x in p],
                           "loss": round(loss, 6)})
        if step in report_at:
            rows.append((step, p.copy(), loss))
        if step == steps:
            break
        # gradient of mean cross-entropy w.r.t. logits: p - empirical_frequency
        empirical = np.bincount(targets, minlength=len(VOCAB)) / N
        grad = p - empirical
        logits -= lr * grad              # "nudge every parameter slightly"
    return rows, softmax(logits), trajectory


def main():
    print("=" * 66)
    print("WHAT PRETRAINING ACTUALLY TARGETS")
    print("the token that followed, not the truth")
    print("=" * 66)
    print(f'\ncontext: "{CONTEXT} ___"')
    print("\nCONSTRUCTED corpus (invented for this demo, not real web text):")
    for tok in VOCAB:
        flag = "  <- TRUE" if tok == TRUTH else ""
        print(f"   {tok:<10} followed {COUNTS[tok]} times{flag}")
    print(f"\n   corpus frequency: "
          f"{', '.join(f'{t}={COUNTS[t]/N:.2f}' for t in VOCAB)}")
    print(f"   external truth  : {TRUTH}")

    rows, final, trajectory = train()

    print("\n" + "-" * 66)
    print("training: hide the next token, compare, nudge. repeat.")
    print("-" * 66)
    print(f"{'step':>6} | {'P(sydney)':>10} {'P(canberra)':>12} "
          f"{'P(melbourne)':>13} | {'loss':>7}")
    for step, p, loss in rows:
        print(f"{step:>6} | {p[0]:>10.4f} {p[1]:>12.4f} {p[2]:>13.4f} "
              f"| {loss:>7.4f}")

    print("\n" + "-" * 66)
    print("where it converged")
    print("-" * 66)
    for i, tok in enumerate(VOCAB):
        print(f"   P({tok:<10}) = {final[i]:.4f}   "
              f"corpus frequency = {COUNTS[tok]/N:.4f}")

    gap_corpus = float(np.abs(final - np.array([COUNTS[t] / N for t in VOCAB])).max())
    truth_onehot = np.array([1.0 if t == TRUTH else 0.0 for t in VOCAB])
    gap_truth = float(np.abs(final - truth_onehot).max())

    print(f"\n   max gap from CORPUS FREQUENCY : {gap_corpus:.4f}")
    print(f"   max gap from TRUTH            : {gap_truth:.4f}")
    print(f"\n   argmax = {VOCAB[int(np.argmax(final))]}   "
          f"(truth = {TRUTH})")
    # The loss floor: a perfectly-fit model cannot reach zero loss here,
    # because the corpus itself is inconsistent about this context. The
    # minimum achievable mean cross-entropy IS the corpus's own entropy.
    freq = np.array([COUNTS[t] / N for t in VOCAB])
    nz = freq[freq > 0]
    entropy = float(-(nz * np.log(nz)).sum())
    final_loss = rows[-1][2]
    print("\n" + "-" * 66)
    print("the loss floor")
    print("-" * 66)
    print(f"   loss at step 600        = {final_loss:.4f}")
    print(f"   entropy of the corpus   = {entropy:.4f}")
    print("   the objective bottoms out AT the corpus's own entropy, not at 0.")
    print("   a perfect fit to a contradictory corpus is still a perfect fit.")

    out = Path(__file__).with_name("trajectory.json")
    json.dump({"vocab": VOCAB, "counts": COUNTS, "truth": TRUTH, "lr": 0.5,
               "entropy": round(entropy, 6), "steps": trajectory},
              open(out, "w"), indent=0)
    print(f"\n   full trajectory ({len(trajectory)} steps) -> code/{out.name}")
    print("\nThe loop minimized its loss by matching the corpus, and the corpus")
    print("was wrong. Truth never entered the objective.")


if __name__ == "__main__":
    main()
