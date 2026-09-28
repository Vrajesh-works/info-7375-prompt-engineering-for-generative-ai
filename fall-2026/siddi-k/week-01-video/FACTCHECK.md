# FACTCHECK — every claim in the narration

Evidence = `code/evidence.json`, written by `code/evidence.py` (runs the course's unchanged `main.py`;
Python 3.13.2, Windows 11). Re-run with `python code/evidence.py`.

| Beat | Claim (as narrated) | Verdict | Evidence |
|---|---|---|---|
| B00 | "One line in the Chapter 1 code subtracts the largest score before it calls exp." | TRUE | `main.py`: `peak = max(logits)`; `math.exp((x - peak) / temperature)` |
| B00 | "every number you'll see was printed by Python, running the course's own code" | TRUE | All scene numbers are read from `evidence.json`; the direct route is a separate 3-line function in `evidence.py`, labelled "direct" |
| B01 | "changes the weights, not the answer" | TRUE in exact arithmetic; in floats the answer agrees to ~1e-16 (stated in B06) | `cases.chapter`; `chapter_direct_minus_shifted` |
| B01 | "keeps exp from overflowing" | TRUE for large positive scores, as tested | `cases.test_02`, `cases.offset` |
| B02 | Direct weights 2.7, 7.4, 20.1 | TRUE (2.718, 7.389, 20.086; total 30.193) | `cases.chapter.direct` |
| B02 | Shifted scores −2, −1, 0 → .14, .37, 1 | TRUE (0.1353, 0.3679, 1.0; total 1.5032) | `cases.chapter.shifted` |
| B02 | "Both columns land on the same three probabilities" | TRUE to 4 dp on screen (0.0900, 0.2447, 0.6652); last-digit differences disclosed in B06 | `probs` in both routes |
| B03 | Subtracting 3 multiplies every weight by e^−3 ≈ 0.05 | TRUE (0.049787) | `factor_exp_minus_3`; identity e^(z−m) = e^z · e^−m |
| B03 | "Twenty point one times that is exactly one" | TRUE in exact arithmetic (e³ · e^−3 = 1); shown value 1.000 | identity |
| B03 | Common factor cancels from numerator and denominator | TRUE (algebra; chapter §"The subtraction that changes nothing important") | chapter eq. |
| B03 | Ratios unchanged: 20.086/7.389 = 1.000/0.368 = 2.718 | TRUE (both = e) | computed in scene from evidence weights |
| B04 | `math.exp(1000)` raises OverflowError | TRUE on CPython 3.13.2 | `exp_1000_traceback_last_line` |
| B04 | exp(709) fits in a float, exp(710) does not | TRUE here (8.218e+307; OverflowError) | `exp_709`, `exp_710` |
| B04 | Shifted [1000, 1000] → [0,0] → [1,1] → [0.5, 0.5]; "exactly what the test asserts" | TRUE: test_02 uses `assertEqual(..., [0.5, 0.5])` | `cases.test_02.shifted`; `tests/test_main.py` |
| B04 | "the test passes" | TRUE: 6 tests, 0 failures, 0 errors | `lesson_tests` |
| B05 | [1001,1002,1003]: direct crashes; shifted gives the same −2,−1,0 and the same distribution | TRUE | `cases.offset` |
| B05 | "An offset shared by every score says nothing about which one is preferred. Softmax only listens to the gaps." | TRUE for softmax (shift invariance; the chapter says the offset "carries no information about their relative preference") | chapter §The subtraction… |
| B06 | True second probability of [0, −1000] ≈ 5 × 10^−435 | TRUE: e^−1000/(1+e^−1000) = 5.0760E-435 to shown precision | `true_exp_minus_1000` (Decimal, 30 digits) |
| B06 | "Python returns exactly zero, by either route" | TRUE: direct 0.0, main.py 0.0 | `cases.boundary` |
| B06 | Shown: exp(−745) = 5e−324, exp(−746) = 0.0 | TRUE on this machine | `exp_minus_745`, `exp_minus_746` |
| B06 | "the routes differ in the sixteenth decimal place" | TRUE: largest difference 1.11e−16 (outcome 2: …8218 vs …8219) | `chapter_direct_minus_shifted` |
| BVDT | Three findings | Restate B02–B06 | — |
| BHTF | Viewer prompt (no factual claim) | n/a. It asks for a prediction, then a run; I did not pre-run it for the viewer | — |

## Scope notes (what is NOT claimed)

- Nothing is claimed about NumPy/PyTorch (those return `inf`/`nan` rather than raising); the video says "math dot exp" and "Python".
- The boundary is illustrated with one constructed input, not a proof about all inputs.
- The temperature is 1 throughout (`main.py` default); the video doesn't discuss T ≠ 1.

## Corrections applied during the build

- Removed an on-screen "largest float ≈ 1.8e+308" label. It was true but not produced by `evidence.py`.
- Removed the spoken date from B00 so narration can't drift from the date of the evidence run.
