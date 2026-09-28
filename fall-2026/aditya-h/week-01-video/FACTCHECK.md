# FACTCHECK: seed-repeatable-not-correct

| # | Claim (beat) | Verdict | Source / check |
|---|---|---|---|
| 1 | Box sizes: box 2 ≈ 2 in 3, box 1 ≈ 1 in 4, box 0 ≈ 1 in 10 (B01) | TRUE (rounded) | softmax([1,2,3], T=1.0) = [0.0900, 0.2447, 0.6652] (factcheck_probe.txt). "About 1 in 10" rounds 0.090 up; "about 1 in 4" rounds 0.245. Box widths on screen use the exact values, imported from seeded_sampler.py. |
| 2 | A seed makes the draws repeatable (B01) | TRUE for this setup | Same seed, same Python version, same code → same sequence (run1 = run2; 100/100 identical). Different seeds give different counts (seed 8 → {0: 76, 1: 239, 2: 685}). Scope: Python's `random` is only guaranteed to be reproducible across runs of the same Python version, so the video claims nothing about other versions or machines. |
| 3 | The ball drops in B01 | ILLUSTRATION | Playful draw animation (2, 1, 2), not the recorded run. Nothing on screen claims these are recorded draws. |
| 4 | Seed 7, 1,000 draws → {0: 102, 1: 268, 2: 630}, twice (B02) | TRUE (recorded) | evidence/run1.txt, evidence/run2.txt: two separate processes, both exit 0. |
| 5 | "The two output files match byte for byte" (B02) | TRUE | `diff` in capture.sh: byte-identical. The on-screen line is computed at render time with `filecmp.cmp(shallow=False)`. |
| 6 | Outcome 0 is "the correct answer" (B03) | CONSTRUCTED | Stipulated by the author, not determined by the program. Styled as a hand-written sticky note and tagged "HYPOTHETICAL: stipulated by me, not by the program". |
| 7 | Box 0 picked 102 times; 898 misses (B03) | TRUE (recorded) | run1.txt counts; 1000 − 102 = 898. The dot grid replays the exact 1,000 draws (`random.Random(7).choices`, same call as the script), and the scene asserts they sum to the recorded counts. |
| 8 | "I reran it a hundred times: a hundred identical results" (B03) | TRUE (recorded) | evidence/run100.txt: `uniq -c` shows one distinct output ×100. |
| 9 | The sampler's only inputs are scores, temperature, seed, count; no answer key (B03) | TRUE | seeded_sampler.py: `softmax(SCORES, TEMPERATURE)`, `sample(probs, SEED, COUNT)`. No other input exists. The chips show the script's own constants. |
| 10 | Chat: "What's the capital of Australia?" → "Sydney." ×2 (B04) | CONSTRUCTED ILLUSTRATION | Mock chat, labelled on screen "Illustration: mock chat, not a real transcript". It is not a claim about any real AI system's output. |
| 11 | Actual capital of Australia: Canberra (B04) | TRUE | Canberra has been Australia's capital since 1913 (Sydney is the largest city). |
| 12 | Boundary statement (B05) | USER-SPECIFIED, verbatim | Read aloud and shown word for word. |

Environment for all recorded runs: evidence/ENV.txt (Python 3.13.3, Darwin 24.5.0 arm64; seeded_sampler.py sha256 5109526d…).

Display-only transformation (disclosed in B02's caption): the settings line `scores=[1, 2, 3] temperature=1.0 seed=7 count=1000` is wrapped before `seed=` to fit a half-width panel. No characters are changed.
